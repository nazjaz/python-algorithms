# Heap Data Structure API Documentation

## MinHeap Class

Min-heap implementation where parent nodes are always smaller than or equal to their children. The minimum element is always at the root.

### Constructor

```python
MinHeap(items: Optional[List[T]] = None) -> None
```

Initialize MinHeap.

**Parameters:**
- `items` (Optional[List[T]]): Optional list of items to build heap from

**Example:**
```python
heap = MinHeap([5, 2, 8, 1, 9, 3])
```

### Methods

#### insert

```python
insert(item: T) -> None
```

Insert item into heap.

**Parameters:**
- `item` (T): Item to insert

**Time Complexity:** O(log n)

**Example:**
```python
heap = MinHeap()
heap.insert(5)
heap.insert(2)
heap.insert(8)
```

#### extract_min

```python
extract_min() -> Optional[T]
```

Extract and return minimum element.

**Returns:**
- `Optional[T]`: Minimum element, or None if heap is empty

**Time Complexity:** O(log n)

**Example:**
```python
heap = MinHeap([5, 2, 8, 1, 9, 3])
min_val = heap.extract_min()  # Returns 1
```

#### peek

```python
peek() -> Optional[T]
```

Peek at minimum element without removing it.

**Returns:**
- `Optional[T]`: Minimum element, or None if heap is empty

**Time Complexity:** O(1)

**Example:**
```python
heap = MinHeap([5, 2, 8, 1, 9, 3])
min_val = heap.peek()  # Returns 1, heap unchanged
```

#### build_heap

```python
build_heap(items: List[T]) -> None
```

Build heap from list of items using heapify operations.

**Parameters:**
- `items` (List[T]): List of items to build heap from

**Time Complexity:** O(n)

**Example:**
```python
heap = MinHeap()
heap.build_heap([5, 2, 8, 1, 9, 3])
```

#### size

```python
size() -> int
```

Get heap size.

**Returns:**
- `int`: Number of elements in heap

**Time Complexity:** O(1)

#### is_empty

```python
is_empty() -> bool
```

Check if heap is empty.

**Returns:**
- `bool`: True if heap is empty, False otherwise

**Time Complexity:** O(1)

### Private Methods

#### heapify_up

```python
heapify_up(index: int) -> None
```

Heapify up from given index to maintain min-heap property.

**Parameters:**
- `index`: Index to start heapify up from

**Time Complexity:** O(log n)

#### heapify_down

```python
heapify_down(index: int) -> None
```

Heapify down from given index to maintain min-heap property.

**Parameters:**
- `index`: Index to start heapify down from

**Time Complexity:** O(log n)

## MaxHeap Class

Max-heap implementation where parent nodes are always larger than or equal to their children. The maximum element is always at the root.

### Constructor

```python
MaxHeap(items: Optional[List[T]] = None) -> None
```

Initialize MaxHeap.

**Parameters:**
- `items` (Optional[List[T]]): Optional list of items to build heap from

**Example:**
```python
heap = MaxHeap([5, 2, 8, 1, 9, 3])
```

### Methods

#### insert

```python
insert(item: T) -> None
```

Insert item into heap.

**Parameters:**
- `item` (T): Item to insert

**Time Complexity:** O(log n)

**Example:**
```python
heap = MaxHeap()
heap.insert(5)
heap.insert(2)
heap.insert(8)
```

#### extract_max

```python
extract_max() -> Optional[T]
```

Extract and return maximum element.

**Returns:**
- `Optional[T]`: Maximum element, or None if heap is empty

**Time Complexity:** O(log n)

**Example:**
```python
heap = MaxHeap([5, 2, 8, 1, 9, 3])
max_val = heap.extract_max()  # Returns 9
```

#### peek

```python
peek() -> Optional[T]
```

Peek at maximum element without removing it.

**Returns:**
- `Optional[T]`: Maximum element, or None if heap is empty

**Time Complexity:** O(1)

**Example:**
```python
heap = MaxHeap([5, 2, 8, 1, 9, 3])
max_val = heap.peek()  # Returns 9, heap unchanged
```

#### build_heap

```python
build_heap(items: List[T]) -> None
```

Build heap from list of items using heapify operations.

**Parameters:**
- `items` (List[T]): List of items to build heap from

**Time Complexity:** O(n)

**Example:**
```python
heap = MaxHeap()
heap.build_heap([5, 2, 8, 1, 9, 3])
```

#### size

```python
size() -> int
```

Get heap size.

**Returns:**
- `int`: Number of elements in heap

**Time Complexity:** O(1)

#### is_empty

```python
is_empty() -> bool
```

Check if heap is empty.

**Returns:**
- `bool`: True if heap is empty, False otherwise

**Time Complexity:** O(1)

### Private Methods

#### heapify_up

```python
heapify_up(index: int) -> None
```

Heapify up from given index to maintain max-heap property.

**Parameters:**
- `index`: Index to start heapify up from

**Time Complexity:** O(log n)

#### heapify_down

```python
heapify_down(index: int) -> None
```

Heapify down from given index to maintain max-heap property.

**Parameters:**
- `index`: Index to start heapify down from

**Time Complexity:** O(log n)

## HeapSort Class

Heap sort algorithm implementation using heap data structure.

### Constructor

```python
HeapSort(config_path: str = "config.yaml") -> None
```

Initialize HeapSort with configuration.

**Parameters:**
- `config_path` (str): Path to configuration YAML file. Default: "config.yaml"

**Raises:**
- `FileNotFoundError`: If config file doesn't exist
- `yaml.YAMLError`: If config file is invalid YAML

### Methods

#### sort_ascending

```python
sort_ascending(arr: List[T]) -> List[T]
```

Sort array in ascending order using heap sort.

Uses max-heap to sort in ascending order.

**Parameters:**
- `arr` (List[T]): Array to sort

**Returns:**
- `List[T]`: Sorted array in ascending order

**Time Complexity:** O(n log n)

**Example:**
```python
heap_sort = HeapSort()
result = heap_sort.sort_ascending([5, 2, 8, 1, 9, 3])
# result = [1, 2, 3, 5, 8, 9]
```

#### sort_descending

```python
sort_descending(arr: List[T]) -> List[T]
```

Sort array in descending order using heap sort.

Uses min-heap to sort in descending order.

**Parameters:**
- `arr` (List[T]): Array to sort

**Returns:**
- `List[T]`: Sorted array in descending order

**Time Complexity:** O(n log n)

**Example:**
```python
heap_sort = HeapSort()
result = heap_sort.sort_descending([5, 2, 8, 1, 9, 3])
# result = [9, 8, 5, 3, 2, 1]
```

#### compare_with_builtin

```python
compare_with_builtin(
    arr: List[T],
    iterations: int = 1
) -> Dict[str, any]
```

Compare heap sort performance with built-in sorted().

**Parameters:**
- `arr` (List[T]): Array to sort
- `iterations` (int): Number of iterations for timing. Default: 1

**Returns:**
- `Dict[str, any]`: Dictionary containing performance comparison data with keys:
    - `array_length`: Length of input array
    - `iterations`: Number of iterations
    - `heap_sort_asc`: Dictionary with ascending sort results and timing
    - `heap_sort_desc`: Dictionary with descending sort results and timing
    - `builtin_sorted`: Dictionary with built-in sorted() results and timing

**Example:**
```python
heap_sort = HeapSort()
comparison = heap_sort.compare_with_builtin([5, 2, 8, 1, 9, 3])
print(comparison["heap_sort_asc"]["time_milliseconds"])
```

## Command-Line Interface

The module can be run as a script with the following interface:

```bash
python src/main.py NUMBERS [OPTIONS]
```

### Arguments

- `NUMBERS`: (Required) Numbers to operate on (space-separated)

### Options

- `-c, --config`: Path to configuration file (default: config.yaml)
- `-o, --operation`: Operation to perform - minheap, maxheap, heapsort, or compare (default: compare)
- `-d, --direction`: Sort direction for heap sort - asc or desc (default: asc)
- `-i, --iterations`: Number of iterations for timing (default: 1)

### Examples

```bash
# Min-heap operations
python src/main.py 5 2 8 1 9 3 --operation minheap

# Max-heap operations
python src/main.py 5 2 8 1 9 3 --operation maxheap

# Heap sort ascending
python src/main.py 5 2 8 1 9 3 --operation heapsort --direction asc

# Heap sort descending
python src/main.py 5 2 8 1 9 3 --operation heapsort --direction desc

# Compare with built-in sorted()
python src/main.py 5 2 8 1 9 3 --operation compare --iterations 1000
```

## Error Handling

All methods handle edge cases gracefully:

- Empty heap operations return None
- Empty array sorting returns empty list
- Single element arrays are handled correctly
- Duplicate values are preserved
- Negative numbers and floats are supported

## Algorithm Complexity

### Heap Operations

- **Insert**: O(log n) - heapify up after insertion
- **Extract**: O(log n) - heapify down after extraction
- **Peek**: O(1) - access root element
- **Build Heap**: O(n) - efficient bottom-up construction

### Heap Sort

- **Time Complexity**: O(n log n) in all cases (best, average, worst)
- **Space Complexity**: O(1) for in-place sorting, O(n) if creating copy
- **Stability**: Not stable (equal elements may change order)

## Notes

- Heaps are complete binary trees stored in arrays
- Parent-child relationships: parent at index i, children at 2i+1 and 2i+2
- Min-heap: parent ≤ children (minimum at root)
- Max-heap: parent ≥ children (maximum at root)
- Heapify operations maintain heap property after modifications
- Build heap is O(n) using bottom-up approach
- Heap sort provides guaranteed O(n log n) performance
- Heaps are ideal for priority queue implementations
- Both integer and floating point numbers are supported
