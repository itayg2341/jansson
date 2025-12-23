#!/usr/bin/env python3
"""
Patch 3: Add bounds checking to strbuffer operations (fixed)
"""

def apply_patch():
    with open('src/strbuffer.c', 'r') as f:
        content = f.read()
    
    # Replace the specific function with improved version
    old_start = '''int strbuffer_append_bytes(strbuffer_t *strbuff, const char *data, size_t size) {
    if (size >= strbuff->size - strbuff->length) {
        size_t new_size;
        char *new_value;

        /* avoid integer overflow */
        if (strbuff->size > STRBUFFER_SIZE_MAX / STRBUFFER_FACTOR ||
            size > STRBUFFER_SIZE_MAX - 1 ||
            strbuff->length > STRBUFFER_SIZE_MAX - 1 - size)
            return -1;

        new_size = max(strbuff->size * STRBUFFER_FACTOR, strbuff->length + size + 1);

        new_value = jsonp_realloc(strbuff->value, strbuff->size, new_size);
        if (!new_value)
            return -1;

        strbuff->value = new_value;
        strbuff->size = new_size;
    }

    memcpy(strbuff->value + strbuff->length, data, size);
    strbuff->length += size;
    strbuff->value[strbuff->length] = '\0';

    return 0;
}'''
    
    new_start = '''int strbuffer_append_bytes(strbuffer_t *strbuff, const char *data, size_t size) {
    if (size == 0)
        return 0;
        
    if (data == NULL)
        return -1;
        
    if (size >= strbuff->size - strbuff->length) {
        size_t new_size;
        char *new_value;

        /* avoid integer overflow */
        if (strbuff->size > STRBUFFER_SIZE_MAX / STRBUFFER_FACTOR ||
            size > STRBUFFER_SIZE_MAX - 1 ||
            strbuff->length > STRBUFFER_SIZE_MAX - 1 - size)
            return -1;

        new_size = max(strbuff->size * STRBUFFER_FACTOR, strbuff->length + size + 1);

        new_value = jsonp_realloc(strbuff->value, strbuff->size, new_size);
        if (!new_value)
            return -1;

        strbuff->value = new_value;
        strbuff->size = new_size;
    }

    /* bounds checking - ensure we don't write past buffer */
    if (strbuff->length + size >= strbuff->size)
        return -1;
        
    memcpy(strbuff->value + strbuff->length, data, size);
    strbuff->length += size;
    strbuff->value[strbuff->length] = '\0';

    return 0;
}'''
    
    # Replace the function
    content = content.replace(old_start, new_start)
    
    # Write the modified content back
    with open('src/strbuffer.c', 'w') as f:
        f.write(content)
    
    print("Patch 3 applied: Bounds checking added to strbuffer operations")

if __name__ == "__main__":
    apply_patch()
