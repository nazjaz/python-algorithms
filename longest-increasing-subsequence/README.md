# Longest Increasing Subsequence

A Python implementation of algorithms to find the longest increasing subsequence (LIS) in an array using both dynamic programming and binary search optimization approaches. This tool provides comprehensive LIS analysis, performance comparison, and detailed logging.

## Project Title and Description

The Longest Increasing Subsequence tool implements two approaches to find the longest increasing subsequence: dynamic programming (O(n²)) and binary search optimization (O(n log n)). A subsequence is a sequence that can be derived from an array by deleting some or no elements without changing the order of remaining elements. An increasing subsequence has elements in strictly increasing order.

This tool solves the problem of finding the longest subsequence where elements are in strictly increasing order. The LIS problem has applications in bioinformatics, data analysis, scheduling, and various optimization problems.

**Target Audience**: Students learning dynamic programming and optimization algorithms, developers studying LIS and subsequence problems, educators teaching computer science concepts, and anyone interested in understanding different algorithmic approaches and their trade-offs.

## Features

- Dynamic programming implementation (O(n²))
- Binary search optimization implementation (O(n log n))
- LIS length calculation
- LIS sequence reconstruction
- Comprehensive edge case handling
- Performance comparison with timing analysis
- Detailed step-by-step logging
- Comprehensive performance reports
- Multiple iterations support for accurate timing
- Input validation
- Error handling for invalid inputs

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

### Step 1: Navigate to Project Directory

```bash
cd /path/to/python-algorithms/longest-increasing-subsequence
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
python src/main.py 10 9 2 5 3 7 101 18 --method compare
```

### Dynamic Programming Approach

Use DP approach only:

```bash
python src/main.py 10 9 2 5 3 7 101 18 --method dp
```

### Binary Search Approach

Use binary search approach only:

```bash
python src/main.py 10 9 2 5 3 7 101 18 --method binary
```

### Multiple Iterations

Run multiple iterations for more accurate timing:

```bash
python src/main.py 10 9 2 5 3 7 101 18 --iterations 1000 --method compare
```

### Generate Report

Generate performance report:

```bash
python src/main.py 10 9 2 5 3 7 101 18 --method compare --report report.txt
```

### Command-Line Arguments

- `numbers`: (Required) Numbers in the array (space-separated)
- `-c, --config`: Path to configuration file (default: config.yaml)
- `-m, --method`: Solution method - dp, binary, or compare (default: compare)
- `-i, --iterations`: Number of iterations for timing (default: 1)
- `-r, --report`: Output path for performance report

### Common Use Cases

**Compare Approaches:**
1. Run: `python src/main.py 10 9 2 5 3 7 101 18 --method compare`
2. Review timing for each approach
3. Identify fastest approach for your array size

**Study Algorithms:**
1. Use specific method: `python src/main.py 10 9 2 5 3 7 --method dp`
2. Review logs to see algorithm execution
3. Understand different approaches

**Performance Analysis:**
1. Test with different array sizes
2. Use multiple iterations: `python src/main.py 10 9 2 5 3 7 --iterations 1000 --method compare`
3. Generate reports for detailed metrics

**Edge Case Testing:**
1. Test with empty array
2. Test with single element
3. Test with already sorted array
4. Test with reverse sorted array
5. Test with all equal elements
6. Test with duplicates

## Project Structure

```
longest-increasing-subsequence/
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

- `src/main.py`: Contains the `LongestIncreasingSubsequence` class and main logic
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `logs/`: Directory for application log files

## Algorithm Details

### Longest Increasing Subsequence

**Definition:**
A subsequence is a sequence that can be derived from an array by deleting some or no elements without changing the order of remaining elements. The longest increasing subsequence (LIS) is the subsequence with maximum length where elements are in strictly increasing order.

**Example:**
- Array: [10, 9, 2, 5, 3, 7, 101, 18]
- LIS: [2, 3, 7, 18] or [2, 5, 7, 101] (length: 4)

**Applications:**
- Bioinformatics (DNA sequence analysis)
- Data analysis (trend detection)
- Scheduling problems
- Stock price analysis
- Pattern recognition

### Dynamic Programming Approach

**How It Works:**
1. Create DP table where dp[i] = length of LIS ending at index i
2. For each element, check all previous elements
3. If previous element is smaller, extend that subsequence
4. Track maximum length found
5. Reconstruct LIS using parent pointers

**Time Complexity:**
- Best Case: O(n²) where n=array length
- Average Case: O(n²)
- Worst Case: O(n²)

**Space Complexity:**
- O(n) for DP table and parent array

**Characteristics:**
- Simple to understand and implement
- Always O(n²) regardless of input
- Good for small arrays
- Can find all LIS if needed

### Binary Search Optimization

**How It Works:**
1. Maintain array `tails` where tails[i] = smallest tail element of all LIS of length i+1
2. For each element, use binary search to find position in tails
3. Update tails array to maintain invariant
4. Length of tails array is LIS length
5. Reconstruct LIS using parent pointers

**Time Complexity:**
- Best Case: O(n log n) where n=array length
- Average Case: O(n log n)
- Worst Case: O(n log n)

**Space Complexity:**
- O(n) for tails array and parent array

**Characteristics:**
- More efficient for large arrays
- Uses binary search for optimization
- O(n log n) is optimal for comparison-based algorithms
- May have overhead for small arrays

### Edge Cases Handled

- Empty array
- Single element array
- Already sorted array (LIS = entire array)
- Reverse sorted array (LIS length = 1)
- All equal elements (LIS length = 1)
- Duplicate values
- Negative numbers
- Floating point numbers
- Large arrays

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
- DP approach with various arrays
- Binary search approach with various arrays
- Edge cases (empty, single element, sorted, reverse sorted, duplicates)
- Performance comparison functionality
- Error handling
- Report generation
- Both implementation approaches
- Input validation

## Troubleshooting

### Common Issues

**Empty Array:**
- Returns length 0 and empty sequence
- This is expected behavior

**All Equal Elements:**
- LIS length is 1 (any single element)
- This is correct (strictly increasing requires different values)

**Import Errors:**
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (requires 3.8+)
- Verify virtual environment is activated

### Error Messages

**"Configuration file not found"**: The config.yaml file doesn't exist. Create it or specify path with `-c` option.

### Best Practices

1. **Use DP approach** for small arrays or when simplicity is preferred
2. **Use binary search approach** for large arrays or when performance is critical
3. **Compare both approaches** to understand trade-offs
4. **Use multiple iterations** for accurate timing measurements
5. **Review logs** to see algorithm execution details
6. **Note that LIS may not be unique** - algorithm returns one valid LIS
7. **Understand that subsequence** means elements don't need to be consecutive

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
