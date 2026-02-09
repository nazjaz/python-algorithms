# API Documentation

## ArrayQueue Class

The array-based queue implementation using Python list.

### Methods

#### `__init__()`

Initialize empty queue.

**Example:**
```python
queue = ArrayQueue()
```

#### `enqueue(item: Any) -> None`

Add item to rear of queue.

**Parameters:**
- `item` (Any): Item to add to queue.

**Time Complexity:** O(1) amortized, O(n) worst case (list resizing)

**Example:**
```python
queue = ArrayQueue()
queue.enqueue(10)
queue.enqueue(20)
```

#### `dequeue() -> Any`

Remove and return item from front of queue.

**Returns:**
- `Any`: Item from front of queue.

**Raises:**
- `IndexError`: If queue is empty.

**Time Complexity:** O(n) - requires shifting all elements

**Example:**
```python
queue = ArrayQueue()
queue.enqueue(10)
queue.enqueue(20)
item = queue.dequeue()  # Returns 10
```

#### `front() -> Any`

Get front item without removing it.

**Returns:**
- `Any`: Item at front of queue.

**Raises:**
- `IndexError`: If queue is empty.

**Time Complexity:** O(1)

**Example:**
```python
queue = ArrayQueue()
queue.enqueue(10)
queue.enqueue(20)
item = queue.front()  # Returns 10, queue unchanged
```

#### `rear() -> Any`

Get rear item without removing it.

**Returns:**
- `Any`: Item at rear of queue.

**Raises:**
- `IndexError`: If queue is empty.

**Time Complexity:** O(1)

**Example:**
```python
queue = ArrayQueue()
queue.enqueue(10)
queue.enqueue(20)
item = queue.rear()  # Returns 20, queue unchanged
```

#### `is_empty() -> bool`

Check if queue is empty.

**Returns:**
- `bool`: True if queue is empty, False otherwise.

**Time Complexity:** O(1)

**Example:**
```python
queue = ArrayQueue()
if queue.is_empty():
    print("Queue is empty")
```

#### `size() -> int`

Get size of queue.

**Returns:**
- `int`: Number of items in queue.

**Time Complexity:** O(1)

**Example:**
```python
queue = ArrayQueue()
queue.enqueue(10)
queue.enqueue(20)
print(queue.size())  # 2
```

## LinkedListQueue Class

The linked list-based queue implementation.

### Methods

#### `__init__()`

Initialize empty queue.

**Example:**
```python
queue = LinkedListQueue()
```

#### `enqueue(item: Any) -> None`

Add item to rear of queue.

**Parameters:**
- `item` (Any): Item to add to queue.

**Time Complexity:** O(1) - constant time

**Example:**
```python
queue = LinkedListQueue()
queue.enqueue(10)
queue.enqueue(20)
```

#### `dequeue() -> Any`

Remove and return item from front of queue.

**Returns:**
- `Any`: Item from front of queue.

**Raises:**
- `IndexError`: If queue is empty.

**Time Complexity:** O(1) - constant time

**Example:**
```python
queue = LinkedListQueue()
queue.enqueue(10)
queue.enqueue(20)
item = queue.dequeue()  # Returns 10
```

#### `front() -> Any`

Get front item without removing it.

**Returns:**
- `Any`: Item at front of queue.

**Raises:**
- `IndexError`: If queue is empty.

**Time Complexity:** O(1)

**Example:**
```python
queue = LinkedListQueue()
queue.enqueue(10)
queue.enqueue(20)
item = queue.front()  # Returns 10, queue unchanged
```

#### `rear() -> Any`

Get rear item without removing it.

**Returns:**
- `Any`: Item at rear of queue.

**Raises:**
- `IndexError`: If queue is empty.

**Time Complexity:** O(1)

**Example:**
```python
queue = LinkedListQueue()
queue.enqueue(10)
queue.enqueue(20)
item = queue.rear()  # Returns 20, queue unchanged
```

#### `is_empty() -> bool`

Check if queue is empty.

**Returns:**
- `bool`: True if queue is empty, False otherwise.

**Time Complexity:** O(1)

**Example:**
```python
queue = LinkedListQueue()
if queue.is_empty():
    print("Queue is empty")
```

#### `size() -> int`

Get size of queue.

**Returns:**
- `int`: Number of items in queue.

**Time Complexity:** O(1)

**Example:**
```python
queue = LinkedListQueue()
queue.enqueue(10)
queue.enqueue(20)
print(queue.size())  # 2
```

## QueuePerformanceAnalyzer Class

The main class for analyzing performance of different queue implementations.

### Methods

#### `__init__(config_path: str = "config.yaml")`

Initialize the QueuePerformanceAnalyzer with configuration.

**Parameters:**
- `config_path` (str): Path to configuration YAML file. Defaults to "config.yaml".

**Raises:**
- `FileNotFoundError`: If config file doesn't exist.
- `yaml.YAMLError`: If config file is invalid YAML.

#### `compare_implementations(operations: List[str], iterations: int = 1) -> Dict[str, any]`

Compare performance of array and linked list queue implementations.

**Parameters:**
- `operations` (List[str]): List of operations to perform (format: "enqueue X" or "dequeue").
- `iterations` (int): Number of iterations for timing. Default: 1.

**Returns:**
- `Dict[str, any]`: Dictionary containing performance comparison data with keys:
  - `operations_count`: Number of operations
  - `iterations`: Number of iterations performed
  - `array_queue`: Dictionary with time and success status
  - `linked_list_queue`: Dictionary with time and success status
  - `fastest`: Name of fastest implementation (if both succeeded)
  - `fastest_time`: Time of fastest implementation
  - `speedup`: Speedup ratio (if both succeeded)

**Example:**
```python
analyzer = QueuePerformanceAnalyzer()
operations = ["enqueue 1", "enqueue 2", "dequeue"]
comparison = analyzer.compare_implementations(operations, iterations=100)
print(f"Fastest: {comparison['fastest']}")
```

#### `generate_report(comparison_data: Dict[str, any], output_path: Optional[str] = None) -> str`

Generate performance comparison report.

**Parameters:**
- `comparison_data` (Dict[str, any]): Performance comparison data from compare_implementations().
- `output_path` (Optional[str]): Optional path to save report file.

**Returns:**
- `str`: Report content as string.

**Example:**
```python
comparison = analyzer.compare_implementations(operations)
report = analyzer.generate_report(comparison, output_path="report.txt")
```

### Example Usage

```python
from src.main import ArrayQueue, LinkedListQueue, QueuePerformanceAnalyzer

# Array queue
array_queue = ArrayQueue()
array_queue.enqueue(10)
array_queue.enqueue(20)
print(array_queue.front())  # 10
print(array_queue.dequeue())  # 10

# Linked list queue
linked_queue = LinkedListQueue()
linked_queue.enqueue(10)
linked_queue.enqueue(20)
print(linked_queue.front())  # 10
print(linked_queue.dequeue())  # 10

# Performance comparison
analyzer = QueuePerformanceAnalyzer()
operations = ["enqueue 1", "enqueue 2", "dequeue", "enqueue 3"]
comparison = analyzer.compare_implementations(operations)
print(f"Fastest: {comparison['fastest']}")
```

### Algorithm Complexity Comparison

**Array Queue:**
- Enqueue: O(1) amortized, O(n) worst case
- Dequeue: O(n) - requires shifting
- Front/Rear: O(1)
- Space: O(n)

**Linked List Queue:**
- Enqueue: O(1) - constant time
- Dequeue: O(1) - constant time
- Front/Rear: O(1)
- Space: O(n) - one node per element

### Performance Notes

- Array queue has fast enqueue but slow dequeue
- Linked list queue has fast enqueue and dequeue
- Array queue is better for mostly enqueue operations
- Linked list queue is better for mixed operations
- Performance differences become noticeable with many operations
- Linked list has more memory overhead per element

### Edge Cases

- Empty queue: All operations check for empty queue
- Single element: Handled correctly in both implementations
- Large number of operations: Performance differences become significant
- Both implementations maintain FIFO behavior
