# Interval Tree API Documentation

This document provides detailed API documentation for the interval tree implementation with efficient range overlap queries and interval management.

## Classes

### Interval

Represents an interval [low, high].

#### Attributes

- `low` (int): Lower endpoint of interval
- `high` (int): Upper endpoint of interval

#### Methods

##### `__init__(low: int, high: int) -> None`

Initialize interval.

**Parameters:**
- `low`: Lower endpoint of interval
- `high`: Upper endpoint of interval

**Raises:**
- `ValueError`: If low > high

**Example:**
```python
interval = Interval(10, 20)
```

##### `overlaps(other: Interval) -> bool`

Check if this interval overlaps with another interval.

**Parameters:**
- `other`: Other interval to check

**Returns:**
- `True` if intervals overlap, `False` otherwise

**Example:**
```python
interval1 = Interval(10, 20)
interval2 = Interval(15, 25)
assert interval1.overlaps(interval2) is True
```

##### `overlaps_point(point: int) -> bool`

Check if this interval contains a point.

**Parameters:**
- `point`: Point to check

**Returns:**
- `True` if point is in interval, `False` otherwise

**Example:**
```python
interval = Interval(10, 20)
assert interval.overlaps_point(15) is True
assert interval.overlaps_point(25) is False
```

### IntervalNode

Node in interval tree.

#### Attributes

- `interval` (Interval): Interval stored in this node
- `max_endpoint` (int): Maximum endpoint in subtree
- `left` (Optional[IntervalNode]): Left child node
- `right` (Optional[IntervalNode]): Right child node

#### Methods

##### `update_max_endpoint() -> None`

Update max endpoint based on subtree.

**Example:**
```python
node.update_max_endpoint()
```

### IntervalTree

Main class for interval tree data structure.

#### Methods

##### `__init__(config_path: str = "config.yaml") -> None`

Initialize interval tree.

**Parameters:**
- `config_path`: Path to configuration YAML file (default: "config.yaml")

**Example:**
```python
tree = IntervalTree()
```

##### `insert(low: int, high: int) -> bool`

Insert interval into tree.

**Parameters:**
- `low`: Lower endpoint of interval
- `high`: Upper endpoint of interval

**Returns:**
- `True` if inserted, `False` if already exists

**Raises:**
- `ValueError`: If low > high

**Time Complexity:** O(log n)

**Example:**
```python
tree.insert(10, 20)  # Returns True
tree.insert(10, 20)  # Returns False (duplicate)
```

##### `delete(low: int, high: int) -> bool`

Delete interval from tree.

**Parameters:**
- `low`: Lower endpoint of interval
- `high`: Upper endpoint of interval

**Returns:**
- `True` if deleted, `False` if not found

**Raises:**
- `ValueError`: If low > high

**Time Complexity:** O(log n)

**Example:**
```python
tree.delete(10, 20)  # Returns True if deleted
```

##### `find_overlapping_intervals(low: int, high: int) -> List[Interval]`

Find all intervals overlapping with given interval.

**Parameters:**
- `low`: Lower endpoint of query interval
- `high`: Upper endpoint of query interval

**Returns:**
- List of overlapping intervals

**Raises:**
- `ValueError`: If low > high

**Time Complexity:** O(log n + k) where k is number of results

**Example:**
```python
overlapping = tree.find_overlapping_intervals(12, 18)
for interval in overlapping:
    print(interval)
```

##### `find_intervals_containing_point(point: int) -> List[Interval]`

Find all intervals containing a point.

**Parameters:**
- `point`: Query point

**Returns:**
- List of intervals containing the point

**Time Complexity:** O(log n + k) where k is number of results

**Example:**
```python
containing = tree.find_intervals_containing_point(15)
for interval in containing:
    print(interval)
```

##### `get_all_intervals() -> List[Interval]`

Get all intervals in sorted order by low endpoint.

**Returns:**
- List of all intervals sorted by low endpoint

**Time Complexity:** O(n)

**Example:**
```python
all_intervals = tree.get_all_intervals()
```

##### `is_empty() -> bool`

Check if tree is empty.

**Returns:**
- `True` if empty, `False` otherwise

**Time Complexity:** O(1)

**Example:**
```python
if tree.is_empty():
    print("Tree is empty")
```

##### `get_size() -> int`

Get number of intervals in tree.

**Returns:**
- Number of intervals

**Time Complexity:** O(1)

**Example:**
```python
size = tree.get_size()
```

##### `clear() -> None`

Clear all intervals from tree.

**Example:**
```python
tree.clear()
```

## Usage Examples

### Basic Operations

```python
from src.main import IntervalTree

# Create tree
tree = IntervalTree()

# Insert intervals
tree.insert(10, 20)
tree.insert(15, 25)
tree.insert(5, 15)

# Find overlapping intervals
overlapping = tree.find_overlapping_intervals(12, 18)
for interval in overlapping:
    print(f"Overlaps: {interval}")

# Find intervals containing point
containing = tree.find_intervals_containing_point(15)
for interval in containing:
    print(f"Contains point: {interval}")

# Delete interval
tree.delete(10, 20)

# Get all intervals
all_intervals = tree.get_all_intervals()
```

### Scheduling Example

```python
from src.main import IntervalTree

# Create schedule
schedule = IntervalTree()

# Add appointments
schedule.insert(9, 10)   # 9:00 - 10:00
schedule.insert(10, 11)  # 10:00 - 11:00
schedule.insert(14, 15)  # 2:00 PM - 3:00 PM

# Check for conflicts when scheduling new appointment
new_appointment = (10, 11)
conflicts = schedule.find_overlapping_intervals(*new_appointment)
if conflicts:
    print(f"Conflict found with: {conflicts}")
else:
    schedule.insert(*new_appointment)
    print("Appointment scheduled")
```

### Range Query Example

```python
from src.main import IntervalTree

# Create interval tree
tree = IntervalTree()

# Insert intervals
tree.insert(10, 20)
tree.insert(15, 25)
tree.insert(5, 15)
tree.insert(30, 40)

# Query for intervals in range [12, 18]
overlapping = tree.find_overlapping_intervals(12, 18)
print(f"Intervals overlapping [12, 18]: {overlapping}")

# Query for intervals containing point 15
containing = tree.find_intervals_containing_point(15)
print(f"Intervals containing point 15: {containing}")
```

### Error Handling

```python
from src.main import IntervalTree, Interval

tree = IntervalTree()

# Invalid interval (low > high)
try:
    tree.insert(20, 10)
except ValueError as e:
    print(f"Error: {e}")

# Duplicate interval
tree.insert(10, 20)
result = tree.insert(10, 20)
if not result:
    print("Interval already exists")

# Delete non-existent interval
result = tree.delete(30, 40)
if not result:
    print("Interval not found")
```

## Time Complexity Summary

| Operation | Average Case | Worst Case |
|-----------|--------------|------------|
| `insert` | O(log n) | O(n) |
| `delete` | O(log n) | O(n) |
| `find_overlapping_intervals` | O(log n + k) | O(n + k) |
| `find_intervals_containing_point` | O(log n + k) | O(n + k) |
| `get_all_intervals` | O(n) | O(n) |
| `is_empty` | O(1) | O(1) |
| `get_size` | O(1) | O(1) |
| `clear` | O(1) | O(1) |

Where n is the number of intervals and k is the number of results.

## Notes

- Intervals are stored ordered by low endpoint
- Max endpoint tracking enables efficient overlap queries
- Duplicate intervals (same low and high) are not allowed
- All intervals must satisfy low <= high
- Query operations return all matching intervals
- The tree structure may become unbalanced, affecting worst-case performance
