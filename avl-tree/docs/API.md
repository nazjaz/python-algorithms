# AVL Tree API Documentation

## AVLTree Class

Main class for AVL tree (self-balancing binary search tree) operations.

### Constructor

```python
AVLTree(config_path: str = "config.yaml") -> None
```

Initialize AVLTree with configuration.

**Parameters:**
- `config_path` (str): Path to configuration YAML file. Default: "config.yaml"

**Raises:**
- `FileNotFoundError`: If config file doesn't exist
- `yaml.YAMLError`: If config file is invalid YAML

### Methods

#### insert

```python
insert(key: float) -> None
```

Insert key into AVL tree.

**Parameters:**
- `key` (float): Key to insert

**Time Complexity:** O(log n) where n is number of nodes

**Example:**
```python
avl = AVLTree()
avl.insert(10)
avl.insert(20)
avl.insert(30)
```

#### delete

```python
delete(key: float) -> bool
```

Delete key from AVL tree.

**Parameters:**
- `key` (float): Key to delete

**Returns:**
- `bool`: True if key was deleted, False if not found

**Time Complexity:** O(log n) where n is number of nodes

**Example:**
```python
avl = AVLTree()
avl.insert(10)
avl.insert(20)
result = avl.delete(10)  # Returns True
```

#### search

```python
search(key: float) -> bool
```

Search for key in AVL tree.

**Parameters:**
- `key` (float): Key to search for

**Returns:**
- `bool`: True if key exists, False otherwise

**Time Complexity:** O(log n) where n is number of nodes

**Example:**
```python
avl = AVLTree()
avl.insert(10)
result = avl.search(10)  # Returns True
result = avl.search(20)  # Returns False
```

#### inorder_traversal

```python
inorder_traversal() -> List[float]
```

Get inorder traversal of tree.

**Returns:**
- `List[float]`: List of keys in inorder (sorted order)

**Time Complexity:** O(n) where n is number of nodes

**Example:**
```python
avl = AVLTree()
avl.insert(30)
avl.insert(10)
avl.insert(20)
inorder = avl.inorder_traversal()  # Returns [10, 20, 30]
```

#### preorder_traversal

```python
preorder_traversal() -> List[float]
```

Get preorder traversal of tree.

**Returns:**
- `List[float]`: List of keys in preorder

**Time Complexity:** O(n) where n is number of nodes

#### postorder_traversal

```python
postorder_traversal() -> List[float]
```

Get postorder traversal of tree.

**Returns:**
- `List[float]`: List of keys in postorder

**Time Complexity:** O(n) where n is number of nodes

#### get_height

```python
get_height() -> int
```

Get height of tree.

**Returns:**
- `int`: Height of tree

**Time Complexity:** O(1)

**Example:**
```python
avl = AVLTree()
avl.insert(10)
height = avl.get_height()  # Returns 1
```

#### is_balanced

```python
is_balanced() -> bool
```

Check if tree is balanced.

**Returns:**
- `bool`: True if tree is balanced, False otherwise

**Time Complexity:** O(n) where n is number of nodes

**Example:**
```python
avl = AVLTree()
avl.insert(10)
avl.insert(20)
avl.insert(30)
balanced = avl.is_balanced()  # Returns True
```

#### build_from_list

```python
build_from_list(keys: List[float]) -> None
```

Build AVL tree from list of keys.

**Parameters:**
- `keys` (List[float]): List of keys to insert

**Time Complexity:** O(n log n) where n is number of keys

**Example:**
```python
avl = AVLTree()
keys = [10, 20, 30, 40, 50]
avl.build_from_list(keys)
```

#### compare_performance

```python
compare_performance(
    keys: List[float],
    search_keys: List[float],
    iterations: int = 1
) -> Dict[str, any]
```

Compare performance of AVL tree operations.

**Parameters:**
- `keys` (List[float]): List of keys to insert
- `search_keys` (List[float]): List of keys to search for
- `iterations` (int): Number of iterations for timing. Default: 1

**Returns:**
- `Dict[str, any]`: Dictionary containing performance data for insert, search, and delete operations

**Example:**
```python
avl = AVLTree()
keys = [10, 20, 30, 40, 50]
search_keys = [10, 20, 30]
performance = avl.compare_performance(keys, search_keys, iterations=1000)
print(performance["insert"]["time_milliseconds"])
```

#### generate_report

```python
generate_report(
    performance_data: Dict[str, any],
    output_path: Optional[str] = None
) -> str
```

Generate performance report for AVL tree operations.

**Parameters:**
- `performance_data` (Dict[str, any]): Performance data from compare_performance()
- `output_path` (Optional[str]): Optional path to save report file

**Returns:**
- `str`: Report content as string

**Raises:**
- `IOError`: If file cannot be written
- `PermissionError`: If file is not writable

## AVLNode Class

Node in AVL tree.

### Constructor

```python
AVLNode(key: float) -> None
```

Initialize AVLNode.

**Parameters:**
- `key` (float): Node key value

### Properties

- `key`: Node key value
- `left`: Left child node
- `right`: Right child node
- `height`: Height of node

## Command-Line Interface

The module can be run as a script with the following interface:

```bash
python src/main.py KEYS [OPTIONS]
```

### Arguments

- `KEYS`: (Required) Keys to insert into AVL tree (space-separated)

### Options

- `-c, --config`: Path to configuration file (default: config.yaml)
- `-o, --operation`: Operation to perform - insert, search, delete, traverse, compare, or all (default: all)
- `-k, --key`: Key for search or delete operation
- `-t, --traversal`: Traversal type - inorder, preorder, or postorder (default: inorder)
- `-i, --iterations`: Number of iterations for timing (default: 1)
- `-r, --report`: Output path for performance report

### Examples

```bash
# Insert keys
python src/main.py 10 20 30 40 50 --operation insert

# Search for key
python src/main.py 10 20 30 40 50 --operation search --key 30

# Delete key
python src/main.py 10 20 30 40 50 --operation delete --key 30

# Traverse tree
python src/main.py 10 20 30 40 50 --operation traverse --traversal inorder

# Compare performance
python src/main.py 10 20 30 40 50 --operation compare --report report.txt
```

## Error Handling

All methods handle edge cases gracefully:

- Empty tree returns height 0
- Duplicate keys are not inserted
- Searching in empty tree returns False
- Deleting from empty tree returns False
- Tree remains balanced after all operations

## Algorithm Complexity

### AVL Tree Operations

- **Insert**: O(log n) where n is number of nodes
- **Delete**: O(log n) where n is number of nodes
- **Search**: O(log n) where n is number of nodes
- **Traversal**: O(n) where n is number of nodes
- **Space Complexity**: O(n) for storing nodes

### Rotation Operations

- **Left Rotation**: O(1)
- **Right Rotation**: O(1)
- **Left-Right Rotation**: O(1)
- **Right-Left Rotation**: O(1)

## Notes

- AVL tree maintains balance automatically
- Height difference between subtrees is at most 1
- All operations are O(log n) guaranteed
- Inorder traversal gives sorted order
- Duplicate keys are not inserted
- Tree remains balanced after insertions and deletions
- Rotations maintain BST property
- Balance factor = height(left) - height(right)
- Tree height is O(log n) where n is number of nodes
- More balanced than regular BST
- Better worst-case performance than BST
