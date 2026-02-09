# Van Emde Boas Tree API Documentation

This document provides detailed API documentation for the van Emde Boas tree implementation with O(log log U) operations for integer priority queues.

## Classes

### VEBNode

Node in van Emde Boas tree.

#### Attributes

- `universe_size` (int): Size of universe (must be power of 2)
- `min` (Optional[int]): Minimum value in subtree
- `max` (Optional[int]): Maximum value in subtree
- `clusters` (Optional[List[VEBNode]]): Array of cluster nodes
- `summary` (Optional[VEBNode]): Summary node

#### Methods

##### `__init__(universe_size: int) -> None`

Initialize vEB node.

**Parameters:**
- `universe_size`: Size of universe (must be power of 2)

**Raises:**
- `ValueError`: If universe_size is not a power of 2

**Example:**
```python
node = VEBNode(16)
```

##### `is_empty() -> bool`

Check if node is empty.

**Returns:**
- `True` if empty, `False` otherwise

**Example:**
```python
if node.is_empty():
    print("Node is empty")
```

##### `high(x: int) -> int`

Get high bits (cluster index).

**Parameters:**
- `x`: Value

**Returns:**
- Cluster index

**Example:**
```python
cluster = node.high(10)  # For U=16, returns 2
```

##### `low(x: int) -> int`

Get low bits (position in cluster).

**Parameters:**
- `x`: Value

**Returns:**
- Position in cluster

**Example:**
```python
position = node.low(10)  # For U=16, returns 2
```

##### `index(high: int, low: int) -> int`

Combine high and low to get value.

**Parameters:**
- `high`: Cluster index
- `low`: Position in cluster

**Returns:**
- Combined value

**Example:**
```python
value = node.index(2, 2)  # Returns 10 for U=16
```

### VanEmdeBoasTree

Main class for van Emde Boas tree data structure.

#### Methods

##### `__init__(universe_size: int, config_path: str = "config.yaml") -> None`

Initialize van Emde Boas tree.

**Parameters:**
- `universe_size`: Size of universe [0, U-1] (must be power of 2)
- `config_path`: Path to configuration YAML file (default: "config.yaml")

**Raises:**
- `ValueError`: If universe_size is not a power of 2

**Example:**
```python
tree = VanEmdeBoasTree(universe_size=16)
```

##### `insert(x: int) -> bool`

Insert value into tree.

**Parameters:**
- `x`: Value to insert

**Returns:**
- `True` if inserted, `False` if already exists

**Raises:**
- `ValueError`: If value is out of universe range

**Time Complexity:** O(log log U)

**Example:**
```python
result = tree.insert(5)
if result:
    print("Inserted successfully")
```

##### `delete(x: int) -> bool`

Delete value from tree.

**Parameters:**
- `x`: Value to delete

**Returns:**
- `True` if deleted, `False` if not found

**Raises:**
- `ValueError`: If value is out of universe range

**Time Complexity:** O(log log U)

**Example:**
```python
result = tree.delete(5)
if result:
    print("Deleted successfully")
```

##### `contains(x: int) -> bool`

Check if value exists in tree.

**Parameters:**
- `x`: Value to check

**Returns:**
- `True` if exists, `False` otherwise

**Raises:**
- `ValueError`: If value is out of universe range

**Time Complexity:** O(log log U)

**Example:**
```python
exists = tree.contains(5)
if exists:
    print("Value exists")
```

##### `get_min() -> Optional[int]`

Get minimum value in tree.

**Returns:**
- Minimum value or `None` if empty

**Time Complexity:** O(1)

**Example:**
```python
min_val = tree.get_min()
if min_val is not None:
    print(f"Minimum: {min_val}")
```

##### `get_max() -> Optional[int]`

Get maximum value in tree.

**Returns:**
- Maximum value or `None` if empty

**Time Complexity:** O(1)

**Example:**
```python
max_val = tree.get_max()
if max_val is not None:
    print(f"Maximum: {max_val}")
```

##### `predecessor(x: int) -> Optional[int]`

Find predecessor of value.

**Parameters:**
- `x`: Value to find predecessor for

**Returns:**
- Predecessor or `None` if not found

**Raises:**
- `ValueError`: If value is out of universe range

**Time Complexity:** O(log log U)

**Example:**
```python
pred = tree.predecessor(7)
if pred is not None:
    print(f"Predecessor: {pred}")
```

##### `successor(x: int) -> Optional[int]`

Find successor of value.

**Parameters:**
- `x`: Value to find successor for

**Returns:**
- Successor or `None` if not found

**Raises:**
- `ValueError`: If value is out of universe range

**Time Complexity:** O(log log U)

**Example:**
```python
succ = tree.successor(5)
if succ is not None:
    print(f"Successor: {succ}")
```

##### `is_empty() -> bool`

Check if tree is empty.

**Returns:**
- `True` if empty, `False` otherwise

**Example:**
```python
if tree.is_empty():
    print("Tree is empty")
```

##### `get_size() -> int`

Get number of elements in tree.

**Returns:**
- Number of elements

**Example:**
```python
size = tree.get_size()
print(f"Tree size: {size}")
```

## Usage Examples

### Basic Operations

```python
from src.main import VanEmdeBoasTree

# Create vEB tree
tree = VanEmdeBoasTree(universe_size=16)

# Insert values
tree.insert(2)
tree.insert(5)
tree.insert(7)

# Get min/max
min_val = tree.get_min()  # 2
max_val = tree.get_max()  # 7

# Search
exists = tree.contains(5)  # True

# Predecessor/Successor
pred = tree.predecessor(7)  # 5
succ = tree.successor(2)   # 5

# Delete
tree.delete(5)
```

### Priority Queue Operations

```python
from src.main import VanEmdeBoasTree

tree = VanEmdeBoasTree(universe_size=256)

# Insert elements
for value in [10, 20, 30, 40, 50]:
    tree.insert(value)

# Extract minimum
while not tree.is_empty():
    min_val = tree.get_min()
    print(f"Extracted: {min_val}")
    tree.delete(min_val)
```

### Predecessor and Successor Queries

```python
from src.main import VanEmdeBoasTree

tree = VanEmdeBoasTree(universe_size=64)
values = [5, 10, 15, 20, 25, 30]

for value in values:
    tree.insert(value)

# Find predecessor
for x in [12, 18, 22]:
    pred = tree.predecessor(x)
    print(f"Predecessor of {x}: {pred}")

# Find successor
for x in [12, 18, 22]:
    succ = tree.successor(x)
    print(f"Successor of {x}: {succ}")
```

### Error Handling

```python
from src.main import VanEmdeBoasTree

# Invalid universe size
try:
    tree = VanEmdeBoasTree(universe_size=10)
except ValueError as e:
    print(f"Error: {e}")

# Valid universe size
tree = VanEmdeBoasTree(universe_size=16)

# Out of bounds
try:
    tree.insert(-1)
except ValueError as e:
    print(f"Error: {e}")

try:
    tree.insert(16)
except ValueError as e:
    print(f"Error: {e}")

# Duplicate insertion
tree.insert(5)
result = tree.insert(5)  # Returns False
if not result:
    print("Value already exists")
```

## Time Complexity Summary

| Operation | Time Complexity |
|-----------|----------------|
| `insert` | O(log log U) |
| `delete` | O(log log U) |
| `contains` | O(log log U) |
| `get_min` | O(1) |
| `get_max` | O(1) |
| `predecessor` | O(log log U) |
| `successor` | O(log log U) |
| `is_empty` | O(1) |
| `get_size` | O(1) |

Where U is the universe size.

## Notes

- Universe size must be a power of 2
- Values must be in range [0, U-1]
- Min and max operations are O(1)
- All other operations are O(log log U)
- Space complexity is O(U)
- Optimal for bounded universe integer sets
