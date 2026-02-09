# Skip List API Documentation

This document provides detailed API documentation for the skip list implementation with probabilistic balancing.

## Classes

### SkipListNode

Represents a node in the skip list.

#### Attributes

- `key` (int): Node key value
- `value` (Optional[int]): Node value (optional)
- `level` (int): Maximum level for this node
- `forward` (List[Optional[SkipListNode]]): List of forward pointers at each level

#### Methods

##### `__init__(key: int, value: Optional[int] = None, level: int = 0) -> None`

Initialize SkipListNode.

**Parameters:**
- `key`: Node key value
- `value`: Node value (optional, default: None)
- `level`: Maximum level for this node (default: 0)

**Example:**
```python
node = SkipListNode(10, 20, 3)
```

### SkipList

Main class for skip list data structure with probabilistic balancing.

#### Methods

##### `__init__(max_level: int = 16, probability: float = 0.5, config_path: str = "config.yaml") -> None`

Initialize skip list.

**Parameters:**
- `max_level`: Maximum level for skip list (default: 16)
- `probability`: Probability for level assignment (default: 0.5)
- `config_path`: Path to configuration YAML file (default: "config.yaml")

**Raises:**
- `ValueError`: If max_level < 1 or probability not in (0, 1)

**Example:**
```python
skip_list = SkipList(max_level=16, probability=0.5)
```

##### `insert(key: int, value: Optional[int] = None) -> bool`

Insert key-value pair into skip list.

**Parameters:**
- `key`: Key to insert
- `value`: Value to associate with key (optional)

**Returns:**
- `True` if insertion successful, `False` if key already exists

**Time Complexity:** O(log n) average, O(n) worst-case

**Example:**
```python
skip_list.insert(10, 20)  # Returns True
skip_list.insert(10, 30)  # Returns False (duplicate)
```

##### `search(key: int) -> Tuple[bool, Optional[int]]`

Search for key in skip list.

**Parameters:**
- `key`: Key to search for

**Returns:**
- Tuple of (found, value) where found is True if key exists

**Time Complexity:** O(log n) average, O(n) worst-case

**Example:**
```python
found, value = skip_list.search(10)  # Returns (True, 20) if found
```

##### `delete(key: int) -> bool`

Delete key from skip list.

**Parameters:**
- `key`: Key to delete

**Returns:**
- `True` if deletion successful, `False` if key not found

**Time Complexity:** O(log n) average, O(n) worst-case

**Example:**
```python
skip_list.delete(10)  # Returns True if deleted
```

##### `get_size() -> int`

Get number of elements in skip list.

**Returns:**
- Number of elements

**Example:**
```python
size = skip_list.get_size()  # Returns number of elements
```

##### `is_empty() -> bool`

Check if skip list is empty.

**Returns:**
- `True` if empty, `False` otherwise

**Example:**
```python
if skip_list.is_empty():
    print("Skip list is empty")
```

##### `get_all_keys() -> List[int]`

Get all keys in sorted order.

**Returns:**
- List of all keys

**Time Complexity:** O(n)

**Example:**
```python
keys = skip_list.get_all_keys()  # Returns sorted list of keys
```

##### `get_all_items() -> List[Tuple[int, Optional[int]]]`

Get all key-value pairs in sorted order.

**Returns:**
- List of (key, value) tuples

**Time Complexity:** O(n)

**Example:**
```python
items = skip_list.get_all_items()  # Returns [(key1, val1), (key2, val2), ...]
```

##### `get_range(start_key: int, end_key: int) -> List[Tuple[int, Optional[int]]]`

Get all items with keys in range [start_key, end_key].

**Parameters:**
- `start_key`: Start key (inclusive)
- `end_key`: End key (inclusive)

**Returns:**
- List of (key, value) tuples in range

**Time Complexity:** O(log n + k) where k is number of items in range

**Example:**
```python
range_items = skip_list.get_range(10, 30)  # Returns items with keys 10-30
```

##### `get_min_key() -> Optional[int]`

Get minimum key.

**Returns:**
- Minimum key, None if empty

**Time Complexity:** O(1)

**Example:**
```python
min_key = skip_list.get_min_key()  # Returns minimum key
```

##### `get_max_key() -> Optional[int]`

Get maximum key.

**Returns:**
- Maximum key, None if empty

**Time Complexity:** O(log n) average

**Example:**
```python
max_key = skip_list.get_max_key()  # Returns maximum key
```

##### `get_current_level() -> int`

Get current maximum level.

**Returns:**
- Current maximum level

**Example:**
```python
level = skip_list.get_current_level()  # Returns current max level
```

##### `clear() -> None`

Clear all elements from skip list.

**Example:**
```python
skip_list.clear()  # Removes all elements
```

##### `is_valid() -> bool`

Validate skip list structure.

**Returns:**
- `True` if valid, `False` otherwise

**Time Complexity:** O(n)

**Example:**
```python
if skip_list.is_valid():
    print("Skip list structure is valid")
```

## Usage Examples

### Basic Operations

```python
from src.main import SkipList

# Create skip list
skip_list = SkipList(max_level=16, probability=0.5)

# Insert keys
skip_list.insert(10, 20)
skip_list.insert(20, 40)
skip_list.insert(30, 60)

# Search
found, value = skip_list.search(20)  # Returns (True, 40)

# Delete
skip_list.delete(20)

# Get all keys
all_keys = skip_list.get_all_keys()  # Returns [10, 30]
```

### Range Queries

```python
skip_list = SkipList()

# Insert multiple keys
for i in range(1, 21):
    skip_list.insert(i * 10, i * 20)

# Get range
range_items = skip_list.get_range(30, 70)
# Returns items with keys 30, 40, 50, 60, 70
```

### Min/Max Operations

```python
skip_list = SkipList()
skip_list.insert(30)
skip_list.insert(10)
skip_list.insert(50)
skip_list.insert(20)

min_key = skip_list.get_min_key()  # Returns 10
max_key = skip_list.get_max_key()  # Returns 50
```

### Iterating All Items

```python
skip_list = SkipList()
skip_list.insert(10, 20)
skip_list.insert(20, 40)
skip_list.insert(30, 60)

items = skip_list.get_all_items()
# Returns [(10, 20), (20, 40), (30, 60)]
```

### Validation

```python
skip_list = SkipList()
skip_list.insert(10)
skip_list.insert(20)

if skip_list.is_valid():
    print("Skip list is valid")
```

## Error Handling

The implementation handles the following cases gracefully:

- **Invalid max_level**: Raises `ValueError` if max_level < 1
- **Invalid probability**: Raises `ValueError` if probability not in (0, 1)
- **Duplicate keys**: `insert()` returns `False` for duplicates
- **Missing keys**: `search()` and `delete()` return `False`/`None` for non-existent keys

## Performance Characteristics

| Operation | Average Case | Worst Case | Space |
|-----------|-------------|------------|-------|
| Search | O(log n) | O(n) | O(1) |
| Insert | O(log n) | O(n) | O(log n) |
| Delete | O(log n) | O(n) | O(1) |
| Range Query | O(log n + k) | O(n) | O(k) |
| Get All Keys | O(n) | O(n) | O(n) |
| Min Key | O(1) | O(1) | O(1) |
| Max Key | O(log n) | O(n) | O(1) |

Where:
- n = number of elements
- k = number of elements in range

## Algorithm Details

### Probabilistic Level Assignment

Each node is assigned a level probabilistically:
1. Start at level 0
2. With probability p, increase level
3. Continue until random() >= p or max_level reached

Expected level: 1/(1-p)
With p = 0.5: Expected level ≈ 1

### Search Algorithm

1. Start from head at current maximum level
2. Move right if next key < target
3. Otherwise, go down one level
4. Repeat until found or bottom level reached

### Insert Algorithm

1. Find insertion position (like search)
2. Generate random level for new node
3. Update forward pointers at all levels up to new node's level
4. Insert new node

### Delete Algorithm

1. Find node to delete (like search)
2. Update forward pointers to bypass deleted node
3. Update current level if necessary

## Thread Safety

This implementation is not thread-safe. For concurrent access, external synchronization is required.
