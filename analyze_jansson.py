#!/usr/bin/env python3
"""
Jansson Code Analysis Script
This script analyzes the Jansson JSON library codebase to identify potential issues
and gather information for the engineering report.
"""

import os
import subprocess
import re
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run a shell command and return output"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return -1, "", str(e)

def analyze_c_file(filepath):
    """Analyze a C source file for potential issues"""
    issues = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            lines = content.split('\n')
            
        # Check for potential security issues
        for i, line in enumerate(lines, 1):
            # Check for unsafe functions
            if any(func in line for func in ['strcpy', 'strcat', 'sprintf', 'gets']):
                issues.append(f"Line {i}: Potentially unsafe function usage")
            
            # Check for buffer overflows
            if 'malloc' in line and not 'free' in content:
                issues.append(f"Line {i}: Memory allocation without corresponding free")
            
            # Check for integer overflows
            if any(op in line for op in ['*', '+', '-']) and 'size_t' in line:
                issues.append(f"Line {i}: Potential integer overflow in size calculation")
                
    except Exception as e:
        issues.append(f"Error analyzing file: {e}")
    
    return issues

def analyze_build_system():
    """Analyze build configuration files"""
    build_files = [
        'CMakeLists.txt', 'Makefile.am', 'configure.ac', 'Android.mk'
    ]
    
    build_info = {}
    for file in build_files:
        filepath = Path(file)
        if filepath.exists():
            try:
                with open(filepath, 'r') as f:
                    content = f.read()
                    build_info[file] = {
                        'size': len(content),
                        'lines': len(content.split('\n')),
                        'has_warnings': '-W' in content,
                        'has_security_flags': '-fstack-protector' in content or '-D_FORTIFY_SOURCE' in content
                    }
            except Exception as e:
                build_info[file] = f"Error reading {file}: {e}"
    
    return build_info

def check_dependencies():
    """Check for external dependencies"""
    dependencies = []
    
    # Check CMakeLists.txt
    if Path('CMakeLists.txt').exists():
        with open('CMakeLists.txt', 'r') as f:
            content = f.read()
            if 'find_package' in content:
                deps = re.findall(r'find_package\(([^)]+)\)', content)
                dependencies.extend(deps)
    
    # Check configure.ac
    if Path('configure.ac').exists():
        with open('configure.ac', 'r') as f:
            content = f.read()
            if 'PKG_CHECK_MODULES' in content:
                deps = re.findall(r'PKG_CHECK_MODULES\([^,]+,\s*([^)]+)\)', content)
                dependencies.extend(deps)
    
    return dependencies

def analyze_test_coverage():
    """Analyze test coverage"""
    test_info = {}
    
    if Path('test').exists():
        test_files = list(Path('test').rglob('*.c'))
        test_info['test_files'] = len(test_files)
        
        # Check for test types
        test_info['has_unit_tests'] = any('test' in str(f).lower() for f in test_files)
        test_info['has_integration_tests'] = any('suite' in str(f).lower() for f in test_files)
        
        # Check test scripts
        if Path('test/run-suites').exists():
            test_info['has_test_runner'] = True
        
    return test_info

def main():
    """Main analysis function"""
    print("Jansson Code Analysis Report")
    print("=" * 50)
    
    # Repository overview
    print("\n1. REPOSITORY OVERVIEW")
    print("-" * 30)
    
    src_files = list(Path('src').rglob('*.c'))
    header_files = list(Path('src').rglob('*.h'))
    
    print(f"Source files: {len(src_files)}")
    print(f"Header files: {len(header_files)}")
    
    # Analyze source files
    print("\n2. SOURCE CODE ANALYSIS")
    print("-" * 30)
    
    total_issues = 0
    for src_file in src_files[:10]:  # Analyze first 10 files
        issues = analyze_c_file(src_file)
        if issues:
            print(f"\n{src_file}:")
            for issue in issues[:5]:  # Show first 5 issues
                print(f"  - {issue}")
            total_issues += len(issues)
    
    print(f"\nTotal potential issues found: {total_issues}")
    
    # Build system analysis
    print("\n3. BUILD SYSTEM ANALYSIS")
    print("-" * 30)
    
    build_info = analyze_build_system()
    for file, info in build_info.items():
        if isinstance(info, dict):
            print(f"\n{file}:")
            print(f"  Lines: {info['lines']}")
            print(f"  Has warning flags: {info['has_warnings']}")
            print(f"  Has security flags: {info['has_security_flags']}")
        else:
            print(f"\n{file}: {info}")
    
    # Dependencies
    print("\n4. DEPENDENCIES")
    print("-" * 30)
    
    deps = check_dependencies()
    if deps:
        for dep in deps:
            print(f"  - {dep}")
    else:
        print("  No external dependencies found")
    
    # Test coverage
    print("\n5. TEST COVERAGE")
    print("-" * 30)
    
    test_info = analyze_test_coverage()
    for key, value in test_info.items():
        print(f"{key}: {value}")
    
    # Security analysis
    print("\n6. SECURITY ANALYSIS")
    print("-" * 30)
    
    # Check for security-related files
    security_files = ['SECURITY.md', '.gitignore', '.clang-format']
    for file in security_files:
        if Path(file).exists():
            print(f"✓ {file} exists")
        else:
            print(f"✗ {file} missing")
    
    print("\nAnalysis complete!")

if __name__ == "__main__":
    main()
