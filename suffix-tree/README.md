# Suffix Tree Construction Using Ukkonen's Algorithm

A Python implementation of suffix tree construction using Ukkonen's algorithm for efficient substring matching. This tool provides O(n) time construction and O(m) substring queries where n is the text length and m is the pattern length.

## Project Title and Description

The Suffix Tree tool implements a suffix tree data structure using Ukkonen's linear-time algorithm. A suffix tree is a compressed trie containing all suffixes of a given text, enabling extremely fast substring queries, pattern matching, and various string processing operations.

This tool solves the problem of efficient substring matching and pattern searching in text. Suffix trees are widely used in bioinformatics (DNA sequence analysis), text editors (find and replace), data compression, and string algorithms.

**Target Audience**: Bioinformatics researchers, text processing engineers, algorithm students, competitive programmers, string algorithm researchers, and anyone interested in understanding advanced string data structures and Ukkonen's algorithm.

## Features

- Suffix tree construction using Ukkonen's O(n) algorithm
- Efficient substring search in O(m) time
- Find all occurrences of a pattern
- Count substring occurrences
- Find longest repeated substring
- Check if pattern is a suffix
- Get all suffixes of the text
- Tree structure validation
- Comprehensive edge case handling
- Detailed step-by-step logging
- Input validation
- Error handling for invalid inputs

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

### Step 1: Navigate to Project Directory

```bash
cd /path/to/python-algorithms/suffix-tree
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
python src/main.py
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

### Basic Usage

Run the main script to see a demonstration of suffix tree operations:

```bash
python src/main.py
```

This will:
1. Build a suffix tree for the text "banana"
2. Display tree properties
3. Search for various patterns
4. Find all occurrences of patterns
5. Find longest repeated substring

### Programmatic Usage

```python
from src.main import SuffixTree

# Create suffix tree
tree = SuffixTree("banana")

# Search for pattern
found = tree.search("ana")  # Returns True

# Find all occurrences
occurrences = tree.find_all_occurrences("ana")  # Returns [1, 3]

# Count occurrences
count = tree.get_substring_count("an")  # Returns 2

# Find longest repeated substring
longest = tree.get_longest_repeated_substring()  # Returns "ana"

# Check if pattern is suffix
is_suffix = tree.is_suffix("ana")  # Returns True

# Get all suffixes
suffixes = tree.get_all_suffixes()

# Get tree properties
size = tree.get_tree_size()
is_valid = tree.is_valid()  # Validates tree structure
```

### Common Use Cases

**Pattern Matching:**
1. Build suffix tree for text
2. Search for patterns
3. Find all occurrences efficiently

**DNA Sequence Analysis:**
1. Build suffix tree for DNA sequence
2. Search for genetic patterns
3. Find repeated sequences

**Text Processing:**
1. Build suffix tree for document
2. Find all occurrences of words/phrases
3. Analyze text patterns

## Project Structure

```
suffix-tree/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── config.yaml              # Configuration file
├── .gitignore               # Git ignore patterns
├── src/
│   └── main.py           # Main application code
├── tests/
│   └── test_main.py         # Unit tests
├── docs/
│   └── API.md               # API documentation
└── logs/
    └── .gitkeep             # Placeholder for logs directory
```

### File Descriptions

- `src/main.py`: Contains `SuffixTree` and `SuffixTreeNode` classes with Ukkonen's algorithm
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `logs/`: Directory for application log files

## Algorithm Details

### Suffix Tree

**Definition:**
A suffix tree is a compressed trie containing all suffixes of a given text. Each edge is labeled with a substring, and each path from root to leaf represents a suffix of the text.

**Properties:**
1. Contains all suffixes of the text
2. Each internal node has at least 2 children
3. Edges are labeled with substrings
4. Leaves represent suffix starting positions
5. O(n) space complexity

**Example (text = "banana"):**
```
        (root)
       /  |  \
      b   a   n
     /    |    \
    an    na   ana
   /  \    |     \
  ana$ na$  na$   na$
```

### Ukkonen's Algorithm

**Overview:**
Ukkonen's algorithm constructs a suffix tree in O(n) time using an online approach, processing characters one at a time.

**Key Concepts:**

1. **Active Point**: Tracks current position in tree
   - `active_node`: Current node
   - `active_edge`: Character index for edge
   - `active_length`: Length along current edge

2. **Extension Rules**:
   - **Rule 1**: Path ends at leaf - extend leaf
   - **Rule 2**: Path ends at internal node - create new leaf
   - **Rule 3**: Path already exists - no extension needed

3. **Suffix Links**: Links from internal nodes to other nodes representing shorter suffixes

4. **Phases and Extensions**: 
   - Phase i processes character at position i
   - Extension j processes suffix starting at position j

**Time Complexity:**
- Construction: O(n) where n is text length
- Space: O(n)

**Advantages:**
- Linear time construction
- Online algorithm (processes one character at a time)
- Efficient for large texts
- Enables fast substring queries

### Operations

**Search:**
- Time Complexity: O(m) where m is pattern length
- Space Complexity: O(1)
- Traverse tree following pattern characters

**Find All Occurrences:**
- Time Complexity: O(m + k) where k is number of occurrences
- Space Complexity: O(k)
- Find pattern node, then collect all leaf indices

**Longest Repeated Substring:**
- Time Complexity: O(n)
- Space Complexity: O(n)
- Find deepest internal node with multiple children

**Count Occurrences:**
- Time Complexity: O(m + k)
- Space Complexity: O(1)
- Find pattern and count leaves in subtree

### Edge Cases Handled

- Empty text (raises ValueError)
- Single character text
- Repeated characters
- No repeated substrings
- Overlapping patterns
- Patterns at text boundaries
- Empty pattern searches
- Very long texts

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
- Suffix tree construction
- Pattern searching
- Finding all occurrences
- Counting occurrences
- Longest repeated substring
- Suffix checking
- Tree validation
- Edge cases (empty text, single char, repeated chars)
- Various text patterns

## Troubleshooting

### Common Issues

**Tree construction fails:**
- Verify text is not empty
- Check for proper initialization
- Review active point management

**Search returns incorrect results:**
- Verify tree was built correctly
- Check pattern matching logic
- Validate pattern characters

**Performance issues with large texts:**
- This is expected - suffix trees use O(n) space
- Consider using suffix arrays for very large texts
- Monitor memory usage

### Error Messages

**"Text cannot be empty"**: Attempted to create suffix tree with empty string. Provide a non-empty text string.

**Pattern not found**: The pattern does not exist in the text. This is expected behavior for non-existent patterns.

### Best Practices

1. **Use for frequent substring queries** - Suffix trees excel when many queries are needed
2. **Consider space trade-off** - O(n) space may be large for very long texts
3. **Use sentinel character** - Algorithm uses '$' to mark end of text
4. **Validate tree structure** - Use is_valid() to verify tree correctness
5. **Handle empty patterns** - Empty pattern matches all positions
6. **Monitor memory** - Large texts require significant memory

## Performance Characteristics

### Time Complexity

| Operation | Time Complexity |
|-----------|----------------|
| Construction | O(n) |
| Search | O(m) |
| Find All Occurrences | O(m + k) |
| Count Occurrences | O(m + k) |
| Longest Repeated Substring | O(n) |
| Is Suffix | O(m) |

Where:
- n = text length
- m = pattern length
- k = number of occurrences

### Space Complexity

- Tree storage: O(n)
- Auxiliary space: O(1) per operation
- Total: O(n)

## Applications

- **Bioinformatics**: DNA/RNA sequence analysis, pattern matching
- **Text Processing**: Find and replace, text search engines
- **Data Compression**: LZ77, LZ78 algorithms
- **String Algorithms**: Longest common substring, palindrome detection
- **Information Retrieval**: Full-text search, document indexing

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
