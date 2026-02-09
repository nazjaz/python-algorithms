# Heap Data Structure

A Python implementation of heap data structure with min-heap and max-heap, including heapify operations and heap sort algorithm. This tool provides comprehensive heap operations, performance comparison, and detailed analysis.

## Project Title and Description

The Heap Data Structure tool implements both min-heap and max-heap data structures with heapify operations and heap sort algorithm. A heap is a complete binary tree that satisfies the heap property, making it efficient for priority queue operations and sorting.

This tool solves the problem of implementing efficient heap data structures for priority queue operations, finding minimum/maximum elements, and sorting arrays using heap sort algorithm. It demonstrates how heapify operations maintain heap properties and how heap sort provides O(n log n) sorting.

**Target Audience**: Students learning data structures, developers studying heap operations and sorting algorithms, educators teaching computer science concepts, and anyone interested in understanding heap data structures and their applications.

## Features

- Min-heap implementation with all operations
- Max-heap implementation with all operations
- Heapify up and heapify down operations
- Heap sort algorithm (ascending and descending)
- Build heap from array
- Insert and extract operations
- Peek at root element
- Performance comparison with built-in sorted()
- Comprehensive edge case handling
- Detailed step-by-step logging
- Multiple iterations support for accurate timing

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

### Step 1: Navigate to Project Directory

```bash
cd /path/to/python-algorithms/heap-data-structure
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

### Min-Heap Operations

Build and use min-heap:

```bash
python src/main.py 5 2 8 1 9 3 --operation minheap
```

### Max-Heap Operations

Build and use max-heap:

```bash
python src/main.py 5 2 8 1 9 3 --operation maxheap
```

### Heap Sort

Sort array using heap sort:

```bash
python src/main.py 5 2 8 1 9 3 --operation heapsort --direction asc
python src/main.py 5 2 8 1 9 3 --operation heapsort --direction desc
```

### Performance Comparison

Compare heap sort with built-in sorted():

```bash
python src/main.py 5 2 8 1 9 3 --operation compare
```

### Multiple Iterations

Run multiple iterations for more accurate timing:

```bash
python src/main.py 5 2 8 1 9 3 --operation compare --iterations 1000
```

### Command-Line Arguments

- `numbers`: (Required) Numbers to operate on (space-separated)
- `-c, --config`: Path to configuration file (default: config.yaml)
- `-o, --operation`: Operation to perform - minheap, maxheap, heapsort, or compare (default: compare)
- `-d, --direction`: Sort direction for heap sort - asc or desc (default: asc)
- `-i, --iterations`: Number of iterations for timing (default: 1)

### Common Use Cases

**Priority Queue (Min-Heap):**
1. Run: `python src/main.py 5 2 8 1 9 3 --operation minheap`
2. Review heap structure
3. Extract minimum elements in order

**Priority Queue (Max-Heap):**
1. Run: `python src/main.py 5 2 8 1 9 3 --operation maxheap`
2. Review heap structure
3. Extract maximum elements in order

**Sorting:**
1. Use heap sort: `python src/main.py 5 2 8 1 9 3 --operation heapsort`
2. Compare with built-in: `python src/main.py 5 2 8 1 9 3 --operation compare`
3. Review performance differences

**Performance Analysis:**
1. Test with different array sizes
2. Use multiple iterations: `python src/main.py 5 2 8 1 9 3 --iterations 1000 --operation compare`
3. Compare heap sort with built-in sorted()

**Edge Case Testing:**
1. Test with single element
2. Test with duplicate values
3. Test with already sorted array
4. Test with reverse sorted array
5. Test with empty array

## Project Structure

```
heap-data-structure/
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

- `src/main.py`: Contains `MinHeap`, `MaxHeap`, and `HeapSort` classes
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `logs/`: Directory for application log files

## Algorithm Details

### Heap Data Structure

**Definition:**
A heap is a complete binary tree that satisfies the heap property:
- **Min-Heap**: Parent ≤ Children (minimum at root)
- **Max-Heap**: Parent ≥ Children (maximum at root)

**Properties:**
- Complete binary tree (all levels filled except possibly last)
- Heap property maintained at all times
- Root contains min (min-heap) or max (max-heap)
- Efficient insertion and extraction operations

### Min-Heap Operations

**Insert:**
1. Add element to end of array
2. Heapify up to maintain heap property
3. Time: O(log n)

**Extract Min:**
1. Remove root element
2. Move last element to root
3. Heapify down to maintain heap property
4. Time: O(log n)

**Build Heap:**
1. Start from last non-leaf node
2. Heapify down for each node
3. Time: O(n)

### Max-Heap Operations

**Insert:**
1. Add element to end of array
2. Heapify up to maintain heap property
3. Time: O(log n)

**Extract Max:**
1. Remove root element
2. Move last element to root
3. Heapify down to maintain heap property
4. Time: O(log n)

**Build Heap:**
1. Start from last non-leaf node
2. Heapify down for each node
3. Time: O(n)

### Heapify Operations

**Heapify Up:**
- Moves element up tree by swapping with parent
- Used after insertion
- Maintains heap property upward
- Time: O(log n)

**Heapify Down:**
- Moves element down tree by swapping with child
- Used after extraction or during build
- Maintains heap property downward
- Time: O(log n)

### Heap Sort Algorithm

**How It Works:**
1. Build max-heap (for ascending) or min-heap (for descending)
2. Repeatedly extract root and place at end
3. Reduce heap size and heapify
4. Continue until heap is empty

**Time Complexity:**
- Best Case: O(n log n)
- Average Case: O(n log n)
- Worst Case: O(n log n)

**Space Complexity:**
- O(1) for in-place sorting (if modifying input)
- O(n) if creating copy

**Characteristics:**
- In-place sorting algorithm
- Guaranteed O(n log n) time complexity
- Not stable (equal elements may change order)
- Good for worst-case scenarios

### Edge Cases Handled

- Empty array
- Single element array
- Duplicate values
- Already sorted array
- Reverse sorted array
- Large arrays
- Negative numbers
- Floating point numbers

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
- Min-heap operations (insert, extract, peek, build)
- Max-heap operations (insert, extract, peek, build)
- Heapify operations (up and down)
- Heap sort (ascending and descending)
- Edge cases (empty, single element, duplicates, sorted arrays)
- Performance comparison functionality
- Error handling (empty heap operations)
- Input validation

## Troubleshooting

### Common Issues

**Empty Heap Operations:**
- extract_min() and extract_max() return None for empty heap
- peek() returns None for empty heap
- Check is_empty() before extraction

**Heap Property Violation:**
- Always use heapify operations after modifications
- Use build_heap() when constructing from array
- Don't manually modify heap array

**Import Errors:**
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (requires 3.8+)
- Verify virtual environment is activated

### Error Messages

**"Attempted to extract from empty heap"**: Heap is empty. Check is_empty() before extraction.

**"Configuration file not found"**: The config.yaml file doesn't exist. Create it or specify path with `-c` option.

### Best Practices

1. **Use build_heap()** when constructing heap from existing array (O(n) vs O(n log n))
2. **Use heapify operations** to maintain heap property after modifications
3. **Check is_empty()** before extraction operations
4. **Use appropriate heap type** (min-heap for minimum, max-heap for maximum)
5. **Heap sort is in-place** but creates copy by default for safety
6. **Compare performance** to understand trade-offs
7. **Use multiple iterations** for accurate timing measurements
8. **Review logs** to see heapify operations

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
