# Maximum Flow API Documentation

This document provides detailed API documentation for the maximum flow implementation using Ford-Fulkerson, Edmonds-Karp, and Dinic's algorithms.

## Classes

### FlowNetwork

Represents a flow network with vertices and edges with capacities.

#### Methods

##### `__init__(num_vertices: int) -> None`

Initialize a flow network.

**Parameters:**
- `num_vertices`: Number of vertices in the graph

**Raises:**
- `ValueError`: If num_vertices < 2

**Example:**
```python
network = FlowNetwork(6)
```

##### `add_edge(u: int, v: int, capacity: int) -> None`

Add edge with capacity to network.

**Parameters:**
- `u`: Source vertex
- `v`: Destination vertex
- `capacity`: Edge capacity (must be non-negative)

**Raises:**
- `ValueError`: If vertices are invalid or capacity is negative

**Example:**
```python
network.add_edge(0, 1, 10)
```

##### `get_capacity(u: int, v: int) -> int`

Get capacity of edge.

**Parameters:**
- `u`: Source vertex
- `v`: Destination vertex

**Returns:**
- Edge capacity, 0 if edge doesn't exist

**Example:**
```python
capacity = network.get_capacity(0, 1)  # Returns 10
```

##### `get_residual_capacity(u: int, v: int) -> int`

Get residual capacity of edge.

**Parameters:**
- `u`: Source vertex
- `v`: Destination vertex

**Returns:**
- Residual capacity, 0 if edge doesn't exist

##### `update_residual(u: int, v: int, flow: int) -> None`

Update residual capacities after sending flow.

**Parameters:**
- `u`: Source vertex
- `v`: Destination vertex
- `flow`: Flow amount to send

### MaxFlowSolver

Solver for maximum flow problems with multiple algorithms.

#### Methods

##### `__init__(network: FlowNetwork) -> None`

Initialize max flow solver.

**Parameters:**
- `network`: Flow network to solve

**Example:**
```python
solver = MaxFlowSolver(network)
```

##### `ford_fulkerson(source: int, sink: int) -> Tuple[int, Dict[Tuple[int, int], int]]`

Compute maximum flow using Ford-Fulkerson algorithm.

**Parameters:**
- `source`: Source vertex
- `sink`: Sink vertex

**Returns:**
- Tuple of (max_flow, flow_dict) where flow_dict maps (u, v) to flow

**Time Complexity:** O(E * max_flow)

**Raises:**
- `ValueError`: If source or sink is invalid

**Example:**
```python
max_flow, flow_dict = solver.ford_fulkerson(0, 5)
print(f"Maximum flow: {max_flow}")
```

##### `edmonds_karp(source: int, sink: int) -> Tuple[int, Dict[Tuple[int, int], int]]`

Compute maximum flow using Edmonds-Karp algorithm.

**Parameters:**
- `source`: Source vertex
- `sink`: Sink vertex

**Returns:**
- Tuple of (max_flow, flow_dict) where flow_dict maps (u, v) to flow

**Time Complexity:** O(V * E^2)

**Raises:**
- `ValueError`: If source or sink is invalid

**Example:**
```python
max_flow, flow_dict = solver.edmonds_karp(0, 5)
```

##### `dinic(source: int, sink: int) -> Tuple[int, Dict[Tuple[int, int], int]]`

Compute maximum flow using Dinic's algorithm.

**Parameters:**
- `source`: Source vertex
- `sink`: Sink vertex

**Returns:**
- Tuple of (max_flow, flow_dict) where flow_dict maps (u, v) to flow

**Time Complexity:** O(V^2 * E)

**Raises:**
- `ValueError`: If source or sink is invalid

**Example:**
```python
max_flow, flow_dict = solver.dinic(0, 5)
```

##### `get_min_cut(source: int, sink: int, algorithm: str = "edmonds_karp") -> Tuple[List[int], List[int]]`

Find minimum cut (source side and sink side).

**Parameters:**
- `source`: Source vertex
- `sink`: Sink vertex
- `algorithm`: Algorithm to use ("ford_fulkerson", "edmonds_karp", "dinic")

**Returns:**
- Tuple of (source_side, sink_side) vertex lists

**Raises:**
- `ValueError`: If algorithm name is invalid

**Example:**
```python
source_side, sink_side = solver.get_min_cut(0, 5)
print(f"Source side: {source_side}")
print(f"Sink side: {sink_side}")
```

## Usage Examples

### Basic Maximum Flow

```python
from src.main import FlowNetwork, MaxFlowSolver

# Create network
network = FlowNetwork(4)
network.add_edge(0, 1, 10)
network.add_edge(0, 2, 10)
network.add_edge(1, 3, 10)
network.add_edge(2, 3, 10)

# Solve
solver = MaxFlowSolver(network)
max_flow, flow_dict = solver.ford_fulkerson(0, 3)
print(f"Maximum flow: {max_flow}")
```

### Comparing Algorithms

```python
network = FlowNetwork(6)
# ... add edges ...

solver = MaxFlowSolver(network)

# Compare all three algorithms
flow_ff, _ = solver.ford_fulkerson(0, 5)
flow_ek, _ = solver.edmonds_karp(0, 5)
flow_dinic, _ = solver.dinic(0, 5)

print(f"Ford-Fulkerson: {flow_ff}")
print(f"Edmonds-Karp: {flow_ek}")
print(f"Dinic's: {flow_dinic}")
# All should be equal
```

### Flow Distribution

```python
network = FlowNetwork(6)
# ... add edges ...

solver = MaxFlowSolver(network)
max_flow, flow_dict = solver.edmonds_karp(0, 5)

# Print flow on each edge
for (u, v), flow in flow_dict.items():
    print(f"Edge ({u}, {v}): {flow} units")
```

### Minimum Cut

```python
network = FlowNetwork(6)
# ... add edges ...

solver = MaxFlowSolver(network)
source_side, sink_side = solver.get_min_cut(0, 5)

print(f"Vertices on source side: {source_side}")
print(f"Vertices on sink side: {sink_side}")
```

### Complex Network

```python
network = FlowNetwork(6)
network.add_edge(0, 1, 16)
network.add_edge(0, 2, 13)
network.add_edge(1, 2, 10)
network.add_edge(1, 3, 12)
network.add_edge(2, 1, 4)  # Reverse edge
network.add_edge(2, 4, 14)
network.add_edge(3, 2, 9)
network.add_edge(3, 5, 20)
network.add_edge(4, 3, 7)
network.add_edge(4, 5, 4)

solver = MaxFlowSolver(network)
max_flow, flow_dict = solver.dinic(0, 5)
print(f"Maximum flow: {max_flow}")
```

## Error Handling

The implementation handles the following cases gracefully:

- **Invalid vertices**: Raises `ValueError` for out-of-bounds vertices
- **Negative capacities**: Raises `ValueError` for negative edge capacities
- **Source equals sink**: Raises `ValueError` if source and sink are same
- **No path**: Returns 0 flow if no path exists from source to sink
- **Invalid algorithm**: Raises `ValueError` for unknown algorithm names

## Performance Characteristics

| Operation | Time Complexity | Space Complexity |
|-----------|----------------|------------------|
| Add Edge | O(1) | O(1) |
| Ford-Fulkerson | O(E * max_flow) | O(V + E) |
| Edmonds-Karp | O(V * E^2) | O(V + E) |
| Dinic's | O(V^2 * E) | O(V + E) |
| Minimum Cut | Same as flow | O(V + E) |

Where:
- V = number of vertices
- E = number of edges
- max_flow = maximum flow value

## Algorithm Selection Guide

**Use Ford-Fulkerson when:**
- Learning about maximum flow algorithms
- Graph is small with small capacities
- Educational purposes

**Use Edmonds-Karp when:**
- General purpose maximum flow
- Need polynomial time guarantee
- Graph is medium-sized

**Use Dinic's when:**
- Graph is large or dense
- Need best performance
- V^2 * E complexity is acceptable

## Thread Safety

This implementation is not thread-safe. For concurrent access, external synchronization is required.
