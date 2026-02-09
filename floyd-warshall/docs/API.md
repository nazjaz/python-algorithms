# Floyd-Warshall Algorithm API Documentation

## FloydWarshall Class

Main class for Floyd-Warshall algorithm for all-pairs shortest paths.

### Constructor

```python
FloydWarshall(config_path: str = "config.yaml") -> None
```

Initialize FloydWarshall with configuration.

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
    edges: List[Tuple[int, int, float]]
) -> Tuple[List[List[float]], List[List[Optional[int]]], bool]
```

Find shortest paths between all pairs using Floyd-Warshall.

**Parameters:**
- `num_vertices` (int): Number of vertices
- `edges` (List[Tuple[int, int, float]]): List of edges as (source, destination, weight) tuples

**Returns:**
- `Tuple[List[List[float]], List[List[Optional[int]]], bool]`: Distance matrix, next matrix (for path reconstruction), and negative cycle flag

**Raises:**
- `ValueError`: If inputs are invalid

**Time Complexity:** O(V³) where V is number of vertices

**Space Complexity:** O(V²)

**Example:**
```python
fw = FloydWarshall()
edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3)]
dist, next_matrix, has_negative_cycle = fw.find_shortest_paths(4, edges)
# dist[0][3] = 6.0
# has_negative_cycle = False
```

#### reconstruct_path

```python
reconstruct_path(
    next_matrix: List[List[Optional[int]]],
    start: int,
    end: int
) -> Optional[List[int]]
```

Reconstruct shortest path from start to end.

**Parameters:**
- `next_matrix` (List[List[Optional[int]]]): Next matrix from find_shortest_paths()
- `start` (int): Start vertex
- `end` (int): End vertex

**Returns:**
- `Optional[List[int]]`: List of vertices in path, or None if no path exists

**Example:**
```python
fw = FloydWarshall()
edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3)]
dist, next_matrix, _ = fw.find_shortest_paths(4, edges)
path = fw.reconstruct_path(next_matrix, 0, 3)
# path = [0, 1, 2, 3]
```

#### get_shortest_distance

```python
get_shortest_distance(
    num_vertices: int,
    edges: List[Tuple[int, int, float]],
    start: int,
    end: int
) -> Optional[float]
```

Get shortest distance between two vertices.

**Parameters:**
- `num_vertices` (int): Number of vertices
- `edges` (List[Tuple[int, int, float]]): List of edges
- `start` (int): Start vertex
- `end` (int): End vertex

**Returns:**
- `Optional[float]`: Shortest distance, or None if no path exists or negative cycle

**Example:**
```python
fw = FloydWarshall()
edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3)]
distance = fw.get_shortest_distance(4, edges, 0, 3)
# distance = 6.0
```

#### get_all_distances

```python
get_all_distances(
    num_vertices: int,
    edges: List[Tuple[int, int, float]]
) -> Tuple[List[List[float]], bool]
```

Get all-pairs shortest distances.

**Parameters:**
- `num_vertices` (int): Number of vertices
- `edges` (List[Tuple[int, int, float]]): List of edges

**Returns:**
- `Tuple[List[List[float]], bool]`: Distance matrix and negative cycle flag

**Example:**
```python
fw = FloydWarshall()
edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3)]
dist, has_negative_cycle = fw.get_all_distances(4, edges)
# dist[i][j] = shortest distance from i to j
```

#### compare_performance

```python
compare_performance(
    num_vertices: int,
    edges: List[Tuple[int, int, float]],
    iterations: int = 1
) -> Dict[str, any]
```

Compare performance of Floyd-Warshall algorithm.

**Parameters:**
- `num_vertices` (int): Number of vertices
- `edges` (List[Tuple[int, int, float]]): List of edges
- `iterations` (int): Number of iterations for timing. Default: 1

**Returns:**
- `Dict[str, any]`: Dictionary containing performance data

**Example:**
```python
fw = FloydWarshall()
edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3)]
performance = fw.compare_performance(4, edges, iterations=1000)
print(performance["floyd_warshall"]["time_milliseconds"])
```

#### generate_report

```python
generate_report(
    performance_data: Dict[str, any],
    output_path: Optional[str] = None
) -> str
```

Generate performance report for Floyd-Warshall algorithm.

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
- `-c, --config`: Path to configuration file (default: config.yaml)
- `-q, --query`: Query shortest path from START to END (two integers)
- `-a, --all-pairs`: Display all-pairs shortest distances
- `-p, --path`: Reconstruct path from START to END (two integers)
- `-i, --iterations`: Number of iterations for timing (default: 1)
- `-r, --report`: Output path for performance report

### Examples

```bash
# Find all-pairs shortest paths
python src/main.py -n 4 --edges 0-1-1 1-2-2 2-3-3 --all-pairs

# Query specific path
python src/main.py -n 4 --edges 0-1-1 1-2-2 --query 0 2

# Reconstruct path
python src/main.py -n 4 --edges 0-1-1 1-2-2 --path 0 2

# Generate report
python src/main.py -n 10 --edges 0-1-5 1-2-3 --report report.txt
```

## Error Handling

All methods validate inputs and raise appropriate exceptions:

- `ValueError`: Invalid input parameters (negative num_vertices)
- `FileNotFoundError`: Configuration file not found
- `yaml.YAMLError`: Invalid YAML in configuration file
- `IOError`: File I/O errors when saving reports
- `PermissionError`: Insufficient permissions for file operations

## Algorithm Complexity

### Floyd-Warshall Algorithm

- **Time Complexity**: O(V³) where V is number of vertices
- **Space Complexity**: O(V²) for distance and next matrices
- **Optimal**: For all-pairs shortest paths in dense graphs
- **Works with**: Weighted directed graphs
- **Handles**: Negative edge weights (but not negative cycles)

## Notes

- Floyd-Warshall finds shortest paths between all pairs of vertices
- Algorithm works with negative edge weights
- Negative cycles are detected and reported
- Path reconstruction uses next matrix
- Distance matrix initialized with infinity for no path
- Diagonal elements are 0 (distance from vertex to itself)
- Algorithm is optimal for all-pairs queries in dense graphs
- More efficient than running single-source algorithms V times
- Can handle disconnected graphs (infinity for unreachable vertices)
- Self-loops are handled correctly
- Multiple edges between same pair use minimum weight
