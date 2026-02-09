# Kruskal's Algorithm for Minimum Spanning Tree

A Python implementation of Kruskal's algorithm for finding minimum spanning tree (MST) in weighted graphs. This tool provides efficient MST computation using union-find data structure for cycle detection.

## Project Title and Description

The Kruskal's Algorithm tool implements the greedy algorithm to find minimum spanning tree in weighted undirected graphs. It uses union-find data structure with path compression and union by rank for efficient cycle detection, making it optimal for MST problems.

This tool solves the problem of finding the minimum cost spanning tree that connects all vertices in a weighted graph. The MST has applications in network design, clustering, approximation algorithms, and various optimization problems.

**Target Audience**: Students learning graph algorithms, developers studying minimum spanning trees and greedy algorithms, educators teaching computer science concepts, and anyone interested in understanding MST algorithms and their applications.

## Features

- Kruskal's algorithm implementation
- Union-find data structure for cycle detection
- Path compression and union by rank optimizations
- MST edge list and total weight calculation
- Comprehensive edge case handling
- Performance comparison and analysis
- Detailed step-by-step logging
- Multiple iterations support for accurate timing
- Input validation for edges and vertices
- Error handling for disconnected graphs

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

### Step 1: Navigate to Project Directory

```bash
cd /path/to/python-algorithms/kruskal-mst
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

### Find Minimum Spanning Tree

Find MST with edges and total weight:

```bash
python src/main.py -n 4 --edges 0-1-1 1-2-2 2-3-3 0-3-4 0-2-5 --operation mst
```

### Get MST Edges Only

Get only the edges in MST:

```bash
python src/main.py -n 4 --edges 0-1-1 1-2-2 2-3-3 0-3-4 --operation edges
```

### Get MST Weight Only

Get only the total weight of MST:

```bash
python src/main.py -n 4 --edges 0-1-1 1-2-2 2-3-3 0-3-4 --operation weight
```

### Performance Comparison

Compare performance of different operations:

```bash
python src/main.py -n 10 --edges 0-1-5 1-2-3 2-3-4 --operation compare
```

### Multiple Iterations

Run multiple iterations for more accurate timing:

```bash
python src/main.py -n 10 --edges 0-1-5 1-2-3 --iterations 1000 --operation compare
```

### Generate Report

Generate performance report:

```bash
python src/main.py -n 10 --edges 0-1-5 1-2-3 --operation compare --report report.txt
```

### Command-Line Arguments

- `-n, --num-vertices`: (Required) Number of vertices
- `-e, --edges`: Edges as 'source-dest-weight' (e.g., '0-1-5 1-2-3')
- `-c, --config`: Path to configuration file (default: config.yaml)
- `-o, --operation`: Operation to perform - mst, edges, weight, or compare (default: mst)
- `-i, --iterations`: Number of iterations for timing (default: 1)
- `-r, --report`: Output path for performance report

### Common Use Cases

**Find MST:**
1. Run: `python src/main.py -n 4 --edges 0-1-1 1-2-2 2-3-3 0-3-4 --operation mst`
2. Review MST edges and total weight
3. Verify MST connects all vertices

**Network Design:**
1. Model network as weighted graph
2. Find MST to minimize connection cost
3. Use MST edges for optimal network topology

**Performance Analysis:**
1. Test with different graph sizes
2. Use multiple iterations: `python src/main.py -n 100 --edges 0-1-5 --iterations 1000 --operation compare`
3. Generate reports for detailed metrics

**Edge Case Testing:**
1. Test with single vertex
2. Test with disconnected graph
3. Test with complete graph
4. Test with negative weights
5. Test with duplicate edges

## Project Structure

```
kruskal-mst/
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

- `src/main.py`: Contains `KruskalMST` and `UnionFind` classes
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `logs/`: Directory for application log files

## Algorithm Details

### Minimum Spanning Tree

**Definition:**
A minimum spanning tree (MST) of a weighted undirected graph is a spanning tree with minimum total edge weight. It connects all vertices with the minimum cost.

**Properties:**
- Connects all vertices
- Has exactly V-1 edges (for V vertices)
- No cycles
- Minimum total weight among all spanning trees

**Applications:**
- Network design (minimize connection costs)
- Clustering algorithms
- Approximation algorithms
- Image segmentation
- Circuit design

### Kruskal's Algorithm

**How It Works:**
1. Sort all edges by weight in ascending order
2. Initialize union-find data structure
3. Iterate through edges in sorted order
4. For each edge, check if adding it creates a cycle
5. If no cycle, add edge to MST
6. Stop when we have V-1 edges

**Time Complexity:**
- Best Case: O(E log E) where E=edges
- Average Case: O(E log E)
- Worst Case: O(E log E)

**Space Complexity:**
- O(V) for union-find
- O(E) for edges
- Total: O(V + E)

**Characteristics:**
- Greedy algorithm
- Works with any graph (connected)
- Optimal for sparse graphs
- Uses union-find for cycle detection

### Union-Find for Cycle Detection

**Why Union-Find:**
- Efficiently checks if adding an edge creates a cycle
- Two vertices in same set = cycle would be created
- Two vertices in different sets = safe to add edge

**Optimizations:**
- Path compression: Flattens trees during find
- Union by rank: Keeps trees balanced
- Amortized O(α(n)) per operation

### Edge Cases Handled

- Empty graph (0 vertices)
- Single vertex graph
- Disconnected graph (error detection)
- Complete graph
- Duplicate edges
- Negative weights
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
- Kruskal's algorithm with various graphs
- MST finding with different graph structures
- Edge cases (empty, single vertex, disconnected, complete graph)
- Performance comparison functionality
- Error handling (invalid inputs, disconnected graphs)
- Report generation
- Input validation

## Troubleshooting

### Common Issues

**ValueError: Graph is disconnected:**
- Graph must be connected for MST to exist
- Check that all vertices are reachable
- Verify edge list is complete

**ValueError: Number of vertices must be non-negative:**
- num_vertices must be non-negative
- Check that value is correct

**ValueError: Source/Destination vertex out of range:**
- Vertex indices must be in range [0, num_vertices-1]
- Check vertex indices in edges

**Invalid edge format:**
- Edges must be in 'source-dest-weight' format (e.g., '0-1-5')
- Use hyphens to separate components
- Ensure all are valid numbers

**Import Errors:**
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (requires 3.8+)
- Verify virtual environment is activated

### Error Messages

**"Graph is disconnected"**: The graph is not connected. MST requires a connected graph.

**"Number of vertices must be non-negative"**: The num_vertices parameter must be non-negative.

**"Source/Destination vertex out of range"**: Vertex indices must be within the valid range.

**"Configuration file not found"**: The config.yaml file doesn't exist. Create it or specify path with `-c` option.

### Best Practices

1. **Ensure graph is connected** before finding MST
2. **Use appropriate data types** for weights (int or float)
3. **Validate inputs** before processing
4. **Handle disconnected graphs** gracefully
5. **Compare performance** to understand trade-offs
6. **Use multiple iterations** for accurate timing measurements
7. **Review logs** to see algorithm execution details
8. **Check MST properties** (V-1 edges, connects all vertices)

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
