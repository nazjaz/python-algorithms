# LCA Algorithms API Documentation

This document provides detailed API documentation for the LCA (Lowest Common Ancestor) algorithms implementation using binary lifting and Euler tour techniques.

## Classes

### TreeNode

Node in a tree.

#### Attributes

- `value` (int): Node value
- `children` (List[TreeNode]): List of child nodes
- `parent` (Optional[TreeNode]): Parent node

#### Methods

##### `__init__(value: int) -> None`

Initialize tree node.

**Parameters:**
- `value`: Node value

**Example:**
```python
node = TreeNode(5)
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

### LCABinaryLifting

LCA using binary lifting technique.

#### Methods

##### `__init__(root: TreeNode, config_path: str = "config.yaml") -> None`

Initialize LCA with binary lifting.

**Parameters:**
- `root`: Root of the tree
- `config_path`: Path to configuration YAML file (default: "config.yaml")

**Time Complexity:** O(n log n) preprocessing

**Example:**
```python
root = TreeNode(0)
lca = LCABinaryLifting(root)
```

##### `lca(u: TreeNode, v: TreeNode) -> Optional[TreeNode]`

Find lowest common ancestor of two nodes.

**Parameters:**
- `u`: First node
- `v`: Second node

**Returns:**
- LCA node or None if nodes not in tree

**Time Complexity:** O(log n)

**Example:**
```python
result = lca.lca(node1, node2)
if result:
    print(f"LCA: {result.value}")
```

### LCAEulerTour

LCA using Euler tour technique.

#### Methods

##### `__init__(root: TreeNode, config_path: str = "config.yaml") -> None`

Initialize LCA with Euler tour.

**Parameters:**
- `root`: Root of the tree
- `config_path`: Path to configuration YAML file (default: "config.yaml")

**Time Complexity:** O(n log n) preprocessing

**Example:**
```python
root = TreeNode(0)
lca = LCAEulerTour(root)
```

##### `lca(u: TreeNode, v: TreeNode) -> Optional[TreeNode]`

Find lowest common ancestor of two nodes.

**Parameters:**
- `u`: First node
- `v`: Second node

**Returns:**
- LCA node or None if nodes not in tree

**Time Complexity:** O(log n)

**Example:**
```python
result = lca.lca(node1, node2)
if result:
    print(f"LCA: {result.value}")
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

### Basic LCA Query

```python
from src.main import TreeNode, LCABinaryLifting

# Build tree
root = TreeNode(0)
node1 = TreeNode(1)
node2 = TreeNode(2)
node3 = TreeNode(3)
root.add_child(node1)
root.add_child(node2)
node1.add_child(node3)

# Create LCA structure
lca = LCABinaryLifting(root)

# Query LCA
result = lca.lca(node2, node3)
print(f"LCA: {result.value}")  # Output: 0
```

### Building Tree from Edges

```python
from src.main import build_tree_from_edges, LCABinaryLifting

# Build tree from edges
n = 7
edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)]
root = build_tree_from_edges(n, edges, 0)

# Create LCA structure
lca = LCABinaryLifting(root)

# Get nodes
node3 = root.children[0].children[0]
node4 = root.children[0].children[1]

# Query LCA
result = lca.lca(node3, node4)
print(f"LCA: {result.value}")  # Output: 1
```

### Comparing Both Algorithms

```python
from src.main import TreeNode, LCABinaryLifting, LCAEulerTour

# Build tree
root = TreeNode(0)
node1 = TreeNode(1)
node2 = TreeNode(2)
root.add_child(node1)
root.add_child(node2)

# Create both LCA structures
lca_bl = LCABinaryLifting(root)
lca_et = LCAEulerTour(root)

# Query with both
result_bl = lca_bl.lca(node1, node2)
result_et = lca_et.lca(node1, node2)

# Both should give same result
assert result_bl.value == result_et.value
print(f"LCA: {result_bl.value}")
```

### Error Handling

```python
from src.main import TreeNode, LCABinaryLifting, build_tree_from_edges

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

# Query with invalid node
root = TreeNode(0)
lca = LCABinaryLifting(root)
invalid_node = TreeNode(99)
result = lca.lca(root, invalid_node)
assert result is None
```

### Complex Tree Example

```python
from src.main import TreeNode, LCABinaryLifting

# Build complex tree
root = TreeNode(0)
nodes = [root]

# Create binary tree structure
for i in range(1, 15):
    parent_idx = (i - 1) // 2
    node = TreeNode(i)
    nodes[parent_idx].add_child(node)
    nodes.append(node)

# Create LCA structure
lca = LCABinaryLifting(root)

# Query LCA of distant nodes
result = lca.lca(nodes[10], nodes[14])
print(f"LCA of nodes 10 and 14: {result.value}")
```

## Time Complexity Summary

| Operation | Binary Lifting | Euler Tour |
|-----------|----------------|------------|
| Preprocessing | O(n log n) | O(n log n) |
| Query | O(log n) | O(log n) |
| Space | O(n log n) | O(n log n) |

Where n is the number of nodes in the tree.

## Notes

- Both algorithms require preprocessing before queries
- Preprocessing is done automatically in constructor
- Both algorithms give same results for same queries
- Nodes must be in the tree for queries to work
- Tree structure should be valid (no cycles, single root)
- Both algorithms support arbitrary tree structures
