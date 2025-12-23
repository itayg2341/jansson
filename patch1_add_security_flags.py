#!/usr/bin/env python3
"""
Patch 1: Add security compiler flags to CMakeLists.txt
"""

def apply_patch():
    with open('CMakeLists.txt', 'r') as f:
        content = f.read()
    
    # Find the line with MSVC flags and add security flags after it
    lines = content.split('\n')
    
    for i, line in enumerate(lines):
        if 'add_definitions( "/W3 /D_CRT_SECURE_NO_WARNINGS /wd4005 /wd4996 /nologo" )' in line:
            # Add security flags after this line
            security_flags = [
                '   # Security hardening flags',
                '   add_definitions( "-fstack-protector-strong" )',
                '   add_definitions( "-D_FORTIFY_SOURCE=2" )',
                '   add_definitions( "-fPIE" )',
                '   add_definitions( "-Wformat" )',
                '   add_definitions( "-Wformat-security" )'
            ]
            lines[i+1:i+1] = security_flags
            break
    
    # Write the modified content back
    with open('CMakeLists.txt', 'w') as f:
        f.write('\n'.join(lines))
    
    print("Patch 1 applied: Security compiler flags added")

if __name__ == "__main__":
    apply_patch()
