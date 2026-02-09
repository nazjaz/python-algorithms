# Merge Sort Algorithm

A Python implementation of the merge sort algorithm with detailed visualization of the divide and conquer process. This tool demonstrates how merge sort recursively divides arrays and merges sorted subarrays, making it ideal for understanding the divide and conquer paradigm.

## Project Title and Description

The Merge Sort Visualizer provides a complete implementation of the merge sort algorithm with comprehensive visualization capabilities. It shows step-by-step how the algorithm divides the array into smaller subarrays, recursively sorts them, and merges them back together in sorted order.

This tool solves the problem of understanding merge sort's divide and conquer approach by providing detailed visualization of each step in the sorting process, including recursion depth, array divisions, and merge operations.

**Target Audience**: Students learning sorting algorithms, developers studying divide and conquer techniques, educators teaching computer science concepts, and anyone interested in understanding how merge sort works.

## Features

- Complete merge sort algorithm implementation
- Detailed visualization of divide and conquer process
- Step-by-step tracking of array divisions
- Merge operation visualization
- Recursion depth tracking
- Comprehensive logging
- Detailed visualization reports
- Error handling for edge cases
- Command-line interface
- Demonstration mode with examples
- Support for various data types (integers, floats, strings)

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

### Step 1: Navigate to Project Directory

```bash
cd /path/to/python-algorithms/merge-sort
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

Sort an array of numbers:

```bash
python src/main.py 64 34 25 12 22 11 90
```

### With Visualization

Show visualization of sorting process:

```bash
python src/main.py 64 34 25 12 22 11 90 --visualize
```

### Detailed Visualization

Show detailed visualization information:

```bash
python src/main.py 64 34 25 12 22 11 90 --visualize --detailed
```

### Generate Report

Generate detailed visualization report:

```bash
python src/main.py 64 34 25 12 22 11 90 --visualize --report report.txt
```

### Demonstration Mode

Run demonstration with example arrays:

```bash
python src/main.py --demo
```

### Command-Line Arguments

- `numbers`: (Optional) Numbers to sort (space-separated)
- `-c, --config`: Path to configuration file (default: config.yaml)
- `-v, --visualize`: Show visualization of sorting process
- `-d, --detailed`: Show detailed visualization information
- `-r, --report`: Output path for visualization report
- `--demo`: Run demonstration with example arrays

### Common Use Cases

**Learn Merge Sort:**
1. Run: `python src/main.py --demo`
2. Review visualization steps
3. Understand divide and conquer process

**Sort Custom Array:**
1. Run: `python src/main.py 64 34 25 12 22 11 90`
2. Review sorted result
3. Use `--visualize` to see process

**Study Algorithm:**
1. Run with visualization: `python src/main.py 5 2 8 1 9 --visualize`
2. Review divide steps
3. Review merge steps
4. Understand recursion depth

**Generate Documentation:**
1. Run: `python src/main.py 5 2 8 1 9 --visualize --report report.txt`
2. Review detailed report
3. Study algorithm complexity

## Project Structure

```
merge-sort/
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

- `src/main.py`: Contains the `MergeSortVisualizer` class with merge sort algorithm and visualization
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `docs/API.md`: API documentation for the visualizer
- `logs/`: Directory for application log files

## Algorithm Details

### Merge Sort Algorithm

Merge sort is a divide and conquer algorithm that works in three phases:

**1. Divide Phase:**
- Split the array into two halves
- Recursively divide each half until arrays have one element

**2. Conquer Phase:**
- Base case: arrays of size 1 are already sorted
- Recursively sort left and right halves

**3. Combine Phase:**
- Merge two sorted subarrays
- Compare elements from both arrays
- Place smaller element in result array
- Continue until both arrays are merged

### Algorithm Steps

**Example: Sorting [64, 34, 25, 12]**

```
Divide:
  [64, 34, 25, 12]
  ├── [64, 34]
  │   ├── [64]
  │   └── [34]
  └── [25, 12]
      ├── [25]
      └── [12]

Conquer (sort):
  [64, 34] → [34, 64]
  [25, 12] → [12, 25]

Combine (merge):
  [34, 64] + [12, 25] → [12, 25, 34, 64]
```

### Time Complexity

- **Best Case**: O(n log n)
- **Average Case**: O(n log n)
- **Worst Case**: O(n log n)

**Analysis:**
- Divide: O(log n) levels of recursion
- Merge: O(n) work at each level
- Total: O(n log n)

### Space Complexity

- **O(n)**: Requires temporary arrays for merging subarrays

### Properties

- **Stable**: Maintains relative order of equal elements
- **Not in-place**: Requires O(n) extra space
- **Guaranteed performance**: Always O(n log n) regardless of input
- **Well-suited for**: Linked lists, external sorting, parallel processing

### Advantages

- Predictable O(n log n) performance
- Stable sorting algorithm
- Works well with linked lists
- Suitable for external sorting
- Parallelizable

### Disadvantages

- Requires O(n) extra space
- Not in-place algorithm
- Slower than quicksort for small arrays
- More complex than simpler algorithms

## Visualization Features

The visualizer provides detailed tracking of:

1. **Divide Steps**: Shows when array is split into subarrays
   - Left and right indices
   - Middle index
   - Subarray contents
   - Recursion depth

2. **Merge Steps**: Shows merging of sorted subarrays
   - Left and right subarrays being merged
   - Merged result
   - Full array state after merge

3. **Recursion Depth**: Tracks level of recursion for each operation

4. **Array States**: Complete array state at each step

5. **Step Counter**: Sequential numbering of all operations

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
- Basic sorting functionality
- Edge cases (empty array, single element, already sorted)
- Different data types (integers, floats, strings)
- Visualization step recording
- Divide and conquer structure
- Merge operation correctness
- Stability of sorting
- Error handling

## Troubleshooting

### Common Issues

**No visualization data available:**
- Visualization was disabled during sorting
- Use `visualize=True` when calling sort method
- Use `--visualize` flag in command line

**Import Errors:**
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (requires 3.8+)
- Verify virtual environment is activated

**Configuration Errors:**
- Check that config.yaml exists and is valid YAML
- Verify logging file path is writable
- Check file permissions

### Error Messages

**"Configuration file not found"**: Config file doesn't exist at specified path. Check file path or create config.yaml.

**"Invalid YAML in configuration file"**: Config file has syntax errors. Verify YAML format.

**"Failed to save report"**: Cannot write report file. Check file permissions and path.

### Best Practices

1. **Use visualization** to understand algorithm: `--visualize`
2. **Generate reports** for documentation: `--report report.txt`
3. **Check logs** to understand sorting process
4. **Start with small arrays** to understand visualization
5. **Use demonstration mode** to see examples: `--demo`
6. **Review recursion depth** to understand divide and conquer

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
