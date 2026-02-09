# Tarjan's Algorithm for Finding Strongly Connected Components and Articulation Points

A Python implementation of Tarjan's algorithm that finds strongly connected components (SCCs) in directed graphs and articulation points in undirected graphs. Tarjan's algorithm achieves O(V + E) time complexity using depth-first search with low-link values.

## Project Title and Description

The Tarjan's Algorithm tool implements two variants of Tarjan's algorithm: one for finding strongly connected components in directed graphs and another for finding articulation points (cut vertices) in undirected graphs. Both algorithms use depth-first search with discovery times and low-link values.

This tool solves the problem of efficiently finding strongly connected components and articulation points, which is fundamental in many applications including graph analysis, network reliability, compiler design, and social network analysis. Tarjan's algorithm provides O(V + E) time complexity for both problems.

**Target Audience**: Algorithm students, competitive programmers, data structure researchers, software engineers, and anyone interested in understanding advanced graph algorithms and connectivity analysis.

## Features

- Tarjan's algorithm for strongly connected components (directed graphs)
- Tarjan's algorithm for articulation points (undirected graphs)
- O(V + E) time complexity for both algorithms
- Graph representation supporting directed and undirected graphs
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
cd /path/to/python-algorithms/tarjan-algorithm
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
- `logging.file`: Path to log file (default: "logs/tarjan_algorithm.log")

### Example Configuration

```yaml
logging:
  level: "INFO"
  file: "logs/tarjan_algorithm.log"
```

### Environment Variables

No environment variables are currently required. All configuration is managed through the `config.yaml` file.

## Usage

### Basic Usage

Run the main script to see a demonstration of Tarjan's algorithm:

```bash
python src/main.py
```

This will:
1. Create directed and undirected graphs
2. Find strongly connected components
3. Find articulation points
4. Display results

### Programmatic Usage

```python
from src.main import Graph, TarjanAlgorithm

# Strongly Connected Components (directed graph)
graph = Graph(5, directed=True)
graph.add_edge(0, 1)
graph.add_edge(1, 2)
graph.add_edge(2, 0)
graph.add_edge(1, 3)
graph.add_edge(3, 4)

tarjan = TarjanAlgorithm(graph)
sccs = tarjan.find_strongly_connected_components()
print(f"Number of SCCs: {tarjan.get_scc_count()}")
for scc in sccs:
    print(f"SCC: {scc}")

# Articulation Points (undirected graph)
graph2 = Graph(5, directed=False)
graph2.add_edge(0, 1)
graph2.add_edge(1, 2)
graph2.add_edge(2, 3)
graph2.add_edge(3, 4)

tarjan2 = TarjanAlgorithm(graph2)
articulation_points = tarjan2.find_articulation_points()
print(f"Articulation points: {articulation_points}")
```

### Common Use Cases

**Graph Analysis:**
1. Find strongly connected components
2. Identify articulation points
3. Analyze graph connectivity

**Network Reliability:**
1. Find critical nodes (articulation points)
2. Analyze network robustness
3. Identify vulnerabilities

**Competitive Programming:**
1. Graph connectivity problems
2. SCC-based problems
3. Articulation point problems

## Project Structure

```
tarjan-algorithm/
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

- `src/main.py`: Contains `Graph` and `TarjanAlgorithm` classes
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `logs/`: Directory for application log files

## Algorithm Details

### Tarjan's Algorithm for SCCs

**Definition:**
Tarjan's algorithm finds strongly connected components in a directed graph using DFS with discovery times and low-link values. A strongly connected component is a maximal set of vertices where every vertex can reach every other vertex.

**Properties:**
1. O(V + E) time complexity
2. Uses DFS with stack
3. Tracks discovery time and low-link value
4. Identifies SCCs when low[u] == disc[u]

**Algorithm:**
1. Perform DFS from each unvisited vertex
2. Track discovery time (disc) and low-link value (low)
3. Push vertices onto stack during DFS
4. When low[u] == disc[u], pop stack to form SCC
5. Update low-link values from back edges

### Tarjan's Algorithm for Articulation Points

**Definition:**
Tarjan's algorithm finds articulation points (cut vertices) in an undirected graph. An articulation point is a vertex whose removal increases the number of connected components.

**Properties:**
1. O(V + E) time complexity
2. Uses DFS with parent tracking
3. Tracks discovery time and low-link value
4. Identifies articulation points based on low-link values

**Algorithm:**
1. Perform DFS from each unvisited vertex
2. Track discovery time (disc) and low-link value (low)
3. Track parent in DFS tree
4. Vertex is articulation point if:
   - Root with > 1 children, or
   - Non-root with low[child] >= disc[u]

### Operations

**Add Edge:**
- Time Complexity: O(1)
- Adds edge to graph
- Handles directed/undirected graphs

**Find SCCs:**
- Time Complexity: O(V + E)
- Finds all strongly connected components
- Returns list of SCCs

**Find Articulation Points:**
- Time Complexity: O(V + E)
- Finds all articulation points
- Returns set of vertices

### Edge Cases Handled

- Empty graphs
- Single vertex graphs
- Disconnected graphs
- Cycles
- Trees
- Invalid vertices
- Wrong graph type for operation

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
- Graph creation and operations
- Strongly connected components on various graphs
- Articulation points on various graphs
- Edge cases (empty, single vertex, invalid inputs)
- Error handling for wrong graph types

## Troubleshooting

### Common Issues

**Incorrect SCC/articulation point results:**
- Verify graph structure is correct
- Check that graph type matches operation
- Ensure algorithm completed successfully

**Performance issues:**
- Tarjan's algorithm is O(V + E)
- For very large graphs, monitor performance
- Consider graph size limitations

**Memory issues:**
- Algorithm uses O(V + E) space
- For very large graphs, monitor memory
- Consider optimizations

### Error Messages

**"Strongly connected components require directed graph"**: Attempted to find SCCs in undirected graph.

**"Articulation points require undirected graph"**: Attempted to find articulation points in directed graph.

**"Invalid vertices"**: Vertex index out of bounds.

### Best Practices

1. **Use correct graph type** - SCCs for directed, articulation points for undirected
2. **Validate inputs** - Check vertices before operations
3. **Monitor performance** - Track algorithm times for your graph
4. **Check results** - Verify SCCs and articulation points are correct
5. **Consider alternatives** - For simple cases, other algorithms may be simpler

## Performance Characteristics

### Time Complexity

| Operation | Time Complexity |
|-----------|----------------|
| Add Edge | O(1) |
| Find SCCs | O(V + E) |
| Find Articulation Points | O(V + E) |

Where V is the number of vertices and E is the number of edges.

### Space Complexity

- Graph storage: O(V + E)
- Algorithm overhead: O(V)
- Total: O(V + E)

### Query Performance

- SCC finding: O(V + E) - optimal for directed graphs
- Articulation points: O(V + E) - optimal for undirected graphs
- Both algorithms are optimal

## Applications

- **Graph Analysis**: Connectivity analysis in graphs
- **Network Reliability**: Finding critical nodes
- **Compiler Design**: Control flow analysis
- **Social Networks**: Community detection
- **Competitive Programming**: Graph connectivity problems

## Comparison with Other Methods

**Tarjan's Algorithm:**
- O(V + E) time
- Optimal complexity
- Single DFS pass
- Efficient implementation

**Kosaraju's Algorithm:**
- O(V + E) time
- Two DFS passes
- Simpler but less efficient
- Also finds SCCs

**DFS-based Methods:**
- O(V + E) time
- Multiple passes
- Less efficient
- Simpler implementation

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
