# Z-Algorithm for Pattern Matching with Linear Time Complexity

A Python implementation of Z-algorithm for pattern matching with O(n + m) time complexity where n is text length and m is pattern length. This tool supports both single and multiple pattern matching operations.

## Project Title and Description

The Z-Algorithm tool implements the Z-algorithm (also known as Z-box algorithm) for efficient pattern matching. The Z-algorithm constructs a Z-array where Z[i] is the length of the longest substring starting at position i that matches the prefix of the string, enabling linear-time pattern matching.

This tool solves the problem of efficient pattern matching in strings. Unlike naive pattern matching which requires O(nm) time, the Z-algorithm achieves O(n + m) time complexity, making it ideal for large-scale text processing and pattern matching applications.

**Target Audience**: Algorithm students, competitive programmers, text processing engineers, string algorithm researchers, bioinformatics researchers, and anyone interested in understanding linear-time pattern matching algorithms.

## Features

- Z-algorithm implementation with O(n + m) time complexity
- Single pattern matching
- Multiple pattern matching support
- Z-array computation
- Occurrence counting
- Longest repeated substring finding
- Longest prefix match queries
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
cd /path/to/python-algorithms/z-algorithm
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

Run the main script to see a demonstration of Z-algorithm operations:

```bash
python src/main.py
```

This will:
1. Create Z-algorithm instance with text
2. Search for single patterns
3. Search for multiple patterns
4. Find longest repeated substring
5. Display Z-array values

### Programmatic Usage

```python
from src.main import ZAlgorithm

# Create Z-algorithm instance
z_algo = ZAlgorithm("banana")

# Single pattern search
occurrences = z_algo.search("ana")  # Returns [1, 3]

# Count occurrences
count = z_algo.count_occurrences("ana")  # Returns 2

# Check if substring exists
is_sub = z_algo.is_substring("ana")  # Returns True

# Multiple pattern search
patterns = ["ana", "nan", "ban"]
results = z_algo.search_all(patterns)
# Returns {"ana": [1, 3], "nan": [2], "ban": [0]}

# Get Z-array
z_array = z_algo.get_z_array("ana")

# Find longest repeated substring
longest = z_algo.find_longest_repeated_substring()
```

### Common Use Cases

**Pattern Matching:**
1. Create Z-algorithm instance with text
2. Search for patterns efficiently
3. Get all occurrences in linear time

**Multiple Pattern Search:**
1. Create instance with text
2. Search for multiple patterns at once
3. Get results for all patterns

**String Analysis:**
1. Find longest repeated substrings
2. Analyze prefix matches
3. Count pattern occurrences

## Project Structure

```
z-algorithm/
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

- `src/main.py`: Contains `ZAlgorithm` class with all operations
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `logs/`: Directory for application log files

## Algorithm Details

### Z-Algorithm

**Definition:**
The Z-algorithm constructs a Z-array for a string where Z[i] is the length of the longest substring starting at position i that matches the prefix of the string.

**Properties:**
1. O(n) time complexity for Z-array construction
2. O(n + m) time complexity for pattern matching
3. Linear space complexity
4. Handles overlapping patterns efficiently

**Example (string = "aabxaabx"):**
```
Z-array: [0, 1, 0, 0, 4, 1, 0, 0]
         a  a  b  x  a  a  b  x
```

**Key Insight:**
The algorithm maintains a "Z-box" [left, right] representing the rightmost substring that matches the prefix. This allows efficient computation by reusing previously computed values.

### Pattern Matching

**Process:**
1. Concatenate pattern + separator + text
2. Compute Z-array for combined string
3. Find positions where Z[i] equals pattern length
4. These positions indicate pattern occurrences

**Time Complexity:** O(n + m) where n is text length, m is pattern length

### Multiple Pattern Matching

**Process:**
1. For each pattern, run Z-algorithm
2. Collect results for all patterns
3. Return dictionary mapping patterns to occurrences

**Time Complexity:** O(k(n + m)) where k is number of patterns

### Operations

**Search:**
- Time Complexity: O(n + m)
- Space Complexity: O(n + m)
- Returns all occurrence positions

**Search All:**
- Time Complexity: O(k(n + m))
- Space Complexity: O(n + m) per pattern
- Returns results for all patterns

**Z-Array Construction:**
- Time Complexity: O(n)
- Space Complexity: O(n)
- Uses Z-box optimization

### Edge Cases Handled

- Empty text (rejected)
- Empty pattern (rejected)
- Pattern longer than text
- Single character text
- Repeated characters
- Overlapping patterns
- Multiple patterns (some found, some not)

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
- Z-algorithm initialization
- Single pattern searching
- Multiple pattern searching
- Occurrence counting
- Z-array computation
- Longest repeated substring
- Edge cases (empty, single char, overlapping)
- Invalid input handling

## Troubleshooting

### Common Issues

**Pattern not found:**
- Verify pattern exists in text
- Check for case sensitivity
- Ensure pattern is not empty

**Incorrect occurrence positions:**
- Verify Z-array computation
- Check separator handling
- Validate position calculations

**Performance issues:**
- Z-algorithm is O(n + m) - should be fast
- Check for excessive logging
- Verify text length is reasonable

### Error Messages

**"Text cannot be empty"**: Must provide non-empty text string.

**"Pattern cannot be empty"**: Pattern must be non-empty for search operations.

**"Patterns list cannot be empty"**: Must provide at least one pattern for multiple pattern search.

### Best Practices

1. **Use for frequent searches** - Z-algorithm excels with many queries
2. **Leverage linear time** - O(n + m) is optimal for pattern matching
3. **Handle empty patterns** - Check for empty patterns before searching
4. **Use multiple pattern search** - Efficient for searching multiple patterns
5. **Consider text length** - Very long texts may require optimization

## Performance Characteristics

### Time Complexity

| Operation | Time Complexity |
|-----------|----------------|
| Z-Array Construction | O(n) |
| Single Pattern Search | O(n + m) |
| Multiple Pattern Search | O(k(n + m)) |
| Count Occurrences | O(n + m) |
| Longest Repeated Substring | O(n) |

Where:
- n = text length
- m = pattern length
- k = number of patterns

### Space Complexity

- Z-array storage: O(n + m)
- Text storage: O(n)
- Total: O(n + m)

## Applications

- **Text Processing**: Pattern matching in documents
- **Bioinformatics**: DNA/RNA sequence matching
- **String Algorithms**: Substring problems
- **Competitive Programming**: Pattern matching problems
- **Search Engines**: Fast pattern matching
- **Data Validation**: Pattern checking

## Comparison with Other Algorithms

**vs. Naive Pattern Matching:**
- Z-algorithm: O(n + m) time
- Naive: O(nm) time

**vs. KMP Algorithm:**
- Z-algorithm: Similar time complexity, different approach
- KMP: Preprocesses pattern, searches in text

**vs. Rabin-Karp:**
- Z-algorithm: Deterministic O(n + m)
- Rabin-Karp: Average O(n + m), worst O(nm)

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
