# Treap API Documentation

This document provides detailed API documentation for the treap (tree + heap) implementation with randomized balancing.

## Classes

### TreapNode

Represents a node in the treap.

#### Attributes

- `key` (int): Node key value
- `priority` (int): Node priority value
- `left` (Optional[TreapNode]): Left child node
- `right` (Optional[TreapNode]): Right child node

#### Methods

##### `__init__(key: int, priority: Optional[int] = None) -> None`

Initialize TreapNode.

**Parameters:**
- `key`: Node key value
- `priority`: Node priority (random if None)

**Example:**
```python
node = TreapNode(10, 5)
```

### Treap

Main class for treap data structure with randomized balancing.

#### Methods

##### `__init__(config_path: str = "config.yaml") -> None`

Initialize treap.

**Parameters:**
- `config_path`: Path to configuration YAML file (default: "config.yaml")

**Example:**
```python
treap = Treap()
```

##### `insert(key: int, priority: Optional[int] = None) -> bool`

Insert key into treap.

**Parameters:**
- `key`: Key to insert
- `priority`: Priority for new node (random if None)

**Returns:**
- `True` if insertion successful, `False` if key already exists

**Time Complexity:** O(log n) expected

**Example:**
```python
treap.insert(10)  # Returns True
treap.insert(10)  # Returns False (duplicate)
```

##### `delete(key: int) -> bool`

Delete key from treap.

**Parameters:**
- `key`: Key to delete

**Returns:**
- `True` if deletion successful, `False` if key not found

**Time Complexity:** O(log n) expected

**Example:**
```python
treap.delete(10)  # Returns True if deleted
```

##### `search(key: int) -> bool`

Search for key in treap.

**Parameters:**
- `key`: Key to search for

**Returns:**
- `True` if key found, `False` otherwise

**Time Complexity:** O(log n) expected

**Example:**
```python
found = treap.search(10)  # Returns True if found
```

##### `split(key: int) -> Tuple[Treap, Treap]`

Split treap into two treaps at key.

**Parameters:**
- `key`: Split key

**Returns:**
- Tuple of (left_treap, right_treap) where left contains keys < key, right contains keys >= key

**Time Complexity:** O(log n) expected

**Example:**
```python
left, right = treap.split(25)
```

##### `merge(other: Treap) -> Treap`

Merge this treap with another treap.

**Parameters:**
- `other`: Treap to merge with (all keys must be > all keys in this treap)

**Returns:**
- New merged treap

**Time Complexity:** O(log n) expected

**Example:**
```python
merged = left.merge(right)
```

##### `get_size() -> int`

Get number of elements in treap.

**Returns:**
- Number of elements

**Example:**
```python
size = treap.get_size()  # Returns number of elements
```

##### `is_empty() -> bool`

Check if treap is empty.

**Returns:**
- `True` if empty, `False` otherwise

**Example:**
```python
if treap.is_empty():
    print("Treap is empty")
```

##### `get_all_keys() -> List[int]`

Get all keys in sorted order.

**Returns:**
- List of all keys

**Time Complexity:** O(n)

**Example:**
```python
keys = treap.get_all_keys()  # Returns sorted list of keys
```

##### `get_min_key() -> Optional[int]`

Get minimum key.

**Returns:**
- Minimum key, None if empty

**Time Complexity:** O(log n) expected

**Example:**
```python
min_key = treap.get_min_key()  # Returns minimum key
```

##### `get_max_key() -> Optional[int]`

Get maximum key.

**Returns:**
- Maximum key, None if empty

**Time Complexity:** O(log n) expected

**Example:**
```python
max_key = treap.get_max_key()  # Returns maximum key
```

##### `clear() -> None`

Clear all elements from treap.

**Example:**
```python
treap.clear()  # Removes all elements
```

##### `is_valid() -> bool`

Validate treap structure.

**Returns:**
- `True` if valid, `False` otherwise

**Time Complexity:** O(n)

**Example:**
```python
if treap.is_valid():
    print("Treap structure is valid")
```

## Usage Examples

### Basic Operations

```python
from src.main import Treap

# Create treap
treap = Treap()

# Insert keys
treap.insert(10)
treap.insert(20)
treap.insert(30)

# Search
found = treap.search(20)  # Returns True

# Delete
treap.delete(20)

# Get all keys
all_keys = treap.get_all_keys()  # Returns [10, 30]
```

### Split and Merge

```python
treap = Treap()
for i in range(1, 11):
    treap.insert(i * 10)

# Split treap
left, right = treap.split(50)
# Left: keys < 50, Right: keys >= 50

# Merge treaps
merged = left.merge(right)
```

### Min/Max Operations

```python
treap = Treap()
treap.insert(30)
treap.insert(10)
treap.insert(50)
treap.insert(20)

min_key = treap.get_min_key()  # Returns 10
max_key = treap.get_max_key()  # Returns 50
```

### Validation

```python
treap = Treap()
treap.insert(10)
treap.insert(20)

if treap.is_valid():
    print("Treap is valid")
```

## Error Handling

The implementation handles the following cases gracefully:

- **Duplicate keys**: `insert()` returns `False` for duplicates
- **Missing keys**: `delete()` and `search()` return `False`/`None` for non-existent keys
- **Configuration errors**: Falls back to defaults if config file missing

## Performance Characteristics

| Operation | Expected Case | Worst Case | Space |
|-----------|--------------|------------|-------|
| Insert | O(log n) | O(n) | O(1) |
| Delete | O(log n) | O(n) | O(1) |
| Search | O(log n) | O(n) | O(1) |
| Split | O(log n) | O(n) | O(log n) |
| Merge | O(log n) | O(n) | O(log n) |
| Get All Keys | O(n) | O(n) | O(n) |
| Min/Max Key | O(log n) | O(n) | O(1) |

Where n is the number of elements.

## Algorithm Details

### Randomized Balancing

Each node gets a random priority when inserted. The treap maintains:
1. **BST Property**: Left child key < node key < right child key
2. **Heap Property**: Parent priority > children priorities

### Insert Process

1. Insert as BST (maintain key ordering)
2. Rotate up to maintain heap property (priority ordering)
3. Rotations ensure balanced structure

### Delete Process

1. Find node to delete
2. Rotate down to leaf (maintain heap property)
3. Remove leaf node

### Split Process

1. Split treap at key
2. Left treap: all keys < split key
3. Right treap: all keys >= split key

### Merge Process

1. Merge two treaps
2. Requires: all keys in left < all keys in right
3. Merge based on priorities

## Thread Safety

This implementation is not thread-safe. For concurrent access, external synchronization is required.
