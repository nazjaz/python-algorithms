# Manacher's Algorithm for Finding Longest Palindromic Substring

A Python implementation of Manacher's algorithm for finding the longest palindromic substring in a string with O(n) linear time complexity. This algorithm efficiently finds palindromes by using center expansion and mirroring techniques.

## Project Title and Description

The Manacher's Algorithm tool implements Manacher's algorithm (also known as the longest palindromic substring algorithm) to find the longest palindromic substring in linear time. Unlike naive approaches that require O(n^3) or O(n^2) time, Manacher's algorithm achieves O(n) time complexity by reusing information from previously computed palindromes.

This tool solves the problem of efficiently finding the longest palindromic substring in a string. Palindromic substring problems are common in competitive programming, string analysis, and text processing applications. Manacher's algorithm provides an optimal solution with linear time complexity.

**Target Audience**: Competitive programmers, algorithm students, string algorithm researchers, text processing engineers, and anyone interested in understanding linear-time palindrome algorithms.

## Features

- Manacher's algorithm implementation with O(n) time complexity
- Longest palindromic substring finding
- All palindromic substrings enumeration
- Palindrome counting
- Palindrome validation at specific positions
- Support for both odd and even length palindromes
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
cd /path/to/python-algorithms/manacher-algorithm
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

Run the main script to see a demonstration of Manacher's algorithm operations:

```bash
python src/main.py
```

This will:
1. Analyze multiple text strings
2. Find longest palindromic substrings
3. Count total palindromes
4. Display all palindromes
5. Validate results

### Programmatic Usage

```python
from src.main import ManacherAlgorithm

# Create Manacher's algorithm instance
manacher = ManacherAlgorithm("babad")

# Get longest palindromic substring
longest = manacher.get_longest_palindrome()  # Returns "bab" or "aba"

# Get longest palindrome with info
info = manacher.get_longest_palindrome_info()
# Returns (palindrome, start_position, length)

# Get all palindromes
all_palindromes = manacher.get_all_palindromes()
# Returns list of (palindrome, start, length) sorted by length

# Count palindromes
count = manacher.count_palindromes()  # Returns total count

# Check if substring is palindrome
is_pal = manacher.is_palindrome_at(0, 3)  # Returns True/False
```

### Common Use Cases

**Longest Palindrome Finding:**
1. Create instance with text
2. Get longest palindromic substring
3. Analyze palindrome properties

**Palindrome Analysis:**
1. Find all palindromic substrings
2. Count total palindromes
3. Analyze palindrome distribution

**Palindrome Validation:**
1. Check if specific substring is palindrome
2. Validate palindrome properties
3. Verify algorithm correctness

## Project Structure

```
manacher-algorithm/
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

- `src/main.py`: Contains `ManacherAlgorithm` class with all operations
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `logs/`: Directory for application log files

## Algorithm Details

### Manacher's Algorithm

**Definition:**
Manacher's algorithm finds the longest palindromic substring in O(n) time by maintaining a center and right boundary of the rightmost palindrome, and using mirroring to reuse previously computed information.

**Properties:**
1. O(n) time complexity
2. O(n) space complexity
3. Handles both odd and even length palindromes
4. Uses center expansion with optimization

**Key Insight:**
The algorithm transforms the string to handle both odd and even length palindromes uniformly, then uses the concept of "mirroring" to avoid redundant computations.

**Example (text = "babad"):**
```
Transformed: ^#b#a#b#a#d#$
Radii:       [0,0,1,0,3,0,1,0,1,0,0,0]
Longest: "bab" or "aba" (length 3)
```

### Algorithm Steps

1. **Transform Text**: Insert separators (#) between characters
   - Handles both odd and even length palindromes uniformly
   - Example: "aba" → "^#a#b#a#$"

2. **Initialize**: Set center = 0, right = 0

3. **For each position i**:
   - If i is within current rightmost palindrome, use mirror
   - Otherwise, expand from center
   - Update center and right if palindrome extends further

4. **Extract Result**: Find maximum radius, convert back to original string

**Time Complexity:** O(n) - each character is compared at most once

**Space Complexity:** O(n) - stores radii array

### Operations

**Get Longest Palindrome:**
- Time Complexity: O(n) (computed during initialization)
- Returns longest palindromic substring

**Get All Palindromes:**
- Time Complexity: O(n)
- Returns all palindromic substrings sorted by length

**Count Palindromes:**
- Time Complexity: O(n)
- Counts total number of palindromic substrings

**Is Palindrome At:**
- Time Complexity: O(1) (validation)
- Checks if substring at position is palindrome

### Edge Cases Handled

- Empty text (rejected)
- Single character text
- All same characters
- No palindromes longer than one character
- Even length palindromes
- Odd length palindromes
- Multiple palindromes of same length

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
- Manacher's algorithm initialization
- Longest palindrome finding
- All palindromes enumeration
- Palindrome counting
- Palindrome validation
- Edge cases (empty, single char, all same, no long palindromes)
- Invalid input handling
- Validation

## Troubleshooting

### Common Issues

**Incorrect longest palindrome:**
- Verify algorithm implementation
- Check text transformation
- Validate radius computation

**Performance issues:**
- Manacher's is O(n) - should be fast
- Check for excessive logging
- Verify text length is reasonable

**Missing palindromes:**
- Verify all palindromes enumeration
- Check radius computation
- Validate palindrome extraction

### Error Messages

**"Text cannot be empty"**: Must provide non-empty text string.

**"Start position out of range"**: Position must be in [0, n-1].

**"Invalid length"**: Length must be positive and within bounds.

### Best Practices

1. **Use for palindrome problems** - Optimal O(n) solution
2. **Leverage linear time** - Much faster than naive O(n^2) or O(n^3)
3. **Check results** - Validate that longest is actually a palindrome
4. **Handle edge cases** - Single characters, all same, etc.
5. **Consider space** - O(n) space for radii array

## Performance Characteristics

### Time Complexity

| Operation | Time Complexity |
|-----------|----------------|
| Initialization | O(n) |
| Get Longest Palindrome | O(1) |
| Get All Palindromes | O(n) |
| Count Palindromes | O(n) |
| Is Palindrome At | O(1) |

Where n is the text length.

### Space Complexity

- Radii array: O(n)
- Transformed text: O(n)
- Total: O(n)

## Applications

- **Competitive Programming**: Palindrome problems
- **String Analysis**: Finding palindromic structures
- **Text Processing**: Palindrome detection
- **Bioinformatics**: DNA palindrome analysis
- **Data Validation**: Palindrome checking
- **Algorithm Education**: Teaching linear-time algorithms

## Comparison with Other Approaches

**vs. Naive O(n^3):**
- Manacher's: O(n) time
- Naive: O(n^3) time

**vs. Dynamic Programming O(n^2):**
- Manacher's: O(n) time, O(n) space
- DP: O(n^2) time, O(n^2) space

**vs. Center Expansion O(n^2):**
- Manacher's: O(n) time with optimization
- Center Expansion: O(n^2) time

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
