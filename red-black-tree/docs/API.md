# Red-Black Tree API Documentation

This document provides detailed API documentation for the red-black tree implementation.

## Classes

### RedBlackNode

Represents a node in the red-black tree.

#### Attributes

- `key` (float): The key value stored in the node
- `color` (Color): The color of the node (RED or BLACK)
- `parent` (Optional[RedBlackNode]): Reference to parent node
- `left` (Optional[RedBlackNode]): Reference to left child
- `right` (Optional[RedBlackNode]): Reference to right child

#### Methods

##### `__init__(key: float, color: Color = Color.RED, parent: Optional[RedBlackNode] = None) -> None`

Initialize a new red-black node.

**Parameters:**
- `key`: The key value to store
- `color`: Initial color (default: RED)
- `parent`: Parent node reference (default: None)

##### `is_red() -> bool`

Check if the node is red.

**Returns:**
- `True` if node is red, `False` otherwise

##### `is_black() -> bool`

Check if the node is black.

**Returns:**
- `True` if node is black, `False` otherwise

### RedBlackTree

Main class for red-black tree data structure.

#### Methods

##### `__init__(config_path: str = "config.yaml") -> None`

Initialize a new red-black tree.

**Parameters:**
- `config_path`: Path to configuration YAML file (default: "config.yaml")

##### `insert(key: float) -> bool`

Insert a key into the red-black tree.

**Parameters:**
- `key`: The key value to insert

**Returns:**
- `True` if insertion successful, `False` if key already exists

**Time Complexity:** O(log n)

**Example:**
```python
tree = RedBlackTree()
tree.insert(10)  # Returns True
tree.insert(10)  # Returns False (duplicate)
```

##### `delete(key: float) -> bool`

Delete a key from the red-black tree.

**Parameters:**
- `key`: The key value to delete

**Returns:**
- `True` if deletion successful, `False` if key not found

**Time Complexity:** O(log n)

**Example:**
```python
tree.insert(10)
tree.delete(10)  # Returns True
tree.delete(20)  # Returns False (not found)
```

##### `search(key: float) -> bool`

Search for a key in the red-black tree.

**Parameters:**
- `key`: The key value to search for

**Returns:**
- `True` if key found, `False` otherwise

**Time Complexity:** O(log n)

**Example:**
```python
tree.insert(10)
tree.search(10)  # Returns True
tree.search(20)  # Returns False
```

##### `inorder_traversal() -> List[float]`

Perform inorder traversal of the tree.

**Returns:**
- List of keys in sorted (ascending) order

**Time Complexity:** O(n)

**Example:**
```python
tree.insert(10)
tree.insert(5)
tree.insert(15)
tree.inorder_traversal()  # Returns [5, 10, 15]
```

##### `preorder_traversal() -> List[float]`

Perform preorder traversal of the tree.

**Returns:**
- List of keys in preorder (root, left, right)

**Time Complexity:** O(n)

##### `postorder_traversal() -> List[float]`

Perform postorder traversal of the tree.

**Returns:**
- List of keys in postorder (left, right, root)

**Time Complexity:** O(n)

##### `height() -> int`

Calculate the height of the tree.

**Returns:**
- Height of the tree (number of edges from root to deepest leaf)

**Time Complexity:** O(n)

**Example:**
```python
tree.insert(10)
tree.height()  # Returns 1
tree.insert(5)
tree.insert(15)
tree.height()  # Returns 2
```

##### `get_size() -> int`

Get the number of nodes in the tree.

**Returns:**
- Number of nodes in the tree

**Time Complexity:** O(n)

**Example:**
```python
tree.insert(10)
tree.insert(20)
tree.get_size()  # Returns 2
```

##### `is_valid() -> bool`

Validate that the tree satisfies all red-black tree properties.

**Returns:**
- `True` if tree is valid, `False` otherwise

**Time Complexity:** O(n)

**Red-Black Properties Checked:**
1. Root is black
2. No two consecutive red nodes
3. Black height property (all paths have same number of black nodes)

**Example:**
```python
tree.insert(10)
tree.insert(20)
tree.is_valid()  # Returns True
```

## Enumerations

### Color

Enumeration for node colors.

#### Values

- `Color.RED`: Red node color
- `Color.BLACK`: Black node color

## Usage Examples

### Basic Operations

```python
from src.main import RedBlackTree

# Create tree
tree = RedBlackTree()

# Insert keys
tree.insert(10)
tree.insert(20)
tree.insert(30)
tree.insert(5)
tree.insert(15)

# Search
found = tree.search(20)  # True

# Delete
tree.delete(20)

# Traverse
sorted_keys = tree.inorder_traversal()  # [5, 10, 15, 30]

# Get properties
size = tree.get_size()  # 4
height = tree.height()  # 2 or 3
is_valid = tree.is_valid()  # True
```

### Large Dataset

```python
tree = RedBlackTree()

# Insert many keys
for i in range(1, 1001):
    tree.insert(i)

# All operations remain O(log n)
tree.search(500)  # O(log n)
tree.delete(500)  # O(log n)
tree.is_valid()  # True
```

### Validation

```python
tree = RedBlackTree()
keys = [10, 20, 30, 40, 50, 5, 15, 25, 35, 45]

for key in keys:
    tree.insert(key)
    assert tree.is_valid()  # Tree remains valid after each insertion

# Delete and validate
for key in keys:
    tree.delete(key)
    assert tree.is_valid()  # Tree remains valid after each deletion
```

## Error Handling

The implementation handles the following cases gracefully:

- **Duplicate keys**: `insert()` returns `False` for duplicates
- **Missing keys**: `delete()` and `search()` return `False` for non-existent keys
- **Empty tree**: All operations work correctly on empty tree
- **Configuration errors**: Falls back to defaults if config file missing

## Performance Characteristics

| Operation | Time Complexity | Space Complexity |
|-----------|----------------|-------------------|
| Insert    | O(log n)       | O(1)              |
| Delete    | O(log n)       | O(1)              |
| Search    | O(log n)       | O(1)              |
| Traversal | O(n)           | O(n)              |
| Height    | O(n)           | O(log n)          |
| Size      | O(n)           | O(log n)          |
| Validation| O(n)           | O(log n)          |

Where n is the number of nodes in the tree.

## Thread Safety

This implementation is not thread-safe. For concurrent access, external synchronization is required.
