# Longest Common Subsequence (LCS)

A Python implementation of the Longest Common Subsequence algorithm using dynamic programming with backtracking. This tool finds the longest subsequence common to two strings, where a subsequence is a sequence that appears in the same relative order but not necessarily contiguous.

## Project Title and Description

The Longest Common Subsequence Calculator provides a complete implementation of the LCS algorithm using dynamic programming. It demonstrates how dynamic programming solves the problem efficiently by building a DP table and using backtracking to reconstruct the actual LCS string.

This tool solves the problem of finding common patterns between two sequences, which is essential in bioinformatics (DNA sequence alignment), version control (diff algorithms), text comparison, and many other applications.

**Target Audience**: Students learning dynamic programming, developers studying string algorithms, educators teaching algorithm design, bioinformatics researchers, and anyone interested in understanding LCS and dynamic programming.

## Features

- Dynamic programming implementation for LCS calculation
- Backtracking to reconstruct the actual LCS string
- DP table visualization
- Support for finding all LCS (when multiple exist)
- Detailed analysis with statistics
- Comprehensive logging
- Detailed analysis reports
- Error handling for edge cases
- Command-line interface
- Demonstration mode with examples

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

### Step 1: Navigate to Project Directory

```bash
cd /path/to/python-algorithms/longest-common-subsequence
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

### Basic LCS Calculation

Find LCS between two strings:

```bash
python src/main.py "ABCDGH" "AEDFHR"
```

### With DP Table Visualization

Show DP table visualization:

```bash
python src/main.py "ABCDGH" "AEDFHR" --visualize
```

### Find All LCS

Find all longest common subsequences:

```bash
python src/main.py "ABCD" "ACBD" --all
```

### Generate Report

Generate detailed analysis report:

```bash
python src/main.py "ABCDGH" "AEDFHR" --report report.txt
```

### Demonstration Mode

Run demonstration with example strings:

```bash
python src/main.py --demo
```

### Command-Line Arguments

- `string1`: (Optional) First string
- `string2`: (Optional) Second string
- `-c, --config`: Path to configuration file (default: config.yaml)
- `-v, --visualize`: Show DP table visualization
- `-a, --all`: Find all LCS (may be slow for large strings)
- `-r, --report`: Output path for analysis report
- `--demo`: Run demonstration with example strings

### Common Use Cases

**Find LCS:**
1. Run: `python src/main.py "ABCDGH" "AEDFHR"`
2. Review LCS result
3. Understand subsequence concept

**Study DP Table:**
1. Run: `python src/main.py "ABC" "AC" --visualize`
2. Review DP table structure
3. Understand dynamic programming approach

**Find All LCS:**
1. Run: `python src/main.py "ABCD" "ACBD" --all`
2. Review all possible LCS
3. Understand that LCS may not be unique

**Generate Documentation:**
1. Run: `python src/main.py "ABCDGH" "AEDFHR" --report report.txt`
2. Review detailed report
3. Study algorithm complexity

## Project Structure

```
longest-common-subsequence/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── config.yaml              # Configuration file
├── .gitignore               # Git ignore patterns
├── .env.example             # Environment variables template
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

- `src/main.py`: Contains the `LCSCalculator` class with dynamic programming and backtracking
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `docs/API.md`: API documentation for the calculator
- `logs/`: Directory for application log files

## Algorithm Details

### Longest Common Subsequence

A subsequence is a sequence that can be derived from another sequence by deleting some or no elements without changing the order of the remaining elements.

**Example:**
- String 1: "ABCDGH"
- String 2: "AEDFHR"
- LCS: "ADH" (length 3)

### Dynamic Programming Approach

The algorithm uses a 2D DP table where:
- `dp[i][j]` = length of LCS of `str1[0:i]` and `str2[0:j]`

**Recurrence Relation:**
```
If str1[i-1] == str2[j-1]:
    dp[i][j] = dp[i-1][j-1] + 1
Else:
    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
```

**Base Cases:**
- `dp[0][j] = 0` for all j (empty string has no common subsequence)
- `dp[i][0] = 0` for all i

### Algorithm Steps

**1. Build DP Table:**
```
For i from 1 to m:
    For j from 1 to n:
        If str1[i-1] == str2[j-1]:
            dp[i][j] = dp[i-1][j-1] + 1
        Else:
            dp[i][j] = max(dp[i-1][j], dp[i][j-1])
```

**2. Backtrack to Reconstruct LCS:**
```
Start from dp[m][n]
While i > 0 and j > 0:
    If str1[i-1] == str2[j-1]:
        Add str1[i-1] to LCS
        Move diagonally (i--, j--)
    Else if dp[i-1][j] > dp[i][j-1]:
        Move up (i--)
    Else:
        Move left (j--)
Reverse LCS to get correct order
```

### Example: Finding LCS of "ABC" and "AC"

**DP Table:**
```
      A  C
   0  0  0
A 0  1  1
B 0  1  1
C 0  1  2
```

**Backtracking:**
- Start at dp[3][2] = 2
- Move diagonally (C matches) → add 'C'
- Move up (B doesn't match, dp[1][2] >= dp[2][1])
- Move diagonally (A matches) → add 'A'
- Result: "AC" (reversed from "CA")

### Time Complexity

- **Time Complexity:** O(m * n) where:
  - m = length of string 1
  - n = length of string 2
  - Filling DP table: O(m * n)
  - Backtracking: O(m + n)

### Space Complexity

- **Space Complexity:** O(m * n) for DP table
  - Can be optimized to O(min(m, n)) using space optimization
  - Current implementation uses O(m * n) for clarity

### Properties

- **Subsequence vs Substring**: Subsequence doesn't require contiguous characters
- **Not Unique**: Multiple LCS may exist for same pair of strings
- **Optimal Substructure**: Problem can be broken into smaller subproblems
- **Overlapping Subproblems**: DP table stores solutions to avoid recomputation

## Applications

### Bioinformatics

- **DNA Sequence Alignment**: Finding common patterns in genetic sequences
- **Protein Sequence Comparison**: Identifying similar protein structures
- **Phylogenetic Analysis**: Comparing evolutionary relationships

### Version Control

- **Diff Algorithms**: Finding differences between file versions
- **Merge Conflict Resolution**: Identifying common and conflicting changes
- **Code Comparison**: Comparing code versions

### Text Processing

- **Plagiarism Detection**: Finding similar text patterns
- **Spell Checking**: Finding closest matching words
- **Text Similarity**: Measuring similarity between documents

### Other Applications

- **File Comparison**: Comparing file contents
- **Data Deduplication**: Finding duplicate data patterns
- **Pattern Matching**: Finding common patterns in sequences

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
- LCS length calculation
- LCS string reconstruction
- Backtracking correctness
- DP table structure
- Edge cases (empty strings, no common characters, identical strings)
- All LCS finding
- Visualization
- Report generation

## Troubleshooting

### Common Issues

**Empty LCS:**
- Strings may have no common characters
- Check that strings are not empty
- Verify input strings are correct

**Import Errors:**
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (requires 3.8+)
- Verify virtual environment is activated

**Slow Performance with --all:**
- Finding all LCS can be slow for large strings
- Use `--all` only when necessary
- For large strings, use basic LCS calculation

### Error Messages

**"Configuration file not found"**: Config file doesn't exist at specified path. Check file path or create config.yaml.

**"Invalid YAML in configuration file"**: Config file has syntax errors. Verify YAML format.

**"Failed to save report"**: Cannot write report file. Check file permissions and path.

### Best Practices

1. **Use visualization** to understand DP table: `--visualize`
2. **Generate reports** for documentation: `--report report.txt`
3. **Check logs** to understand algorithm execution
4. **Use demonstration mode** to see examples: `--demo`
5. **Avoid --all** for very large strings (can be slow)
6. **Understand subsequence** vs substring difference

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
