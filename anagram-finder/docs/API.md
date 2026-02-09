# Anagram Finder API Documentation

## Overview

The Anagram Finder provides efficient anagram detection using character frequency comparison and hash-based grouping. It groups words that are anagrams of each other by analyzing character frequencies and using hash keys for efficient grouping.

## Classes

### AnagramFinder

Main class for finding anagrams using character frequency and hash-based grouping.

#### Constructor

```python
AnagramFinder(config_path: str = "config.yaml") -> None
```

Initialize finder with configuration.

**Parameters:**
- `config_path` (str): Path to configuration YAML file. Default: "config.yaml"

**Raises:**
- `FileNotFoundError`: If config file doesn't exist
- `yaml.YAMLError`: If config file is invalid YAML

#### Methods

##### find_anagrams

```python
find_anagrams(words: List[str], case_sensitive: bool = False) -> Dict[str, List[str]]
```

Find all anagrams in a list using hash-based grouping.

**Parameters:**
- `words` (List[str]): List of strings to analyze
- `case_sensitive` (bool): If True, consider case when comparing

**Returns:**
- `Dict[str, List[str]]`: Dictionary mapping hash keys to lists of anagram groups

**Example:**
```python
finder = AnagramFinder()
result = finder.find_anagrams(["listen", "silent", "enlist"])
# Returns: {hash_key: ["listen", "silent", "enlist"]}
```

##### find_anagrams_detailed

```python
find_anagrams_detailed(
    words: List[str], case_sensitive: bool = False
) -> Dict[str, Dict[str, any]]
```

Find anagrams with detailed analysis.

**Parameters:**
- `words` (List[str]): List of strings to analyze
- `case_sensitive` (bool): If True, consider case when comparing

**Returns:**
- `Dict[str, Dict[str, any]]`: Dictionary with detailed anagram information

**Example:**
```python
result = finder.find_anagrams_detailed(["listen", "silent", "cat", "act"])
# Returns: {
#   'groups': {...},
#   'statistics': {...},
#   'character_frequencies': {...}
# }
```

##### find_anagrams_for_word

```python
find_anagrams_for_word(target_word: str, word_list: List[str]) -> List[str]
```

Find all anagrams of a specific word in a list.

**Parameters:**
- `target_word` (str): Word to find anagrams for
- `word_list` (List[str]): List of words to search in

**Returns:**
- `List[str]`: List of words that are anagrams of target_word

**Example:**
```python
anagrams = finder.find_anagrams_for_word("listen", ["silent", "enlist", "cat"])
# Returns: ["silent", "enlist"]
```

##### get_character_frequency_analysis

```python
get_character_frequency_analysis(word: str) -> Dict[str, any]
```

Get detailed character frequency analysis for a word.

**Parameters:**
- `word` (str): Input string

**Returns:**
- `Dict[str, any]`: Dictionary with frequency analysis

**Example:**
```python
analysis = finder.get_character_frequency_analysis("hello")
# Returns: {
#   'word': 'hello',
#   'frequencies': {'h': 1, 'e': 1, 'l': 2, 'o': 1},
#   'hash_key': '...',
#   ...
# }
```

##### generate_report

```python
generate_report(
    result: Dict[str, Dict[str, any]], output_path: Optional[str] = None
) -> str
```

Generate detailed anagram analysis report.

**Parameters:**
- `result` (Dict[str, Dict[str, any]]): Result dictionary from find_anagrams_detailed
- `output_path` (Optional[str]): Optional path to save report file

**Returns:**
- `str`: Report content as string

## Algorithm Details

### Character Frequency Comparison

- Count frequency of each character in each word
- Normalize to lowercase for case-insensitive comparison
- Two words are anagrams if they have same character frequencies

### Hash-Based Grouping

- Generate hash key from sorted character frequencies
- Group words with same hash key together
- Hash key format: sorted characters with their counts

### Time Complexity

- **O(n * m)** where:
  - n = number of words
  - m = average word length

### Space Complexity

- **O(n * m)** for storing groups and frequencies

## Usage Examples

### Basic Anagram Finding

```python
from src.main import AnagramFinder

finder = AnagramFinder()
result = finder.find_anagrams(["listen", "silent", "enlist"])
print(result)
```

### Detailed Analysis

```python
finder = AnagramFinder()
result = finder.find_anagrams_detailed(["listen", "silent", "cat", "act"])
print(result["statistics"])
```

### Find Anagrams for Specific Word

```python
finder = AnagramFinder()
anagrams = finder.find_anagrams_for_word("listen", ["silent", "enlist", "cat"])
print(anagrams)
```

### Character Frequency Analysis

```python
finder = AnagramFinder()
analysis = finder.get_character_frequency_analysis("hello")
print(analysis["frequencies"])
```
