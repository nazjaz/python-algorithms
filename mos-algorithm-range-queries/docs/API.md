# Mo's Algorithm API Documentation

## Classes

### Query

Represents a range query.

#### Attributes

- `left` (int): Left endpoint (inclusive, 0-indexed)
- `right` (int): Right endpoint (inclusive, 0-indexed)
- `index` (int): Query index for preserving order

#### Methods

##### `__init__(self, left: int, right: int, index: int = 0) -> None`

Initialize a query.

**Parameters**:
- `left` (int): Left endpoint (inclusive, 0-indexed).
- `right` (int): Right endpoint (inclusive, 0-indexed).
- `index` (int): Query index for preserving order. Default: 0.

**Example**:
```python
query = Query(0, 5, index=0)
```

---

### MosAlgorithm

Main class for Mo's algorithm implementation.

#### Methods

##### `__init__(self, array: List[int]) -> None`

Initialize Mo's algorithm with an array.

**Parameters**:
- `array` (List[int]): Input array for queries.

**Example**:
```python
mos = MosAlgorithm([1, 2, 3, 4, 5])
```

---

##### `process_queries(self, queries: List[Query], add_func: Callable[[int], None], remove_func: Callable[[int], None], get_result_func: Callable[[], any]) -> List[any]`

Process queries using Mo's algorithm with custom functions.

**Parameters**:
- `queries` (List[Query]): List of queries to process.
- `add_func` (Callable[[int], None]): Function to call when adding an element at index.
- `remove_func` (Callable[[int], None]): Function to call when removing an element at index.
- `get_result_func` (Callable[[], any]): Function to get current result.

**Returns**:
- `List[any]`: List of results in original query order.

**Example**:
```python
def add(index):
    # Handle adding element at index
    pass

def remove(index):
    # Handle removing element at index
    pass

def get_result():
    return current_result

results = mos.process_queries(queries, add, remove, get_result)
```

---

##### `range_sum_queries(self, queries: List[Query]) -> List[int]`

Answer range sum queries.

**Parameters**:
- `queries` (List[Query]): List of range sum queries.

**Returns**:
- `List[int]`: List of sum results.

**Example**:
```python
queries = [Query(0, 2, 0), Query(1, 3, 1)]
results = mos.range_sum_queries(queries)
# Returns: [6, 9] for array [1, 2, 3, 4, 5]
```

---

##### `range_distinct_count_queries(self, queries: List[Query]) -> List[int]`

Answer range distinct count queries.

**Parameters**:
- `queries` (List[Query]): List of range distinct count queries.

**Returns**:
- `List[int]`: List of distinct count results.

**Example**:
```python
queries = [Query(0, 2, 0)]
results = mos.range_distinct_count_queries(queries)
# Returns: [2] for array [1, 2, 2, 3]
```

---

##### `range_max_queries(self, queries: List[Query]) -> List[Optional[int]]`

Answer range maximum queries.

**Parameters**:
- `queries` (List[Query]): List of range maximum queries.

**Returns**:
- `List[Optional[int]]`: List of maximum values.

**Example**:
```python
queries = [Query(0, 2, 0)]
results = mos.range_max_queries(queries)
# Returns: [5] for array [1, 5, 3]
```

---

##### `range_min_queries(self, queries: List[Query]) -> List[Optional[int]]`

Answer range minimum queries.

**Parameters**:
- `queries` (List[Query]): List of range minimum queries.

**Returns**:
- `List[Optional[int]]`: List of minimum values.

**Example**:
```python
queries = [Query(0, 2, 0)]
results = mos.range_min_queries(queries)
# Returns: [1] for array [1, 5, 3]
```

---

##### `range_frequency_queries(self, queries: List[Query], target_value: int) -> List[int]`

Answer range frequency queries for a specific value.

**Parameters**:
- `queries` (List[Query]): List of range frequency queries.
- `target_value` (int): Value to count frequency of.

**Returns**:
- `List[int]`: List of frequency results.

**Example**:
```python
queries = [Query(0, 2, 0)]
results = mos.range_frequency_queries(queries, target_value=2)
# Returns: [2] for array [1, 2, 2, 3]
```

---

##### `range_mode_queries(self, queries: List[Query]) -> List[Optional[int]]`

Answer range mode (most frequent element) queries.

**Parameters**:
- `queries` (List[Query]): List of range mode queries.

**Returns**:
- `List[Optional[int]]`: List of mode values. In case of tie, returns smaller value.

**Example**:
```python
queries = [Query(0, 2, 0)]
results = mos.range_mode_queries(queries)
# Returns: [2] for array [1, 2, 2, 3]
```

---

## Internal Methods

The following methods are used internally and are not part of the public API, but are documented for completeness:

##### `_get_block(self, index: int) -> int`

Get block number for an index.

##### `_compare_queries(self, q1: Query, q2: Query) -> int`

Compare two queries for sorting.

---

## Usage Examples

### Basic Range Sum Queries

```python
from src.main import MosAlgorithm, Query

array = [1, 2, 3, 4, 5]
mos = MosAlgorithm(array)

queries = [Query(0, 2, 0), Query(1, 3, 1)]
results = mos.range_sum_queries(queries)
print(f"Results: {results}")  # [6, 9]
```

### Custom Query Processing

```python
mos = MosAlgorithm([1, 2, 3, 4, 5])

count = 0

def add(index):
    nonlocal count
    count += 1

def remove(index):
    nonlocal count
    count -= 1

def get_result():
    return count

queries = [Query(0, 2, 0)]
results = mos.process_queries(queries, add, remove, get_result)
# Returns: [3] (count of elements in range)
```

### Multiple Query Types

```python
array = [1, 2, 2, 3, 3, 3]
mos = MosAlgorithm(array)
queries = [Query(0, 5, 0)]

# Sum
sum_results = mos.range_sum_queries(queries)

# Distinct count
distinct_results = mos.range_distinct_count_queries(queries)

# Mode
mode_results = mos.range_mode_queries(queries)
```

---

## Performance Characteristics

- **Time Complexity**: O((n + q) × √n) where n is array size, q is number of queries
- **Space Complexity**: O(n) for storing array and frequency maps
- **Per Query**: O(√n) amortized time

---

## Notes

- Queries use 0-indexed positions
- Left endpoint must be <= right endpoint
- Results are returned in original query order (preserved by index)
- Algorithm is most efficient when processing multiple queries offline
- For online queries, consider using segment trees or Fenwick trees
