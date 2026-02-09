# KMP (Knuth-Morris-Pratt) Algorithm for Pattern Matching

A Python implementation of the KMP (Knuth-Morris-Pratt) algorithm for pattern matching with failure function optimization. The KMP algorithm achieves O(n + m) time complexity where n is text length and m is pattern length by using a failure function to avoid unnecessary character comparisons.

## Project Title and Description

The KMP Algorithm tool implements the Knuth-Morris-Pratt algorithm for efficient pattern matching. Unlike naive pattern matching which requires O(nm) time, the KMP algorithm achieves O(n + m) time complexity by preprocessing the pattern to build a failure function (LPS array) that allows skipping characters when a mismatch occurs.

This tool solves the problem of efficient pattern matching in strings. The KMP algorithm is particularly useful when searching for the same pattern multiple times or when patterns have repeating substrings, as it avoids redundant comparisons by using the failure function.

**Target Audience**: Algorithm students, competitive programmers, text processing engineers, string algorithm researchers, bioinformatics researchers, and anyone interested in understanding linear-time pattern matching algorithms.

## Features

- KMP algorithm implementation with O(n + m) time complexity
- Failure function (LPS array) construction
- Single pattern matching
- Multiple pattern matching support
- Occurrence counting
- Failure function analysis
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
cd /path/to/python-algorithms/kmp-algorithm
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

Run the main script to see a demonstration of KMP algorithm operations:

```bash
python src/main.py
```

This will:
1. Create KMP algorithm instance with text
2. Search for single patterns
3. Display failure functions
4. Search for multiple patterns
5. Show occurrence counts

### Programmatic Usage

```python
from src.main import KMPAlgorithm

# Create KMP algorithm instance
kmp = KMPAlgorithm("ABABDABACDABABCABCAB")

# Single pattern search
occurrences = kmp.search("ABABCABCAB")  # Returns [10]

# Count occurrences
count = kmp.count_occurrences("ABAB")  # Returns 2

# Check if substring exists
is_sub = kmp.is_substring("ABC")  # Returns True

# Get failure function
lps = kmp.get_failure_function("ABABCABCAB")
# Returns [0, 0, 1, 2, 0, 1, 2, 3, 4, 0]

# Multiple pattern search
patterns = ["ABAB", "ABC", "AB"]
results = kmp.search_all(patterns)
# Returns {"ABAB": [0, 4], "ABC": [12, 15], "AB": [0, 2, 4, ...]}
```

### Common Use Cases

**Pattern Matching:**
1. Create instance with text
2. Search for patterns efficiently
3. Get all occurrences in linear time

**Multiple Pattern Search:**
1. Create instance with text
2. Search for multiple patterns at once
3. Get results for all patterns

**Failure Function Analysis:**
1. Get failure function for pattern
2. Analyze pattern structure
3. Understand algorithm behavior

## Project Structure

```
kmp-algorithm/
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

- `src/main.py`: Contains `KMPAlgorithm` class with all operations
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `logs/`: Directory for application log files

## Algorithm Details

### KMP Algorithm

**Definition:**
The KMP algorithm preprocesses the pattern to build a failure function (LPS - Longest Proper Prefix which is also a Suffix) that allows skipping characters when a mismatch occurs, achieving O(n + m) time complexity.

**Properties:**
1. O(n + m) time complexity
2. O(m) space for failure function
3. No backtracking in text
4. Efficient for repeated pattern searches

**Key Insight:**
When a mismatch occurs, the failure function tells us how many characters we can skip, avoiding redundant comparisons.

**Example (pattern = "ABABCABCAB"):**
```
Failure Function (LPS): [0, 0, 1, 2, 0, 1, 2, 3, 4, 0]
```

### Failure Function (LPS Array)

**Definition:**
LPS[i] is the length of the longest proper prefix of pattern[0..i] that is also a suffix of pattern[0..i].

**Construction:**
1. Initialize LPS[0] = 0
2. For each position i:
   - If pattern[i] == pattern[length], extend match
   - Otherwise, use LPS[length-1] to find next possible match
   - Update length accordingly

**Time Complexity:** O(m) where m is pattern length

**Example:**
```
Pattern: "abab"
LPS:     [0, 0, 1, 2]

Explanation:
- Position 0: "a" - no prefix/suffix match → 0
- Position 1: "ab" - no prefix/suffix match → 0
- Position 2: "aba" - "a" is prefix and suffix → 1
- Position 3: "abab" - "ab" is prefix and suffix → 2
```

### Pattern Matching Process

1. **Preprocess**: Build failure function for pattern - O(m)
2. **Search**: Use failure function to match pattern in text - O(n)
3. **On Match**: Record position, continue with LPS[j-1]
4. **On Mismatch**: Use failure function to skip characters

**Time Complexity:** O(n + m) total

### Operations

**Search:**
- Time Complexity: O(n + m)
- Space Complexity: O(m)
- Returns all occurrence positions

**Build Failure Function:**
- Time Complexity: O(m)
- Space Complexity: O(m)
- Constructs LPS array

**Count Occurrences:**
- Time Complexity: O(n + m)
- Returns number of occurrences

**Multiple Pattern Search:**
- Time Complexity: O(k(n + m)) where k is number of patterns
- Returns results for all patterns

### Edge Cases Handled

- Empty text (rejected)
- Empty pattern (rejected)
- Pattern longer than text
- Single character text
- Repeated characters
- Overlapping patterns
- Patterns with no matches

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
- KMP algorithm initialization
- Single pattern searching
- Multiple pattern searching
- Failure function construction
- Occurrence counting
- Edge cases (empty, single char, overlapping, long texts)
- Invalid input handling
- Failure function correctness

## Troubleshooting

### Common Issues

**Pattern not found:**
- Verify pattern exists in text
- Check for case sensitivity
- Ensure pattern is not empty

**Incorrect failure function:**
- Verify LPS construction algorithm
- Check edge cases (single char, all same, no repeats)
- Validate LPS properties

**Performance issues:**
- KMP is O(n + m) - should be fast
- Check for excessive logging
- Verify text/pattern lengths

### Error Messages

**"Text cannot be empty"**: Must provide non-empty text string.

**"Pattern cannot be empty"**: Pattern must be non-empty for search operations.

**"Patterns list cannot be empty"**: Must provide at least one pattern for multiple pattern search.

### Best Practices

1. **Use for repeated searches** - Preprocess pattern once, search multiple times
2. **Leverage linear time** - O(n + m) is optimal for pattern matching
3. **Understand failure function** - Helps understand algorithm behavior
4. **Handle empty patterns** - Check for empty patterns before searching
5. **Use multiple pattern search** - Efficient for searching multiple patterns

## Performance Characteristics

### Time Complexity

| Operation | Time Complexity |
|-----------|----------------|
| Build Failure Function | O(m) |
| Single Pattern Search | O(n + m) |
| Multiple Pattern Search | O(k(n + m)) |
| Count Occurrences | O(n + m) |

Where:
- n = text length
- m = pattern length
- k = number of patterns

### Space Complexity

- Failure function: O(m)
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
- KMP: O(n + m) time
- Naive: O(nm) time

**vs. Z-Algorithm:**
- KMP: Preprocesses pattern, searches in text
- Z-Algorithm: Concatenates pattern + text, computes Z-array

**vs. Rabin-Karp:**
- KMP: Deterministic O(n + m)
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
