# Bellman-Ford Algorithm

A Python implementation of Bellman-Ford algorithm for finding shortest paths from a source vertex with negative edge detection and cycle finding. This tool provides O(V*E) solution for shortest path problems and can detect negative cycles.

## Project Title and Description

The Bellman-Ford tool implements the Bellman-Ford algorithm to find shortest paths from a single source vertex in a weighted directed graph. It includes negative cycle detection and cycle finding capabilities. The algorithm works with negative edge weights and can detect negative cycles, making it more flexible than Dijkstra's algorithm.

This tool solves the problem of finding shortest paths from a source vertex when negative edge weights are present. Bellman-Ford is widely used in network routing, currency arbitrage detection, and applications requiring negative cycle detection.

**Target Audience**: Students learning graph algorithms, developers studying shortest path problems, network engineers, competitive programmers, educators teaching computer science concepts, and anyone interested in understanding shortest path algorithms with negative edge support.

## Features

- Bellman-Ford algorithm implementation
- Single-source shortest path calculation
- Negative cycle detection
- Negative cycle finding (returns cycle vertices)
- Path reconstruction between vertices
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
cd /path/to/python-algorithms/bellman-ford
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

### Find Shortest Paths

Find shortest paths from source:

```bash
python src/main.py -n 4 --edges 0-1-1 1-2-2 2-3-3 --source 0
```

### Query Specific Distance

Query shortest distance to target:

```bash
python src/main.py -n 4 --edges 0-1-1 1-2-2 2-3-3 --source 0 --query 3
```

### Display All Distances

Display all distances from source:

```bash
python src/main.py -n 4 --edges 0-1-1 1-2-2 2-3-3 --source 0 --all-distances
```

### Reconstruct Path

Reconstruct actual path to target:

```bash
python src/main.py -n 4 --edges 0-1-1 1-2-2 2-3-3 --source 0 --path 3
```

### Find Negative Cycle

Find negative cycle in graph:

```bash
python src/main.py -n 3 --edges 0-1-1 1-2--2 2-0--1 --source 0 --cycle
```

### Generate Report

Generate performance report:

```bash
python src/main.py -n 10 --edges 0-1-5 1-2-3 --source 0 --report report.txt --iterations 1000
```

### Command-Line Arguments

- `-n, --num-vertices`: (Required) Number of vertices
- `-e, --edges`: Edges as 'source-dest-weight' (e.g., '0-1-5 1-2-3')
- `-s, --source`: Source vertex (default: 0)
- `-c, --config`: Path to configuration file (default: config.yaml)
- `-q, --query`: Query shortest distance to target vertex
- `-a, --all-distances`: Display all distances from source
- `-p, --path`: Reconstruct path to target vertex
- `-cy, --cycle`: Find negative cycle
- `-i, --iterations`: Number of iterations for timing (default: 1)
- `-r, --report`: Output path for performance report

### Common Use Cases

**Shortest Paths from Source:**
1. Create graph: `python src/main.py -n 4 --edges 0-1-1 1-2-2 --source 0 --all-distances`
2. Review distances from source
3. Understand shortest paths

**Path Reconstruction:**
1. Reconstruct: `python src/main.py -n 4 --edges 0-1-1 1-2-2 --source 0 --path 2`
2. See actual path vertices
3. Understand route

**Negative Cycle Detection:**
1. Detect cycle: `python src/main.py -n 3 --edges 0-1-1 1-2--2 2-0--1 --source 0 --cycle`
2. Get cycle vertices
3. Understand negative cycle structure

**Network Routing:**
1. Model network as graph
2. Find shortest paths from router
3. Analyze network connectivity

## Project Structure

```
bellman-ford/
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

- `src/main.py`: Contains the `BellmanFord` class
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `logs/`: Directory for application log files

## Algorithm Details

### Bellman-Ford Algorithm

**Definition:**
Bellman-Ford is a dynamic programming algorithm that finds shortest paths from a single source vertex in a weighted directed graph. It works by relaxing edges repeatedly and can detect negative cycles.

**How It Works:**
1. Initialize distances: dist[source] = 0, others = infinity
2. Relax all edges V-1 times:
   - For each edge (u, v, w): if dist[u] + w < dist[v], update dist[v]
3. Check for negative cycles:
   - If any edge can still be relaxed, negative cycle exists

**Time Complexity:**
- O(V*E) where V is vertices, E is edges

**Space Complexity:**
- O(V) for distance and parent arrays

**Applications:**
- Network routing
- Currency arbitrage detection
- Game development (pathfinding with negative weights)
- Transportation networks
- Distance-vector routing protocols

### Negative Cycle Detection

**How It Works:**
1. After V-1 relaxations, check all edges again
2. If any edge can still be relaxed, negative cycle exists
3. Negative cycle means shortest paths are not well-defined

**Cycle Finding:**
1. Identify edge that can still be relaxed
2. Trace back through parent pointers to find cycle
3. Return cycle vertices

### Path Reconstruction

**How It Works:**
1. Maintain parent array during algorithm
2. parent[v] = vertex that updated v's distance
3. Reconstruct path by following parent pointers backwards

**Example:**
- If parent[3] = 2, parent[2] = 1, parent[1] = 0
- Path from 0 to 3: 0 -> 1 -> 2 -> 3

### Edge Cases Handled

- Empty graph (0 vertices)
- Single vertex graph
- Disconnected graph (no path = infinity)
- Negative edge weights
- Negative cycles (detected and found)
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
- Bellman-Ford algorithm with various graphs
- Shortest path calculation
- Path reconstruction
- Negative cycle detection
- Negative cycle finding
- Edge cases (empty graph, disconnected, negative cycles)
- Performance comparison functionality
- Error handling
- Report generation
- Input validation

## Troubleshooting

### Common Issues

**Negative cycle detected:**
- Graph contains negative cycle reachable from source
- Shortest paths are not well-defined
- Check graph for negative cycles
- Remove or fix negative cycles

**No path exists:**
- Target may be unreachable from source
- Distance will be infinity
- This is expected for disconnected graphs

**ValueError: Source vertex out of range:**
- Source must be in range [0, num_vertices-1]
- Check source vertex value

**Invalid edge format:**
- Edges must be in 'source-dest-weight' format (e.g., '0-1-5')
- Use hyphens to separate components
- Ensure all are valid numbers

**Import Errors:**
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (requires 3.8+)
- Verify virtual environment is activated

### Error Messages

**"Graph contains negative cycle reachable from source"**: The graph has a negative cycle. Shortest paths may not be well-defined.

**"No path from X to Y"**: There is no path between the specified vertices (disconnected graph).

**"Source vertex X out of range"**: The source vertex must be within the valid range.

**"Configuration file not found"**: The config.yaml file doesn't exist. Create it or specify path with `-c` option.

### Best Practices

1. **Use for negative edges** - More flexible than Dijkstra's algorithm
2. **Check for negative cycles** - Always verify no negative cycles before using results
3. **Handle disconnected graphs** - Some paths may be infinity
4. **Use path reconstruction** - Get actual paths, not just distances
5. **Consider graph density** - O(V*E) may be slow for very dense graphs
6. **Use for sparse graphs** - More efficient than Floyd-Warshall for single source
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
