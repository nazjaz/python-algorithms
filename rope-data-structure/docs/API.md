# Rope Data Structure API Documentation

This document provides detailed API documentation for the rope data structure implementation with efficient string concatenation and substring operations.

## Classes

### RopeNode

Node in rope tree structure.

#### Attributes

- `data` (Optional[str]): String data (for leaf nodes)
- `left` (Optional[RopeNode]): Left child node
- `right` (Optional[RopeNode]): Right child node
- `weight` (int): Weight (length of left subtree)
- `length` (int): Total length of subtree

#### Methods

##### `__init__(data: Optional[str] = None, left: Optional[RopeNode] = None, right: Optional[RopeNode] = None, weight: int = 0) -> None`

Initialize rope node.

**Parameters:**
- `data`: String data (for leaf nodes)
- `left`: Left child node
- `right`: Right child node
- `weight`: Weight (length of left subtree)

**Example:**
```python
node = RopeNode(data="hello")
```

##### `is_leaf() -> bool`

Check if node is a leaf.

**Returns:**
- `True` if leaf, `False` otherwise

**Example:**
```python
if node.is_leaf():
    print("Node is a leaf")
```

##### `update_weight() -> None`

Update weight based on left subtree.

**Example:**
```python
node.update_weight()
```

### Rope

Main class for rope data structure.

#### Methods

##### `__init__(initial_string: str = "", config_path: str = "config.yaml") -> None`

Initialize rope.

**Parameters:**
- `initial_string`: Initial string
- `config_path`: Path to configuration YAML file (default: "config.yaml")

**Example:**
```python
rope = Rope("Hello World")
```

##### `concatenate(other: Rope) -> Rope`

Concatenate this rope with another rope.

**Parameters:**
- `other`: Other rope to concatenate

**Returns:**
- New rope containing concatenated result

**Time Complexity:** O(log n)

**Example:**
```python
rope1 = Rope("Hello")
rope2 = Rope(" World")
rope3 = rope1.concatenate(rope2)
```

##### `substring(start: int, end: int) -> Rope`

Extract substring from rope.

**Parameters:**
- `start`: Start index (inclusive)
- `end`: End index (exclusive)

**Returns:**
- New rope containing substring

**Raises:**
- `IndexError`: If indices are invalid

**Time Complexity:** O(log n + m) where m is substring length

**Example:**
```python
substr = rope.substring(0, 5)
```

##### `insert(index: int, string: str) -> Rope`

Insert string at index.

**Parameters:**
- `index`: Insertion index
- `string`: String to insert

**Returns:**
- New rope with inserted string

**Raises:**
- `IndexError`: If index is invalid

**Time Complexity:** O(log n)

**Example:**
```python
new_rope = rope.insert(5, " Beautiful")
```

##### `delete(start: int, end: int) -> Rope`

Delete substring from rope.

**Parameters:**
- `start`: Start index (inclusive)
- `end`: End index (exclusive)

**Returns:**
- New rope with deleted substring

**Raises:**
- `IndexError`: If indices are invalid

**Time Complexity:** O(log n)

**Example:**
```python
new_rope = rope.delete(5, 11)
```

##### `get_char(index: int) -> str`

Get character at index.

**Parameters:**
- `index`: Character index

**Returns:**
- Character at index

**Raises:**
- `IndexError`: If index is invalid

**Time Complexity:** O(log n)

**Example:**
```python
char = rope.get_char(0)
```

##### `get_length() -> int`

Get length of rope.

**Returns:**
- Length of rope

**Time Complexity:** O(1)

**Example:**
```python
length = rope.get_length()
```

##### `to_string() -> str`

Convert rope to string.

**Returns:**
- String representation of rope

**Time Complexity:** O(n)

**Example:**
```python
string = rope.to_string()
```

## Usage Examples

### Basic Operations

```python
from src.main import Rope

# Create ropes
rope1 = Rope("Hello")
rope2 = Rope(" World")

# Concatenate
rope3 = rope1.concatenate(rope2)
print(rope3.to_string())  # "Hello World"

# Get length
length = rope3.get_length()  # 11

# Get character
char = rope3.get_char(0)  # "H"
```

### Substring Operations

```python
from src.main import Rope

rope = Rope("Hello World")

# Extract substring
substr = rope.substring(0, 5)
print(substr.to_string())  # "Hello"

substr = rope.substring(6, 11)
print(substr.to_string())  # "World"
```

### Insert and Delete Operations

```python
from src.main import Rope

rope = Rope("Hello World")

# Insert string
new_rope = rope.insert(5, " Beautiful")
print(new_rope.to_string())  # "Hello Beautiful World"

# Delete substring
new_rope = new_rope.delete(5, 15)
print(new_rope.to_string())  # "Hello World"
```

### Complex Operations

```python
from src.main import Rope

# Create and concatenate multiple ropes
rope = Rope("A")
rope = rope.concatenate(Rope("B"))
rope = rope.concatenate(Rope("C"))
print(rope.to_string())  # "ABC"

# Insert and delete
rope = rope.insert(1, "X")
print(rope.to_string())  # "AXBC"

rope = rope.delete(1, 2)
print(rope.to_string())  # "ABC"
```

### Error Handling

```python
from src.main import Rope

rope = Rope("Hello World")

# Invalid index
try:
    rope.get_char(-1)
except IndexError as e:
    print(f"Error: {e}")

# Invalid substring range
try:
    rope.substring(5, 3)
except IndexError as e:
    print(f"Error: {e}")

# Out of bounds
try:
    rope.insert(100, "test")
except IndexError as e:
    print(f"Error: {e}")
```

## Time Complexity Summary

| Operation | Time Complexity |
|-----------|----------------|
| `concatenate` | O(log n) |
| `substring` | O(log n + m) |
| `insert` | O(log n) |
| `delete` | O(log n) |
| `get_char` | O(log n) |
| `get_length` | O(1) |
| `to_string` | O(n) |

Where n is the length of the rope and m is the length of the substring.

## Notes

- Rope operations are immutable (create new ropes)
- Original ropes remain unchanged after operations
- Efficient for large strings and frequent operations
- Tree structure enables O(log n) operations
- Leaf nodes contain actual string data
- Internal nodes store weights for navigation
