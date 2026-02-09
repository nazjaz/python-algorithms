# Kruskal's Algorithm API Documentation

## KruskalMST Class

Main class for finding minimum spanning tree using Kruskal's algorithm.

### Constructor

```python
KruskalMST(config_path: str = "config.yaml") -> None
```

Initialize KruskalMST with configuration.

**Parameters:**
- `config_path` (str): Path to configuration YAML file. Default: "config.yaml"

**Raises:**
- `FileNotFoundError`: If config file doesn't exist
- `yaml.YAMLError`: If config file is invalid YAML

### Methods

#### find_mst

```python
find_mst(
    num_vertices: int,
    edges: List[Tuple[int, int, float]],
) -> Tuple[List[Tuple[int, int, float]], float]
```

Find minimum spanning tree using Kruskal's algorithm.

Algorithm steps:
1. Sort all edges by weight in ascending order
2. Initialize union-find data structure
3. Iterate through edges in sorted order
4. Add edge to MST if it doesn't create a cycle
5. Stop when we have V-1 edges (for V vertices)

**Parameters:**
- `num_vertices` (int): Number of vertices in graph
- `edges` (List[Tuple[int, int, float]]): List of edges as (source, destination, weight) tuples

**Returns:**
- `Tuple[List[Tuple[int, int, float]], float]`: List of edges in MST and total weight

**Raises:**
- `ValueError`: If inputs are invalid or graph is disconnected

**Time Complexity:** O(E log E) where E is number of edges

**Example:**
```python
kruskal = KruskalMST()
edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3), (0, 3, 4)]
mst_edges, total_weight = kruskal.find_mst(4, edges)
# mst_edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3)]
# total_weight = 6.0
```

#### get_mst_edges

```python
get_mst_edges(
    num_vertices: int,
    edges: List[Tuple[int, int, float]],
) -> List[Tuple[int, int, float]]
```

Get edges in minimum spanning tree.

**Parameters:**
- `num_vertices` (int): Number of vertices in graph
- `edges` (List[Tuple[int, int, float]]): List of edges as (source, destination, weight) tuples

**Returns:**
- `List[Tuple[int, int, float]]`: List of edges in MST

**Example:**
```python
kruskal = KruskalMST()
edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3), (0, 3, 4)]
mst_edges = kruskal.get_mst_edges(4, edges)
# Returns list of MST edges
```

#### get_mst_weight

```python
get_mst_weight(
    num_vertices: int,
    edges: List[Tuple[int, int, float]],
) -> float
```

Get total weight of minimum spanning tree.

**Parameters:**
- `num_vertices` (int): Number of vertices in graph
- `edges` (List[Tuple[int, int, float]]): List of edges as (source, destination, weight) tuples

**Returns:**
- `float`: Total weight of MST

**Example:**
```python
kruskal = KruskalMST()
edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3), (0, 3, 4)]
total_weight = kruskal.get_mst_weight(4, edges)
# Returns 6.0
```

#### compare_performance

```python
compare_performance(
    num_vertices: int,
    edges: List[Tuple[int, int, float]],
    iterations: int = 1
) -> Dict[str, any]
```

Compare performance of MST operations.

**Parameters:**
- `num_vertices` (int): Number of vertices in graph
- `edges` (List[Tuple[int, int, float]]): List of edges as (source, destination, weight) tuples
- `iterations` (int): Number of iterations for timing. Default: 1

**Returns:**
- `Dict[str, any]`: Dictionary containing performance data for:
    - `find_mst`: Complete MST finding operation
    - `get_mst_edges`: MST edges retrieval
    - `get_mst_weight`: MST weight calculation

**Example:**
```python
kruskal = KruskalMST()
edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3)]
performance = kruskal.compare_performance(4, edges, iterations=1000)
print(performance["find_mst"]["time_milliseconds"])
```

#### generate_report

```python
generate_report(
    performance_data: Dict[str, any],
    output_path: Optional[str] = None
) -> str
```

Generate performance report for MST operations.

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
kruskal = KruskalMST()
edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3)]
performance = kruskal.compare_performance(4, edges)
report = kruskal.generate_report(performance, output_path="report.txt")
```

## UnionFind Class

Union-Find data structure for cycle detection in Kruskal's algorithm.

### Constructor

```python
UnionFind(num_vertices: int) -> None
```

Initialize UnionFind.

**Parameters:**
- `num_vertices` (int): Number of vertices

### Methods

#### find

```python
find(x: int) -> int
```

Find root with path compression.

**Parameters:**
- `x` (int): Vertex to find root for

**Returns:**
- `int`: Root vertex

**Time Complexity:** O(α(n)) amortized

#### union

```python
union(x: int, y: int) -> bool
```

Union two sets using union by rank.

**Parameters:**
- `x` (int): First vertex
- `y` (int): Second vertex

**Returns:**
- `bool`: True if union was performed, False if already in same set

**Time Complexity:** O(α(n)) amortized

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
- `-o, --operation`: Operation to perform - mst, edges, weight, or compare (default: mst)
- `-i, --iterations`: Number of iterations for timing (default: 1)
- `-r, --report`: Output path for performance report

### Examples

```bash
# Find MST
python src/main.py -n 4 --edges 0-1-1 1-2-2 2-3-3 0-3-4 --operation mst

# Get MST edges only
python src/main.py -n 4 --edges 0-1-1 1-2-2 2-3-3 --operation edges

# Get MST weight only
python src/main.py -n 4 --edges 0-1-1 1-2-2 2-3-3 --operation weight

# Compare performance
python src/main.py -n 10 --edges 0-1-5 1-2-3 --operation compare --report report.txt
```

## Error Handling

All methods validate inputs and raise appropriate exceptions:

- `ValueError`: Invalid input parameters (negative num_vertices, invalid vertex indices, disconnected graph, self-loops)
- `FileNotFoundError`: Configuration file not found
- `yaml.YAMLError`: Invalid YAML in configuration file
- `IOError`: File I/O errors when saving reports
- `PermissionError`: Insufficient permissions for file operations

## Algorithm Complexity

### Kruskal's Algorithm

- **Time Complexity**: O(E log E) where E is number of edges
  - Sorting edges: O(E log E)
  - Union-Find operations: O(E α(V)) where α is inverse Ackermann function
- **Space Complexity**: O(V + E)
  - O(V) for union-find
  - O(E) for edges

### Union-Find Operations

- **Find**: O(α(n)) amortized with path compression
- **Union**: O(α(n)) amortized with union by rank

## Notes

- Kruskal's algorithm is a greedy algorithm
- Works with any connected weighted undirected graph
- MST has exactly V-1 edges for V vertices
- Algorithm selects edges in order of increasing weight
- Union-find efficiently detects cycles
- Graph must be connected for MST to exist
- Self-loops are not allowed in MST
- Negative weights are supported
- Floating point weights are supported
- Duplicate edges are handled (algorithm selects minimum weight)
