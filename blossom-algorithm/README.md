# Blossom Algorithm for Finding Maximum Matching in General Graphs

A Python implementation of the blossom algorithm (Edmonds' algorithm) that finds maximum matching in general graphs. The algorithm handles odd cycles (blossoms) by contracting them and then expanding after finding augmenting paths.

## Project Title and Description

The Blossom Algorithm tool implements Edmonds' algorithm to find maximum matching in general graphs (not just bipartite graphs). The algorithm handles odd cycles by detecting and contracting them into blossoms, finding augmenting paths, and then expanding the blossoms.

This tool solves the problem of efficiently finding maximum matching in general graphs, which is fundamental in many applications including graph theory, network optimization, and resource allocation. The blossom algorithm provides O(V^2 E) time complexity for finding maximum matching.

**Target Audience**: Algorithm students, competitive programmers, data structure researchers, software engineers, and anyone interested in understanding advanced graph matching algorithms.

## Features

- Blossom algorithm implementation (Edmonds' algorithm)
- O(V^2 E) time complexity for maximum matching
- Handles odd cycles (blossoms) in general graphs
- Blossom contraction and expansion
- Augmenting path finding
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
cd /path/to/python-algorithms/blossom-algorithm
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
- `logging.file`: Path to log file (default: "logs/blossom_algorithm.log")

### Example Configuration

```yaml
logging:
  level: "INFO"
  file: "logs/blossom_algorithm.log"
```

### Environment Variables

No environment variables are currently required. All configuration is managed through the `config.yaml` file.

## Usage

### Basic Usage

Run the main script to see a demonstration of blossom algorithm:

```bash
python src/main.py
```

This will:
1. Create a graph
2. Add edges
3. Find maximum matching
4. Display matching results

### Programmatic Usage

```python
from src.main import BlossomAlgorithm

# Create blossom algorithm instance
blossom = BlossomAlgorithm(6)

# Add edges
blossom.add_edge(0, 1)
blossom.add_edge(1, 2)
blossom.add_edge(2, 3)
blossom.add_edge(3, 4)
blossom.add_edge(4, 5)
blossom.add_edge(5, 0)

# Find maximum matching
matching = blossom.find_maximum_matching()
print(f"Matching size: {blossom.get_matching_size()}")
print(f"Matching: {matching}")

# Check if vertex is matched
if blossom.is_matched(0):
    print(f"Vertex 0 matched to {blossom.get_matched_vertex(0)}")
```

### Common Use Cases

**Graph Matching:**
1. Maximum matching in general graphs
2. Resource allocation
3. Assignment problems

**Competitive Programming:**
1. Maximum matching problems
2. Graph algorithms
3. Optimization problems

**Network Optimization:**
1. Network flow problems
2. Graph theory applications
3. Matching in networks

## Project Structure

```
blossom-algorithm/
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

- `src/main.py`: Contains `BlossomAlgorithm` class
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `logs/`: Directory for application log files

## Algorithm Details

### Blossom Algorithm (Edmonds' Algorithm)

**Definition:**
The blossom algorithm finds maximum matching in general graphs by handling odd cycles (blossoms). It contracts blossoms, finds augmenting paths, and expands blossoms to update the matching.

**Properties:**
1. Works on general graphs (not just bipartite)
2. Handles odd cycles by contraction
3. Finds augmenting paths in contracted graph
4. Expands blossoms after augmentation

**Key Concepts:**
- **Blossom**: Odd cycle in alternating tree
- **Contraction**: Replace blossom with single vertex
- **Augmenting Path**: Path that increases matching
- **Alternating Tree**: Tree with alternating matched/unmatched edges

### Algorithm Steps

1. **Initialize**: Start with empty matching
2. **Find Augmenting Path**: Search for augmenting path from unmatched vertex
3. **Detect Blossom**: If odd cycle found, contract it
4. **Augment**: If augmenting path found, augment matching
5. **Expand**: Expand contracted blossoms
6. **Repeat**: Continue until no augmenting path exists

### Operations

**Add Edge:**
- Time Complexity: O(1)
- Adds undirected edge to graph
- Validates vertices

**Find Maximum Matching:**
- Time Complexity: O(V^2 E)
- Finds maximum matching using blossom algorithm
- Handles odd cycles

**Is Matched:**
- Time Complexity: O(1)
- Checks if vertex is in matching

**Get Matched Vertex:**
- Time Complexity: O(1)
- Returns vertex matched to given vertex

### Edge Cases Handled

- Empty graphs
- Single edge graphs
- Cycles (even and odd)
- Complete graphs
- Star graphs
- Invalid vertices
- Self-loops (ignored)

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
- BlossomAlgorithm creation
- Edge addition
- Maximum matching on various graphs
- Matching queries
- Edge cases (empty, single edge, invalid inputs)
- Different graph structures (paths, cycles, complete graphs)

## Troubleshooting

### Common Issues

**Incorrect matching results:**
- Verify graph structure is correct
- Check that edges are added correctly
- Ensure algorithm completed successfully

**Performance issues:**
- Blossom algorithm is O(V^2 E)
- For large graphs, consider optimizations
- Monitor algorithm performance

**Memory issues:**
- Blossom algorithm uses O(V + E) space
- For very large graphs, monitor memory
- Consider graph size limitations

### Error Messages

**"Invalid vertices"**: Vertex index out of bounds.

**"Invalid vertex"**: Vertex index invalid for query.

### Best Practices

1. **Use for general graphs** - Blossom algorithm works on any graph
2. **Validate inputs** - Check vertices before operations
3. **Monitor performance** - Track algorithm times for your graph
4. **Consider alternatives** - For bipartite graphs, simpler algorithms exist
5. **Test on small graphs** - Verify correctness before scaling

## Performance Characteristics

### Time Complexity

| Operation | Time Complexity |
|-----------|----------------|
| Add Edge | O(1) |
| Find Maximum Matching | O(V^2 E) |
| Is Matched | O(1) |
| Get Matched Vertex | O(1) |

Where V is the number of vertices and E is the number of edges.

### Space Complexity

- Graph storage: O(V + E)
- Algorithm overhead: O(V)
- Total: O(V + E)

### Query Performance

- Maximum matching: O(V^2 E) - handles general graphs
- Matching queries: O(1) - constant time
- Optimal for general graph matching

## Applications

- **Graph Theory**: Maximum matching in general graphs
- **Resource Allocation**: Optimal resource assignment
- **Competitive Programming**: Maximum matching problems
- **Network Optimization**: Matching in networks
- **Assignment Problems**: Optimal assignments

## Comparison with Other Methods

**Blossom Algorithm:**
- O(V^2 E) time
- Works on general graphs
- Handles odd cycles
- More complex

**Bipartite Matching:**
- O(V E) time
- Only works on bipartite graphs
- Simpler implementation
- Faster for bipartite graphs

**Greedy Matching:**
- O(E) time
- Not optimal
- Simple
- Fast but suboptimal

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
