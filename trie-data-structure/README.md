# Trie (Prefix Tree) Data Structure

A Python implementation of trie (prefix tree) data structure for efficient string prefix matching and autocomplete operations. This tool provides fast string operations including insertion, search, prefix matching, and autocomplete suggestions.

## Project Title and Description

The Trie Data Structure tool implements a prefix tree that stores strings in a tree-like structure where each node represents a character. This allows for efficient prefix searches, autocomplete functionality, and string matching operations. Tries are particularly useful for applications requiring fast prefix lookups.

This tool solves the problem of efficiently storing and searching strings, especially when prefix matching is required. Tries are widely used in autocomplete systems, spell checkers, IP routing, and search engines.

**Target Audience**: Students learning data structures, developers studying trie implementations, software engineers building autocomplete features, educators teaching computer science concepts, and anyone interested in understanding efficient string operations and prefix matching.

## Features

- Trie data structure implementation
- Word insertion and deletion
- Exact word search
- Prefix matching (starts_with)
- Autocomplete with configurable limit
- Word counting and prefix counting
- Longest common prefix finding
- Performance comparison and analysis
- Comprehensive edge case handling
- Detailed step-by-step logging
- Multiple iterations support for accurate timing
- Input validation
- Error handling for invalid inputs

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

### Step 1: Navigate to Project Directory

```bash
cd /path/to/python-algorithms/trie-data-structure
```

### Step 2: Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Verify Installation

```bash
python src/main.py --help
```

## Configuration

### Configuration File (config.yaml)

The tool uses a YAML configuration file to define logging settings. The default configuration file is `config.yaml` in the project root.

#### Key Configuration Options

**Logging Settings:**
- `logging.level`: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `logging.file`: Path to log file (default: "logs/app.log")

### Example Configuration

```yaml
logging:
  level: "INFO"
  file: "logs/app.log"
```

### Environment Variables

No environment variables are currently required. All configuration is managed through the `config.yaml` file.

## Usage

### Insert Words

Insert words into trie:

```bash
python src/main.py apple apply application --operation insert
```

### Search for Word

Search for exact word:

```bash
python src/main.py apple apply application --operation search --word apple
```

### Autocomplete

Get autocomplete suggestions:

```bash
python src/main.py apple apply application app --operation autocomplete --prefix app
```

### Check Prefix

Check if prefix exists:

```bash
python src/main.py apple apply application --operation prefix --prefix app
```

### All Operations

Perform all operations:

```bash
python src/main.py apple apply application app --operation all --prefix app --word apple
```

### Performance Comparison

Compare performance of operations:

```bash
python src/main.py apple apply application app --operation compare --prefix app --iterations 1000
```

### Generate Report

Generate performance report:

```bash
python src/main.py apple apply application app --operation compare --prefix app --report report.txt
```

### Command-Line Arguments

- `words`: (Required) Words to insert into trie (space-separated)
- `-c, --config`: Path to configuration file (default: config.yaml)
- `-o, --operation`: Operation to perform - insert, search, autocomplete, prefix, compare, or all (default: all)
- `-p, --prefix`: Prefix for autocomplete or prefix check
- `-w, --word`: Word for search operation
- `-l, --limit`: Limit number of autocomplete suggestions
- `-i, --iterations`: Number of iterations for timing (default: 1)
- `-r, --report`: Output path for performance report

### Common Use Cases

**Autocomplete System:**
1. Build trie with dictionary: `python src/main.py word1 word2 word3 ... --operation insert`
2. Get suggestions: `python src/main.py ... --operation autocomplete --prefix "user_input"`
3. Display suggestions to user

**Prefix Matching:**
1. Insert words: `python src/main.py apple apply application --operation insert`
2. Check prefix: `python src/main.py ... --operation prefix --prefix app`
3. Count words with prefix

**Word Search:**
1. Build trie: `python src/main.py word1 word2 word3 --operation insert`
2. Search: `python src/main.py ... --operation search --word word1`
3. Verify word exists

**Performance Analysis:**
1. Test with large dictionary
2. Compare operations: `python src/main.py ... --operation compare --iterations 1000`
3. Generate reports for detailed metrics

## Project Structure

```
trie-data-structure/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── config.yaml              # Configuration file
├── .gitignore               # Git ignore patterns
├── src/
│   └── main.py              # Main application code
├── tests/
│   └── test_main.py         # Unit tests
├── docs/
│   └── API.md               # API documentation
└── logs/
    └── .gitkeep             # Placeholder for logs directory
```

### File Descriptions

- `src/main.py`: Contains `Trie` and `TrieNode` classes
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `logs/`: Directory for application log files

## Algorithm Details

### Trie Data Structure

**Definition:**
A trie (prefix tree) is a tree-like data structure that stores strings. Each node represents a character, and paths from root to nodes represent strings. Nodes can be marked to indicate end of words.

**Structure:**
- Root node (empty)
- Each node has children (characters)
- Nodes can be marked as end of word
- Paths represent strings

**Example:**
```
        root
       /    \
      a      b
     / \      \
    p   n      a
   /     \      \
  p       t      t
 /         \
l           h
e           e
```

**Applications:**
- Autocomplete systems
- Spell checkers
- IP routing (longest prefix matching)
- Search engines
- Phone directory
- Text editors

### Operations

**Insert:**
- Time Complexity: O(m) where m is word length
- Space Complexity: O(m)
- Traverse/create path character by character

**Search:**
- Time Complexity: O(m) where m is word length
- Space Complexity: O(1)
- Traverse path and check end marker

**Prefix Matching:**
- Time Complexity: O(m) where m is prefix length
- Space Complexity: O(1)
- Traverse path to prefix

**Autocomplete:**
- Time Complexity: O(m + k) where m is prefix length, k is number of suggestions
- Space Complexity: O(k)
- Traverse to prefix, then collect all words

**Delete:**
- Time Complexity: O(m) where m is word length
- Space Complexity: O(1)
- Traverse path, remove end marker, clean up unused nodes

### Advantages

- Fast prefix matching (O(m) independent of dictionary size)
- Efficient autocomplete
- Space efficient for common prefixes
- O(m) search time independent of number of words
- Natural for string operations

### Disadvantages

- Can use significant memory for sparse tries
- More complex than hash tables
- Slower than hash tables for exact matches (if no prefix needed)

### Edge Cases Handled

- Empty strings
- Single character words
- Duplicate words
- Words with common prefixes
- Words with no common prefixes
- Very long words
- Large dictionaries
- Empty prefix autocomplete
- Non-existent words
- Non-existent prefixes

## Testing

### Run Tests

```bash
python -m pytest tests/
```

### Run Tests with Coverage

```bash
python -m pytest tests/ --cov=src --cov-report=html
```

### Test Coverage

The test suite aims for minimum 80% code coverage, testing:
- Trie insertion and search
- Prefix matching
- Autocomplete functionality
- Word deletion
- Edge cases (empty strings, duplicates, non-existent words)
- Performance comparison functionality
- Error handling
- Report generation
- Input validation

## Troubleshooting

### Common Issues

**Empty autocomplete results:**
- Prefix may not exist in trie
- Check that words were inserted correctly
- Verify prefix spelling

**Word not found:**
- Word may not have been inserted
- Check spelling
- Verify insertion was successful

**Import Errors:**
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (requires 3.8+)
- Verify virtual environment is activated

### Error Messages

**"Configuration file not found"**: The config.yaml file doesn't exist. Create it or specify path with `-c` option.

### Best Practices

1. **Use trie for prefix operations** - More efficient than linear search
2. **Consider memory usage** - Tries can use significant memory
3. **Use autocomplete limits** - Limit suggestions for better performance
4. **Handle empty results** - Autocomplete may return empty list
5. **Clean up unused nodes** - Delete operation removes unused nodes
6. **Use for large dictionaries** - Trie excels with many words
7. **Consider alternatives** - Hash tables may be better for exact matches only

## Contributing

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Make your changes following PEP 8 style guidelines
4. Add tests for new functionality
5. Ensure all tests pass: `pytest tests/`
6. Submit a pull request

### Code Style Guidelines

- Follow PEP 8 strictly
- Maximum line length: 88 characters
- Use type hints for all functions
- Include docstrings for all public functions and classes
- Use meaningful variable names
- Write tests for all new functionality

### Pull Request Process

1. Ensure code follows project standards
2. Update documentation if needed
3. Add/update tests
4. Ensure all tests pass
5. Submit PR with clear description of changes

## License

This project is part of the python-algorithms collection. Please refer to the parent repository for license information.
