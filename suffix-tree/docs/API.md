# Suffix Tree API Documentation

This document provides detailed API documentation for the suffix tree implementation using Ukkonen's algorithm.

## Classes

### SuffixTreeNode

Represents a node in the suffix tree.

#### Attributes

- `start` (Optional[int]): Start index of edge label (None for root)
- `end` (Optional[int]): End index of edge label (-1 for leaf, None for root)
- `suffix_link` (Optional[SuffixTreeNode]): Suffix link to another node
- `children` (Dict[str, SuffixTreeNode]): Dictionary mapping characters to child nodes
- `leaf_count` (int): Number of leaves in subtree (for some algorithms)

#### Methods

##### `edge_length(string_end: int) -> int`

Calculate the length of the edge label.

**Parameters:**
- `string_end`: End index of the string

**Returns:**
- Length of edge label

**Example:**
```python
node = SuffixTreeNode(start=0, end=5)
length = node.edge_length(10)  # Returns 5
```

##### `get_edge_label(text: str) -> str`

Get the edge label substring from the text.

**Parameters:**
- `text`: The input string

**Returns:**
- Edge label substring

**Example:**
```python
node = SuffixTreeNode(start=0, end=3)
label = node.get_edge_label("banana")  # Returns "ban"
```

### SuffixTree

Main class for suffix tree constructed using Ukkonen's algorithm.

#### Methods

##### `__init__(text: str, config_path: str = "config.yaml") -> None`

Initialize a new suffix tree.

**Parameters:**
- `text`: Input string to build suffix tree for
- `config_path`: Path to configuration YAML file (default: "config.yaml")

**Raises:**
- `ValueError`: If text is empty

**Example:**
```python
tree = SuffixTree("banana")
```

##### `search(pattern: str) -> bool`

Search for pattern in suffix tree.

**Parameters:**
- `pattern`: Pattern to search for

**Returns:**
- `True` if pattern found, `False` otherwise

**Time Complexity:** O(m) where m is pattern length

**Example:**
```python
tree = SuffixTree("banana")
tree.search("ana")  # Returns True
tree.search("xyz")  # Returns False
```

##### `find_all_occurrences(pattern: str) -> List[int]`

Find all occurrences of pattern in text.

**Parameters:**
- `pattern`: Pattern to search for

**Returns:**
- List of starting positions where pattern occurs

**Time Complexity:** O(m + k) where m is pattern length, k is number of occurrences

**Example:**
```python
tree = SuffixTree("banana")
occurrences = tree.find_all_occurrences("ana")  # Returns [1, 3]
```

##### `get_substring_count(pattern: str) -> int`

Count occurrences of pattern.

**Parameters:**
- `pattern`: Pattern to count

**Returns:**
- Number of occurrences

**Time Complexity:** O(m + k)

**Example:**
```python
tree = SuffixTree("banana")
count = tree.get_substring_count("an")  # Returns 2
```

##### `is_suffix(pattern: str) -> bool`

Check if pattern is a suffix of text.

**Parameters:**
- `pattern`: Pattern to check

**Returns:**
- `True` if pattern is suffix, `False` otherwise

**Time Complexity:** O(m)

**Example:**
```python
tree = SuffixTree("banana")
tree.is_suffix("ana")  # Returns True
tree.is_suffix("ban")  # Returns False
```

##### `get_longest_repeated_substring() -> str`

Find longest repeated substring.

**Returns:**
- Longest repeated substring (empty string if none)

**Time Complexity:** O(n) where n is text length

**Example:**
```python
tree = SuffixTree("banana")
longest = tree.get_longest_repeated_substring()  # Returns "ana"
```

##### `get_all_suffixes() -> List[str]`

Get all suffixes of the text.

**Returns:**
- List of all suffixes

**Time Complexity:** O(n)

**Example:**
```python
tree = SuffixTree("abc")
suffixes = tree.get_all_suffixes()  # Returns ["abc$", "bc$", "c$", "$"]
```

##### `get_tree_size() -> int`

Get number of nodes in tree.

**Returns:**
- Number of nodes

**Time Complexity:** O(n)

**Example:**
```python
tree = SuffixTree("banana")
size = tree.get_tree_size()  # Returns number of nodes
```

##### `is_valid() -> bool`

Validate suffix tree structure.

**Returns:**
- `True` if tree is valid, `False` otherwise

**Time Complexity:** O(n)

**Validates:**
- Edge labels are valid
- Node structure is correct
- Tree properties are maintained

**Example:**
```python
tree = SuffixTree("banana")
tree.is_valid()  # Returns True
```

## Usage Examples

### Basic Pattern Matching

```python
from src.main import SuffixTree

# Create suffix tree
tree = SuffixTree("banana")

# Search for patterns
tree.search("ban")  # True
tree.search("ana")  # True
tree.search("xyz")  # False

# Find all occurrences
occurrences = tree.find_all_occurrences("ana")  # [1, 3]

# Count occurrences
count = tree.get_substring_count("an")  # 2
```

### Text Analysis

```python
tree = SuffixTree("mississippi")

# Find longest repeated substring
longest = tree.get_longest_repeated_substring()  # "issi"

# Check if pattern is suffix
tree.is_suffix("ppi")  # True
tree.is_suffix("miss")  # False

# Get all suffixes
suffixes = tree.get_all_suffixes()
```

### DNA Sequence Analysis

```python
dna_sequence = "ATCGATCGATCG"
tree = SuffixTree(dna_sequence)

# Search for genetic patterns
tree.search("ATCG")  # True

# Find all occurrences of pattern
occurrences = tree.find_all_occurrences("ATCG")  # [0, 4, 8]

# Count pattern frequency
count = tree.get_substring_count("ATCG")  # 3
```

### Large Text Processing

```python
large_text = "..."  # Very long text
tree = SuffixTree(large_text)

# Efficient pattern matching
found = tree.search("pattern")  # O(m) time

# Find all occurrences efficiently
occurrences = tree.find_all_occurrences("pattern")  # O(m + k) time
```

## Error Handling

The implementation handles the following cases gracefully:

- **Empty text**: Raises `ValueError` during construction
- **Empty pattern**: Returns `True` for search (matches all positions)
- **Non-existent patterns**: Returns `False` or empty list appropriately
- **Configuration errors**: Falls back to defaults if config file missing

## Performance Characteristics

| Operation | Time Complexity | Space Complexity |
|-----------|----------------|------------------|
| Construction | O(n) | O(n) |
| Search | O(m) | O(1) |
| Find All Occurrences | O(m + k) | O(k) |
| Count Occurrences | O(m + k) | O(1) |
| Longest Repeated Substring | O(n) | O(n) |
| Is Suffix | O(m) | O(1) |
| Get All Suffixes | O(n) | O(n) |
| Tree Size | O(n) | O(1) |
| Validation | O(n) | O(1) |

Where:
- n = text length
- m = pattern length
- k = number of occurrences

## Algorithm Details

### Ukkonen's Algorithm

The implementation uses Ukkonen's algorithm which:

1. **Processes characters online**: Builds tree incrementally
2. **Uses active point**: Tracks current position efficiently
3. **Implements suffix links**: Enables O(n) construction
4. **Applies extension rules**: Handles three cases optimally

### Key Features

- **Linear time construction**: O(n) for text of length n
- **Efficient queries**: O(m) for pattern of length m
- **Space efficient**: O(n) space for n-length text
- **Online algorithm**: Can process text character by character

## Thread Safety

This implementation is not thread-safe. For concurrent access, external synchronization is required.
