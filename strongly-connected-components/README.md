# Strongly Connected Components

A Python implementation of Kosaraju's algorithm to find strongly connected components (SCCs) in a directed graph. This tool provides comprehensive SCC analysis, performance comparison, and detailed logging to help understand how the algorithm works.

## Project Title and Description

The Strongly Connected Components tool implements Kosaraju's algorithm to find all strongly connected components in a directed graph. A strongly connected component is a maximal set of vertices such that every vertex in the set is reachable from every other vertex in the set. The tool provides detailed logging, performance analysis, and comprehensive edge case handling.

This tool solves the problem of identifying groups of vertices in a directed graph that form strongly connected components, which is fundamental to understanding graph structure and is used in various applications like compiler design, social network analysis, and web page ranking.

**Target Audience**: Students learning graph algorithms, developers studying strongly connected components and Kosaraju's algorithm, educators teaching computer science concepts, and anyone interested in understanding graph algorithms and their performance characteristics.

## Features

- Kosaraju's algorithm implementation for finding SCCs
- SCC count and statistics
- Largest SCC identification
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
cd /path/to/python-algorithms/strongly-connected-components
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

### Find All SCCs (Default)

Find all strongly connected components:

```bash
python src/main.py --edges 0-1 1-2 2-0 3-4 --num-vertices 5 --method find
```

### Get SCC Count

Get the number of strongly connected components:

```bash
python src/main.py --edges 0-1 1-2 2-0 3-4 --num-vertices 5 --method count
```

### Get Largest SCC

Get the largest strongly connected component:

```bash
python src/main.py --edges 0-1 1-2 2-0 3-4 --num-vertices 5 --method largest
```

### Get SCC Statistics

Get statistics about all SCCs:

```bash
python src/main.py --edges 0-1 1-2 2-0 3-4 --num-vertices 5 --method stats
```

### Performance Comparison

Compare performance of different operations:

```bash
python src/main.py --edges 0-1 1-2 2-0 3-4 --num-vertices 5 --method compare
```

### Multiple Iterations

Run multiple iterations for more accurate timing:

```bash
python src/main.py --edges 0-1 1-2 2-0 --iterations 1000 --method compare
```

### Generate Report

Generate performance report:

```bash
python src/main.py --edges 0-1 1-2 2-0 --method compare --report report.txt
```

### Command-Line Arguments

- `-e, --edges`: Edges as 'source-dest' pairs (e.g., '0-1 1-2')
- `-n, --num-vertices`: Number of vertices (if not specified, inferred from edges)
- `-c, --config`: Path to configuration file (default: config.yaml)
- `-m, --method`: Operation method - find, count, largest, stats, or compare (default: find)
- `-i, --iterations`: Number of iterations for timing (default: 1)
- `-r, --report`: Output path for performance report

### Common Use Cases

**Find All SCCs:**
1. Run: `python src/main.py --edges 0-1 1-2 2-0 --method find`
2. Review all strongly connected components
3. Understand graph structure

**Analyze Graph:**
1. Get statistics: `python src/main.py --edges 0-1 1-2 2-0 --method stats`
2. Review SCC count, sizes, and distribution
3. Identify largest components

**Performance Analysis:**
1. Test with different graph sizes
2. Use multiple iterations: `python src/main.py --edges 0-1 1-2 --iterations 1000 --method compare`
3. Generate reports for detailed metrics

**Edge Case Testing:**
1. Test with empty graph
2. Test with single vertex
3. Test with isolated vertices
4. Test with complete graph (all vertices in one SCC)
5. Test with no edges (each vertex is its own SCC)

## Project Structure

```
strongly-connected-components/
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

- `src/main.py`: Contains the `StronglyConnectedComponents` class and main logic
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `logs/`: Directory for application log files

## Algorithm Details

### Strongly Connected Components

**Definition:**
A strongly connected component (SCC) of a directed graph is a maximal set of vertices such that for every pair of vertices u and v in the set, there is a directed path from u to v and from v to u.

**Applications:**
- Compiler design (finding loops in control flow graphs)
- Social network analysis (identifying communities)
- Web page ranking (identifying related pages)
- Network analysis (identifying clusters)
- Database systems (optimizing queries)

### Kosaraju's Algorithm

**How It Works:**
1. **First DFS Pass**: Perform DFS on the original graph and fill a stack with vertices in order of finishing times (vertices that finish later are pushed first)
2. **Build Transpose Graph**: Create a graph with all edges reversed
3. **Second DFS Pass**: Process vertices from the stack (in reverse finishing order) on the transpose graph. Each DFS tree in this pass forms one SCC

**Time Complexity:**
- Best Case: O(V + E) where V=vertices, E=edges
- Average Case: O(V + E)
- Worst Case: O(V + E)

**Space Complexity:**
- O(V + E) for adjacency lists, transpose graph, and stack

**Characteristics:**
- Two-pass DFS algorithm
- Requires building transpose graph
- Optimal time complexity
- Simple to understand and implement

### Why Kosaraju's Algorithm Works

1. **First Pass**: By processing vertices in finishing time order, we ensure that when we process a vertex in the second pass, all vertices in its SCC that finish later have already been processed
2. **Transpose Graph**: Reversing edges allows us to explore backwards from sink components
3. **Second Pass**: Processing in reverse finishing order ensures we find complete SCCs before moving to the next

### Edge Cases Handled

- Empty graph (no vertices)
- Single vertex graph
- Graph with isolated vertices (each vertex is its own SCC)
- Complete graph (all vertices in one SCC)
- Graph with no edges (each vertex is its own SCC)
- Multiple SCCs of different sizes
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
- Kosaraju's algorithm with various graphs
- SCC finding with different graph structures
- Edge cases (empty graph, single vertex, isolated vertices, complete graph)
- Performance comparison functionality
- Error handling (invalid inputs, invalid edges)
- Report generation
- All operation methods (find, count, largest, stats)
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

1. **Use find_sccs()** to get all SCCs when you need complete information
2. **Use get_scc_count()** when you only need the number of SCCs (faster)
3. **Use get_largest_scc()** to identify the largest component
4. **Use get_scc_statistics()** for comprehensive analysis
5. **Compare performance** to understand trade-offs between operations
6. **Use multiple iterations** for accurate timing measurements
7. **Review logs** to see algorithm execution details
8. **Validate inputs** before processing to catch errors early

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
