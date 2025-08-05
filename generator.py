#!/usr/bin/env python3
"""
Comprehensive code generator for demoparser2 dataclasses, enums, and schemas.
Automatically generates Python code based on actual demo data to ensure completeness.
"""

import os
import sys
import traceback
from typing import Dict, Any, Set, List, Optional
import pandas as pd
import json
from collections import defaultdict
import re

try:
    from demoparser2 import DemoParser
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure demoparser2 is properly installed")
    sys.exit(1)


class DemoParserCodeGenerator:
    """Generates Python code for dataclasses, enums, and schemas based on demo data."""
    
    def __init__(self, demo_path: str):
        self.demo_path = demo_path
        self.parser = DemoParser(demo_path)
        self.analysis_results = {}
    
    def analyze_demo(self) -> Dict[str, Any]:
        """Analyze the demo file to extract all possible schemas and enums."""
        print("🔍 Analyzing demo file for code generation...")
        
        results = {
            'events': {},
            'server_cvars': set(),
            'header_fields': {},
            'grenades_schema': {},
            'voice_data_schema': {},
            'player_info_schema': {},
            'item_drops_schema': {},
            'skins_schema': {},
            'ticks_schema': {}
        }
        
        # Analyze events
        print("Analyzing events...")
        events = self.parser.list_game_events()
        for event in events:
            try:
                df = self.parser.parse_event(event)
                if isinstance(df, pd.DataFrame) and not df.empty:
                    results['events'][event] = {
                        'columns': list(df.columns),
                        'dtypes': {col: str(dtype) for col, dtype in df.dtypes.items()},
                        'sample_data': df.head(2).to_dict()
                    }
            except Exception as e:
                print(f"  ⚠️  Could not analyze event {event}: {e}")
        
        # Analyze server CVars
        print("Analyzing server CVars...")
        try:
            cvars = self.parser.list_updated_fields()
            results['server_cvars'] = set(cvars)
        except Exception as e:
            print(f"  ⚠️  Could not analyze CVars: {e}")
        
        # Analyze header
        print("Analyzing header...")
        try:
            header = self.parser.parse_header()
            results['header_fields'] = header
        except Exception as e:
            print(f"  ⚠️  Could not analyze header: {e}")
        
        # Analyze other data structures
        for method_name, result_key in [
            ('parse_grenades', 'grenades_schema'),
            ('parse_player_info', 'player_info_schema'),
            ('parse_item_drops', 'item_drops_schema'),
            ('parse_skins', 'skins_schema')
        ]:
            print(f"Analyzing {method_name}...")
            try:
                if hasattr(self.parser, method_name):
                    df = getattr(self.parser, method_name)()
                    if isinstance(df, pd.DataFrame) and not df.empty:
                        results[result_key] = {
                            'columns': list(df.columns),
                            'dtypes': {col: str(dtype) for col, dtype in df.dtypes.items()},
                            'sample_data': df.head(2).to_dict()
                        }
            except Exception as e:
                print(f"  ⚠️  Could not analyze {method_name}: {e}")
        
        # Analyze voice data
        print("Analyzing voice data...")
        try:
            if hasattr(self.parser, 'parse_voice'):
                voice_data = self.parser.parse_voice()
                if voice_data:
                    results['voice_data_schema'] = {
                        'type': 'dict',
                        'key_type': 'steamid (str)',
                        'value_type': 'audio bytes',
                        'sample_keys': list(voice_data.keys())[:3]
                    }
        except Exception as e:
            print(f"  ⚠️  Could not analyze voice data: {e}")
        
        # Analyze ticks with common props
        print("Analyzing ticks...")
        try:
            available_props = list(results['server_cvars'])[:5]  # Use first 5 CVars
            if available_props:
                df = self.parser.parse_ticks(available_props)
                if isinstance(df, pd.DataFrame) and not df.empty:
                    results['ticks_schema'] = {
                        'columns': list(df.columns),
                        'dtypes': {col: str(dtype) for col, dtype in df.dtypes.items()},
                        'sample_data': df.head(2).to_dict()
                    }
        except Exception as e:
            print(f"  ⚠️  Could not analyze ticks: {e}")
        
        self.analysis_results = results
        return results
    
    def generate_enums_py(self) -> str:
        """Generate the complete enums.py file."""
        code = '''from enum import Enum

class Scope(Enum):
    PER_TICK: str = "PER_TICK"
    PER_ROUND: str = "PER_ROUND"
    GLOBAL: str = "GLOBAL"
    EVENT: str = "EVENT"

'''
        
        # Generate Event enum
        code += "class Event(Enum):\n"
        events = sorted(self.analysis_results.get('events', {}).keys())
        for event in events:
            safe_name = self._to_safe_enum_name(event.upper())
            code += f'    {safe_name}: str = \'{event}\'\n'
        code += '\n'
        
        # Generate ServerCVar enum
        code += "class ServerCVar(Enum):\n"
        cvars = sorted(self.analysis_results.get('server_cvars', set()))
        
        # Group CVars by prefix for better organization
        cvar_groups = defaultdict(list)
        for cvar in cvars:
            if '.' in cvar:
                prefix = cvar.split('.')[0]
                cvar_groups[prefix].append(cvar)
            else:
                cvar_groups['basic'].append(cvar)
        
        # Generate basic CVars first
        if 'basic' in cvar_groups:
            code += "    # Basic CVars\n"
            for cvar in sorted(cvar_groups['basic']):
                safe_name = self._to_safe_enum_name(cvar)
                code += f'    {safe_name}: str = "{cvar}"\n'
            code += '\n'
        
        # Generate prefixed CVars
        for prefix in sorted(cvar_groups.keys()):
            if prefix == 'basic':
                continue
            code += f"    # {prefix} prefixed CVars\n"
            for cvar in sorted(cvar_groups[prefix]):
                safe_name = self._to_safe_enum_name(cvar)
                code += f'    {safe_name}: str = "{cvar}"\n'
            code += '\n'
        
        # Generate NType enum (if needed)
        code += '''
class NType(Enum):
    CLIENT: str = "CLIENT"
    SERVER: str = "SERVER"
    OBSERVER: str = "OBSERVER"
    ENGINE: str = "ENGINE"
'''
        
        return code
    
    def generate_dataclass_py(self) -> str:
        """Generate the complete dataclass.py file."""
        code = '''from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Union
import pandas as pd

class DotSeparatedString(str):
    """
    A string that represents a dot-separated value.
    """
    @property
    def parts(self) -> List[str]:
        """Returns a list of strings split by the dot separator."""
        return self.split('.')

    def __repr__(self):
        return f"DotSeparatedString({super().__repr__()})"

'''
        
        # Generate Header dataclass
        header_fields = self.analysis_results.get('header_fields', {})
        if header_fields:
            code += "@dataclass\nclass Header:\n"
            for field_name, value in header_fields.items():
                field_type = self._infer_python_type(value)
                if field_name == 'addons':
                    code += f'    {field_name}: DotSeparatedString = field(default_factory=DotSeparatedString)\n'
                else:
                    code += f'    {field_name}: {field_type}\n'
            
            code += '''
    @property
    def addons_list(self) -> List[str]:
        return self.addons.parts

'''
        
        # Generate VoiceData dataclass
        voice_schema = self.analysis_results.get('voice_data_schema', {})
        if voice_schema:
            code += '''@dataclass
class VoiceData:
    """
    Container for voice data from parse_voice().
    Maps Steam IDs to voice audio bytes.
    """
    voice_clips: Dict[str, bytes]  # steamid -> audio bytes
    
    @property
    def player_count(self) -> int:
        """Number of players with voice data."""
        return len(self.voice_clips)
    
    @property
    def player_ids(self) -> List[str]:
        """List of Steam IDs with voice data."""
        return list(self.voice_clips.keys())
    
    @property
    def total_audio_size(self) -> int:
        """Total size of all voice clips in bytes."""
        return sum(len(clip) for clip in self.voice_clips.values())
    
    def get_player_voice(self, steamid: str) -> Optional[bytes]:
        """Get voice data for a specific player."""
        return self.voice_clips.get(steamid)
    
    def has_voice_data(self, steamid: str) -> bool:
        """Check if player has voice data."""
        return steamid in self.voice_clips

'''
        
        # Generate dataclasses for other schemas
        schema_mappings = {
            'grenades_schema': 'GrenadesData',
            'player_info_schema': 'PlayerInfoData',
            'item_drops_schema': 'ItemDropsData',
            'skins_schema': 'SkinsData',
            'ticks_schema': 'TicksData'
        }
        
        for schema_key, class_name in schema_mappings.items():
            schema = self.analysis_results.get(schema_key, {})
            if schema and 'columns' in schema:
                code += f"@dataclass\nclass {class_name}:\n"
                code += f'    """\n    Auto-generated dataclass for {schema_key.replace("_", " ").title()}.\n    """\n'
                code += "    data: pd.DataFrame\n\n"
                
                # Add property methods for easy access to columns
                for col in schema['columns']:
                    safe_prop_name = self._to_safe_property_name(col)
                    code += f'    @property\n'
                    code += f'    def {safe_prop_name}(self) -> pd.Series:\n'
                    code += f'        """Access {col} column."""\n'
                    code += f'        return self.data["{col}"]\n\n'
        
        return code
    
    def generate_schema_py(self) -> str:
        """Generate schema.py with Pandera schemas."""
        code = '''from typing import Optional
from dataclasses import dataclass
import pandera as pa
from pandera.typing import Series
import pandas as pd

from .enums import ServerCVar, Scope, NType

'''
        
        # Generate schemas for each data structure
        schema_mappings = {
            'grenades_schema': 'GrenadesSchema',
            'player_info_schema': 'PlayerInfoSchema', 
            'item_drops_schema': 'ItemDropsSchema',
            'skins_schema': 'SkinsSchema',
            'ticks_schema': 'TicksSchema'
        }
        
        for schema_key, schema_name in schema_mappings.items():
            schema = self.analysis_results.get(schema_key, {})
            if schema and 'columns' in schema:
                code += f"class {schema_name}(pa.SchemaModel):\n"
                code += f'    """\n    Auto-generated Pandera schema for {schema_key.replace("_", " ").title()}.\n    """\n'
                
                for col in schema['columns']:
                    dtype = schema.get('dtypes', {}).get(col, 'object')
                    pandera_type = self._map_dtype_to_pandera(dtype)
                    safe_col_name = self._to_safe_property_name(col)
                    code += f'    {safe_col_name}: Series[{pandera_type}] = pa.Field(alias="{col}")\n'
                
                code += '\n    class Config:\n'
                code += '        strict = False  # Allow extra columns\n\n'
        
        # Generate event schemas
        events = self.analysis_results.get('events', {})
        if events:
            code += "# Event Schemas\n"
            for event_name, event_data in events.items():
                if 'columns' in event_data:
                    safe_class_name = self._to_safe_class_name(event_name) + "Schema"
                    code += f"class {safe_class_name}(pa.SchemaModel):\n"
                    code += f'    """\n    Schema for {event_name} event.\n    """\n'
                    
                    for col in event_data['columns']:
                        dtype = event_data.get('dtypes', {}).get(col, 'object')
                        pandera_type = self._map_dtype_to_pandera(dtype)
                        safe_col_name = self._to_safe_property_name(col)
                        code += f'    {safe_col_name}: Series[{pandera_type}] = pa.Field(alias="{col}")\n'
                    
                    code += '\n    class Config:\n'
                    code += '        strict = False\n\n'
        
        return code
    
    def _to_safe_enum_name(self, name: str) -> str:
        """Convert a string to a safe Python enum name."""
        # Replace problematic characters
        safe = name.replace(".", "_").replace("[", "_").replace("]", "_").replace(" ", "_").replace("+", "plus").replace("-", "_")
        # Remove multiple underscores
        while "__" in safe:
            safe = safe.replace("__", "_")
        # Remove leading/trailing underscores
        safe = safe.strip("_")
        # Ensure it starts with a letter
        if safe and safe[0].isdigit():
            safe = "N" + safe
        return safe or "UNKNOWN"
    
    def _to_safe_property_name(self, name: str) -> str:
        """Convert a string to a safe Python property name."""
        safe = re.sub(r'[^a-zA-Z0-9_]', '_', name)
        safe = re.sub(r'_+', '_', safe)
        safe = safe.strip('_')
        if safe and safe[0].isdigit():
            safe = "prop_" + safe
        return safe or "unknown"
    
    def _to_safe_class_name(self, name: str) -> str:
        """Convert a string to a safe Python class name."""
        # Split by common separators and capitalize each part
        parts = re.split(r'[^a-zA-Z0-9]', name)
        safe = ''.join(part.capitalize() for part in parts if part)
        if safe and safe[0].isdigit():
            safe = "Event" + safe
        return safe or "Unknown"
    
    def _infer_python_type(self, value: Any) -> str:
        """Infer Python type annotation from a value."""
        if isinstance(value, bool):
            return "bool"
        elif isinstance(value, int):
            return "int"
        elif isinstance(value, float):
            return "float"
        elif isinstance(value, str):
            return "str"
        elif isinstance(value, list):
            return "List[Any]"
        elif isinstance(value, dict):
            return "Dict[str, Any]"
        else:
            return "Any"
    
    def _map_dtype_to_pandera(self, dtype: str) -> str:
        """Map pandas dtype to Pandera type."""
        dtype_mapping = {
            'int64': 'int',
            'int32': 'int', 
            'float64': 'float',
            'float32': 'float',
            'object': 'str',
            'bool': 'bool',
            'datetime64[ns]': 'pd.Timestamp'
        }
        return dtype_mapping.get(dtype, 'Any')
    
    def generate_all_files(self, output_dir: str = "src/python/src") -> None:
        """Generate all files and save them."""
        print("🚀 Starting code generation...")
        
        # Analyze demo first
        self.analyze_demo()
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate enums.py
        print("Generating enums.py...")
        enums_code = self.generate_enums_py()
        with open(os.path.join(output_dir, "enums.py"), "w") as f:
            f.write(enums_code)
        print("✅ Generated enums.py")
        
        # Generate dataclass.py
        print("Generating dataclass.py...")
        dataclass_code = self.generate_dataclass_py()
        with open(os.path.join(output_dir, "dataclass.py"), "w") as f:
            f.write(dataclass_code)
        print("✅ Generated dataclass.py")
        
        # Generate schema.py
        print("Generating schema.py...")
        schema_code = self.generate_schema_py()
        with open(os.path.join(output_dir, "schema.py"), "w") as f:
            f.write(schema_code)
        print("✅ Generated schema.py")
        
        # Save analysis results
        analysis_file = os.path.join(output_dir, "analysis_results.json")
        with open(analysis_file, "w") as f:
            # Convert sets to lists for JSON serialization
            serializable_results = {}
            for key, value in self.analysis_results.items():
                if isinstance(value, set):
                    serializable_results[key] = list(value)
                else:
                    serializable_results[key] = value
            json.dump(serializable_results, f, indent=2, default=str)
        print(f"✅ Saved analysis results to {analysis_file}")
        
        print(f"\n🎉 Code generation complete! Generated files in {output_dir}/")
        print(f"📊 Analysis summary:")
        print(f"  - Events: {len(self.analysis_results.get('events', {}))}")
        print(f"  - Server CVars: {len(self.analysis_results.get('server_cvars', set()))}")
        print(f"  - Header fields: {len(self.analysis_results.get('header_fields', {}))}")


def main():
    """Main function to run the code generator."""
    # Look for demo file
    demo_files = ['dem.dem', 'test_demo.dem']
    demo_path = None
    
    for demo_file in demo_files:
        if os.path.exists(demo_file):
            demo_path = demo_file
            break
    
    if not demo_path:
        print("❌ No demo file found. Please ensure 'dem.dem' or 'test_demo.dem' exists.")
        return
    
    print(f"Using demo file: {demo_path}")
    
    try:
        generator = DemoParserCodeGenerator(demo_path)
        generator.generate_all_files()
        
    except Exception as e:
        print(f"❌ Code generation failed with error: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    main()
