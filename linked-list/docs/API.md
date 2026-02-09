# Linked List API Documentation

## Overview

The Linked List implementation provides a complete singly linked list data structure with insertion, deletion, and traversal operations. It includes visualization capabilities to show the structure and operations of the linked list.

## Classes

### Node

Node class for linked list elements.

#### Constructor

```python
Node(data: Any) -> None
```

Initialize node with data.

**Parameters:**
- `data` (Any): Data to store in node

### LinkedList

Main linked list implementation.

#### Constructor

```python
LinkedList() -> None
```

Initialize empty linked list.

#### Methods

##### insert_at_beginning

```python
insert_at_beginning(data: Any) -> None
```

Insert node at the beginning of the list.

**Parameters:**
- `data` (Any): Data to insert

**Time Complexity:** O(1)

##### insert_at_end

```python
insert_at_end(data: Any) -> None
```

Insert node at the end of the list.

**Parameters:**
- `data` (Any): Data to insert

**Time Complexity:** O(n)

##### insert_at_position

```python
insert_at_position(data: Any, position: int) -> bool
```

Insert node at a specific position.

**Parameters:**
- `data` (Any): Data to insert
- `position` (int): Position to insert at (0-indexed)

**Returns:**
- `bool`: True if insertion successful, False otherwise

**Time Complexity:** O(n)

##### delete_at_beginning

```python
delete_at_beginning() -> Optional[Any]
```

Delete node at the beginning of the list.

**Returns:**
- `Optional[Any]`: Data of deleted node, or None if list is empty

**Time Complexity:** O(1)

##### delete_at_end

```python
delete_at_end() -> Optional[Any]
```

Delete node at the end of the list.

**Returns:**
- `Optional[Any]`: Data of deleted node, or None if list is empty

**Time Complexity:** O(n)

##### delete_at_position

```python
delete_at_position(position: int) -> Optional[Any]
```

Delete node at a specific position.

**Parameters:**
- `position` (int): Position to delete from (0-indexed)

**Returns:**
- `Optional[Any]`: Data of deleted node, or None if deletion failed

**Time Complexity:** O(n)

##### delete_by_value

```python
delete_by_value(value: Any) -> bool
```

Delete first node with given value.

**Parameters:**
- `value` (Any): Value to delete

**Returns:**
- `bool`: True if deletion successful, False otherwise

**Time Complexity:** O(n)

##### search

```python
search(value: Any) -> Optional[int]
```

Search for a value in the list.

**Parameters:**
- `value` (Any): Value to search for

**Returns:**
- `Optional[int]`: Position of value if found, None otherwise

**Time Complexity:** O(n)

##### traverse

```python
traverse() -> List[Any]
```

Traverse the linked list and return all values.

**Returns:**
- `List[Any]`: List of all values in the linked list

**Time Complexity:** O(n)

##### visualize

```python
visualize() -> str
```

Generate visual representation of the linked list.

**Returns:**
- `str`: String representation of the linked list structure

##### reverse

```python
reverse() -> None
```

Reverse the linked list in-place.

**Time Complexity:** O(n)

### LinkedListVisualizer

Visualizer for linked list operations with history tracking.

#### Constructor

```python
LinkedListVisualizer(config_path: str = "config.yaml") -> None
```

Initialize visualizer with configuration.

## Usage Examples

### Basic Operations

```python
from src.main import LinkedList

ll = LinkedList()
ll.insert_at_end(10)
ll.insert_at_end(20)
ll.insert_at_end(30)
print(ll.traverse())  # [10, 20, 30]
```

### Visualization

```python
ll = LinkedList()
ll.insert_at_end(10)
ll.insert_at_end(20)
print(ll.visualize())
```

### With Visualizer

```python
from src.main import LinkedListVisualizer

visualizer = LinkedListVisualizer()
visualizer.insert_at_end(10)
visualizer.insert_at_end(20)
visualizer.print_visualization()
```
