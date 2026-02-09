# B-Tree API Documentation

This document provides detailed API documentation for the B-tree implementation optimized for disk-based storage.

## Classes

### BTreeNode

Represents a node in the B-tree.

#### Attributes

- `keys` (List[float]): List of keys stored in the node
- `children` (List[Optional[BTreeNode]]): List of child node references
- `is_leaf` (bool): Whether this node is a leaf node
- `parent` (Optional[BTreeNode]): Reference to parent node

#### Methods

##### `is_full(min_degree: int) -> bool`

Check if the node is full (has maximum keys).

**Parameters:**
- `min_degree`: Minimum degree of B-tree

**Returns:**
- `True` if node has maximum keys, `False` otherwise

##### `is_underfull(min_degree: int) -> bool`

Check if the node is underfull (has fewer than minimum keys).

**Parameters:**
- `min_degree`: Minimum degree of B-tree

**Returns:**
- `True` if node has fewer than minimum keys, `False` otherwise

### BTree

Main class for B-tree data structure optimized for disk-based storage.

#### Methods

##### `__init__(min_degree: int = 3, config_path: str = "config.yaml") -> None`

Initialize a new B-tree.

**Parameters:**
- `min_degree`: Minimum degree of B-tree (default: 3, must be >= 2)
- `config_path`: Path to configuration YAML file (default: "config.yaml")

**Raises:**
- `ValueError`: If min_degree is less than 2

##### `insert(key: float) -> bool`

Insert a key into the B-tree.

**Parameters:**
- `key`: The key value to insert

**Returns:**
- `True` if insertion successful, `False` if key already exists

**Time Complexity:** O(log n)

**Disk I/O:** O(log n) reads and writes

**Example:**
```python
tree = BTree()
tree.insert(10)  # Returns True
tree.insert(10)  # Returns False (duplicate)
```

##### `delete(key: float) -> bool`

Delete a key from the B-tree.

**Parameters:**
- `key`: The key value to delete

**Returns:**
- `True` if deletion successful, `False` if key not found

**Time Complexity:** O(log n)

**Disk I/O:** O(log n) reads and writes

**Example:**
```python
tree.insert(10)
tree.delete(10)  # Returns True
tree.delete(20)  # Returns False (not found)
```

##### `search(key: float) -> Tuple[Optional[BTreeNode], Optional[int]]`

Search for a key in the B-tree.

**Parameters:**
- `key`: The key value to search for

**Returns:**
- Tuple of (node, index) if found, (None, None) otherwise

**Time Complexity:** O(log n)

**Disk I/O:** O(log n) reads

**Example:**
```python
tree.insert(10)
node, index = tree.search(10)  # Returns (node, 0)
node, index = tree.search(20)  # Returns (None, None)
```

##### `inorder_traversal() -> List[float]`

Perform inorder traversal of the tree.

**Returns:**
- List of keys in sorted (ascending) order

**Time Complexity:** O(n)

**Disk I/O:** O(n) reads

**Example:**
```python
tree.insert(10)
tree.insert(5)
tree.insert(15)
tree.inorder_traversal()  # Returns [5, 10, 15]
```

##### `get_height() -> int`

Calculate the height of the tree.

**Returns:**
- Height of the tree (number of levels)

**Time Complexity:** O(log n)

**Example:**
```python
tree.insert(10)
tree.get_height()  # Returns 1
tree.insert(5)
tree.insert(15)
tree.get_height()  # Returns 1 or 2
```

##### `get_size() -> int`

Get the number of keys in the tree.

**Returns:**
- Number of keys in the tree

**Time Complexity:** O(n)

**Example:**
```python
tree.insert(10)
tree.insert(20)
tree.get_size()  # Returns 2
```

##### `is_valid() -> bool`

Validate that the tree satisfies all B-tree properties.

**Returns:**
- `True` if tree is valid, `False` otherwise

**Time Complexity:** O(n)

**B-Tree Properties Checked:**
1. Root has at least 1 key (unless empty)
2. Every node (except root) has at least min_degree - 1 keys
3. Every node has at most 2 * min_degree - 1 keys
4. All leaves are at the same level
5. Node with k keys has k + 1 children

**Example:**
```python
tree.insert(10)
tree.insert(20)
tree.is_valid()  # Returns True
```

##### `get_disk_io_stats() -> Dict[str, int]`

Get disk I/O statistics.

**Returns:**
- Dictionary with 'disk_reads' and 'disk_writes' counts

**Example:**
```python
tree.insert(10)
stats = tree.get_disk_io_stats()
print(stats['disk_reads'])  # Number of disk reads
print(stats['disk_writes'])  # Number of disk writes
```

##### `reset_disk_io_stats() -> None`

Reset disk I/O statistics to zero.

**Example:**
```python
tree.insert(10)
tree.reset_disk_io_stats()
stats = tree.get_disk_io_stats()
# stats['disk_reads'] == 0 and stats['disk_writes'] == 0
```

## Usage Examples

### Basic Operations

```python
from src.main import BTree

# Create tree with minimum degree 3
tree = BTree(min_degree=3)

# Insert keys
tree.insert(10)
tree.insert(20)
tree.insert(30)
tree.insert(40)
tree.insert(50)

# Search
node, index = tree.search(30)  # (node, index) if found

# Delete
tree.delete(30)

# Traverse
sorted_keys = tree.inorder_traversal()  # [10, 20, 40, 50]

# Get properties
size = tree.get_size()  # 4
height = tree.get_height()  # 1 or 2
is_valid = tree.is_valid()  # True
```

### Disk I/O Monitoring

```python
tree = BTree()

# Reset stats before operation
tree.reset_disk_io_stats()

# Perform operations
for i in range(100):
    tree.insert(i)

# Check I/O statistics
stats = tree.get_disk_io_stats()
print(f"Reads: {stats['disk_reads']}")
print(f"Writes: {stats['disk_writes']}")
```

### Large Dataset

```python
tree = BTree(min_degree=4)

# Insert many keys
for i in range(1, 1001):
    tree.insert(i)

# All operations remain O(log n)
node, index = tree.search(500)  # O(log n)
tree.delete(500)  # O(log n)
tree.is_valid()  # True
```

### Different Minimum Degrees

```python
# Small minimum degree (more splits, taller tree)
tree_small = BTree(min_degree=2)

# Medium minimum degree (balanced)
tree_medium = BTree(min_degree=3)

# Large minimum degree (fewer splits, shorter tree)
tree_large = BTree(min_degree=5)
```

### Validation

```python
tree = BTree()
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
- **Missing keys**: `delete()` and `search()` return `False`/`None` for non-existent keys
- **Empty tree**: All operations work correctly on empty tree
- **Invalid minimum degree**: Raises `ValueError` if min_degree < 2
- **Configuration errors**: Falls back to defaults if config file missing

## Performance Characteristics

| Operation | Time Complexity | Disk Reads | Disk Writes |
|-----------|----------------|------------|-------------|
| Insert    | O(log n)       | O(log n)   | O(log n)    |
| Delete    | O(log n)       | O(log n)   | O(log n)    |
| Search    | O(log n)       | O(log n)   | 0           |
| Traversal | O(n)           | O(n)       | 0           |
| Height    | O(log n)       | 0          | 0           |
| Size      | O(n)           | 0          | 0           |
| Validation| O(n)           | 0          | 0           |

Where n is the number of keys in the tree.

## Disk I/O Optimization

The B-tree is designed to minimize disk I/O:

1. **Multiple keys per node**: Reduces tree height, fewer disk reads
2. **Split before full**: Prevents cascading splits
3. **Merge when underfull**: Maintains minimum keys per node
4. **Sequential access**: Inorder traversal reads nodes sequentially
5. **Statistics tracking**: Monitor I/O to optimize operations

## Thread Safety

This implementation is not thread-safe. For concurrent access, external synchronization is required.
