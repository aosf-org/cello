/* Dynamic buffer implementation - common pattern in C infrastructure */

#include <stdlib.h>
#include <string.h>

typedef struct {
    char* data;
    size_t size;      // Current size
    size_t capacity;  // Allocated capacity
} Buffer;

/**
 * Initialize a new buffer with initial capacity
 */
Buffer* buffer_new(size_t initial_capacity) {
    Buffer* buf = (Buffer*)malloc(sizeof(Buffer));
    if (!buf) return NULL;
    
    buf->data = (char*)malloc(initial_capacity);
    if (!buf->data) {
        free(buf);
        return NULL;
    }
    
    buf->size = 0;
    buf->capacity = initial_capacity;
    buf->data[0] = '\0';
    
    return buf;
}

/**
 * Grow buffer capacity (doubles current capacity)
 */
static int buffer_grow(Buffer* buf) {
    if (!buf) return -1;
    
    size_t new_capacity = buf->capacity * 2;
    if (new_capacity < 16) new_capacity = 16;
    
    char* new_data = (char*)realloc(buf->data, new_capacity);
    if (!new_data) return -1;
    
    buf->data = new_data;
    buf->capacity = new_capacity;
    return 0;
}

/**
 * Append data to buffer
 */
int buffer_append(Buffer* buf, const char* data, size_t len) {
    if (!buf || !data) return -1;
    
    while (buf->size + len + 1 > buf->capacity) {
        if (buffer_grow(buf) != 0) return -1;
    }
    
    memcpy(buf->data + buf->size, data, len);
    buf->size += len;
    buf->data[buf->size] = '\0';
    
    return 0;
}

/**
 * Append a string to buffer
 */
int buffer_append_str(Buffer* buf, const char* str) {
    if (!str) return -1;
    return buffer_append(buf, str, strlen(str));
}

/**
 * Clear buffer contents
 */
void buffer_clear(Buffer* buf) {
    if (!buf) return;
    buf->size = 0;
    if (buf->data) buf->data[0] = '\0';
}

/**
 * Free buffer and its data
 */
void buffer_free(Buffer* buf) {
    if (!buf) return;
    free(buf->data);
    free(buf);
}

/**
 * Get current buffer contents as C string
 */
const char* buffer_cstr(const Buffer* buf) {
    return buf ? buf->data : NULL;
}
