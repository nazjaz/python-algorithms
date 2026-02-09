# Rolling Hash with Multiple Moduli

A Python implementation of rolling hash (polynomial hash) with multiple prime moduli for robust string matching and substring hashing.

## Project Title and Description

This project implements a polynomial rolling hash algorithm using multiple prime moduli to minimize hash collisions and provide reliable string matching capabilities. The rolling hash technique allows efficient computation of hash values for substrings and enables fast pattern matching in text.

The multiple moduli approach significantly reduces the probability of hash collisions, making the algorithm more robust for string matching applications. This is particularly useful in competitive programming, text processing, and string algorithm implementations.

**Target Audience**: Developers working with string algorithms, competitive programmers, and anyone needing efficient substring hashing and pattern matching.

## Features

- Polynomial rolling hash with multiple prime moduli
- Efficient substring hashing in O(1) time after preprocessing
- Fast pattern matching using rolling hash technique
- Prefix hash array for efficient substring queries
- Substring comparison using hash values
- Longest common prefix computation using binary search
- Configurable moduli and base values
- Command-line interface for interactive use
- Comprehensive test suite

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

No external dependencies are required. The implementation uses only Python standard library.

## Installation

### Step 1: Clone or Navigate to Project Directory

```bash
cd /Users/nasihjaseem/projects/github/python-algorithms/rolling-hash-multiple-moduli
```

### Step 2: Create Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

Note: This project has no external dependencies for core functionality, but pytest is included for testing.

## Configuration

This project does not require configuration files or environment variables. All functionality is available through the command-line interface or by importing the classes directly.

### Default Configuration

- **Moduli**: `[10^9 + 7, 10^9 + 9, 10^9 + 21]` (large prime numbers)
- **Base**: `256` (suitable for ASCII and extended ASCII)

These defaults provide excellent collision resistance while maintaining good performance.

## Usage

### Command-Line Interface

#### Basic Hash Computation

Compute hash of a string:

```bash
python src/main.py "hello world"
```

Output:
```
Text: hello world
Hash values: (1234567890, 9876543210, 5555555555)
Using moduli: [1000000007, 1000000009, 1000000021]
Using base: 256
```

#### Compute Hash Explicitly

```bash
python src/main.py "hello world" --hash
```

#### Pattern Matching

Find all occurrences of a pattern:

```bash
python src/main.py "abababab" --pattern "ab"
```

Output:
```
Pattern 'ab' found at positions: [0, 2, 4, 6]
Total occurrences: 4
```

#### Substring Hashing

Compute hash of a substring:

```bash
python src/main.py "hello world" --substring "0:5"
```

Output:
```
Substring 'hello' (start=0, length=5): (1234567890, 9876543210, 5555555555)
```

#### Substring Comparison

Compare two substrings:

```bash
python src/main.py "hello world" --compare "world hello,0,0,5"
```

Output:
```
Substring 1: 'hello' (start=0)
Substring 2: 'world' (start=0)
Are equal: False
```

#### Custom Moduli and Base

```bash
python src/main.py "hello" --moduli "1000000007,1000000009" --base 131
```

### Programmatic Usage

```python
from src.main import RollingHash

# Create rolling hash instance
rh = RollingHash()

# Hash a string
text = "hello world"
hashes = rh.hash_string(text)
print(f"Hash values: {hashes}")

# Hash a substring
substring_hash = rh.hash_substring(text, 0, 5)
print(f"Substring hash: {substring_hash}")

# Build prefix hash array for efficient queries
prefix_hashes = rh.build_prefix_hashes(text)

# Get substring hash from prefix array
substring_hash = rh.get_substring_hash_from_prefix(prefix_hashes, 0, 5)

# Find pattern occurrences
text = "abababab"
pattern = "ab"
occurrences = rh.find_pattern(text, pattern)
print(f"Pattern found at: {occurrences}")

# Compare substrings
text1 = "hello world"
text2 = "hello there"
are_equal = rh.compare_substrings(text1, 0, text2, 0, 5)
print(f"Substrings equal: {are_equal}")

# Find longest common prefix
lcp = rh.longest_common_prefix_hash(text1, 0, text2, 0)
print(f"Longest common prefix: {lcp}")
```

### Common Use Cases

1. **Pattern Matching in Text**
   ```bash
   python src/main.py "your_text" --pattern "pattern"
   ```

2. **Substring Hashing for Comparison**
   ```bash
   python src/main.py "text1" --compare "text2,start1,start2,length"
   ```

3. **Efficient Substring Queries**
   ```python
   rh = RollingHash()
   prefix_hashes = rh.build_prefix_hashes(text)
   # Now query any substring in O(1) time
   hash_value = rh.get_substring_hash_from_prefix(prefix_hashes, i, length)
   ```

## Project Structure

```
rolling-hash-multiple-moduli/
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore patterns
├── src/
│   └── main.py              # Main rolling hash implementation and CLI
├── tests/
│   └── test_main.py         # Comprehensive test suite
├── docs/
│   └── API.md               # API documentation
└── logs/
    └── .gitkeep             # Placeholder for log directory
```

### File Descriptions

- **src/main.py**: Contains the `RollingHash` class with all core functionality for string hashing, pattern matching, and substring operations.
- **tests/test_main.py**: Comprehensive test suite covering all functionality including edge cases, large strings, and special characters.
- **docs/API.md**: Detailed API documentation for all classes and methods.
- **logs/**: Directory for log files (if logging to files is enabled).

## Testing

### Run All Tests

```bash
pytest tests/
```

### Run Tests with Coverage

```bash
pytest tests/ --cov=src --cov-report=html
```

### Run Specific Test

```bash
pytest tests/test_main.py::TestRollingHash::test_find_pattern_multiple_occurrences
```

### Test Coverage

The test suite aims for comprehensive coverage including:
- Basic hashing operations
- Substring hashing and prefix arrays
- Pattern matching
- Substring comparison
- Edge cases (empty strings, out of bounds)
- Large strings and performance
- Special and unicode characters

## Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'src'`

**Solution**: Ensure you're running commands from the project root directory, or add the project root to your Python path:
```bash
export PYTHONPATH="${PYTHONPATH}:/path/to/rolling-hash-multiple-moduli"
```

**Issue**: Tests fail with import errors

**Solution**: Make sure you've installed pytest:
```bash
pip install pytest pytest-cov
```

**Issue**: Hash collisions (rare but possible)

**Solution**: Use more moduli or larger prime moduli. The default configuration uses 3 large primes which provides excellent collision resistance for most use cases.

### Error Messages

- **"At least one modulus is required"**: Provide at least one modulus when initializing RollingHash.
- **"Base must be at least 2"**: Use a base value of 2 or greater.
- **"Substring indices out of bounds"**: Check that start and length parameters are within string bounds.

## Contributing

### Development Setup

1. Fork the repository
2. Create a virtual environment
3. Install development dependencies:
   ```bash
   pip install pytest pytest-cov
   ```
4. Create a feature branch: `git checkout -b feature/your-feature-name`

### Code Style Guidelines

- Follow PEP 8 strictly
- Maximum line length: 88 characters
- Use type hints for all functions
- Write docstrings for all public functions and classes
- Run tests before committing

### Pull Request Process

1. Ensure all tests pass
2. Update documentation if needed
3. Write clear commit messages following conventional commit format
4. Submit pull request with description of changes

## Algorithm Details

### Polynomial Rolling Hash

The rolling hash uses a polynomial hash function:

```
hash(s) = (s[0] * base^(n-1) + s[1] * base^(n-2) + ... + s[n-1]) mod m
```

Where:
- `s` is the string
- `base` is the base (typically 256 or a prime)
- `m` is the modulus (prime number)
- `n` is the length of the string

### Multiple Moduli

Using multiple moduli reduces hash collisions:

- Single modulus: Probability of collision ≈ 1/m
- k moduli: Probability of collision ≈ 1/(m₁ * m₂ * ... * mₖ)

This makes the hash much more robust for string matching.

### Rolling Hash Technique

For a sliding window, the hash can be updated in O(1) time:

```
hash_new = ((hash_old - s[left] * base^(n-1)) * base + s[right]) mod m
```

This allows efficient pattern matching in O(n + m) time where n is text length and m is pattern length.

### Time Complexity

- **Hash computation**: O(n) where n is string length
- **Substring hash (direct)**: O(k) where k is substring length
- **Substring hash (from prefix)**: O(1) after O(n) preprocessing
- **Pattern matching**: O(n + m) where n is text length, m is pattern length
- **Substring comparison**: O(k) where k is substring length

### Space Complexity

- **Hash computation**: O(1) additional space
- **Prefix hash array**: O(n * k) where n is string length, k is number of moduli
- **Power precomputation**: O(max_length) for powers array

## License

This project is provided as-is for educational and practical use. Please refer to the LICENSE file in the parent directory for license information.
