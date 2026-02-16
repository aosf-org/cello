/* Simple string utility functions - common in infrastructure code */

#include <stdlib.h>
#include <string.h>
#include <ctype.h>

/**
 * Duplicate a string (like strdup)
 * Returns allocated string or NULL on failure
 */
char* str_duplicate(const char* src) {
    if (!src) return NULL;
    
    size_t len = strlen(src);
    char* dst = (char*)malloc(len + 1);
    if (!dst) return NULL;
    
    strcpy(dst, src);
    return dst;
}

/**
 * Trim whitespace from both ends of a string
 * Modifies string in place, returns pointer to start
 */
char* str_trim(char* str) {
    if (!str) return NULL;
    
    // Trim leading whitespace
    while (isspace((unsigned char)*str)) str++;
    
    if (*str == 0) return str;
    
    // Trim trailing whitespace
    char* end = str + strlen(str) - 1;
    while (end > str && isspace((unsigned char)*end)) end--;
    
    end[1] = '\0';
    return str;
}

/**
 * Convert string to lowercase
 * Modifies string in place
 */
void str_tolower(char* str) {
    if (!str) return;
    
    while (*str) {
        *str = tolower((unsigned char)*str);
        str++;
    }
}

/**
 * Safe string concatenation with buffer size
 * Returns 0 on success, -1 on overflow
 */
int str_concat(char* dst, size_t dst_size, const char* src) {
    if (!dst || !src || dst_size == 0) return -1;
    
    size_t dst_len = strlen(dst);
    size_t src_len = strlen(src);
    
    if (dst_len + src_len + 1 > dst_size) {
        return -1; // Would overflow
    }
    
    strcat(dst, src);
    return 0;
}

/**
 * Count occurrences of a character in a string
 */
int str_count_char(const char* str, char c) {
    if (!str) return 0;
    
    int count = 0;
    while (*str) {
        if (*str == c) count++;
        str++;
    }
    return count;
}
