# Trie Data Structure API Documentation

## Trie Class

Main class for trie (prefix tree) data structure operations.

### Constructor

```python
Trie(config_path: str = "config.yaml") -> None
```

Initialize Trie with configuration.

**Parameters:**
- `config_path` (str): Path to configuration YAML file. Default: "config.yaml"

**Raises:**
- `FileNotFoundError`: If config file doesn't exist
- `yaml.YAMLError`: If config file is invalid YAML

### Methods

#### insert

```python
insert(word: str) -> None
```

Insert word into trie.

**Parameters:**
- `word` (str): Word to insert

**Time Complexity:** O(m) where m is word length

**Example:**
```python
trie = Trie()
trie.insert("apple")
trie.insert("apply")
```

#### search

```python
search(word: str) -> bool
```

Search for exact word in trie.

**Parameters:**
- `word` (str): Word to search for

**Returns:**
- `bool`: True if word exists, False otherwise

**Time Complexity:** O(m) where m is word length

**Example:**
```python
trie = Trie()
trie.insert("apple")
result = trie.search("apple")  # Returns True
result = trie.search("app")    # Returns False
```

#### starts_with

```python
starts_with(prefix: str) -> bool
```

Check if any word in trie starts with given prefix.

**Parameters:**
- `prefix` (str): Prefix to check

**Returns:**
- `bool`: True if prefix exists, False otherwise

**Time Complexity:** O(m) where m is prefix length

**Example:**
```python
trie = Trie()
trie.insert("apple")
trie.insert("apply")
result = trie.starts_with("app")  # Returns True
result = trie.starts_with("ora")  # Returns False
```

#### autocomplete

```python
autocomplete(prefix: str, limit: Optional[int] = None) -> List[str]
```

Get autocomplete suggestions for given prefix.

**Parameters:**
- `prefix` (str): Prefix to autocomplete
- `limit` (Optional[int]): Maximum number of suggestions (None for all)

**Returns:**
- `List[str]`: List of words that start with the prefix

**Time Complexity:** O(m + k) where m is prefix length, k is number of suggestions

**Example:**
```python
trie = Trie()
trie.insert("apple")
trie.insert("apply")
trie.insert("application")
suggestions = trie.autocomplete("app")  # Returns ["apple", "apply", "application"]
suggestions = trie.autocomplete("app", limit=2)  # Returns first 2 suggestions
```

#### delete

```python
delete(word: str) -> bool
```

Delete word from trie.

**Parameters:**
- `word` (str): Word to delete

**Returns:**
- `bool`: True if word was deleted, False if word doesn't exist

**Time Complexity:** O(m) where m is word length

**Example:**
```python
trie = Trie()
trie.insert("apple")
result = trie.delete("apple")  # Returns True
result = trie.delete("orange")  # Returns False
```

#### count_words

```python
count_words() -> int
```

Get total number of words in trie.

**Returns:**
- `int`: Total number of words

**Time Complexity:** O(1)

**Example:**
```python
trie = Trie()
trie.insert("apple")
trie.insert("apply")
count = trie.count_words()  # Returns 2
```

#### count_words_with_prefix

```python
count_words_with_prefix(prefix: str) -> int
```

Count number of words with given prefix.

**Parameters:**
- `prefix` (str): Prefix to count words for

**Returns:**
- `int`: Number of words starting with prefix

**Time Complexity:** O(m) where m is prefix length

**Example:**
```python
trie = Trie()
trie.insert("apple")
trie.insert("apply")
trie.insert("application")
count = trie.count_words_with_prefix("app")  # Returns 3
```

#### get_all_words

```python
get_all_words() -> List[str]
```

Get all words in trie.

**Returns:**
- `List[str]`: List of all words

**Time Complexity:** O(n) where n is total number of characters

**Example:**
```python
trie = Trie()
trie.insert("apple")
trie.insert("apply")
words = trie.get_all_words()  # Returns ["apple", "apply"]
```

#### longest_common_prefix

```python
longest_common_prefix() -> str
```

Find longest common prefix of all words in trie.

**Returns:**
- `str`: Longest common prefix string

**Time Complexity:** O(m) where m is length of shortest word

**Example:**
```python
trie = Trie()
trie.insert("apple")
trie.insert("apply")
trie.insert("application")
prefix = trie.longest_common_prefix()  # Returns "app"
```

#### build_from_list

```python
build_from_list(words: List[str]) -> None
```

Build trie from list of words.

**Parameters:**
- `words` (List[str]): List of words to insert

**Time Complexity:** O(n * m) where n is number of words, m is average word length

**Example:**
```python
trie = Trie()
words = ["apple", "apply", "application"]
trie.build_from_list(words)
```

#### compare_performance

```python
compare_performance(
    words: List[str],
    prefix: str,
    iterations: int = 1
) -> Dict[str, any]
```

Compare performance of trie operations.

**Parameters:**
- `words` (List[str]): List of words to insert
- `prefix` (str): Prefix for autocomplete testing
- `iterations` (int): Number of iterations for timing. Default: 1

**Returns:**
- `Dict[str, any]`: Dictionary containing performance data for insert, search, autocomplete, and starts_with operations

**Example:**
```python
trie = Trie()
words = ["apple", "apply", "application"]
performance = trie.compare_performance(words, "app", iterations=1000)
print(performance["insert"]["time_milliseconds"])
```

#### generate_report

```python
generate_report(
    performance_data: Dict[str, any],
    output_path: Optional[str] = None
) -> str
```

Generate performance report for trie operations.

**Parameters:**
- `performance_data` (Dict[str, any]): Performance data from `compare_performance()`
- `output_path` (Optional[str]): Optional path to save report file

**Returns:**
- `str`: Report content as string

**Raises:**
- `IOError`: If file cannot be written
- `PermissionError`: If file is not writable

## TrieNode Class

Node in the trie data structure.

### Constructor

```python
TrieNode() -> None
```

Initialize TrieNode.

### Properties

- `children` (Dict[str, TrieNode]): Dictionary mapping characters to child nodes
- `is_end_of_word` (bool): Whether this node marks end of a word
- `word_count` (int): Number of words passing through this node

## Command-Line Interface

The module can be run as a script with the following interface:

```bash
python src/main.py WORDS [OPTIONS]
```

### Arguments

- `WORDS`: (Required) Words to insert into trie (space-separated)

### Options

- `-c, --config`: Path to configuration file (default: config.yaml)
- `-o, --operation`: Operation to perform - insert, search, autocomplete, prefix, compare, or all (default: all)
- `-p, --prefix`: Prefix for autocomplete or prefix check
- `-w, --word`: Word for search operation
- `-l, --limit`: Limit number of autocomplete suggestions
- `-i, --iterations`: Number of iterations for timing (default: 1)
- `-r, --report`: Output path for performance report

### Examples

```bash
# Insert words
python src/main.py apple apply application --operation insert

# Search for word
python src/main.py apple apply application --operation search --word apple

# Autocomplete
python src/main.py apple apply application --operation autocomplete --prefix app

# Check prefix
python src/main.py apple apply application --operation prefix --prefix app

# Compare performance
python src/main.py apple apply application --operation compare --prefix app --report report.txt
```

## Error Handling

All methods handle edge cases gracefully:

- Empty strings are ignored for insert
- Empty strings return False for search
- Empty prefix returns True for starts_with
- Empty prefix returns all words for autocomplete
- Non-existent words return False for search
- Non-existent prefixes return empty list for autocomplete

## Algorithm Complexity

### Time Complexity

- **Insert**: O(m) where m is word length
- **Search**: O(m) where m is word length
- **Starts With**: O(m) where m is prefix length
- **Autocomplete**: O(m + k) where m is prefix length, k is number of suggestions
- **Delete**: O(m) where m is word length
- **Count Words**: O(1)
- **Count Words With Prefix**: O(m) where m is prefix length
- **Get All Words**: O(n) where n is total number of characters
- **Longest Common Prefix**: O(m) where m is length of shortest word

### Space Complexity

- **Overall**: O(ALPHABET_SIZE * N * M) where N is number of words, M is average word length
- **Per Operation**: O(1) for most operations, O(k) for autocomplete where k is number of suggestions

## Notes

- Trie is optimal for prefix matching operations
- Search time is independent of dictionary size
- Space efficient for words with common prefixes
- Autocomplete can be limited for better performance
- Delete operation cleans up unused nodes
- Empty strings are handled gracefully
- Duplicate words are not stored multiple times
- All operations are case-sensitive
- Trie structure allows efficient prefix operations
