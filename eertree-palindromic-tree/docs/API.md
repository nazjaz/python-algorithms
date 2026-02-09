# Eertree API Documentation

## Classes

### EertreeNode

Represents a node in the eertree data structure.

#### Attributes

- `length` (int): Length of the palindrome represented by this node
- `edges` (Dict[str, EertreeNode]): Dictionary mapping characters to child nodes
- `suffix_link` (Optional[EertreeNode]): Link to the longest palindromic suffix
- `count` (int): Number of occurrences of this palindrome

#### Methods

No public methods. This is a data class used internally by `Eertree`.

---

### Eertree

Main class for the eertree (palindromic tree) data structure.

#### Methods

##### `__init__(self) -> None`

Initialize an empty eertree.

**Returns**: None

**Example**:
```python
tree = Eertree()
```

---

##### `build(self, text: str) -> None`

Build the eertree from a given string.

**Parameters**:
- `text` (str): Input string to build the eertree from

**Returns**: None

**Raises**:
- No exceptions raised

**Example**:
```python
tree = Eertree()
tree.build("abacaba")
```

---

##### `add_char(self, char: str) -> Optional[EertreeNode]`

Add a character to the eertree and update current node.

**Parameters**:
- `char` (str): Character to add to the string

**Returns**:
- `Optional[EertreeNode]`: New node created if a new palindrome was found, None otherwise

**Example**:
```python
tree = Eertree()
new_node = tree.add_char("a")
tree.add_char("b")
tree.add_char("a")
```

---

##### `get_all_palindromes(self) -> Set[str]`

Get all distinct palindromic substrings in the string.

**Returns**:
- `Set[str]`: Set of all distinct palindromic substrings

**Example**:
```python
tree = Eertree()
tree.build("abacaba")
palindromes = tree.get_all_palindromes()
# Returns: {'a', 'b', 'c', 'aba', 'aca', 'bacab', 'abacaba'}
```

---

##### `count_distinct_palindromes(self) -> int`

Count the number of distinct palindromic substrings.

**Returns**:
- `int`: Number of distinct palindromic substrings

**Example**:
```python
tree = Eertree()
tree.build("abacaba")
count = tree.count_distinct_palindromes()
# Returns: 7
```

---

##### `count_total_palindromes(self) -> int`

Count the total number of palindromic substrings (with duplicates).

**Returns**:
- `int`: Total count of all palindromic substrings including duplicates

**Example**:
```python
tree = Eertree()
tree.build("abacaba")
total = tree.count_total_palindromes()
# Returns: 15 (includes overlapping occurrences)
```

---

##### `get_palindrome_count(self, palindrome: str) -> int`

Get the count of occurrences of a specific palindrome.

**Parameters**:
- `palindrome` (str): The palindrome string to count

**Returns**:
- `int`: Number of times the palindrome appears as a substring, or 0 if it's not a palindrome or doesn't exist

**Example**:
```python
tree = Eertree()
tree.build("abacaba")
count = tree.get_palindrome_count("aba")
# Returns: 2
```

---

##### `is_palindrome_substring(self, substring: str) -> bool`

Check if a substring exists in the string and is a palindrome.

**Parameters**:
- `substring` (str): Substring to check

**Returns**:
- `bool`: True if the substring is a palindrome and exists in the string, False otherwise

**Example**:
```python
tree = Eertree()
tree.build("abacaba")
result = tree.is_palindrome_substring("aba")
# Returns: True
```

---

##### `get_longest_palindrome(self) -> str`

Get the longest palindromic substring.

**Returns**:
- `str`: Longest palindromic substring, or empty string if none exists

**Example**:
```python
tree = Eertree()
tree.build("abacaba")
longest = tree.get_longest_palindrome()
# Returns: "abacaba"
```

---

## Internal Methods

The following methods are used internally and are not part of the public API, but are documented for completeness:

##### `_get_suffix_link(self, node: EertreeNode, char: str, position: int) -> EertreeNode`

Find the suffix link for a node when adding a character.

##### `_update_counts(self) -> None`

Update palindrome counts by propagating counts through suffix links.

##### `_collect_palindromes(self, node: EertreeNode, current: str, palindromes: Set[str]) -> None`

Recursively collect all palindromes from the tree.

##### `_is_palindrome(self, text: str) -> bool`

Check if a string is a palindrome.

##### `_find_node(self, palindrome: str) -> Optional[EertreeNode]`

Find the node representing a specific palindrome.

---

## Usage Examples

### Basic Usage

```python
from src.main import Eertree

# Create and build eertree
tree = Eertree()
tree.build("abacaba")

# Get statistics
distinct = tree.count_distinct_palindromes()
total = tree.count_total_palindromes()
longest = tree.get_longest_palindrome()

print(f"Distinct: {distinct}, Total: {total}, Longest: {longest}")
```

### Query Operations

```python
tree = Eertree()
tree.build("racecar")

# Check if substring is palindrome
if tree.is_palindrome_substring("racecar"):
    count = tree.get_palindrome_count("racecar")
    print(f"Found {count} times")
```

### Get All Palindromes

```python
tree = Eertree()
tree.build("aaa")
palindromes = tree.get_all_palindromes()
# Returns: {'a', 'aa', 'aaa'}
```

---

## Performance Characteristics

- **Time Complexity**: O(n) for building the tree, where n is the string length
- **Space Complexity**: O(n) for storing all distinct palindromes
- **Query Operations**: O(1) to O(m) where m is the length of the queried palindrome

---

## Notes

- The eertree stores only distinct palindromes, but counts include all occurrences
- Overlapping palindromes are counted separately
- The tree is rebuilt when `build()` is called with a new string
- Characters are case-sensitive (e.g., "A" and "a" are different)
