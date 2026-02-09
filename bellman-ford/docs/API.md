# Bellman-Ford Algorithm API Documentation

## BellmanFord Class

Main class for Bellman-Ford algorithm for shortest paths with negative cycle detection.

### Constructor

```python
BellmanFord(config_path: str = "config.yaml") -> None
```

Initialize BellmanFord with configuration.

**Parameters:**
- `config_path` (str): Path to configuration YAML file. Default: "config.yaml"

**Raises:**
- `FileNotFoundError`: If config file doesn't exist
- `yaml.YAMLError`: If config file is invalid YAML

### Methods

#### find_shortest_paths

```python
find_shortest_paths(
    num_vertices: int,
    edges: List[Tuple[int, int, float]],
    source: int
) -> Tuple[List[float], List[Optional[int]], bool]
```

Find shortest paths from source using Bellman-Ford algorithm.

**Parameters:**
- `num_vertices` (int): Number of vertices
- `edges` (List[Tuple[int, int, float]]): List of edges as (source, destination, weight) tuples
- `source` (int): Source vertex

**Returns:**
- `Tuple[List[float], List[Optional[int]], bool]`: Distance array, parent array (for path reconstruction), and negative cycle flag

**Raises:**
- `ValueError`: If inputs are invalid

**Time Complexity:** O(V*E) where V=vertices, E=edges

**Space Complexity:** O(V)

**Example:**
```python
bf = BellmanFord()
edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3)]
dist, parent, has_negative_cycle = bf.find_shortest_paths(4, edges, 0)
# dist[3] = 6.0
# has_negative_cycle = False
```

#### find_negative_cycle

```python
find_negative_cycle(
    num_vertices: int,
    edges: List[Tuple[int, int, float]],
    source: int
) -> Optional[List[int]]
```

Find negative cycle in graph.

**Parameters:**
- `num_vertices` (int): Number of vertices
- `edges` (List[Tuple[int, int, float]]): List of edges
- `source` (int): Source vertex

**Returns:**
- `Optional[List[int]]`: List of vertices in negative cycle, or None if no cycle exists

**Example:**
```python
bf = BellmanFord()
edges = [(0, 1, 1), (1, 2, -2), (2, 0, -1)]
cycle = bf.find_negative_cycle(3, edges, 0)
# cycle = [0, 1, 2, 0] or similar
```

#### reconstruct_path

```python
reconstruct_path(
    parent: List[Optional[int]],
    start: int,
    end: int
) -> Optional[List[int]]
```

Reconstruct shortest path from start to end.

**Parameters:**
- `parent` (List[Optional[int]]): Parent array from find_shortest_paths()
- `start` (int): Start vertex
- `end` (int): End vertex

**Returns:**
- `Optional[List[int]]`: List of vertices in path, or None if no path exists

**Example:**
```python
bf = BellmanFord()
edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3)]
dist, parent, _ = bf.find_shortest_paths(4, edges, 0)
path = bf.reconstruct_path(parent, 0, 3)
# path = [0, 1, 2, 3]
```

#### get_shortest_distance

```python
get_shortest_distance(
    num_vertices: int,
    edges: List[Tuple[int, int, float]],
    source: int,
    target: int
) -> Optional[float]
```

Get shortest distance from source to target.

**Parameters:**
- `num_vertices` (int): Number of vertices
- `edges` (List[Tuple[int, int, float]]): List of edges
- `source` (int): Source vertex
- `target` (int): Target vertex

**Returns:**
- `Optional[float]`: Shortest distance, or None if no path exists or negative cycle

**Example:**
```python
bf = BellmanFord()
edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3)]
distance = bf.get_shortest_distance(4, edges, 0, 3)
# distance = 6.0
```

#### get_all_distances

```python
get_all_distances(
    num_vertices: int,
    edges: List[Tuple[int, int, float]],
    source: int
) -> Tuple[List[float], bool]
```

Get all shortest distances from source.

**Parameters:**
- `num_vertices` (int): Number of vertices
- `edges` (List[Tuple[int, int, float]]): List of edges
- `source` (int): Source vertex

**Returns:**
- `Tuple[List[float], bool]`: Distance array and negative cycle flag

**Example:**
```python
bf = BellmanFord()
edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3)]
dist, has_negative_cycle = bf.get_all_distances(4, edges, 0)
# dist[i] = shortest distance from 0 to i
```

#### compare_performance

```python
compare_performance(
    num_vertices: int,
    edges: List[Tuple[int, int, float]],
    source: int,
    iterations: int = 1
) -> Dict[str, any]
```

Compare performance of Bellman-Ford algorithm.

**Parameters:**
- `num_vertices` (int): Number of vertices
- `edges` (List[Tuple[int, int, float]]): List of edges
- `source` (int): Source vertex
- `iterations` (int): Number of iterations for timing. Default: 1

**Returns:**
- `Dict[str, any]`: Dictionary containing performance data

**Example:**
```python
bf = BellmanFord()
edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3)]
performance = bf.compare_performance(4, edges, 0, iterations=1000)
print(performance["bellman_ford"]["time_milliseconds"])
```

#### generate_report

```python
generate_report(
    performance_data: Dict[str, any],
    output_path: Optional[str] = None
) -> str
```

Generate performance report for Bellman-Ford algorithm.

**Parameters:**
- `performance_data` (Dict[str, any]): Performance data from compare_performance()
- `output_path` (Optional[str]): Optional path to save report file

**Returns:**
- `str`: Report content as string

**Raises:**
- `IOError`: If file cannot be written
- `PermissionError`: If file is not writable

## Command-Line Interface

The module can be run as a script with the following interface:

```bash
python src/main.py -n NUM_VERTICES [OPTIONS]
```

### Arguments

- `-n, --num-vertices`: (Required) Number of vertices

### Options

- `-e, --edges`: Edges as 'source-dest-weight' (e.g., '0-1-5 1-2-3')
- `-s, --source`: Source vertex (default: 0)
- `-c, --config`: Path to configuration file (default: config.yaml)
- `-q, --query`: Query shortest distance to target vertex
- `-a, --all-distances`: Display all distances from source
- `-p, --path`: Reconstruct path to target vertex
- `-cy, --cycle`: Find negative cycle
- `-i, --iterations`: Number of iterations for timing (default: 1)
- `-r, --report`: Output path for performance report

### Examples

```bash
# Find shortest paths
python src/main.py -n 4 --edges 0-1-1 1-2-2 2-3-3 --source 0

# Query specific distance
python src/main.py -n 4 --edges 0-1-1 1-2-2 --source 0 --query 2

# Reconstruct path
python src/main.py -n 4 --edges 0-1-1 1-2-2 --source 0 --path 2

# Find negative cycle
python src/main.py -n 3 --edges 0-1-1 1-2--2 2-0--1 --source 0 --cycle

# Generate report
python src/main.py -n 10 --edges 0-1-5 1-2-3 --source 0 --report report.txt
```

## Error Handling

All methods validate inputs and raise appropriate exceptions:

- `ValueError`: Invalid input parameters (negative num_vertices, invalid source vertex)
- `FileNotFoundError`: Configuration file not found
- `yaml.YAMLError`: Invalid YAML in configuration file
- `IOError`: File I/O errors when saving reports
- `PermissionError`: Insufficient permissions for file operations

## Algorithm Complexity

### Bellman-Ford Algorithm

- **Time Complexity**: O(V*E) where V is vertices, E is edges
- **Space Complexity**: O(V) for distance and parent arrays
- **Optimal**: For single-source shortest paths with negative edges
- **Works with**: Weighted directed graphs
- **Handles**: Negative edge weights and negative cycles

## Notes

- Bellman-Ford finds shortest paths from single source vertex
- Algorithm works with negative edge weights
- Negative cycles are detected and can be found
- Path reconstruction uses parent array
- Distance array initialized with infinity for unreachable vertices
- Source distance is always 0
- Algorithm relaxes edges V-1 times
- Additional check detects negative cycles
- More flexible than Dijkstra's algorithm (handles negative edges)
- Can handle disconnected graphs (infinity for unreachable vertices)
- Self-loops are handled correctly
- Multiple edges between same pair use minimum weight
