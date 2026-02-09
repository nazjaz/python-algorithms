# Suffix Array API Documentation

This document provides detailed API documentation for the suffix array implementation with LCP array computation.

## Classes

### SuffixArray

Main class for suffix array construction and LCP array computation.

#### Methods

##### `__init__(text: str, config_path: str = "config.yaml") -> None`

Initialize suffix array.

**Parameters:**
- `text`: Input string to build suffix array for
- `config_path`: Path to configuration YAML file (default: "config.yaml")

**Raises:**
- `ValueError`: If text is empty

**Example:**
```python
sa = SuffixArray("banana")
```

##### `get_suffix_array() -> List[int]`

Get suffix array.

**Returns:**
- Copy of suffix array where suffix_array[i] is starting index of i-th smallest suffix

**Example:**
```python
suffix_array = sa.get_suffix_array()  # Returns [6, 5, 3, 1, 0, 4, 2]
```

##### `get_lcp_array() -> List[int]`

Get LCP array.

**Returns:**
- Copy of LCP array where lcp_array[i] is LCP between suffix_array[i] and suffix_array[i-1]

**Example:**
```python
lcp_array = sa.get_lcp_array()  # Returns [0, 0, 1, 3, 0, 0, 2]
```

##### `get_inverse_suffix_array() -> List[int]`

Get inverse suffix array.

**Returns:**
- Copy of inverse suffix array where inverse_suffix_array[i] is rank of suffix starting at index i

**Example:**
```python
inverse = sa.get_inverse_suffix_array()
```

##### `get_suffix(index: int) -> str`

Get suffix at given index in suffix array.

**Parameters:**
- `index`: Index in suffix array

**Returns:**
- Suffix string

**Raises:**
- `ValueError`: If index is invalid

**Example:**
```python
suffix = sa.get_suffix(0)  # Returns "$"
```

##### `get_all_suffixes() -> List[str]`

Get all suffixes in suffix array order.

**Returns:**
- List of all suffixes in sorted order

**Example:**
```python
suffixes = sa.get_all_suffixes()  # Returns all suffixes sorted
```

##### `search(pattern: str) -> List[int]`

Search for pattern in text using suffix array.

**Parameters:**
- `pattern`: Pattern to search for

**Returns:**
- List of starting positions where pattern occurs

**Time Complexity:** O(m log n) where m is pattern length

**Example:**
```python
occurrences = sa.search("ana")  # Returns [1, 3]
```

##### `get_lcp(i: int, j: int) -> int`

Get longest common prefix between two suffixes.

**Parameters:**
- `i`: First suffix index in suffix array
- `j`: Second suffix index in suffix array

**Returns:**
- Length of longest common prefix

**Raises:**
- `ValueError`: If indices are invalid

**Time Complexity:** O(j - i)

**Example:**
```python
lcp = sa.get_lcp(0, 1)  # Returns LCP length
```

##### `get_longest_common_substring() -> str`

Find longest common substring using LCP array.

**Returns:**
- Longest common substring

**Time Complexity:** O(n)

**Example:**
```python
longest = sa.get_longest_common_substring()  # Returns "ana"
```

##### `get_all_longest_common_substrings() -> List[str]`

Find all longest common substrings.

**Returns:**
- List of all longest common substrings

**Time Complexity:** O(n)

**Example:**
```python
all_longest = sa.get_all_longest_common_substrings()
```

##### `get_size() -> int`

Get size of suffix array.

**Returns:**
- Number of suffixes (text length + 1 for sentinel)

**Example:**
```python
size = sa.get_size()  # Returns 7 for "banana"
```

##### `get_text() -> str`

Get original text (without sentinel).

**Returns:**
- Original text string

**Example:**
```python
text = sa.get_text()  # Returns "banana"
```

##### `is_valid() -> bool`

Validate suffix array structure.

**Returns:**
- `True` if valid, `False` otherwise

**Time Complexity:** O(n)

**Example:**
```python
if sa.is_valid():
    print("Suffix array is valid")
```

## Usage Examples

### Basic Operations

```python
from src.main import SuffixArray

# Create suffix array
sa = SuffixArray("banana")

# Get arrays
suffix_array = sa.get_suffix_array()
lcp_array = sa.get_lcp_array()

# Search for pattern
occurrences = sa.search("ana")  # Returns [1, 3]

# Get longest common substring
longest = sa.get_longest_common_substring()  # Returns "ana"
```

### Pattern Matching

```python
sa = SuffixArray("mississippi")

# Search for patterns
occurrences_ssi = sa.search("ssi")  # Returns [5, 6]
occurrences_iss = sa.search("iss")  # Returns [1, 4]
```

### Longest Common Substring

```python
sa = SuffixArray("banana")

# Get longest common substring
longest = sa.get_longest_common_substring()  # Returns "ana"

# Get all longest common substrings
all_longest = sa.get_all_longest_common_substrings()
```

### LCP Queries

```python
sa = SuffixArray("banana")

# Get LCP between suffixes
lcp_0_1 = sa.get_lcp(0, 1)  # LCP between first two suffixes
lcp_2_3 = sa.get_lcp(2, 3)  # LCP between third and fourth suffixes
```

### Suffix Iteration

```python
sa = SuffixArray("abc")

# Get all suffixes
suffixes = sa.get_all_suffixes()
# Returns ["$", "abc$", "bc$", "c$"]

# Get specific suffix
suffix = sa.get_suffix(1)  # Returns "abc$"
```

## Error Handling

The implementation handles the following cases gracefully:

- **Empty text**: Raises `ValueError` during initialization
- **Invalid indices**: Raises `ValueError` for out-of-bounds access
- **Configuration errors**: Falls back to defaults if config file missing

## Performance Characteristics

| Operation | Time Complexity | Space Complexity |
|-----------|----------------|------------------|
| Construction | O(n log n) | O(n) |
| LCP Computation | O(n) | O(n) |
| Pattern Search | O(m log n) | O(1) |
| Get Suffix | O(1) | O(1) |
| Get LCP | O(j - i) | O(1) |
| Longest Common Substring | O(n) | O(n) |
| Validation | O(n) | O(1) |

Where:
- n = text length
- m = pattern length
- i, j = suffix array indices

## Algorithm Details

### Suffix Array Construction

The suffix array is constructed by:
1. Generating all suffixes
2. Sorting suffixes lexicographically
3. Storing starting indices in sorted order

### Kasai's Algorithm for LCP

Kasai's algorithm computes LCP array in O(n) time:
1. Build inverse suffix array
2. Traverse text from left to right
3. For each position, compute LCP with next suffix
4. Use previous LCP value to optimize computation

### Pattern Search

Pattern search uses binary search:
1. Binary search for leftmost occurrence
2. Binary search for rightmost occurrence
3. Return all positions in range

## Thread Safety

This implementation is not thread-safe. For concurrent access, external synchronization is required.
