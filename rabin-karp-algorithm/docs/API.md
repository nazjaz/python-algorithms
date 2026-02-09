# Rabin-Karp Algorithm API Documentation

This document provides detailed API documentation for the Rabin-Karp algorithm implementation for pattern matching with rolling hash.

## Classes

### RabinKarpAlgorithm

Main class for Rabin-Karp algorithm pattern matching operations.

#### Methods

##### `__init__(text: str, base: int = 256, modulus: int = 101, config_path: str = "config.yaml") -> None`

Initialize Rabin-Karp algorithm with text.

**Parameters:**
- `text`: Input text to search in
- `base`: Base for hash computation (default: 256)
- `modulus`: Modulus for hash computation (default: 101)
- `config_path`: Path to configuration YAML file (default: "config.yaml")

**Raises:**
- `ValueError`: If text is empty, base < 2, or modulus < 2

**Example:**
```python
rk = RabinKarpAlgorithm("ABABDABACDABABCABCAB", base=256, modulus=101)
```

##### `search(pattern: str, verify_collisions: bool = True) -> List[int]`

Search for pattern in text using Rabin-Karp algorithm.

**Parameters:**
- `pattern`: Pattern to search for
- `verify_collisions`: Whether to verify hash collisions (default: True)

**Returns:**
- List of starting positions where pattern occurs

**Raises:**
- `ValueError`: If pattern is empty

**Time Complexity:** O(n + m) average, O(nm) worst-case

**Example:**
```python
occurrences = rk.search("ABABCABCAB", verify_collisions=True)  # Returns [10]
```

##### `count_occurrences(pattern: str, verify_collisions: bool = True) -> int`

Count occurrences of pattern in text.

**Parameters:**
- `pattern`: Pattern to count
- `verify_collisions`: Whether to verify hash collisions (default: True)

**Returns:**
- Number of occurrences

**Raises:**
- `ValueError`: If pattern is empty

**Time Complexity:** O(n + m) average

**Example:**
```python
count = rk.count_occurrences("ABAB")  # Returns 2
```

##### `find_all_occurrences(pattern: str, verify_collisions: bool = True) -> List[Tuple[int, int]]`

Find all occurrences with their positions and lengths.

**Parameters:**
- `pattern`: Pattern to search for
- `verify_collisions`: Whether to verify hash collisions (default: True)

**Returns:**
- List of (position, length) tuples

**Raises:**
- `ValueError`: If pattern is empty

**Example:**
```python
occurrences = rk.find_all_occurrences("ABAB")
# Returns [(0, 4), (4, 4)]
```

##### `is_substring(pattern: str, verify_collisions: bool = True) -> bool`

Check if pattern is a substring of text.

**Parameters:**
- `pattern`: Pattern to check
- `verify_collisions`: Whether to verify hash collisions (default: True)

**Returns:**
- `True` if pattern found, `False` otherwise

**Raises:**
- `ValueError`: If pattern is empty

**Time Complexity:** O(n + m) average

**Example:**
```python
is_sub = rk.is_substring("ABC")  # Returns True
```

##### `get_hash(pattern: str) -> int`

Get hash value for pattern.

**Parameters:**
- `pattern`: Pattern to hash

**Returns:**
- Hash value

**Raises:**
- `ValueError`: If pattern is empty

**Time Complexity:** O(m) where m is pattern length

**Example:**
```python
pattern_hash = rk.get_hash("ABAB")  # Returns hash value
```

##### `search_all(patterns: List[str], verify_collisions: bool = True) -> Dict[str, List[int]]`

Search for multiple patterns in text.

**Parameters:**
- `patterns`: List of patterns to search for
- `verify_collisions`: Whether to verify hash collisions (default: True)

**Returns:**
- Dictionary mapping pattern to list of occurrences

**Raises:**
- `ValueError`: If patterns list is empty

**Time Complexity:** O(k(n + m)) average where k is number of patterns

**Example:**
```python
results = rk.search_all(["ABAB", "ABC", "AB"], verify_collisions=True)
# Returns {"ABAB": [0, 4], "ABC": [12, 15], "AB": [0, 2, 4, ...]}
```

##### `get_text() -> str`

Get text string.

**Returns:**
- Text string

**Example:**
```python
text = rk.get_text()  # Returns "ABABDABACDABABCABCAB"
```

##### `get_length() -> int`

Get text length.

**Returns:**
- Length of text

**Example:**
```python
length = rk.get_length()  # Returns 20
```

##### `get_base() -> int`

Get hash base.

**Returns:**
- Hash base value

**Example:**
```python
base = rk.get_base()  # Returns 256
```

##### `get_modulus() -> int`

Get hash modulus.

**Returns:**
- Hash modulus value

**Example:**
```python
modulus = rk.get_modulus()  # Returns 101
```

## Usage Examples

### Basic Pattern Matching

```python
from src.main import RabinKarpAlgorithm

# Create Rabin-Karp algorithm instance
rk = RabinKarpAlgorithm("ABABDABACDABABCABCAB", base=256, modulus=101)

# Search for pattern with collision verification
occurrences = rk.search("ABABCABCAB", verify_collisions=True)  # Returns [10]

# Count occurrences
count = rk.count_occurrences("ABAB")  # Returns 2

# Check if substring exists
is_sub = rk.is_substring("ABC")  # Returns True
```

### Rolling Hash Analysis

```python
rk = RabinKarpAlgorithm("banana", base=256, modulus=101)

# Get hash for pattern
pattern_hash = rk.get_hash("ana")  # Returns hash value

# Search with/without collision verification
occurrences_with = rk.search("ana", verify_collisions=True)
occurrences_without = rk.search("ana", verify_collisions=False)
```

### Multiple Pattern Matching

```python
rk = RabinKarpAlgorithm("ABABDABACDABABCABCAB")

# Search for multiple patterns
patterns = ["ABAB", "ABC", "AB", "XYZ"]
results = rk.search_all(patterns, verify_collisions=True)

# Results: {"ABAB": [0, 4], "ABC": [12, 15], "AB": [0, 2, 4, ...], "XYZ": []}
for pattern, occurrences in results.items():
    print(f"Pattern '{pattern}': {occurrences}")
```

### Custom Hash Parameters

```python
# Use custom base and modulus
rk = RabinKarpAlgorithm(
    "banana",
    base=31,
    modulus=1000000007  # Large prime for fewer collisions
)

occurrences = rk.search("ana", verify_collisions=True)
```

## Error Handling

The implementation handles the following cases gracefully:

- **Empty text**: Raises `ValueError` during initialization
- **Empty pattern**: Raises `ValueError` for search operations
- **Invalid base/modulus**: Raises `ValueError` for invalid values
- **Empty patterns list**: Raises `ValueError` for multiple pattern search
- **Configuration errors**: Falls back to defaults if config file missing

## Performance Characteristics

| Operation | Average Case | Worst Case | Space |
|-----------|-------------|------------|-------|
| Single Pattern Search | O(n + m) | O(nm) | O(1) |
| Multiple Pattern Search | O(k(n + m)) | O(knm) | O(1) |
| Rolling Hash Update | O(1) | O(1) | O(1) |
| Get Hash | O(m) | O(m) | O(1) |
| Count Occurrences | O(n + m) | O(nm) | O(1) |

Where:
- n = text length
- m = pattern length
- k = number of patterns

## Algorithm Details

### Rolling Hash Computation

The rolling hash computes hash for substring s[i..i+m-1] from hash of s[i-1..i+m-2]:

```
hash_new = ((hash_old - s[i-1] * base^(m-1)) * base + s[i+m-1]) % modulus
```

This allows O(1) update time for consecutive substrings.

### Collision Handling

When hash values match:
1. If `verify_collisions=True`: Compare actual strings to verify match
2. If `verify_collisions=False`: Accept hash match (may have false positives)

**Trade-off:**
- With verification: Correct results, slightly slower
- Without verification: Faster, may have false positives

### Pattern Matching Process

1. **Precompute**: Pattern hash - O(m)
2. **Initialize**: First text substring hash - O(m)
3. **For each position**:
   - Compare hashes
   - If match and verify_collisions, compare strings
   - Update hash using rolling hash - O(1)
4. **Return**: All occurrence positions

## Thread Safety

This implementation is not thread-safe. For concurrent access, external synchronization is required.
