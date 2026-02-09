# Aho-Corasick Algorithm API Documentation

This document provides detailed API documentation for the Aho-Corasick algorithm implementation for multiple pattern matching.

## Classes

### TrieNode

Node in Aho-Corasick automaton.

#### Attributes

- `children` (Dict[str, TrieNode]): Dictionary mapping characters to child nodes
- `failure` (Optional[TrieNode]): Failure link to another node
- `output` (Set[str]): Set of patterns ending at this node
- `is_end` (bool): Whether this node marks end of a pattern

### AhoCorasickAlgorithm

Main class for Aho-Corasick algorithm operations.

#### Methods

##### `__init__(patterns: List[str], config_path: str = "config.yaml") -> None`

Initialize Aho-Corasick algorithm with patterns.

**Parameters:**
- `patterns`: List of patterns to search for
- `config_path`: Path to configuration YAML file (default: "config.yaml")

**Raises:**
- `ValueError`: If patterns list is empty or all patterns are empty

**Example:**
```python
ac = AhoCorasickAlgorithm(["he", "she", "his", "hers"])
```

##### `search(text: str) -> Dict[str, List[int]]`

Search for all patterns in text.

**Parameters:**
- `text`: Text to search in

**Returns:**
- Dictionary mapping pattern to list of occurrence positions

**Time Complexity:** O(n + m + z) where n is text length, m is total pattern length, z is number of matches

**Example:**
```python
results = ac.search("ushers")
# Returns {"he": [2], "she": [1], "his": [], "hers": [2]}
```

##### `count_occurrences(text: str) -> Dict[str, int]`

Count occurrences of each pattern in text.

**Parameters:**
- `text`: Text to search in

**Returns:**
- Dictionary mapping pattern to occurrence count

**Time Complexity:** O(n + m + z)

**Example:**
```python
counts = ac.count_occurrences("ushers")
# Returns {"he": 1, "she": 1, "his": 0, "hers": 1}
```

##### `find_all_occurrences(text: str) -> List[Tuple[str, int, int]]`

Find all occurrences with pattern, position, and length.

**Parameters:**
- `text`: Text to search in

**Returns:**
- List of (pattern, position, length) tuples sorted by position

**Time Complexity:** O(n + m + z)

**Example:**
```python
occurrences = ac.find_all_occurrences("ushers")
# Returns [("she", 1, 3), ("he", 2, 2), ("hers", 2, 4)]
```

##### `is_pattern_found(text: str, pattern: str) -> bool`

Check if specific pattern is found in text.

**Parameters:**
- `text`: Text to search in
- `pattern`: Pattern to check

**Returns:**
- `True` if pattern found, `False` otherwise

**Raises:**
- `ValueError`: If pattern not in automaton

**Time Complexity:** O(n + m + z)

**Example:**
```python
found = ac.is_pattern_found("ushers", "he")  # Returns True
```

##### `get_patterns() -> List[str]`

Get list of patterns.

**Returns:**
- List of patterns

**Example:**
```python
patterns = ac.get_patterns()  # Returns ["he", "she", "his", "hers"]
```

##### `get_pattern_count() -> int`

Get number of patterns.

**Returns:**
- Number of patterns

**Example:**
```python
count = ac.get_pattern_count()  # Returns 4
```

## Usage Examples

### Basic Multiple Pattern Matching

```python
from src.main import AhoCorasickAlgorithm

# Create Aho-Corasick automaton
patterns = ["he", "she", "his", "hers"]
ac = AhoCorasickAlgorithm(patterns)

# Search for all patterns
text = "ushers"
results = ac.search(text)
# Returns {"he": [2], "she": [1], "his": [], "hers": [2]}

# Count occurrences
counts = ac.count_occurrences(text)
# Returns {"he": 1, "she": 1, "his": 0, "hers": 1}
```

### Finding All Occurrences

```python
ac = AhoCorasickAlgorithm(["ab", "abc", "bc"])

# Get all occurrences with positions
occurrences = ac.find_all_occurrences("abcabc")
# Returns [("ab", 0, 2), ("abc", 0, 3), ("bc", 1, 2), ("ab", 3, 2), ("abc", 3, 3), ("bc", 4, 2)]
```

### Checking Specific Patterns

```python
ac = AhoCorasickAlgorithm(["he", "she", "his", "hers"])

# Check if specific pattern found
found = ac.is_pattern_found("ushers", "he")  # Returns True
found = ac.is_pattern_found("ushers", "his")  # Returns False
```

### Overlapping Patterns

```python
ac = AhoCorasickAlgorithm(["a", "aa", "aaa"])

# Find all overlapping patterns
results = ac.search("aaa")
# Returns {"a": [0, 1, 2], "aa": [0, 1], "aaa": [0]}
```

## Error Handling

The implementation handles the following cases gracefully:

- **Empty patterns list**: Raises `ValueError` during initialization
- **All empty patterns**: Raises `ValueError` during initialization
- **Pattern not in automaton**: Raises `ValueError` for is_pattern_found
- **Empty text**: Returns empty results for all patterns
- **Configuration errors**: Falls back to defaults if config file missing

## Performance Characteristics

| Operation | Time Complexity | Space Complexity |
|-----------|----------------|------------------|
| Build Automaton | O(m) | O(m) |
| Search | O(n + m + z) | O(1) |
| Count Occurrences | O(n + m + z) | O(1) |
| Find All Occurrences | O(n + m + z) | O(z) |

Where:
- n = text length
- m = total pattern length
- z = number of matches

## Algorithm Details

### Automaton Construction

The automaton is built in three phases:

1. **Trie Construction**: Insert all patterns into trie
2. **Failure Links**: Build failure links using BFS (similar to KMP)
3. **Output Links**: Propagate outputs through failure links

### Failure Link Construction

Failure links are built using BFS:
- Root's children point to root
- For each node, follow failure links until finding matching character
- Similar to KMP failure function but for trie structure

### Pattern Matching

Pattern matching traverses the automaton:
1. Start at root
2. For each character, follow edge or failure link
3. Collect all outputs at current node
4. Continue until text ends

This ensures all patterns are found in a single pass.

## Thread Safety

This implementation is not thread-safe. For concurrent access, external synchronization is required.
