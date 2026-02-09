# Manacher's Algorithm API Documentation

This document provides detailed API documentation for the Manacher's algorithm implementation for finding longest palindromic substring.

## Classes

### ManacherAlgorithm

Main class for Manacher's algorithm operations.

#### Methods

##### `__init__(text: str, config_path: str = "config.yaml") -> None`

Initialize Manacher's algorithm with text.

**Parameters:**
- `text`: Input string to analyze
- `config_path`: Path to configuration YAML file (default: "config.yaml")

**Raises:**
- `ValueError`: If text is empty

**Example:**
```python
manacher = ManacherAlgorithm("babad")
```

##### `get_longest_palindrome() -> str`

Get longest palindromic substring.

**Returns:**
- Longest palindromic substring

**Time Complexity:** O(1) (computed during initialization)

**Example:**
```python
longest = manacher.get_longest_palindrome()  # Returns "bab" or "aba"
```

##### `get_longest_palindrome_info() -> Tuple[str, int, int]`

Get longest palindrome with position and length.

**Returns:**
- Tuple of (palindrome, start_position, length)

**Time Complexity:** O(1)

**Example:**
```python
info = manacher.get_longest_palindrome_info()
# Returns ("bab", 0, 3)
```

##### `get_all_palindromes() -> List[Tuple[str, int, int]]`

Get all palindromic substrings with positions and lengths.

**Returns:**
- List of (palindrome, start_position, length) tuples sorted by length

**Time Complexity:** O(n)

**Example:**
```python
all_palindromes = manacher.get_all_palindromes()
# Returns [(palindrome, start, length), ...] sorted by length
```

##### `count_palindromes() -> int`

Count total number of palindromic substrings.

**Returns:**
- Number of palindromic substrings

**Time Complexity:** O(n)

**Example:**
```python
count = manacher.count_palindromes()  # Returns total count
```

##### `is_palindrome_at(start: int, length: int) -> bool`

Check if substring at position is palindrome.

**Parameters:**
- `start`: Start position in original text
- `length`: Length of substring

**Returns:**
- `True` if palindrome, `False` otherwise

**Raises:**
- `ValueError`: If position or length is invalid

**Time Complexity:** O(1)

**Example:**
```python
is_pal = manacher.is_palindrome_at(0, 3)  # Returns True/False
```

##### `get_palindrome_radii() -> List[int]`

Get palindrome radii array.

**Returns:**
- Copy of palindrome radii array

**Example:**
```python
radii = manacher.get_palindrome_radii()
```

##### `get_text() -> str`

Get original text.

**Returns:**
- Original text string

**Example:**
```python
text = manacher.get_text()  # Returns "babad"
```

##### `get_length() -> int`

Get text length.

**Returns:**
- Length of text

**Example:**
```python
length = manacher.get_length()  # Returns 5
```

##### `is_valid() -> bool`

Validate algorithm results.

**Returns:**
- `True` if valid, `False` otherwise

**Time Complexity:** O(1)

**Example:**
```python
if manacher.is_valid():
    print("Algorithm results are valid")
```

## Usage Examples

### Basic Operations

```python
from src.main import ManacherAlgorithm

# Create Manacher's algorithm instance
manacher = ManacherAlgorithm("babad")

# Get longest palindrome
longest = manacher.get_longest_palindrome()  # Returns "bab" or "aba"

# Get longest palindrome info
info = manacher.get_longest_palindrome_info()
palindrome, start, length = info
print(f"Palindrome: {palindrome}, Start: {start}, Length: {length}")
```

### All Palindromes

```python
manacher = ManacherAlgorithm("babad")

# Get all palindromes
all_palindromes = manacher.get_all_palindromes()
for palindrome, start, length in all_palindromes:
    print(f"'{palindrome}' at position {start}, length {length}")
```

### Palindrome Counting

```python
manacher = ManacherAlgorithm("babad")

# Count total palindromes
count = manacher.count_palindromes()
print(f"Total palindromic substrings: {count}")
```

### Palindrome Validation

```python
manacher = ManacherAlgorithm("racecar")

# Check if substring is palindrome
is_pal = manacher.is_palindrome_at(0, 7)  # Returns True
is_pal = manacher.is_palindrome_at(1, 5)  # Returns True (aceca)
is_pal = manacher.is_palindrome_at(0, 3)  # Returns False (rac)
```

### Different Text Types

```python
# Even length palindrome
manacher = ManacherAlgorithm("abba")
longest = manacher.get_longest_palindrome()  # Returns "abba"

# Odd length palindrome
manacher = ManacherAlgorithm("racecar")
longest = manacher.get_longest_palindrome()  # Returns "racecar"

# All same characters
manacher = ManacherAlgorithm("aaa")
longest = manacher.get_longest_palindrome()  # Returns "aaa"
```

## Error Handling

The implementation handles the following cases gracefully:

- **Empty text**: Raises `ValueError` during initialization
- **Invalid position**: Raises `ValueError` for out-of-bounds positions
- **Invalid length**: Raises `ValueError` for invalid substring lengths
- **Configuration errors**: Falls back to defaults if config file missing

## Performance Characteristics

| Operation | Time Complexity | Space Complexity |
|-----------|----------------|------------------|
| Initialization | O(n) | O(n) |
| Get Longest Palindrome | O(1) | O(1) |
| Get Longest Palindrome Info | O(1) | O(1) |
| Get All Palindromes | O(n) | O(n) |
| Count Palindromes | O(n) | O(1) |
| Is Palindrome At | O(1) | O(1) |
| Validation | O(1) | O(1) |

Where n is the text length.

## Algorithm Details

### Text Transformation

The algorithm transforms the text to handle both odd and even length palindromes:
- Original: "aba"
- Transformed: "^#a#b#a#$"
- Separators (#) allow uniform handling

### Center and Right Boundary

The algorithm maintains:
- **Center**: Center of rightmost palindrome
- **Right**: Right boundary of rightmost palindrome
- **Mirror**: Position mirrored across center

### Z-Box Optimization

For position i:
1. If i is within [center, right], use mirror value
2. Otherwise, expand from center
3. Update center and right if palindrome extends further

This optimization ensures each character is compared at most once, achieving O(n) time complexity.

## Thread Safety

This implementation is not thread-safe. For concurrent access, external synchronization is required.
