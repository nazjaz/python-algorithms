# Union-Find API Documentation

## UnionFind Class

Union-Find (Disjoint Set) data structure with path compression and union by rank optimizations.

### Constructor

```python
UnionFind(
    num_elements: int,
    config_path: str = "config.yaml"
) -> None
```

Initialize UnionFind with specified number of elements.

**Parameters:**
- `num_elements` (int): Number of elements (0 to num_elements-1)
- `config_path` (str): Path to configuration YAML file. Default: "config.yaml"

**Raises:**
- `ValueError`: If num_elements is negative
- `FileNotFoundError`: If config file doesn't exist
- `yaml.YAMLError`: If config file is invalid YAML

**Example:**
```python
uf = UnionFind(10)
```

### Methods

#### find

```python
find(x: int) -> int
```

Find root of element with path compression.

Path compression flattens the tree by making all nodes point directly to the root during the find operation.

**Parameters:**
- `x` (int): Element to find root for

**Returns:**
- `int`: Root element of the set containing x

**Raises:**
- `ValueError`: If element index is invalid

**Time Complexity:** O(α(n)) amortized where α is inverse Ackermann function

**Example:**
```python
uf = UnionFind(10)
uf.union(0, 1)
root = uf.find(0)  # Returns root of set containing 0
```

#### union

```python
union(x: int, y: int) -> bool
```

Union two sets using union by rank.

Union by rank attaches the smaller tree under the larger tree, keeping the tree height small.

**Parameters:**
- `x` (int): First element
- `y` (int): Second element

**Returns:**
- `bool`: True if union was performed, False if already in same set

**Raises:**
- `ValueError`: If element indices are invalid

**Time Complexity:** O(α(n)) amortized where α is inverse Ackermann function

**Example:**
```python
uf = UnionFind(10)
result = uf.union(0, 1)  # Returns True
result = uf.union(0, 1)  # Returns False (already connected)
```

#### connected

```python
connected(x: int, y: int) -> bool
```

Check if two elements are in the same set.

**Parameters:**
- `x` (int): First element
- `y` (int): Second element

**Returns:**
- `bool`: True if elements are in same set, False otherwise

**Raises:**
- `ValueError`: If element indices are invalid

**Time Complexity:** O(α(n)) amortized where α is inverse Ackermann function

**Example:**
```python
uf = UnionFind(10)
uf.union(0, 1)
result = uf.connected(0, 1)  # Returns True
result = uf.connected(0, 2)  # Returns False
```

#### get_component_count

```python
get_component_count() -> int
```

Get number of disjoint components.

**Returns:**
- `int`: Number of disjoint sets

**Time Complexity:** O(1)

**Example:**
```python
uf = UnionFind(10)
count = uf.get_component_count()  # Returns 10
uf.union(0, 1)
count = uf.get_component_count()  # Returns 9
```

#### get_component

```python
get_component(x: int) -> List[int]
```

Get all elements in the same component as x.

**Parameters:**
- `x` (int): Element to get component for

**Returns:**
- `List[int]`: List of all elements in the same component

**Raises:**
- `ValueError`: If element index is invalid

**Time Complexity:** O(n) where n is number of elements

**Example:**
```python
uf = UnionFind(10)
uf.union(0, 1)
uf.union(1, 2)
component = uf.get_component(0)  # Returns [0, 1, 2]
```

#### get_all_components

```python
get_all_components() -> Dict[int, List[int]]
```

Get all disjoint components.

**Returns:**
- `Dict[int, List[int]]`: Dictionary mapping root to list of elements in that component

**Time Complexity:** O(n) where n is number of elements

**Example:**
```python
uf = UnionFind(10)
uf.union(0, 1)
uf.union(2, 3)
components = uf.get_all_components()
# Returns dictionary with roots as keys and component lists as values
```

#### get_largest_component

```python
get_largest_component() -> Optional[List[int]]
```

Get the largest component.

**Returns:**
- `Optional[List[int]]`: List of elements in largest component, or None if no elements

**Time Complexity:** O(n) where n is number of elements

**Example:**
```python
uf = UnionFind(10)
uf.union(0, 1)
uf.union(1, 2)
uf.union(3, 4)
largest = uf.get_largest_component()  # Returns [0, 1, 2] or [3, 4]
```

#### get_component_statistics

```python
get_component_statistics() -> Dict[str, any]
```

Get statistics about components.

**Returns:**
- `Dict[str, any]`: Dictionary containing component statistics:
    - `count`: Total number of components
    - `sizes`: List of component sizes
    - `largest_size`: Size of largest component
    - `smallest_size`: Size of smallest component
    - `average_size`: Average component size

**Time Complexity:** O(n) where n is number of elements

**Example:**
```python
uf = UnionFind(10)
uf.union(0, 1)
uf.union(1, 2)
stats = uf.get_component_statistics()
# Returns dictionary with count, sizes, largest_size, etc.
```

#### union_all

```python
union_all(pairs: List[Tuple[int, int]]) -> int
```

Union multiple pairs of elements.

**Parameters:**
- `pairs` (List[Tuple[int, int]]): List of (x, y) tuples to union

**Returns:**
- `int`: Number of unions performed

**Time Complexity:** O(m * α(n)) where m is number of pairs, n is number of elements

**Example:**
```python
uf = UnionFind(10)
pairs = [(0, 1), (1, 2), (3, 4)]
unions = uf.union_all(pairs)  # Returns 3
```

#### reset

```python
reset() -> None
```

Reset union-find to initial state (all elements separate).

**Time Complexity:** O(n) where n is number of elements

**Example:**
```python
uf = UnionFind(10)
uf.union(0, 1)
uf.reset()  # All elements are now separate again
```

#### compare_performance

```python
compare_performance(
    pairs: List[Tuple[int, int]],
    iterations: int = 1
) -> Dict[str, any]
```

Compare performance of union-find operations.

**Parameters:**
- `pairs` (List[Tuple[int, int]]): List of (x, y) tuples to union
- `iterations` (int): Number of iterations for timing. Default: 1

**Returns:**
- `Dict[str, any]`: Dictionary containing performance data for:
    - `union_all`: Union operations performance
    - `find_operations`: Find operations performance
    - `connected_checks`: Connectivity check performance

**Example:**
```python
uf = UnionFind(100)
pairs = [(0, 1), (1, 2), (2, 3)]
performance = uf.compare_performance(pairs, iterations=1000)
print(performance["union_all"]["time_milliseconds"])
```

#### generate_report

```python
generate_report(
    performance_data: Dict[str, any],
    output_path: Optional[str] = None
) -> str
```

Generate performance report for union-find operations.

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
uf = UnionFind(100)
pairs = [(0, 1), (1, 2), (2, 3)]
performance = uf.compare_performance(pairs)
report = uf.generate_report(performance, output_path="report.txt")
```

## Command-Line Interface

The module can be run as a script with the following interface:

```bash
python src/main.py -n NUM_ELEMENTS [OPTIONS]
```

### Arguments

- `-n, --num-elements`: (Required) Number of elements

### Options

- `-p, --pairs`: Pairs as 'x-y' (e.g., '0-1 1-2')
- `-c, --config`: Path to configuration file (default: config.yaml)
- `-o, --operation`: Operation to perform - union, find, connected, components, stats, or compare (default: union)
- `-i, --iterations`: Number of iterations for timing (default: 1)
- `-r, --report`: Output path for performance report

### Examples

```bash
# Union operations
python src/main.py -n 10 --pairs 0-1 1-2 2-3 --operation union

# Find operations
python src/main.py -n 10 --pairs 0-1 1-2 --operation find

# Connectivity checks
python src/main.py -n 10 --pairs 0-1 1-2 0-2 --operation connected

# Get all components
python src/main.py -n 10 --pairs 0-1 1-2 3-4 --operation components

# Get statistics
python src/main.py -n 10 --pairs 0-1 1-2 3-4 --operation stats

# Compare performance
python src/main.py -n 100 --pairs 0-1 1-2 --operation compare --report report.txt
```

## Error Handling

All methods validate inputs and raise appropriate exceptions:

- `ValueError`: Invalid input parameters (negative num_elements, invalid element indices)
- `FileNotFoundError`: Configuration file not found
- `yaml.YAMLError`: Invalid YAML in configuration file
- `IOError`: File I/O errors when saving reports
- `PermissionError`: Insufficient permissions for file operations

## Algorithm Complexity

### With Optimizations (Path Compression + Union by Rank)

- **Find**: O(α(n)) amortized where α is inverse Ackermann function
- **Union**: O(α(n)) amortized
- **Connected**: O(α(n)) amortized

### Without Optimizations

- **Find**: O(n) worst case
- **Union**: O(n) worst case

### Space Complexity

- O(n) for parent array
- O(n) for rank array
- Total: O(n)

## Notes

- Path compression flattens trees during find operations
- Union by rank keeps trees balanced
- α(n) is the inverse Ackermann function, which grows extremely slowly
- For practical purposes, α(n) ≤ 4 for all reasonable values of n
- The optimizations provide near-constant time complexity
- Union-Find is fundamental to many graph algorithms
- All elements start as separate components
- Union operations merge components
- Find operations determine component membership
- Component count tracks number of disjoint sets
