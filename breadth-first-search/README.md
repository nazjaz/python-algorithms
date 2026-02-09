# Breadth-First Search (BFS) Algorithm

A Python implementation of the breadth-first search algorithm for finding shortest paths in unweighted graphs. BFS explores all vertices at the current depth level before moving to the next level, making it ideal for shortest path finding and level-order traversal.

## Project Title and Description

The Breadth-First Search implementation provides complete BFS algorithm for traversing graphs and finding shortest paths in unweighted graphs. It demonstrates how BFS guarantees shortest paths by exploring vertices level by level, ensuring the first path found is always the shortest.

This tool solves the problem of finding shortest paths in unweighted graphs, which is fundamental to many applications including network routing, social network analysis, puzzle solving, and graph traversal problems.

**Target Audience**: Students learning graph algorithms, developers studying shortest path algorithms, educators teaching BFS, and anyone interested in understanding graph traversal and path finding.

## Features

- Graph data structure with adjacency list representation
- BFS traversal implementation
- Shortest path finding in unweighted graphs
- Shortest distances to all reachable vertices
- Level-order traversal (vertices grouped by distance)
- Connected component detection
- Graph visualization
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
cd /path/to/python-algorithms/breadth-first-search
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

### With Graph Visualization

Show graph structure:

```bash
python src/main.py --demo --visualize
```

### Find Shortest Path

Find shortest path between vertices:

```bash
python src/main.py --demo --target 7
```

### Show Shortest Distances

Show shortest distances to all vertices:

```bash
python src/main.py --demo --distances
```

### Level-Order Traversal

Show vertices grouped by level:

```bash
python src/main.py --demo --levels
```

### Find Connected Components

Find all connected components:

```bash
python src/main.py --demo --components
```

### Generate Report

Generate detailed analysis report:

```bash
python src/main.py --demo --target 7 --report report.txt
```

### Command-Line Arguments

- `-c, --config`: Path to configuration file (default: config.yaml)
- `-s, --start`: Starting vertex for BFS
- `-t, --target`: Target vertex for shortest path finding
- `--distances`: Show shortest distances to all vertices
- `--levels`: Show level-order traversal
- `--components`: Find all connected components
- `-v, --visualize`: Show graph visualization
- `-r, --report`: Output path for analysis report
- `--demo`: Run demonstration with example graphs

### Common Use Cases

**Learn BFS Algorithm:**
1. Run: `python src/main.py --demo`
2. Review traversal order
3. Understand level-by-level exploration

**Find Shortest Path:**
1. Run: `python src/main.py --demo --target 7`
2. Review shortest path
3. Understand path reconstruction

**Study Level Structure:**
1. Run: `python src/main.py --demo --levels`
2. Review vertices by level
3. Understand distance from start

**Analyze Graph:**
1. Run: `python src/main.py --demo --visualize --distances`
2. Review graph structure
3. Review shortest distances

## Project Structure

```
breadth-first-search/
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

- `src/main.py`: Contains `Graph` and `BFS` classes with shortest path finding
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `docs/API.md`: API documentation for the BFS implementation
- `logs/`: Directory for application log files

## Algorithm Details

### Breadth-First Search

BFS is a graph traversal algorithm that explores all vertices at the current depth level before moving to the next level.

**Key Characteristics:**
- Explores breadth-first (level by level)
- Uses queue data structure (FIFO)
- Guarantees shortest path in unweighted graphs
- Visits all vertices in connected component

### BFS Algorithm

**Algorithm Steps:**
```
1. Initialize queue with start vertex
2. Mark start as visited
3. While queue is not empty:
   a. Dequeue vertex
   b. Process/visit vertex
   c. Enqueue all unvisited neighbors
   d. Mark neighbors as visited
4. Continue until queue is empty
```

**Example Traversal:**
```
Graph: 0 -> 1, 0 -> 2, 1 -> 3, 2 -> 4
Start: 0

Queue: [0]
Dequeue 0, visit 0, enqueue [1, 2]
Queue: [1, 2]
Dequeue 1, visit 1, enqueue [3]
Queue: [2, 3]
Dequeue 2, visit 2, enqueue [4]
Queue: [3, 4]
Dequeue 3, visit 3
Queue: [4]
Dequeue 4, visit 4
Queue: []

Traversal: [0, 1, 2, 3, 4]
Levels: [[0], [1, 2], [3, 4]]
```

### Shortest Path Finding

BFS guarantees shortest path in unweighted graphs because it explores vertices level by level, ensuring the first path found is the shortest.

**Algorithm Steps:**
```
1. Use BFS to explore graph level by level
2. Track parent of each vertex
3. Track distance from start
4. When target is found, backtrack using parents
5. First path found is guaranteed to be shortest
```

**Example Path Finding:**
```
Graph: 0 -> 1, 0 -> 2, 1 -> 3, 2 -> 3
Find path from 0 to 3

Level 0: 0 (distance 0, parent None)
Level 1: 1 (distance 1, parent 0), 2 (distance 1, parent 0)
Level 2: 3 (distance 2, parent 1 or 2)

Path: [0, 1, 3] or [0, 2, 3] (both distance 2)
```

### Time Complexity

- **Time Complexity:** O(V + E) where:
  - V = number of vertices
  - E = number of edges
  - Each vertex visited once
  - Each edge examined once

### Space Complexity

- **Space Complexity:** O(V) for:
  - Queue: O(V) in worst case
  - Visited set: O(V)
  - Distance/parent dictionaries: O(V)

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

### Why BFS Guarantees Shortest Path

1. **Level-by-level exploration**: BFS explores all vertices at distance d before exploring vertices at distance d+1
2. **First discovery**: The first time a vertex is discovered, it's at the minimum distance
3. **No shorter path**: Since all shorter paths are explored first, the first path found is shortest

## Applications

### Shortest Path Finding

- Find shortest path in unweighted graphs
- Network routing (hop count)
- Social network analysis (degrees of separation)
- GPS navigation (unweighted roads)

### Level-Order Traversal

- Tree level-order traversal
- Hierarchical data processing
- Distance-based analysis

### Other Applications

- Web crawling
- Puzzle solving (minimum moves)
- Connected component detection
- Cycle detection in undirected graphs
- Bipartite graph checking
- Minimum spanning tree (unweighted)

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
- BFS traversal
- Shortest path finding
- Shortest distances
- Level-order traversal
- Connected component detection
- Edge cases (empty graph, single vertex, disconnected graph)
- Directed and undirected graphs
- Path guarantees (shortest path verification)

## Troubleshooting

### Common Issues

**ValueError: Start vertex not in graph:**
- Starting vertex doesn't exist in graph
- Check vertex exists before traversal
- Use graph.get_vertices() to see available vertices

**ValueError: Target vertex not in graph:**
- Target vertex doesn't exist in graph
- Check vertex exists before path finding
- Use graph.get_vertices() to see available vertices

**No path found:**
- Vertices are in different connected components
- Check graph connectivity
- Use --components to find all components

**Import Errors:**
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (requires 3.8+)
- Verify virtual environment is activated

### Error Messages

**"Start vertex not in graph"**: Starting vertex doesn't exist. Check vertex exists in graph.

**"Target vertex not in graph"**: Target vertex doesn't exist. Check vertex exists in graph.

**"Configuration file not found"**: Config file doesn't exist at specified path. Check file path or create config.yaml.

### Best Practices

1. **Use BFS for shortest paths** in unweighted graphs
2. **Use level-order traversal** to understand graph structure
3. **Use shortest distances** to analyze reachability
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
