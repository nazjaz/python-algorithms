# Prim's Algorithm for Minimum Spanning Tree

A Python implementation of Prim's algorithm for finding minimum spanning tree (MST) in weighted graphs with different data structure choices. This tool provides both list-based and heap-based implementations, allowing comparison of their performance characteristics.

## Project Title and Description

The Prim's Algorithm tool implements the greedy algorithm to find minimum spanning tree in weighted undirected graphs. It provides two implementations: list-based (O(V²)) and heap-based (O(E log V)), allowing users to choose the optimal approach based on graph density.

This tool solves the problem of finding the minimum cost spanning tree that connects all vertices in a weighted graph. The MST has applications in network design, clustering, approximation algorithms, and various optimization problems. By providing multiple data structure choices, users can optimize performance for their specific graph characteristics.

**Target Audience**: Students learning graph algorithms, developers studying minimum spanning trees and greedy algorithms, educators teaching computer science concepts, and anyone interested in understanding MST algorithms and data structure trade-offs.

## Features

- Prim's algorithm with list-based implementation (O(V²))
- Prim's algorithm with heap-based implementation (O(E log V))
- Min-heap priority queue implementation
- Performance comparison between approaches
- Comprehensive edge case handling
- Detailed step-by-step logging
- Multiple iterations support for accurate timing
- Input validation for edges and vertices
- Error handling for disconnected graphs
- Configurable starting vertex

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

### Step 1: Navigate to Project Directory

```bash
cd /path/to/python-algorithms/prim-mst
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

### List-Based Approach

Find MST using list-based approach (good for dense graphs):

```bash
python src/main.py -n 4 --edges 0-1-1 1-2-2 2-3-3 0-3-4 --operation list
```

### Heap-Based Approach

Find MST using heap-based approach (good for sparse graphs):

```bash
python src/main.py -n 4 --edges 0-1-1 1-2-2 2-3-3 0-3-4 --operation heap
```

### Compare Approaches

Compare performance of both approaches:

```bash
python src/main.py -n 4 --edges 0-1-1 1-2-2 2-3-3 0-3-4 --operation compare
```

### Custom Starting Vertex

Specify starting vertex:

```bash
python src/main.py -n 4 --edges 0-1-1 1-2-2 2-3-3 --operation compare -s 2
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
- `-s, --start-vertex`: Starting vertex (default: 0)
- `-c, --config`: Path to configuration file (default: config.yaml)
- `-o, --operation`: Operation to perform - list, heap, or compare (default: compare)
- `-i, --iterations`: Number of iterations for timing (default: 1)
- `-r, --report`: Output path for performance report

### Common Use Cases

**Dense Graphs (E ≈ V²):**
1. Use list-based approach: `python src/main.py -n 10 --edges ... --operation list`
2. Better performance for dense graphs
3. Simpler implementation

**Sparse Graphs (E << V²):**
1. Use heap-based approach: `python src/main.py -n 100 --edges ... --operation heap`
2. Better performance for sparse graphs
3. More efficient for large sparse graphs

**Performance Comparison:**
1. Compare both: `python src/main.py -n 10 --edges ... --operation compare`
2. Review timing for each approach
3. Choose optimal approach for your graph

**Network Design:**
1. Model network as weighted graph
2. Find MST to minimize connection cost
3. Use MST edges for optimal network topology

## Project Structure

```
prim-mst/
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

- `src/main.py`: Contains `PrimMST` and `MinHeap` classes
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `logs/`: Directory for application log files

## Algorithm Details

### Prim's Algorithm

**How It Works:**
1. Start from an arbitrary vertex
2. Maintain a set of vertices in MST
3. For each vertex not in MST, maintain minimum edge weight to MST
4. Repeatedly add vertex with minimum edge weight to MST
5. Update minimum edge weights for adjacent vertices
6. Stop when all vertices are in MST

**Key Differences from Kruskal's:**
- Prim's grows MST from a starting vertex
- Kruskal's adds edges in sorted order
- Both produce optimal MST but with different approaches

### List-Based Implementation

**How It Works:**
- Uses simple list/array to find minimum key
- Scans all vertices to find minimum in each iteration
- Straightforward implementation

**Time Complexity:**
- O(V²) where V is number of vertices

**Space Complexity:**
- O(V + E) for adjacency list

**Best For:**
- Dense graphs (E ≈ V²)
- Small graphs
- When simplicity is preferred

### Heap-Based Implementation

**How It Works:**
- Uses binary min-heap as priority queue
- Efficiently extracts minimum key vertex
- Updates heap when keys change

**Time Complexity:**
- O(E log V) where E is edges, V is vertices

**Space Complexity:**
- O(V + E) for adjacency list and heap

**Best For:**
- Sparse graphs (E << V²)
- Large graphs
- When performance is critical

### Choosing the Right Approach

**Use List-Based When:**
- Graph is dense (many edges)
- Graph is small
- Simplicity is important

**Use Heap-Based When:**
- Graph is sparse (few edges)
- Graph is large
- Performance is critical

**Rule of Thumb:**
- If E > V log V, list-based may be faster
- If E < V log V, heap-based is usually faster

### Edge Cases Handled

- Empty graph (0 vertices)
- Single vertex graph
- Disconnected graph (error detection)
- Complete graph
- Duplicate edges
- Negative weights
- Large graphs
- Invalid edge formats
- Invalid starting vertex

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
- Prim's algorithm with list-based approach
- Prim's algorithm with heap-based approach
- Performance comparison
- Edge cases (empty, single vertex, disconnected, complete graph)
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

**ValueError: Start vertex out of range:**
- Start vertex must be in range [0, num_vertices-1]
- Check start vertex value

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

**"Start vertex X out of range"**: The start vertex must be within the valid range.

**"Configuration file not found"**: The config.yaml file doesn't exist. Create it or specify path with `-c` option.

### Best Practices

1. **Choose appropriate approach** based on graph density
2. **Use list-based** for dense graphs
3. **Use heap-based** for sparse graphs
4. **Compare approaches** to find optimal for your graph
5. **Ensure graph is connected** before finding MST
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
