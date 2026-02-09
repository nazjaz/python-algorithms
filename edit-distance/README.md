# Edit Distance (Levenshtein Distance)

A Python implementation of edit distance (Levenshtein distance) calculation using dynamic programming with both standard and space-optimized approaches. This tool calculates the minimum number of operations needed to transform one string into another.

## Project Title and Description

The Edit Distance tool implements the Levenshtein distance algorithm using dynamic programming. It provides both standard O(m*n) space and optimized O(min(m,n)) space implementations. Edit distance measures the minimum number of single-character edits (insertions, deletions, substitutions) required to transform one string into another.

This tool solves the problem of measuring string similarity and finding the minimum edit operations. Edit distance is widely used in spell checkers, DNA sequence alignment, natural language processing, and fuzzy string matching.

**Target Audience**: Students learning dynamic programming, developers studying string algorithms, NLP engineers, bioinformatics researchers, educators teaching computer science concepts, and anyone interested in understanding string similarity and edit operations.

## Features

- Standard dynamic programming implementation (O(m*n) space)
- Space-optimized implementation (O(min(m,n)) space)
- Edit distance calculation
- Operation sequence reconstruction
- Performance comparison between approaches
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
cd /path/to/python-algorithms/edit-distance
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

### Performance Comparison (Default)

Compare both approaches:

```bash
python src/main.py "kitten" "sitting" --method compare
```

### Standard DP Approach

Use standard DP approach only:

```bash
python src/main.py "kitten" "sitting" --method dp
```

### Space-Optimized Approach

Use space-optimized approach only:

```bash
python src/main.py "kitten" "sitting" --method optimized
```

### Show Operations

Display sequence of operations:

```bash
python src/main.py "kitten" "sitting" --method compare --operations
```

### Multiple Iterations

Run multiple iterations for timing:

```bash
python src/main.py "kitten" "sitting" --method compare --iterations 1000
```

### Generate Report

Generate performance report:

```bash
python src/main.py "kitten" "sitting" --method compare --report report.txt
```

### Command-Line Arguments

- `str1`: (Required) First string
- `str2`: (Required) Second string
- `-c, --config`: Path to configuration file (default: config.yaml)
- `-m, --method`: Solution method - dp, optimized, or compare (default: compare)
- `-o, --operations`: Show sequence of operations
- `-i, --iterations`: Number of iterations for timing (default: 1)
- `-r, --report`: Output path for performance report

### Common Use Cases

**String Similarity:**
1. Calculate distance: `python src/main.py "hello" "hallo" --method compare`
2. Review edit distance
3. Understand similarity measure

**Spell Checking:**
1. Compare words: `python src/main.py "recieve" "receive" --method compare`
2. Get edit distance
3. Use for spell correction

**DNA Sequence Alignment:**
1. Compare sequences: `python src/main.py "ACGT" "ACCT" --method compare`
2. Get minimum edits
3. Understand sequence differences

**Operation Analysis:**
1. Get operations: `python src/main.py "kitten" "sitting" --operations`
2. Review transformation steps
3. Understand edit sequence

## Project Structure

```
edit-distance/
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

- `src/main.py`: Contains the `EditDistance` class
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `logs/`: Directory for application log files

## Algorithm Details

### Edit Distance (Levenshtein Distance)

**Definition:**
Edit distance is the minimum number of single-character edits (insertions, deletions, substitutions) required to transform one string into another. It measures string similarity.

**Operations:**
- **Insert**: Add a character to str1
- **Delete**: Remove a character from str1
- **Replace**: Replace a character in str1

**Example:**
- "kitten" -> "sitting"
  - Replace 'k' with 's'
  - Replace 'e' with 'i'
  - Insert 'g' at end
  - Edit distance: 3

**Applications:**
- Spell checkers
- DNA sequence alignment
- Natural language processing
- Fuzzy string matching
- Autocomplete systems
- Plagiarism detection

### Dynamic Programming Approach

**How It Works:**
1. Create DP table where dp[i][j] = edit distance between str1[0:i] and str2[0:j]
2. Base cases: dp[i][0] = i, dp[0][j] = j
3. For each cell, take minimum of:
   - Delete: dp[i-1][j] + 1
   - Insert: dp[i][j-1] + 1
   - Replace: dp[i-1][j-1] + (0 if match, 1 if mismatch)
4. Result is dp[m][n]

**Time Complexity:**
- O(m*n) where m=len(str1), n=len(str2)

**Space Complexity:**
- O(m*n) for DP table

### Space-Optimized Approach

**How It Works:**
1. Use only two rows instead of full table
2. Keep previous and current rows
3. Swap rows after each iteration
4. Use shorter string for column dimension

**Time Complexity:**
- O(m*n) where m=len(str1), n=len(str2)

**Space Complexity:**
- O(min(m,n)) using two rows

**Benefits:**
- Significant space savings for large strings
- Same time complexity
- Essential for memory-constrained environments

### Edge Cases Handled

- Empty strings
- Identical strings (distance = 0)
- One string is substring of another
- Completely different strings
- Single character strings
- Very long strings
- Unicode characters
- Special characters

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
- Standard DP approach
- Space-optimized approach
- Edit distance calculation
- Operation sequence reconstruction
- Edge cases (empty strings, identical strings, single characters)
- Performance comparison functionality
- Error handling
- Report generation
- Input validation

## Troubleshooting

### Common Issues

**Empty Strings:**
- Empty string to empty string: distance = 0
- Empty string to non-empty: distance = length of non-empty string
- This is expected behavior

**Large Strings:**
- Standard DP may use significant memory
- Use space-optimized approach for large strings
- Consider string length before choosing approach

**Import Errors:**
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (requires 3.8+)
- Verify virtual environment is activated

### Error Messages

**"Configuration file not found"**: The config.yaml file doesn't exist. Create it or specify path with `-c` option.

### Best Practices

1. **Use space-optimized approach** for large strings or memory constraints
2. **Use standard DP** when operation sequence is needed
3. **Compare both approaches** to understand trade-offs
4. **Use multiple iterations** for accurate timing measurements
5. **Review operations** to understand transformation steps
6. **Consider string length** when choosing approach
7. **Handle empty strings** appropriately in applications

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
