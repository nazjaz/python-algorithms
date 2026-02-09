# Wavelet Tree for Range Queries and Rank/Select Operations on Sequences

A Python implementation of wavelet tree data structure that efficiently supports range queries, rank, and select operations on sequences. Wavelet trees achieve O(log σ) time complexity for queries where σ is the alphabet size.

## Project Title and Description

The Wavelet Tree tool implements a data structure that recursively partitions sequences based on alphabet values, enabling efficient rank, select, and range queries. Wavelet trees use bitvectors at each level to track which half of the alphabet each element belongs to.

This tool solves the problem of efficiently querying sequences for rank (number of occurrences up to position), select (position of k-th occurrence), and range queries (count elements in range with values in range). Wavelet trees provide O(log σ) time complexity for these operations.

**Target Audience**: Algorithm students, competitive programmers, data structure researchers, software engineers, and anyone interested in understanding advanced sequence data structures and compressed data structures.

## Features

- Wavelet tree implementation with recursive alphabet partitioning
- O(log σ) time complexity for rank, select, and range queries
- Bitvector support with rank and select operations
- Range count queries for value ranges
- Access operation for sequence elements
- Comprehensive edge case handling
- Detailed step-by-step logging
- Input validation
- Error handling for invalid inputs

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

### Step 1: Navigate to Project Directory

```bash
cd /path/to/python-algorithms/wavelet-tree
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
python src/main.py
```

## Configuration

### Configuration File (config.yaml)

The tool uses a YAML configuration file to define logging settings. The default configuration file is `config.yaml` in the project root.

#### Key Configuration Options

**Logging Settings:**
- `logging.level`: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `logging.file`: Path to log file (default: "logs/wavelet_tree.log")

### Example Configuration

```yaml
logging:
  level: "INFO"
  file: "logs/wavelet_tree.log"
```

### Environment Variables

No environment variables are currently required. All configuration is managed through the `config.yaml` file.

## Usage

### Basic Usage

Run the main script to see a demonstration of wavelet tree operations:

```bash
python src/main.py
```

This will:
1. Create a wavelet tree from sequence
2. Perform rank operations
3. Perform select operations
4. Perform range count queries

### Programmatic Usage

```python
from src.main import WaveletTree

# Create wavelet tree
sequence = [1, 2, 3, 1, 2, 3, 1, 2, 3, 4, 5]
tree = WaveletTree(sequence)

# Rank operation
rank = tree.rank(5, 1)  # Number of 1's up to position 5
print(f"Rank: {rank}")

# Select operation
pos = tree.select(2, 1)  # Position of 2nd occurrence of 1
print(f"Position: {pos}")

# Range count
count = tree.range_count(0, 5, 1, 2)  # Count values [1,2] in positions [0,5]
print(f"Count: {count}")

# Access
value = tree.access(3)  # Element at position 3
print(f"Value: {value}")
```

### Common Use Cases

**Sequence Queries:**
1. Count occurrences of values up to position
2. Find positions of k-th occurrences
3. Query ranges of values in position ranges

**Competitive Programming:**
1. Fast rank/select queries
2. Range queries on sequences
3. Sequence-based problems

**Data Compression:**
1. Compressed sequence representation
2. Efficient queries on compressed data
3. Text indexing

## Project Structure

```
wavelet-tree/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── config.yaml              # Configuration file
├── .gitignore               # Git ignore patterns
├── src/
│   └── main.py           # Main application code
├── tests/
│   └── test_main.py         # Unit tests
├── docs/
│   └── API.md               # API documentation
└── logs/
    └── .gitkeep             # Placeholder for logs directory
```

### File Descriptions

- `src/main.py`: Contains `WaveletTree`, `WaveletNode`, and `BitVector` classes
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `logs/`: Directory for application log files

## Algorithm Details

### Wavelet Tree

**Definition:**
A wavelet tree is a data structure that recursively partitions a sequence based on alphabet values. At each level, elements are split into two groups based on whether their value is in the lower or upper half of the current alphabet range.

**Properties:**
1. O(log σ) height where σ is alphabet size
2. Bitvector at each level
3. O(n log σ) space complexity
4. O(log σ) query time

**Structure:**
```
        Root (alphabet [1, 5])
       /                        \
   Left [1, 3]              Right [4, 5]
   /        \                /        \
[1,2]      [3,3]          [4,4]      [5,5]
```

### Alphabet Partitioning

**Strategy:**
- At each level, split alphabet in half
- Left subtree: values <= mid
- Right subtree: values > mid
- Continue recursively until single value

**Bitvector:**
- 0 if value <= mid (goes to left)
- 1 if value > mid (goes to right)

### Rank Operation

**Definition:**
Rank(pos, value) returns number of occurrences of value up to position pos.

**Algorithm:**
1. Start at root
2. Determine which subtree value belongs to
3. Count elements in that subtree up to mapped position
4. Recursively query appropriate subtree

**Time Complexity:** O(log σ)

### Select Operation

**Definition:**
Select(k, value) returns position of k-th occurrence of value.

**Algorithm:**
1. Recursively find position in child subtree
2. Map position back using bitvector select
3. Continue up tree

**Time Complexity:** O(log σ)

### Range Count Operation

**Definition:**
RangeCount(left, right, min_val, max_val) counts elements in positions [left, right] with values in [min_val, max_val].

**Algorithm:**
1. If range entirely in one subtree, query that subtree
2. If range spans both subtrees, query both and combine
3. Map positions correctly at each level

**Time Complexity:** O(log σ)

### Operations

**Construction:**
- Time Complexity: O(n log σ)
- Builds tree recursively
- One-time preprocessing

**Rank:**
- Time Complexity: O(log σ)
- Counts occurrences up to position

**Select:**
- Time Complexity: O(log σ)
- Finds k-th occurrence position

**Range Count:**
- Time Complexity: O(log σ)
- Counts elements in range

**Access:**
- Time Complexity: O(1)
- Direct array access

### Edge Cases Handled

- Empty sequence
- Single element sequence
- Single value sequence
- Out of bounds positions
- Invalid value ranges
- Values not in alphabet
- Invalid k values

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
- BitVector creation and operations
- WaveletTree creation
- Rank operations
- Select operations
- Range count operations
- Access operations
- Edge cases (empty, single element, invalid inputs)
- Large sequences

## Troubleshooting

### Common Issues

**Incorrect query results:**
- Verify sequence is correct
- Check that values are in alphabet
- Ensure positions are valid

**Performance issues:**
- Wavelet trees are O(log σ) per query
- For small alphabets, performance is excellent
- For large alphabets, consider optimizations

**Memory issues:**
- Wavelet trees use O(n log σ) space
- For very large sequences, monitor memory
- Consider compressed representations

### Error Messages

**"Sequence cannot be empty"**: Attempted to create tree from empty sequence.

**"Position X out of bounds"**: Position not in valid range [0, n-1].

**"k must be positive"**: Invalid k value for select operation.

**"Invalid range"**: Range positions are invalid.

### Best Practices

1. **Use for sequence queries** - Wavelet trees excel at rank/select/range queries
2. **Consider alphabet size** - Performance depends on log of alphabet size
3. **Validate inputs** - Check positions and values before queries
4. **Monitor performance** - Track query times for your specific use case
5. **Consider alternatives** - For simple queries, arrays might be sufficient

## Performance Characteristics

### Time Complexity

| Operation | Time Complexity |
|-----------|----------------|
| Construction | O(n log σ) |
| Rank | O(log σ) |
| Select | O(log σ) |
| Range Count | O(log σ) |
| Access | O(1) |

Where n is sequence length and σ is alphabet size.

### Space Complexity

- Sequence storage: O(n)
- Bitvectors: O(n log σ)
- Total: O(n log σ)

### Query Performance

- Rank/Select: O(log σ) - depends on alphabet size
- Range Count: O(log σ) - efficient for value ranges
- Access: O(1) - direct array access
- Optimal for sequences with small alphabets

## Applications

- **Text Indexing**: Rank/select on text sequences
- **Compressed Data Structures**: Efficient queries on compressed sequences
- **Competitive Programming**: Fast sequence queries
- **Bioinformatics**: Sequence analysis and queries
- **Data Compression**: Compressed sequence representation

## Comparison with Other Data Structures

**Wavelet Tree:**
- O(log σ) queries
- O(n log σ) space
- Good for small alphabets
- Supports rank/select/range

**Suffix Array:**
- O(log n) queries
- O(n) space
- Good for text
- Different use case

**Fenwick Tree:**
- O(log n) queries
- O(n) space
- Good for prefix sums
- Less flexible

**Segment Tree:**
- O(log n) queries
- O(n) space
- Good for ranges
- Less efficient for rank/select

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
