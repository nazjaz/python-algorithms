# KMP Algorithm API Documentation

This document provides detailed API documentation for the KMP (Knuth-Morris-Pratt) algorithm implementation for pattern matching.

## Classes

### KMPAlgorithm

Main class for KMP algorithm pattern matching operations.

#### Methods

##### `__init__(text: str, config_path: str = "config.yaml") -> None`

Initialize KMP algorithm with text.

**Parameters:**
- `text`: Input text to search in
- `config_path`: Path to configuration YAML file (default: "config.yaml")

**Raises:**
- `ValueError`: If text is empty

**Example:**
```python
kmp = KMPAlgorithm("ABABDABACDABABCABCAB")
```

##### `search(pattern: str) -> List[int]`

Search for pattern in text using KMP algorithm.

**Parameters:**
- `pattern`: Pattern to search for

**Returns:**
- List of starting positions where pattern occurs

**Raises:**
- `ValueError`: If pattern is empty

**Time Complexity:** O(n + m) where n is text length, m is pattern length

**Example:**
```python
occurrences = kmp.search("ABABCABCAB")  # Returns [10]
```

##### `count_occurrences(pattern: str) -> int`

Count occurrences of pattern in text.

**Parameters:**
- `pattern`: Pattern to count

**Returns:**
- Number of occurrences

**Raises:**
- `ValueError`: If pattern is empty

**Time Complexity:** O(n + m)

**Example:**
```python
count = kmp.count_occurrences("ABAB")  # Returns 2
```

##### `find_all_occurrences(pattern: str) -> List[tuple]`

Find all occurrences with their positions and lengths.

**Parameters:**
- `pattern`: Pattern to search for

**Returns:**
- List of (position, length) tuples

**Raises:**
- `ValueError`: If pattern is empty

**Example:**
```python
occurrences = kmp.find_all_occurrences("ABAB")
# Returns [(0, 4), (4, 4)]
```

##### `is_substring(pattern: str) -> bool`

Check if pattern is a substring of text.

**Parameters:**
- `pattern`: Pattern to check

**Returns:**
- `True` if pattern found, `False` otherwise

**Raises:**
- `ValueError`: If pattern is empty

**Time Complexity:** O(n + m)

**Example:**
```python
is_sub = kmp.is_substring("ABC")  # Returns True
```

##### `get_failure_function(pattern: str) -> List[int]`

Get failure function (LPS array) for pattern.

**Parameters:**
- `pattern`: Pattern to get failure function for

**Returns:**
- Failure function (LPS array) where LPS[i] is the length of longest proper prefix which is also a suffix for pattern[0..i]

**Raises:**
- `ValueError`: If pattern is empty

**Time Complexity:** O(m) where m is pattern length

**Example:**
```python
lps = kmp.get_failure_function("abab")
# Returns [0, 0, 1, 2]
```

##### `search_all(patterns: List[str]) -> dict`

Search for multiple patterns in text.

**Parameters:**
- `patterns`: List of patterns to search for

**Returns:**
- Dictionary mapping pattern to list of occurrences

**Raises:**
- `ValueError`: If patterns list is empty

**Time Complexity:** O(k(n + m)) where k is number of patterns

**Example:**
```python
results = kmp.search_all(["ABAB", "ABC", "AB"])
# Returns {"ABAB": [0, 4], "ABC": [12, 15], "AB": [0, 2, 4, ...]}
```

##### `get_text() -> str`

Get text string.

**Returns:**
- Text string

**Example:**
```python
text = kmp.get_text()  # Returns "ABABDABACDABABCABCAB"
```

##### `get_length() -> int`

Get text length.

**Returns:**
- Length of text

**Example:**
```python
length = kmp.get_length()  # Returns 20
```

## Usage Examples

### Basic Pattern Matching

```python
from src.main import KMPAlgorithm

# Create KMP algorithm instance
kmp = KMPAlgorithm("ABABDABACDABABCABCAB")

# Search for pattern
occurrences = kmp.search("ABABCABCAB")  # Returns [10]

# Count occurrences
count = kmp.count_occurrences("ABAB")  # Returns 2

# Check if substring exists
is_sub = kmp.is_substring("ABC")  # Returns True
```

### Failure Function Analysis

```python
kmp = KMPAlgorithm("text")

# Get failure function for pattern
lps = kmp.get_failure_function("abab")
# Returns [0, 0, 1, 2]

# Analyze pattern structure
pattern = "ABABCABCAB"
lps = kmp.get_failure_function(pattern)
# Returns [0, 0, 1, 2, 0, 1, 2, 3, 4, 0]
```

### Multiple Pattern Matching

```python
kmp = KMPAlgorithm("ABABDABACDABABCABCAB")

# Search for multiple patterns
patterns = ["ABAB", "ABC", "AB", "XYZ"]
results = kmp.search_all(patterns)

# Results: {"ABAB": [0, 4], "ABC": [12, 15], "AB": [0, 2, 4, ...], "XYZ": []}
for pattern, occurrences in results.items():
    print(f"Pattern '{pattern}': {occurrences}")
```

### All Occurrences with Positions

```python
kmp = KMPAlgorithm("banana")

# Get all occurrences with positions and lengths
occurrences = kmp.find_all_occurrences("ana")
# Returns [(1, 3), (3, 3)]
```

## Error Handling

The implementation handles the following cases gracefully:

- **Empty text**: Raises `ValueError` during initialization
- **Empty pattern**: Raises `ValueError` for search operations
- **Empty patterns list**: Raises `ValueError` for multiple pattern search
- **Configuration errors**: Falls back to defaults if config file missing

## Performance Characteristics

| Operation | Time Complexity | Space Complexity |
|-----------|----------------|------------------|
| Build Failure Function | O(m) | O(m) |
| Single Pattern Search | O(n + m) | O(m) |
| Multiple Pattern Search | O(k(n + m)) | O(m) |
| Count Occurrences | O(n + m) | O(m) |
| Get Failure Function | O(m) | O(m) |

Where:
- n = text length
- m = pattern length
- k = number of patterns

## Algorithm Details

### Failure Function (LPS Array) Construction

The failure function is built using the following algorithm:

1. **Initialize**: LPS[0] = 0, length = 0, i = 1
2. **For each position i**:
   - If pattern[i] == pattern[length], extend match
   - Otherwise, use LPS[length-1] to find next possible match
   - Update length accordingly
3. **Store**: LPS[i] = length

**Key Insight**: When a mismatch occurs at position i, LPS[i-1] tells us how many characters we can skip.

### Pattern Matching Process

1. **Preprocess**: Build failure function for pattern - O(m)
2. **Initialize**: i = 0 (text index), j = 0 (pattern index)
3. **While i < n**:
   - If text[i] == pattern[j], advance both
   - If j == m, pattern found at i - j
   - On mismatch, use LPS[j-1] to skip characters
4. **Continue**: Until text is fully scanned

**Optimization**: The failure function allows skipping characters in text without backtracking, ensuring each character is compared at most once.

## Thread Safety

This implementation is not thread-safe. For concurrent access, external synchronization is required.
