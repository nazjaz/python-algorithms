# Link-Cut Tree API Documentation

This document provides detailed API documentation for the link-cut tree implementation with dynamic forest maintenance and link/cut operations.

## Classes

### LinkCutNode

Node in link-cut tree.

#### Attributes

- `value` (int): Node value/identifier
- `data` (float): Data stored in node
- `path_parent` (Optional[LinkCutNode]): Path parent pointer
- `left` (Optional[LinkCutNode]): Left child in splay tree
- `right` (Optional[LinkCutNode]): Right child in splay tree
- `parent` (Optional[LinkCutNode]): Parent in splay tree
- `reversed` (bool): Reverse flag for lazy propagation

#### Methods

##### `is_root() -> bool`

Check if node is root of its splay tree.

**Returns:**
- `True` if root, `False` otherwise

**Example:**
```python
node = LinkCutNode(1)
assert node.is_root() is True
```

### LinkCutTree

Main class for link-cut tree data structure.

#### Methods

##### `__init__(config_path: str = "config.yaml") -> None`

Initialize link-cut tree.

**Parameters:**
- `config_path`: Path to configuration YAML file (default: "config.yaml")

**Example:**
```python
tree = LinkCutTree()
```

##### `create_node(value: int, data: float = 0.0) -> LinkCutNode`

Create a new node.

**Parameters:**
- `value`: Node value
- `data`: Node data (default: 0.0)

**Returns:**
- Created node

**Example:**
```python
node = tree.create_node(5, data=10.0)
```

##### `link(child: LinkCutNode, parent: LinkCutNode) -> bool`

Link child to parent.

**Parameters:**
- `child`: Child node
- `parent`: Parent node

**Returns:**
- `True` if linked, `False` if already connected

**Time Complexity:** O(log n) amortized

**Example:**
```python
result = tree.link(node1, node0)
if result:
    print("Linked successfully")
```

##### `cut(node: LinkCutNode) -> bool`

Cut edge from node to its parent.

**Parameters:**
- `node`: Node to cut from parent

**Returns:**
- `True` if cut, `False` if node is root

**Time Complexity:** O(log n) amortized

**Example:**
```python
result = tree.cut(node1)
if result:
    print("Cut successfully")
```

##### `find_root(node: LinkCutNode) -> LinkCutNode`

Find root of tree containing node.

**Parameters:**
- `node`: Node to find root for

**Returns:**
- Root node

**Time Complexity:** O(log n) amortized

**Example:**
```python
root = tree.find_root(node1)
print(f"Root: {root.value}")
```

##### `path_query(u: LinkCutNode, v: LinkCutNode) -> float`

Query path from u to v.

**Parameters:**
- `u`: First node
- `v`: Second node

**Returns:**
- Sum of data along path (0.0 if not connected)

**Time Complexity:** O(log n) amortized

**Example:**
```python
result = tree.path_query(node1, node2)
print(f"Path sum: {result}")
```

##### `path_update(u: LinkCutNode, v: LinkCutNode, value: float) -> None`

Update path from u to v by adding value.

**Parameters:**
- `u`: First node
- `v`: Second node
- `value`: Value to add

**Time Complexity:** O(log n) amortized

**Example:**
```python
tree.path_update(node1, node2, 10.0)
```

##### `are_connected(u: LinkCutNode, v: LinkCutNode) -> bool`

Check if two nodes are in same tree.

**Parameters:**
- `u`: First node
- `v`: Second node

**Returns:**
- `True` if connected, `False` otherwise

**Time Complexity:** O(log n) amortized

**Example:**
```python
connected = tree.are_connected(node1, node2)
if connected:
    print("Nodes are connected")
```

##### `get_path_nodes(u: LinkCutNode, v: LinkCutNode) -> List[LinkCutNode]`

Get all nodes on path from u to v.

**Parameters:**
- `u`: First node
- `v`: Second node

**Returns:**
- List of nodes on path

**Example:**
```python
path = tree.get_path_nodes(node1, node2)
for node in path:
    print(node.value)
```

## Usage Examples

### Basic Operations

```python
from src.main import LinkCutTree

# Create link-cut tree
tree = LinkCutTree()

# Create nodes
node0 = tree.create_node(0, data=1.0)
node1 = tree.create_node(1, data=2.0)
node2 = tree.create_node(2, data=3.0)

# Link nodes
tree.link(node1, node0)
tree.link(node2, node0)

# Find root
root = tree.find_root(node1)
print(f"Root: {root.value}")

# Check connectivity
connected = tree.are_connected(node1, node2)
print(f"Connected: {connected}")

# Path query
result = tree.path_query(node1, node2)
print(f"Path sum: {result}")

# Cut edge
tree.cut(node1)
```

### Dynamic Forest Maintenance

```python
from src.main import LinkCutTree

tree = LinkCutTree()
nodes = [tree.create_node(i) for i in range(5)]

# Create two separate trees
tree.link(nodes[1], nodes[0])
tree.link(nodes[2], nodes[0])
tree.link(nodes[4], nodes[3])

# Check connectivity
assert tree.are_connected(nodes[0], nodes[1]) is True
assert tree.are_connected(nodes[3], nodes[4]) is True
assert tree.are_connected(nodes[0], nodes[3]) is False

# Merge trees
tree.link(nodes[0], nodes[3])
assert tree.are_connected(nodes[0], nodes[3]) is True

# Split tree
tree.cut(nodes[1])
assert tree.are_connected(nodes[0], nodes[1]) is False
```

### Path Operations

```python
from src.main import LinkCutTree

tree = LinkCutTree()
nodes = [tree.create_node(i, data=float(i)) for i in range(5)]

# Build tree
tree.link(nodes[1], nodes[0])
tree.link(nodes[2], nodes[0])
tree.link(nodes[3], nodes[1])
tree.link(nodes[4], nodes[1])

# Path query
result = tree.path_query(nodes[3], nodes[2])
print(f"Path sum: {result}")

# Path update
tree.path_update(nodes[3], nodes[2], 10.0)

# Query after update
result = tree.path_query(nodes[3], nodes[2])
print(f"Path sum after update: {result}")
```

### Error Handling

```python
from src.main import LinkCutTree

tree = LinkCutTree()
node0 = tree.create_node(0)
node1 = tree.create_node(1)

# Link nodes
tree.link(node1, node0)

# Try to link again (already connected)
result = tree.link(node0, node1)
if not result:
    print("Nodes already connected")

# Try to cut root
result = tree.cut(node0)
if not result:
    print("Cannot cut root node")

# Path query on disconnected nodes
tree.cut(node1)
result = tree.path_query(node0, node1)
print(f"Path query result: {result}")  # 0.0
```

## Time Complexity Summary

| Operation | Amortized | Worst Case |
|-----------|-----------|------------|
| `create_node` | O(1) | O(1) |
| `link` | O(log n) | O(n) |
| `cut` | O(log n) | O(n) |
| `find_root` | O(log n) | O(n) |
| `path_query` | O(log n) | O(n) |
| `path_update` | O(log n) | O(n) |
| `are_connected` | O(log n) | O(n) |
| `get_path_nodes` | O(log n) | O(n) |

Where n is the number of nodes in the forest.

## Notes

- Link-cut trees maintain a forest of trees
- All operations have O(log n) amortized time complexity
- Individual operations may have O(n) worst-case time
- Nodes must be in same tree for path operations
- Link operation requires nodes in different trees
- Cut operation requires node to have a parent
- Splay trees are used internally for efficient operations
