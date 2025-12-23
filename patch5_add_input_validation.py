#!/usr/bin/env python3
"""
Patch 5: Add input validation to hashtable functions
"""

def apply_patch():
    with open('src/hashtable.c', 'r') as f:
        content = f.read()
    
    # Add input validation to hashtable_set
    old_hashtable_set = '''int hashtable_set(hashtable_t *hashtable, const char *key, size_t key_len,
                  json_t *value) {
    pair_t *pair;
    bucket_t *bucket;
    size_t hash, index;

    /* rehash if the load ratio exceeds 1 */
    if (hashtable->size >= hashsize(hashtable->order))
        if (hashtable_do_rehash(hashtable))
            return -1;

    hash = hash_str(key, key_len);
    index = hash & hashmask(hashtable->order);
    bucket = &hashtable->buckets[index];
    pair = hashtable_find_pair(hashtable, bucket, key, key_len, hash);

    if (pair) {
        json_decref(pair->value);
        pair->value = value;
    } else {
        pair = init_pair(value, key, key_len, hash);

        if (!pair)
            return -1;

        insert_to_bucket(hashtable, bucket, &pair->list);
        list_insert(&hashtable->ordered_list, &pair->ordered_list);

        hashtable->size++;
    }
    return 0;
}'''
    
    new_hashtable_set = '''int hashtable_set(hashtable_t *hashtable, const char *key, size_t key_len,
                  json_t *value) {
    pair_t *pair;
    bucket_t *bucket;
    size_t hash, index;

    /* input validation */
    if (!hashtable || !key || key_len == 0 || !value)
        return -1;

    /* rehash if the load ratio exceeds 1 */
    if (hashtable->size >= hashsize(hashtable->order))
        if (hashtable_do_rehash(hashtable))
            return -1;

    hash = hash_str(key, key_len);
    index = hash & hashmask(hashtable->order);
    bucket = &hashtable->buckets[index];
    pair = hashtable_find_pair(hashtable, bucket, key, key_len, hash);

    if (pair) {
        json_decref(pair->value);
        pair->value = value;
    } else {
        pair = init_pair(value, key, key_len, hash);

        if (!pair)
            return -1;

        insert_to_bucket(hashtable, bucket, &pair->list);
        list_insert(&hashtable->ordered_list, &pair->ordered_list);

        hashtable->size++;
    }
    return 0;
}'''
    
    # Add input validation to hashtable_get
    old_hashtable_get = '''void *hashtable_get(hashtable_t *hashtable, const char *key, size_t key_len) {
    pair_t *pair;
    size_t hash;
    bucket_t *bucket;

    hash = hash_str(key, key_len);
    bucket = &hashtable->buckets[hash & hashmask(hashtable->order)];

    pair = hashtable_find_pair(hashtable, bucket, key, key_len, hash);
    if (!pair)
        return NULL;

    return pair->value;
}'''
    
    new_hashtable_get = '''void *hashtable_get(hashtable_t *hashtable, const char *key, size_t key_len) {
    pair_t *pair;
    size_t hash;
    bucket_t *bucket;

    /* input validation */
    if (!hashtable || !key || key_len == 0)
        return NULL;

    hash = hash_str(key, key_len);
    bucket = &hashtable->buckets[hash & hashmask(hashtable->order)];

    pair = hashtable_find_pair(hashtable, bucket, key, key_len, hash);
    if (!pair)
        return NULL;

    return pair->value;
}'''
    
    # Add input validation to hashtable_del
    old_hashtable_del = '''int hashtable_del(hashtable_t *hashtable, const char *key, size_t key_len) {
    size_t hash = hash_str(key, key_len);
    return hashtable_do_del(hashtable, key, key_len, hash);
}'''
    
    new_hashtable_del = '''int hashtable_del(hashtable_t *hashtable, const char *key, size_t key_len) {
    size_t hash;

    /* input validation */
    if (!hashtable || !key || key_len == 0)
        return -1;

    hash = hash_str(key, key_len);
    return hashtable_do_del(hashtable, key, key_len, hash);
}'''
    
    # Apply all patches
    content = content.replace(old_hashtable_set, new_hashtable_set)
    content = content.replace(old_hashtable_get, new_hashtable_get)
    content = content.replace(old_hashtable_del, new_hashtable_del)
    
    # Write the modified content back
    with open('src/hashtable.c', 'w') as f:
        f.write(content)
    
    print("Patch 5 applied: Input validation added to hashtable functions")

if __name__ == "__main__":
    apply_patch()
