# Prim's Algorithm API Documentation

## PrimMST Class

Main class for finding minimum spanning tree using Prim's algorithm with different data structure choices.

### Constructor

```python
PrimMST(config_path: str = "config.yaml") -> None
```

Initialize PrimMST with configuration.

**Parameters:**
- `config_path` (str): Path to configuration YAML file. Default: "config.yaml"

**Raises:**
- `FileNotFoundError`: If config file doesn't exist
- `yaml.YAMLError`: If config file is invalid YAML

### Methods

#### find_mst_list

```python
find_mst_list(
    num_vertices: int,
    edges: List[Tuple[int, int, float]],
    start_vertex: int = 0
) -> Tuple[List[Tuple[int, int, float]], float]
```

Find MST using Prim's algorithm with list-based approach.

Uses simple list to find minimum edge, resulting in O(V²) time complexity. Suitable for dense graphs.

**Parameters:**
- `num_vertices` (int): Number of vertices in graph
- `edges` (List[Tuple[int, int, float]]): List of edges as (source, destination, weight) tuples
- `start_vertex` (int): Starting vertex. Default: 0

**Returns:**
- `Tuple[List[Tuple[int, int, float]], float]`: List of edges in MST and total weight

**Raises:**
- `ValueError`: If inputs are invalid or graph is disconnected

**Time Complexity:** O(V²) where V is number of vertices

**Example:**
```python
prim = PrimMST()
edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3), (0, 3, 4)]
mst_edges, total_weight = prim.find_mst_list(4, edges)
# mst_edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3)]
# total_weight = 6.0
```

#### find_mst_heap

```python
find_mst_heap(
    num_vertices: int,
    edges: List[Tuple[int, int, float]],
    start_vertex: int = 0
) -> Tuple[List[Tuple[int, int, float]], float]
```

Find MST using Prim's algorithm with binary heap approach.

Uses binary min-heap for priority queue, resulting in O(E log V) time complexity. Suitable for sparse graphs.

**Parameters:**
- `num_vertices` (int): Number of vertices in graph
- `edges` (List[Tuple[int, int, float]]): List of edges as (source, destination, weight) tuples
- `start_vertex` (int): Starting vertex. Default: 0

**Returns:**
- `Tuple[List[Tuple[int, int, float]], float]`: List of edges in MST and total weight

**Raises:**
- `ValueError`: If inputs are invalid or graph is disconnected

**Time Complexity:** O(E log V) where E is edges, V is vertices

**Example:**
```python
prim = PrimMST()
edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3), (0, 3, 4)]
mst_edges, total_weight = prim.find_mst_heap(4, edges)
# mst_edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3)]
# total_weight = 6.0
```

#### get_mst_edges_list

```python
get_mst_edges_list(
    num_vertices: int,
    edges: List[Tuple[int, int, float]],
    start_vertex: int = 0
) -> List[Tuple[int, int, float]]
```

Get MST edges using list-based approach.

**Parameters:**
- `num_vertices` (int): Number of vertices in graph
- `edges` (List[Tuple[int, int, float]]): List of edges as (source, destination, weight) tuples
- `start_vertex` (int): Starting vertex. Default: 0

**Returns:**
- `List[Tuple[int, int, float]]`: List of edges in MST

#### get_mst_edges_heap

```python
get_mst_edges_heap(
    num_vertices: int,
    edges: List[Tuple[int, int, float]],
    start_vertex: int = 0
) -> List[Tuple[int, int, float]]
```

Get MST edges using heap-based approach.

**Parameters:**
- `num_vertices` (int): Number of vertices in graph
- `edges` (List[Tuple[int, int, float]]): List of edges as (source, destination, weight) tuples
- `start_vertex` (int): Starting vertex. Default: 0

**Returns:**
- `List[Tuple[int, int, float]]`: List of edges in MST

#### get_mst_weight_list

```python
get_mst_weight_list(
    num_vertices: int,
    edges: List[Tuple[int, int, float]],
    start_vertex: int = 0
) -> float
```

Get MST weight using list-based approach.

**Parameters:**
- `num_vertices` (int): Number of vertices in graph
- `edges` (List[Tuple[int, int, float]]): List of edges as (source, destination, weight) tuples
- `start_vertex` (int): Starting vertex. Default: 0

**Returns:**
- `float`: Total weight of MST

#### get_mst_weight_heap

```python
get_mst_weight_heap(
    num_vertices: int,
    edges: List[Tuple[int, int, float]],
    start_vertex: int = 0
) -> float
```

Get MST weight using heap-based approach.

**Parameters:**
- `num_vertices` (int): Number of vertices in graph
- `edges` (List[Tuple[int, int, float]]): List of edges as (source, destination, weight) tuples
- `start_vertex` (int): Starting vertex. Default: 0

**Returns:**
- `float`: Total weight of MST

#### compare_approaches

```python
compare_approaches(
    num_vertices: int,
    edges: List[Tuple[int, int, float]],
    start_vertex: int = 0,
    iterations: int = 1
) -> Dict[str, any]
```

Compare list-based and heap-based approaches.

**Parameters:**
- `num_vertices` (int): Number of vertices in graph
- `edges` (List[Tuple[int, int, float]]): List of edges as (source, destination, weight) tuples
- `start_vertex` (int): Starting vertex. Default: 0
- `iterations` (int): Number of iterations for timing. Default: 1

**Returns:**
- `Dict[str, any]`: Dictionary containing comparison data for:
    - `list_based`: List-based approach results and timing
    - `heap_based`: Heap-based approach results and timing
    - `fastest`: Fastest approach name (if both successful)
    - `fastest_time`: Time of fastest approach

**Example:**
```python
prim = PrimMST()
edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3)]
comparison = prim.compare_approaches(4, edges, iterations=1000)
print(comparison["list_based"]["time_milliseconds"])
print(comparison["heap_based"]["time_milliseconds"])
```

#### generate_report

```python
generate_report(
    comparison_data: Dict[str, any],
    output_path: Optional[str] = None
) -> str
```

Generate comparison report for Prim's algorithm approaches.

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
prim = PrimMST()
edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3)]
comparison = prim.compare_approaches(4, edges)
report = prim.generate_report(comparison, output_path="report.txt")
```

## MinHeap Class

Min-heap implementation for priority queue in Prim's algorithm.

### Constructor

```python
MinHeap() -> None
```

Initialize MinHeap.

### Methods

#### insert

```python
insert(weight: float, vertex: int) -> None
```

Insert element into heap.

**Parameters:**
- `weight` (float): Weight/priority value
- `vertex` (int): Vertex identifier

**Time Complexity:** O(log n)

#### extract_min

```python
extract_min() -> Optional[Tuple[float, int]]
```

Extract and return minimum element.

**Returns:**
- `Optional[Tuple[float, int]]`: Tuple of (weight, vertex) or None if empty

**Time Complexity:** O(log n)

#### is_empty

```python
is_empty() -> bool
```

Check if heap is empty.

**Returns:**
- `bool`: True if heap is empty, False otherwise

**Time Complexity:** O(1)

## Command-Line Interface

The module can be run as a script with the following interface:

```bash
python src/main.py -n NUM_VERTICES [OPTIONS]
```

### Arguments

- `-n, --num-vertices`: (Required) Number of vertices

### Options

- `-e, --edges`: Edges as 'source-dest-weight' (e.g., '0-1-5 1-2-3')
- `-s, --start-vertex`: Starting vertex (default: 0)
- `-c, --config`: Path to configuration file (default: config.yaml)
- `-o, --operation`: Operation to perform - list, heap, or compare (default: compare)
- `-i, --iterations`: Number of iterations for timing (default: 1)
- `-r, --report`: Output path for performance report

### Examples

```bash
# List-based approach
python src/main.py -n 4 --edges 0-1-1 1-2-2 2-3-3 --operation list

# Heap-based approach
python src/main.py -n 4 --edges 0-1-1 1-2-2 2-3-3 --operation heap

# Compare approaches
python src/main.py -n 4 --edges 0-1-1 1-2-2 2-3-3 --operation compare

# With custom start vertex
python src/main.py -n 4 --edges 0-1-1 1-2-2 2-3-3 --operation compare -s 2

# Generate report
python src/main.py -n 10 --edges 0-1-5 1-2-3 --operation compare --report report.txt
```

## Error Handling

All methods validate inputs and raise appropriate exceptions:

- `ValueError`: Invalid input parameters (negative num_vertices, invalid vertex indices, disconnected graph, self-loops, invalid start vertex)
- `FileNotFoundError`: Configuration file not found
- `yaml.YAMLError`: Invalid YAML in configuration file
- `IOError`: File I/O errors when saving reports
- `PermissionError`: Insufficient permissions for file operations

## Algorithm Complexity

### List-Based Approach

- **Time Complexity**: O(V²) where V is number of vertices
- **Space Complexity**: O(V + E) for adjacency list
- **Best For**: Dense graphs (E ≈ V²)

### Heap-Based Approach

- **Time Complexity**: O(E log V) where E is edges, V is vertices
- **Space Complexity**: O(V + E) for adjacency list and heap
- **Best For**: Sparse graphs (E << V²)

## Notes

- Prim's algorithm is a greedy algorithm
- Works with any connected weighted undirected graph
- MST has exactly V-1 edges for V vertices
- Algorithm grows MST from a starting vertex
- List-based approach is simpler but slower for sparse graphs
- Heap-based approach is more complex but faster for sparse graphs
- Both approaches produce identical MST (same edges and weight)
- Starting vertex can be any vertex (MST is independent of start)
- Graph must be connected for MST to exist
- Self-loops are not allowed in MST
- Negative weights are supported
- Floating point weights are supported
