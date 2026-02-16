# CELLO Evaluation Report: string_utils

**Generated:** 2026-02-16T12:12:23.821239

---

## Original C Code (1768 bytes)

```c
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

```

---

## CLAUDE Transpilation

### Overall Score: 76/100

| Dimension | Score | Max | Details |
|-----------|-------|-----|----------|
| Compilation | 25 | 25 | ✓ Compiles successfully |
| Safety | 18 | 20 | ✓ No unsafe blocks | ✓ Uses Result for error handling | ✓ Uses Option for nullable values |
| Quality | 13 | 20 | ✓ Snake_case naming | ✓ Well documented (10 doc comments) | ✓ Functional programming patterns |
| Correctness | 7 | 15 | ✓ Edge case checks | ✓ Pattern matching |
| Maintainability | 3 | 10 | ✓ Clear public API (5 items) |
| Performance | 10 | 10 | ✓ Minimal cloning | ✓ Reference usage |

✅ **Compilation:** PASSED

### Generated Rust Code (1294 bytes)

```rust
/// Duplicate a string
/// Returns Some(String) or None if the input is None
pub fn str_duplicate(src: Option<&str>) -> Option<String> {
    src.map(|s| s.to_string())
}

/// Trim whitespace from both ends of a string
/// Returns a new String with whitespace removed, or None if input is None
pub fn str_trim(s: Option<String>) -> Option<String> {
    s.map(|string| string.trim().to_string())
}

/// Convert string to lowercase
/// Modifies string in place by returning a new lowercase String
pub fn str_tolower(s: Option<String>) -> Option<String> {
    s.map(|string| string.to_lowercase())
}

/// Safe string concatenation with buffer size limit
/// Returns Ok(()) on success, Err with message on overflow or invalid input
pub fn str_concat(dst: &mut String, dst_size: usize, src: &str) -> Result<(), String> {
    let new_len = dst.len() + src.len();
    
    if new_len > dst_size {
        return Err("Buffer overflow: concatenation would exceed size limit".to_string());
    }
    
    dst.push_str(src);
    Ok(())
}

/// Count occurrences of a character in a string
/// Returns the count, or 0 if the input is None
pub fn str_count_char(s: Option<&str>, c: char) -> usize {
    match s {
        Some(string) => string.chars().filter(|&ch| ch == c).count(),
        None => 0,
    }
}
```

### Safety Analysis

✓ No unsafe blocks | ✓ Uses Result for error handling | ✓ Uses Option for nullable values

### Code Quality

✓ Snake_case naming | ✓ Well documented (10 doc comments) | ✓ Functional programming patterns

### Correctness Indicators

✓ Edge case checks | ✓ Pattern matching

### Maintainability

✓ Clear public API (5 items)

### Performance Patterns

✓ Minimal cloning | ✓ Reference usage

---

## GEMINI Transpilation

### Overall Score: 81/100

| Dimension | Score | Max | Details |
|-----------|-------|-----|----------|
| Compilation | 25 | 25 | ✓ Compiles successfully |
| Safety | 15 | 20 | ✓ No unsafe blocks | ✓ Uses Result for error handling |
| Quality | 13 | 20 | ✓ Snake_case naming | ✓ Well documented (9 doc comments) | ✓ Functional programming patterns |
| Correctness | 12 | 15 | ✓ Includes tests | ✓ Edge case checks |
| Maintainability | 6 | 10 | ✓ Modular structure | ✓ Clear public API (5 items) |
| Performance | 10 | 10 | ✓ Minimal cloning | ✓ Reference usage |

✅ **Compilation:** PASSED

### Generated Rust Code (2174 bytes)

```rust
use std::{ffi::CString, os::raw::c_char};

/// Duplicate a string (like strdup)
/// Returns allocated string or an error on failure
pub fn str_duplicate(src: &str) -> Result<CString, std::ffi::NulError> {
    CString::new(src)
}

/// Trim whitespace from both ends of a string
/// Returns a new String with the trimmed content.
pub fn str_trim(s: &str) -> String {
    s.trim().to_string()
}

/// Convert string to lowercase
/// Returns a new String with the lowercase content.
pub fn str_tolower(s: &str) -> String {
    s.to_lowercase()
}

/// Safe string concatenation with buffer size
/// Returns Ok on success, Err on overflow
pub fn str_concat(dst: &mut String, src: &str, dst_size: usize) -> Result<(), String> {
    if dst.len() + src.len() + 1 > dst_size {
        return Err("Would overflow".to_string());
    }

    dst.push_str(src);
    Ok(())
}

/// Count occurrences of a character in a string
pub fn str_count_char(s: &str, c: char) -> usize {
    s.chars().filter(|&x| x == c).count()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_str_duplicate() {
        let src = "hello";
        let result = str_duplicate(src).unwrap();
        assert_eq!(result.to_str().unwrap(), src);
    }

    #[test]
    fn test_str_trim() {
        let src = "  hello  ";
        let result = str_trim(src);
        assert_eq!(result, "hello");
    }

    #[test]
    fn test_str_tolower() {
        let src = "Hello";
        let result = str_tolower(src);
        assert_eq!(result, "hello");
    }

    #[test]
    fn test_str_concat() {
        let mut dst = String::from("hello");
        let src = " world";
        let dst_size = 20;
        let result = str_concat(&mut dst, src, dst_size);
        assert!(result.is_ok());
        assert_eq!(dst, "hello world");

        let mut dst = String::from("hello");
        let src = " world";
        let dst_size = 10;
        let result = str_concat(&mut dst, src, dst_size);
        assert!(result.is_err());
    }

    #[test]
    fn test_str_count_char() {
        let src = "hello world";
        let c = 'l';
        let result = str_count_char(src, c);
        assert_eq!(result, 3);
    }
}
```

### Safety Analysis

✓ No unsafe blocks | ✓ Uses Result for error handling

### Code Quality

✓ Snake_case naming | ✓ Well documented (9 doc comments) | ✓ Functional programming patterns

### Correctness Indicators

✓ Includes tests | ✓ Edge case checks

### Maintainability

✓ Modular structure | ✓ Clear public API (5 items)

### Performance Patterns

✓ Minimal cloning | ✓ Reference usage

---

## Model Comparison

| Model | Total | Compilation | Safety | Quality | Correctness | Maintainability | Performance |
|-------|-------|-------------|--------|---------|-------------|-----------------|-------------|
| CLAUDE | 76/100 | 25/25 | 18/20 | 13/20 | 7/15 | 3/10 | 10/10 |
| GEMINI | 81/100 | 25/25 | 15/20 | 13/20 | 12/15 | 6/10 | 10/10 |

---

## Evaluation Methodology

CELLO evaluates transpilation quality across 6 dimensions:

1. **Compilation (25%)** — Does the code compile with rustc?
2. **Safety (20%)** — Memory safety improvements (reduced unsafe, proper error handling)
3. **Quality (20%)** — Idiomatic Rust patterns, documentation, naming conventions
4. **Correctness (15%)** — Functional equivalence, edge case handling, tests
5. **Maintainability (10%)** — Code organization, public API clarity, modularity
6. **Performance (10%)** — Efficiency patterns (minimal cloning, reference usage)

**Total possible score:** 100 points

