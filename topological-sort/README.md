# Topological Sort Algorithm

A Python implementation of topological sort algorithm for directed acyclic graphs (DAGs) with cycle detection. This tool provides both Kahn's algorithm (BFS-based) and DFS-based implementations, with comprehensive performance comparison and detailed analysis.

## Project Title and Description

The Topological Sort tool implements topological sorting algorithms using both Kahn's algorithm (BFS-based) and DFS-based approaches. It provides detailed logging, performance comparison, cycle detection, and comprehensive edge case handling to help understand how different algorithms solve graph ordering problems.

This tool solves the problem of finding a linear ordering of vertices in a directed graph such that for every directed edge (u, v), vertex u comes before vertex v in the ordering. It also detects cycles, which prevent topological sorting in directed graphs.

**Target Audience**: Students learning graph algorithms, developers studying topological sorting and cycle detection, educators teaching computer science concepts, and anyone interested in understanding graph algorithms and their performance characteristics.

## Features

- Kahn's algorithm implementation (BFS-based)
- DFS-based topological sort implementation
- Cycle detection with cycle path identification
- Comprehensive edge case handling
- Performance comparison with timing analysis
- Detailed step-by-step logging
- Comprehensive performance reports
- Multiple iterations support for accurate timing
- Input validation for edges and vertices
- Error handling for invalid inputs
- Support for graphs with isolated vertices

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

### Step 1: Navigate to Project Directory

```bash
cd /path/to/python-algorithms/topological-sort
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
python src/main.py --edges 0-1 1-2 2-3 --num-vertices 4
```

### Specific Method

Use a specific solution method:

```bash
python src/main.py --edges 0-1 1-2 2-3 --num-vertices 4 --method kahn
python src/main.py --edges 0-1 1-2 2-3 --num-vertices 4 --method dfs
```

### Cycle Detection

Detect cycles in the graph:

```bash
python src/main.py --edges 0-1 1-2 2-0 --method cycle
```

### Multiple Iterations

Run multiple iterations for more accurate timing:

```bash
python src/main.py --edges 0-1 1-2 2-3 --num-vertices 4 --iterations 1000
```

### Generate Report

Generate performance report:

```bash
python src/main.py --edges 0-1 1-2 2-3 --num-vertices 4 --report report.txt
```

### Command-Line Arguments

- `-e, --edges`: Edges as 'source-dest' pairs (e.g., '0-1 1-2')
- `-n, --num-vertices`: Number of vertices (if not specified, inferred from edges)
- `-c, --config`: Path to configuration file (default: config.yaml)
- `-m, --method`: Solution method - kahn, dfs, compare, or cycle (default: compare)
- `-i, --iterations`: Number of iterations for timing (default: 1)
- `-r, --report`: Output path for performance report

### Common Use Cases

**Compare Approaches:**
1. Run: `python src/main.py --edges 0-1 1-2 2-3 --num-vertices 4`
2. Review timing for each approach
3. Identify fastest approach

**Study Algorithms:**
1. Use specific method: `python src/main.py --edges 0-1 1-2 --method kahn`
2. Review logs to see algorithm execution
3. Understand different approaches

**Cycle Detection:**
1. Test with cyclic graph: `python src/main.py --edges 0-1 1-2 2-0 --method cycle`
2. Review cycle path if detected
3. Understand why topological sort fails with cycles

**Performance Analysis:**
1. Test with different graph sizes
2. Use multiple iterations: `python src/main.py --edges 0-1 1-2 --iterations 1000`
3. Generate reports for detailed metrics

**Edge Case Testing:**
1. Test with empty graph
2. Test with single vertex
3. Test with isolated vertices
4. Test with complete DAG
5. Test with cyclic graph

## Project Structure

```
topological-sort/
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

- `src/main.py`: Contains the `TopologicalSort` class and main logic
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `logs/`: Directory for application log files

## Algorithm Details

### Topological Sort

**Problem Definition:**
Given a directed graph, find a linear ordering of its vertices such that for every directed edge (u, v), vertex u comes before vertex v in the ordering.

**Applications:**
- Task scheduling with dependencies
- Build systems (compiling source files)
- Course prerequisites
- Event ordering
- Package dependency resolution

### Kahn's Algorithm (BFS-based)

**How It Works:**
1. Calculate in-degree for each vertex
2. Initialize queue with vertices having in-degree 0
3. While queue is not empty:
   - Remove vertex from queue and add to result
   - Reduce in-degree of all neighbors
   - Add neighbors with in-degree 0 to queue
4. If all vertices processed, return topological order
5. If not all processed, cycle exists

**Time Complexity:**
- Best Case: O(V + E) where V=vertices, E=edges
- Average Case: O(V + E)
- Worst Case: O(V + E)

**Space Complexity:**
- O(V) for queue and in-degree storage

**Characteristics:**
- BFS-based approach
- Processes vertices level by level
- Natural for parallel processing
- Easy to understand and implement

### DFS-based Algorithm

**How It Works:**
1. Perform DFS traversal of graph
2. Use recursion stack to detect cycles (back edges)
3. Add vertex to result after all descendants processed
4. Reverse result to get topological order
5. If back edge found during DFS, cycle exists

**Time Complexity:**
- Best Case: O(V + E) where V=vertices, E=edges
- Average Case: O(V + E)
- Worst Case: O(V + E)

**Space Complexity:**
- O(V) for recursion stack and visited set

**Characteristics:**
- DFS-based approach
- Processes vertices in depth-first order
- Natural recursion structure
- Can detect cycles during traversal

### Cycle Detection

**How It Works:**
1. Perform DFS traversal
2. Maintain recursion stack to track current path
3. If edge to vertex in recursion stack found, cycle exists
4. Reconstruct cycle path by backtracking

**Time Complexity:**
- O(V + E) where V=vertices, E=edges

**Space Complexity:**
- O(V) for recursion stack and visited set

**Characteristics:**
- Detects cycles efficiently
- Can return cycle path
- Essential for topological sort validation

### Edge Cases Handled

- Empty graph (no vertices)
- Single vertex graph
- Graph with isolated vertices
- Complete DAG (all possible edges)
- Cyclic graph (cycle detection)
- Self-loops (cycles of length 1)
- Multiple cycles
- Disconnected components
- Large graphs
- Invalid edge formats

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
- Kahn's algorithm with various graphs
- DFS algorithm with various graphs
- Cycle detection with various graphs
- Edge cases (empty graph, single vertex, cycles, isolated vertices)
- Performance comparison functionality
- Error handling (invalid inputs, invalid edges)
- Report generation
- Both implementation approaches
- Input validation

## Troubleshooting

### Common Issues

**ValueError: Either edges or num_vertices must be provided:**
- Provide at least edges or num_vertices
- Check that input is not empty

**ValueError: Vertex indices must be non-negative:**
- All vertex indices must be non-negative integers
- Check for negative vertex indices in edges

**ValueError: num_vertices is less than vertices in edges:**
- num_vertices must be at least as large as highest vertex index
- Increase num_vertices or fix edge indices

**Cycle Detected:**
- Topological sort only works on DAGs
- Remove cycles or use cycle detection to identify problematic edges
- Review graph structure

**Invalid edge format:**
- Edges must be in 'source-dest' format (e.g., '0-1')
- Use hyphen to separate source and destination
- Ensure both are integers

**Import Errors:**
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (requires 3.8+)
- Verify virtual environment is activated

### Error Messages

**"Either edges or num_vertices must be provided"**: Provide at least edges or num_vertices parameter.

**"Vertex indices must be non-negative"**: All vertex indices in edges must be non-negative integers.

**"num_vertices is less than vertices in edges"**: The num_vertices parameter must be at least as large as the highest vertex index in edges.

**"Configuration file not found"**: The config.yaml file doesn't exist. Create it or specify path with `-c` option.

### Best Practices

1. **Use Kahn's algorithm** for BFS-style processing and level-by-level ordering
2. **Use DFS algorithm** for recursive processing and depth-first ordering
3. **Always check for cycles** before performing topological sort
4. **Compare both approaches** to understand trade-offs
5. **Use multiple iterations** for accurate timing measurements
6. **Review logs** to see algorithm execution details
7. **Validate inputs** before processing to catch errors early
8. **Handle cycle detection** gracefully in applications

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
