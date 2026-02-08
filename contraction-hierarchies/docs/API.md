# Contraction Hierarchies API Documentation

## Classes

### ContractionHierarchies

Main class for preprocessing and querying road networks using Contraction Hierarchies.

#### Methods

##### `__init__(config_path: str = "config.yaml")`

Initialize ContractionHierarchies with configuration.

**Parameters:**
- `config_path` (str): Path to configuration YAML file. Default: "config.yaml"

**Raises:**
- `FileNotFoundError`: If config file doesn't exist
- `yaml.YAMLError`: If config file is invalid YAML

**Example:**
```python
ch = ContractionHierarchies(config_path="config.yaml")
```

##### `preprocess(graph: RoadGraph) -> Dict[str, any]`

Preprocess graph using contraction hierarchies.

**Parameters:**
- `graph` (RoadGraph): Road graph to preprocess

**Returns:**
Dictionary containing:
- `nodes_contracted` (int): Number of nodes contracted
- `shortcuts_added` (int): Number of shortcuts added
- `total_edges` (int): Total edges after preprocessing

**Example:**
```python
stats = ch.preprocess(graph)
print(f"Shortcuts added: {stats['shortcuts_added']}")
```

##### `query(graph: RoadGraph, start: int, goal: int) -> Dict[str, any]`

Query shortest path using preprocessed contraction hierarchies.

**Parameters:**
- `graph` (RoadGraph): Preprocessed road graph
- `start` (int): Start node ID
- `goal` (int): Goal node ID

**Returns:**
Dictionary containing:
- `path` (List[int]): List of nodes from start to goal
- `cost` (float): Total path cost
- `nodes_explored` (int): Nodes explored during query
- `path_length` (int): Number of nodes in path
- `found` (bool): Whether path was found

**Raises:**
- `ValueError`: If graph not preprocessed or nodes invalid

**Example:**
```python
result = ch.query(graph, 0, 10)
if result['found']:
    print(f"Path: {result['path']}")
    print(f"Cost: {result['cost']}")
```

### RoadGraph

Represents a road network graph.

#### Methods

##### `__init__(edges: Optional[List[Tuple[int, int, float]]] = None, num_nodes: Optional[int] = None)`

Initialize road graph.

**Parameters:**
- `edges` (Optional[List[Tuple[int, int, float]]]): List of (source, target, weight) tuples
- `num_nodes` (Optional[int]): Number of nodes (if None, inferred from edges)

**Example:**
```python
edges = [(0, 1, 1.0), (1, 2, 2.0)]
graph = RoadGraph(edges=edges, num_nodes=3)
```

##### `get_outgoing(node: int) -> List[Tuple[int, float]]`

Get outgoing edges from node.

**Parameters:**
- `node` (int): Node ID

**Returns:**
- `List[Tuple[int, float]]`: List of (target, weight) tuples

##### `get_incoming(node: int) -> List[Tuple[int, float]]`

Get incoming edges to node.

**Parameters:**
- `node` (int): Node ID

**Returns:**
- `List[Tuple[int, float]]`: List of (source, weight) tuples

##### `add_edge(source: int, target: int, weight: float) -> None`

Add edge to graph.

**Parameters:**
- `source` (int): Source node
- `target` (int): Target node
- `weight` (float): Edge weight

## Configuration

### Configuration File Format

The algorithm uses YAML configuration files with the following structure:

```yaml
contraction_hierarchies:
  edge_difference_weight: 1.0
  deleted_neighbors_weight: 1.0
  hop_limit: 2

logging:
  level: "INFO"
  file: "logs/app.log"
```

### Configuration Parameters

- `edge_difference_weight` (float): Weight for edge difference in importance calculation
- `deleted_neighbors_weight` (float): Weight for deleted neighbors in importance calculation
- `hop_limit` (int): Hop limit for shortcut search (not used in simplified version)

## Examples

### Basic Usage

```python
from src.main import ContractionHierarchies, RoadGraph

# Create graph
edges = [(0, 1, 1.0), (1, 2, 2.0), (2, 3, 1.0)]
graph = RoadGraph(edges=edges, num_nodes=4)

# Preprocess
ch = ContractionHierarchies()
stats = ch.preprocess(graph)

# Query
result = ch.query(graph, 0, 3)
print(f"Path: {result['path']}")
print(f"Cost: {result['cost']}")
```

### Custom Configuration

```python
ch = ContractionHierarchies(config_path="custom_config.yaml")
stats = ch.preprocess(graph)
result = ch.query(graph, start, goal)
```

### Multiple Queries

```python
# Preprocess once
ch = ContractionHierarchies()
ch.preprocess(graph)

# Fast queries
for start, goal in queries:
    result = ch.query(graph, start, goal)
    print(f"{start}->{goal}: {result['cost']}")
```
