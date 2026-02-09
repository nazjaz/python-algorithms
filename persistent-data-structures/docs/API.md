# Persistent Data Structures API Documentation

This document provides detailed API documentation for the persistent arrays and lists implementation with path copying technique.

## Classes

### PersistentNode

Node in persistent tree structure.

#### Attributes

- `left` (Optional[PersistentNode]): Left child node
- `right` (Optional[PersistentNode]): Right child node
- `value` (Any): Value stored in leaf node
- `size` (int): Size of subtree

#### Methods

##### `__init__(left: Optional[PersistentNode] = None, right: Optional[PersistentNode] = None, value: Any = None, size: int = 0) -> None`

Initialize persistent node.

**Parameters:**
- `left`: Left child node
- `right`: Right child node
- `value`: Value stored in leaf node
- `size`: Size of subtree

**Example:**
```python
node = PersistentNode(value=5, size=1)
```

##### `is_leaf() -> bool`

Check if node is a leaf.

**Returns:**
- `True` if leaf, `False` otherwise

**Example:**
```python
if node.is_leaf():
    print("Node is a leaf")
```

##### `copy() -> PersistentNode`

Create a copy of this node.

**Returns:**
- New node with same structure

**Example:**
```python
copied = node.copy()
```

### PersistentArray

Persistent array with path copying technique.

#### Methods

##### `__init__(initial_data: Optional[List[Any]] = None, config_path: str = "config.yaml") -> None`

Initialize persistent array.

**Parameters:**
- `initial_data`: Initial array data
- `config_path`: Path to configuration YAML file (default: "config.yaml")

**Example:**
```python
arr = PersistentArray([1, 2, 3, 4, 5])
```

##### `get(version: int, index: int) -> Any`

Get value at index in specific version.

**Parameters:**
- `version`: Version number
- `index`: Index to get

**Returns:**
- Value at index

**Raises:**
- `IndexError`: If version or index is invalid

**Time Complexity:** O(log n)

**Example:**
```python
value = arr.get(0, 2)  # Get value at index 2 in version 0
```

##### `set(version: int, index: int, value: Any) -> int`

Set value at index in specific version, creating new version.

**Parameters:**
- `version`: Version number to base on
- `index`: Index to set
- `value`: New value

**Returns:**
- New version number

**Raises:**
- `IndexError`: If version or index is invalid

**Time Complexity:** O(log n)

**Example:**
```python
v1 = arr.set(0, 2, 10)  # Set index 2 to 10, creating version 1
```

##### `get_current_version() -> int`

Get current version number.

**Returns:**
- Current version number

**Example:**
```python
current = arr.get_current_version()
```

##### `get_size(version: int) -> int`

Get size of array in specific version.

**Parameters:**
- `version`: Version number

**Returns:**
- Size of array

**Raises:**
- `IndexError`: If version is invalid

**Example:**
```python
size = arr.get_size(0)
```

### PersistentList

Persistent list with path copying technique.

#### Methods

##### `__init__(initial_data: Optional[List[Any]] = None, config_path: str = "config.yaml") -> None`

Initialize persistent list.

**Parameters:**
- `initial_data`: Initial list data
- `config_path`: Path to configuration YAML file (default: "config.yaml")

**Example:**
```python
lst = PersistentList([10, 20, 30])
```

##### `get(version: int, index: int) -> Any`

Get value at index in specific version.

**Parameters:**
- `version`: Version number
- `index`: Index to get

**Returns:**
- Value at index

**Raises:**
- `IndexError`: If version or index is invalid

**Time Complexity:** O(log n)

**Example:**
```python
value = lst.get(0, 1)  # Get value at index 1 in version 0
```

##### `set(version: int, index: int, value: Any) -> int`

Set value at index in specific version, creating new version.

**Parameters:**
- `version`: Version number to base on
- `index`: Index to set
- `value`: New value

**Returns:**
- New version number

**Raises:**
- `IndexError`: If version or index is invalid

**Time Complexity:** O(log n)

**Example:**
```python
v1 = lst.set(0, 1, 25)  # Set index 1 to 25, creating version 1
```

##### `append(version: int, value: Any) -> int`

Append value to list in specific version, creating new version.

**Parameters:**
- `version`: Version number to base on
- `value`: Value to append

**Returns:**
- New version number

**Raises:**
- `IndexError`: If version is invalid

**Time Complexity:** O(log n)

**Example:**
```python
v1 = lst.append(0, 40)  # Append 40, creating version 1
```

##### `get_current_version() -> int`

Get current version number.

**Returns:**
- Current version number

**Example:**
```python
current = lst.get_current_version()
```

##### `get_size(version: int) -> int`

Get size of list in specific version.

**Parameters:**
- `version`: Version number

**Returns:**
- Size of list

**Raises:**
- `IndexError`: If version is invalid

**Example:**
```python
size = lst.get_size(0)
```

## Usage Examples

### Persistent Array

```python
from src.main import PersistentArray

# Create array
arr = PersistentArray([1, 2, 3, 4, 5])
v0 = arr.get_current_version()

# Get value
value = arr.get(v0, 2)  # 3

# Create new version by modifying
v1 = arr.set(v0, 2, 10)

# Old version still accessible
print(arr.get(v0, 2))  # 3
print(arr.get(v1, 2))  # 10

# Multiple modifications
v2 = arr.set(v1, 0, 20)
v3 = arr.set(v2, 4, 50)

# All versions accessible
print(arr.get(v0, 0))  # 1
print(arr.get(v1, 0))  # 1
print(arr.get(v2, 0))  # 20
print(arr.get(v3, 4))  # 50
```

### Persistent List

```python
from src.main import PersistentList

# Create list
lst = PersistentList([10, 20, 30])
v0 = lst.get_current_version()

# Append creates new version
v1 = lst.append(v0, 40)
v2 = lst.append(v1, 50)

# Set creates new version
v3 = lst.set(v2, 1, 25)

# All versions accessible
print([lst.get(v0, i) for i in range(lst.get_size(v0))])  # [10, 20, 30]
print([lst.get(v1, i) for i in range(lst.get_size(v1))])  # [10, 20, 30, 40]
print([lst.get(v2, i) for i in range(lst.get_size(v2))])  # [10, 20, 30, 40, 50]
print([lst.get(v3, i) for i in range(lst.get_size(v3))])  # [10, 25, 30, 40, 50]
```

### Version Management

```python
from src.main import PersistentArray

arr = PersistentArray([1, 2, 3])
v0 = arr.get_current_version()

# Create multiple versions
versions = [v0]
for i in range(5):
    new_v = arr.set(versions[-1], 0, i * 10)
    versions.append(new_v)

# Access any version
for v in versions:
    print(f"Version {v}: {arr.get(v, 0)}")
```

### Error Handling

```python
from src.main import PersistentArray

arr = PersistentArray([1, 2, 3])

# Invalid version
try:
    arr.get(10, 0)
except IndexError as e:
    print(f"Error: {e}")

# Out of bounds index
try:
    arr.get(0, 10)
except IndexError as e:
    print(f"Error: {e}")

# Set with invalid version
try:
    arr.set(10, 0, 100)
except IndexError as e:
    print(f"Error: {e}")
```

## Time Complexity Summary

| Operation | Time Complexity |
|-----------|----------------|
| `get` | O(log n) |
| `set` | O(log n) |
| `append` | O(log n) |
| `get_size` | O(1) |
| `get_current_version` | O(1) |

Where n is the size of the array/list.

## Space Complexity

- Per operation: O(log n)
- Total for k operations: O(k log n)
- Unchanged subtrees are shared
- Only modified paths are copied

## Notes

- Persistent data structures maintain all previous versions
- Path copying creates new versions by copying only modified paths
- Unchanged subtrees are shared between versions
- All versions remain accessible and immutable
- Optimal for version management and undo/redo functionality
