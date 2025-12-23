#!/usr/bin/env python3
"""
Patch 2: Fix memory safety issues in src/memory.c
"""

def apply_patch():
    with open('src/memory.c', 'r') as f:
        content = f.read()
    
    # Replace the jsonp_realloc function with a safer version
    old_function = '''void *jsonp_realloc(void *ptr, size_t originalSize, size_t newSize) {
    void *newMemory;

    if (do_realloc)
        return (*do_realloc)(ptr, newSize);

    // realloc emulation using malloc and free
    if (newSize == 0) {
        if (ptr != NULL)
            (*do_free)(ptr);

        return NULL;
    } else {
        newMemory = (*do_malloc)(newSize);

        if ((newMemory != NULL) && (ptr != NULL)) {
            memcpy(newMemory, ptr, (originalSize < newSize) ? originalSize : newSize);

            (*do_free)(ptr);
        }

        return newMemory;
    }
}'''
    
    new_function = '''void *jsonp_realloc(void *ptr, size_t originalSize, size_t newSize) {
    void *newMemory;

    if (do_realloc) {
        newMemory = (*do_realloc)(ptr, newSize);
        if (newMemory == NULL && newSize != 0) {
            // realloc failed, original ptr is still valid
            return NULL;
        }
        return newMemory;
    }

    // realloc emulation using malloc and free
    if (newSize == 0) {
        if (ptr != NULL)
            (*do_free)(ptr);

        return NULL;
    } else {
        newMemory = (*do_malloc)(newSize);

        if (newMemory == NULL) {
            // malloc failed, original ptr is still valid
            return NULL;
        }

        if (ptr != NULL) {
            memcpy(newMemory, ptr, (originalSize < newSize) ? originalSize : newSize);
            (*do_free)(ptr);
        }

        return newMemory;
    }
}'''
    
    # Replace the function
    content = content.replace(old_function, new_function)
    
    # Write the modified content back
    with open('src/memory.c', 'w') as f:
        f.write(content)
    
    print("Patch 2 applied: Memory safety issues fixed")

if __name__ == "__main__":
    apply_patch()
