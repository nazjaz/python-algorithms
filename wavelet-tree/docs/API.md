# Wavelet Tree API Documentation

This document provides detailed API documentation for the wavelet tree implementation with range queries and rank/select operations on sequences.

## Classes

### BitVector

Bit vector with rank and select support.

#### Methods

##### `__init__(bits: List[bool]) -> None`

Initialize bit vector.

**Parameters:**
- `bits`: List of boolean values

**Example:**
```python
bv = BitVector([True, False, True, True, False])
```

##### `rank(pos: int, bit: bool) -> int`

Compute rank of bit up to position.

**Parameters:**
- `pos`: Position (0-indexed, inclusive)
- `bit`: Bit value to rank

**Returns:**
- Number of occurrences of bit up to position

**Example:**
```python
rank = bv.rank(3, True)  # Number of True bits up to position 3
```

##### `select(k: int, bit: bool) -> Optional[int]`

Find position of k-th occurrence of bit.

**Parameters:**
- `k`: Occurrence number (1-indexed)
- `bit`: Bit value to select

**Returns:**
- Position of k-th occurrence or None if not found

**Example:**
```python
pos = bv.select(2, True)  # Position of 2nd True bit
```

##### `access(pos: int) -> bool`

Access bit at position.

**Parameters:**
- `pos`: Position

**Returns:**
- Bit value at position

**Example:**
```python
bit = bv.access(0)  # Bit at position 0
```

### WaveletNode

Node in wavelet tree.

#### Attributes

- `sequence` (List[int]): Sequence stored in node
- `alphabet_min` (int): Minimum value in alphabet
- `alphabet_max` (int): Maximum value in alphabet
- `level` (int): Level in tree
- `bitvector` (Optional[BitVector]): Bitvector for this level
- `left` (Optional[WaveletNode]): Left child node
- `right` (Optional[WaveletNode]): Right child node

### WaveletTree

Main class for wavelet tree data structure.

#### Methods

##### `__init__(sequence: List[int], config_path: str = "config.yaml") -> None`

Initialize wavelet tree.

**Parameters:**
- `sequence`: Sequence of integers
- `config_path`: Path to configuration YAML file (default: "config.yaml")

**Raises:**
- `ValueError`: If sequence is empty

**Time Complexity:** O(n log σ) construction

**Example:**
```python
sequence = [1, 2, 3, 1, 2, 3]
tree = WaveletTree(sequence)
```

##### `rank(pos: int, value: int) -> int`

Compute rank of value up to position.

**Parameters:**
- `pos`: Position in sequence (0-indexed, inclusive)
- `value`: Value to rank

**Returns:**
- Number of occurrences of value up to position

**Raises:**
- `ValueError`: If position is out of bounds

**Time Complexity:** O(log σ)

**Example:**
```python
rank = tree.rank(5, 1)  # Number of 1's up to position 5
```

##### `select(k: int, value: int) -> Optional[int]`

Find position of k-th occurrence of value.

**Parameters:**
- `k`: Occurrence number (1-indexed)
- `value`: Value to select

**Returns:**
- Position of k-th occurrence or None if not found

**Raises:**
- `ValueError`: If k <= 0

**Time Complexity:** O(log σ)

**Example:**
```python
pos = tree.select(2, 1)  # Position of 2nd occurrence of 1
```

##### `range_count(left: int, right: int, min_val: int, max_val: int) -> int`

Count elements in range [left, right] with values in [min_val, max_val].

**Parameters:**
- `left`: Left position (0-indexed, inclusive)
- `right`: Right position (0-indexed, inclusive)
- `min_val`: Minimum value
- `max_val`: Maximum value

**Returns:**
- Count of elements in range

**Raises:**
- `ValueError`: If positions are invalid

**Time Complexity:** O(log σ)

**Example:**
```python
count = tree.range_count(0, 5, 1, 2)  # Count values [1,2] in positions [0,5]
```

##### `access(pos: int) -> int`

Access element at position.

**Parameters:**
- `pos`: Position in sequence

**Returns:**
- Element at position

**Raises:**
- `ValueError`: If position is out of bounds

**Time Complexity:** O(1)

**Example:**
```python
value = tree.access(3)  # Element at position 3
```

##### `get_sequence() -> List[int]`

Get original sequence.

**Returns:**
- Original sequence

**Example:**
```python
sequence = tree.get_sequence()
```

## Usage Examples

### Basic Operations

```python
from src.main import WaveletTree

# Create wavelet tree
sequence = [1, 2, 3, 1, 2, 3, 1, 2, 3, 4, 5]
tree = WaveletTree(sequence)

# Rank operation
rank = tree.rank(5, 1)
print(f"Rank of 1 up to position 5: {rank}")

# Select operation
pos = tree.select(2, 1)
print(f"Position of 2nd occurrence of 1: {pos}")

# Range count
count = tree.range_count(0, 5, 1, 2)
print(f"Count of values [1,2] in positions [0,5]: {count}")

# Access
value = tree.access(3)
print(f"Value at position 3: {value}")
```

### Rank and Select Consistency

```python
from src.main import WaveletTree

sequence = [1, 2, 1, 3, 1, 2, 1]
tree = WaveletTree(sequence)

# Find 2nd occurrence of 1
pos = tree.select(2, 1)
if pos is not None:
    # Rank at that position should be at least 2
    rank = tree.rank(pos, 1)
    print(f"Position: {pos}, Rank: {rank}")
    assert rank >= 2
```

### Range Queries

```python
from src.main import WaveletTree

sequence = [1, 2, 3, 4, 5, 1, 2, 3, 4, 5]
tree = WaveletTree(sequence)

# Count values in range [2, 4] in positions [0, 9]
count = tree.range_count(0, 9, 2, 4)
print(f"Count: {count}")

# Count values in range [1, 3] in positions [5, 9]
count = tree.range_count(5, 9, 1, 3)
print(f"Count: {count}")
```

### Error Handling

```python
from src.main import WaveletTree

# Empty sequence
try:
    tree = WaveletTree([])
except ValueError as e:
    print(f"Error: {e}")

# Out of bounds
sequence = [1, 2, 3]
tree = WaveletTree(sequence)

try:
    tree.rank(-1, 1)
except ValueError as e:
    print(f"Error: {e}")

try:
    tree.select(0, 1)
except ValueError as e:
    print(f"Error: {e}")

# Invalid range
try:
    tree.range_count(5, 0, 1, 3)
except ValueError as e:
    print(f"Error: {e}")
```

## Time Complexity Summary

| Operation | Time Complexity |
|-----------|----------------|
| Construction | O(n log σ) |
| `rank` | O(log σ) |
| `select` | O(log σ) |
| `range_count` | O(log σ) |
| `access` | O(1) |
| `get_sequence` | O(n) |

Where n is the sequence length and σ is the alphabet size.

## Notes

- Wavelet trees require preprocessing before queries
- Preprocessing is done automatically in constructor
- Rank and select operations work on any value in alphabet
- Range count efficiently handles value ranges
- Access operation is O(1) direct array access
- Performance depends on log of alphabet size, not sequence length
