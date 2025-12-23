#!/usr/bin/env python3
"""
Patch 3: Add bounds checking to strbuffer operations (fixed)
"""

def apply_patch():
    with open('src/strbuffer.c', 'r') as f:
        lines = f.readlines()
    
    # Find the strbuffer_append_bytes function and replace it
    start_line = None
    end_line = None
    
    for i, line in enumerate(lines):
        if 'int strbuffer_append_bytes(strbuffer_t *strbuff, const char *data, size_t size)' in line:
            start_line = i
        elif start_line is not None and line.strip() == '}' and 'strbuffer_pop' in lines[i+1]:
            end_line = i
            break
    
    if start_line is None or end_line is None:
        print("Could not find strbuffer_append_bytes function")
        return
    
    # New function with bounds checking
    new_function = [
        'int strbuffer_append_bytes(strbuffer_t *strbuff, const char *data, size_t size) {\n',
        '    if (size == 0)\n',
        '        return 0;\n',
        '        \n',
        '    if (data == NULL)\n',
        '        return -1;\n',
        '        \n',
        '    if (size >= strbuff->size - strbuff->length) {\n',
        '        size_t new_size;\n',
        '        char *new_value;\n',
        '\n',
        '        /* avoid integer overflow */\n',
        '        if (strbuff->size > STRBUFFER_SIZE_MAX / STRBUFFER_FACTOR ||\n',
        '            size > STRBUFFER_SIZE_MAX - 1 ||\n',
        '            strbuff->length > STRBUFFER_SIZE_MAX - 1 - size)\n',
        '            return -1;\n',
        '\n',
        '        new_size = max(strbuff->size * STRBUFFER_FACTOR, strbuff->length + size + 1);\n',
        '\n',
        '        new_value = jsonp_realloc(strbuff->value, strbuff->size, new_size);\n',
        '        if (!new_value)\n',
        '            return -1;\n',
        '\n',
        '        strbuff->value = new_value;\n',
        '        strbuff->size = new_size;\n',
        '    }\n',
        '\n',
        '    /* bounds checking - ensure we don\'t write past buffer */\n',
        '    if (strbuff->length + size >= strbuff->size)\n',
        '        return -1;\n',
        '        \n',
        '    memcpy(strbuff->value + strbuff->length, data, size);\n',
        '    strbuff->length += size;\n',
        '    strbuff->value[strbuff->length] = \'\\0\';\n',
        '\n',
        '    return 0;\n',
        '}\n'
    ]
    
    # Replace the function
    lines[start_line:end_line+1] = new_function
    
    # Write the modified content back
    with open('src/strbuffer.c', 'w') as f:
        f.writelines(lines)
    
    print("Patch 3 applied: Bounds checking added to strbuffer operations")

if __name__ == "__main__":
    apply_patch()
