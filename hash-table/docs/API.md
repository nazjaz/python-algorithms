# Hash Table API Documentation

## Overview

The Hash Table implementation provides two collision handling methods: chaining (separate chaining) and open addressing (linear probing). Both implementations support insert, get, delete, and contains operations with automatic resizing.

## Classes

### HashTableChaining

Hash table using separate chaining for collision resolution.

#### Constructor

```python
HashTableChaining(initial_capacity: int = 11) -> None
```

Initialize hash table with chaining.

**Parameters:**
- `initial_capacity` (int): Initial capacity of hash table. Default: 11

#### Methods

##### insert

```python
insert(key: Any, value: Any) -> None
```

Insert key-value pair into hash table.

**Parameters:**
- `key` (Any): Key to insert
- `value` (Any): Value to associate with key

**Time Complexity:** O(1) average, O(n) worst case

##### get

```python
get(key: Any) -> Optional[Any]
```

Get value associated with key.

**Parameters:**
- `key` (Any): Key to search for

**Returns:**
- `Optional[Any]`: Value associated with key, or None if not found

**Time Complexity:** O(1) average, O(n) worst case

##### delete

```python
delete(key: Any) -> bool
```

Delete key-value pair from hash table.

**Parameters:**
- `key` (Any): Key to delete

**Returns:**
- `bool`: True if key was deleted, False if not found

**Time Complexity:** O(1) average, O(n) worst case

##### contains

```python
contains(key: Any) -> bool
```

Check if key exists in hash table.

**Parameters:**
- `key` (Any): Key to check

**Returns:**
- `bool`: True if key exists, False otherwise

##### get_load_factor

```python
get_load_factor() -> float
```

Get current load factor.

**Returns:**
- `float`: Load factor (size / capacity)

##### visualize

```python
visualize() -> str
```

Generate visual representation of hash table.

**Returns:**
- `str`: String representation of hash table structure

### HashTableOpenAddressing

Hash table using open addressing (linear probing) for collision resolution.

#### Constructor

```python
HashTableOpenAddressing(initial_capacity: int = 11) -> None
```

Initialize hash table with open addressing.

**Parameters:**
- `initial_capacity` (int): Initial capacity of hash table. Default: 11

#### Methods

Same methods as HashTableChaining with same signatures and time complexities.

## Collision Handling

### Chaining (Separate Chaining)

- Each bucket contains a list of key-value pairs
- Collisions handled by adding to the list
- No probing needed
- Can handle unlimited collisions per bucket

### Open Addressing (Linear Probing)

- All elements stored directly in table
- Collisions handled by probing to next available slot
- Linear probing: next slot = (index + 1) % capacity
- Requires careful load factor management

## Usage Examples

### Chaining Method

```python
from src.main import HashTableChaining

table = HashTableChaining()
table.insert("key1", "value1")
table.insert("key2", "value2")
print(table.get("key1"))  # "value1"
print(table.contains("key2"))  # True
table.delete("key1")
```

### Open Addressing Method

```python
from src.main import HashTableOpenAddressing

table = HashTableOpenAddressing()
table.insert("key1", "value1")
table.insert("key2", "value2")
print(table.get("key1"))  # "value1"
print(table.visualize())
```
