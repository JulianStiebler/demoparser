#!/usr/bin/env python3
"""
Comprehensive validation and code generation script for demoparser2.
Tests all parser methods against actual demo data and can generate complete schemas.
"""

import os
import sys
import traceback
from typing import Dict, Any
import pandas as pd
import json
from collections import defaultdict
import re

try:
    from demoparser2 import DemoParser
    from src.python.src.enums import Event, ServerCVar
    from src.python.src.dataclass import VoiceData, DotSeparatedString
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure the package is properly installed and paths are correct")
    sys.exit(1)


class DemoParserValidator:
    """Comprehensive validator for demoparser2 schemas and enums."""
    
    def __init__(self, demo_path: str):
        self.demo_path = demo_path
        self.parser = DemoParser(demo_path)
        self.validation_results = {
            'header': {'status': 'pending', 'issues': []},
            'events': {'status': 'pending', 'issues': [], 'missing_events': [], 'extra_events': []},
            'event_schemas': {'status': 'pending', 'issues': []},
            'server_cvars': {'status': 'pending', 'issues': [], 'missing_cvars': [], 'extra_cvars': []},
            'grenades': {'status': 'pending', 'issues': []},
            'voice_data': {'status': 'pending', 'issues': []},
            'player_info': {'status': 'pending', 'issues': []},
            'item_drops': {'status': 'pending', 'issues': []},
            'skins': {'status': 'pending', 'issues': []},
            'ticks': {'status': 'pending', 'issues': []}
        }
        self.analysis_data = {}  # Store analysis data for code generation
    
    def validate_header(self) -> bool:
        """Validate Header dataclass against actual header data."""
        print("\n=== Validating Header Dataclass ===")
        try:
            header_data = self.parser.parse_header()
            print(f"Parsed header fields: {list(header_data.keys())}")
            
            # Expected fields from Header dataclass
            expected_fields = {
                'server_name', 'demo_file_stamp', 'network_protocol', 'map_name',
                'fullpackets_version', 'allow_clientside_entities', 'allow_clientside_particles',
                'demo_version_name', 'demo_version_guid', 'client_name', 'game_directory', 'addons'
            }
            
            actual_fields = set(header_data.keys())
            missing_fields = expected_fields - actual_fields
            extra_fields = actual_fields - expected_fields
            
            if missing_fields:
                self.validation_results['header']['issues'].append(f"Missing fields in Header dataclass: {missing_fields}")
                print(f"❌ Missing fields: {missing_fields}")
            
            if extra_fields:
                self.validation_results['header']['issues'].append(f"Extra fields not in Header dataclass: {extra_fields}")
                print(f"⚠️  Extra fields found: {extra_fields}")
            
            # Test DotSeparatedString functionality
            addons_value = header_data.get('addons', '')
            if addons_value:
                dot_string = DotSeparatedString(addons_value)
                print(f"Addons as DotSeparatedString: {dot_string}")
                print(f"Addons parts: {dot_string.parts}")
            
            if not missing_fields and not extra_fields:
                print("✅ Header dataclass validation passed")
                self.validation_results['header']['status'] = 'passed'
                return True
            else:
                self.validation_results['header']['status'] = 'failed'
                return False
                
        except Exception as e:
            error_msg = f"Header validation failed: {str(e)}"
            print(f"❌ {error_msg}")
            self.validation_results['header']['issues'].append(error_msg)
            self.validation_results['header']['status'] = 'error'
            return False
    
    def validate_events_enum(self) -> bool:
        """Validate Event enum against actual game events in demo."""
        print("\n=== Validating Event Enum ===")
        try:
            actual_events = set(self.parser.list_game_events())
            print(f"Found {len(actual_events)} events in demo")
            
            # Get all events from enum
            enum_events = {event.value for event in Event}
            print(f"Event enum contains {len(enum_events)} events")
            
            missing_events = actual_events - enum_events
            extra_events = enum_events - actual_events
            
            if missing_events:
                print(f"❌ Events in demo but missing from enum: {sorted(missing_events)}")
                self.validation_results['events']['missing_events'] = list(missing_events)
                self.validation_results['events']['issues'].append(f"Missing {len(missing_events)} events from enum")
            
            if extra_events:
                print(f"⚠️  Events in enum but not found in demo: {sorted(extra_events)}")
                self.validation_results['events']['extra_events'] = list(extra_events)
                # This might be OK - demo might not contain all possible events
            
            print(f"✅ Found {len(actual_events & enum_events)} matching events")
            
            if not missing_events:
                self.validation_results['events']['status'] = 'passed'
                return True
            else:
                self.validation_results['events']['status'] = 'failed'
                return False
                
        except Exception as e:
            error_msg = f"Events enum validation failed: {str(e)}"
            print(f"❌ {error_msg}")
            self.validation_results['events']['issues'].append(error_msg)
            self.validation_results['events']['status'] = 'error'
            return False
    
    def validate_event_schemas(self) -> bool:
        """Test parsing all events to validate field schemas."""
        print("\n=== Validating Event Schemas ===")
        try:
            actual_events = self.parser.list_game_events()
            issues_found = []
            
            for i, event_name in enumerate(actual_events[:10]):  # Test first 10 events
                print(f"Testing event {i+1}/{min(10, len(actual_events))}: {event_name}")
                try:
                    df = self.parser.parse_event(event_name)
                    if isinstance(df, pd.DataFrame) and not df.empty:
                        columns = list(df.columns)
                        print(f"  ✅ {event_name}: {len(df)} rows, columns: {columns}")
                        
                        # Check for common required columns
                        expected_base_columns = {'tick'}  # Most events should have tick
                        missing_base = expected_base_columns - set(columns)
                        if missing_base:
                            issues_found.append(f"{event_name} missing base columns: {missing_base}")
                    else:
                        print(f"  ⚠️  {event_name}: No data or empty DataFrame")
                        
                except Exception as event_error:
                    error_msg = f"Failed to parse {event_name}: {str(event_error)}"
                    print(f"  ❌ {error_msg}")
                    issues_found.append(error_msg)
            
            # Test parsing multiple events at once
            print("\nTesting multiple events parsing...")
            try:
                events_list = actual_events[:5]  # Test first 5 events
                multi_result = self.parser.parse_events(events_list)
                print(f"✅ Successfully parsed {len(multi_result)} events in batch")
                
                for event_name, df in multi_result:
                    if isinstance(df, pd.DataFrame):
                        print(f"  {event_name}: {len(df)} rows")
                    
            except Exception as multi_error:
                error_msg = f"Multiple events parsing failed: {str(multi_error)}"
                print(f"❌ {error_msg}")
                issues_found.append(error_msg)
            
            self.validation_results['event_schemas']['issues'] = issues_found
            
            if not issues_found:
                print("✅ Event schemas validation passed")
                self.validation_results['event_schemas']['status'] = 'passed'
                return True
            else:
                print(f"⚠️  Found {len(issues_found)} issues with event schemas")
                self.validation_results['event_schemas']['status'] = 'partial'
                return False
                
        except Exception as e:
            error_msg = f"Event schemas validation failed: {str(e)}"
            print(f"❌ {error_msg}")
            self.validation_results['event_schemas']['issues'].append(error_msg)
            self.validation_results['event_schemas']['status'] = 'error'
            return False
    
    def validate_server_cvars(self) -> bool:
        """Validate ServerCVar enum against actual updated fields."""
        print("\n=== Validating ServerCVar Enum ===")
        try:
            actual_fields = set(self.parser.list_updated_fields())
            print(f"Found {len(actual_fields)} updated fields in demo")
            
            # Get all server cvars from enum
            enum_cvars = {cvar.value for cvar in ServerCVar}
            print(f"ServerCVar enum contains {len(enum_cvars)} cvars")
            
            missing_cvars = actual_fields - enum_cvars
            extra_cvars = enum_cvars - actual_fields
            
            if missing_cvars:
                print("❌ Fields in demo but missing from ServerCVar enum:")
                print(f"Found {len(missing_cvars)} missing CVars")
                self.validation_results['server_cvars']['missing_cvars'] = list(missing_cvars)
                self.validation_results['server_cvars']['issues'].append(f"Missing {len(missing_cvars)} cvars from enum")
                
                # Output in format ready to paste into enum
                print("\n" + "="*80)
                print("MISSING CVARS - READY TO PASTE INTO ENUM:")
                print("="*80)
                
                missing_sorted = sorted(missing_cvars)
                for cvar in missing_sorted:
                    # Convert to valid Python identifier
                    # Replace dots with underscores, brackets with underscores, etc.
                    enum_name = cvar.replace(".", "_").replace("[", "_").replace("]", "_").replace(" ", "_").replace("+", "plus")
                    # Remove any double underscores
                    while "__" in enum_name:
                        enum_name = enum_name.replace("__", "_")
                    # Remove leading/trailing underscores
                    enum_name = enum_name.strip("_")
                    
                    print(f'    {enum_name}: str = "{cvar}"')
                
                print("="*80)
                print(f"Total: {len(missing_cvars)} missing CVars formatted above")
                print("="*80)
            
            if extra_cvars:
                print(f"⚠️  CVars in enum but not found in demo: {len(extra_cvars)} items")
                self.validation_results['server_cvars']['extra_cvars'] = list(extra_cvars)
            
            print(f"✅ Found {len(actual_fields & enum_cvars)} matching cvars")
            
            if not missing_cvars:
                self.validation_results['server_cvars']['status'] = 'passed'
                return True
            else:
                self.validation_results['server_cvars']['status'] = 'failed'
                return False
                
        except Exception as e:
            error_msg = f"ServerCVar validation failed: {str(e)}"
            print(f"❌ {error_msg}")
            self.validation_results['server_cvars']['issues'].append(error_msg)
            self.validation_results['server_cvars']['status'] = 'error'
            return False
    
    def validate_grenades(self) -> bool:
        """Validate grenades parsing and schema."""
        print("\n=== Validating Grenades ===")
        try:
            grenades_df = self.parser.parse_grenades()
            
            if isinstance(grenades_df, pd.DataFrame) and not grenades_df.empty:
                columns = list(grenades_df.columns)
                print(f"✅ Grenades: {len(grenades_df)} rows")
                print(f"Actual columns: {columns}")
                
                # Check expected columns based on documentation and common usage
                expected_columns = {'tick', 'thrower_steamid'}  # These are commonly expected
                actual_columns_set = set(columns)
                missing_columns = expected_columns - actual_columns_set
                
                # Check for coordinate columns (X, Y, Z are mentioned in docstring)
                coordinate_columns = {'X', 'Y', 'Z'}
                missing_coordinates = coordinate_columns - actual_columns_set
                
                if missing_columns:
                    self.validation_results['grenades']['issues'].append(f"Missing expected columns: {missing_columns}")
                    print(f"❌ Missing expected columns: {missing_columns}")
                
                if missing_coordinates:
                    self.validation_results['grenades']['issues'].append(f"Missing coordinate columns: {missing_coordinates}")
                    print(f"❌ Missing coordinate columns: {missing_coordinates}")
                
                # Check grenade types
                if 'grenade_type' in grenades_df.columns:
                    grenade_types = grenades_df['grenade_type'].unique()
                    print(f"Found grenade types: {list(grenade_types)}")
                else:
                    print("⚠️  No 'grenade_type' column found")
                
                # Show sample of data
                print("Sample data:")
                print(grenades_df.head(3).to_string())
                
                if not missing_columns and not missing_coordinates:
                    self.validation_results['grenades']['status'] = 'passed'
                    return True
                else:
                    self.validation_results['grenades']['status'] = 'failed'
                    return False
            else:
                print("⚠️  No grenades data found")
                self.validation_results['grenades']['status'] = 'no_data'
                return True
                
        except Exception as e:
            error_msg = f"Grenades validation failed: {str(e)}"
            print(f"❌ {error_msg}")
            self.validation_results['grenades']['issues'].append(error_msg)
            self.validation_results['grenades']['status'] = 'error'
            return False
    
    def validate_voice_data(self) -> bool:
        """Validate voice data parsing and VoiceData dataclass."""
        print("\n=== Validating Voice Data ===")
        try:
            # Check if voice feature is available
            if not hasattr(self.parser, 'parse_voice'):
                print("⚠️  Voice parsing not available (feature not enabled)")
                self.validation_results['voice_data']['status'] = 'not_available'
                return True
            
            voice_data_dict = self.parser.parse_voice()
            
            if voice_data_dict:
                print(f"✅ Voice data: {len(voice_data_dict)} players")
                
                # Test VoiceData dataclass
                voice_data = VoiceData(voice_clips=voice_data_dict)
                print(f"Player count: {voice_data.player_count}")
                print(f"Player IDs: {voice_data.player_ids}")
                print(f"Total audio size: {voice_data.total_audio_size} bytes")
                
                # Test methods
                for steamid in voice_data.player_ids[:3]:  # Test first 3 players
                    has_voice = voice_data.has_voice_data(steamid)
                    voice_clip = voice_data.get_player_voice(steamid)
                    print(f"  Player {steamid}: has_voice={has_voice}, clip_size={len(voice_clip) if voice_clip else 0}")
                
                self.validation_results['voice_data']['status'] = 'passed'
                return True
            else:
                print("⚠️  No voice data found in demo")
                self.validation_results['voice_data']['status'] = 'no_data'
                return True
                
        except Exception as e:
            error_msg = f"Voice data validation failed: {str(e)}"
            print(f"❌ {error_msg}")
            self.validation_results['voice_data']['issues'].append(error_msg)
            self.validation_results['voice_data']['status'] = 'error'
            return False
    
    def validate_other_methods(self) -> bool:
        """Validate other parsing methods."""
        print("\n=== Validating Other Parser Methods ===")
        
        methods_to_test = [
            ('player_info', 'parse_player_info'),
            ('item_drops', 'parse_item_drops'), 
            ('skins', 'parse_skins')
        ]
        
        all_passed = True
        
        for method_name, parser_method in methods_to_test:
            try:
                print(f"\nTesting {method_name}...")
                if hasattr(self.parser, parser_method):
                    result = getattr(self.parser, parser_method)()
                    
                    if isinstance(result, pd.DataFrame):
                        print(f"✅ {method_name}: {len(result)} rows, columns: {list(result.columns)}")
                        self.validation_results[method_name]['status'] = 'passed'
                    else:
                        print(f"⚠️  {method_name}: Unexpected result type: {type(result)}")
                        self.validation_results[method_name]['status'] = 'warning'
                else:
                    print(f"❌ {method_name}: Method {parser_method} not found")
                    self.validation_results[method_name]['status'] = 'not_found'
                    all_passed = False
                    
            except Exception as e:
                error_msg = f"{method_name} failed: {str(e)}"
                print(f"❌ {error_msg}")
                self.validation_results[method_name]['issues'].append(error_msg)
                self.validation_results[method_name]['status'] = 'error'
                all_passed = False
        
        return all_passed
    
    def validate_ticks_parsing(self) -> bool:
        """Validate ticks parsing with common props."""
        print("\n=== Validating Ticks Parsing ===")
        try:
            # Test with some common props
            common_props = [
                'm_iHealth', 'm_ArmorValue', 'm_iTeamNum', 
                'm_vec + m_cell', 'm_angEyeAngles[0]', 'm_angEyeAngles[1]'
            ]
            
            # Get available props first
            available_props = self.parser.list_updated_fields()
            test_props = [prop for prop in common_props if prop in available_props]
            
            if not test_props:
                test_props = list(available_props)[:5]  # Use first 5 available props
            
            print(f"Testing with props: {test_props}")
            
            ticks_df = self.parser.parse_ticks(test_props)
            
            if isinstance(ticks_df, pd.DataFrame) and not ticks_df.empty:
                print(f"✅ Ticks: {len(ticks_df)} rows, columns: {list(ticks_df.columns)}")
                
                # Check for required columns
                expected_base_columns = {'tick', 'steamid'}
                missing_base = expected_base_columns - set(ticks_df.columns)
                
                if missing_base:
                    self.validation_results['ticks']['issues'].append(f"Missing base columns: {missing_base}")
                    print(f"❌ Missing base columns: {missing_base}")
                    self.validation_results['ticks']['status'] = 'failed'
                    return False
                else:
                    self.validation_results['ticks']['status'] = 'passed'
                    return True
            else:
                print("⚠️  No ticks data found")
                self.validation_results['ticks']['status'] = 'no_data'
                return True
                
        except Exception as e:
            error_msg = f"Ticks validation failed: {str(e)}"
            print(f"❌ {error_msg}")
            self.validation_results['ticks']['issues'].append(error_msg)
            self.validation_results['ticks']['status'] = 'error'
            return False
    
    def run_full_validation(self) -> Dict[str, Any]:
        """Run all validations and return comprehensive results."""
        print("🚀 Starting comprehensive demoparser2 validation...")
        print(f"Demo file: {self.demo_path}")
        
        # Run all validations
        validation_methods = [
            self.validate_header,
            self.validate_events_enum, 
            self.validate_event_schemas,
            self.validate_server_cvars,
            self.validate_grenades,
            self.validate_voice_data,
            self.validate_other_methods,
            self.validate_ticks_parsing
        ]
        
        results = []
        for validation_method in validation_methods:
            try:
                result = validation_method()
                results.append(result)
            except Exception as e:
                print(f"❌ Validation method {validation_method.__name__} crashed: {e}")
                results.append(False)
        
        # Print summary
        self.print_validation_summary()
        
        return self.validation_results
    
    def print_validation_summary(self):
        """Print a comprehensive summary of all validation results."""
        print("\n" + "="*60)
        print("🔍 VALIDATION SUMMARY")
        print("="*60)
        
        passed = 0
        failed = 0
        warnings = 0
        errors = 0
        
        for category, result in self.validation_results.items():
            status = result['status']
            issues_count = len(result.get('issues', []))
            
            if status == 'passed':
                icon = "✅"
                passed += 1
            elif status == 'failed':
                icon = "❌"
                failed += 1
            elif status in ['warning', 'partial', 'no_data']:
                icon = "⚠️ "
                warnings += 1
            else:  # error, not_available, etc.
                icon = "💥"
                errors += 1
            
            print(f"{icon} {category.upper()}: {status}")
            if issues_count > 0:
                print(f"    Issues: {issues_count}")
                for issue in result['issues'][:3]:  # Show first 3 issues
                    print(f"    - {issue}")
                if issues_count > 3:
                    print(f"    - ... and {issues_count - 3} more issues")
        
        print("\n📊 OVERALL RESULTS:")
        print(f"✅ Passed: {passed}")
        print(f"⚠️  Warnings: {warnings}")
        print(f"❌ Failed: {failed}")
        print(f"💥 Errors: {errors}")
        
        if failed == 0 and errors == 0:
            print("\n🎉 All critical validations passed!")
        elif failed > 0:
            print(f"\n⚠️  {failed} validations failed - schemas may need updates")
        
        if errors > 0:
            print(f"\n💥 {errors} validations had errors - check implementation")


def main():
    """Main function to run the validation."""
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
        validator = DemoParserValidator(demo_path)
        results = validator.run_full_validation()
        
        # Optionally save results to file
        import json
        with open('validation_results.json', 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print("\n💾 Detailed results saved to 'validation_results.json'")
        
    except Exception as e:
        print(f"❌ Validation failed with error: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    main()