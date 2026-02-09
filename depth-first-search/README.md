# Depth-First Search (DFS) Algorithm

A Python implementation of the depth-first search algorithm on graphs with both recursive and iterative approaches. This tool demonstrates how DFS explores graphs by going as deep as possible before backtracking, and compares the performance and implementation differences between recursive and iterative methods.

## Project Title and Description

The Depth-First Search implementation provides complete DFS algorithms using both recursive and iterative approaches. It demonstrates how the same algorithm can be implemented using function call stack (recursive) or explicit stack data structure (iterative), each with its own advantages and trade-offs.

This tool solves the problem of understanding graph traversal algorithms, which are fundamental to many graph algorithms including path finding, cycle detection, topological sorting, and connected component analysis.

**Target Audience**: Students learning graph algorithms, developers studying graph traversal, educators teaching DFS, and anyone interested in understanding recursive vs iterative algorithm implementations.

## Features

- Graph data structure with adjacency list representation
- Recursive DFS implementation
- Iterative DFS implementation (using stack)
- Path finding between vertices
- Connected component detection
- Graph visualization
- Method comparison functionality
- Comprehensive logging
- Detailed analysis reports
- Support for directed and undirected graphs
- Error handling for edge cases
- Command-line interface
- Demonstration mode with examples

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

### Step 1: Navigate to Project Directory

```bash
cd /path/to/python-algorithms/depth-first-search
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

### Demonstration Mode

Run demonstration with example graphs:

```bash
python src/main.py --demo
```

### With Specific Method

Use recursive or iterative method:

```bash
python src/main.py --demo --method recursive
python src/main.py --demo --method iterative
```

### Compare Methods

Compare recursive and iterative approaches:

```bash
python src/main.py --demo --method both
```

### With Graph Visualization

Show graph structure:

```bash
python src/main.py --demo --visualize
```

### Path Finding

Find path between vertices:

```bash
python src/main.py --demo --target G
```

### Find Connected Components

Find all connected components:

```bash
python src/main.py --demo --components
```

### Generate Report

Generate detailed analysis report:

```bash
python src/main.py --demo --method both --report report.txt
```

### Command-Line Arguments

- `-c, --config`: Path to configuration file (default: config.yaml)
- `-m, --method`: DFS method to use (recursive, iterative, both)
- `-s, --start`: Starting vertex for DFS
- `-t, --target`: Target vertex for path finding
- `--components`: Find all connected components
- `-v, --visualize`: Show graph visualization
- `-r, --report`: Output path for analysis report
- `--demo`: Run demonstration with example graphs

### Common Use Cases

**Learn DFS Algorithm:**
1. Run: `python src/main.py --demo`
2. Review traversal order
3. Understand depth-first exploration

**Compare Methods:**
1. Run: `python src/main.py --demo --method both`
2. Review execution times
3. Understand implementation differences

**Study Graph Structure:**
1. Run: `python src/main.py --demo --visualize`
2. Review graph representation
3. Understand adjacency list

**Path Finding:**
1. Run: `python src/main.py --demo --target G`
2. Review path from start to target
3. Understand path discovery

## Project Structure

```
depth-first-search/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── config.yaml              # Configuration file
├── .gitignore               # Git ignore patterns
├── .env.example             # Environment variables template
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

- `src/main.py`: Contains `Graph` and `DFS` classes with both implementations
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `docs/API.md`: API documentation for the DFS implementation
- `logs/`: Directory for application log files

## Algorithm Details

### Depth-First Search

DFS is a graph traversal algorithm that explores as far as possible along each branch before backtracking.

**Key Characteristics:**
- Explores depth-first (goes deep before going wide)
- Uses stack (implicit in recursion, explicit in iteration)
- Visits all vertices in connected component
- Can be used for path finding

### Recursive DFS

Uses function call stack for backtracking.

**Algorithm Steps:**
```
1. Mark current vertex as visited
2. Process/visit current vertex
3. For each unvisited neighbor:
   - Recursively call DFS on neighbor
4. Backtrack when function returns
```

**Example Traversal:**
```
Graph: 0 -> 1, 0 -> 2, 1 -> 3
Start: 0

DFS(0):
  Visit 0
  DFS(1):
    Visit 1
    DFS(3):
      Visit 3
      (no neighbors, backtrack)
    (backtrack)
  DFS(2):
    Visit 2
    (no neighbors, backtrack)
  (backtrack)

Path: [0, 1, 3, 2]
```

**Advantages:**
- Natural, intuitive implementation
- Less code
- Easy to understand

**Disadvantages:**
- Stack overflow risk for deep graphs
- Less control over stack
- Function call overhead

### Iterative DFS

Uses explicit stack data structure.

**Algorithm Steps:**
```
1. Push start vertex onto stack
2. While stack is not empty:
   - Pop vertex from stack
   - If not visited:
     - Mark as visited
     - Process/visit vertex
     - Push all unvisited neighbors onto stack
```

**Example Traversal:**
```
Graph: 0 -> 1, 0 -> 2, 1 -> 3
Start: 0

Stack: [0]
Pop 0, visit 0, push [2, 1]
Stack: [2, 1]
Pop 1, visit 1, push [3]
Stack: [2, 3]
Pop 3, visit 3
Stack: [2]
Pop 2, visit 2

Path: [0, 1, 3, 2]
```

**Advantages:**
- No stack overflow risk
- More control over traversal
- Can handle very deep graphs
- Better for iterative processing

**Disadvantages:**
- More code
- Explicit stack management
- Slightly more complex

### Time Complexity

- **Time Complexity:** O(V + E) where:
  - V = number of vertices
  - E = number of edges
  - Each vertex visited once
  - Each edge examined once

### Space Complexity

- **Recursive:** O(V) for recursion stack
- **Iterative:** O(V) for explicit stack
- Both have same space complexity in worst case

### Graph Representation

**Adjacency List:**
- Each vertex has list of neighbors
- Space efficient: O(V + E)
- Fast neighbor lookup: O(degree of vertex)

**Example:**
```
Graph: 0 -> 1, 0 -> 2, 1 -> 3
Adjacency List:
  0: [1, 2]
  1: [3]
  2: []
  3: []
```

## Applications

### Path Finding

- Find path between two vertices
- Check connectivity
- Maze solving

### Cycle Detection

- Detect cycles in graphs
- Check for back edges
- Topological sorting (DAG detection)

### Connected Components

- Find all connected components
- Check graph connectivity
- Network analysis

### Other Applications

- Topological sorting
- Strongly connected components
- Tree/graph traversal
- Puzzle solving (e.g., Sudoku)
- Web crawling
- Dependency resolution

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
- Graph operations (add edge, add vertex, get neighbors)
- Recursive DFS traversal
- Iterative DFS traversal
- Path finding
- Connected component detection
- Method comparison
- Edge cases (empty graph, single vertex, disconnected graph)
- Directed and undirected graphs

## Troubleshooting

### Common Issues

**ValueError: Start vertex not in graph:**
- Starting vertex doesn't exist in graph
- Check vertex exists before traversal
- Use graph.get_vertices() to see available vertices

**Stack Overflow (Recursive):**
- Graph is too deep for recursion
- Use iterative method instead
- Increase recursion limit (not recommended)

**Import Errors:**
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (requires 3.8+)
- Verify virtual environment is activated

### Error Messages

**"Start vertex not in graph"**: Starting vertex doesn't exist. Check vertex exists in graph.

**"Configuration file not found"**: Config file doesn't exist at specified path. Check file path or create config.yaml.

### Best Practices

1. **Use recursive** for simplicity and readability
2. **Use iterative** for deep graphs or when avoiding recursion
3. **Compare methods** to see performance differences: `--method both`
4. **Use visualization** to understand graph: `--visualize`
5. **Generate reports** for documentation: `--report report.txt`
6. **Use demonstration mode** to see examples: `--demo`

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
