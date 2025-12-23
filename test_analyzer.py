#!/usr/bin/env python3
"""
Test script for the Jansson Code Analyzer
"""

import os
import sys
from code_analyzer import JanssonAnalyzer

def test_analyzer():
    """Test the analyzer with various scenarios"""
    
    print("Testing Jansson Code Analyzer...")
    
    # Test 1: Basic functionality
    print("\n1. Testing basic functionality...")
    analyzer = JanssonAnalyzer()
    story = analyzer.run_analysis()
    
    # Verify output file was created
    if os.path.exists("PROJECT_STORY.md"):
        print("✓ Output file created successfully")
    else:
        print("✗ Output file not created")
        return False
    
    # Test 2: Check story content
    print("\n2. Testing story content...")
    with open("PROJECT_STORY.md", "r") as f:
        content = f.read()
    
    required_sections = [
        "Project Context & Overview",
        "Problem Statement", 
        "Architecture & Structure",
        "Technology Stack",
        "Key Features & Capabilities",
        "Security Considerations",
        "Development Insights",
        "Quality Assessment",
        "Developer Recommendations"
    ]
    
    for section in required_sections:
        if section in content:
            print(f"✓ Found section: {section}")
        else:
            print(f"✗ Missing section: {section}")
            return False
    
    # Test 3: Check analysis data
    print("\n3. Testing analysis data...")
    
    # Verify structure analysis
    if analyzer.analysis_data.get('structure', {}).get('total_files', 0) > 0:
        print("✓ Project structure analyzed")
    else:
        print("✗ Project structure not analyzed")
        return False
    
    # Verify source analysis
    if analyzer.analysis_data.get('source_analysis', {}).get('functions', 0) > 0:
        print("✓ Source code analyzed")
    else:
        print("✗ Source code not analyzed")
        return False
    
    # Test 4: Check line count (should be under 500)
    print("\n4. Testing line count...")
    line_count = len(content.splitlines())
    if line_count <= 500:
        print(f"✓ Story is {line_count} lines (under 500 limit)")
    else:
        print(f"✗ Story is {line_count} lines (exceeds 500 limit)")
        return False
    
    # Test 5: Test edge case - non-existent directory
    print("\n5. Testing edge case handling...")
    try:
        edge_analyzer = JanssonAnalyzer("/non/existent/path")
        edge_analyzer.analyze_project_structure()
        print("✓ Handles non-existent paths gracefully")
    except Exception as e:
        print(f"✗ Failed on non-existent path: {e}")
        return False
    
    print("\n✓ All tests passed!")
    return True

if __name__ == "__main__":
    success = test_analyzer()
    sys.exit(0 if success else 1)
