# Eertree (Palindromic Tree)

A Python implementation of the eertree (palindromic tree) data structure for efficient palindrome substring queries and counting.

## Project Title and Description

The eertree, also known as a palindromic tree, is a specialized data structure that efficiently stores all distinct palindromic substrings of a string. This implementation provides O(n) time complexity for building the tree and supports various query operations for palindrome detection, counting, and retrieval.

This project solves the problem of efficiently finding, counting, and querying palindromic substrings in a given string, which is useful in string processing, competitive programming, and text analysis applications.

**Target Audience**: Developers working with string algorithms, competitive programmers, and anyone needing efficient palindrome substring operations.

## Features

- Efficient O(n) time construction of the palindromic tree
- Count distinct palindromic substrings
- Count total palindromic substrings (including duplicates)
- List all distinct palindromic substrings
- Find the longest palindromic substring
- Query specific palindromes and get their occurrence counts
- Check if a substring is a palindrome
- Command-line interface for interactive use
- Comprehensive test suite

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

No external dependencies are required. The implementation uses only Python standard library.

## Installation

### Step 1: Clone or Navigate to Project Directory

```bash
cd /Users/nasihjaseem/projects/github/python-algorithms/eertree-palindromic-tree
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

Note: This project has no external dependencies, but the requirements.txt file is included for consistency with project standards.

## Configuration

This project does not require configuration files or environment variables. All functionality is available through the command-line interface or by importing the classes directly.

## Usage

### Command-Line Interface

#### Basic Usage

Display summary statistics for a string:

```bash
python src/main.py "abacaba"
```

Output:
```
Input string: abacaba
Distinct palindromes: 7
Total palindromes: 15
Longest palindrome: abacaba
```

#### Count Distinct Palindromes

```bash
python src/main.py "abacaba" --count-distinct
```

Output:
```
Distinct palindromes: 7
```

#### Count Total Palindromes

```bash
python src/main.py "abacaba" --count-total
```

Output:
```
Total palindromes: 15
```

#### List All Palindromes

```bash
python src/main.py "abacaba" --list-all
```

Output:
```
All distinct palindromes (7):
  a
  aba
  abacaba
  aca
  b
  bacab
  c
```

#### Find Longest Palindrome

```bash
python src/main.py "racecar" --longest
```

Output:
```
Longest palindrome: racecar
```

#### Query Specific Palindrome

```bash
python src/main.py "abacaba" --query "aba"
```

Output:
```
'aba' is a palindrome appearing 2 time(s)
```

### Programmatic Usage

```python
from src.main import Eertree

# Create and build eertree
tree = Eertree()
tree.build("abacaba")

# Count distinct palindromes
distinct_count = tree.count_distinct_palindromes()
print(f"Distinct palindromes: {distinct_count}")

# Count total palindromes
total_count = tree.count_total_palindromes()
print(f"Total palindromes: {total_count}")

# Get all palindromes
all_palindromes = tree.get_all_palindromes()
print(f"All palindromes: {all_palindromes}")

# Find longest palindrome
longest = tree.get_longest_palindrome()
print(f"Longest: {longest}")

# Query specific palindrome
count = tree.get_palindrome_count("aba")
print(f"Count of 'aba': {count}")

# Check if substring is palindrome
is_pal = tree.is_palindrome_substring("aba")
print(f"Is 'aba' a palindrome substring: {is_pal}")
```

### Common Use Cases

1. **Find all palindromic substrings in a string**
   ```bash
   python src/main.py "your_string" --list-all
   ```

2. **Count palindromes for analysis**
   ```bash
   python src/main.py "your_string" --count-distinct --count-total
   ```

3. **Find the longest palindrome**
   ```bash
   python src/main.py "your_string" --longest
   ```

4. **Check if a specific substring is a palindrome**
   ```bash
   python src/main.py "your_string" --query "substring"
   ```

## Project Structure

```
eertree-palindromic-tree/
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies (none required)
├── .gitignore               # Git ignore patterns
├── src/
│   └── main.py              # Main eertree implementation and CLI
├── tests/
│   └── test_main.py         # Comprehensive test suite
├── docs/
│   └── API.md               # API documentation
└── logs/
    └── .gitkeep             # Placeholder for log directory
```

### File Descriptions

- **src/main.py**: Contains the `EertreeNode` and `Eertree` classes, along with the CLI interface. Implements all core functionality for palindrome detection and counting.
- **tests/test_main.py**: Comprehensive test suite covering all functionality including edge cases, special characters, and various string patterns.
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
pytest tests/test_main.py::TestEertree::test_build_simple_palindrome
```

### Test Coverage

The test suite aims for comprehensive coverage including:
- Basic functionality (building tree, counting palindromes)
- Edge cases (empty strings, single characters)
- Special characters and mixed case
- Long strings and performance
- Query operations
- Palindrome detection accuracy

## Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'src'`

**Solution**: Ensure you're running commands from the project root directory, or add the project root to your Python path:
```bash
export PYTHONPATH="${PYTHONPATH}:/path/to/eertree-palindromic-tree"
```

**Issue**: Tests fail with import errors

**Solution**: Make sure you've installed pytest:
```bash
pip install pytest pytest-cov
```

**Issue**: Incorrect palindrome counts

**Solution**: The eertree counts palindromes as substrings. A palindrome may appear multiple times as overlapping substrings. This is expected behavior.

### Error Messages

- **"Error processing string"**: Check that the input string is valid and doesn't contain unexpected encoding issues.
- **Import errors**: Ensure you're in the correct directory and virtual environment is activated.

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

The eertree (palindromic tree) is built using the following approach:

1. **Two Special Nodes**: 
   - Imaginary root (length -1) for odd-length palindromes
   - Empty root (length 0) for even-length palindromes

2. **Node Structure**: Each node represents a palindrome and stores:
   - Length of the palindrome
   - Edges to child nodes (representing extended palindromes)
   - Suffix link to the longest palindromic suffix

3. **Construction**: The tree is built incrementally by processing each character:
   - Find the longest palindromic suffix that can be extended
   - Create new node if palindrome doesn't exist
   - Update suffix links for efficient traversal

4. **Time Complexity**: O(n) where n is the length of the input string

5. **Space Complexity**: O(n) for storing all distinct palindromes

## License

This project is provided as-is for educational and practical use. Please refer to the LICENSE file in the parent directory for license information.
