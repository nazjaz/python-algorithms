# Min-Cost Max-Flow API Documentation

This document provides detailed API documentation for the min-cost max-flow implementation using successive shortest paths and cycle canceling algorithms.

## Classes

### Edge

Edge in flow network.

#### Attributes

- `to` (int): Destination vertex
- `capacity` (float): Edge capacity
- `cost` (float): Edge cost per unit flow
- `flow` (float): Current flow on edge
- `reverse` (Optional[Edge]): Reverse edge

#### Methods

##### `__init__(to: int, capacity: float, cost: float, reverse: Optional[Edge] = None) -> None`

Initialize edge.

**Parameters:**
- `to`: Destination vertex
- `capacity`: Edge capacity
- `cost`: Edge cost per unit flow
- `reverse`: Reverse edge

**Example:**
```python
edge = Edge(to=1, capacity=10.0, cost=2.0)
```

### FlowNetwork

Flow network for min-cost max-flow algorithms.

#### Methods

##### `__init__(num_vertices: int) -> None`

Initialize flow network.

**Parameters:**
- `num_vertices`: Number of vertices in network

**Example:**
```python
network = FlowNetwork(5)
```

##### `add_edge(from_vertex: int, to_vertex: int, capacity: float, cost: float) -> None`

Add edge to network.

**Parameters:**
- `from_vertex`: Source vertex
- `to_vertex`: Destination vertex
- `capacity`: Edge capacity
- `cost`: Edge cost per unit flow

**Example:**
```python
network.add_edge(0, 1, 10.0, 2.0)
```

##### `get_residual_capacity(edge: Edge) -> float`

Get residual capacity of edge.

**Parameters:**
- `edge`: Edge to check

**Returns:**
- Residual capacity

**Example:**
```python
capacity = network.get_residual_capacity(edge)
```

##### `is_residual(edge: Edge) -> bool`

Check if edge has residual capacity.

**Parameters:**
- `edge`: Edge to check

**Returns:**
- `True` if has residual capacity, `False` otherwise

**Example:**
```python
if network.is_residual(edge):
    print("Edge has residual capacity")
```

### MinCostMaxFlow

Main class for min-cost max-flow solver.

#### Methods

##### `__init__(network: FlowNetwork, config_path: str = "config.yaml") -> None`

Initialize min-cost max-flow solver.

**Parameters:**
- `network`: Flow network
- `config_path`: Path to configuration YAML file (default: "config.yaml")

**Example:**
```python
solver = MinCostMaxFlow(network)
```

##### `successive_shortest_paths(source: int, sink: int) -> Tuple[float, float]`

Solve min-cost max-flow using successive shortest paths.

**Parameters:**
- `source`: Source vertex
- `sink`: Sink vertex

**Returns:**
- Tuple of (max_flow, min_cost)

**Time Complexity:** O(V E log V)

**Example:**
```python
flow, cost = solver.successive_shortest_paths(0, 3)
print(f"Max Flow: {flow}, Min Cost: {cost}")
```

##### `cycle_canceling(source: int, sink: int) -> Tuple[float, float]`

Solve min-cost max-flow using cycle canceling.

**Parameters:**
- `source`: Source vertex
- `sink`: Sink vertex

**Returns:**
- Tuple of (max_flow, min_cost)

**Time Complexity:** O(V^2 E)

**Example:**
```python
flow, cost = solver.cycle_canceling(0, 3)
print(f"Max Flow: {flow}, Min Cost: {cost}")
```

##### `get_flow() -> Dict[Tuple[int, int], float]`

Get flow on each edge.

**Returns:**
- Dictionary mapping (from, to) to flow

**Example:**
```python
flow_dict = solver.get_flow()
for (u, v), flow in flow_dict.items():
    print(f"Flow from {u} to {v}: {flow}")
```

## Usage Examples

### Basic Usage

```python
from src.main import FlowNetwork, MinCostMaxFlow

# Create flow network
network = FlowNetwork(4)
network.add_edge(0, 1, 10.0, 1.0)
network.add_edge(0, 2, 5.0, 2.0)
network.add_edge(1, 2, 15.0, 1.0)
network.add_edge(1, 3, 10.0, 3.0)
network.add_edge(2, 3, 10.0, 1.0)

# Solve using successive shortest paths
solver = MinCostMaxFlow(network)
flow, cost = solver.successive_shortest_paths(0, 3)
print(f"Max Flow: {flow}, Min Cost: {cost}")
```

### Cycle Canceling

```python
from src.main import FlowNetwork, MinCostMaxFlow

# Create flow network
network = FlowNetwork(4)
network.add_edge(0, 1, 10.0, 1.0)
network.add_edge(1, 2, 10.0, 2.0)
network.add_edge(2, 3, 10.0, 1.0)

# Solve using cycle canceling
solver = MinCostMaxFlow(network)
flow, cost = solver.cycle_canceling(0, 3)
print(f"Max Flow: {flow}, Min Cost: {cost}")
```

### Getting Flow Details

```python
from src.main import FlowNetwork, MinCostMaxFlow

network = FlowNetwork(3)
network.add_edge(0, 1, 10.0, 1.0)
network.add_edge(1, 2, 10.0, 1.0)

solver = MinCostMaxFlow(network)
flow, cost = solver.successive_shortest_paths(0, 2)

# Get flow on each edge
flow_dict = solver.get_flow()
for (u, v), f in flow_dict.items():
    print(f"Edge ({u}, {v}): flow = {f}")
```

### Comparing Algorithms

```python
from src.main import FlowNetwork, MinCostMaxFlow

network1 = FlowNetwork(4)
network1.add_edge(0, 1, 10.0, 1.0)
network1.add_edge(1, 3, 10.0, 1.0)

network2 = FlowNetwork(4)
network2.add_edge(0, 1, 10.0, 1.0)
network2.add_edge(1, 3, 10.0, 1.0)

# Successive shortest paths
solver1 = MinCostMaxFlow(network1)
flow1, cost1 = solver1.successive_shortest_paths(0, 3)

# Cycle canceling
solver2 = MinCostMaxFlow(network2)
flow2, cost2 = solver2.cycle_canceling(0, 3)

print(f"SSP: flow={flow1}, cost={cost1}")
print(f"CC: flow={flow2}, cost={cost2}")
```

## Time Complexity Summary

| Operation | Time Complexity |
|-----------|----------------|
| `add_edge` | O(1) |
| `successive_shortest_paths` | O(V E log V) |
| `cycle_canceling` | O(V^2 E) |
| `get_flow` | O(V + E) |

Where V is the number of vertices and E is the number of edges.

## Notes

- Successive shortest paths uses Dijkstra with potentials for efficiency
- Cycle canceling uses Bellman-Ford and handles negative costs
- Both algorithms find the same optimal solution
- Flow network maintains residual graph for augmenting paths
- Algorithms preserve flow conservation and capacity constraints
