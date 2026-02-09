# API Documentation

## CharacterFrequencyAnalyzer Class

The main class for analyzing character frequency in strings using dictionary data structures.

### Methods

#### `__init__(config_path: str = "config.yaml")`

Initialize the CharacterFrequencyAnalyzer with configuration.

**Parameters:**
- `config_path` (str): Path to configuration YAML file. Defaults to "config.yaml".

**Raises:**
- `FileNotFoundError`: If config file doesn't exist.
- `yaml.YAMLError`: If config file is invalid YAML.
- `ValueError`: If configuration file is empty.

**Side Effects:**
- Loads configuration
- Sets up logging
- Initializes frequency data structures

#### `count_characters_dict(text: str) -> Dict[str, int]`

Count character occurrences using standard dictionary.

**Parameters:**
- `text` (str): String to analyze.

**Returns:**
- `Dict[str, int]`: Dictionary mapping characters to their counts.

**Time Complexity:** O(n)
**Space Complexity:** O(k) where k is number of unique characters

**Example:**
```python
analyzer = CharacterFrequencyAnalyzer()
frequency = analyzer.count_characters_dict("hello")
print(frequency)  # {'h': 1, 'e': 1, 'l': 2, 'o': 1}
```

#### `count_characters_defaultdict(text: str) -> Dict[str, int]`

Count character occurrences using defaultdict.

**Parameters:**
- `text` (str): String to analyze.

**Returns:**
- `Dict[str, int]`: Dictionary mapping characters to their counts.

**Time Complexity:** O(n)
**Space Complexity:** O(k)

**Example:**
```python
analyzer = CharacterFrequencyAnalyzer()
frequency = analyzer.count_characters_defaultdict("hello")
print(frequency)  # {'h': 1, 'e': 1, 'l': 2, 'o': 1}
```

#### `count_characters_counter(text: str) -> Dict[str, int]`

Count character occurrences using Counter.

**Parameters:**
- `text` (str): String to analyze.

**Returns:**
- `Dict[str, int]`: Dictionary mapping characters to their counts.

**Time Complexity:** O(n)
**Space Complexity:** O(k)

**Example:**
```python
analyzer = CharacterFrequencyAnalyzer()
frequency = analyzer.count_characters_counter("hello")
print(frequency)  # {'h': 1, 'e': 1, 'l': 2, 'o': 1}
```

#### `get_frequency_analysis() -> Dict[str, any]`

Get detailed frequency analysis.

**Returns:**
- `Dict[str, any]`: Dictionary containing analysis data with keys:
  - `total_characters`: Total number of characters
  - `unique_characters`: Number of unique characters
  - `most_common`: Tuple of (character, count) for most common
  - `least_common`: Tuple of (character, count) for least common
  - `average_frequency`: Average frequency per character
  - `frequency_distribution`: List of (char, count) tuples sorted by frequency
  - `character_percentages`: Dictionary mapping characters to percentages

**Example:**
```python
analyzer.count_characters_dict("hello")
analysis = analyzer.get_frequency_analysis()
print(f"Most common: {analysis['most_common']}")
print(f"Unique chars: {analysis['unique_characters']}")
```

#### `get_top_characters(n: int = 10) -> List[tuple]`

Get top N most frequent characters.

**Parameters:**
- `n` (int): Number of top characters to return. Default: 10.

**Returns:**
- `List[tuple]`: List of tuples (character, count) sorted by frequency (descending).

**Example:**
```python
analyzer.count_characters_dict("hello world")
top = analyzer.get_top_characters(3)
print(top)  # [('l', 3), ('o', 2), ('h', 1)]
```

#### `get_character_info(char: str) -> Optional[Dict[str, any]]`

Get detailed information about a specific character.

**Parameters:**
- `char` (str): Character to get information for.

**Returns:**
- `Optional[Dict[str, any]]`: Dictionary with character information or None if not found. Contains:
  - `character`: The character itself
  - `count`: Number of occurrences
  - `percentage`: Percentage of total characters
  - `unicode_code`: Unicode code point
  - `is_whitespace`: Whether character is whitespace
  - `is_alphanumeric`: Whether character is alphanumeric
  - `is_alpha`: Whether character is alphabetic
  - `is_digit`: Whether character is a digit

**Example:**
```python
analyzer.count_characters_dict("hello")
info = analyzer.get_character_info("l")
print(f"Count: {info['count']}, Percentage: {info['percentage']:.2f}%")
```

#### `generate_report(output_path: Optional[str] = None) -> str`

Generate frequency analysis report.

**Parameters:**
- `output_path` (Optional[str]): Optional path to save report file.

**Returns:**
- `str`: Report content as string.

**Report Contents:**
- Summary statistics
- Most and least common characters
- Top 10 most frequent characters
- Complete frequency distribution
- Character percentages

**Example:**
```python
analyzer.count_characters_dict("hello")
report = analyzer.generate_report(output_path="report.txt")
print(report)
```

### Attributes

#### `frequency_data: Dict[str, int]`

Dictionary containing character frequency counts from the last analysis.

#### `analysis_stats: Dict[str, any]`

Dictionary containing analysis statistics including totals, most/least common, and averages.

#### `config: dict`

Configuration dictionary loaded from YAML file.

### Example Usage

```python
from src.main import CharacterFrequencyAnalyzer

# Initialize with default config
analyzer = CharacterFrequencyAnalyzer()

# Or with custom config
analyzer = CharacterFrequencyAnalyzer(config_path="custom_config.yaml")

# Count characters using different methods
frequency = analyzer.count_characters_dict("hello world")
frequency = analyzer.count_characters_defaultdict("hello world")
frequency = analyzer.count_characters_counter("hello world")

# Get analysis
analysis = analyzer.get_frequency_analysis()
print(f"Most common: {analysis['most_common']}")

# Get top characters
top = analyzer.get_top_characters(5)

# Get character info
info = analyzer.get_character_info("l")

# Generate report
report = analyzer.generate_report(output_path="analysis.txt")
```

### Algorithm Complexity

**All Methods:**
- Time Complexity: O(n) - single pass through string
- Space Complexity: O(k) where k is number of unique characters

**Method Comparison:**
- Dictionary: Manual key checking, explicit code
- DefaultDict: Automatic initialization, cleaner code
- Counter: Most Pythonic, optimized implementation

**Characteristics:**
- All methods produce identical results
- Same time and space complexity
- Different code styles and readability
- Counter is generally preferred for production code

### Performance Notes

- All three methods have identical performance characteristics
- Dictionary operations are O(1) average case
- Space usage depends on number of unique characters
- Works with any Unicode characters
- Handles special characters, whitespace, and control characters
