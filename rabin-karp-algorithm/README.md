# Rabin-Karp Algorithm for Multiple Pattern Matching with Rolling Hash

A Python implementation of the Rabin-Karp algorithm for pattern matching using rolling hash with collision handling. The algorithm achieves O(n + m) average-case time complexity where n is text length and m is pattern length by using rolling hash to efficiently compute hash values for substrings.

## Project Title and Description

The Rabin-Karp Algorithm tool implements the Rabin-Karp algorithm for efficient pattern matching using rolling hash. Unlike naive pattern matching which requires O(nm) time, the Rabin-Karp algorithm achieves O(n + m) average-case time complexity by using hash values to quickly identify potential matches, then verifying actual matches to handle collisions.

This tool solves the problem of efficient pattern matching in strings, especially for multiple patterns. The rolling hash technique allows computing hash values for consecutive substrings in O(1) time after initial computation, making it ideal for pattern matching applications.

**Target Audience**: Algorithm students, competitive programmers, text processing engineers, string algorithm researchers, bioinformatics researchers, and anyone interested in understanding rolling hash-based pattern matching algorithms.

## Features

- Rabin-Karp algorithm implementation with O(n + m) average-case time complexity
- Rolling hash computation for efficient substring hashing
- Single pattern matching
- Multiple pattern matching support
- Collision handling with optional verification
- Configurable hash base and modulus
- Occurrence counting
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
cd /path/to/python-algorithms/rabin-karp-algorithm
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

Run the main script to see a demonstration of Rabin-Karp algorithm operations:

```bash
python src/main.py
```

This will:
1. Create Rabin-Karp algorithm instance with text
2. Search for single patterns with collision verification
3. Display hash values
4. Search for multiple patterns
5. Show occurrence counts

### Programmatic Usage

```python
from src.main import RabinKarpAlgorithm

# Create Rabin-Karp algorithm instance
rk = RabinKarpAlgorithm("ABABDABACDABABCABCAB", base=256, modulus=101)

# Single pattern search with collision verification
occurrences = rk.search("ABABCABCAB", verify_collisions=True)  # Returns [10]

# Count occurrences
count = rk.count_occurrences("ABAB")  # Returns 2

# Check if substring exists
is_sub = rk.is_substring("ABC")  # Returns True

# Get hash value
pattern_hash = rk.get_hash("ABAB")  # Returns hash value

# Multiple pattern search
patterns = ["ABAB", "ABC", "AB"]
results = rk.search_all(patterns, verify_collisions=True)
# Returns {"ABAB": [0, 4], "ABC": [12, 15], "AB": [0, 2, 4, ...]}
```

### Common Use Cases

**Pattern Matching:**
1. Create instance with text
2. Search for patterns efficiently
3. Get all occurrences in average linear time

**Multiple Pattern Search:**
1. Create instance with text
2. Search for multiple patterns at once
3. Get results for all patterns

**Hash Analysis:**
1. Get hash values for patterns
2. Analyze hash distribution
3. Understand collision behavior

## Project Structure

```
rabin-karp-algorithm/
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

- `src/main.py`: Contains `RabinKarpAlgorithm` class with all operations
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `logs/`: Directory for application log files

## Algorithm Details

### Rabin-Karp Algorithm

**Definition:**
The Rabin-Karp algorithm uses rolling hash to compute hash values for substrings efficiently. It compares pattern hash with text substring hashes, and when hashes match, verifies the actual match to handle collisions.

**Properties:**
1. O(n + m) average-case time complexity
2. O(nm) worst-case time complexity (many hash collisions)
3. O(1) space for hash computation
4. Efficient for multiple pattern matching

**Key Insight:**
Rolling hash allows computing hash for next substring in O(1) time by removing leftmost character and adding rightmost character.

**Example (text = "banana", pattern = "ana"):**
```
Pattern hash: h("ana")
Text hashes:  h("ban"), h("ana"), h("nan"), h("ana")
Matches:      positions 1 and 3
```

### Rolling Hash

**Definition:**
Rolling hash computes hash for substring s[i..i+m-1] from hash of s[i-1..i+m-2] in O(1) time.

**Formula:**
```
hash_new = ((hash_old - s[i-1] * base^(m-1)) * base + s[i+m-1]) % modulus
```

**Advantages:**
- O(1) update time
- Efficient for consecutive substrings
- Enables fast pattern matching

**Disadvantages:**
- Hash collisions possible
- Requires collision verification
- Worst-case O(nm) with many collisions

### Collision Handling

**Problem:**
Hash values may match even when strings don't match (hash collision).

**Solution:**
1. Compare hash values first (fast)
2. When hashes match, verify actual string match (handles collisions)
3. Optional: Skip verification for speed (may have false positives)

**Trade-off:**
- With verification: Correct results, slightly slower
- Without verification: Faster, may have false positives

### Operations

**Search:**
- Time Complexity: O(n + m) average, O(nm) worst-case
- Space Complexity: O(1)
- Returns all occurrence positions

**Rolling Hash:**
- Time Complexity: O(1) per update
- Computes hash for next substring efficiently

**Multiple Pattern Search:**
- Time Complexity: O(k(n + m)) average where k is number of patterns
- Returns results for all patterns

### Edge Cases Handled

- Empty text (rejected)
- Empty pattern (rejected)
- Pattern longer than text
- Single character text
- Repeated characters
- Overlapping patterns
- Hash collisions
- Custom base and modulus

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
- Rabin-Karp algorithm initialization
- Single pattern searching
- Multiple pattern searching
- Rolling hash computation
- Collision handling
- Occurrence counting
- Edge cases (empty, single char, overlapping, long texts)
- Invalid input handling
- Hash consistency

## Troubleshooting

### Common Issues

**Pattern not found:**
- Verify pattern exists in text
- Check for case sensitivity
- Ensure pattern is not empty

**Hash collisions:**
- Enable collision verification
- Use larger modulus to reduce collisions
- Verify actual matches when hashes match

**Performance issues:**
- Rabin-Karp is O(n + m) average - should be fast
- Many collisions can cause O(nm) worst-case
- Consider larger modulus to reduce collisions
- Check for excessive logging

### Error Messages

**"Text cannot be empty"**: Must provide non-empty text string.

**"Pattern cannot be empty"**: Pattern must be non-empty for search operations.

**"Base must be at least 2"**: Hash base must be at least 2.

**"Modulus must be at least 2"**: Hash modulus must be at least 2.

### Best Practices

1. **Use collision verification** - Enable verify_collisions=True for correct results
2. **Choose appropriate modulus** - Larger modulus reduces collisions
3. **Leverage rolling hash** - Efficient for consecutive substring hashing
4. **Handle edge cases** - Empty patterns, single characters, etc.
5. **Use multiple pattern search** - Efficient for searching multiple patterns

## Performance Characteristics

### Time Complexity

| Operation | Average Case | Worst Case |
|-----------|-------------|------------|
| Single Pattern Search | O(n + m) | O(nm) |
| Multiple Pattern Search | O(k(n + m)) | O(knm) |
| Rolling Hash Update | O(1) | O(1) |
| Count Occurrences | O(n + m) | O(nm) |

Where:
- n = text length
- m = pattern length
- k = number of patterns

### Space Complexity

- Hash computation: O(1)
- Text storage: O(n)
- Total: O(n)

### Hash Collision Probability

- Probability of collision: approximately 1/modulus
- Larger modulus reduces collision probability
- Typical modulus: 10^9 + 7 or large prime

## Applications

- **Text Processing**: Pattern matching in documents
- **Bioinformatics**: DNA/RNA sequence matching
- **String Algorithms**: Substring problems
- **Competitive Programming**: Pattern matching problems
- **Search Engines**: Fast pattern matching
- **Data Validation**: Pattern checking
- **Multiple Pattern Matching**: Efficient multi-pattern search

## Comparison with Other Algorithms

**vs. Naive Pattern Matching:**
- Rabin-Karp: O(n + m) average, O(nm) worst
- Naive: O(nm) always

**vs. KMP Algorithm:**
- Rabin-Karp: Uses hashing, O(nm) worst-case
- KMP: Deterministic O(n + m), no worst-case degradation

**vs. Z-Algorithm:**
- Rabin-Karp: Hash-based, good for multiple patterns
- Z-Algorithm: Z-array based, O(n + m) deterministic

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
