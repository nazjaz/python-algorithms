# Strongly Connected Components API Documentation

## StronglyConnectedComponents Class

Main class for finding strongly connected components (SCCs) in directed graphs using Kosaraju's algorithm.

### Constructor

```python
StronglyConnectedComponents(config_path: str = "config.yaml") -> None
```

Initialize the SCC finder with configuration.

**Parameters:**
- `config_path` (str): Path to configuration YAML file. Default: "config.yaml"

**Raises:**
- `FileNotFoundError`: If config file doesn't exist
- `yaml.YAMLError`: If config file is invalid YAML

### Methods

#### find_sccs

```python
find_sccs(
    edges: List[Tuple[int, int]],
    num_vertices: Optional[int] = None
) -> List[List[int]]
```

Find strongly connected components using Kosaraju's algorithm.

Kosaraju's algorithm works in two passes:
1. First DFS pass: Fill stack with vertices in order of finishing times
2. Second DFS pass: Process vertices from stack on transpose graph to find SCCs

**Parameters:**
- `edges` (List[Tuple[int, int]]): List of (source, destination) tuples representing edges
- `num_vertices` (Optional[int]): Number of vertices. If None, inferred from edges

**Returns:**
- `List[List[int]]`: List of SCCs, where each SCC is a list of vertex indices

**Raises:**
- `ValueError`: If inputs are invalid (negative vertices, num_vertices too small)

**Example:**
```python
scc_finder = StronglyConnectedComponents()
edges = [(0, 1), (1, 2), (2, 0)]
sccs = scc_finder.find_sccs(edges)
# sccs = [[0, 1, 2]]
```

#### get_scc_count

```python
get_scc_count(
    edges: List[Tuple[int, int]],
    num_vertices: Optional[int] = None
) -> int
```

Get count of strongly connected components.

**Parameters:**
- `edges` (List[Tuple[int, int]]): List of (source, destination) tuples representing edges
- `num_vertices` (Optional[int]): Number of vertices. If None, inferred from edges

**Returns:**
- `int`: Number of strongly connected components

**Example:**
```python
scc_finder = StronglyConnectedComponents()
edges = [(0, 1), (1, 0), (2, 3), (3, 2)]
count = scc_finder.get_scc_count(edges)
# count = 2
```

#### get_largest_scc

```python
get_largest_scc(
    edges: List[Tuple[int, int]],
    num_vertices: Optional[int] = None
) -> Optional[List[int]]
```

Get the largest strongly connected component.

**Parameters:**
- `edges` (List[Tuple[int, int]]): List of (source, destination) tuples representing edges
- `num_vertices` (Optional[int]): Number of vertices. If None, inferred from edges

**Returns:**
- `Optional[List[int]]`: Largest SCC as list of vertices, or None if graph is empty

**Example:**
```python
scc_finder = StronglyConnectedComponents()
edges = [(0, 1), (1, 0), (2, 3), (3, 2), (4, 5), (5, 4)]
largest = scc_finder.get_largest_scc(edges)
# largest = [0, 1] or [2, 3] or [4, 5] (any of the size-2 SCCs)
```

#### get_scc_statistics

```python
get_scc_statistics(
    edges: List[Tuple[int, int]],
    num_vertices: Optional[int] = None
) -> Dict[str, any]
```

Get statistics about strongly connected components.

**Parameters:**
- `edges` (List[Tuple[int, int]]): List of (source, destination) tuples representing edges
- `num_vertices` (Optional[int]): Number of vertices. If None, inferred from edges

**Returns:**
- `Dict[str, any]`: Dictionary containing SCC statistics:
    - `count`: Total number of SCCs
    - `sizes`: List of SCC sizes
    - `largest_size`: Size of largest SCC
    - `smallest_size`: Size of smallest SCC
    - `average_size`: Average SCC size

**Example:**
```python
scc_finder = StronglyConnectedComponents()
edges = [(0, 1), (1, 0), (2, 3), (3, 2), (4,)]
stats = scc_finder.get_scc_statistics(edges, num_vertices=5)
# stats = {
#     "count": 3,
#     "sizes": [2, 2, 1],
#     "largest_size": 2,
#     "smallest_size": 1,
#     "average_size": 1.67
# }
```

#### compare_performance

```python
compare_performance(
    edges: List[Tuple[int, int]],
    num_vertices: Optional[int] = None,
    iterations: int = 1
) -> Dict[str, any]
```

Compare performance of SCC finding operations.

**Parameters:**
- `edges` (List[Tuple[int, int]]): List of (source, destination) tuples representing edges
- `num_vertices` (Optional[int]): Number of vertices. If None, inferred from edges
- `iterations` (int): Number of iterations for timing. Default: 1

**Returns:**
- `Dict[str, any]`: Dictionary containing performance data for:
    - `find_sccs`: Complete SCC finding operation
    - `get_scc_count`: SCC count operation
    - `get_largest_scc`: Largest SCC finding operation
    - `get_scc_statistics`: Statistics calculation operation

**Example:**
```python
scc_finder = StronglyConnectedComponents()
edges = [(0, 1), (1, 2), (2, 0)]
performance = scc_finder.compare_performance(edges)
print(performance["find_sccs"]["time_milliseconds"])
```

#### generate_report

```python
generate_report(
    performance_data: Dict[str, any],
    output_path: Optional[str] = None
) -> str
```

Generate performance report for SCC operations.

**Parameters:**
- `performance_data` (Dict[str, any]): Performance data from `compare_performance()`
- `output_path` (Optional[str]): Optional path to save report file

**Returns:**
- `str`: Report content as string

**Raises:**
- `IOError`: If file cannot be written
- `PermissionError`: If file is not writable

**Example:**
```python
scc_finder = StronglyConnectedComponents()
edges = [(0, 1), (1, 2), (2, 0)]
performance = scc_finder.compare_performance(edges)
report = scc_finder.generate_report(performance, output_path="report.txt")
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

#### _transpose_graph

```python
_transpose_graph(
    adjacency_list: Dict[int, List[int]],
    vertices: List[int]
) -> Dict[int, List[int]]
```

Build transpose (reversed) graph.

**Returns:**
- `Dict[int, List[int]]`: Transpose adjacency list with all edges reversed

#### _dfs_fill_order

```python
_dfs_fill_order(
    vertex: int,
    adjacency_list: Dict[int, List[int]],
    visited: Set[int],
    stack: List[int],
) -> None
```

DFS helper to fill stack with vertices in order of finishing times.

**Parameters:**
- `vertex`: Current vertex to visit
- `adjacency_list`: Adjacency list representation of graph
- `visited`: Set of visited vertices
- `stack`: Stack to store vertices in finishing time order

#### _dfs_collect_scc

```python
_dfs_collect_scc(
    vertex: int,
    transpose: Dict[int, List[int]],
    visited: Set[int],
    scc: List[int],
) -> None
```

DFS helper to collect vertices in current SCC.

**Parameters:**
- `vertex`: Current vertex to visit
- `transpose`: Transpose adjacency list
- `visited`: Set of visited vertices
- `scc`: List to collect vertices in current SCC

## Command-Line Interface

The module can be run as a script with the following interface:

```bash
python src/main.py [OPTIONS]
```

### Options

- `-e, --edges`: Edges as 'source-dest' pairs (e.g., '0-1 1-2')
- `-n, --num-vertices`: Number of vertices (if not specified, inferred from edges)
- `-c, --config`: Path to configuration file (default: config.yaml)
- `-m, --method`: Operation method - find, count, largest, stats, or compare (default: find)
- `-i, --iterations`: Number of iterations for timing (default: 1)
- `-r, --report`: Output path for performance report

### Examples

```bash
# Find all SCCs
python src/main.py --edges 0-1 1-2 2-0 --method find

# Get SCC count
python src/main.py --edges 0-1 1-2 2-0 --method count

# Get largest SCC
python src/main.py --edges 0-1 1-2 2-0 --method largest

# Get statistics
python src/main.py --edges 0-1 1-2 2-0 --method stats

# Compare performance
python src/main.py --edges 0-1 1-2 2-0 --method compare --report report.txt
```

## Error Handling

All methods validate inputs and raise appropriate exceptions:

- `ValueError`: Invalid input parameters (empty edges without num_vertices, negative vertices, num_vertices too small)
- `FileNotFoundError`: Configuration file not found
- `yaml.YAMLError`: Invalid YAML in configuration file
- `IOError`: File I/O errors when saving reports
- `PermissionError`: Insufficient permissions for file operations

## Algorithm Complexity

### Kosaraju's Algorithm

- **Time Complexity**: O(V + E) where V = number of vertices, E = number of edges
- **Space Complexity**: O(V + E) for adjacency lists, transpose graph, and stack
- **Approach**: Two-pass DFS
  - First pass: Fill stack with vertices in finishing order
  - Second pass: Process transpose graph to find SCCs

## Notes

- Kosaraju's algorithm requires two DFS passes
- The transpose graph must be built, requiring O(V + E) space
- All vertices are guaranteed to be in exactly one SCC
- Isolated vertices form their own SCCs (size 1)
- The algorithm works correctly for any directed graph
- SCCs are returned in arbitrary order (not sorted by size)
- Empty graphs return empty SCC lists
- Single-vertex graphs return one SCC containing that vertex
