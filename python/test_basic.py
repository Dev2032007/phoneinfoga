#!/usr/bin/env python3
"""Basic test script for PhoneInfoga Python conversion."""

import sys
sys.path.insert(0, '.')

print("=" * 60)
print("PhoneInfoga Python Conversion - Basic Tests")
print("=" * 60)

# Test 1: Build module
print("\n1. Testing build module...")
try:
    from phoneinfoga.build import get_version_string, is_release, is_demo
    print(f"   ✓ Version: {get_version_string()}")
    print(f"   ✓ Is Release: {is_release()}")
    print(f"   ✓ Is Demo: {is_demo()}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 2: Logs module
print("\n2. Testing logs module...")
try:
    from phoneinfoga.logs import init_logging, get_logger
    init_logging()
    logger = get_logger("test")
    logger.debug("Debug message")
    print("   ✓ Logging initialized successfully")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 3: Filter module
print("\n3. Testing filter module...")
try:
    from phoneinfoga.lib.filter import Engine
    engine = Engine()
    engine.add_rule("scanner1", "scanner2")
    assert engine.match("scanner1") == True
    assert engine.match("scanner3") == False
    print("   ✓ Filter engine works correctly")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 4: Number utilities (without phonenumbers library)
print("\n4. Testing number utilities...")
try:
    from phoneinfoga.lib.number.utils import format_number, is_valid
    formatted = format_number("+33 678 34 23 11")
    assert formatted == "33678342311"
    assert is_valid("+33678342311") == True
    assert is_valid("invalid") == False
    print("   ✓ Number utilities work correctly")
    print(f"   ✓ Formatted: {formatted}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 5: Output module
print("\n5. Testing output module...")
try:
    from phoneinfoga.lib.output import get_output, OutputType
    from io import StringIO
    
    output_stream = StringIO()
    output = get_output(OutputType.CONSOLE, output_stream)
    
    results = {"test_scanner": {"field1": "value1", "field2": 123}}
    errors = {}
    
    output.write(results, errors)
    result_text = output_stream.getvalue()
    
    assert "test_scanner" in result_text
    print("   ✓ Output module works correctly")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 6: Scanner system
print("\n6. Testing scanner system...")
try:
    from phoneinfoga.lib.remote import Library, LocalScanner
    from phoneinfoga.lib.filter import Engine
    
    filter_engine = Engine()
    library = Library(filter_engine)
    library.add_scanner(LocalScanner())
    
    scanners = library.get_all_scanners()
    assert len(scanners) == 1
    assert scanners[0].name() == "local"
    print(f"   ✓ Scanner library works correctly")
    print(f"   ✓ Loaded scanners: {[s.name() for s in scanners]}")
except Exception as e:
    print(f"   ✗ Error: {e}")

print("\n" + "=" * 60)
print("Basic tests completed!")
print("=" * 60)
print("\nNote: Full functionality requires installing dependencies:")
print("  pip install -r requirements.txt")
print("\nThen you can run:")
print("  python main.py version")
print("  python main.py scanners")
print("  python main.py scan -n +33678342311")
