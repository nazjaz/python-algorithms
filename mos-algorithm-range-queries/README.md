# Mo's Algorithm for Offline Range Queries

A Python implementation of Mo's algorithm for efficiently processing multiple offline range queries using square root decomposition optimization.

## Project Title and Description

This project implements Mo's algorithm, a technique for efficiently answering multiple range queries offline. The algorithm uses square root decomposition to reorder queries, reducing the total number of operations needed to process all queries from O(n²) to O(n√n).

Mo's algorithm is particularly useful in competitive programming and computational problems where you need to answer many range queries on an array, such as range sum, distinct count, maximum, minimum, frequency, and mode queries.

**Target Audience**: Competitive programmers, developers working with range query problems, and anyone needing efficient offline query processing.

## Features

- Mo's algorithm with square root decomposition
- Multiple query types:
  - Range sum queries
  - Range distinct count queries
  - Range maximum queries
  - Range minimum queries
  - Range frequency queries (for specific value)
  - Range mode queries (most frequent element)
- Custom query processing with user-defined functions
- Efficient O(n√n) time complexity for Q queries on array of size n
- Command-line interface for interactive use
- Comprehensive test suite

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

No external dependencies are required. The implementation uses only Python standard library.

## Installation

### Step 1: Clone or Navigate to Project Directory

```bash
cd /Users/nasihjaseem/projects/github/python-algorithms/mos-algorithm-range-queries
```

### Step 2: Create Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

Note: This project has no external dependencies for core functionality, but pytest is included for testing.

## Configuration

This project does not require configuration files or environment variables. All functionality is available through the command-line interface or by importing the classes directly.

## Usage

### Command-Line Interface

#### Range Sum Queries

```bash
python src/main.py --array "1,2,3,4,5" --queries "0,2;1,3" --type sum
```

Output:
```
Array: [1, 2, 3, 4, 5]
Number of queries: 2
Block size: 2

Range Sum Queries:
  Query 1: Sum[0..2] = 6
  Query 2: Sum[1..3] = 9
```

#### Range Distinct Count Queries

```bash
python src/main.py --array "1,2,2,3,3,3" --queries "0,2;1,5" --type distinct
```

Output:
```
Range Distinct Count Queries:
  Query 1: Distinct[0..2] = 2
  Query 2: Distinct[1..5] = 3
```

#### Range Maximum Queries

```bash
python src/main.py --array "1,5,3,2,4" --queries "0,2;1,4" --type max
```

#### Range Minimum Queries

```bash
python src/main.py --array "5,1,3,2,4" --queries "0,2;1,4" --type min
```

#### Range Frequency Queries

```bash
python src/main.py --array "1,2,2,3,2,4" --queries "0,2;1,4" --type frequency --target 2
```

#### Range Mode Queries

```bash
python src/main.py --array "1,2,2,3,2,4" --queries "0,2;1,4" --type mode
```

### Programmatic Usage

```python
from src.main import MosAlgorithm, Query

# Create array and queries
array = [1, 2, 3, 4, 5]
mos = MosAlgorithm(array)

queries = [
    Query(0, 2, index=0),
    Query(1, 3, index=1),
]

# Range sum queries
results = mos.range_sum_queries(queries)
print(f"Sum results: {results}")  # [6, 9]

# Range distinct count queries
results = mos.range_distinct_count_queries(queries)
print(f"Distinct count: {results}")

# Range maximum queries
results = mos.range_max_queries(queries)
print(f"Maximum values: {results}")

# Range minimum queries
results = mos.range_min_queries(queries)
print(f"Minimum values: {results}")

# Range frequency queries
results = mos.range_frequency_queries(queries, target_value=2)
print(f"Frequency of 2: {results}")

# Range mode queries
results = mos.range_mode_queries(queries)
print(f"Mode values: {results}")

# Custom query processing
def add_func(index):
    # Custom logic when adding element
    pass

def remove_func(index):
    # Custom logic when removing element
    pass

def get_result():
    # Return current result
    return 0

results = mos.process_queries(queries, add_func, remove_func, get_result)
```

### Common Use Cases

1. **Range Sum Queries**
   ```bash
   python src/main.py --array "1,2,3,4,5" --queries "0,2;1,3" --type sum
   ```

2. **Distinct Element Count**
   ```bash
   python src/main.py --array "1,2,2,3,3,3" --queries "0,5" --type distinct
   ```

3. **Find Maximum in Ranges**
   ```bash
   python src/main.py --array "1,5,3,2,4" --queries "0,2;1,4" --type max
   ```

## Project Structure

```
mos-algorithm-range-queries/
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore patterns
├── src/
│   └── main.py              # Main Mo's algorithm implementation and CLI
├── tests/
│   └── test_main.py         # Comprehensive test suite
├── docs/
│   └── API.md               # API documentation
└── logs/
    └── .gitkeep             # Placeholder for log directory
```

### File Descriptions

- **src/main.py**: Contains the `Query` and `MosAlgorithm` classes with all core functionality for processing range queries.
- **tests/test_main.py**: Comprehensive test suite covering all functionality including edge cases and various query types.
- **docs/API.md**: Detailed API documentation for all classes and methods.
- **logs/**: Directory for log files (if logging to files is enabled).

## Testing

### Run All Tests

```bash
pytest tests/
```

### Run Tests with Coverage

```bash
pytest tests/ --cov=src --cov-report=html
```

### Run Specific Test

```bash
pytest tests/test_main.py::TestMosAlgorithm::test_range_sum_queries_simple
```

### Test Coverage

The test suite aims for comprehensive coverage including:
- All query types (sum, distinct, max, min, frequency, mode)
- Edge cases (empty arrays, single elements, overlapping queries)
- Large arrays
- Negative numbers
- Duplicate values
- Query order preservation

## Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'src'`

**Solution**: Ensure you're running commands from the project root directory, or add the project root to your Python path:
```bash
export PYTHONPATH="${PYTHONPATH}:/path/to/mos-algorithm-range-queries"
```

**Issue**: Tests fail with import errors

**Solution**: Make sure you've installed pytest:
```bash
pip install pytest pytest-cov
```

**Issue**: Queries return incorrect results

**Solution**: 
- Ensure queries use 0-indexed positions
- Check that left <= right for each query
- Verify array indices are within bounds [0, n-1]

**Issue**: Performance is slow for large arrays

**Solution**: Mo's algorithm has O(n√n) complexity. For very large arrays, consider:
- Using segment trees or Fenwick trees for online queries
- Optimizing add/remove functions
- Reducing number of queries if possible

### Error Messages

- **"Queries must have valid indices"**: Ensure all query indices are within array bounds.
- **"Left must be <= right"**: Query left endpoint must be <= right endpoint.

## Contributing

### Development Setup

1. Fork the repository
2. Create a virtual environment
3. Install development dependencies:
   ```bash
   pip install pytest pytest-cov
   ```
4. Create a feature branch: `git checkout -b feature/your-feature-name`

### Code Style Guidelines

- Follow PEP 8 strictly
- Maximum line length: 88 characters
- Use type hints for all functions
- Write docstrings for all public functions and classes
- Run tests before committing

### Pull Request Process

1. Ensure all tests pass
2. Update documentation if needed
3. Write clear commit messages following conventional commit format
4. Submit pull request with description of changes

## Algorithm Details

### Mo's Algorithm

Mo's algorithm processes queries in a specific order to minimize the number of add/remove operations:

1. **Divide into blocks**: Array is divided into blocks of size √n
2. **Sort queries**: 
   - Primary sort by block number of left endpoint
   - Secondary sort by right endpoint (alternating direction for odd blocks)
3. **Process queries**: Maintain current range [L, R] and move it to each query range
4. **Answer queries**: Store results in original query order

### Square Root Decomposition

The algorithm uses square root decomposition:
- Block size = √n
- Queries are grouped by the block containing their left endpoint
- Within each block, queries are sorted by right endpoint
- This ordering minimizes total range movements

### Time Complexity

- **Time**: O((n + q) × √n) where n is array size, q is number of queries
- **Space**: O(n) for storing array and frequency maps
- **Per query**: O(√n) amortized

### Why It Works

By processing queries in the optimized order:
- Left pointer moves at most O(q × √n) times
- Right pointer moves at most O(n × √n) times
- Total operations: O(n√n) instead of O(n²) for naive approach

### Query Types Supported

1. **Sum**: Sum of all elements in range
2. **Distinct Count**: Number of distinct elements
3. **Maximum**: Maximum element in range
4. **Minimum**: Minimum element in range
5. **Frequency**: Count of specific value in range
6. **Mode**: Most frequent element in range

## Mathematical Background

### Square Root Decomposition

Given an array of size n:
- Divide into blocks of size √n
- Process queries grouped by block
- This reduces total operations from O(n²) to O(n√n)

### Query Ordering

Queries are sorted by:
1. Block number: ⌊left / √n⌋
2. Right endpoint: Within same block, sort by right (alternating direction)

This ordering ensures:
- Left pointer moves O(q × √n) times total
- Right pointer moves O(n × √n) times total

## Performance Considerations

- Best for: Multiple offline range queries
- Worst case: When queries are not well-distributed
- Optimization: Alternating right pointer direction reduces movements
- Memory: O(n) for frequency tracking

## Applications

- Competitive programming problems
- Range query problems in arrays
- Statistical queries on data streams
- Offline query processing
- Frequency analysis

## License

This project is provided as-is for educational and practical use. Please refer to the LICENSE file in the parent directory for license information.
