# Persistent Segment Tree API Documentation

This document provides detailed API documentation for the persistent segment tree implementation.

## Classes

### SegmentTreeNode

Represents a node in the persistent segment tree.

#### Attributes

- `left` (Optional[SegmentTreeNode]): Left child node
- `right` (Optional[SegmentTreeNode]): Right child node
- `value` (int): Node value (sum/min/max depending on operation)

#### Methods

##### `copy() -> SegmentTreeNode`

Create a copy of this node.

**Returns:**
- Copy of the node

### PersistentSegmentTree

Main class for persistent segment tree supporting range queries across versions.

#### Methods

##### `__init__(array: List[int], config_path: str = "config.yaml") -> None`

Initialize persistent segment tree.

**Parameters:**
- `array`: Initial array values
- `config_path`: Path to configuration YAML file (default: "config.yaml")

**Raises:**
- `ValueError`: If array is empty

**Example:**
```python
tree = PersistentSegmentTree([1, 2, 3, 4, 5])
```

##### `update(version: int, index: int, value: int) -> int`

Update element at index in specified version, creating new version.

**Parameters:**
- `version`: Version to update from
- `index`: Index to update (0-indexed)
- `value`: New value

**Returns:**
- New version number

**Raises:**
- `ValueError`: If version or index is invalid

**Time Complexity:** O(log n)

**Example:**
```python
version_1 = tree.update(0, 2, 10)  # Update index 2 to 10 in version 0
```

##### `query_sum(version: int, left: int, right: int) -> int`

Query sum in range [left, right] for specified version.

**Parameters:**
- `version`: Version to query
- `left`: Start index (0-indexed, inclusive)
- `right`: End index (0-indexed, inclusive)

**Returns:**
- Sum of elements in range

**Raises:**
- `ValueError`: If version or indices are invalid

**Time Complexity:** O(log n)

**Example:**
```python
sum_value = tree.query_sum(0, 1, 4)  # Sum of elements [1, 2, 3, 4]
```

##### `query_min(version: int, left: int, right: int) -> int`

Query minimum in range [left, right] for specified version.

**Parameters:**
- `version`: Version to query
- `left`: Start index (0-indexed, inclusive)
- `right`: End index (0-indexed, inclusive)

**Returns:**
- Minimum value in range

**Raises:**
- `ValueError`: If version or indices are invalid

**Time Complexity:** O(log n)

**Example:**
```python
min_value = tree.query_min(0, 0, 4)  # Minimum in range [0, 1, 2, 3, 4]
```

##### `query_max(version: int, left: int, right: int) -> int`

Query maximum in range [left, right] for specified version.

**Parameters:**
- `version`: Version to query
- `left`: Start index (0-indexed, inclusive)
- `right`: End index (0-indexed, inclusive)

**Returns:**
- Maximum value in range

**Raises:**
- `ValueError`: If version or indices are invalid

**Time Complexity:** O(log n)

**Example:**
```python
max_value = tree.query_max(0, 0, 4)  # Maximum in range [0, 1, 2, 3, 4]
```

##### `get_version_array(version: int) -> List[int]`

Get array representation of specified version.

**Parameters:**
- `version`: Version to reconstruct

**Returns:**
- Array values for specified version

**Raises:**
- `ValueError`: If version is invalid

**Time Complexity:** O(n)

**Example:**
```python
array = tree.get_version_array(0)  # Get array for version 0
```

##### `get_version_count() -> int`

Get number of versions.

**Returns:**
- Number of versions

**Example:**
```python
count = tree.get_version_count()  # Returns number of versions
```

##### `get_size() -> int`

Get size of array.

**Returns:**
- Number of elements

**Example:**
```python
size = tree.get_size()  # Returns array size
```

## Usage Examples

### Basic Operations

```python
from src.main import PersistentSegmentTree

# Create tree
array = [1, 3, 5, 7, 9, 11]
tree = PersistentSegmentTree(array)

# Query version 0
sum_v0 = tree.query_sum(0, 0, 5)  # 36
min_v0 = tree.query_min(0, 0, 5)  # 1
max_v0 = tree.query_max(0, 0, 5)  # 11

# Create new version
version_1 = tree.update(0, 2, 10)

# Query new version
sum_v1 = tree.query_sum(version_1, 0, 5)  # 41

# Query old version (unchanged)
sum_v0_again = tree.query_sum(0, 0, 5)  # Still 36
```

### Multiple Versions

```python
tree = PersistentSegmentTree([1, 2, 3, 4, 5])

# Create multiple versions
v1 = tree.update(0, 0, 10)
v2 = tree.update(v1, 1, 20)
v3 = tree.update(v2, 2, 30)

# Query all versions
for version in range(tree.get_version_count()):
    total = tree.query_sum(version, 0, 4)
    arr = tree.get_version_array(version)
    print(f"Version {version}: {arr}, sum: {total}")
```

### Time-Travel Queries

```python
tree = PersistentSegmentTree([0] * 10)

# Build up versions over time
current_version = 0
for i in range(10):
    current_version = tree.update(current_version, i, i + 1)

# Query any historical version
for v in range(tree.get_version_count()):
    sum_v = tree.query_sum(v, 0, 9)
    print(f"Version {v} sum: {sum_v}")
```

### Range Queries

```python
tree = PersistentSegmentTree([5, 2, 8, 1, 9])

# Query different ranges
min_0_2 = tree.query_min(0, 0, 2)  # 2
max_2_4 = tree.query_max(0, 2, 4)  # 9
sum_1_3 = tree.query_sum(0, 1, 3)  # 11

# Update and query new version
v1 = tree.update(0, 1, 0)
min_0_2_v1 = tree.query_min(v1, 0, 2)  # 0
```

## Error Handling

The implementation handles the following cases gracefully:

- **Empty array**: Raises `ValueError` during initialization
- **Invalid version**: Raises `ValueError` for out-of-range versions
- **Invalid indices**: Raises `ValueError` for out-of-bounds indices
- **Invalid range**: Raises `ValueError` if left > right
- **Configuration errors**: Falls back to defaults if config file missing

## Performance Characteristics

| Operation | Time Complexity | Space Complexity |
|-----------|----------------|------------------|
| Construction | O(n log n) | O(n) |
| Query Sum | O(log n) | O(1) |
| Query Min | O(log n) | O(1) |
| Query Max | O(log n) | O(1) |
| Update | O(log n) | O(log n) |
| Get Version Array | O(n) | O(n) |
| Get Version Count | O(1) | O(1) |

Where n is the number of elements.

## Algorithm Details

### Persistence Mechanism

The persistent segment tree maintains multiple versions by:

1. **Node Copying**: When updating, only nodes on the path from root to updated leaf are copied
2. **Shared Subtrees**: Unchanged subtrees are shared between versions
3. **Version Storage**: All version roots are stored in a list

### Update Process

1. Start from root of source version
2. Copy nodes on path to updated index
3. Update copied nodes with new value
4. Store new root as new version

### Query Process

1. Start from root of specified version
2. Traverse tree based on query range
3. Combine results from left and right subtrees
4. Return aggregated result

## Thread Safety

This implementation is not thread-safe. For concurrent access, external synchronization is required.
