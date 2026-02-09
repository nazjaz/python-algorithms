# K-D Tree API Documentation

This document provides detailed API documentation for the k-d tree implementation with multidimensional range queries and nearest neighbor search.

## Classes

### KDNode

Node in k-d tree.

#### Attributes

- `point` (List[float]): Point coordinates in k-dimensional space
- `dimension` (int): Dimension used for splitting at this node
- `left` (Optional[KDNode]): Left child node
- `right` (Optional[KDNode]): Right child node

#### Methods

##### `__init__(point: List[float], dimension: int = 0) -> None`

Initialize KDNode.

**Parameters:**
- `point`: Point coordinates in k-dimensional space
- `dimension`: Dimension used for splitting at this node

**Example:**
```python
node = KDNode([1.0, 2.0, 3.0], dimension=1)
```

### KDTree

Main class for k-d tree data structure.

#### Methods

##### `__init__(points: Optional[List[List[float]]] = None, config_path: str = "config.yaml") -> None`

Initialize k-d tree.

**Parameters:**
- `points`: Optional list of points to build tree from
- `config_path`: Path to configuration YAML file (default: "config.yaml")

**Example:**
```python
# Empty tree
tree = KDTree()

# Tree from points
points = [[1, 2], [3, 4], [5, 6]]
tree = KDTree(points)
```

##### `build_tree(points: List[List[float]]) -> None`

Build k-d tree from list of points.

**Parameters:**
- `points`: List of points, each point is a list of coordinates

**Raises:**
- `ValueError`: If points have inconsistent dimensions

**Time Complexity:** O(n log n)

**Example:**
```python
points = [[1, 2], [3, 4], [5, 6]]
tree = KDTree()
tree.build_tree(points)
```

##### `insert(point: List[float]) -> None`

Insert point into tree.

**Parameters:**
- `point`: Point coordinates to insert

**Raises:**
- `ValueError`: If point dimensions don't match tree dimension

**Time Complexity:** O(log n) average

**Example:**
```python
tree.insert([7, 8])
```

##### `range_query(min_range: List[float], max_range: List[float]) -> List[List[float]]`

Find all points within given range.

**Parameters:**
- `min_range`: Minimum bounds for each dimension
- `max_range`: Maximum bounds for each dimension

**Returns:**
- List of points within range

**Raises:**
- `ValueError`: If range dimensions don't match tree dimension or invalid range

**Time Complexity:** O(n^(1-1/k) + m) where m is number of results

**Example:**
```python
results = tree.range_query([3, 3], [7, 7])
for point in results:
    print(point)
```

##### `nearest_neighbor(query_point: List[float]) -> Optional[List[float]]`

Find nearest neighbor to query point.

**Parameters:**
- `query_point`: Query point coordinates

**Returns:**
- Nearest point or None if tree is empty

**Raises:**
- `ValueError`: If query point dimension doesn't match tree dimension

**Time Complexity:** O(log n) average, O(n) worst case

**Example:**
```python
nearest = tree.nearest_neighbor([6, 5])
print(f"Nearest: {nearest}")
```

##### `k_nearest_neighbors(query_point: List[float], k: int) -> List[List[float]]`

Find k nearest neighbors to query point.

**Parameters:**
- `query_point`: Query point coordinates
- `k`: Number of neighbors to find

**Returns:**
- List of k nearest points

**Raises:**
- `ValueError`: If query point dimension doesn't match tree dimension or k <= 0

**Time Complexity:** O(k log n) average

**Example:**
```python
k_nearest = tree.k_nearest_neighbors([6, 5], 3)
for point in k_nearest:
    print(point)
```

##### `get_all_points() -> List[List[float]]`

Get all points in tree.

**Returns:**
- List of all points

**Time Complexity:** O(n)

**Example:**
```python
all_points = tree.get_all_points()
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

Get number of points in tree.

**Returns:**
- Number of points

**Time Complexity:** O(1)

**Example:**
```python
size = tree.get_size()
```

##### `get_dimension() -> int`

Get dimension of points in tree.

**Returns:**
- Dimension of points

**Time Complexity:** O(1)

**Example:**
```python
dim = tree.get_dimension()
```

##### `clear() -> None`

Clear all points from tree.

**Example:**
```python
tree.clear()
```

## Usage Examples

### Basic Operations

```python
from src.main import KDTree

# Create tree from points
points = [[2, 3], [5, 4], [9, 6], [4, 7], [8, 1], [7, 2]]
tree = KDTree(points)

# Range query
results = tree.range_query([3, 3], [7, 7])
for point in results:
    print(f"Point in range: {point}")

# Nearest neighbor
nearest = tree.nearest_neighbor([6, 5])
print(f"Nearest: {nearest}")

# K-nearest neighbors
k_nearest = tree.k_nearest_neighbors([6, 5], 3)
for point in k_nearest:
    print(f"Neighbor: {point}")
```

### 3D Example

```python
from src.main import KDTree

# Create 3D tree
points_3d = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [2, 3, 4]]
tree = KDTree(points_3d)

# 3D range query
results = tree.range_query([2, 2, 2], [5, 5, 5])
print(f"Points in 3D range: {results}")

# 3D nearest neighbor
nearest = tree.nearest_neighbor([3, 4, 5])
print(f"Nearest 3D point: {nearest}")
```

### Incremental Building

```python
from src.main import KDTree

# Create empty tree
tree = KDTree()

# Insert points one by one
tree.insert([1, 2])
tree.insert([3, 4])
tree.insert([5, 6])

# Query
results = tree.range_query([0, 0], [10, 10])
```

### Machine Learning Example

```python
from src.main import KDTree
import random

# Generate training data
training_data = [[random.random() * 100, random.random() * 100] 
                 for _ in range(1000)]
tree = KDTree(training_data)

# Query for k-NN classification
query_point = [50, 50]
k_nearest = tree.k_nearest_neighbors(query_point, 5)
print(f"5 nearest neighbors: {k_nearest}")

# Calculate distances (for classification)
for neighbor in k_nearest:
    distance = ((neighbor[0] - query_point[0])**2 + 
                (neighbor[1] - query_point[1])**2)**0.5
    print(f"Distance: {distance}")
```

### Error Handling

```python
from src.main import KDTree

tree = KDTree([[1, 2], [3, 4]])

# Wrong dimension
try:
    tree.insert([1, 2, 3])
except ValueError as e:
    print(f"Error: {e}")

# Invalid range
try:
    tree.range_query([10, 10], [5, 5])
except ValueError as e:
    print(f"Error: {e}")

# Invalid k
try:
    tree.k_nearest_neighbors([1, 2], 0)
except ValueError as e:
    print(f"Error: {e}")
```

## Time Complexity Summary

| Operation | Average Case | Worst Case |
|-----------|--------------|------------|
| `build_tree` | O(n log n) | O(n log n) |
| `insert` | O(log n) | O(n) |
| `range_query` | O(n^(1-1/k) + m) | O(n) |
| `nearest_neighbor` | O(log n) | O(n) |
| `k_nearest_neighbors` | O(k log n) | O(kn) |
| `get_all_points` | O(n) | O(n) |
| `is_empty` | O(1) | O(1) |
| `get_size` | O(1) | O(1) |
| `get_dimension` | O(1) | O(1) |
| `clear` | O(1) | O(1) |

Where n is the number of points, k is the dimension, and m is the number of results.

## Notes

- Points must have consistent dimensions throughout the tree
- Tree structure may become unbalanced with incremental insertion
- Performance degrades significantly in high dimensions (k > 20)
- Range queries return all points within the hyperrectangle
- Nearest neighbor uses Euclidean distance
- K-nearest neighbors returns up to k points (fewer if tree has fewer points)
