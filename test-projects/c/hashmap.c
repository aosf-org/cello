/* Simple hash map implementation - fundamental data structure */

#include <stdlib.h>
#include <string.h>

#define HASHMAP_INITIAL_CAPACITY 16

typedef struct HashMapEntry {
    char* key;
    void* value;
    struct HashMapEntry* next;
} HashMapEntry;

typedef struct {
    HashMapEntry** buckets;
    size_t capacity;
    size_t size;
} HashMap;

/**
 * Simple hash function (djb2)
 */
static unsigned long hash_string(const char* str) {
    unsigned long hash = 5381;
    int c;
    while ((c = *str++)) {
        hash = ((hash << 5) + hash) + c;
    }
    return hash;
}

/**
 * Create a new hash map
 */
HashMap* hashmap_new(void) {
    HashMap* map = (HashMap*)malloc(sizeof(HashMap));
    if (!map) return NULL;
    
    map->capacity = HASHMAP_INITIAL_CAPACITY;
    map->size = 0;
    map->buckets = (HashMapEntry**)calloc(map->capacity, sizeof(HashMapEntry*));
    
    if (!map->buckets) {
        free(map);
        return NULL;
    }
    
    return map;
}

/**
 * Insert or update a key-value pair
 */
int hashmap_put(HashMap* map, const char* key, void* value) {
    if (!map || !key) return -1;
    
    unsigned long hash = hash_string(key);
    size_t index = hash % map->capacity;
    
    // Check if key exists
    HashMapEntry* entry = map->buckets[index];
    while (entry) {
        if (strcmp(entry->key, key) == 0) {
            entry->value = value;
            return 0;
        }
        entry = entry->next;
    }
    
    // Create new entry
    HashMapEntry* new_entry = (HashMapEntry*)malloc(sizeof(HashMapEntry));
    if (!new_entry) return -1;
    
    new_entry->key = strdup(key);
    if (!new_entry->key) {
        free(new_entry);
        return -1;
    }
    
    new_entry->value = value;
    new_entry->next = map->buckets[index];
    map->buckets[index] = new_entry;
    map->size++;
    
    return 0;
}

/**
 * Get value for a key
 */
void* hashmap_get(HashMap* map, const char* key) {
    if (!map || !key) return NULL;
    
    unsigned long hash = hash_string(key);
    size_t index = hash % map->capacity;
    
    HashMapEntry* entry = map->buckets[index];
    while (entry) {
        if (strcmp(entry->key, key) == 0) {
            return entry->value;
        }
        entry = entry->next;
    }
    
    return NULL;
}

/**
 * Remove a key-value pair
 */
int hashmap_remove(HashMap* map, const char* key) {
    if (!map || !key) return -1;
    
    unsigned long hash = hash_string(key);
    size_t index = hash % map->capacity;
    
    HashMapEntry** indirect = &map->buckets[index];
    HashMapEntry* entry = *indirect;
    
    while (entry) {
        if (strcmp(entry->key, key) == 0) {
            *indirect = entry->next;
            free(entry->key);
            free(entry);
            map->size--;
            return 0;
        }
        indirect = &entry->next;
        entry = entry->next;
    }
    
    return -1;
}

/**
 * Free hash map and all entries
 */
void hashmap_free(HashMap* map) {
    if (!map) return;
    
    for (size_t i = 0; i < map->capacity; i++) {
        HashMapEntry* entry = map->buckets[i];
        while (entry) {
            HashMapEntry* next = entry->next;
            free(entry->key);
            free(entry);
            entry = next;
        }
    }
    
    free(map->buckets);
    free(map);
}
