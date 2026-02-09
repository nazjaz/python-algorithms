# Dijkstra's Algorithm

A Python implementation of Dijkstra's algorithm for finding shortest paths in weighted graphs. The algorithm uses a priority queue (min-heap) for efficient vertex selection, ensuring optimal performance for finding shortest paths from a source vertex to all other vertices.

## Project Title and Description

The Dijkstra's algorithm implementation provides complete shortest path finding in weighted graphs using a priority queue optimization. It demonstrates how Dijkstra's greedy algorithm guarantees optimal shortest paths when all edge weights are non-negative, making it ideal for applications like GPS navigation, network routing, and pathfinding.

This tool solves the problem of finding shortest paths in weighted graphs, which is fundamental to many real-world applications including route planning, network optimization, and resource allocation.

**Target Audience**: Students learning graph algorithms, developers studying shortest path algorithms, educators teaching Dijkstra's algorithm, and anyone interested in understanding weighted graph traversal and optimization.

## Features

- Weighted graph data structure with adjacency list representation
- Dijkstra's algorithm implementation with priority queue (heapq)
- Shortest path finding between two vertices
- Shortest distances to all reachable vertices
- All shortest paths from source vertex
- Path reconstruction using parent tracking
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
cd /path/to/python-algorithms/dijkstra-algorithm
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
python src/main.py --demo --target 3
```

### Show Shortest Distances

Show shortest distances to all vertices:

```bash
python src/main.py --demo --distances
```

### Show All Shortest Paths

Show shortest paths to all vertices:

```bash
python src/main.py --demo --paths
```

### Generate Report

Generate detailed analysis report:

```bash
python src/main.py --demo --target 3 --report report.txt
```

### Command-Line Arguments

- `-c, --config`: Path to configuration file (default: config.yaml)
- `-s, --start`: Starting vertex for Dijkstra's algorithm
- `-t, --target`: Target vertex for shortest path finding
- `--distances`: Show shortest distances to all vertices
- `--paths`: Show shortest paths to all vertices
- `-v, --visualize`: Show graph visualization
- `-r, --report`: Output path for analysis report
- `--demo`: Run demonstration with example graphs

### Common Use Cases

**Learn Dijkstra's Algorithm:**
1. Run: `python src/main.py --demo`
2. Review shortest paths
3. Understand greedy selection

**Find Shortest Path:**
1. Run: `python src/main.py --demo --target 3`
2. Review shortest path
3. Understand path reconstruction

**Analyze Graph:**
1. Run: `python src/main.py --demo --visualize --distances`
2. Review graph structure
3. Review shortest distances

**Study All Paths:**
1. Run: `python src/main.py --demo --paths`
2. Review all shortest paths
3. Understand single-source shortest paths

## Project Structure

```
dijkstra-algorithm/
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

- `src/main.py`: Contains `WeightedGraph` and `Dijkstra` classes with priority queue implementation
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `docs/API.md`: API documentation for the Dijkstra implementation
- `logs/`: Directory for application log files

## Algorithm Details

### Dijkstra's Algorithm

Dijkstra's algorithm is a greedy algorithm for finding shortest paths in weighted graphs with non-negative edge weights.

**Key Characteristics:**
- Greedy algorithm (makes locally optimal choice)
- Uses priority queue for efficient vertex selection
- Guarantees shortest path when all weights are non-negative
- Finds shortest paths from single source to all vertices

### Algorithm Steps

```
1. Initialize distance to start as 0, all others as infinity
2. Add start vertex to priority queue
3. While queue is not empty:
   a. Extract vertex with minimum distance (u)
   b. Mark u as visited
   c. For each unvisited neighbor v of u:
      - Calculate new distance = distance[u] + weight(u, v)
      - If new distance < distance[v]:
        * Update distance[v] = new distance
        * Set parent[v] = u
        * Add (distance[v], v) to priority queue
4. Reconstruct path using parent pointers
```

### Example Execution

```
Graph: 0 -> 1 (w:4), 0 -> 2 (w:1), 1 -> 3 (w:1), 2 -> 3 (w:5)
Find shortest path from 0 to 3

Initial: distance[0] = 0, others = infinity
Queue: [(0, 0)]

Extract 0 (distance 0):
  Update 1: distance = 0 + 4 = 4
  Update 2: distance = 0 + 1 = 1
  Queue: [(1, 2), (4, 1)]

Extract 2 (distance 1):
  Update 3: distance = 1 + 5 = 6
  Queue: [(4, 1), (6, 3)]

Extract 1 (distance 4):
  Update 3: distance = 4 + 1 = 5 (better than 6)
  Queue: [(5, 3)]

Extract 3 (distance 5):
  Target reached!

Path: [0, 1, 3] with distance 5
```

### Priority Queue Optimization

**Why Priority Queue?**
- Without priority queue: O(V²) time complexity
- With priority queue (heap): O((V + E) log V) time complexity
- Always processes vertex with minimum distance first
- Ensures optimal greedy selection

**Implementation:**
- Uses Python's `heapq` module (min-heap)
- Operations: O(log n) for insert/extract
- More efficient than checking all vertices each iteration

### Time Complexity

- **Time Complexity:** O((V + E) log V) where:
  - V = number of vertices
  - E = number of edges
  - log V factor from priority queue operations

### Space Complexity

- **Space Complexity:** O(V) for:
  - Distance dictionary: O(V)
  - Parent dictionary: O(V)
  - Priority queue: O(V) in worst case
  - Visited set: O(V)

### Graph Representation

**Weighted Adjacency List:**
- Each vertex has list of (neighbor, weight) tuples
- Space efficient: O(V + E)
- Fast neighbor lookup: O(degree of vertex)

**Example:**
```
Graph: 0 -> 1 (w:4), 0 -> 2 (w:1), 1 -> 3 (w:1)
Adjacency List:
  0: [(1, 4.0), (2, 1.0)]
  1: [(3, 1.0)]
  2: []
  3: []
```

### Why Non-Negative Weights?

Dijkstra's algorithm requires non-negative edge weights because:
1. **Greedy assumption**: Once a vertex is processed, its distance is final
2. **Negative weights break this**: A shorter path might be found later
3. **Alternative**: Use Bellman-Ford algorithm for graphs with negative weights

## Applications

### GPS Navigation

- Find shortest route between locations
- Consider road distances/weights
- Real-time route planning

### Network Routing

- Internet routing protocols
- Packet routing optimization
- Network topology analysis

### Other Applications

- Social network analysis (weighted connections)
- Game pathfinding (terrain costs)
- Resource allocation
- Transportation planning
- Map applications
- Supply chain optimization

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
- Shortest path finding
- Shortest distances
- All shortest paths from source
- Priority queue optimization
- Edge cases (empty graph, single vertex, disconnected graph)
- Directed and undirected graphs
- Path optimality verification

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

**Negative weights warning:**
- Dijkstra's algorithm requires non-negative weights
- Algorithm may not find optimal path with negative weights
- Use Bellman-Ford algorithm for negative weights

**Import Errors:**
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (requires 3.8+)
- Verify virtual environment is activated

### Error Messages

**"Start vertex not in graph"**: Starting vertex doesn't exist. Check vertex exists in graph.

**"Target vertex not in graph"**: Target vertex doesn't exist. Check vertex exists in graph.

**"Configuration file not found"**: Config file doesn't exist at specified path. Check file path or create config.yaml.

### Best Practices

1. **Use Dijkstra for non-negative weights** only
2. **Use priority queue** for efficient implementation
3. **Verify path optimality** by checking distances
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
