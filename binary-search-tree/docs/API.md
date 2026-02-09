# Binary Search Tree API Documentation

## Overview

The Binary Search Tree implementation provides both unbalanced BST and balanced AVL tree implementations with performance analysis capabilities. It demonstrates the importance of tree balancing for optimal performance.

## Classes

### BSTNode

Node class for binary search tree.

#### Constructor

```python
BSTNode(value: Any) -> None
```

Initialize BST node.

**Parameters:**
- `value` (Any): Value stored in the node

### BST

Binary Search Tree (unbalanced) implementation.

#### Constructor

```python
BST(config_path: str = "config.yaml") -> None
```

Initialize BST with configuration.

#### Methods

##### insert

```python
insert(value: Any) -> bool
```

Insert value into BST.

**Parameters:**
- `value` (Any): Value to insert

**Returns:**
- `bool`: True if inserted, False if duplicate

**Time Complexity:** O(n) worst case, O(log n) average case

##### search

```python
search(value: Any) -> bool
```

Search for value in BST.

**Parameters:**
- `value` (Any): Value to search for

**Returns:**
- `bool`: True if found, False otherwise

**Time Complexity:** O(n) worst case, O(log n) average case

##### delete

```python
delete(value: Any) -> bool
```

Delete value from BST.

**Parameters:**
- `value` (Any): Value to delete

**Returns:**
- `bool`: True if deleted, False if not found

**Time Complexity:** O(n) worst case, O(log n) average case

##### inorder_traversal

```python
inorder_traversal() -> List[Any]
```

Perform inorder traversal (produces sorted order).

**Returns:**
- `List[Any]`: List of values in sorted order

**Time Complexity:** O(n)

##### get_statistics

```python
get_statistics() -> Dict[str, Any]
```

Get performance statistics.

**Returns:**
- `Dict[str, Any]`: Dictionary with performance statistics

### AVLTree

AVL Tree (self-balancing BST) implementation.

#### Constructor

```python
AVLTree(config_path: str = "config.yaml") -> None
```

Initialize AVL tree with configuration.

#### Methods

##### insert

```python
insert(value: Any) -> bool
```

Insert value into AVL tree with automatic balancing.

**Parameters:**
- `value` (Any): Value to insert

**Returns:**
- `bool`: True if inserted, False if duplicate

**Time Complexity:** O(log n) guaranteed

##### search

```python
search(value: Any) -> bool
```

Search for value in AVL tree.

**Parameters:**
- `value` (Any): Value to search for

**Returns:**
- `bool`: True if found, False otherwise

**Time Complexity:** O(log n) guaranteed

##### delete

```python
delete(value: Any) -> bool
```

Delete value from AVL tree with automatic balancing.

**Parameters:**
- `value` (Any): Value to delete

**Returns:**
- `bool`: True if deleted, False if not found

**Time Complexity:** O(log n) guaranteed

##### get_statistics

```python
get_statistics() -> Dict[str, Any]
```

Get performance statistics including rotations.

**Returns:**
- `Dict[str, Any]`: Dictionary with performance statistics

### PerformanceAnalyzer

Performance analyzer for comparing BST vs AVL Tree.

#### Methods

##### compare_trees

```python
compare_trees(
    values: List[Any], search_values: Optional[List[Any]] = None
) -> Dict[str, Any]
```

Compare performance of BST vs AVL Tree.

**Parameters:**
- `values` (List[Any]): Values to insert into both trees
- `search_values` (Optional[List[Any]]): Optional values to search for

**Returns:**
- `Dict[str, Any]`: Dictionary with comparison results

##### generate_report

```python
generate_report(output_path: Optional[str] = None) -> str
```

Generate performance analysis report.

**Parameters:**
- `output_path` (Optional[str]): Optional path to save report

**Returns:**
- `str`: Report content as string

## Usage Examples

### Basic BST Operations

```python
from src.main import BST

bst = BST()
bst.insert(10)
bst.insert(5)
bst.insert(15)

found = bst.search(5)  # True
bst.delete(5)
inorder = bst.inorder_traversal()  # [10, 15]
```

### AVL Tree Operations

```python
from src.main import AVLTree

avl = AVLTree()
avl.insert(10)
avl.insert(5)
avl.insert(15)

found = avl.search(5)  # True
stats = avl.get_statistics()
print(stats["rotations"])  # Number of rotations performed
```

### Performance Comparison

```python
from src.main import PerformanceAnalyzer

analyzer = PerformanceAnalyzer()
values = [50, 30, 70, 20, 40, 60, 80]
search_values = [20, 50, 80]

results = analyzer.compare_trees(values, search_values)
print(f"BST Height: {results['bst']['height']}")
print(f"AVL Height: {results['avl']['height']}")

report = analyzer.generate_report(output_path="report.txt")
```
