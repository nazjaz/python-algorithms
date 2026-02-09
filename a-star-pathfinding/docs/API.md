# A* Pathfinding API Documentation

## AStarPathfinder Class

Main class for A* pathfinding algorithm with customizable heuristics and visualization.

### Constructor

```python
AStarPathfinder(config_path: str = "config.yaml") -> None
```

Initialize AStarPathfinder with configuration.

**Parameters:**
- `config_path` (str): Path to configuration YAML file. Default: "config.yaml"

**Raises:**
- `FileNotFoundError`: If config file doesn't exist
- `yaml.YAMLError`: If config file is invalid YAML

### Methods

#### find_path

```python
find_path(
    grid: List[List[int]],
    start: Tuple[int, int],
    goal: Tuple[int, int],
    heuristic: str = "manhattan",
    allow_diagonal: bool = False
) -> Tuple[Optional[List[Tuple[int, int]]], Dict[str, any]]
```

Find path using A* algorithm.

**Parameters:**
- `grid` (List[List[int]]): Grid representation (0=free, 1=obstacle)
- `start` (Tuple[int, int]): Start position as (x, y) tuple
- `goal` (Tuple[int, int]): Goal position as (x, y) tuple
- `heuristic` (str): Heuristic function name (manhattan, euclidean, chebyshev, diagonal). Default: "manhattan"
- `allow_diagonal` (bool): Whether to allow diagonal movement. Default: False

**Returns:**
- `Tuple[Optional[List[Tuple[int, int]]], Dict[str, any]]`: Path as list of (x, y) tuples (or None if no path), and statistics dictionary

**Raises:**
- `ValueError`: If inputs are invalid

**Time Complexity:** O(b^d) where b=branching factor, d=depth

**Example:**
```python
pathfinder = AStarPathfinder()
grid = [[0 for _ in range(10)] for _ in range(10)]
path, stats = pathfinder.find_path(grid, (0, 0), (9, 9), "manhattan")
# path = [(0, 0), (0, 1), ..., (9, 9)]
# stats = {"nodes_explored": 50, "path_length": 18, "success": True}
```

#### visualize_path

```python
visualize_path(
    grid: List[List[int]],
    path: Optional[List[Tuple[int, int]]],
    start: Tuple[int, int],
    goal: Tuple[int, int]
) -> str
```

Visualize grid with path.

**Parameters:**
- `grid` (List[List[int]]): Grid representation (0=free, 1=obstacle)
- `path` (Optional[List[Tuple[int, int]]]): Path as list of (x, y) tuples
- `start` (Tuple[int, int]): Start position
- `goal` (Tuple[int, int]): Goal position

**Returns:**
- `str`: String representation of visualized grid

**Example:**
```python
pathfinder = AStarPathfinder()
grid = [[0 for _ in range(5)] for _ in range(5)]
path = [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)]
visualization = pathfinder.visualize_path(grid, path, (0, 0), (2, 2))
# Returns ASCII visualization with S, G, *, #, .
```

#### compare_heuristics

```python
compare_heuristics(
    grid: List[List[int]],
    start: Tuple[int, int],
    goal: Tuple[int, int],
    allow_diagonal: bool = False,
    iterations: int = 1
) -> Dict[str, any]
```

Compare different heuristics.

**Parameters:**
- `grid` (List[List[int]]): Grid representation (0=free, 1=obstacle)
- `start` (Tuple[int, int]): Start position
- `goal` (Tuple[int, int]): Goal position
- `allow_diagonal` (bool): Whether to allow diagonal movement. Default: False
- `iterations` (int): Number of iterations for timing. Default: 1

**Returns:**
- `Dict[str, any]`: Dictionary containing comparison data for all heuristics

**Example:**
```python
pathfinder = AStarPathfinder()
grid = [[0 for _ in range(10)] for _ in range(10)]
comparison = pathfinder.compare_heuristics(grid, (0, 0), (9, 9))
print(comparison["manhattan"]["time_milliseconds"])
```

#### generate_report

```python
generate_report(
    comparison_data: Dict[str, any],
    output_path: Optional[str] = None
) -> str
```

Generate comparison report for heuristics.

**Parameters:**
- `comparison_data` (Dict[str, any]): Comparison data from `compare_heuristics()`
- `output_path` (Optional[str]): Optional path to save report file

**Returns:**
- `str`: Report content as string

**Raises:**
- `IOError`: If file cannot be written
- `PermissionError`: If file is not writable

### Heuristic Methods

#### manhattan_distance

```python
manhattan_distance(x1: int, y1: int, x2: int, y2: int) -> float
```

Calculate Manhattan distance heuristic.

**Returns:** |x1 - x2| + |y1 - y2|

**Best for:** 4-directional movement

#### euclidean_distance

```python
euclidean_distance(x1: int, y1: int, x2: int, y2: int) -> float
```

Calculate Euclidean distance heuristic.

**Returns:** sqrt((x1 - x2)² + (y1 - y2)²)

**Best for:** Continuous movement

#### chebyshev_distance

```python
chebyshev_distance(x1: int, y1: int, x2: int, y2: int) -> float
```

Calculate Chebyshev distance heuristic.

**Returns:** max(|x1 - x2|, |y1 - y2|)

**Best for:** 8-directional movement

#### diagonal_distance

```python
diagonal_distance(x1: int, y1: int, x2: int, y2: int) -> float
```

Calculate diagonal distance heuristic.

**Returns:** (dx + dy) + (√2 - 2) * min(dx, dy)

**Best for:** 8-directional movement with different costs

## Node Class

Node in the pathfinding grid.

### Constructor

```python
Node(x: int, y: int, g: float = float("inf"), h: float = 0.0) -> None
```

Initialize Node.

**Parameters:**
- `x` (int): X coordinate
- `y` (int): Y coordinate
- `g` (float): Cost from start to this node. Default: inf
- `h` (float): Heuristic estimate from this node to goal. Default: 0.0

### Properties

- `x`: X coordinate
- `y`: Y coordinate
- `g`: Cost from start
- `h`: Heuristic estimate
- `f`: Total cost (g + h)
- `parent`: Parent node for path reconstruction

## Command-Line Interface

The module can be run as a script with the following interface:

```bash
python src/main.py [OPTIONS]
```

### Options

- `-g, --grid`: Grid size as 'rows-cols' (e.g., '10x10')
- `-s, --start`: Start position as 'x-y' (e.g., '0-0')
- `-e, --end`: End position as 'x-y' (e.g., '9-9')
- `-o, --obstacles`: Obstacles as 'x-y' pairs (e.g., '1-1 2-2')
- `-h, --heuristic`: Heuristic function - manhattan, euclidean, chebyshev, or diagonal (default: manhattan)
- `-d, --diagonal`: Allow diagonal movement
- `-c, --config`: Path to configuration file (default: config.yaml)
- `-m, --mode`: Operation mode - find, compare, or visualize (default: find)
- `-i, --iterations`: Number of iterations for timing (default: 1)
- `-r, --report`: Output path for performance report

### Examples

```bash
# Find path
python src/main.py -g 10x10 -s 0-0 -e 9-9 --mode find

# Find path with obstacles
python src/main.py -g 10x10 -s 0-0 -e 9-9 -o 1-1 2-2 --mode find

# Find path with diagonal movement
python src/main.py -g 10x10 -s 0-0 -e 9-9 --diagonal --mode find

# Visualize path
python src/main.py -g 10x10 -s 0-0 -e 9-9 --mode visualize

# Compare heuristics
python src/main.py -g 10x10 -s 0-0 -e 9-9 --mode compare --report report.txt
```

## Error Handling

All methods validate inputs and raise appropriate exceptions:

- `ValueError`: Invalid input parameters (empty grid, invalid positions, obstacles at start/goal, unknown heuristic)
- `FileNotFoundError`: Configuration file not found
- `yaml.YAMLError`: Invalid YAML in configuration file
- `IOError`: File I/O errors when saving reports
- `PermissionError`: Insufficient permissions for file operations

## Algorithm Complexity

### A* Algorithm

- **Time Complexity**: O(b^d) where b=branching factor, d=depth
- **Space Complexity**: O(b^d) for open and closed sets
- **Optimal**: Yes (with admissible heuristic)
- **Complete**: Yes (will find path if one exists)

### Heuristic Properties

All provided heuristics are:
- **Admissible**: Never overestimate the actual cost
- **Consistent**: Satisfy triangle inequality
- **Optimal**: Guarantee optimal paths

## Notes

- A* guarantees optimal path when heuristic is admissible
- Grid uses 0-indexed coordinates
- Grid values: 0 = free cell, 1 = obstacle
- Path includes both start and goal positions
- Diagonal movement has cost √2
- Non-diagonal movement has cost 1
- Visualization uses ASCII characters (S=start, G=goal, #=obstacle, *=path, .=free)
- All heuristics produce optimal paths but may explore different numbers of nodes
- Manhattan is typically fastest for 4-directional movement
- Chebyshev/Diagonal are better for 8-directional movement
- Euclidean is most accurate but may be slower due to square root calculation
