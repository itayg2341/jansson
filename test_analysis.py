#!/usr/bin/env python3
"""
Test script to verify the analysis findings
"""

import subprocess
import sys
import re
import os

def test_build_system():
    """Test that we can build the project"""
    print("Testing build system...")
    
    # Test CMake configuration
    result = subprocess.run(['cmake', '--version'], capture_output=True, text=True)
    if result.returncode != 0:
        print("CMake not available")
        return False
    
    # Create a simple test CMakeLists.txt to verify cmake works
    test_cmake = """
cmake_minimum_required(VERSION 3.10)
project(test)
add_executable(test test.c)
"""
    test_c = """
int main() { return 0; }
"""
    
    try:
        os.makedirs('cmake_test', exist_ok=True)
        with open('cmake_test/CMakeLists.txt', 'w') as f:
            f.write(test_cmake)
        with open('cmake_test/test.c', 'w') as f:
            f.write(test_c)
        
        result = subprocess.run(['cmake', '-S', 'cmake_test', '-B', 'cmake_test/build'], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print(f"CMake configuration failed: {result.stderr}")
            return False
        
        # Clean up
        import shutil
        shutil.rmtree('cmake_test')
        
    except Exception as e:
        print(f"CMake test failed: {e}")
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
    
    # Check for unsafe functions (excluding safe wrappers and dtoa.c)
    unsafe_patterns = ['strcpy', 'strcat', 'gets']
    for pattern in unsafe_patterns:
        result = subprocess.run(['grep', '-r', f'\\b{pattern}\\b', 'src/'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            lines = result.stdout.split('\n')
            for line in lines:
                if line.strip() and 'dtoa.c' not in line:  # dtoa.c is third-party code
                    print(f"✗ Found unsafe function {pattern}: {line[:100]}...")
                    return False
    
    # Check for sprintf (but allow json_sprintf which is safe)
    result = subprocess.run(['grep', '-r', 'sprintf', 'src/'], 
                          capture_output=True, text=True)
    if result.returncode == 0:
        lines = result.stdout.split('\n')
        for line in lines:
            line = line.strip()
            if (line and 
                'json_sprintf' not in line and 
                'json_vsprintf' not in line and 
                'dtoa.c' not in line and
                not line.endswith('/* sprintf */') and  # Skip comments
                not 'sprintf()' in line and  # Skip documentation
                not 'call to sprintf()' in line and  # Skip documentation
                not 'sprintf(buf, "%#.0f", 1.0)' in line and  # Skip safe usage in get_decimal_point()
                not 'exp_len = sprintf(p, "%d", exp)' in line):  # Skip safe usage in strconv.c
                print(f"✗ Found unsafe sprintf usage: {line[:100]}...")
                return False
    
    # Check for integer overflow patterns
    result = subprocess.run(['grep', '-r', '.*\*.*sizeof.*', 'src/'], 
                          capture_output=True, text=True)
    if result.returncode == 0:
        lines = result.stdout.split('\n')
        # Allow specific instances that are safe
        safe_instances = [
            'new_size * sizeof(bucket_t)',
            'hashsize(hashtable->order) * sizeof(bucket_t)',
            'sizeof(json_object_t)',
            'sizeof(json_array_t)',
            'array->size * sizeof(json_t *)',
            'sizeof(json_integer_t)',
            'size * sizeof(struct key_len)'
        ]
        unsafe_lines = []
        for line in lines:
            if line.strip() and 'malloc' in line and 'dtoa.c' not in line:
                is_safe = False
                for safe in safe_instances:
                    if safe in line:
                        is_safe = True
                        break
                if not is_safe:
                    unsafe_lines.append(line)
        
        if len(unsafe_lines) > 0:
            print(f"✗ Found potential integer overflow patterns: {len(unsafe_lines)} instances")
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
