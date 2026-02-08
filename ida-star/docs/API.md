# IDA* Pathfinding API Documentation

## Classes

### IDAStar

Main class for running Iterative Deepening A* pathfinding algorithm.

#### Methods

##### `__init__(config_path: str = "config.yaml")`

Initialize IDA* algorithm with configuration.

**Parameters:**
- `config_path` (str): Path to configuration YAML file. Default: "config.yaml"

**Raises:**
- `FileNotFoundError`: If config file doesn't exist
- `yaml.YAMLError`: If config file is invalid YAML

**Example:**
```python
ida = IDAStar(config_path="config.yaml")
```

##### `search(graph, start, goal)`

Run IDA* search algorithm.

**Parameters:**
- `graph` (GridGraph): GridGraph instance
- `start` (Tuple[int, int]): Start node coordinates (x, y)
- `goal` (Tuple[int, int]): Goal node coordinates (x, y)

**Returns:**
Dictionary containing:
- `path` (List[Tuple[int, int]]): List of nodes from start to goal
- `cost` (float): Total path cost
- `iterations` (int): Number of iterations performed
- `nodes_explored` (int): Total nodes explored across iterations
- `path_length` (int): Number of nodes in path
- `found` (bool): Whether path was found

**Raises:**
- `ValueError`: If start or goal nodes are invalid

**Example:**
```python
result = ida.search(graph, (0, 0), (9, 9))
if result['found']:
    print(f"Path: {result['path']}")
    print(f"Iterations: {result['iterations']}")
```

### GridGraph

Represents a grid-based graph for pathfinding.

#### Methods

##### `__init__(grid, allow_diagonal=True, movement_cost=None)`

Initialize grid graph.

**Parameters:**
- `grid` (np.ndarray): 2D numpy array where 0 = walkable, 1 = obstacle
- `allow_diagonal` (bool): Whether diagonal movement is allowed
- `movement_cost` (Optional[Dict[str, float]]): Dictionary with 'straight' and 'diagonal' costs

**Example:**
```python
grid = np.zeros((10, 10))
graph = GridGraph(grid, allow_diagonal=True)
```

##### `is_valid(node)`

Check if node is valid and walkable.

**Parameters:**
- `node` (Tuple[int, int]): Node coordinates (x, y)

**Returns:**
- `bool`: True if node is valid and walkable

##### `get_neighbors(node)`

Get neighboring nodes with movement costs.

**Parameters:**
- `node` (Tuple[int, int]): Current node coordinates (x, y)

**Returns:**
- `List[Tuple[Tuple[int, int], float]]`: List of tuples (neighbor, cost)

### Heuristic

Implements various heuristic functions for IDA* algorithm.

#### Static Methods

##### `manhattan_distance(node1, node2)`

Calculate Manhattan distance (L1 norm).

**Parameters:**
- `node1` (Tuple[int, int]): First node coordinates (x, y)
- `node2` (Tuple[int, int]): Second node coordinates (x, y)

**Returns:**
- `float`: Manhattan distance between nodes

##### `euclidean_distance(node1, node2)`

Calculate Euclidean distance (L2 norm).

**Parameters:**
- `node1` (Tuple[int, int]): First node coordinates (x, y)
- `node2` (Tuple[int, int]): Second node coordinates (x, y)

**Returns:**
- `float`: Euclidean distance between nodes

##### `chebyshev_distance(node1, node2)`

Calculate Chebyshev distance (L∞ norm).

**Parameters:**
- `node1` (Tuple[int, int]): First node coordinates (x, y)
- `node2` (Tuple[int, int]): Second node coordinates (x, y)

**Returns:**
- `float`: Chebyshev distance between nodes

##### `diagonal_distance(node1, node2)`

Calculate diagonal distance (octile distance).

**Parameters:**
- `node1` (Tuple[int, int]): First node coordinates (x, y)
- `node2` (Tuple[int, int]): Second node coordinates (x, y)

**Returns:**
- `float`: Diagonal distance between nodes

##### `octile_distance(node1, node2)`

Calculate octile distance (8-directional movement).

**Parameters:**
- `node1` (Tuple[int, int]): First node coordinates (x, y)
- `node2` (Tuple[int, int]): Second node coordinates (x, y)

**Returns:**
- `float`: Octile distance between nodes

##### `zero_heuristic(node1, node2)`

Zero heuristic (equivalent to iterative deepening DFS).

**Parameters:**
- `node1` (Tuple[int, int]): First node coordinates (x, y)
- `node2` (Tuple[int, int]): Second node coordinates (x, y)

**Returns:**
- `float`: Always returns 0

##### `get_heuristic(heuristic_name)`

Get heuristic function by name.

**Parameters:**
- `heuristic_name` (str): Name of heuristic

**Returns:**
- `Callable`: Heuristic function

**Raises:**
- `ValueError`: If heuristic name is unknown

## Configuration

### Configuration File Format

The algorithm uses YAML configuration files with the following structure:

```yaml
ida_star:
  heuristic: "manhattan"
  allow_diagonal: true
  max_iterations: 1000
  movement_cost:
    straight: 1.0
    diagonal: 1.414

logging:
  level: "INFO"
  file: "logs/app.log"
```

### Configuration Parameters

- `heuristic` (str): One of "manhattan", "euclidean", "chebyshev", "diagonal", "octile", "zero"
- `allow_diagonal` (bool): Whether diagonal movement is allowed
- `max_iterations` (int): Maximum number of iterations (f-limit increases)
- `movement_cost` (dict): Dictionary with "straight" and "diagonal" costs

## Examples

### Basic Pathfinding

```python
from src.main import IDAStar, GridGraph
import numpy as np

grid = np.zeros((10, 10))
graph = GridGraph(grid, allow_diagonal=True)
ida = IDAStar()

result = ida.search(graph, (0, 0), (9, 9))
print(f"Path found: {result['found']}")
print(f"Path: {result['path']}")
print(f"Iterations: {result['iterations']}")
```

### Custom Configuration

```python
ida = IDAStar(config_path="custom_config.yaml")
result = ida.search(graph, start, goal)
```

### Using Different Heuristics

```python
config = {
    'ida_star': {'heuristic': 'euclidean', 'max_iterations': 500},
    'logging': {'level': 'WARNING', 'file': 'logs/test.log'}
}
# Save config and use...
```
