# Suffix Array Construction with Longest Common Prefix (LCP) Array

A Python implementation of suffix array construction with longest common prefix (LCP) array computation. This tool provides efficient string processing capabilities including pattern matching, longest common substring finding, and substring queries.

## Project Title and Description

The Suffix Array tool implements suffix array construction and LCP array computation for efficient string processing. A suffix array is a sorted array of all suffixes of a string, enabling O(m log n) pattern matching where m is pattern length and n is text length. The LCP array stores the longest common prefix between consecutive suffixes, enabling additional efficient operations.

This tool solves the problem of efficient string processing including pattern matching, longest common substring finding, and substring analysis. Suffix arrays are more space-efficient than suffix trees while providing similar capabilities, making them ideal for large-scale string processing applications.

**Target Audience**: Bioinformatics researchers, text processing engineers, algorithm students, competitive programmers, string algorithm researchers, and anyone interested in understanding suffix arrays and LCP arrays.

## Features

- Suffix array construction from text
- LCP array computation using Kasai's algorithm
- Pattern search using binary search
- Longest common substring finding
- Inverse suffix array computation
- Suffix retrieval and iteration
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
cd /path/to/python-algorithms/suffix-array
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

Run the main script to see a demonstration of suffix array operations:

```bash
python src/main.py
```

This will:
1. Build suffix array from text
2. Compute LCP array
3. Display suffix array and LCP array
4. Search for patterns
5. Find longest common substring

### Programmatic Usage

```python
from src.main import SuffixArray

# Create suffix array
sa = SuffixArray("banana")

# Get suffix array
suffix_array = sa.get_suffix_array()  # [6, 5, 3, 1, 0, 4, 2]

# Get LCP array
lcp_array = sa.get_lcp_array()  # [0, 0, 1, 3, 0, 0, 2]

# Search for pattern
occurrences = sa.search("ana")  # Returns [1, 3]

# Get longest common substring
longest = sa.get_longest_common_substring()  # Returns "ana"

# Get suffix at index
suffix = sa.get_suffix(0)  # Returns "$"

# Get LCP between two suffixes
lcp = sa.get_lcp(0, 1)  # Returns LCP length
```

### Common Use Cases

**Pattern Matching:**
1. Build suffix array for text
2. Search for patterns using binary search
3. Get all occurrences efficiently

**Longest Common Substring:**
1. Build suffix array
2. Compute LCP array
3. Find maximum LCP value
4. Extract longest common substring

**String Analysis:**
1. Build suffix array
2. Analyze suffix ordering
3. Compute LCP values
4. Find repeated substrings

## Project Structure

```
suffix-array/
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

- `src/main.py`: Contains `SuffixArray` class with all operations
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `logs/`: Directory for application log files

## Algorithm Details

### Suffix Array

**Definition:**
A suffix array is a sorted array of all suffixes of a string. For string S of length n, the suffix array SA is an array of integers where SA[i] is the starting position of the i-th smallest suffix.

**Properties:**
1. Contains all suffixes in sorted order
2. O(n log n) construction time
3. O(n) space complexity
4. Enables efficient pattern matching

**Example (text = "banana"):**
```
Suffix Array: [6, 5, 3, 1, 0, 4, 2]
Suffixes:     ["$", "a$", "ana$", "anana$", "banana$", "na$", "nana$"]
```

### LCP Array

**Definition:**
The LCP array stores the longest common prefix between consecutive suffixes in the suffix array. LCP[i] is the length of the longest common prefix between SA[i] and SA[i-1].

**Properties:**
1. LCP[0] = 0 (first suffix has no predecessor)
2. O(n) construction time using Kasai's algorithm
3. Enables efficient longest common substring finding
4. Useful for string analysis

**Example:**
```
LCP Array: [0, 0, 1, 3, 0, 0, 2]
```

### Kasai's Algorithm

**Overview:**
Kasai's algorithm constructs the LCP array in O(n) time by traversing the text once and using the inverse suffix array.

**Steps:**
1. Build inverse suffix array
2. Traverse text from left to right
3. For each position, compute LCP with next suffix
4. Use previous LCP value to optimize

**Time Complexity:** O(n)

### Operations

**Construction:**
- Time Complexity: O(n log n) for sorting
- Space Complexity: O(n)
- Sorts all suffixes lexicographically

**Pattern Search:**
- Time Complexity: O(m log n) where m is pattern length
- Uses binary search on suffix array
- Returns all occurrences

**LCP Computation:**
- Time Complexity: O(n)
- Uses Kasai's algorithm
- Linear time construction

**Longest Common Substring:**
- Time Complexity: O(n)
- Finds maximum LCP value
- Extracts substring

### Edge Cases Handled

- Empty text (rejected)
- Single character text
- Repeated characters
- Long texts
- Patterns at boundaries
- Empty patterns
- Non-existent patterns

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
- Suffix array construction
- LCP array computation
- Pattern searching
- Longest common substring finding
- Suffix retrieval
- Edge cases (empty, single char, repeated chars)
- Invalid input handling
- Validation

## Troubleshooting

### Common Issues

**Incorrect suffix array:**
- Verify sorting is correct
- Check sentinel character handling
- Ensure all suffixes are included

**Incorrect LCP array:**
- Verify Kasai's algorithm implementation
- Check inverse suffix array
- Validate LCP computation

**Search not finding patterns:**
- Verify binary search implementation
- Check pattern matching logic
- Ensure sentinel is handled correctly

### Error Messages

**"Text cannot be empty"**: Must provide non-empty text string.

**"Index out of range"**: Index must be in valid range for suffix array.

**"Indices out of range"**: Both indices must be valid for LCP query.

### Best Practices

1. **Use for large texts** - Suffix arrays are efficient for long strings
2. **Leverage LCP array** - Use for longest common substring problems
3. **Binary search** - Pattern search uses binary search efficiently
4. **Validate structure** - Use is_valid() to verify correctness
5. **Consider space** - O(n) space for n-length string

## Performance Characteristics

### Time Complexity

| Operation | Time Complexity |
|-----------|----------------|
| Construction | O(n log n) |
| LCP Computation | O(n) |
| Pattern Search | O(m log n) |
| Longest Common Substring | O(n) |
| Get Suffix | O(1) |
| Get LCP | O(j - i) |

Where:
- n = text length
- m = pattern length
- i, j = suffix array indices

### Space Complexity

- Suffix array: O(n)
- LCP array: O(n)
- Inverse suffix array: O(n)
- Total: O(n)

## Applications

- **Bioinformatics**: DNA/RNA sequence analysis
- **Text Processing**: Pattern matching
- **Data Compression**: LZ77, LZ78 algorithms
- **String Algorithms**: Longest common substring, repeated substrings
- **Information Retrieval**: Full-text search, document indexing
- **Competitive Programming**: String problems

## Comparison with Other Structures

**vs. Suffix Tree:**
- Suffix array: More space-efficient, simpler structure
- Suffix tree: Faster queries, more complex

**vs. Naive Pattern Matching:**
- Suffix array: O(m log n) search
- Naive: O(nm) search

**vs. KMP Algorithm:**
- Suffix array: Preprocess text once, query multiple patterns
- KMP: Preprocess pattern, search in text

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
