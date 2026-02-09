# Blossom Algorithm API Documentation

This document provides detailed API documentation for the blossom algorithm implementation for finding maximum matching in general graphs.

## Classes

### BlossomAlgorithm

Main class for blossom algorithm (Edmonds' algorithm).

#### Methods

##### `__init__(num_vertices: int, config_path: str = "config.yaml") -> None`

Initialize blossom algorithm.

**Parameters:**
- `num_vertices`: Number of vertices in graph
- `config_path`: Path to configuration YAML file (default: "config.yaml")

**Example:**
```python
blossom = BlossomAlgorithm(10)
```

##### `add_edge(u: int, v: int) -> None`

Add undirected edge to graph.

**Parameters:**
- `u`: First vertex
- `v`: Second vertex

**Raises:**
- `ValueError`: If vertices are invalid

**Example:**
```python
blossom.add_edge(0, 1)
```

##### `find_maximum_matching() -> Dict[int, int]`

Find maximum matching in graph.

**Returns:**
- Dictionary mapping vertex to its matched vertex

**Time Complexity:** O(V^2 E)

**Example:**
```python
matching = blossom.find_maximum_matching()
print(f"Matching: {matching}")
```

##### `get_matching_size() -> int`

Get size of current matching.

**Returns:**
- Number of edges in matching

**Time Complexity:** O(V)

**Example:**
```python
size = blossom.get_matching_size()
print(f"Matching size: {size}")
```

##### `is_matched(vertex: int) -> bool`

Check if vertex is matched.

**Parameters:**
- `vertex`: Vertex to check

**Returns:**
- `True` if matched, `False` otherwise

**Raises:**
- `ValueError`: If vertex is invalid

**Time Complexity:** O(1)

**Example:**
```python
if blossom.is_matched(0):
    print("Vertex 0 is matched")
```

##### `get_matched_vertex(vertex: int) -> Optional[int]`

Get vertex matched to given vertex.

**Parameters:**
- `vertex`: Vertex to check

**Returns:**
- Matched vertex or `None` if not matched

**Raises:**
- `ValueError`: If vertex is invalid

**Time Complexity:** O(1)

**Example:**
```python
matched = blossom.get_matched_vertex(0)
if matched is not None:
    print(f"Vertex 0 matched to {matched}")
```

## Usage Examples

### Basic Usage

```python
from src.main import BlossomAlgorithm

# Create blossom algorithm
blossom = BlossomAlgorithm(6)

# Add edges
blossom.add_edge(0, 1)
blossom.add_edge(1, 2)
blossom.add_edge(2, 3)
blossom.add_edge(3, 4)
blossom.add_edge(4, 5)
blossom.add_edge(5, 0)

# Find maximum matching
matching = blossom.find_maximum_matching()
print(f"Matching size: {blossom.get_matching_size()}")
print(f"Matching: {matching}")
```

### Checking Matching Status

```python
from src.main import BlossomAlgorithm

blossom = BlossomAlgorithm(4)
blossom.add_edge(0, 1)
blossom.add_edge(2, 3)

blossom.find_maximum_matching()

# Check if vertices are matched
for i in range(4):
    if blossom.is_matched(i):
        matched = blossom.get_matched_vertex(i)
        print(f"Vertex {i} matched to {matched}")
    else:
        print(f"Vertex {i} is unmatched")
```

### Different Graph Types

```python
from src.main import BlossomAlgorithm

# Path graph
blossom = BlossomAlgorithm(5)
blossom.add_edge(0, 1)
blossom.add_edge(1, 2)
blossom.add_edge(2, 3)
blossom.add_edge(3, 4)

matching = blossom.find_maximum_matching()
print(f"Path graph matching size: {blossom.get_matching_size()}")

# Cycle graph
blossom2 = BlossomAlgorithm(6)
for i in range(6):
    blossom2.add_edge(i, (i + 1) % 6)

matching2 = blossom2.find_maximum_matching()
print(f"Cycle graph matching size: {blossom2.get_matching_size()}")

# Complete graph
blossom3 = BlossomAlgorithm(4)
for i in range(4):
    for j in range(i + 1, 4):
        blossom3.add_edge(i, j)

matching3 = blossom3.find_maximum_matching()
print(f"Complete graph matching size: {blossom3.get_matching_size()}")
```

### Error Handling

```python
from src.main import BlossomAlgorithm

blossom = BlossomAlgorithm(5)

# Invalid vertices
try:
    blossom.add_edge(-1, 1)
except ValueError as e:
    print(f"Error: {e}")

try:
    blossom.is_matched(10)
except ValueError as e:
    print(f"Error: {e}")
```

## Time Complexity Summary

| Operation | Time Complexity |
|-----------|----------------|
| `add_edge` | O(1) |
| `find_maximum_matching` | O(V^2 E) |
| `get_matching_size` | O(V) |
| `is_matched` | O(1) |
| `get_matched_vertex` | O(1) |

Where V is the number of vertices and E is the number of edges.

## Notes

- Blossom algorithm works on general graphs (not just bipartite)
- Handles odd cycles by contracting them into blossoms
- Finds maximum matching (not just any matching)
- Matching is stored internally and can be queried
- Algorithm is based on Edmonds' algorithm
