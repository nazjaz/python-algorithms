# Kth Largest Element Finder

A Python implementation for finding the kth largest element in an array using two different approaches: heap data structure and quickselect algorithm. This tool includes performance comparison to analyze the efficiency and trade-offs of each method.

## Project Title and Description

The Kth Largest Element Finder provides complete implementations of two algorithms for finding the kth largest element: heap-based approach and quickselect algorithm. It demonstrates how different data structures and algorithms can solve the same problem with different time/space complexity trade-offs.

This tool solves the problem of efficiently finding the kth largest element without sorting the entire array, which is essential in many applications like finding top-k elements, statistics (median, percentiles), and selection problems.

**Target Audience**: Students learning data structures and algorithms, developers studying selection algorithms, educators teaching algorithm analysis, and anyone interested in understanding heap and quickselect algorithms.

## Features

- Heap-based kth largest finding (min-heap of size k)
- Quickselect algorithm implementation
- Performance comparison between methods
- Execution time measurement
- Comparison and swap counting for quickselect
- Find all k largest elements
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
cd /path/to/python-algorithms/kth-largest-element
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

### Basic Finding

Find kth largest element using both methods:

```bash
python src/main.py 3 1 4 1 5 9 2 6 3
```

### With Specific Method

Find using heap method only:

```bash
python src/main.py 3 1 4 1 5 9 2 6 --method heap 3
```

Find using quickselect method only:

```bash
python src/main.py 3 1 4 1 5 9 2 6 --method quickselect 3
```

### Compare Methods

Compare performance of both methods:

```bash
python src/main.py 3 1 4 1 5 9 2 6 --method both 3
```

### Find All K Largest

Find all k largest elements:

```bash
python src/main.py 3 1 4 1 5 9 2 6 --all 3
```

### Generate Report

Generate detailed analysis report:

```bash
python src/main.py 3 1 4 1 5 9 2 6 --method both --report report.txt 3
```

### Demonstration Mode

Run demonstration with example arrays:

```bash
python src/main.py --demo
```

### Command-Line Arguments

- `numbers`: (Optional) Numbers in array (space-separated)
- `k`: (Optional) Position of largest element to find (1-indexed)
- `-c, --config`: Path to configuration file (default: config.yaml)
- `-m, --method`: Method to use (heap, quickselect, both)
- `--all`: Find all k largest elements (not just kth)
- `-r, --report`: Output path for analysis report
- `--demo`: Run demonstration with example arrays

### Common Use Cases

**Find Kth Largest:**
1. Run: `python src/main.py 3 1 4 1 5 9 2 6 3`
2. Review result from both methods
3. Understand algorithm differences

**Compare Performance:**
1. Run: `python src/main.py 3 1 4 1 5 9 2 6 --method both 3`
2. Review execution times
3. Understand time complexity trade-offs

**Find Top K Elements:**
1. Run: `python src/main.py 3 1 4 1 5 9 2 6 --all 3`
2. Review all k largest elements
3. Understand heap-based approach

## Project Structure

```
kth-largest-element/
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

- `src/main.py`: Contains the `KthLargestFinder` class with heap and quickselect implementations
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `docs/API.md`: API documentation for the finder
- `logs/`: Directory for application log files

## Algorithm Details

### Heap Method

Uses a min-heap of size k to maintain the k largest elements seen so far.

**Algorithm Steps:**
1. Initialize empty min-heap
2. For each element in array:
   - If heap size < k: add element to heap
   - Else if element > heap minimum: replace minimum with element
3. Root of heap is kth largest element

**Example: Finding 3rd largest in [3, 1, 4, 1, 5, 9, 2, 6]**
```
Process 3: heap = [3]
Process 1: heap = [1, 3]
Process 4: heap = [1, 3, 4] (full, min=1)
Process 1: heap = [1, 3, 4] (1 <= 1, skip)
Process 5: heap = [3, 4, 5] (5 > 1, replace)
Process 9: heap = [4, 5, 9] (9 > 3, replace)
Process 2: heap = [4, 5, 9] (2 <= 4, skip)
Process 6: heap = [5, 6, 9] (6 > 4, replace)
Result: 5 (root of heap)
```

**Time Complexity:** O(n log k)
- Process n elements
- Each heap operation: O(log k)
- Total: O(n log k)

**Space Complexity:** O(k)
- Heap stores k elements

### Quickselect Method

Variant of quicksort that only recurses on one side to find kth element.

**Algorithm Steps:**
1. Select random pivot
2. Partition array around pivot
3. If pivot is kth largest: return it
4. Else if pivot rank > k: recurse on left partition
5. Else: recurse on right partition with adjusted k

**Example: Finding 3rd largest in [3, 1, 4, 1, 5, 9, 2, 6]**
```
Initial: [3, 1, 4, 1, 5, 9, 2, 6], k=3
Partition around pivot 5: [9, 6, 5, 3, 4, 1, 2, 1]
Pivot at position 2 (0-indexed), rank = 3
Rank == k: return 5
```

**Time Complexity:**
- **Average Case:** O(n) - each partition reduces problem size
- **Worst Case:** O(n²) - unbalanced partitions

**Space Complexity:** O(log n) - recursion stack depth

### Comparison

| Aspect | Heap Method | Quickselect Method |
|--------|-------------|-------------------|
| Time (Average) | O(n log k) | O(n) |
| Time (Worst) | O(n log k) | O(n²) |
| Space | O(k) | O(log n) |
| Best for | Small k | k near n/2 |
| Guarantees | Always O(n log k) | Average O(n) |

## Applications

### Top-K Problems

- **Top-K Recommendations**: Find top k items
- **Leaderboards**: Find top k players
- **Trending Topics**: Find top k trending items

### Statistics

- **Median Finding**: k = n/2
- **Percentiles**: Various k values
- **Outlier Detection**: Find kth largest/smallest

### Selection Problems

- **Order Statistics**: Finding elements by rank
- **Partitioning**: Divide array by kth element
- **Ranking**: Find rank of specific elements

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
- Heap method correctness
- Quickselect method correctness
- Edge cases (empty array, invalid k, single element)
- Method comparison
- Statistics tracking
- All k largest finding
- Report generation

## Troubleshooting

### Common Issues

**IndexError: k cannot be greater than array length:**
- k must be between 1 and array length
- Check k value before calling methods

**ValueError: k must be at least 1:**
- k must be positive
- Use k >= 1

**Import Errors:**
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (requires 3.8+)
- Verify virtual environment is activated

### Error Messages

**"k must be at least 1"**: k is zero or negative. Use k >= 1.

**"k cannot be greater than array length"**: k exceeds array size. Use k <= array length.

**"Array cannot be empty"**: Array is empty. Provide non-empty array.

### Best Practices

1. **Use heap method** for small k (k << n): `--method heap`
2. **Use quickselect method** for k near n/2: `--method quickselect`
3. **Compare methods** to see performance: `--method both`
4. **Generate reports** for documentation: `--report report.txt`
5. **Use --all** to find all k largest: `--all`
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
