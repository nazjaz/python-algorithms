# Fenwick Tree API Documentation

This document provides detailed API documentation for the Fenwick tree (Binary Indexed Tree) implementation.

## Classes

### FenwickTree

Main class for Fenwick tree data structure supporting range sum queries and point updates.

#### Methods

##### `__init__(size: Optional[int] = None, array: Optional[List[int]] = None, config_path: str = "config.yaml") -> None`

Initialize Fenwick tree.

**Parameters:**
- `size`: Size of the tree (if creating empty tree)
- `array`: Initial array values (if constructing from array)
- `config_path`: Path to configuration YAML file (default: "config.yaml")

**Raises:**
- `ValueError`: If neither size nor array provided, or both provided, or size < 1

**Example:**
```python
# From array
tree = FenwickTree(array=[1, 2, 3, 4, 5])

# Empty tree
tree = FenwickTree(size=10)
```

##### `update(index: int, delta: int) -> None`

Update element at index by adding delta.

**Parameters:**
- `index`: Index to update (0-indexed)
- `delta`: Value to add to element at index

**Raises:**
- `ValueError`: If index is out of bounds

**Time Complexity:** O(log n)

**Example:**
```python
tree.update(2, 5)  # Add 5 to element at index 2
```

##### `set_value(index: int, value: int) -> None`

Set element at index to specific value.

**Parameters:**
- `index`: Index to set (0-indexed)
- `value`: New value for element at index

**Raises:**
- `ValueError`: If index is out of bounds

**Time Complexity:** O(log n)

**Example:**
```python
tree.set_value(3, 20)  # Set element at index 3 to 20
```

##### `prefix_sum(index: int) -> int`

Get prefix sum from index 0 to index (inclusive).

**Parameters:**
- `index`: End index (0-indexed, inclusive)

**Returns:**
- Sum of elements from index 0 to index

**Raises:**
- `ValueError`: If index is out of bounds

**Time Complexity:** O(log n)

**Example:**
```python
sum_0_to_4 = tree.prefix_sum(4)  # Sum of elements [0, 1, 2, 3, 4]
```

##### `range_sum(left: int, right: int) -> int`

Get sum of elements from left to right (inclusive).

**Parameters:**
- `left`: Start index (0-indexed, inclusive)
- `right`: End index (0-indexed, inclusive)

**Returns:**
- Sum of elements from left to right

**Raises:**
- `ValueError`: If indices are out of bounds or left > right

**Time Complexity:** O(log n)

**Example:**
```python
sum_1_to_4 = tree.range_sum(1, 4)  # Sum of elements [1, 2, 3, 4]
```

##### `get_value(index: int) -> int`

Get value at specific index.

**Parameters:**
- `index`: Index to query (0-indexed)

**Returns:**
- Value at index

**Raises:**
- `ValueError`: If index is out of bounds

**Time Complexity:** O(1)

**Example:**
```python
value = tree.get_value(2)  # Get value at index 2
```

##### `get_size() -> int`

Get size of the tree.

**Returns:**
- Number of elements in the tree

**Example:**
```python
size = tree.get_size()  # Returns number of elements
```

##### `get_all_values() -> List[int]`

Get all values in the tree.

**Returns:**
- List of all values

**Example:**
```python
values = tree.get_all_values()  # Returns [1, 2, 3, 4, 5]
```

##### `get_tree_array() -> List[int]`

Get internal tree array (for debugging).

**Returns:**
- Internal tree array (1-indexed)

**Example:**
```python
tree_array = tree.get_tree_array()  # Internal representation
```

##### `is_valid() -> bool`

Validate tree structure.

**Returns:**
- `True` if tree is valid, `False` otherwise

**Time Complexity:** O(n log n)

**Example:**
```python
is_valid = tree.is_valid()  # Validates tree structure
```

## Usage Examples

### Basic Operations

```python
from src.main import FenwickTree

# Create tree from array
array = [1, 3, 5, 7, 9, 11]
tree = FenwickTree(array=array)

# Query prefix sum
prefix = tree.prefix_sum(4)  # Sum of [1, 3, 5, 7, 9] = 25

# Query range sum
range_sum = tree.range_sum(1, 4)  # Sum of [3, 5, 7, 9] = 24

# Update element
tree.update(2, 5)  # Add 5 to element at index 2
# Now array is [1, 3, 10, 7, 9, 11]

# Set value
tree.set_value(3, 20)  # Set element at index 3 to 20
# Now array is [1, 3, 10, 20, 9, 11]

# Get value
value = tree.get_value(2)  # Returns 10
```

### Empty Tree Initialization

```python
# Create empty tree
tree = FenwickTree(size=10)

# Update elements
for i in range(10):
    tree.update(i, i + 1)

# Query range
total = tree.range_sum(0, 9)  # Sum of 1 to 10 = 55
```

### Dynamic Updates and Queries

```python
tree = FenwickTree(array=[0] * 100)

# Multiple updates
tree.update(10, 5)
tree.update(20, 10)
tree.update(30, 15)

# Query ranges
sum_0_to_50 = tree.range_sum(0, 50)  # 30
sum_10_to_30 = tree.range_sum(10, 30)  # 30
```

### Validation

```python
tree = FenwickTree(array=[1, 2, 3, 4, 5])

# Validate tree structure
if tree.is_valid():
    print("Tree is valid")
else:
    print("Tree structure error")
```

## Error Handling

The implementation handles the following cases gracefully:

- **Invalid initialization**: Raises `ValueError` if neither size nor array provided
- **Out of bounds**: Raises `ValueError` for invalid indices
- **Invalid range**: Raises `ValueError` if left > right in range query
- **Configuration errors**: Falls back to defaults if config file missing

## Performance Characteristics

| Operation | Time Complexity | Space Complexity |
|-----------|----------------|------------------|
| Construction | O(n log n) | O(n) |
| Update | O(log n) | O(1) |
| Set Value | O(log n) | O(1) |
| Prefix Sum | O(log n) | O(1) |
| Range Sum | O(log n) | O(1) |
| Get Value | O(1) | O(1) |
| Validation | O(n log n) | O(1) |

Where n is the number of elements in the tree.

## Algorithm Details

### Least Significant Bit (LSB)

The Fenwick tree uses the least significant bit to determine which elements each tree node covers:

- Index i covers LSB(i) elements
- LSB is computed using: `i & (-i)`

### Update Operation

1. Update original array
2. Add delta to tree[index + 1]
3. Move to next index: `index += LSB(index)`
4. Repeat until index > n

### Prefix Sum Operation

1. Start with index + 1
2. Add tree[index] to result
3. Move to previous index: `index -= LSB(index)`
4. Repeat until index == 0

### Range Sum Operation

Uses prefix sums:
- `range_sum(left, right) = prefix_sum(right) - prefix_sum(left - 1)`
- Special case: if left == 0, just return `prefix_sum(right)`

## Thread Safety

This implementation is not thread-safe. For concurrent access, external synchronization is required.
