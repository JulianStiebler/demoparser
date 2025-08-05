#!/usr/bin/env python3
"""
Comprehensive code generator for demoparser2 dataclasses, enums, and schemas.
Automatically generates Python code based on actual demo data to ensure completeness.
Note: parse_ticks schema is manually maintained as demoparser_schema.
"""

import os
import sys
import traceback
from typing import Dict, Any, Optional
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

    def __init__(self, demo_path: str):
        self.demo_path = demo_path
        self.parser = DemoParser(demo_path)
        self.analysis_results = {}
    
    def analyze_demo(self) -> Dict[str, Any]:
        results = {
            'events': {},
            'server_cvars': set(),
            'server_cvars_stats': {},  # Added: detailed cvar analysis
            'header_fields': {},
            'grenades_schema': {},
            'voice_data_schema': {},
            'player_info_schema': {},
            'item_drops_schema': {},
            'skins_schema': {},
            'parsing_methods_available': [],  # Added: list of available methods
            'demo_metadata': {},  # Added: demo file metadata
            'analysis_summary': {}  # Added: high-level summary
            # Note: ticks_schema excluded - using manual demoparser_schema
        }
        
        # Analyze events
        print("Analyzing events...")
        events = self.parser.list_game_events()
        for event in events:
            try:
                df = self.parser.parse_event(event)
                if isinstance(df, pd.DataFrame) and not df.empty:
                    # Get comprehensive analysis but truncated
                    results['events'][event] = {
                        'columns': list(df.columns),
                        'dtypes': {col: str(dtype) for col, dtype in df.dtypes.items()},
                        'row_count': len(df),
                        'null_counts': {col: int(df[col].isnull().sum()) for col in df.columns},
                        'unique_counts': {col: int(df[col].nunique()) for col in df.columns},
                        'sample_data': df.head(3).to_dict(),  # First 3 rows
                        'data_ranges': self._get_data_ranges(df),
                        'column_stats': self._get_column_stats(df)
                    }
            except Exception as e:
                print(f"  ⚠️  Could not analyze event {event}: {e}")
                results['events'][event] = {
                    'error': str(e),
                    'columns': [],
                    'dtypes': {},
                    'row_count': 0
                }
        
        # Analyze server CVars
        print("Analyzing server CVars...")
        try:
            cvars = self.parser.list_updated_fields()
            results['server_cvars'] = set(cvars)
            
            # Enhanced CVars analysis
            results['server_cvars_stats'] = {
                'total_count': len(cvars),
                'by_prefix': self._analyze_cvar_prefixes(cvars),
                'sample_cvars': list(cvars)[:20]  # First 20 for sample
            }
        except Exception as e:
            print(f"  ⚠️  Could not analyze CVars: {e}")
            results['server_cvars_stats'] = {'error': str(e)}
        
        # Analyze header
        print("Analyzing header...")
        try:
            header = self.parser.parse_header()
            results['header_fields'] = header
        except Exception as e:
            print(f"  ⚠️  Could not analyze header: {e}")
        
        # Analyze other data structures (excluding parse_ticks)
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
                            'row_count': len(df),
                            'null_counts': {col: int(df[col].isnull().sum()) for col in df.columns},
                            'unique_counts': {col: int(df[col].nunique()) for col in df.columns},
                            'sample_data': df.head(3).to_dict(),  # First 3 rows
                            'data_ranges': self._get_data_ranges(df),
                            'column_stats': self._get_column_stats(df)
                        }
                    else:
                        results[result_key] = {
                            'columns': [],
                            'dtypes': {},
                            'row_count': 0,
                            'note': 'DataFrame is empty'
                        }
            except Exception as e:
                print(f"  ⚠️  Could not analyze {method_name}: {e}")
                results[result_key] = {
                    'error': str(e),
                    'columns': [],
                    'dtypes': {},
                    'row_count': 0
                }
        
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
        
        # Skip ticks analysis - using manual demoparser_schema
        print("Skipping ticks analysis - using manual demoparser_schema")
        
        # Add available parsing methods
        results['parsing_methods_available'] = [
            method for method in dir(self.parser) 
            if method.startswith('parse_') and callable(getattr(self.parser, method))
        ]
        
        # Add demo metadata
        try:
            import os
            results['demo_metadata'] = {
                'file_path': self.demo_path,
                'file_size_mb': round(os.path.getsize(self.demo_path) / (1024 * 1024), 2),
                'analysis_timestamp': pd.Timestamp.now().isoformat()
            }
        except Exception as e:
            results['demo_metadata'] = {'error': str(e)}
        
        # Create analysis summary
        results['analysis_summary'] = {
            'total_events': len(results['events']),
            'successful_events': len([e for e in results['events'].values() if 'error' not in e]),
            'failed_events': len([e for e in results['events'].values() if 'error' in e]),
            'total_server_cvars': len(results['server_cvars']),
            'header_fields_count': len(results['header_fields']),
            'parsing_methods_count': len(results['parsing_methods_available']),
            'schemas_generated': [k for k in results.keys() if k.endswith('_schema') and results[k]]
        }
        
        self.analysis_results = results
        return results
    
    def _analyze_cvar_prefixes(self, cvars: list) -> dict:
        """Analyze CVars by their prefixes."""
        prefixes = defaultdict(int)
        for cvar in cvars:
            if '_' in cvar:
                prefix = cvar.split('_')[0]
                prefixes[prefix] += 1
            else:
                prefixes['no_prefix'] += 1
        return dict(prefixes)
    
    def generate_enums_py(self) -> str:
        """Generate the complete enums.py file to match existing structure."""
        code = '''from enum import Enum

class Scope(Enum):
    PER_TICK: str = "PER_TICK"
    PER_ROUND: str = "PER_ROUND"
    GLOBAL: str = "GLOBAL"
    EVENT: str = "EVENT"

'''
        
        # Generate Event enum - match existing format exactly
        code += "class Event(Enum):\n"
        events = sorted(self.analysis_results.get('events', {}).keys())
        
        for event in events:
            # Convert event name to enum format
            enum_name = event.upper().replace('-', '_')
            code += f"    {enum_name}: str = '{event}'\n"
        
        code += '\n'
        
        # Generate ServerCVar enum - match existing comprehensive structure
        code += "class ServerCVar(Enum):\n"
        cvars = sorted(self.analysis_results.get('server_cvars', set()))
        
        # Add NA first (commonly found in existing)
        code += '    NA: str = "-"\n'
        code += '    net_tick: str = "net_tick"\n'
        
        # Group CVars by categories like in existing file
        basic_cvars = []
        prefixed_groups = defaultdict(list)
        
        for cvar in cvars:
            if cvar.startswith('m_'):
                # Player/entity properties
                if any(x in cvar for x in ['team', 'Team']):
                    prefixed_groups['team'].append(cvar)
                elif any(x in cvar for x in ['weapon', 'Weapon']):
                    prefixed_groups['weapon'].append(cvar)
                elif any(x in cvar for x in ['player', 'Player', 'Pawn']):
                    prefixed_groups['player'].append(cvar)
                else:
                    prefixed_groups['entity'].append(cvar)
            elif cvar.startswith('C'):
                # Class properties
                prefixed_groups['class'].append(cvar)
            else:
                basic_cvars.append(cvar)
        
        # Generate basic CVars
        for cvar in sorted(basic_cvars):
            safe_name = self._to_safe_enum_name(cvar)
            code += f'    {safe_name}: str = "{cvar}"\n'
        
        # Generate grouped CVars with comments
        for group_name in sorted(prefixed_groups.keys()):
            if prefixed_groups[group_name]:
                code += f'\n    # {group_name.title()} properties\n'
                for cvar in sorted(prefixed_groups[group_name]):
                    safe_name = self._to_safe_enum_name(cvar)
                    code += f'    {safe_name}: str = "{cvar}"\n'
        
        # Generate NType enum
        code += '''

class NType(Enum):
    CLIENT: str = "CLIENT"
    SERVER: str = "SERVER"
    OBSERVER: str = "OBSERVER"
    ENGINE: str = "ENGINE"
'''
        
        return code
    
    def generate_dataclass_py(self) -> str:
        """Generate the complete dataclass.py file to match existing structure."""
        code = '''from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

class DotSeparatedString(str):
    """
    A string that represents a dot-separated value.
    """
    @property
    def parts(self) -> list[str]:
        """Returns a list of strings split by the dot separator."""
        return self.split('.')

    def __repr__(self):
        return f"DotSeparatedString({super().__repr__()})"
    
'''
        
        # Generate Header dataclass - match existing structure exactly
        header_fields = self.analysis_results.get('header_fields', {})
        if header_fields:
            code += "@dataclass\nclass Header:\n"
            
            # Define fields in order (based on your existing structure)
            field_order = [
                'server_name', 'demo_file_stamp', 'network_protocol', 'map_name',
                'fullpackets_version', 'allow_clientside_entities', 
                'allow_clientside_particles', 'demo_version_name', 
                'demo_version_guid', 'client_name', 'game_directory', 'addons'
            ]
            
            for field_name in field_order:
                if field_name in header_fields:
                    if field_name == 'addons':
                        code += '    addons: DotSeparatedString = field(default_factory=DotSeparatedString)\n'
                    else:
                        field_type = self._infer_python_type(header_fields[field_name])
                        code += f'    {field_name}: {field_type}\n'
            
            # Add any missing fields
            for field_name, value in header_fields.items():
                if field_name not in field_order:
                    field_type = self._infer_python_type(value)
                    code += f'    {field_name}: {field_type}\n'
            
            code += '''
    @property
    def addons_list(self) -> List[str]:
        return self.addons.parts


'''
        
        # Generate VoiceData dataclass - match existing structure exactly
        voice_schema = self.analysis_results.get('voice_data_schema', {})
        if voice_schema:
            code += '''@dataclass
class VoiceData:
    """
    Container for voice data from parse_voice().
    Maps Steam IDs to voice audio bytes.
    """
    voice_clips: dict[str, bytes]  # steamid -> audio bytes
    
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

    def export_wav(self, steamid: str):
        try:
            import io
            from pydub import AudioSegment
        except ImportError:
            return

        clip_bytes = self.get_player_voice(steamid)
        if not clip_bytes:
            print(f"No voice data found for Steam ID: {steamid}")
            return

        try:
            audio_file = io.BytesIO(clip_bytes)
            audio_segment = AudioSegment.from_wav(audio_file)
            with open("test.wav", "wb") as temp_file:
                audio_segment.export(temp_file, format="wav")
            
        except Exception as e:
            print(f"Error playing audio for {steamid}: {e}")
'''
        
        
        # Generate dataclasses for parsing methods
        code += "# Auto-generated dataclasses for parsing methods\n\n"
        schema_mappings = {
            'player_info_schema': 'PlayerInfo',
            'grenades_schema': 'Grenade',
            'item_drops_schema': 'ItemDrop',
            'skins_schema': 'Skin'
        }
        
        for schema_key, class_name in schema_mappings.items():
            schema = self.analysis_results.get(schema_key, {})
            if schema and 'columns' in schema and schema['columns']:
                code += f"@dataclass\nclass {class_name}:\n"
                code += f'    """\n    Auto-generated dataclass for {schema_key.replace("_", " ").title()}.\n    """\n'
                
                # Add field definitions
                for col in schema['columns']:
                    dtype = schema.get('dtypes', {}).get(col, 'object')
                    python_type = self._map_dtype_to_python_type(dtype)
                    safe_field_name = self._to_safe_property_name(col)
                    description = self._generate_column_description(col, class_name)
                    
                    # Add comment with description
                    code += f'    {safe_field_name}: {python_type}  # {description}\n'
                
                code += '\n'
        
        # Generate dataclasses for events
        events = self.analysis_results.get('events', {})
        if events:
            code += "# Auto-generated dataclasses for events\n\n"
            for event_name, event_data in events.items():
                if 'columns' in event_data and event_data['columns']:
                    safe_class_name = self._to_safe_class_name(event_name) + "Event"
                    code += f"@dataclass\nclass {safe_class_name}:\n"
                    code += f'    """\n    Auto-generated dataclass for {event_name} event.\n    """\n'
                    
                    # Add field definitions
                    for col in event_data['columns']:
                        dtype = event_data.get('dtypes', {}).get(col, 'object')
                        python_type = self._map_dtype_to_python_type(dtype)
                        safe_field_name = self._to_safe_property_name(col)
                        description = self._generate_column_description(col, event_name)
                        
                        # Add comment with description
                        code += f'    {safe_field_name}: {python_type}  # {description}\n'
                    
                    code += '\n'
        
        return code
    
    def generate_schema_py(self) -> str:
        """Generate a complete schema.py file with only auto-generated schemas."""
        code = '''"""
Auto-generated Pandera schemas for demoparser2.
This file is automatically generated - do not edit manually.

Note: The main demoparser_schema for parse_ticks is located in props.py
"""

import pandera as pa
from pandera.typing import Series

'''
        
        # Generate schemas for main parsing methods
        schema_mappings = {
            'player_info_schema': 'PlayerInfoSchema',
            'grenades_schema': 'GrenadeSchema',
            'item_drops_schema': 'ItemDropSchema',
            'skins_schema': 'SkinSchema'
        }
        
        for schema_key, schema_name in schema_mappings.items():
            schema = self.analysis_results.get(schema_key, {})
            if schema and 'columns' in schema and schema['columns']:
                code += f"class {schema_name}(pa.DataFrameModel):\n"
                
                # Add column definitions
                for col in schema['columns']:
                    dtype = schema.get('dtypes', {}).get(col, 'object')
                    pandera_type, is_nullable = self._map_dtype_to_pandera_field(dtype)
                    description = self._generate_column_description(col, schema_name)
                    
                    # Properly format the pa.Field parameters
                    field_params = []
                    if is_nullable:
                        field_params.append("nullable=True")
                    field_params.append(f'description="{description}"')
                    
                    safe_col_name = self._to_safe_property_name(col)
                    field_params_str = ", ".join(field_params)
                    code += f'    {safe_col_name}: Series[{pandera_type}] = pa.Field({field_params_str})\n'
                
                code += '\n    class Config:\n'
                code += '        strict = True\n'
                code += '        coerce = True\n\n'
        
        # Generate event schemas
        events = self.analysis_results.get('events', {})
        if events:
            for event_name, event_data in events.items():
                if 'columns' in event_data and event_data['columns']:
                    safe_class_name = "Event" + self._to_safe_class_name(event_name) + "Schema"
                    code += f"class {safe_class_name}(pa.DataFrameModel):\n"
                    
                    # Add column definitions
                    for col in event_data['columns']:
                        dtype = event_data.get('dtypes', {}).get(col, 'object')
                        pandera_type, is_nullable = self._map_dtype_to_pandera_field(dtype)
                        description = self._generate_column_description(col, event_name)
                        
                        # Properly format the pa.Field parameters
                        field_params = []
                        if is_nullable:
                            field_params.append("nullable=True")
                        field_params.append(f'description="{description}"')
                        
                        safe_col_name = self._to_safe_property_name(col)
                        field_params_str = ", ".join(field_params)
                        code += f'    {safe_col_name}: Series[{pandera_type}] = pa.Field({field_params_str})\n'
                    
                    code += '\n    class Config:\n'
                    code += '        strict = True\n'
                    code += '        coerce = True\n\n'
        
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
    
    def _map_dtype_to_python_type(self, dtype_str: str) -> str:
        """Map pandas dtype to Python type for dataclasses."""
        dtype_str = str(dtype_str).lower()
        
        if 'int' in dtype_str:
            return "int"
        elif 'float' in dtype_str:
            return "float"
        elif 'bool' in dtype_str:
            return "bool"
        elif 'uint64' in dtype_str:
            return "int"  # Python int can handle uint64
        elif 'object' in dtype_str or 'string' in dtype_str:
            return "str"
        else:
            return "str"  # Default to str for unknown types

    def _map_dtype_to_pandera_field(self, dtype_str: str) -> tuple[str, bool]:
        """Map pandas dtype to Pandera field type and nullable status."""
        dtype_str = str(dtype_str).lower()
        
        # Handle nullable types
        is_nullable = False
        if 'object' in dtype_str:
            is_nullable = True
        
        if 'int' in dtype_str:
            if '64' in dtype_str:
                return "pa.Int64", is_nullable
            elif '32' in dtype_str:
                return "pa.Int32", is_nullable
            else:
                return "pa.Int32", is_nullable
        elif 'float' in dtype_str:
            if '64' in dtype_str:
                return "pa.Float64", is_nullable
            elif '32' in dtype_str:
                return "pa.Float32", is_nullable
            else:
                return "float", is_nullable
        elif 'bool' in dtype_str:
            return "bool", is_nullable
        elif 'uint64' in dtype_str:
            return "pa.UInt64", is_nullable
        elif 'object' in dtype_str or 'string' in dtype_str:
            return "str", True
        else:
            return "str", True
    
    def _generate_column_description(self, column_name: str, context: str) -> str:
        """Generate a descriptive string for a column based on its name and context."""
        # Common column descriptions
        descriptions = {
            'tick': 'Game tick when event occurred',
            'user_name': 'Player name',
            'user_steamid': 'Player Steam ID',
            'attacker_name': 'Attacker name',
            'attacker_steamid': 'Attacker Steam ID',
            'victim_name': 'Victim name',
            'victim_steamid': 'Victim Steam ID',
            'steamid': 'Player Steam ID',
            'name': 'Player name',
            'team_number': 'Team number',
            'X': 'X coordinate',
            'Y': 'Y coordinate',
            'Z': 'Z coordinate',
            'health': 'Player health',
            'armor': 'Player armor',
            'balance': 'Player money balance',
            'weapon': 'Weapon name',
            'item': 'Item name',
            'damage': 'Damage amount',
            'distance': 'Distance',
            'headshot': 'Whether it was a headshot',
            'flash_duration': 'Flash duration in seconds',
            'entity_id': 'Entity ID',
            'defindex': 'Item definition index',
            'paint_index': 'Paint/skin index',
            'paint_seed': 'Paint seed for pattern',
            'paint_wear': 'Wear value of the skin',
            'custom_name': 'Custom name tag'
        }
        
        # Check for exact matches first
        if column_name in descriptions:
            return descriptions[column_name]
        
        # Check for partial matches
        lower_col = column_name.lower()
        for key, desc in descriptions.items():
            if key.lower() in lower_col:
                return desc
        
        # Generate description based on column name patterns
        if 'time' in lower_col:
            return f"{column_name.replace('_', ' ').title()}"
        elif 'id' in lower_col:
            return f"{column_name.replace('_', ' ').title()}"
        elif 'is_' in lower_col:
            return f"Whether {column_name.replace('is_', '').replace('_', ' ')}"
        elif 'has_' in lower_col:
            return f"Whether player has {column_name.replace('has_', '').replace('_', ' ')}"
        elif 'num_' in lower_col or 'count' in lower_col:
            return f"Number of {column_name.replace('num_', '').replace('_', ' ')}"
        else:
            return column_name.replace('_', ' ').title()

    def _get_data_ranges(self, df: pd.DataFrame) -> dict:
        """Get data ranges for numeric columns (truncated)."""
        ranges = {}
        for col in df.columns:
            if df[col].dtype in ['int64', 'int32', 'float64', 'float32']:
                try:
                    min_val = df[col].min()
                    max_val = df[col].max()
                    mean_val = df[col].mean()
                    std_val = df[col].std()
                    
                    ranges[col] = {
                        'min': float(min_val) if not pd.isna(min_val) else "",
                        'max': float(max_val) if not pd.isna(max_val) else "",
                        'mean': float(mean_val) if not pd.isna(mean_val) else "",
                        'std': float(std_val) if not pd.isna(std_val) else ""
                    }
                except Exception:
                    ranges[col] = {'error': 'Could not compute stats'}
            elif df[col].dtype == 'object':
                # For string columns, show length stats
                try:
                    str_lengths = df[col].astype(str).str.len()
                    min_len = str_lengths.min()
                    max_len = str_lengths.max()
                    avg_len = str_lengths.mean()
                    
                    ranges[col] = {
                        'min_length': int(min_len) if not pd.isna(min_len) else "",
                        'max_length': int(max_len) if not pd.isna(max_len) else "",
                        'avg_length': float(avg_len) if not pd.isna(avg_len) else ""
                    }
                except Exception:
                    ranges[col] = {'error': 'Could not compute string stats'}
        return ranges
    
    def _get_column_stats(self, df: pd.DataFrame) -> dict:
        """Get additional column statistics (truncated)."""
        stats = {}
        for col in df.columns:
            try:
                count_val = df[col].count()
                null_sum = df[col].isnull().sum()
                null_percentage = (null_sum / len(df)) * 100 if len(df) > 0 else 0
                
                col_stats = {
                    'dtype': str(df[col].dtype),
                    'non_null_count': int(count_val) if not pd.isna(count_val) else 0,
                    'null_percentage': float(null_percentage) if not pd.isna(null_percentage) else ""
                }
                
                # Add unique values for categorical-like columns (limited to first 10)
                if df[col].nunique() <= 20:  # Only for low-cardinality columns
                    unique_vals = df[col].value_counts().head(10).to_dict()
                    # Handle NaN values in the value counts
                    col_stats['top_values'] = {
                        str(k) if not pd.isna(k) else "": int(v) if not pd.isna(v) else 0 
                        for k, v in unique_vals.items()
                    }
                else:
                    col_stats['top_values'] = f"Too many unique values ({df[col].nunique()})"
                
                stats[col] = col_stats
            except Exception as e:
                stats[col] = {'error': str(e)}
        return stats

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
    
    def _make_json_serializable(self, obj):
        """Recursively convert an object to be JSON serializable, handling NaN values."""
        import math
        
        if isinstance(obj, dict):
            return {key: self._make_json_serializable(value) for key, value in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [self._make_json_serializable(item) for item in obj]
        elif isinstance(obj, set):
            return [self._make_json_serializable(item) for item in obj]
        elif isinstance(obj, float):
            if math.isnan(obj):
                return ""  # Convert NaN to empty string
            elif math.isinf(obj):
                return "inf" if obj > 0 else "-inf"  # Handle infinity
            else:
                return obj
        elif pd.isna(obj):  # Handle pandas NA values
            return ""
        else:
            return obj
    
    def generate_all_files(self, output_dir: Optional[str] = None) -> None:
        """Generate all files and save them."""
        print("🚀 Starting code generation...")
        
        # Use the directory where this script is located if no output_dir specified
        if output_dir is None:
            output_dir = os.path.dirname(os.path.abspath(__file__))
        
        print(f"📁 Output directory: {output_dir}")
        
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
        
        # Generate complete schema.py (auto-generated schemas only)
        print("Generating schema.py...")
        schema_code = self.generate_schema_py()
        schema_path = os.path.join(output_dir, "schema.py")
        
        # Overwrite schema.py with only auto-generated schemas
        with open(schema_path, "w") as f:
            f.write(schema_code)
        print("✅ Generated clean schema.py with auto-generated schemas only")
        print("   Note: The main demoparser_schema is located in props.py")
        
        # Save analysis results
        analysis_file = os.path.join(output_dir, "analysis_results.json")
        with open(analysis_file, "w") as f:
            # Convert sets to lists and handle NaN values for JSON serialization
            serializable_results = self._make_json_serializable(self.analysis_results)
            json.dump(serializable_results, f, indent=2, default=str)
        print(f"✅ Saved analysis results to {analysis_file}")
        
        print(f"\n🎉 Code generation complete! Generated files in {output_dir}/")
        print("📊 Analysis summary:")
        print(f"  - Events: {len(self.analysis_results.get('events', {}))}")
        print(f"  - Server CVars: {len(self.analysis_results.get('server_cvars', set()))}")
        print(f"  - Header fields: {len(self.analysis_results.get('header_fields', {}))}")
        print("\n💡 Note: The main demoparser_schema for parse_ticks is located in props.py")
        print("📝 Generated clean schema.py with only auto-generated schemas")


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
