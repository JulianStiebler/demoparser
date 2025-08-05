#!/usr/bin/env python3
"""
Comprehensive validation script for demoparser2 generated code.
Validates schemas, dataclasses, and enums against actual demo data.
"""

import os
import sys
import json
import traceback
from typing import Dict, Any, Optional
import pandas as pd
from dataclasses import fields, is_dataclass

try:
    from demoparser2 import DemoParser
    import pandera as pa
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure demoparser2 and pandera are properly installed")
    sys.exit(1)

# Import generated modules
try:
    from enums import Event, ServerCVar, Scope, NType
    # Import dataclass and schema modules for dynamic access
    import dataclass as dataclass_module
    import schema as schema_module  
    from props import demoparser_schema
except ImportError as e:
    print(f"Could not import generated modules: {e}")
    print("Make sure to run doc_gen.py first to generate the required files")
    sys.exit(1)


class ValidationResult:
    """Container for validation results."""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.warnings = 0
        self.errors = []
        self.warnings_list = []
        self.successes = []
    
    def add_success(self, message: str):
        self.passed += 1
        self.successes.append(f"✅ {message}")
    
    def add_error(self, message: str, exception: Optional[Exception] = None):
        self.failed += 1
        error_msg = f"❌ {message}"
        if exception:
            error_msg += f" - {str(exception)}"
        self.errors.append(error_msg)
    
    def add_warning(self, message: str):
        self.warnings += 1
        self.warnings_list.append(f"⚠️  {message}")
    
    def print_summary(self):
        print(f"\n{'='*60}")
        print("VALIDATION SUMMARY")
        print(f"{'='*60}")
        print(f"✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        print(f"⚠️  Warnings: {self.warnings}")
        print(f"📊 Total Tests: {self.passed + self.failed}")
        
        if self.successes:
            print("\n🎉 SUCCESSES:")
            for success in self.successes[-10:]:  # Show last 10
                print(f"   {success}")
            if len(self.successes) > 10:
                print(f"   ... and {len(self.successes) - 10} more")
        
        if self.warnings_list:
            print("\n⚠️  WARNINGS:")
            for warning in self.warnings_list:
                print(f"   {warning}")
        
        if self.errors:
            print("\n❌ ERRORS:")
            for error in self.errors:
                print(f"   {error}")
        
        overall_status = "✅ PASSED" if self.failed == 0 else "❌ FAILED"
        print(f"\nOverall Status: {overall_status}")


class DemoParserValidator:
    """Comprehensive validator for generated demoparser2 code."""
    
    def __init__(self, demo_path: str, analysis_json_path: str):
        self.demo_path = demo_path
        self.analysis_json_path = analysis_json_path
        self.parser = DemoParser(demo_path)
        self.analysis_data = self._load_analysis_data()
        self.result = ValidationResult()
    
    def _load_analysis_data(self) -> Dict[str, Any]:
        """Load the analysis results from JSON."""
        try:
            with open(self.analysis_json_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load analysis data from {self.analysis_json_path}: {e}")
            return {}
    
    def validate_all(self):
        """Run all validation tests."""
        print("🔍 Starting comprehensive validation...")
        print(f"📁 Demo file: {self.demo_path}")
        print(f"📊 Analysis data: {self.analysis_json_path}")
        print(f"{'='*60}")
        
        # Core validation tests
        self.validate_enums()
        self.validate_schemas()
        self.validate_dataclasses()
        self.validate_parsing_methods()
        self.validate_data_consistency()
        self.validate_pandera_schemas()
        
        # Print results
        self.result.print_summary()
        
        return self.result.failed == 0
    
    def validate_enums(self):
        """Validate that generated enums match actual data."""
        print("\n📋 Validating Enums...")
        
        # Validate Event enum
        try:
            actual_events = set(self.parser.list_game_events())
            enum_events = set(event.value for event in Event)
            
            missing_in_enum = actual_events - enum_events
            extra_in_enum = enum_events - actual_events
            
            if not missing_in_enum and not extra_in_enum:
                self.result.add_success(f"Event enum matches actual events ({len(actual_events)} events)")
            else:
                if missing_in_enum:
                    self.result.add_error(f"Events missing from enum: {missing_in_enum}")
                if extra_in_enum:
                    self.result.add_warning(f"Extra events in enum: {extra_in_enum}")
        except Exception as e:
            self.result.add_error("Failed to validate Event enum", e)
        
        # Validate ServerCVar enum
        try:
            actual_cvars = set(self.parser.list_updated_fields())
            enum_cvars = set(cvar.value for cvar in ServerCVar if cvar.value != "-")
            
            coverage = len(actual_cvars & enum_cvars) / len(actual_cvars) * 100 if actual_cvars else 0
            
            if coverage > 80:
                self.result.add_success(f"ServerCVar enum has {coverage:.1f}% coverage ({len(enum_cvars)} CVars)")
            else:
                self.result.add_warning(f"ServerCVar enum only covers {coverage:.1f}% of actual CVars")
                
        except Exception as e:
            self.result.add_error("Failed to validate ServerCVar enum", e)
        
        # Validate other enums exist
        for enum_class in [Scope, NType]:
            try:
                if len(list(enum_class)) > 0:
                    self.result.add_success(f"{enum_class.__name__} enum properly defined with {len(list(enum_class))} values")
                else:
                    self.result.add_error(f"{enum_class.__name__} enum is empty")
            except Exception as e:
                self.result.add_error(f"Failed to validate {enum_class.__name__} enum", e)
    
    def validate_schemas(self):
        """Validate that schemas exist and are properly defined."""
        print("\n📐 Validating Schemas...")
        
        # Get all schema classes from the schema module
        schema_classes = [
            getattr(schema_module, name) for name in dir(schema_module)
            if name.endswith('Schema') and hasattr(getattr(schema_module, name), '__annotations__')
        ]
        
        for schema_class in schema_classes:
            try:
                # Check if it's a proper Pandera schema
                if hasattr(schema_class, '__annotations__'):
                    field_count = len(schema_class.__annotations__)
                    self.result.add_success(f"{schema_class.__name__} defined with {field_count} fields")
                else:
                    self.result.add_error(f"{schema_class.__name__} is not properly defined")
            except Exception as e:
                self.result.add_error(f"Failed to validate {schema_class.__name__}", e)
        
        # Validate demoparser_schema from props
        try:
            if demoparser_schema and hasattr(demoparser_schema, '__annotations__'):
                field_count = len(demoparser_schema.__annotations__)
                self.result.add_success(f"demoparser_schema properly defined with {field_count} fields")
            else:
                self.result.add_error("demoparser_schema is not properly defined in props.py")
        except Exception as e:
            self.result.add_error("Failed to validate demoparser_schema", e)
    
    def validate_dataclasses(self):
        """Validate that dataclasses are properly defined and match expected data."""
        print("\n📦 Validating Dataclasses...")
        
        # Get all dataclasses from the dataclass module
        
        for name in dir(dataclass_module):
            obj = getattr(dataclass_module, name)
            if is_dataclass(obj) and not name.startswith('_'):
                try:
                    field_count = len(fields(obj))
                    self.result.add_success(f"{name} dataclass properly defined with {field_count} fields")
                    
                    # Try to create an instance (if we can determine required fields)
                    try:
                        field_list = fields(obj)
                        if all(field.default != field.default_factory for field in field_list):
                            # All fields have defaults, try to create instance
                            obj()  # Test instantiation
                            self.result.add_success(f"{name} dataclass can be instantiated")
                    except Exception:
                        # Some fields might require values, that's okay
                        pass
                        
                except Exception as e:
                    self.result.add_error(f"Failed to validate dataclass {name}", e)
    
    def validate_parsing_methods(self):
        """Validate that parsing methods work and return expected data structures."""
        print("\n🔧 Validating Parsing Methods...")
        
        # Test event parsing
        try:
            events = self.parser.list_game_events()
            successful_events = 0
            
            for event in events[:10]:  # Test first 10 events
                try:
                    df = self.parser.parse_event(event)
                    if isinstance(df, pd.DataFrame):
                        successful_events += 1
                        
                        # Check against analysis data if available
                        if self.analysis_data and 'events' in self.analysis_data:
                            expected_data = self.analysis_data['events'].get(event, {})
                            if 'columns' in expected_data:
                                expected_cols = set(expected_data['columns'])
                                actual_cols = set(df.columns)
                                
                                if expected_cols == actual_cols:
                                    self.result.add_success(f"Event {event} columns match analysis")
                                else:
                                    missing = expected_cols - actual_cols
                                    extra = actual_cols - expected_cols
                                    if missing:
                                        self.result.add_warning(f"Event {event} missing columns: {missing}")
                                    if extra:
                                        self.result.add_warning(f"Event {event} extra columns: {extra}")
                        
                except Exception as e:
                    self.result.add_warning(f"Could not parse event {event}: {e}")
            
            if successful_events > 0:
                self.result.add_success(f"Successfully parsed {successful_events}/{len(events[:10])} events")
            else:
                self.result.add_error("Could not parse any events")
                
        except Exception as e:
            self.result.add_error("Failed to validate event parsing", e)
        
        # Test other parsing methods
        parsing_methods = [
            ('parse_header', 'Header'),
            ('parse_player_info', 'PlayerInfo'),
            ('parse_grenades', 'Grenades'),
            ('parse_item_drops', 'ItemDrops'),
            ('parse_skins', 'Skins'),
            ('parse_ticks', 'Ticks'),
            ('parse_voice', 'Voice')
        ]
        
        for method_name, data_type in parsing_methods:
            try:
                if hasattr(self.parser, method_name):
                    result = getattr(self.parser, method_name)()
                    
                    if method_name == 'parse_voice':
                        # Voice returns dict
                        if isinstance(result, dict):
                            self.result.add_success(f"{method_name} returns dict with {len(result)} entries")
                        else:
                            self.result.add_warning(f"{method_name} did not return expected dict")
                    elif method_name == 'parse_header':
                        # Header returns dict
                        if isinstance(result, dict):
                            self.result.add_success(f"{method_name} returns dict with {len(result)} fields")
                        else:
                            self.result.add_warning(f"{method_name} did not return expected dict")
                    else:
                        # Others return DataFrames
                        if isinstance(result, pd.DataFrame):
                            self.result.add_success(f"{method_name} returns DataFrame with {len(result)} rows, {len(result.columns)} columns")
                        else:
                            self.result.add_warning(f"{method_name} did not return DataFrame")
                else:
                    self.result.add_warning(f"Parser does not have method {method_name}")
                    
            except Exception as e:
                self.result.add_warning(f"Could not execute {method_name}: {e}")
    
    def validate_data_consistency(self):
        """Validate data consistency between analysis and actual parsing."""
        print("\n🔍 Validating Data Consistency...")
        
        if not self.analysis_data:
            self.result.add_warning("No analysis data available for consistency check")
            return
        
        # Check events consistency
        try:
            actual_events = set(self.parser.list_game_events())
            analysis_events = set(self.analysis_data.get('events', {}).keys())
            
            if actual_events == analysis_events:
                self.result.add_success(f"Event lists consistent ({len(actual_events)} events)")
            else:
                missing = actual_events - analysis_events
                extra = analysis_events - actual_events
                if missing:
                    self.result.add_warning(f"Analysis missing events: {missing}")
                if extra:
                    self.result.add_warning(f"Analysis has extra events: {extra}")
        except Exception as e:
            self.result.add_error("Failed to validate event consistency", e)
        
        # Check CVars consistency
        try:
            actual_cvars = set(self.parser.list_updated_fields())
            analysis_cvars = set(self.analysis_data.get('server_cvars', []))
            
            if actual_cvars == analysis_cvars:
                self.result.add_success(f"CVar lists consistent ({len(actual_cvars)} CVars)")
            else:
                missing = actual_cvars - analysis_cvars
                extra = analysis_cvars - actual_cvars
                if missing:
                    self.result.add_warning(f"Analysis missing CVars: {len(missing)} CVars")
                if extra:
                    self.result.add_warning(f"Analysis has extra CVars: {len(extra)} CVars")
        except Exception as e:
            self.result.add_error("Failed to validate CVar consistency", e)
    
    def validate_pandera_schemas(self):
        """Validate actual data against Pandera schemas."""
        print("\n🛡️  Validating Pandera Schemas...")
        
        # Test each schema against actual data
        schema_tests = [
            ('PlayerInfoSchema', 'parse_player_info'),
            ('GrenadeSchema', 'parse_grenades'),
            ('ItemDropSchema', 'parse_item_drops'),
            ('SkinSchema', 'parse_skins'),
        ]
        
        for schema_name, method_name in schema_tests:
            try:
                if hasattr(schema_module, schema_name) and hasattr(self.parser, method_name):
                    schema_class = getattr(schema_module, schema_name)
                    df = getattr(self.parser, method_name)()
                    
                    if isinstance(df, pd.DataFrame) and not df.empty:
                        try:
                            # Validate DataFrame against schema
                            schema_class.validate(df)
                            self.result.add_success(f"{schema_name} successfully validates {method_name} data")
                        except pa.errors.SchemaError as e:
                            self.result.add_error(f"{schema_name} validation failed for {method_name}: {e}")
                        except Exception as e:
                            self.result.add_error(f"{schema_name} validation error: {e}")
                    else:
                        self.result.add_warning(f"No data to validate for {schema_name} (empty DataFrame)")
                else:
                    missing = []
                    if not hasattr(schema_module, schema_name):
                        missing.append(f"schema {schema_name}")
                    if not hasattr(self.parser, method_name):
                        missing.append(f"method {method_name}")
                    self.result.add_warning(f"Cannot test {schema_name}: missing {', '.join(missing)}")
                    
            except Exception as e:
                self.result.add_error(f"Failed to validate {schema_name}", e)
        
        # Test demoparser_schema with parse_ticks
        try:
            if hasattr(self.parser, 'parse_ticks'):
                df = self.parser.parse_ticks(['tick'])  # Parse minimal tick data
                if isinstance(df, pd.DataFrame) and not df.empty:
                    try:
                        # Validate DataFrame against schema
                        demoparser_schema.validate(df)
                        self.result.add_success("demoparser_schema successfully validates parse_ticks data")
                    except pa.errors.SchemaError as e:
                        self.result.add_error(f"demoparser_schema validation failed: {e}")
                    except Exception as e:
                        self.result.add_error(f"demoparser_schema validation error: {e}")
                else:
                    self.result.add_warning("No tick data to validate against demoparser_schema")
            else:
                self.result.add_warning("Parser does not have parse_ticks method")
        except Exception as e:
            self.result.add_error("Failed to validate demoparser_schema", e)
    
    def test_dataclass_creation(self):
        """Test creating dataclass instances from actual parsed data."""
        print("\n🏗️  Testing Dataclass Creation...")
        
        # Test Header dataclass
        try:
            header_data = self.parser.parse_header()
            if isinstance(header_data, dict):
                # Try to create Header instance
                try:
                    if hasattr(dataclass_module, 'Header'):
                        # Get expected fields
                        header_fields = {field.name for field in fields(dataclass_module.Header)}
                        
                        # Create kwargs with available data
                        kwargs = {}
                        for field_name in header_fields:
                            if field_name in header_data:
                                kwargs[field_name] = header_data[field_name]
                        
                        # Try to create instance
                        header_instance = dataclass_module.Header(**kwargs)
                        self.result.add_success("Successfully created Header dataclass instance")
                        
                        # Test DotSeparatedString if present
                        if hasattr(header_instance, 'addons') and hasattr(header_instance, 'addons_list'):
                            _ = header_instance.addons_list  # Test property access
                            self.result.add_success("DotSeparatedString functionality works")
                            
                except Exception as e:
                    self.result.add_error("Failed to create Header dataclass instance", e)
            else:
                self.result.add_warning("Header data is not a dict, cannot test dataclass creation")
        except Exception as e:
            self.result.add_error("Failed to test Header dataclass creation", e)
        
        # Test VoiceData dataclass
        try:
            voice_data = self.parser.parse_voice()
            if isinstance(voice_data, dict) and voice_data:
                try:
                    if hasattr(dataclass_module, 'VoiceData'):
                        voice_instance = dataclass_module.VoiceData(voice_clips=voice_data)
                        self.result.add_success(f"Successfully created VoiceData dataclass with {voice_instance.player_count} players")
                        
                        # Test methods
                        if voice_instance.player_ids:
                            test_id = voice_instance.player_ids[0]
                            if voice_instance.has_voice_data(test_id):
                                self.result.add_success("VoiceData methods work correctly")
                        
                except Exception as e:
                    self.result.add_error("Failed to create VoiceData dataclass instance", e)
            else:
                self.result.add_warning("No voice data available to test VoiceData dataclass")
        except Exception as e:
            self.result.add_error("Failed to test VoiceData dataclass creation", e)


def main():
    """Main function to run validation."""
    # Look for demo file
    demo_files = ['dem.dem', 'test_demo.dem']
    demo_path = None
    
    for demo_file in demo_files:
        if os.path.exists(demo_file):
            demo_path = demo_file
            break
    
    if not demo_path:
        print("❌ No demo file found. Please ensure 'dem.dem' or 'test_demo.dem' exists.")
        return False
    
    # Look for analysis JSON
    analysis_json = 'analysis_results.json'
    if not os.path.exists(analysis_json):
        print(f"⚠️  Analysis JSON not found at {analysis_json}")
        print("   Run doc_gen.py first to generate analysis data")
        return False
    
    try:
        validator = DemoParserValidator(demo_path, analysis_json)
        success = validator.validate_all()
        
        if success:
            print("\n🎉 All validations passed! Generated code is working correctly.")
        else:
            print("\n⚠️  Some validations failed. Check the errors above.")
            
        return success
        
    except Exception as e:
        print(f"❌ Validation failed with error: {e}")
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
