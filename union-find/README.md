# Union-Find (Disjoint Set) Data Structure

A Python implementation of union-find (disjoint set) data structure with path compression and union by rank optimizations. This tool provides efficient operations for tracking disjoint sets and determining connectivity between elements.

## Project Title and Description

The Union-Find tool implements a disjoint set data structure with two key optimizations: path compression and union by rank. These optimizations provide near-constant time complexity for union and find operations, making it ideal for connectivity problems, network analysis, and graph algorithms.

This tool solves the problem of efficiently tracking disjoint sets and determining whether elements belong to the same set. It's fundamental to many algorithms including Kruskal's minimum spanning tree, connected components, and network connectivity analysis.

**Target Audience**: Students learning data structures, developers studying union-find and graph algorithms, educators teaching computer science concepts, and anyone interested in understanding efficient disjoint set operations.

## Features

- Union-Find data structure with optimizations
- Path compression for efficient find operations
- Union by rank for balanced tree structures
- Find operation with path compression
- Union operation with union by rank
- Connectivity checking
- Component analysis and statistics
- Performance comparison and analysis
- Comprehensive edge case handling
- Detailed step-by-step logging
- Multiple iterations support for accurate timing

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

### Step 1: Navigate to Project Directory

```bash
cd /path/to/python-algorithms/union-find
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

### Union Operations

Union pairs of elements:

```bash
python src/main.py -n 10 --pairs 0-1 1-2 2-3 --operation union
```

### Find Operations

Find roots of elements:

```bash
python src/main.py -n 10 --pairs 0-1 1-2 --operation find
```

### Connectivity Checks

Check if elements are connected:

```bash
python src/main.py -n 10 --pairs 0-1 1-2 0-2 --operation connected
```

### Component Analysis

Get all components:

```bash
python src/main.py -n 10 --pairs 0-1 1-2 3-4 4-5 --operation components
```

### Statistics

Get component statistics:

```bash
python src/main.py -n 10 --pairs 0-1 1-2 3-4 4-5 --operation stats
```

### Performance Comparison

Compare performance of operations:

```bash
python src/main.py -n 100 --pairs 0-1 1-2 2-3 3-4 --operation compare
```

### Multiple Iterations

Run multiple iterations for more accurate timing:

```bash
python src/main.py -n 100 --pairs 0-1 1-2 --iterations 1000 --operation compare
```

### Generate Report

Generate performance report:

```bash
python src/main.py -n 100 --pairs 0-1 1-2 --operation compare --report report.txt
```

### Command-Line Arguments

- `-n, --num-elements`: (Required) Number of elements
- `-p, --pairs`: Pairs as 'x-y' (e.g., '0-1 1-2')
- `-c, --config`: Path to configuration file (default: config.yaml)
- `-o, --operation`: Operation to perform - union, find, connected, components, stats, or compare (default: union)
- `-i, --iterations`: Number of iterations for timing (default: 1)
- `-r, --report`: Output path for performance report

### Common Use Cases

**Connectivity Analysis:**
1. Run: `python src/main.py -n 10 --pairs 0-1 1-2 2-3 --operation union`
2. Check connectivity: `python src/main.py -n 10 --pairs 0-1 1-2 0-2 --operation connected`
3. Review components

**Component Discovery:**
1. Union elements: `python src/main.py -n 10 --pairs 0-1 1-2 3-4 --operation union`
2. Get components: `python src/main.py -n 10 --pairs 0-1 1-2 3-4 --operation components`
3. Analyze structure

**Performance Analysis:**
1. Test with different sizes: `python src/main.py -n 1000 --pairs 0-1 1-2 --operation compare`
2. Use multiple iterations: `python src/main.py -n 1000 --pairs 0-1 1-2 --iterations 1000 --operation compare`
3. Generate reports for detailed metrics

**Edge Case Testing:**
1. Test with single element
2. Test with no unions (all separate)
3. Test with all unions (one component)
4. Test with duplicate unions
5. Test with large number of elements

## Project Structure

```
union-find/
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

- `src/main.py`: Contains the `UnionFind` class and main logic
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `logs/`: Directory for application log files

## Algorithm Details

### Union-Find Data Structure

**Definition:**
Union-Find (also called Disjoint Set) is a data structure that tracks a collection of disjoint sets. It supports two main operations:
- **Find**: Determine which set an element belongs to
- **Union**: Merge two sets into one

**Applications:**
- Kruskal's minimum spanning tree algorithm
- Connected components in graphs
- Network connectivity analysis
- Image processing (connected pixel regions)
- Equivalence relations
- Dynamic connectivity problems

### Path Compression

**How It Works:**
During a find operation, path compression makes all nodes on the path point directly to the root. This flattens the tree structure, making future find operations faster.

**Benefits:**
- Reduces tree height
- Speeds up subsequent find operations
- Amortized time complexity improvement

**Implementation:**
```python
def find(x):
    if parent[x] != x:
        parent[x] = find(parent[x])  # Path compression
    return parent[x]
```

### Union by Rank

**How It Works:**
When unioning two sets, union by rank attaches the smaller tree under the larger tree. This keeps the tree height small and balanced.

**Benefits:**
- Prevents tall, unbalanced trees
- Keeps operations efficient
- Works together with path compression

**Implementation:**
- Track rank (approximate tree height) for each root
- Attach smaller rank tree under larger rank tree
- If ranks equal, attach one to other and increment rank

### Time Complexity

**With Optimizations:**
- **Find**: O(α(n)) amortized where α is inverse Ackermann function
- **Union**: O(α(n)) amortized
- **Connected**: O(α(n)) amortized

**Without Optimizations:**
- **Find**: O(n) worst case
- **Union**: O(n) worst case

**Note:** α(n) grows extremely slowly and is effectively constant (≤ 4) for all practical values of n.

### Space Complexity

- O(n) for parent array
- O(n) for rank array
- Total: O(n)

### Edge Cases Handled

- Empty union-find (0 elements)
- Single element
- No unions (all elements separate)
- All unions (one component)
- Duplicate unions (already connected)
- Invalid element indices
- Large number of elements
- Many union operations

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
- Union operations with various scenarios
- Find operations with path compression
- Connectivity checks
- Component analysis
- Edge cases (empty, single element, all separate, all connected)
- Performance comparison functionality
- Error handling (invalid indices)
- Input validation

## Troubleshooting

### Common Issues

**ValueError: Number of elements must be non-negative:**
- num_elements must be non-negative
- Check that value is correct

**ValueError: Element X is out of range:**
- Element indices must be in range [0, num_elements-1]
- Check element indices in pairs

**Invalid pair format:**
- Pairs must be in 'x-y' format (e.g., '0-1')
- Use hyphen to separate elements
- Ensure both are integers

**Import Errors:**
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (requires 3.8+)
- Verify virtual environment is activated

### Error Messages

**"Number of elements must be non-negative"**: The num_elements parameter must be non-negative.

**"Element X is out of range [0, Y]"**: Element indices must be within the valid range.

**"Configuration file not found"**: The config.yaml file doesn't exist. Create it or specify path with `-c` option.

### Best Practices

1. **Use path compression** for efficient find operations
2. **Use union by rank** to keep trees balanced
3. **Check connectivity** before unioning (optional optimization)
4. **Reset when needed** to start fresh analysis
5. **Use component statistics** to understand structure
6. **Compare performance** to understand trade-offs
7. **Use multiple iterations** for accurate timing measurements
8. **Review logs** to see path compression and union operations

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
