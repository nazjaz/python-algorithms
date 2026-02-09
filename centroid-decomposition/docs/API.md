# Centroid Decomposition API Documentation

This document provides detailed API documentation for the centroid decomposition implementation with divide and conquer tree problem solving.

## Classes

### TreeNode

Node in a tree.

#### Attributes

- `value` (int): Node value/identifier
- `data` (float): Data stored in node
- `neighbors` (List[TreeNode]): List of neighbor nodes (undirected edges)
- `parent` (Optional[TreeNode]): Parent node (optional)

#### Methods

##### `__init__(value: int, data: float = 0.0) -> None`

Initialize tree node.

**Parameters:**
- `value`: Node value/identifier
- `data`: Data stored in node (default: 0.0)

**Example:**
```python
node = TreeNode(5, data=10.0)
```

##### `add_neighbor(neighbor: TreeNode) -> None`

Add neighbor node (undirected edge).

**Parameters:**
- `neighbor`: Neighbor node to add

**Example:**
```python
node1 = TreeNode(1)
node2 = TreeNode(2)
node1.add_neighbor(node2)
```

### CentroidDecomposition

Main class for centroid decomposition.

#### Methods

##### `__init__(root: TreeNode, config_path: str = "config.yaml") -> None`

Initialize centroid decomposition.

**Parameters:**
- `root`: Root of the tree
- `config_path`: Path to configuration YAML file (default: "config.yaml")

**Example:**
```python
root = TreeNode(0)
cd = CentroidDecomposition(root)
```

##### `decompose() -> None`

Perform centroid decomposition.

**Time Complexity:** O(n log n)

**Example:**
```python
cd.decompose()
```

##### `solve_with_divide_conquer(problem_solver: Callable[[TreeNode, List[Tuple[TreeNode, int]]], float]) -> float`

Solve tree problem using divide and conquer.

**Parameters:**
- `problem_solver`: Function that solves problem for centroid and distances.
  - Takes (centroid, list of (node, distance) tuples)
  - Returns solution value

**Returns:**
- Problem solution

**Raises:**
- `ValueError`: If tree not decomposed

**Time Complexity:** O(n log n)

**Example:**
```python
def problem_solver(centroid, distances):
    return sum(1 for _, d in distances if d <= 2)

result = cd.solve_with_divide_conquer(problem_solver)
```

##### `count_paths_with_condition(condition: Callable[[int], bool]) -> int`

Count paths satisfying condition using divide and conquer.

**Parameters:**
- `condition`: Function that checks if distance satisfies condition

**Returns:**
- Number of paths satisfying condition

**Raises:**
- `ValueError`: If tree not decomposed

**Time Complexity:** O(n log n)

**Example:**
```python
count = cd.count_paths_with_condition(lambda d: d <= 2)
```

##### `get_centroid_tree_root() -> Optional[TreeNode]`

Get root of centroid tree.

**Returns:**
- Root of centroid tree or None if not decomposed

**Example:**
```python
centroid_root = cd.get_centroid_tree_root()
```

##### `get_centroid_parent(node: TreeNode) -> Optional[TreeNode]`

Get parent of node in centroid tree.

**Parameters:**
- `node`: Node in centroid tree

**Returns:**
- Parent node or None

**Example:**
```python
parent = cd.get_centroid_parent(node)
```

## Functions

### `build_tree_from_edges(n: int, edges: List[Tuple[int, int]], root_value: int = 0) -> TreeNode`

Build tree from list of edges.

**Parameters:**
- `n`: Number of nodes
- `edges`: List of (u, v) edges (undirected)
- `root_value`: Value of root node (default: 0)

**Returns:**
- Root node of tree

**Raises:**
- `ValueError`: If invalid tree structure

**Example:**
```python
n = 7
edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)]
root = build_tree_from_edges(n, edges, 0)
```

## Usage Examples

### Basic Decomposition

```python
from src.main import TreeNode, CentroidDecomposition

# Build tree
root = TreeNode(0)
node1 = TreeNode(1)
node2 = TreeNode(2)
root.add_neighbor(node1)
root.add_neighbor(node2)

# Create and decompose
cd = CentroidDecomposition(root)
cd.decompose()

# Get centroid root
centroid_root = cd.get_centroid_tree_root()
print(f"Centroid root: {centroid_root.value}")
```

### Path Counting

```python
from src.main import build_tree_from_edges, CentroidDecomposition

# Build tree
n = 7
edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)]
root = build_tree_from_edges(n, edges, 0)

# Decompose
cd = CentroidDecomposition(root)
cd.decompose()

# Count paths with distance <= 2
count = cd.count_paths_with_condition(lambda d: d <= 2)
print(f"Paths with distance <= 2: {count}")

# Count paths with even distance
count = cd.count_paths_with_condition(lambda d: d % 2 == 0)
print(f"Paths with even distance: {count}")
```

### Custom Problem Solver

```python
from src.main import TreeNode, CentroidDecomposition

# Build tree
root = TreeNode(0)
node1 = TreeNode(1, data=5.0)
node2 = TreeNode(2, data=10.0)
root.add_neighbor(node1)
root.add_neighbor(node2)

# Decompose
cd = CentroidDecomposition(root)
cd.decompose()

# Custom problem: sum of data for nodes within distance 1
def problem_solver(centroid, distances):
    total = 0.0
    for node, dist in distances:
        if dist <= 1:
            total += node.data
    return total

result = cd.solve_with_divide_conquer(problem_solver)
print(f"Problem result: {result}")
```

### Error Handling

```python
from src.main import TreeNode, CentroidDecomposition

root = TreeNode(0)
cd = CentroidDecomposition(root)

# Try to solve without decomposition
try:
    cd.count_paths_with_condition(lambda d: d <= 2)
except ValueError as e:
    print(f"Error: {e}")

# Decompose first
cd.decompose()

# Now it works
count = cd.count_paths_with_condition(lambda d: d <= 2)
```

## Time Complexity Summary

| Operation | Time Complexity |
|-----------|----------------|
| `decompose` | O(n log n) |
| `solve_with_divide_conquer` | O(n log n) |
| `count_paths_with_condition` | O(n log n) |
| `get_centroid_tree_root` | O(1) |
| `get_centroid_parent` | O(1) |

Where n is the number of nodes in the tree.

## Notes

- Centroid decomposition requires preprocessing before problem solving
- Preprocessing is done via `decompose()` method
- Divide and conquer framework is flexible for various problems
- Each node is processed O(log n) times in decomposition
- Tree structure should be valid (connected, no cycles)
- Supports arbitrary tree structures
