# Rolling Hash API Documentation

## Classes

### RollingHash

Main class for rolling hash with multiple moduli implementation.

#### Constants

- `DEFAULT_MODULI`: `[10**9 + 7, 10**9 + 9, 10**9 + 21]` - Default prime moduli
- `DEFAULT_BASE`: `256` - Default base for polynomial hash

#### Methods

##### `__init__(self, moduli: Optional[List[int]] = None, base: int = DEFAULT_BASE) -> None`

Initialize rolling hash with specified moduli and base.

**Parameters**:
- `moduli` (Optional[List[int]]): List of prime moduli to use. Defaults to large primes.
- `base` (int): Base for polynomial hash. Should be larger than alphabet size. Default: 256.

**Raises**:
- `ValueError`: If moduli list is empty or base is invalid.

**Example**:
```python
rh = RollingHash()
rh = RollingHash(moduli=[1000000007, 1000000009], base=131)
```

---

##### `hash_string(self, text: str) -> Tuple[int, ...]`

Compute hash of a string using all moduli.

**Parameters**:
- `text` (str): String to hash.

**Returns**:
- `Tuple[int, ...]`: Tuple of hash values, one for each modulus.

**Example**:
```python
rh = RollingHash()
hashes = rh.hash_string("hello")
# Returns: (1234567890, 9876543210, 5555555555)
```

---

##### `hash_substring(self, text: str, start: int, length: int) -> Tuple[int, ...]`

Compute hash of a substring using all moduli.

**Parameters**:
- `text` (str): Source string.
- `start` (int): Starting index of substring.
- `length` (int): Length of substring.

**Returns**:
- `Tuple[int, ...]`: Tuple of hash values for the substring.

**Raises**:
- `IndexError`: If start or length is out of bounds.

**Example**:
```python
rh = RollingHash()
text = "hello world"
hash_value = rh.hash_substring(text, 0, 5)
# Returns hash of "hello"
```

---

##### `build_prefix_hashes(self, text: str) -> List[List[int]]`

Build prefix hash array for efficient substring queries.

**Parameters**:
- `text` (str): String to build prefix hashes for.

**Returns**:
- `List[List[int]]`: List of lists, where each inner list contains prefix hashes for one modulus.

**Example**:
```python
rh = RollingHash()
text = "hello"
prefix_hashes = rh.build_prefix_hashes(text)
# Returns: [[0, h1, h2, h3, h4, h5], [0, h1, h2, h3, h4, h5], ...]
```

---

##### `get_substring_hash_from_prefix(self, prefix_hashes: List[List[int]], start: int, length: int) -> Tuple[int, ...]`

Get substring hash from prefix hash array in O(1) time.

Uses the formula: `hash(s[l:r]) = (prefix[r] - prefix[l] * base^(r-l)) mod m`

**Parameters**:
- `prefix_hashes` (List[List[int]]): Prefix hash array from `build_prefix_hashes`.
- `start` (int): Starting index of substring.
- `length` (int): Length of substring.

**Returns**:
- `Tuple[int, ...]`: Tuple of hash values for the substring.

**Raises**:
- `IndexError`: If indices are out of bounds.
- `ValueError`: If prefix_hashes structure is invalid.

**Example**:
```python
rh = RollingHash()
text = "hello world"
prefix_hashes = rh.build_prefix_hashes(text)
hash_value = rh.get_substring_hash_from_prefix(prefix_hashes, 0, 5)
# Returns hash of "hello" in O(1) time
```

---

##### `find_pattern(self, text: str, pattern: str) -> List[int]`

Find all occurrences of pattern in text using rolling hash.

**Parameters**:
- `text` (str): Text to search in.
- `pattern` (str): Pattern to search for.

**Returns**:
- `List[int]`: List of starting indices where pattern occurs.

**Example**:
```python
rh = RollingHash()
text = "abababab"
pattern = "ab"
occurrences = rh.find_pattern(text, pattern)
# Returns: [0, 2, 4, 6]
```

---

##### `compare_substrings(self, text1: str, start1: int, text2: str, start2: int, length: int) -> bool`

Compare two substrings using hashing.

**Parameters**:
- `text1` (str): First text.
- `start1` (int): Starting index in first text.
- `text2` (str): Second text.
- `start2` (int): Starting index in second text.
- `length` (int): Length of substrings to compare.

**Returns**:
- `bool`: True if substrings are equal, False otherwise.

**Raises**:
- `IndexError`: If indices are out of bounds.

**Example**:
```python
rh = RollingHash()
text1 = "hello world"
text2 = "hello there"
are_equal = rh.compare_substrings(text1, 0, text2, 0, 5)
# Returns: True (both start with "hello")
```

---

##### `longest_common_prefix_hash(self, text1: str, start1: int, text2: str, start2: int) -> int`

Find longest common prefix of two substrings using binary search.

**Parameters**:
- `text1` (str): First text.
- `start1` (int): Starting index in first text.
- `text2` (str): Second text.
- `start2` (int): Starting index in second text.

**Returns**:
- `int`: Length of longest common prefix.

**Raises**:
- `IndexError`: If indices are out of bounds.

**Example**:
```python
rh = RollingHash()
text1 = "hello world"
text2 = "hello there"
lcp = rh.longest_common_prefix_hash(text1, 0, text2, 0)
# Returns: 6 (common prefix is "hello ")
```

---

## Internal Methods

The following methods are used internally and are not part of the public API, but are documented for completeness:

##### `_compute_powers(self, length: int) -> None`

Precompute powers of base modulo each modulus.

##### `_roll_hash(self, current_hash: Tuple[int, ...], remove_char: str, add_char: str, pattern_length: int) -> Tuple[int, ...]`

Roll the hash by removing one character and adding another.

---

## Usage Examples

### Basic Hashing

```python
from src.main import RollingHash

rh = RollingHash()
text = "hello world"
hashes = rh.hash_string(text)
print(f"Hash values: {hashes}")
```

### Efficient Substring Queries

```python
rh = RollingHash()
text = "hello world"
prefix_hashes = rh.build_prefix_hashes(text)

# Query any substring in O(1) time
for i in range(len(text)):
    for length in range(1, len(text) - i + 1):
        hash_value = rh.get_substring_hash_from_prefix(prefix_hashes, i, length)
```

### Pattern Matching

```python
rh = RollingHash()
text = "abababab"
pattern = "ab"
occurrences = rh.find_pattern(text, pattern)
print(f"Pattern found at: {occurrences}")
```

### Substring Comparison

```python
rh = RollingHash()
text1 = "hello world"
text2 = "hello there"

# Compare first 5 characters
are_equal = rh.compare_substrings(text1, 0, text2, 0, 5)
print(f"First 5 chars equal: {are_equal}")
```

---

## Performance Characteristics

- **Hash computation**: O(n) where n is string length
- **Substring hash (direct)**: O(k) where k is substring length
- **Substring hash (from prefix)**: O(1) after O(n) preprocessing
- **Pattern matching**: O(n + m) where n is text length, m is pattern length
- **Substring comparison**: O(k) where k is substring length
- **Longest common prefix**: O(log(min(n1, n2))) where n1, n2 are substring lengths

---

## Notes

- Multiple moduli significantly reduce hash collision probability
- Default moduli are large primes chosen for good collision resistance
- Base should be larger than the alphabet size (256 works for ASCII/extended ASCII)
- Hash values are computed modulo each prime separately
- All hash operations are deterministic and consistent
