# Hungarian Algorithm API Documentation

This document provides detailed API documentation for the Hungarian algorithm implementation for solving assignment problems.

## Classes

### HungarianAlgorithm

Main class for solving assignment problems using the Hungarian algorithm.

#### Methods

##### `__init__(cost_matrix: List[List[int]], config_path: str = "config.yaml") -> None`

Initialize Hungarian algorithm with cost matrix.

**Parameters:**
- `cost_matrix`: Square cost matrix (n x n) where cost_matrix[i][j] is cost of assigning worker i to job j
- `config_path`: Path to configuration YAML file (default: "config.yaml")

**Raises:**
- `ValueError`: If matrix is empty or not square

**Example:**
```python
matrix = [[1, 2], [2, 1]]
algorithm = HungarianAlgorithm(matrix)
```

##### `solve() -> Tuple[int, List[Tuple[int, int]]]`

Solve assignment problem using Hungarian algorithm.

**Returns:**
- Tuple of (minimum_cost, assignments) where assignments is list of (worker, job) pairs

**Time Complexity:** O(n^3)

**Example:**
```python
min_cost, assignments = algorithm.solve()
print(f"Minimum cost: {min_cost}")
for worker, job in assignments:
    print(f"Worker {worker} -> Job {job}")
```

##### `solve_maximization() -> Tuple[int, List[Tuple[int, int]]]`

Solve maximization version of assignment problem.

Converts maximization to minimization by transforming costs.

**Returns:**
- Tuple of (maximum_value, assignments)

**Time Complexity:** O(n^3)

**Example:**
```python
max_value, assignments = algorithm.solve_maximization()
print(f"Maximum value: {max_value}")
```

##### `get_assignment_cost(worker: int, job: int) -> int`

Get cost of specific assignment.

**Parameters:**
- `worker`: Worker index
- `job`: Job index

**Returns:**
- Assignment cost

**Raises:**
- `ValueError`: If indices are invalid

**Example:**
```python
cost = algorithm.get_assignment_cost(0, 1)  # Returns cost of worker 0 to job 1
```

##### `is_valid_assignment(assignments: List[Tuple[int, int]]) -> bool`

Check if assignment is valid (one-to-one mapping).

**Parameters:**
- `assignments`: List of (worker, job) pairs

**Returns:**
- `True` if valid, `False` otherwise

**Example:**
```python
assignments = [(0, 1), (1, 0)]
is_valid = algorithm.is_valid_assignment(assignments)  # Returns True
```

### BipartiteGraph

Represents a bipartite graph for assignment problems.

#### Methods

##### `__init__(left_size: int, right_size: int) -> None`

Initialize bipartite graph.

**Parameters:**
- `left_size`: Number of vertices in left partition
- `right_size`: Number of vertices in right partition

**Raises:**
- `ValueError`: If sizes are less than 1

**Example:**
```python
graph = BipartiteGraph(4, 4)
```

##### `add_edge(left: int, right: int, weight: int) -> None`

Add weighted edge to graph.

**Parameters:**
- `left`: Vertex in left partition
- `right`: Vertex in right partition
- `weight`: Edge weight (cost)

**Raises:**
- `ValueError`: If vertices are invalid

**Example:**
```python
graph.add_edge(0, 1, 10)
```

##### `to_cost_matrix() -> List[List[int]]`

Convert bipartite graph to cost matrix.

**Returns:**
- Cost matrix for Hungarian algorithm

**Example:**
```python
matrix = graph.to_cost_matrix()
algorithm = HungarianAlgorithm(matrix)
```

##### `solve_assignment() -> Tuple[int, List[Tuple[int, int]]]`

Solve assignment problem using Hungarian algorithm.

**Returns:**
- Tuple of (minimum_cost, assignments)

**Example:**
```python
min_cost, assignments = graph.solve_assignment()
```

## Usage Examples

### Basic Assignment Problem

```python
from src.main import HungarianAlgorithm

# Create cost matrix
cost_matrix = [
    [9, 2, 7, 8],
    [6, 4, 3, 7],
    [5, 8, 1, 8],
    [7, 6, 9, 4],
]

# Solve
algorithm = HungarianAlgorithm(cost_matrix)
min_cost, assignments = algorithm.solve()

print(f"Minimum cost: {min_cost}")
for worker, job in assignments:
    cost = algorithm.get_assignment_cost(worker, job)
    print(f"Worker {worker} -> Job {job} (cost: {cost})")
```

### Maximization Problem

```python
algorithm = HungarianAlgorithm(cost_matrix)
max_value, assignments = algorithm.solve_maximization()
print(f"Maximum value: {max_value}")
```

### Using Bipartite Graph

```python
from src.main import BipartiteGraph

# Create graph
graph = BipartiteGraph(4, 4)

# Add edges
for i in range(4):
    for j in range(4):
        graph.add_edge(i, j, cost_matrix[i][j])

# Solve
min_cost, assignments = graph.solve_assignment()
print(f"Minimum cost: {min_cost}")
```

### Assignment Validation

```python
algorithm = HungarianAlgorithm(cost_matrix)
min_cost, assignments = algorithm.solve()

if algorithm.is_valid_assignment(assignments):
    print("Assignment is valid")
else:
    print("Assignment is invalid")
```

### Large Matrix

```python
import random

# Create large cost matrix
n = 10
cost_matrix = [[random.randint(1, 100) for _ in range(n)] for _ in range(n)]

algorithm = HungarianAlgorithm(cost_matrix)
min_cost, assignments = algorithm.solve()
print(f"Minimum cost for {n}x{n} matrix: {min_cost}")
```

## Error Handling

The implementation handles the following cases gracefully:

- **Empty matrix**: Raises `ValueError` during initialization
- **Non-square matrix**: Raises `ValueError` during initialization
- **Invalid indices**: Raises `ValueError` for out-of-bounds access
- **Invalid graph sizes**: Raises `ValueError` for zero or negative sizes

## Performance Characteristics

| Operation | Time Complexity | Space Complexity |
|-----------|----------------|------------------|
| Solve | O(n^3) | O(n^2) |
| Solve Maximization | O(n^3) | O(n^2) |
| Get Assignment Cost | O(1) | O(1) |
| Assignment Validation | O(n) | O(n) |
| Add Edge | O(1) | O(1) |
| To Cost Matrix | O(n^2) | O(n^2) |

Where n is the size of the cost matrix (n x n).

## Algorithm Details

### Hungarian Algorithm Steps

1. **Row Reduction**: Subtract minimum from each row
2. **Column Reduction**: Subtract minimum from each column
3. **Zero Covering**: Cover all zeros with minimum lines
4. **Matrix Adjustment**: Adjust if optimal assignment not found
5. **Assignment**: Find optimal assignment from zeros

### Key Properties

- **Optimality**: Guaranteed to find optimal solution
- **Polynomial Time**: O(n^3) complexity
- **Completeness**: Always finds complete assignment if one exists

## Thread Safety

This implementation is not thread-safe. For concurrent access, external synchronization is required.
