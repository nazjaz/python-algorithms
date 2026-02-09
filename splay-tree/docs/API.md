# Splay Tree API Documentation

This document provides detailed API documentation for the splay tree implementation with amortized analysis and self-adjusting operations.

## Classes

### SplayNode

Represents a node in the splay tree.

#### Attributes

- `key` (int): Node key value
- `left` (Optional[SplayNode]): Left child node
- `right` (Optional[SplayNode]): Right child node
- `parent` (Optional[SplayNode]): Parent node

#### Methods

##### `__init__(key: int) -> None`

Initialize SplayNode.

**Parameters:**
- `key`: Node key value

**Example:**
```python
node = SplayNode(10)
```

### SplayTree

Main class for splay tree data structure with self-adjusting operations.

#### Methods

##### `__init__(config_path: str = "config.yaml") -> None`

Initialize splay tree.

**Parameters:**
- `config_path`: Path to configuration YAML file (default: "config.yaml")

**Example:**
```python
tree = SplayTree()
```

##### `insert(key: int) -> bool`

Insert key into splay tree and splay to root.

**Parameters:**
- `key`: Key to insert

**Returns:**
- `True` if insertion successful, `False` if key already exists

**Time Complexity:** O(log n) amortized

**Example:**
```python
tree.insert(10)  # Returns True
tree.insert(10)  # Returns False (duplicate)
```

##### `search(key: int) -> Optional[SplayNode]`

Search for key in splay tree and splay to root.

**Parameters:**
- `key`: Key to search for

**Returns:**
- Node if found, `None` otherwise. If key not found, last visited node is splayed to root.

**Time Complexity:** O(log n) amortized

**Example:**
```python
node = tree.search(10)  # Returns node if found, None otherwise
```

##### `delete(key: int) -> bool`

Delete key from splay tree.

**Parameters:**
- `key`: Key to delete

**Returns:**
- `True` if deletion successful, `False` if key not found

**Time Complexity:** O(log n) amortized

**Example:**
```python
tree.delete(10)  # Returns True if deleted
```

##### `find_min() -> Optional[int]`

Find minimum key in tree and splay to root.

**Returns:**
- Minimum key if tree is not empty, `None` otherwise

**Time Complexity:** O(log n) amortized

**Example:**
```python
min_key = tree.find_min()  # Returns minimum key
```

##### `find_max() -> Optional[int]`

Find maximum key in tree and splay to root.

**Returns:**
- Maximum key if tree is not empty, `None` otherwise

**Time Complexity:** O(log n) amortized

**Example:**
```python
max_key = tree.find_max()  # Returns maximum key
```

##### `inorder_traversal() -> List[int]`

Perform inorder traversal of tree.

**Returns:**
- List of keys in sorted order

**Time Complexity:** O(n)

**Example:**
```python
keys = tree.inorder_traversal()  # Returns sorted list
```

##### `preorder_traversal() -> List[int]`

Perform preorder traversal of tree.

**Returns:**
- List of keys in preorder

**Time Complexity:** O(n)

**Example:**
```python
keys = tree.preorder_traversal()
```

##### `postorder_traversal() -> List[int]`

Perform postorder traversal of tree.

**Returns:**
- List of keys in postorder

**Time Complexity:** O(n)

**Example:**
```python
keys = tree.postorder_traversal()
```

##### `get_amortized_analysis() -> dict`

Get amortized analysis statistics.

**Returns:**
- Dictionary containing:
  - `total_operations`: Total number of operations performed
  - `total_splay_operations`: Total number of splay operations
  - `total_rotations`: Total number of rotations performed
  - `average_rotations_per_splay`: Average rotations per splay operation
  - `amortized_cost_per_operation`: Average rotations per operation

**Example:**
```python
analysis = tree.get_amortized_analysis()
print(analysis['total_operations'])
print(analysis['average_rotations_per_splay'])
```

##### `reset_statistics() -> None`

Reset all operation statistics.

**Example:**
```python
tree.reset_statistics()
```

##### `size() -> int`

Get number of nodes in tree.

**Returns:**
- Number of nodes

**Time Complexity:** O(n)

**Example:**
```python
count = tree.size()
```

##### `is_empty() -> bool`

Check if tree is empty.

**Returns:**
- `True` if empty, `False` otherwise

**Time Complexity:** O(1)

**Example:**
```python
if tree.is_empty():
    print("Tree is empty")
```

## Internal Methods

### `_zig(node: SplayNode) -> None`

Perform zig rotation (single rotation).

**Parameters:**
- `node`: Node to rotate

**Note:** This is an internal method used by splay operations.

### `_zig_zig(node: SplayNode) -> None`

Perform zig-zig rotation (two same-direction rotations).

**Parameters:**
- `node`: Node to rotate

**Note:** This is an internal method used by splay operations.

### `_zig_zag(node: SplayNode) -> None`

Perform zig-zag rotation (two opposite-direction rotations).

**Parameters:**
- `node`: Node to rotate

**Note:** This is an internal method used by splay operations.

### `_splay(node: SplayNode) -> None`

Splay node to root using appropriate rotations.

**Parameters:**
- `node`: Node to splay to root

**Note:** This is an internal method called automatically by public operations.

### `_find_max(node: SplayNode) -> SplayNode`

Find maximum node in subtree.

**Parameters:**
- `node`: Root of subtree

**Returns:**
- Maximum node

**Note:** This is an internal method.

### `_find_min(node: SplayNode) -> SplayNode`

Find minimum node in subtree.

**Parameters:**
- `node`: Root of subtree

**Returns:**
- Minimum node

**Note:** This is an internal method.

## Usage Examples

### Basic Operations

```python
from src.main import SplayTree

# Create tree
tree = SplayTree()

# Insert keys
tree.insert(50)
tree.insert(30)
tree.insert(70)
tree.insert(20)
tree.insert(40)

# Search (automatically splays to root)
node = tree.search(30)
if node:
    print(f"Found: {node.key}")

# Delete
tree.delete(30)

# Get traversals
inorder = tree.inorder_traversal()
print(f"Inorder: {inorder}")

# Find min/max
min_key = tree.find_min()
max_key = tree.find_max()
print(f"Min: {min_key}, Max: {max_key}")
```

### Amortized Analysis

```python
from src.main import SplayTree

tree = SplayTree()

# Perform operations
for i in range(100):
    tree.insert(i)
    if i % 2 == 0:
        tree.search(i)

# Get analysis
analysis = tree.get_amortized_analysis()
print(f"Total operations: {analysis['total_operations']}")
print(f"Total splay operations: {analysis['total_splay_operations']}")
print(f"Total rotations: {analysis['total_rotations']}")
print(f"Average rotations per splay: {analysis['average_rotations_per_splay']}")
print(f"Amortized cost per operation: {analysis['amortized_cost_per_operation']}")
```

### Error Handling

```python
from src.main import SplayTree

tree = SplayTree()

# Insert duplicate (returns False)
result = tree.insert(10)
print(result)  # True

result = tree.insert(10)
print(result)  # False

# Search non-existent (returns None, splays last visited)
node = tree.search(99)
print(node)  # None

# Delete non-existent (returns False)
result = tree.delete(99)
print(result)  # False

# Operations on empty tree
empty_tree = SplayTree()
print(empty_tree.find_min())  # None
print(empty_tree.find_max())  # None
print(empty_tree.inorder_traversal())  # []
```

## Time Complexity Summary

| Operation | Amortized | Worst Case |
|-----------|-----------|------------|
| `insert` | O(log n) | O(n) |
| `search` | O(log n) | O(n) |
| `delete` | O(log n) | O(n) |
| `find_min` | O(log n) | O(n) |
| `find_max` | O(log n) | O(n) |
| `inorder_traversal` | O(n) | O(n) |
| `preorder_traversal` | O(n) | O(n) |
| `postorder_traversal` | O(n) | O(n) |
| `size` | O(n) | O(n) |
| `is_empty` | O(1) | O(1) |
| `get_amortized_analysis` | O(1) | O(1) |
| `reset_statistics` | O(1) | O(1) |

Where n is the number of elements in the tree.

## Notes

- All operations that access nodes automatically splay them to the root
- The tree maintains binary search tree property at all times
- Amortized analysis shows O(log n) average performance over sequences of operations
- Individual operations may have O(n) worst-case time complexity
- The tree adapts to access patterns, moving frequently accessed elements near the root
