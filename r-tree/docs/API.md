# R-Tree API Documentation

This document provides detailed API documentation for the R-tree implementation with spatial indexing and geometric range queries.

## Classes

### Rectangle

Represents a rectangle (bounding box) in 2D space.

#### Attributes

- `min_x` (float): Minimum x coordinate
- `min_y` (float): Minimum y coordinate
- `max_x` (float): Maximum x coordinate
- `max_y` (float): Maximum y coordinate

#### Methods

##### `__init__(min_x: float, min_y: float, max_x: float, max_y: float) -> None`

Initialize rectangle.

**Parameters:**
- `min_x`: Minimum x coordinate
- `min_y`: Minimum y coordinate
- `max_x`: Maximum x coordinate
- `max_y`: Maximum y coordinate

**Raises:**
- `ValueError`: If min_x > max_x or min_y > max_y

**Example:**
```python
rect = Rectangle(1, 2, 3, 4)
```

##### `area() -> float`

Calculate area of rectangle.

**Returns:**
- Area of rectangle

**Example:**
```python
rect = Rectangle(0, 0, 5, 10)
area = rect.area()  # Returns 50
```

##### `intersects(other: Rectangle) -> bool`

Check if this rectangle intersects with another.

**Parameters:**
- `other`: Other rectangle to check

**Returns:**
- `True` if rectangles intersect, `False` otherwise

**Example:**
```python
rect1 = Rectangle(1, 1, 3, 3)
rect2 = Rectangle(2, 2, 4, 4)
assert rect1.intersects(rect2) is True
```

##### `contains(other: Rectangle) -> bool`

Check if this rectangle contains another.

**Parameters:**
- `other`: Other rectangle to check

**Returns:**
- `True` if this rectangle contains other, `False` otherwise

**Example:**
```python
rect1 = Rectangle(0, 0, 10, 10)
rect2 = Rectangle(2, 2, 5, 5)
assert rect1.contains(rect2) is True
```

##### `union(other: Rectangle) -> Rectangle`

Create union rectangle with another.

**Parameters:**
- `other`: Other rectangle

**Returns:**
- Union rectangle

**Example:**
```python
rect1 = Rectangle(1, 1, 3, 3)
rect2 = Rectangle(2, 2, 4, 4)
union = rect1.union(rect2)
```

##### `expansion_area(other: Rectangle) -> float`

Calculate area increase needed to include other rectangle.

**Parameters:**
- `other`: Other rectangle

**Returns:**
- Area increase

**Example:**
```python
rect1 = Rectangle(1, 1, 3, 3)
rect2 = Rectangle(2, 2, 5, 5)
expansion = rect1.expansion_area(rect2)
```

### RTreeNode

Node in R-tree.

#### Attributes

- `is_leaf` (bool): Whether this node is a leaf node
- `entries` (List[Tuple[Rectangle, Optional[RTreeNode], Optional[object]]]): List of entries
- `mbr` (Optional[Rectangle]): Minimum bounding rectangle

#### Methods

##### `__init__(is_leaf: bool = True) -> None`

Initialize R-tree node.

**Parameters:**
- `is_leaf`: Whether this node is a leaf node

**Example:**
```python
node = RTreeNode(is_leaf=True)
```

##### `update_mbr() -> None`

Update minimum bounding rectangle from entries.

**Example:**
```python
node.update_mbr()
```

### RTree

Main class for R-tree data structure.

#### Methods

##### `__init__(max_entries: int = 4, min_entries: int = 2, config_path: str = "config.yaml") -> None`

Initialize R-tree.

**Parameters:**
- `max_entries`: Maximum number of entries per node (default: 4)
- `min_entries`: Minimum number of entries per node (default: 2)
- `config_path`: Path to configuration YAML file (default: "config.yaml")

**Raises:**
- `ValueError`: If min_entries < 1 or max_entries < min_entries

**Example:**
```python
tree = RTree(max_entries=4, min_entries=2)
```

##### `insert(min_x: float, min_y: float, max_x: float, max_y: float, data: Optional[object] = None) -> None`

Insert rectangle into tree.

**Parameters:**
- `min_x`: Minimum x coordinate
- `min_y`: Minimum y coordinate
- `max_x`: Maximum x coordinate
- `max_y`: Maximum y coordinate
- `data`: Optional data associated with rectangle

**Raises:**
- `ValueError`: If rectangle is invalid

**Time Complexity:** O(log n) average

**Example:**
```python
tree.insert(1, 1, 3, 3)
tree.insert(2, 2, 4, 4, data="location_A")
```

##### `range_query(min_x: float, min_y: float, max_x: float, max_y: float) -> List[Tuple[Rectangle, Optional[object]]]`

Find all rectangles intersecting with query rectangle.

**Parameters:**
- `min_x`: Minimum x coordinate of query
- `min_y`: Minimum y coordinate of query
- `max_x`: Maximum x coordinate of query
- `max_y`: Maximum y coordinate of query

**Returns:**
- List of (rectangle, data) tuples

**Raises:**
- `ValueError`: If query rectangle is invalid

**Time Complexity:** O(log n + m) average where m is number of results

**Example:**
```python
results = tree.range_query(2, 2, 6, 6)
for rect, data in results:
    print(f"Rectangle: {rect}, Data: {data}")
```

##### `get_all_rectangles() -> List[Tuple[Rectangle, Optional[object]]]`

Get all rectangles in tree.

**Returns:**
- List of (rectangle, data) tuples

**Time Complexity:** O(n)

**Example:**
```python
all_rects = tree.get_all_rectangles()
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

##### `get_size() -> int`

Get number of rectangles in tree.

**Returns:**
- Number of rectangles

**Time Complexity:** O(1)

**Example:**
```python
size = tree.get_size()
```

##### `clear() -> None`

Clear all rectangles from tree.

**Example:**
```python
tree.clear()
```

## Usage Examples

### Basic Operations

```python
from src.main import RTree

# Create R-tree
tree = RTree(max_entries=4, min_entries=2)

# Insert rectangles
tree.insert(1, 1, 3, 3)
tree.insert(2, 2, 4, 4)
tree.insert(5, 5, 7, 7)

# Range query
results = tree.range_query(2, 2, 6, 6)
for rect, data in results:
    print(f"Rectangle: {rect}")

# Get all rectangles
all_rects = tree.get_all_rectangles()
```

### Geographic Data Example

```python
from src.main import RTree

# Create R-tree for geographic regions
tree = RTree(max_entries=10, min_entries=3)

# Insert city bounding boxes
tree.insert(-122.5, 37.7, -122.3, 37.8, data="San Francisco")
tree.insert(-74.0, 40.7, -73.9, 40.8, data="New York")
tree.insert(-118.3, 34.0, -118.2, 34.1, data="Los Angeles")

# Query for regions in a bounding box
results = tree.range_query(-122.6, 37.6, -122.2, 37.9)
for rect, city in results:
    print(f"City in range: {city}")
```

### Computer Graphics Example

```python
from src.main import RTree

# Create R-tree for object bounding boxes
tree = RTree()

# Insert object bounding boxes
tree.insert(10, 10, 50, 50, data="Object1")
tree.insert(60, 60, 100, 100, data="Object2")
tree.insert(30, 30, 70, 70, data="Object3")

# Query view frustum (camera view)
view_frustum = tree.range_query(0, 0, 80, 80)
visible_objects = [data for _, data in view_frustum]
print(f"Visible objects: {visible_objects}")
```

### Error Handling

```python
from src.main import RTree, Rectangle

tree = RTree()

# Invalid rectangle
try:
    tree.insert(3, 3, 1, 1)
except ValueError as e:
    print(f"Error: {e}")

# Invalid query
try:
    tree.range_query(10, 10, 5, 5)
except ValueError as e:
    print(f"Error: {e}")

# Invalid configuration
try:
    RTree(max_entries=2, min_entries=4)
except ValueError as e:
    print(f"Error: {e}")
```

## Time Complexity Summary

| Operation | Average Case | Worst Case |
|-----------|--------------|------------|
| `insert` | O(log n) | O(n) |
| `range_query` | O(log n + m) | O(n) |
| `get_all_rectangles` | O(n) | O(n) |
| `is_empty` | O(1) | O(1) |
| `get_size` | O(1) | O(1) |
| `clear` | O(1) | O(1) |

Where n is the number of rectangles and m is the number of results.

## Notes

- Rectangles are stored with their minimum bounding rectangles (MBR)
- Node capacity is configurable via max_entries and min_entries
- Range queries return all rectangles that intersect the query rectangle
- Data can be associated with rectangles for additional information
- Tree structure may become unbalanced, affecting worst-case performance
- Performance is best for 2D spatial data
