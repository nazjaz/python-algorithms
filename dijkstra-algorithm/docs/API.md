# Dijkstra's Algorithm API Documentation

## Overview

The Dijkstra's algorithm implementation provides shortest path finding in weighted graphs using a priority queue (min-heap) for efficient vertex selection. It guarantees optimal shortest paths when all edge weights are non-negative.

## Classes

### WeightedGraph

Graph data structure with weighted edges using adjacency list representation.

#### Constructor

```python
WeightedGraph(directed: bool = False) -> None
```

Initialize weighted graph.

**Parameters:**
- `directed` (bool): If True, graph is directed; if False, undirected

#### Methods

##### add_edge

```python
add_edge(u: Any, v: Any, weight: float) -> None
```

Add weighted edge to graph.

**Parameters:**
- `u` (Any): First vertex
- `v` (Any): Second vertex
- `weight` (float): Edge weight (must be non-negative for Dijkstra's algorithm)

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
get_neighbors(vertex: Any) -> List[Tuple[Any, float]]
```

Get neighbors of a vertex with their edge weights.

**Parameters:**
- `vertex` (Any): Vertex to get neighbors for

**Returns:**
- `List[Tuple[Any, float]]`: List of tuples (neighbor, weight)

### Dijkstra

Dijkstra's algorithm implementation with priority queue optimization.

#### Constructor

```python
Dijkstra(config_path: str = "config.yaml") -> None
```

Initialize Dijkstra with configuration.

#### Methods

##### shortest_path

```python
shortest_path(
    graph: WeightedGraph, start: Any, target: Any
) -> Tuple[Optional[List[Any]], float]
```

Find shortest path from start to target using Dijkstra's algorithm.

**Parameters:**
- `graph` (WeightedGraph): Weighted graph to search
- `start` (Any): Starting vertex
- `target` (Any): Target vertex

**Returns:**
- `Tuple[Optional[List[Any]], float]`: Tuple of (path, distance)
  - `path`: List of vertices from start to target, or None if no path
  - `distance`: Shortest distance, or float('inf') if no path

**Time Complexity:** O((V + E) log V) with binary heap
**Space Complexity:** O(V)

##### shortest_distances

```python
shortest_distances(graph: WeightedGraph, start: Any) -> Dict[Any, float]
```

Find shortest distances from start to all reachable vertices.

**Parameters:**
- `graph` (WeightedGraph): Weighted graph to search
- `start` (Any): Starting vertex

**Returns:**
- `Dict[Any, float]`: Dictionary mapping each vertex to its shortest distance from start. Unreachable vertices are not included.

**Time Complexity:** O((V + E) log V)
**Space Complexity:** O(V)

##### shortest_paths_from_source

```python
shortest_paths_from_source(
    graph: WeightedGraph, start: Any
) -> Dict[Any, Tuple[Optional[List[Any]], float]]
```

Find shortest paths from start to all reachable vertices.

**Parameters:**
- `graph` (WeightedGraph): Weighted graph to search
- `start` (Any): Starting vertex

**Returns:**
- `Dict[Any, Tuple[Optional[List[Any]], float]]`: Dictionary mapping each vertex to (path, distance) tuple. Unreachable vertices are not included.

**Time Complexity:** O((V + E) log V)
**Space Complexity:** O(V)

## Usage Examples

### Basic Shortest Path

```python
from src.main import WeightedGraph, Dijkstra

graph = WeightedGraph()
graph.add_edge(0, 1, 4.0)
graph.add_edge(0, 2, 1.0)
graph.add_edge(1, 3, 1.0)
graph.add_edge(2, 3, 5.0)

dijkstra = Dijkstra()
path, distance = dijkstra.shortest_path(graph, 0, 3)
print(path)  # [0, 1, 3]
print(distance)  # 5.0
```

### Shortest Distances

```python
dijkstra = Dijkstra()
distances = dijkstra.shortest_distances(graph, 0)
print(distances)  # {0: 0.0, 1: 4.0, 2: 1.0, 3: 5.0}
```

### All Shortest Paths

```python
dijkstra = Dijkstra()
paths = dijkstra.shortest_paths_from_source(graph, 0)
for vertex, (path, dist) in paths.items():
    print(f"{vertex}: {path} (distance: {dist})")
```

## Priority Queue Optimization

The implementation uses Python's `heapq` module (min-heap) for efficient priority queue operations:

- **Insertion**: O(log n)
- **Extract minimum**: O(log n)
- **More efficient** than checking all vertices each iteration

This ensures optimal performance for large graphs.
