# Tarjan's Algorithm API Documentation

This document provides detailed API documentation for the Tarjan's algorithm implementation for finding strongly connected components and articulation points.

## Classes

### Graph

Graph representation for Tarjan's algorithm.

#### Methods

##### `__init__(num_vertices: int, directed: bool = True) -> None`

Initialize graph.

**Parameters:**
- `num_vertices`: Number of vertices
- `directed`: `True` for directed graph, `False` for undirected (default: `True`)

**Example:**
```python
graph = Graph(10, directed=True)
```

##### `add_edge(u: int, v: int) -> None`

Add edge to graph.

**Parameters:**
- `u`: Source vertex
- `v`: Destination vertex

**Raises:**
- `ValueError`: If vertices are invalid

**Example:**
```python
graph.add_edge(0, 1)
```

### TarjanAlgorithm

Main class for Tarjan's algorithm.

#### Methods

##### `__init__(graph: Graph, config_path: str = "config.yaml") -> None`

Initialize Tarjan's algorithm.

**Parameters:**
- `graph`: Graph to analyze
- `config_path`: Path to configuration YAML file (default: "config.yaml")

**Example:**
```python
tarjan = TarjanAlgorithm(graph)
```

##### `find_strongly_connected_components() -> List[List[int]]`

Find strongly connected components in directed graph.

**Returns:**
- List of strongly connected components (each SCC is a list of vertices)

**Raises:**
- `ValueError`: If graph is undirected

**Time Complexity:** O(V + E)

**Example:**
```python
sccs = tarjan.find_strongly_connected_components()
for scc in sccs:
    print(f"SCC: {scc}")
```

##### `find_articulation_points() -> Set[int]`

Find articulation points in undirected graph.

**Returns:**
- Set of articulation point vertices

**Raises:**
- `ValueError`: If graph is directed

**Time Complexity:** O(V + E)

**Example:**
```python
articulation_points = tarjan.find_articulation_points()
print(f"Articulation points: {articulation_points}")
```

##### `get_scc_count() -> int`

Get number of strongly connected components.

**Returns:**
- Number of SCCs

**Example:**
```python
count = tarjan.get_scc_count()
```

##### `get_articulation_point_count() -> int`

Get number of articulation points.

**Returns:**
- Number of articulation points

**Example:**
```python
count = tarjan.get_articulation_point_count()
```

## Usage Examples

### Strongly Connected Components

```python
from src.main import Graph, TarjanAlgorithm

# Create directed graph
graph = Graph(5, directed=True)
graph.add_edge(0, 1)
graph.add_edge(1, 2)
graph.add_edge(2, 0)
graph.add_edge(1, 3)
graph.add_edge(3, 4)

# Find SCCs
tarjan = TarjanAlgorithm(graph)
sccs = tarjan.find_strongly_connected_components()

print(f"Number of SCCs: {tarjan.get_scc_count()}")
for i, scc in enumerate(sccs):
    print(f"SCC {i}: {scc}")
```

### Articulation Points

```python
from src.main import Graph, TarjanAlgorithm

# Create undirected graph
graph = Graph(5, directed=False)
graph.add_edge(0, 1)
graph.add_edge(1, 2)
graph.add_edge(2, 3)
graph.add_edge(3, 4)

# Find articulation points
tarjan = TarjanAlgorithm(graph)
articulation_points = tarjan.find_articulation_points()

print(f"Number of articulation points: {tarjan.get_articulation_point_count()}")
print(f"Articulation points: {sorted(articulation_points)}")
```

### Complex Graph Analysis

```python
from src.main import Graph, TarjanAlgorithm

# Analyze directed graph for SCCs
graph1 = Graph(6, directed=True)
graph1.add_edge(0, 1)
graph1.add_edge(1, 2)
graph1.add_edge(2, 0)
graph1.add_edge(1, 3)
graph1.add_edge(3, 4)
graph1.add_edge(4, 5)
graph1.add_edge(5, 3)

tarjan1 = TarjanAlgorithm(graph1)
sccs = tarjan1.find_strongly_connected_components()
print(f"SCCs: {sccs}")

# Analyze undirected graph for articulation points
graph2 = Graph(6, directed=False)
graph2.add_edge(0, 1)
graph2.add_edge(1, 2)
graph2.add_edge(2, 0)
graph2.add_edge(1, 3)
graph2.add_edge(3, 4)
graph2.add_edge(4, 5)

tarjan2 = TarjanAlgorithm(graph2)
articulation_points = tarjan2.find_articulation_points()
print(f"Articulation points: {articulation_points}")
```

### Error Handling

```python
from src.main import Graph, TarjanAlgorithm

# Wrong graph type for SCCs
graph = Graph(5, directed=False)
tarjan = TarjanAlgorithm(graph)

try:
    tarjan.find_strongly_connected_components()
except ValueError as e:
    print(f"Error: {e}")

# Wrong graph type for articulation points
graph2 = Graph(5, directed=True)
tarjan2 = TarjanAlgorithm(graph2)

try:
    tarjan2.find_articulation_points()
except ValueError as e:
    print(f"Error: {e}")

# Invalid vertices
graph3 = Graph(5)
try:
    graph3.add_edge(-1, 1)
except ValueError as e:
    print(f"Error: {e}")
```

## Time Complexity Summary

| Operation | Time Complexity |
|-----------|----------------|
| `add_edge` | O(1) |
| `find_strongly_connected_components` | O(V + E) |
| `find_articulation_points` | O(V + E) |
| `get_scc_count` | O(1) |
| `get_articulation_point_count` | O(1) |

Where V is the number of vertices and E is the number of edges.

## Notes

- Strongly connected components require directed graphs
- Articulation points require undirected graphs
- Both algorithms use DFS with discovery times and low-link values
- Algorithms are optimal with O(V + E) time complexity
- Results are deterministic and complete
