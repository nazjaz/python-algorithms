# Quick Sort Algorithm

A Python implementation of the quicksort algorithm with multiple pivot selection strategies and performance comparison. This tool demonstrates how different pivot selection methods affect sorting performance, making it ideal for understanding algorithm optimization and performance analysis.

## Project Title and Description

The Quick Sort implementation provides a complete quicksort algorithm with five different pivot selection strategies: first, last, middle, random, and median-of-three. It includes comprehensive performance comparison functionality to analyze execution time, comparisons, and swaps for each strategy.

This tool solves the problem of understanding how pivot selection affects quicksort performance, demonstrating that the choice of pivot can significantly impact algorithm efficiency, especially for edge cases like already-sorted or reverse-sorted arrays.

**Target Audience**: Students learning sorting algorithms, developers studying algorithm optimization, educators teaching algorithm analysis, and anyone interested in understanding how pivot selection affects quicksort performance.

## Features

- Complete quicksort implementation
- Five pivot selection strategies:
  - First element
  - Last element
  - Middle element
  - Random element
  - Median-of-three
- Performance comparison across strategies
- Execution time measurement
- Comparison and swap counting
- Detailed performance reports
- Error handling for edge cases
- Command-line interface
- Demonstration mode with examples

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

### Step 1: Navigate to Project Directory

```bash
cd /path/to/python-algorithms/quicksort
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

### Basic Sorting

Sort an array with default pivot strategy (median-of-three):

```bash
python src/main.py 64 34 25 12 22 11 90
```

### With Specific Pivot Strategy

Sort using a specific pivot strategy:

```bash
python src/main.py 64 34 25 12 22 11 90 --pivot random
python src/main.py 64 34 25 12 22 11 90 --pivot first
```

### Compare All Strategies

Compare performance of all pivot strategies:

```bash
python src/main.py 64 34 25 12 22 11 90 --compare
```

### Generate Report

Generate detailed performance comparison report:

```bash
python src/main.py 64 34 25 12 22 11 90 --compare --report report.txt
```

### Demonstration Mode

Run demonstration with example arrays:

```bash
python src/main.py --demo
```

### Command-Line Arguments

- `numbers`: (Optional) Numbers to sort (space-separated)
- `-c, --config`: Path to configuration file (default: config.yaml)
- `-p, --pivot`: Pivot selection strategy (first, last, middle, random, median_of_three)
- `--compare`: Compare all pivot strategies
- `-r, --report`: Output path for comparison report
- `--demo`: Run demonstration with example arrays

### Common Use Cases

**Sort Array:**
1. Run: `python src/main.py 64 34 25 12 22 11 90`
2. Review sorted result
3. Understand quicksort algorithm

**Compare Strategies:**
1. Run: `python src/main.py 64 34 25 12 22 11 90 --compare`
2. Review performance metrics
3. Understand pivot selection impact

**Study Performance:**
1. Run with different arrays (sorted, reverse sorted, random)
2. Compare strategies
3. Understand worst case scenarios

## Project Structure

```
quicksort/
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

- `src/main.py`: Contains the `QuickSort` class with all pivot strategies
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `docs/API.md`: API documentation for the sorter
- `logs/`: Directory for application log files

## Algorithm Details

### Quick Sort Algorithm

Quicksort is a divide-and-conquer algorithm that works by:
1. **Partition**: Select a pivot and partition array into elements < pivot and >= pivot
2. **Recurse**: Recursively sort the two partitions
3. **Combine**: No combine step needed (in-place sorting)

### Pivot Selection Strategies

#### 1. First Element
- **Selection**: First element of subarray
- **Pros**: Simple, no extra computation
- **Cons**: O(n²) worst case for sorted arrays
- **Best for**: Educational purposes

#### 2. Last Element
- **Selection**: Last element of subarray
- **Pros**: Simple, no extra computation
- **Cons**: O(n²) worst case for reverse-sorted arrays
- **Best for**: Educational purposes

#### 3. Middle Element
- **Selection**: Middle element of subarray
- **Pros**: Better than first/last for many cases
- **Cons**: Still can have worst case scenarios
- **Best for**: Simple improvement over first/last

#### 4. Random Element
- **Selection**: Random element from subarray
- **Pros**: Expected O(n log n) performance, avoids worst case
- **Cons**: Requires random number generation
- **Best for**: General-purpose sorting with good average performance

#### 5. Median of Three
- **Selection**: Median of first, middle, and last elements
- **Pros**: Good practical performance, reduces worst case probability
- **Cons**: Slight overhead for median calculation
- **Best for**: General-purpose sorting (often best choice)

### Algorithm Steps

**Partition Function:**
```
1. Select pivot using chosen strategy
2. Move pivot to end of array
3. Initialize partition index
4. For each element:
   - If element < pivot: move to left partition
   - Otherwise: leave in right partition
5. Place pivot in correct position
6. Return pivot position
```

**Quicksort Function:**
```
1. If array size <= 1: return (base case)
2. Partition array around pivot
3. Recursively sort left partition
4. Recursively sort right partition
```

### Time Complexity

| Case | First/Last | Middle | Random | Median-of-Three |
|------|-----------|--------|--------|-----------------|
| Best | O(n log n) | O(n log n) | O(n log n) | O(n log n) |
| Average | O(n log n) | O(n log n) | O(n log n) | O(n log n) |
| Worst | O(n²) | O(n²) | O(n²) | O(n log n) |

**Worst Case Scenarios:**
- **First/Last**: Already sorted or reverse-sorted arrays
- **Middle**: Specific patterns can cause worst case
- **Random**: Very unlikely worst case
- **Median-of-Three**: Rare worst case

### Space Complexity

- **Best Case**: O(log n) - balanced recursion stack
- **Average Case**: O(log n)
- **Worst Case**: O(n) - unbalanced recursion stack

### Properties

- **In-place**: Sorts array in-place (with some modifications)
- **Not Stable**: Relative order of equal elements may change
- **Divide and Conquer**: Recursively solves subproblems
- **Pivot Dependent**: Performance heavily depends on pivot selection

## Performance Comparison

### Example: Sorting [1, 2, 3, 4, 5] (Already Sorted)

- **First**: O(n²) - worst case, many comparisons
- **Last**: O(n log n) - better performance
- **Middle**: O(n log n) - good performance
- **Random**: O(n log n) - expected good performance
- **Median-of-Three**: O(n log n) - good performance

### Example: Sorting [5, 4, 3, 2, 1] (Reverse Sorted)

- **First**: O(n log n) - good performance
- **Last**: O(n²) - worst case, many comparisons
- **Middle**: O(n log n) - good performance
- **Random**: O(n log n) - expected good performance
- **Median-of-Three**: O(n log n) - good performance

## Applications

### General Sorting

- **Arrays and Lists**: Efficient sorting of various data structures
- **In-place Sorting**: When memory is limited
- **Large Datasets**: Good average performance

### Algorithm Design

- **Hybrid Algorithms**: Used in introsort (quicksort + heapsort)
- **Library Implementations**: Many standard libraries use quicksort variants
- **Performance Critical**: When average performance matters more than worst case

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
- All pivot selection strategies
- Sorting correctness for various inputs
- Edge cases (empty array, single element, sorted, reverse sorted)
- Performance comparison functionality
- Statistics tracking
- Report generation

## Troubleshooting

### Common Issues

**Slow Performance with First/Last Pivot:**
- Expected for sorted or reverse-sorted arrays
- Use random or median-of-three for better performance
- This demonstrates worst case behavior

**Import Errors:**
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (requires 3.8+)
- Verify virtual environment is activated

**Configuration Errors:**
- Check that config.yaml exists and is valid YAML
- Verify logging file path is writable
- Check file permissions

### Error Messages

**"Invalid pivot strategy"**: Pivot strategy not recognized. Use one of: first, last, middle, random, median_of_three.

**"Configuration file not found"**: Config file doesn't exist at specified path. Check file path or create config.yaml.

### Best Practices

1. **Use median-of-three** for general-purpose sorting
2. **Use random** when worst case avoidance is critical
3. **Compare strategies** to understand performance differences
4. **Generate reports** for documentation: `--report report.txt`
5. **Test with different inputs** (sorted, reverse sorted, random)
6. **Use demonstration mode** to see examples: `--demo`

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
