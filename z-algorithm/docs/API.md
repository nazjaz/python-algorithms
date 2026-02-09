# Z-Algorithm API Documentation

This document provides detailed API documentation for the Z-algorithm implementation for pattern matching.

## Classes

### ZAlgorithm

Main class for Z-algorithm pattern matching operations.

#### Methods

##### `__init__(text: str, config_path: str = "config.yaml") -> None`

Initialize Z-algorithm with text.

**Parameters:**
- `text`: Input text to search in
- `config_path`: Path to configuration YAML file (default: "config.yaml")

**Raises:**
- `ValueError`: If text is empty

**Example:**
```python
z_algo = ZAlgorithm("banana")
```

##### `search(pattern: str) -> List[int]`

Search for pattern in text using Z-algorithm.

**Parameters:**
- `pattern`: Pattern to search for

**Returns:**
- List of starting positions where pattern occurs

**Raises:**
- `ValueError`: If pattern is empty

**Time Complexity:** O(n + m) where n is text length, m is pattern length

**Example:**
```python
occurrences = z_algo.search("ana")  # Returns [1, 3]
```

##### `search_all(patterns: List[str]) -> Dict[str, List[int]]`

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
results = z_algo.search_all(["ana", "nan", "ban"])
# Returns {"ana": [1, 3], "nan": [2], "ban": [0]}
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
count = z_algo.count_occurrences("ana")  # Returns 2
```

##### `find_all_occurrences(pattern: str) -> List[Tuple[int, int]]`

Find all occurrences with their positions and lengths.

**Parameters:**
- `pattern`: Pattern to search for

**Returns:**
- List of (position, length) tuples

**Raises:**
- `ValueError`: If pattern is empty

**Example:**
```python
occurrences = z_algo.find_all_occurrences("ana")
# Returns [(1, 3), (3, 3)]
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
is_sub = z_algo.is_substring("ana")  # Returns True
```

##### `get_z_array(pattern: str) -> List[int]`

Get Z-array for pattern concatenated with text.

**Parameters:**
- `pattern`: Pattern to compute Z-array for

**Returns:**
- Z-array for pattern + separator + text

**Raises:**
- `ValueError`: If pattern is empty

**Time Complexity:** O(n + m)

**Example:**
```python
z_array = z_algo.get_z_array("ana")
```

##### `get_longest_prefix_match(position: int) -> int`

Get length of longest prefix match starting at position.

**Parameters:**
- `position`: Starting position in text

**Returns:**
- Length of longest prefix match

**Raises:**
- `ValueError`: If position is invalid

**Time Complexity:** O(n)

**Example:**
```python
match_length = z_algo.get_longest_prefix_match(1)
```

##### `find_longest_repeated_substring() -> str`

Find longest repeated substring using Z-array.

**Returns:**
- Longest repeated substring

**Time Complexity:** O(n)

**Example:**
```python
longest = z_algo.find_longest_repeated_substring()  # Returns "ana"
```

##### `get_text() -> str`

Get text string.

**Returns:**
- Text string

**Example:**
```python
text = z_algo.get_text()  # Returns "banana"
```

##### `get_length() -> int`

Get text length.

**Returns:**
- Length of text

**Example:**
```python
length = z_algo.get_length()  # Returns 6
```

## Usage Examples

### Basic Pattern Matching

```python
from src.main import ZAlgorithm

# Create Z-algorithm instance
z_algo = ZAlgorithm("banana")

# Search for pattern
occurrences = z_algo.search("ana")  # Returns [1, 3]

# Count occurrences
count = z_algo.count_occurrences("ana")  # Returns 2

# Check if substring exists
is_sub = z_algo.is_substring("ana")  # Returns True
```

### Multiple Pattern Matching

```python
z_algo = ZAlgorithm("banana")

# Search for multiple patterns
patterns = ["ana", "nan", "ban", "xyz"]
results = z_algo.search_all(patterns)

# Results: {"ana": [1, 3], "nan": [2], "ban": [0], "xyz": []}
for pattern, occurrences in results.items():
    print(f"Pattern '{pattern}': {occurrences}")
```

### Z-Array Analysis

```python
z_algo = ZAlgorithm("banana")

# Get Z-array for pattern
z_array = z_algo.get_z_array("ana")

# Get longest prefix match at position
match_length = z_algo.get_longest_prefix_match(1)
```

### Longest Repeated Substring

```python
z_algo = ZAlgorithm("banana")

# Find longest repeated substring
longest = z_algo.find_longest_repeated_substring()  # Returns "ana"
```

### All Occurrences with Positions

```python
z_algo = ZAlgorithm("banana")

# Get all occurrences with positions and lengths
occurrences = z_algo.find_all_occurrences("ana")
# Returns [(1, 3), (3, 3)]
```

## Error Handling

The implementation handles the following cases gracefully:

- **Empty text**: Raises `ValueError` during initialization
- **Empty pattern**: Raises `ValueError` for search operations
- **Empty patterns list**: Raises `ValueError` for multiple pattern search
- **Invalid position**: Raises `ValueError` for position queries
- **Configuration errors**: Falls back to defaults if config file missing

## Performance Characteristics

| Operation | Time Complexity | Space Complexity |
|-----------|----------------|------------------|
| Z-Array Construction | O(n) | O(n) |
| Single Pattern Search | O(n + m) | O(n + m) |
| Multiple Pattern Search | O(k(n + m)) | O(n + m) |
| Count Occurrences | O(n + m) | O(n + m) |
| Longest Prefix Match | O(n) | O(n) |
| Longest Repeated Substring | O(n) | O(n) |

Where:
- n = text length
- m = pattern length
- k = number of patterns

## Algorithm Details

### Z-Array Construction

The Z-array is constructed using a Z-box approach:

1. **Initialize**: Z[0] = n (entire string matches itself)
2. **Maintain Z-box**: Keep track of [left, right] interval
3. **Reuse values**: Use previously computed Z-values when possible
4. **Extend Z-box**: Compare characters to extend matches

### Pattern Matching Process

1. Concatenate: pattern + "$" + text
2. Compute Z-array for combined string
3. Find positions where Z[i] == pattern_length
4. Adjust positions to account for separator

### Z-Box Optimization

The algorithm uses a Z-box [left, right] to optimize:
- If current position is within Z-box, reuse Z[k] value
- If Z[k] extends beyond Z-box, extend Z-box
- Otherwise, compute new Z-box from scratch

## Thread Safety

This implementation is not thread-safe. For concurrent access, external synchronization is required.
