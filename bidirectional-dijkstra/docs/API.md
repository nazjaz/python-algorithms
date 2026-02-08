# Bidirectional Dijkstra API Documentation

## Classes

### BidirectionalDijkstra

Main class for running bidirectional Dijkstra shortest path algorithm.

#### Methods

##### `__init__(config_path: str = "config.yaml")`

Initialize BidirectionalDijkstra with configuration.

**Parameters:**
- `config_path` (str): Path to configuration YAML file. Default: "config.yaml"

**Raises:**
- `FileNotFoundError`: If config file doesn't exist
- `yaml.YAMLError`: If config file is invalid YAML

**Example:**
```python
dijkstra = BidirectionalDijkstra(config_path="config.yaml")
```

##### `search(graph, start, goal)`

Run bidirectional Dijkstra search algorithm.

**Parameters:**
- `graph` (Graph): Graph instance
- `start`: Start node
- `goal`: Goal node

**Returns:**
Dictionary containing:
- `path` (List): List of nodes from start to goal
- `cost` (float): Total path cost
- `nodes_explored_forward` (int): Nodes explored in forward search
- `nodes_explored_backward` (int): Nodes explored in backward search
- `nodes_explored` (int): Total nodes explored
- `path_length` (int): Number of nodes in path
- `found` (bool): Whether path was found
- `meeting_node`: Node where searches met

**Raises:**
- `ValueError`: If start or goal nodes are invalid

**Example:**
```python
result = dijkstra.search(graph, start, goal)
if result['found']:
    print(f"Path: {result['path']}")
    print(f"Cost: {result['cost']}")
```

### Graph

Represents a weighted graph for pathfinding.

#### Methods

##### `__init__(adjacency_list=None, grid=None, allow_diagonal=True, movement_cost=None)`

Initialize graph from adjacency list or grid.

**Parameters:**
- `adjacency_list` (Optional[Dict]): Dictionary mapping nodes to list of (neighbor, weight)
- `grid` (Optional[np.ndarray]): 2D numpy array where 0 = walkable, 1 = obstacle
- `allow_diagonal` (bool): Whether diagonal movement is allowed (for grid)
- `movement_cost` (Optional[Dict]): Dictionary with 'straight' and 'diagonal' costs (for grid)

**Raises:**
- `ValueError`: If neither adjacency_list nor grid is provided

**Example:**
```python
# From adjacency list
graph = Graph(adjacency_list={0: [(1, 1.0)], 1: []})

# From grid
grid = np.zeros((10, 10))
graph = Graph(grid=grid, allow_diagonal=True)
```

##### `get_neighbors(node)`

Get neighboring nodes with edge weights.

**Parameters:**
- `node`: Current node

**Returns:**
- `List[Tuple]`: List of tuples (neighbor, weight)

## Configuration

### Configuration File Format

The algorithm uses YAML configuration files with the following structure:

```yaml
bidirectional_dijkstra:
  max_iterations: 10000

logging:
  level: "INFO"
  file: "logs/app.log"
```

### Configuration Parameters

- `max_iterations` (int): Maximum number of iterations (default: 10000)

## Examples

### Basic Pathfinding with Grid

```python
from src.main import BidirectionalDijkstra, Graph
import numpy as np

grid = np.zeros((10, 10))
graph = Graph(grid=grid, allow_diagonal=True)
dijkstra = BidirectionalDijkstra()

result = dijkstra.search(graph, (0, 0), (9, 9))
print(f"Path found: {result['found']}")
print(f"Path: {result['path']}")
```

### Pathfinding with Adjacency List

```python
from src.main import BidirectionalDijkstra, Graph

adjacency_list = {
    0: [(1, 1.0), (2, 2.0)],
    1: [(2, 1.0)],
    2: []
}

graph = Graph(adjacency_list=adjacency_list)
dijkstra = BidirectionalDijkstra()

result = dijkstra.search(graph, 0, 2)
print(f"Path: {result['path']}")
print(f"Cost: {result['cost']}")
```

### Custom Configuration

```python
dijkstra = BidirectionalDijkstra(config_path="custom_config.yaml")
result = dijkstra.search(graph, start, goal)
```
