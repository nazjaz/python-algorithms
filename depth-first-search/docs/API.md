# Depth-First Search API Documentation

## Overview

The Depth-First Search implementation provides both recursive and iterative approaches for traversing graphs. It includes graph representation, path finding, connected component detection, and comprehensive visualization.

## Classes

### Graph

Graph data structure using adjacency list representation.

#### Constructor

```python
Graph(directed: bool = False) -> None
```

Initialize graph.

**Parameters:**
- `directed` (bool): If True, graph is directed; if False, undirected

#### Methods

##### add_edge

```python
add_edge(u: Any, v: Any) -> None
```

Add edge to graph.

**Parameters:**
- `u` (Any): First vertex
- `v` (Any): Second vertex

##### add_vertex

```python
add_vertex(vertex: Any) -> None
```

Add vertex to graph.

**Parameters:**
- `vertex` (Any): Vertex to add

##### get_vertices

```python
get_vertices() -> List[Any]
```

Get all vertices in graph.

**Returns:**
- `List[Any]`: List of all vertices

##### get_neighbors

```python
get_neighbors(vertex: Any) -> List[Any]
```

Get neighbors of a vertex.

**Parameters:**
- `vertex` (Any): Vertex to get neighbors for

**Returns:**
- `List[Any]`: List of neighboring vertices

### DFS

Depth-First Search implementation with recursive and iterative methods.

#### Constructor

```python
DFS(config_path: str = "config.yaml") -> None
```

Initialize DFS with configuration.

#### Methods

##### dfs_recursive

```python
dfs_recursive(
    graph: Graph, start: Any, track_path: bool = True
) -> List[Any]
```

Perform DFS using recursive approach.

**Parameters:**
- `graph` (Graph): Graph to traverse
- `start` (Any): Starting vertex
- `track_path` (bool): If True, track traversal path

**Returns:**
- `List[Any]`: List of vertices in DFS order

**Time Complexity:** O(V + E)
**Space Complexity:** O(V) for recursion stack

##### dfs_iterative

```python
dfs_iterative(
    graph: Graph, start: Any, track_path: bool = True
) -> List[Any]
```

Perform DFS using iterative approach with stack.

**Parameters:**
- `graph` (Graph): Graph to traverse
- `start` (Any): Starting vertex
- `track_path` (bool): If True, track traversal path

**Returns:**
- `List[Any]`: List of vertices in DFS order

**Time Complexity:** O(V + E)
**Space Complexity:** O(V) for stack

##### find_path

```python
find_path(
    graph: Graph, start: Any, target: Any, method: str = "recursive"
) -> Optional[List[Any]]
```

Find path from start to target using DFS.

**Parameters:**
- `graph` (Graph): Graph to search
- `start` (Any): Starting vertex
- `target` (Any): Target vertex
- `method` (str): Method to use ('recursive' or 'iterative')

**Returns:**
- `Optional[List[Any]]`: Path from start to target, or None if no path exists

##### dfs_all_components

```python
dfs_all_components(
    graph: Graph, method: str = "recursive"
) -> List[List[Any]]
```

Perform DFS on all connected components.

**Parameters:**
- `graph` (Graph): Graph to traverse
- `method` (str): Method to use ('recursive' or 'iterative')

**Returns:**
- `List[List[Any]]`: List of traversal paths for each component

##### compare_methods

```python
compare_methods(graph: Graph, start: Any) -> Dict[str, Dict[str, Any]]
```

Compare recursive and iterative DFS methods.

**Parameters:**
- `graph` (Graph): Graph to traverse
- `start` (Any): Starting vertex

**Returns:**
- `Dict[str, Dict[str, Any]]`: Dictionary with comparison results

## Usage Examples

### Basic DFS

```python
from src.main import Graph, DFS

graph = Graph()
graph.add_edge(0, 1)
graph.add_edge(0, 2)
graph.add_edge(1, 3)

dfs = DFS()
path = dfs.dfs_recursive(graph, 0)
print(path)  # [0, 1, 3, 2]
```

### Iterative DFS

```python
dfs = DFS()
path = dfs.dfs_iterative(graph, 0)
print(path)  # [0, 1, 3, 2]
```

### Path Finding

```python
dfs = DFS()
path = dfs.find_path(graph, 0, 3, method="recursive")
print(path)  # [0, 1, 3]
```

### Connected Components

```python
dfs = DFS()
components = dfs.dfs_all_components(graph, method="recursive")
print(components)  # [[0, 1, 3, 2], [4, 5]]
```
