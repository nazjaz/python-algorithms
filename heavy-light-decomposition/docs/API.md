# Heavy-Light Decomposition API Documentation

This document provides detailed API documentation for the heavy-light decomposition implementation with efficient path queries and updates on trees.

## Classes

### TreeNode

Node in a tree.

#### Attributes

- `value` (int): Node value/identifier
- `data` (float): Data stored in node
- `children` (List[TreeNode]): List of child nodes
- `parent` (Optional[TreeNode]): Parent node

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

##### `add_child(child: TreeNode) -> None`

Add child node.

**Parameters:**
- `child`: Child node to add

**Example:**
```python
parent = TreeNode(1)
child = TreeNode(2)
parent.add_child(child)
```

### SegmentTree

Segment tree for range queries and updates.

#### Methods

##### `__init__(size: int, operation: Callable[[float, float], float] = lambda x, y: x + y, identity: float = 0.0) -> None`

Initialize segment tree.

**Parameters:**
- `size`: Size of array
- `operation`: Binary operation (default: addition)
- `identity`: Identity element for operation (default: 0.0)

**Example:**
```python
seg_tree = SegmentTree(10)
```

##### `query_range(left: int, right: int) -> float`

Query range [left, right].

**Parameters:**
- `left`: Left index (inclusive)
- `right`: Right index (inclusive)

**Returns:**
- Result of operation over range

**Time Complexity:** O(log n)

**Example:**
```python
result = seg_tree.query_range(0, 5)
```

##### `update_range(left: int, right: int, value: float) -> None`

Update range [left, right] with value.

**Parameters:**
- `left`: Left index (inclusive)
- `right`: Right index (inclusive)
- `value`: Value to apply

**Time Complexity:** O(log n)

**Example:**
```python
seg_tree.update_range(0, 5, 10.0)
```

### HeavyLightDecomposition

Main class for heavy-light decomposition.

#### Methods

##### `__init__(root: TreeNode, config_path: str = "config.yaml") -> None`

Initialize heavy-light decomposition.

**Parameters:**
- `root`: Root of the tree
- `config_path`: Path to configuration YAML file (default: "config.yaml")

**Time Complexity:** O(n) preprocessing

**Example:**
```python
root = TreeNode(0)
hld = HeavyLightDecomposition(root)
```

##### `query_path(u: TreeNode, v: TreeNode) -> float`

Query path from u to v.

**Parameters:**
- `u`: First node
- `v`: Second node

**Returns:**
- Sum of data along path

**Time Complexity:** O(log^2 n)

**Example:**
```python
result = hld.query_path(node1, node2)
print(f"Path sum: {result}")
```

##### `update_path(u: TreeNode, v: TreeNode, value: float) -> None`

Update path from u to v by adding value.

**Parameters:**
- `u`: First node
- `v`: Second node
- `value`: Value to add to each node

**Time Complexity:** O(log^2 n)

**Example:**
```python
hld.update_path(node1, node2, 10.0)
```

##### `query_subtree(node: TreeNode) -> float`

Query subtree rooted at node.

**Parameters:**
- `node`: Root of subtree

**Returns:**
- Sum of data in subtree

**Time Complexity:** O(log^2 n)

**Example:**
```python
result = hld.query_subtree(node)
```

##### `get_lca(u: TreeNode, v: TreeNode) -> TreeNode`

Get lowest common ancestor of two nodes.

**Parameters:**
- `u`: First node
- `v`: Second node

**Returns:**
- LCA node

**Time Complexity:** O(log n)

**Example:**
```python
lca = hld.get_lca(node1, node2)
print(f"LCA: {lca.value}")
```

##### `get_distance(u: TreeNode, v: TreeNode) -> int`

Get distance between two nodes.

**Parameters:**
- `u`: First node
- `v`: Second node

**Returns:**
- Distance (number of edges)

**Time Complexity:** O(log n)

**Example:**
```python
distance = hld.get_distance(node1, node2)
print(f"Distance: {distance}")
```

## Functions

### `build_tree_from_edges(n: int, edges: List[Tuple[int, int]], root_value: int = 0) -> TreeNode`

Build tree from list of edges.

**Parameters:**
- `n`: Number of nodes
- `edges`: List of (parent, child) edges
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

### Basic Path Operations

```python
from src.main import TreeNode, HeavyLightDecomposition

# Build tree
root = TreeNode(0, data=1.0)
node1 = TreeNode(1, data=2.0)
node2 = TreeNode(2, data=3.0)
node3 = TreeNode(3, data=4.0)
root.add_child(node1)
root.add_child(node2)
node1.add_child(node3)

# Create HLD
hld = HeavyLightDecomposition(root)

# Path query
result = hld.query_path(node3, node2)
print(f"Path sum: {result}")

# Path update
hld.update_path(node3, node2, 5.0)

# Query after update
result = hld.query_path(node3, node2)
print(f"Path sum after update: {result}")
```

### Building Tree from Edges

```python
from src.main import build_tree_from_edges, HeavyLightDecomposition

# Build tree from edges
n = 7
edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)]
root = build_tree_from_edges(n, edges, 0)

# Create HLD
hld = HeavyLightDecomposition(root)

# Get nodes
node3 = root.children[0].children[0]
node5 = root.children[1].children[0]

# Path query
result = hld.query_path(node3, node5)
print(f"Path sum: {result}")
```

### LCA and Distance Queries

```python
from src.main import TreeNode, HeavyLightDecomposition

# Build tree
root = TreeNode(0)
node1 = TreeNode(1)
node2 = TreeNode(2)
node3 = TreeNode(3)
root.add_child(node1)
root.add_child(node2)
node1.add_child(node3)

# Create HLD
hld = HeavyLightDecomposition(root)

# LCA query
lca = hld.get_lca(node3, node2)
print(f"LCA: {lca.value}")

# Distance query
distance = hld.get_distance(node3, node2)
print(f"Distance: {distance}")
```

### Subtree Queries

```python
from src.main import TreeNode, HeavyLightDecomposition

# Build tree
root = TreeNode(0, data=1.0)
node1 = TreeNode(1, data=2.0)
node2 = TreeNode(2, data=3.0)
root.add_child(node1)
root.add_child(node2)

# Create HLD
hld = HeavyLightDecomposition(root)

# Subtree query
result = hld.query_subtree(root)
print(f"Subtree sum: {result}")
```

### Error Handling

```python
from src.main import build_tree_from_edges, HeavyLightDecomposition

# Invalid edge
try:
    n = 3
    edges = [(0, 1), (0, 10)]  # Node 10 doesn't exist
    root = build_tree_from_edges(n, edges, 0)
except ValueError as e:
    print(f"Error: {e}")

# Invalid root
try:
    n = 3
    edges = [(0, 1), (0, 2)]
    root = build_tree_from_edges(n, edges, 10)  # Root 10 doesn't exist
except ValueError as e:
    print(f"Error: {e}")
```

## Time Complexity Summary

| Operation | Time Complexity |
|-----------|----------------|
| Decomposition | O(n) |
| `query_path` | O(log^2 n) |
| `update_path` | O(log^2 n) |
| `query_subtree` | O(log^2 n) |
| `get_lca` | O(log n) |
| `get_distance` | O(log n) |

Where n is the number of nodes in the tree.

## Notes

- Heavy-light decomposition requires preprocessing before queries
- Preprocessing is done automatically in constructor
- Path queries and updates work on any two nodes in the tree
- Segment trees use lazy propagation for efficient updates
- Tree structure should be valid (no cycles, single root)
- Supports arbitrary tree structures
