# Breadth-First Search API Documentation

## Overview

The Breadth-First Search implementation provides BFS algorithm for traversing graphs and finding shortest paths in unweighted graphs. BFS explores all vertices at the current depth level before moving to the next level, making it ideal for shortest path finding.

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

### BFS

Breadth-First Search implementation for shortest path finding.

#### Constructor

```python
BFS(config_path: str = "config.yaml") -> None
```

Initialize BFS with configuration.

#### Methods

##### bfs_traversal

```python
bfs_traversal(graph: Graph, start: Any) -> List[Any]
```

Perform BFS traversal starting from given vertex.

**Parameters:**
- `graph` (Graph): Graph to traverse
- `start` (Any): Starting vertex

**Returns:**
- `List[Any]`: List of vertices in BFS order

**Time Complexity:** O(V + E)
**Space Complexity:** O(V) for queue and visited set

##### shortest_path

```python
shortest_path(
    graph: Graph, start: Any, target: Any
) -> Tuple[Optional[List[Any]], int]
```

Find shortest path from start to target using BFS.

BFS guarantees shortest path in unweighted graphs because it explores vertices level by level, ensuring the first path found is the shortest.

**Parameters:**
- `graph` (Graph): Graph to search
- `start` (Any): Starting vertex
- `target` (Any): Target vertex

**Returns:**
- `Tuple[Optional[List[Any]], int]`: Tuple of (path, distance)
  - `path`: List of vertices from start to target, or None if no path
  - `distance`: Number of edges in shortest path, or -1 if no path

**Time Complexity:** O(V + E)
**Space Complexity:** O(V)

##### shortest_distances

```python
shortest_distances(graph: Graph, start: Any) -> Dict[Any, int]
```

Find shortest distances from start to all reachable vertices.

**Parameters:**
- `graph` (Graph): Graph to search
- `start` (Any): Starting vertex

**Returns:**
- `Dict[Any, int]`: Dictionary mapping each vertex to its shortest distance from start. Unreachable vertices are not included.

**Time Complexity:** O(V + E)
**Space Complexity:** O(V)

##### level_order_traversal

```python
level_order_traversal(graph: Graph, start: Any) -> List[List[Any]]
```

Get vertices grouped by level (distance from start).

**Parameters:**
- `graph` (Graph): Graph to traverse
- `start` (Any): Starting vertex

**Returns:**
- `List[List[Any]]`: List of lists, where each inner list contains vertices at that level

**Time Complexity:** O(V + E)
**Space Complexity:** O(V)

##### bfs_all_components

```python
bfs_all_components(graph: Graph) -> List[List[Any]]
```

Perform BFS on all connected components.

**Parameters:**
- `graph` (Graph): Graph to traverse

**Returns:**
- `List[List[Any]]`: List of traversal orders for each component

**Time Complexity:** O(V + E)
**Space Complexity:** O(V)

## Usage Examples

### Basic BFS Traversal

```python
from src.main import Graph, BFS

graph = Graph()
graph.add_edge(0, 1)
graph.add_edge(0, 2)
graph.add_edge(1, 3)

bfs = BFS()
traversal = bfs.bfs_traversal(graph, 0)
print(traversal)  # [0, 1, 2, 3]
```

### Shortest Path Finding

```python
bfs = BFS()
path, distance = bfs.shortest_path(graph, 0, 3)
print(path)  # [0, 1, 3]
print(distance)  # 2
```

### Shortest Distances

```python
bfs = BFS()
distances = bfs.shortest_distances(graph, 0)
print(distances)  # {0: 0, 1: 1, 2: 1, 3: 2}
```

### Level-Order Traversal

```python
bfs = BFS()
levels = bfs.level_order_traversal(graph, 0)
print(levels)  # [[0], [1, 2], [3]]
```
