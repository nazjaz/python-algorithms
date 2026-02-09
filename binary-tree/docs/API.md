# Binary Tree API Documentation

## Overview

The Binary Tree implementation provides a complete binary tree data structure with insertion, deletion, and three traversal methods: inorder, preorder, and postorder. The tree maintains the property that each node has at most two children.

## Classes

### TreeNode

Node class for binary tree.

#### Constructor

```python
TreeNode(value: Any) -> None
```

Initialize tree node.

**Parameters:**
- `value` (Any): Value stored in the node

### BinaryTree

Binary tree data structure with insertion, deletion, and traversal methods.

#### Constructor

```python
BinaryTree(config_path: str = "config.yaml") -> None
```

Initialize binary tree with configuration.

#### Methods

##### insert

```python
insert(value: Any) -> None
```

Insert value into binary tree using level-order insertion.

**Parameters:**
- `value` (Any): Value to insert

**Time Complexity:** O(n) where n is number of nodes
**Space Complexity:** O(n) for queue

##### delete

```python
delete(value: Any) -> bool
```

Delete value from binary tree.

**Parameters:**
- `value` (Any): Value to delete

**Returns:**
- `bool`: True if value was found and deleted, False otherwise

**Time Complexity:** O(n)
**Space Complexity:** O(n)

##### search

```python
search(value: Any) -> bool
```

Search for value in binary tree.

**Parameters:**
- `value` (Any): Value to search for

**Returns:**
- `bool`: True if value found, False otherwise

**Time Complexity:** O(n)
**Space Complexity:** O(n)

##### inorder_traversal

```python
inorder_traversal() -> List[Any]
```

Perform inorder traversal (Left, Root, Right).

**Returns:**
- `List[Any]`: List of values in inorder traversal order

**Time Complexity:** O(n)
**Space Complexity:** O(h) where h is height (recursion stack)

##### preorder_traversal

```python
preorder_traversal() -> List[Any]
```

Perform preorder traversal (Root, Left, Right).

**Returns:**
- `List[Any]`: List of values in preorder traversal order

**Time Complexity:** O(n)
**Space Complexity:** O(h)

##### postorder_traversal

```python
postorder_traversal() -> List[Any]
```

Perform postorder traversal (Left, Right, Root).

**Returns:**
- `List[Any]`: List of values in postorder traversal order

**Time Complexity:** O(n)
**Space Complexity:** O(h)

##### level_order_traversal

```python
level_order_traversal() -> List[Any]
```

Perform level-order traversal (breadth-first).

**Returns:**
- `List[Any]`: List of values in level-order traversal order

**Time Complexity:** O(n)
**Space Complexity:** O(n)

##### height

```python
height() -> int
```

Calculate height of binary tree.

**Returns:**
- `int`: Height of tree (number of edges in longest path from root to leaf)

**Time Complexity:** O(n)
**Space Complexity:** O(h)

##### size

```python
size() -> int
```

Calculate number of nodes in binary tree.

**Returns:**
- `int`: Number of nodes in tree

**Time Complexity:** O(n)
**Space Complexity:** O(h)

## Usage Examples

### Basic Operations

```python
from src.main import BinaryTree

tree = BinaryTree()

# Insert values
tree.insert(10)
tree.insert(5)
tree.insert(15)

# Search
found = tree.search(5)  # True

# Traversals
inorder = tree.inorder_traversal()  # [5, 10, 15]
preorder = tree.preorder_traversal()  # [10, 5, 15]
postorder = tree.postorder_traversal()  # [5, 15, 10]

# Delete
tree.delete(5)  # True
```

### Tree Properties

```python
tree = BinaryTree()
tree.insert(10)
tree.insert(5)
tree.insert(15)

size = tree.size()  # 3
height = tree.height()  # 1
```

## Traversal Order

### Inorder (Left, Root, Right)
- Visit left subtree
- Visit root
- Visit right subtree
- For BST: produces sorted order

### Preorder (Root, Left, Right)
- Visit root
- Visit left subtree
- Visit right subtree
- Useful for copying tree structure

### Postorder (Left, Right, Root)
- Visit left subtree
- Visit right subtree
- Visit root
- Useful for deleting tree

### Level-order (Breadth-first)
- Visit nodes level by level
- Left to right at each level
- Uses queue data structure
