# Floyd-Warshall Algorithm

A Python implementation of Floyd-Warshall algorithm for finding all-pairs shortest paths in weighted directed graphs with path reconstruction capabilities. This tool provides O(V³) solution for shortest path problems between all pairs of vertices.

## Project Title and Description

The Floyd-Warshall tool implements the Floyd-Warshall algorithm to find shortest paths between all pairs of vertices in a weighted directed graph. It includes path reconstruction functionality and can detect negative cycles. The algorithm works with negative edge weights but not negative cycles.

This tool solves the problem of finding shortest paths between every pair of vertices in a graph. Floyd-Warshall is widely used in network routing, social network analysis, and applications requiring all-pairs shortest path information.

**Target Audience**: Students learning graph algorithms, developers studying shortest path problems, network engineers, competitive programmers, educators teaching computer science concepts, and anyone interested in understanding all-pairs shortest path algorithms.

## Features

- Floyd-Warshall algorithm implementation
- All-pairs shortest path calculation
- Path reconstruction between any two vertices
- Negative cycle detection
- Support for negative edge weights
- Performance analysis
- Comprehensive edge case handling
- Detailed step-by-step logging
- Multiple iterations support for accurate timing
- Input validation
- Error handling for invalid inputs

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

### Step 1: Navigate to Project Directory

```bash
cd /path/to/python-algorithms/floyd-warshall
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

### Find All-Pairs Shortest Paths

Find shortest paths between all pairs:

```bash
python src/main.py -n 4 --edges 0-1-1 1-2-2 2-3-3 0-3-4 --all-pairs
```

### Query Specific Path

Query shortest distance between two vertices:

```bash
python src/main.py -n 4 --edges 0-1-1 1-2-2 2-3-3 --query 0 3
```

### Reconstruct Path

Reconstruct actual path between two vertices:

```bash
python src/main.py -n 4 --edges 0-1-1 1-2-2 2-3-3 --path 0 3
```

### Generate Report

Generate performance report:

```bash
python src/main.py -n 10 --edges 0-1-5 1-2-3 --report report.txt --iterations 1000
```

### Command-Line Arguments

- `-n, --num-vertices`: (Required) Number of vertices
- `-e, --edges`: Edges as 'source-dest-weight' (e.g., '0-1-5 1-2-3')
- `-c, --config`: Path to configuration file (default: config.yaml)
- `-q, --query`: Query shortest path from START to END (two integers)
- `-a, --all-pairs`: Display all-pairs shortest distances
- `-p, --path`: Reconstruct path from START to END (two integers)
- `-i, --iterations`: Number of iterations for timing (default: 1)
- `-r, --report`: Output path for performance report

### Common Use Cases

**All-Pairs Shortest Paths:**
1. Create graph: `python src/main.py -n 4 --edges 0-1-1 1-2-2 2-3-3 --all-pairs`
2. Review distance matrix
3. Understand shortest paths between all pairs

**Specific Path Query:**
1. Query path: `python src/main.py -n 4 --edges 0-1-1 1-2-2 --query 0 2`
2. Get shortest distance
3. Verify path exists

**Path Reconstruction:**
1. Reconstruct: `python src/main.py -n 4 --edges 0-1-1 1-2-2 --path 0 2`
2. See actual path vertices
3. Understand route

**Network Analysis:**
1. Model network as graph
2. Find all-pairs shortest paths
3. Analyze network connectivity

## Project Structure

```
floyd-warshall/
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

- `src/main.py`: Contains the `FloydWarshall` class
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `logs/`: Directory for application log files

## Algorithm Details

### Floyd-Warshall Algorithm

**Definition:**
Floyd-Warshall is a dynamic programming algorithm that finds shortest paths between all pairs of vertices in a weighted directed graph. It works by considering each vertex as an intermediate vertex and updating shortest paths.

**How It Works:**
1. Initialize distance matrix with direct edges
2. For each intermediate vertex k:
   - For each pair (i, j):
     - If dist[i][k] + dist[k][j] < dist[i][j], update dist[i][j]
3. Check for negative cycles (diagonal elements < 0)

**Formula:**
- dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

**Time Complexity:**
- O(V³) where V is number of vertices

**Space Complexity:**
- O(V²) for distance and next matrices

**Applications:**
- Network routing
- Social network analysis
- Transportation networks
- Game development (pathfinding)
- DNA sequence alignment

### Path Reconstruction

**How It Works:**
1. Maintain next matrix during Floyd-Warshall
2. next[i][j] = next vertex on path from i to j
3. Reconstruct path by following next pointers

**Example:**
- If next[0][3] = 1, next[1][3] = 2, next[2][3] = 3
- Path from 0 to 3: 0 -> 1 -> 2 -> 3

### Negative Cycle Detection

**How It Works:**
- After Floyd-Warshall, check diagonal elements
- If dist[i][i] < 0 for any i, negative cycle exists
- Shortest paths are not well-defined with negative cycles

**Note:**
- Algorithm can handle negative edge weights
- But cannot handle negative cycles
- Detects and reports negative cycles

### Edge Cases Handled

- Empty graph (0 vertices)
- Single vertex graph
- Disconnected graph (no path = infinity)
- Negative edge weights
- Negative cycles (detected and reported)
- Self-loops
- Multiple edges between same pair
- Large graphs

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
- Floyd-Warshall algorithm with various graphs
- All-pairs shortest path calculation
- Path reconstruction
- Negative cycle detection
- Edge cases (empty graph, disconnected, negative cycles)
- Performance comparison functionality
- Error handling
- Report generation
- Input validation

## Troubleshooting

### Common Issues

**Negative cycle detected:**
- Graph contains negative cycle
- Shortest paths are not well-defined
- Check graph for negative cycles
- Remove or fix negative cycles

**No path exists:**
- Vertices may be in different connected components
- Distance will be infinity
- This is expected for disconnected graphs

**ValueError: Number of vertices must be non-negative:**
- num_vertices must be non-negative
- Check that value is correct

**Invalid edge format:**
- Edges must be in 'source-dest-weight' format (e.g., '0-1-5')
- Use hyphens to separate components
- Ensure all are valid numbers

**Import Errors:**
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (requires 3.8+)
- Verify virtual environment is activated

### Error Messages

**"Graph contains negative cycle"**: The graph has a negative cycle. Shortest paths may not be well-defined.

**"No path from X to Y"**: There is no path between the specified vertices (disconnected graph).

**"Number of vertices must be non-negative"**: The num_vertices parameter must be non-negative.

**"Configuration file not found"**: The config.yaml file doesn't exist. Create it or specify path with `-c` option.

### Best Practices

1. **Use for all-pairs queries** - More efficient than running Dijkstra/Bellman-Ford V times
2. **Check for negative cycles** - Always verify no negative cycles before using results
3. **Handle disconnected graphs** - Some paths may be infinity
4. **Use path reconstruction** - Get actual paths, not just distances
5. **Consider graph size** - O(V³) may be slow for very large graphs
6. **Use for dense graphs** - More efficient than multiple single-source algorithms
7. **Verify results** - Check distances make sense

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
