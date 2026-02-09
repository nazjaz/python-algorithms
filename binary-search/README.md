# Binary Search Algorithm

A Python implementation of binary search algorithm with both recursive and iterative approaches. This tool provides comprehensive edge case handling, performance comparison, and detailed analysis of the search process.

## Project Title and Description

The Binary Search tool implements binary search algorithm using both recursive and iterative approaches. It provides detailed logging, performance comparison, and comprehensive edge case handling to help understand how the algorithm works and when to use each approach.

This tool solves the problem of understanding binary search implementation by providing side-by-side performance comparison and detailed analysis of different implementation strategies, with robust handling of edge cases.

**Target Audience**: Students learning search algorithms, developers studying algorithm implementation, educators teaching computer science concepts, and anyone interested in understanding binary search and its performance characteristics.

## Features

- Iterative binary search implementation
- Recursive binary search implementation
- Comprehensive edge case handling
- Performance comparison with timing analysis
- Detailed step-by-step logging
- Comprehensive performance reports
- Multiple iterations support for accurate timing
- Array validation (ensures sorted input)
- Error handling for invalid inputs

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

### Step 1: Navigate to Project Directory

```bash
cd /path/to/python-algorithms/binary-search
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

The tool uses a YAML configuration file to define recursion limits and logging settings. The default configuration file is `config.yaml` in the project root.

#### Key Configuration Options

**Recursion Settings:**
- `recursion.max_depth`: Maximum recursion depth allowed (default: 1000)

**Logging Settings:**
- `logging.level`: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `logging.file`: Path to log file (default: "logs/app.log")

### Example Configuration

```yaml
recursion:
  max_depth: 1000

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
python src/main.py 25 1 2 3 4 5 6 7 8 9 10
```

Note: The first argument is the target, followed by the sorted array elements.

### Specific Method

Use a specific search method:

```bash
python src/main.py 25 --method iterative 1 2 3 4 5 6 7 8 9 10
python src/main.py 25 --method recursive 1 2 3 4 5 6 7 8 9 10
```

### Multiple Iterations

Run multiple iterations for more accurate timing:

```bash
python src/main.py 25 --iterations 1000 1 2 3 4 5 6 7 8 9 10
```

### Generate Report

Generate performance report:

```bash
python src/main.py 25 --report report.txt 1 2 3 4 5 6 7 8 9 10
```

### Command-Line Arguments

- `target`: (Required) Target value to search for
- `numbers`: (Required) Sorted array of numbers
- `-c, --config`: Path to configuration file (default: config.yaml)
- `-m, --method`: Search method - iterative, recursive, or compare (default: compare)
- `-i, --iterations`: Number of iterations for timing (default: 1)
- `-r, --report`: Output path for performance report

### Common Use Cases

**Compare Approaches:**
1. Run: `python src/main.py 25 1 2 3 4 5 6 7 8 9 10`
2. Review timing for each approach
3. Identify fastest approach

**Study Algorithms:**
1. Use specific method: `python src/main.py 25 --method iterative 1 2 3 4 5`
2. Review logs to see algorithm execution
3. Understand different approaches

**Performance Analysis:**
1. Test with different array sizes
2. Use multiple iterations: `python src/main.py 25 --iterations 1000 1 2 3 4 5`
3. Generate reports for detailed metrics

**Edge Case Testing:**
1. Test with target not in array
2. Test with empty array
3. Test with single element
4. Test with target at boundaries

## Project Structure

```
binary-search/
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

- `src/main.py`: Contains the `BinarySearch` class and main logic
- `config.yaml`: Configuration file with recursion and logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `logs/`: Directory for application log files

## Algorithm Details

### Binary Search Algorithm

**How It Works:**
1. Compare target with middle element
2. If equal, return index
3. If target is smaller, search left half
4. If target is larger, search right half
5. Repeat until found or search space exhausted

**Time Complexity:**
- Best Case: O(1) - target at middle
- Average Case: O(log n)
- Worst Case: O(log n) - target at end or not found

**Space Complexity:**
- Iterative: O(1) - constant extra space
- Recursive: O(log n) - call stack depth

**Characteristics:**
- Requires sorted array
- Much faster than linear search for large arrays
- Divide and conquer approach
- Logarithmic time complexity

### Edge Cases Handled

- Empty array
- Single element array
- Target not found
- Target at first position
- Target at last position
- Target at middle position
- Unsorted array (validation error)
- Large arrays
- Duplicate values (returns first occurrence)

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
- Search with various inputs
- Edge cases (empty array, single element, not found, boundaries)
- Performance comparison functionality
- Error handling (unsorted array, recursion depth)
- Report generation
- Both implementation approaches
- Array validation

## Troubleshooting

### Common Issues

**ValueError: Array must be sorted:**
- Binary search requires sorted array
- Array is automatically sorted in command-line usage
- When using API, ensure array is sorted

**Target Not Found:**
- This is expected behavior if target doesn't exist
- Returns None (or -1 in some implementations)
- Check that target value is actually in array

**RecursionError:**
- Array is too large for recursive approach
- Increase max_depth in config.yaml (not recommended for very large arrays)
- Use iterative approach for large arrays

**Import Errors:**
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (requires 3.8+)
- Verify virtual environment is activated

### Error Messages

**"Array must be sorted in ascending order"**: The input array is not sorted. Binary search requires a sorted array.

**"Maximum recursion depth exceeded"**: Array is too large for recursive approach. Use iterative method or increase max_depth.

**"Configuration file not found"**: The config.yaml file doesn't exist. Create it or specify path with `-c` option.

### Best Practices

1. **Use iterative approach** for large arrays and production code
2. **Use recursive approach** for learning and small arrays
3. **Always ensure array is sorted** before searching
4. **Compare performance** to understand trade-offs
5. **Use multiple iterations** for accurate timing measurements
6. **Review logs** to see algorithm execution details
7. **Handle None return value** when target is not found

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
