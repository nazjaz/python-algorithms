# Topological Sort API Documentation

## TopologicalSort Class

Main class for performing topological sort on directed acyclic graphs (DAGs) with cycle detection.

### Constructor

```python
TopologicalSort(config_path: str = "config.yaml") -> None
```

Initialize the solver with configuration.

**Parameters:**
- `config_path` (str): Path to configuration YAML file. Default: "config.yaml"

**Raises:**
- `FileNotFoundError`: If config file doesn't exist
- `yaml.YAMLError`: If config file is invalid YAML

### Methods

#### sort_kahn

```python
sort_kahn(
    edges: List[Tuple[int, int]],
    num_vertices: Optional[int] = None
) -> Tuple[Optional[List[int]], bool]
```

Perform topological sort using Kahn's algorithm (BFS-based).

Kahn's algorithm works by repeatedly removing vertices with in-degree 0. If all vertices are processed, the graph is a DAG. If not, a cycle exists.

**Parameters:**
- `edges` (List[Tuple[int, int]]): List of (source, destination) tuples representing edges
- `num_vertices` (Optional[int]): Number of vertices. If None, inferred from edges

**Returns:**
- `Tuple[Optional[List[int]], bool]`: Topological order (list of vertices) if DAG, None if cycle detected, and boolean indicating if cycle was detected

**Raises:**
- `ValueError`: If inputs are invalid (negative vertices, num_vertices too small)

**Example:**
```python
solver = TopologicalSort()
edges = [(0, 1), (1, 2), (2, 3)]
order, has_cycle = solver.sort_kahn(edges)
# order = [0, 1, 2, 3]
# has_cycle = False
```

#### sort_dfs

```python
sort_dfs(
    edges: List[Tuple[int, int]],
    num_vertices: Optional[int] = None
) -> Tuple[Optional[List[int]], bool]
```

Perform topological sort using DFS-based algorithm.

DFS-based algorithm uses depth-first search with recursion stack to detect cycles. Topological order is built by adding vertices after all their descendants are processed.

**Parameters:**
- `edges` (List[Tuple[int, int]]): List of (source, destination) tuples representing edges
- `num_vertices` (Optional[int]): Number of vertices. If None, inferred from edges

**Returns:**
- `Tuple[Optional[List[int]], bool]`: Topological order (list of vertices) if DAG, None if cycle detected, and boolean indicating if cycle was detected

**Raises:**
- `ValueError`: If inputs are invalid (negative vertices, num_vertices too small)

**Example:**
```python
solver = TopologicalSort()
edges = [(0, 1), (1, 2), (2, 3)]
order, has_cycle = solver.sort_dfs(edges)
# order = [0, 1, 2, 3] (or valid topological order)
# has_cycle = False
```

#### detect_cycle

```python
detect_cycle(
    edges: List[Tuple[int, int]],
    num_vertices: Optional[int] = None
) -> Tuple[bool, Optional[List[int]]]
```

Detect cycles in directed graph.

Uses DFS-based approach to detect cycles. If cycle found, attempts to return cycle path.

**Parameters:**
- `edges` (List[Tuple[int, int]]): List of (source, destination) tuples representing edges
- `num_vertices` (Optional[int]): Number of vertices. If None, inferred from edges

**Returns:**
- `Tuple[bool, Optional[List[int]]]`: Boolean indicating if cycle exists and cycle path if cycle found, None otherwise

**Example:**
```python
solver = TopologicalSort()
edges = [(0, 1), (1, 2), (2, 0)]
has_cycle, cycle_path = solver.detect_cycle(edges)
# has_cycle = True
# cycle_path = [0, 1, 2, 0] (or similar cycle path)
```

#### compare_approaches

```python
compare_approaches(
    edges: List[Tuple[int, int]],
    num_vertices: Optional[int] = None,
    iterations: int = 1
) -> Dict[str, any]
```

Compare Kahn's and DFS-based topological sort approaches.

**Parameters:**
- `edges` (List[Tuple[int, int]]): List of (source, destination) tuples representing edges
- `num_vertices` (Optional[int]): Number of vertices. If None, inferred from edges
- `iterations` (int): Number of iterations for timing. Default: 1

**Returns:**
- `Dict[str, any]`: Dictionary containing comparison data with keys:
  - `num_vertices`: Number of vertices
  - `num_edges`: Number of edges
  - `iterations`: Number of iterations
  - `kahn`: Dictionary with solution details (order, has_cycle, time, success)
  - `dfs`: Dictionary with solution details (order, has_cycle, time, success)
  - `cycle_detection`: Dictionary with cycle detection results
  - `fastest`: Fastest method name (if both successful and no cycles)
  - `fastest_time`: Time of fastest method

**Example:**
```python
solver = TopologicalSort()
edges = [(0, 1), (1, 2), (2, 3)]
results = solver.compare_approaches(edges)
print(results["kahn"]["order"])
print(results["dfs"]["order"])
```

#### generate_report

```python
generate_report(
    comparison_data: Dict[str, any],
    output_path: Optional[str] = None
) -> str
```

Generate comparison report for topological sort solutions.

**Parameters:**
- `comparison_data` (Dict[str, any]): Comparison data from `compare_approaches()`
- `output_path` (Optional[str]): Optional path to save report file

**Returns:**
- `str`: Report content as string

**Raises:**
- `IOError`: If file cannot be written
- `PermissionError`: If file is not writable

**Example:**
```python
solver = TopologicalSort()
edges = [(0, 1), (1, 2), (2, 3)]
results = solver.compare_approaches(edges)
report = solver.generate_report(results, output_path="report.txt")
```

### Private Methods

#### _build_graph

```python
_build_graph(
    edges: List[Tuple[int, int]],
    num_vertices: Optional[int] = None
) -> Tuple[Dict[int, List[int]], List[int]]
```

Build adjacency list representation of graph.

**Returns:**
- `Tuple[Dict[int, List[int]], List[int]]`: Adjacency list dictionary and list of all vertices

**Raises:**
- `ValueError`: If edges are invalid

#### _calculate_in_degrees

```python
_calculate_in_degrees(
    adjacency_list: Dict[int, List[int]],
    vertices: List[int]
) -> Dict[int, int]
```

Calculate in-degree for each vertex.

**Returns:**
- `Dict[int, int]`: Dictionary mapping vertex to its in-degree

## Command-Line Interface

The module can be run as a script with the following interface:

```bash
python src/main.py [OPTIONS]
```

### Options

- `-e, --edges`: Edges as 'source-dest' pairs (e.g., '0-1 1-2')
- `-n, --num-vertices`: Number of vertices (if not specified, inferred from edges)
- `-c, --config`: Path to configuration file (default: config.yaml)
- `-m, --method`: Solution method - kahn, dfs, compare, or cycle (default: compare)
- `-i, --iterations`: Number of iterations for timing (default: 1)
- `-r, --report`: Output path for performance report

### Examples

```bash
# Compare both approaches
python src/main.py --edges 0-1 1-2 2-3 --num-vertices 4

# Use Kahn's algorithm only
python src/main.py --edges 0-1 1-2 2-3 --num-vertices 4 --method kahn

# Use DFS algorithm only
python src/main.py --edges 0-1 1-2 2-3 --num-vertices 4 --method dfs

# Detect cycles
python src/main.py --edges 0-1 1-2 2-0 --method cycle

# Generate report
python src/main.py --edges 0-1 1-2 2-3 --num-vertices 4 --report report.txt
```

## Error Handling

All methods validate inputs and raise appropriate exceptions:

- `ValueError`: Invalid input parameters (empty edges without num_vertices, negative vertices, num_vertices too small)
- `FileNotFoundError`: Configuration file not found
- `yaml.YAMLError`: Invalid YAML in configuration file
- `IOError`: File I/O errors when saving reports
- `PermissionError`: Insufficient permissions for file operations

## Algorithm Complexity

### Kahn's Algorithm

- **Time Complexity**: O(V + E) where V = number of vertices, E = number of edges
- **Space Complexity**: O(V) for queue and in-degree storage
- **Approach**: BFS-based, processes vertices with in-degree 0

### DFS-based Algorithm

- **Time Complexity**: O(V + E) where V = number of vertices, E = number of edges
- **Space Complexity**: O(V) for recursion stack and visited set
- **Approach**: DFS-based, processes vertices in depth-first order

### Cycle Detection

- **Time Complexity**: O(V + E) where V = number of vertices, E = number of edges
- **Space Complexity**: O(V) for recursion stack and visited set
- **Approach**: DFS with recursion stack to detect back edges

## Notes

- Topological sort only works on directed acyclic graphs (DAGs)
- If a cycle is detected, topological sort cannot be performed
- Both Kahn's and DFS algorithms produce valid topological orders, but orders may differ
- Kahn's algorithm processes vertices level by level (BFS-style)
- DFS algorithm processes vertices in depth-first order
- Cycle detection can identify and return cycle paths
- Both algorithms handle isolated vertices correctly
- Empty graphs and single-vertex graphs are handled as edge cases
