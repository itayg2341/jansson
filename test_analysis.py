#!/usr/bin/env python3
"""
Test script to verify the analysis findings
"""

import subprocess
import sys

def test_build_system():
    """Test that we can build the project"""
    print("Testing build system...")
    
    # Test CMake configuration
    result = subprocess.run(['cmake', '--version'], capture_output=True, text=True)
    if result.returncode != 0:
        print("CMake not available")
        return False
    
    # Test if CMakeLists.txt is valid
    result = subprocess.run(['cmake', '-S', '.', '-B', 'build_test', '--dry-run'], 
                          capture_output=True, text=True)
    if result.returncode != 0:
        print(f"CMake configuration failed: {result.stderr}")
        return False
    
    print("✓ Build system test passed")
    return True

def test_security_flags():
    """Test if security flags are present in build files"""
    print("Testing security compilation flags...")
    
    # Check CMakeLists.txt for security flags
    with open('CMakeLists.txt', 'r') as f:
        content = f.read()
        
    security_flags = [
        '-fstack-protector',
        '-D_FORTIFY_SOURCE',
        '-fPIE',
        '-pie'
    ]
    
    missing_flags = []
    for flag in security_flags:
        if flag not in content:
            missing_flags.append(flag)
    
    if missing_flags:
        print(f"✗ Missing security flags: {missing_flags}")
        return False
    
    print("✓ Security flags test passed")
    return True

def test_vulnerable_patterns():
    """Test for vulnerable code patterns"""
    print("Testing for vulnerable code patterns...")
    
    # Check for unsafe functions
    result = subprocess.run(['grep', '-r', 'strcpy\\|strcat\\|sprintf\\|gets', 'src/'], 
                          capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✗ Found unsafe functions: {result.stdout[:100]}...")
        return False
    
    # Check for integer overflow patterns
    result = subprocess.run(['grep', '-r', '.*\*.*sizeof.*', 'src/'], 
                          capture_output=True, text=True)
    if result.returncode == 0:
        lines = result.stdout.split('\n')
        if len(lines) > 5:  # Some expected, but many is concerning
            print(f"✗ Found potential integer overflow patterns: {len(lines)} instances")
            return False
    
    print("✓ Vulnerable patterns test passed")
    return True

def main():
    """Run all tests"""
    print("Running Jansson Analysis Verification Tests")
    print("=" * 50)
    
    tests = [
        test_build_system,
        test_security_flags,
        test_vulnerable_patterns
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            print()
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
            print()
    
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("All tests passed! The analysis findings are consistent.")
        return 0
    else:
        print("Some tests failed. Review the findings.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
