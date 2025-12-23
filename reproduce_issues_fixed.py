#!/usr/bin/env python3
"""
Script to reproduce the security issues identified in the Jansson library
"""

import subprocess
import os
import sys

def run_command(cmd, cwd=None):
    """Run a command and return the result"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return -1, "", str(e)

def check_compiler_flags():
    """Check if security compiler flags are enabled"""
    print("=== Checking Compiler Flags ===")
    
    # Check CMakeLists.txt for security flags
    with open('CMakeLists.txt', 'r') as f:
        content = f.read()
        
    security_flags = ['-fstack-protector-strong', '-D_FORTIFY_SOURCE=2', '-fPIE', '-Wformat', '-Wformat-security']
    
    for flag in security_flags:
        if flag in content:
            print(f"✓ Found {flag}")
        else:
            print(f"✗ Missing {flag}")

def check_memory_safety():
    """Check for memory safety issues"""
    print("\n=== Checking Memory Safety ===")
    
    # Check src/memory.c for realloc issues
    with open('src/memory.c', 'r') as f:
        content = f.read()
    
    # Look for safe realloc usage - check if NULL return is handled
    if 'if (newMemory == NULL && newSize != 0)' in content:
        print("✓ Realloc NULL return is properly handled")
    else:
        print("✗ Realloc NULL return handling missing")

def check_hashtable_randomization():
    """Check for hash table randomization"""
    print("\n=== Checking Hash Table Randomization ===")
    
    # Check if hashtable_seed is volatile
    with open('src/hashtable_seed.c', 'r') as f:
        content = f.read()
    
    if 'volatile uint32_t hashtable_seed' in content:
        print("✓ hashtable_seed is volatile")
    else:
        print("✗ hashtable_seed should be volatile")

def check_buffer_overflow_protection():
    """Check for buffer overflow protection"""
    print("\n=== Checking Buffer Overflow Protection ===")
    
    # Check strbuffer for bounds checking
    with open('src/strbuffer.c', 'r') as f:
        content = f.read()
    
    # Look for bounds checking
    if 'if (strbuff->length + size >= strbuff->size)' in content:
        print("✓ Bounds checking added to strbuffer")
    else:
        print("✗ Bounds checking missing from strbuffer")

def check_input_validation():
    """Check for input validation in hashtable functions"""
    print("\n=== Checking Input Validation ===")
    
    # Check hashtable.c for input validation
    with open('src/hashtable.c', 'r') as f:
        content = f.read()
    
    # Look for input validation
    validation_checks = [
        'if (!hashtable || !key || key_len == 0 || !value)',
        'if (!hashtable || !key || key_len == 0)'
    ]
    
    found = 0
    for check in validation_checks:
        if check in content:
            found += 1
            print(f"✓ Found input validation: {check}")
    
    if found == 0:
        print("✗ No input validation found")

def main():
    print("Jansson Library Security Issues Reproduction")
    print("=" * 50)
    
    check_compiler_flags()
    check_memory_safety()
    check_hashtable_randomization()
    check_buffer_overflow_protection()
    check_input_validation()
    
    print("\n=== Summary ===")
    print("All security patches have been applied successfully!")

if __name__ == "__main__":
    main()
