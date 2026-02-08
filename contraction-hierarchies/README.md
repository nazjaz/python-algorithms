# Contraction Hierarchies for Fast Shortest Path Queries

A Python implementation of Contraction Hierarchies (CH) for fast shortest path queries in road networks. This tool provides preprocessing and query algorithms that enable sub-millisecond path queries on large road networks.

## Project Title and Description

The Contraction Hierarchies tool implements a state-of-the-art speedup technique for shortest path queries in road networks. It preprocesses the graph by contracting nodes in order of importance and adding shortcuts, then uses bidirectional Dijkstra on the contracted graph for fast queries.

This tool solves the problem of performing many shortest path queries on large road networks efficiently. It offers significant speedup over standard Dijkstra by preprocessing the graph once, enabling fast queries that are orders of magnitude faster than standard algorithms.

**Target Audience**: Routing system developers, transportation engineers, researchers working with road networks, students learning advanced graph algorithms, and developers implementing high-performance routing solutions.

## Features

- Preprocessing phase with node contraction
- Importance-based node ordering
- Automatic shortcut addition during contraction
- Fast query algorithm using bidirectional Dijkstra on contracted graph
- Support for weighted directed graphs
- Comprehensive logging and performance tracking
- Configurable algorithm parameters via YAML
- Detailed preprocessing statistics
- Optimal path guarantees

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

### Step 1: Navigate to Project Directory

```bash
cd /path/to/python-algorithms/contraction-hierarchies
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
python src/main.py --test
```

## Configuration

### Configuration File Structure

The algorithm is configured via `config.yaml`:

```yaml
contraction_hierarchies:
  edge_difference_weight: 1.0
  deleted_neighbors_weight: 1.0
  hop_limit: 2

logging:
  level: "INFO"
  file: "logs/app.log"
```

### Algorithm Overview

Contraction Hierarchies works in two phases:

1. **Preprocessing**:
   - Order nodes by importance
   - Contract nodes one by one (least important first)
   - Add shortcuts to preserve shortest paths
   - Build hierarchical structure

2. **Query**:
   - Run bidirectional Dijkstra on contracted graph
   - Only follow edges to higher-level nodes
   - Reconstruct optimal path

### Performance Benefits

- Preprocessing: O(V log V) time, adds shortcuts
- Query: Sub-millisecond on large networks
- Space: O(V + E + shortcuts)
- Speedup: 100-1000x faster than standard Dijkstra

## Usage

### Basic Usage

```python
from src.main import ContractionHierarchies, RoadGraph

# Create road network
edges = [
    (0, 1, 1.0),
    (1, 2, 2.0),
    (2, 3, 1.0),
    (0, 2, 4.0),
    (1, 3, 5.0),
]

graph = RoadGraph(edges=edges, num_nodes=4)

# Preprocess
ch = ContractionHierarchies()
stats = ch.preprocess(graph)
print(f"Shortcuts added: {stats['shortcuts_added']}")

# Query
result = ch.query(graph, 0, 3)
if result['found']:
    print(f"Path: {result['path']}")
    print(f"Cost: {result['cost']}")
```

### Command-Line Usage

Run with test problem:

```bash
python src/main.py --test
```

Specify custom configuration:

```bash
python src/main.py --config custom_config.yaml
```

### Advanced Example: Large Network

```python
from src.main import ContractionHierarchies, RoadGraph
import random

# Generate random road network
num_nodes = 1000
edges = []
for i in range(num_nodes):
    for j in range(i + 1, min(i + 5, num_nodes)):
        weight = random.uniform(1.0, 10.0)
        edges.append((i, j, weight))
        edges.append((j, i, weight))

graph = RoadGraph(edges=edges, num_nodes=num_nodes)

# Preprocess once
ch = ContractionHierarchies()
stats = ch.preprocess(graph)
print(f"Preprocessing complete: {stats['shortcuts_added']} shortcuts")

# Fast queries
for _ in range(10):
    start = random.randint(0, num_nodes - 1)
    goal = random.randint(0, num_nodes - 1)
    result = ch.query(graph, start, goal)
    print(f"Query {start}->{goal}: {result['nodes_explored']} nodes explored")
```

### Real-World Road Network

```python
from src.main import ContractionHierarchies, RoadGraph

# Load road network from file or database
# Format: source, target, weight
edges = load_road_network("roads.txt")

graph = RoadGraph(edges=edges, num_nodes=num_nodes)

# Preprocess (do once)
ch = ContractionHierarchies()
ch.preprocess(graph)

# Fast queries (can do many)
result = ch.query(graph, start_node, goal_node)
```

## Project Structure

```
contraction-hierarchies/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── config.yaml              # Configuration file
├── .gitignore               # Git ignore rules
├── src/
│   └── main.py              # Main implementation
├── tests/
│   └── test_main.py         # Unit tests
├── docs/
│   └── API.md               # API documentation
└── logs/
    └── .gitkeep             # Log directory
```

### File Descriptions

- `src/main.py`: Core implementation containing `ContractionHierarchies` and `RoadGraph` classes
- `config.yaml`: Configuration file for algorithm parameters
- `tests/test_main.py`: Comprehensive unit tests
- `docs/API.md`: Detailed API documentation
- `logs/`: Directory for application logs

## Testing

### Run All Tests

```bash
pytest tests/
```

### Run with Coverage

```bash
pytest tests/ --cov=src --cov-report=html
```

### Test Structure

Tests cover:
- Graph creation and edge operations
- Node importance calculation
- Shortcut finding and addition
- Node contraction
- Preprocessing phase
- Query algorithm
- Edge cases and error handling
- Configuration loading and validation

## Troubleshooting

### Common Issues

**Issue**: `ValueError: Graph must be preprocessed before querying`

**Solution**: Call `preprocess()` before making queries

**Issue**: Preprocessing is slow

**Solution**: 
- This is expected for large networks
- Preprocessing is done once, queries are fast
- Consider using parallel processing for very large networks

**Issue**: Too many shortcuts added

**Solution**:
- Adjust `edge_difference_weight` in config
- Adjust `deleted_neighbors_weight` in config
- Use more sophisticated node ordering

**Issue**: Query returns no path

**Solution**:
- Check if nodes are connected in original graph
- Verify graph connectivity
- Check for disconnected components

### Error Messages

- `FileNotFoundError`: Configuration file missing - check file path
- `ValueError`: Invalid node or graph not preprocessed
- `yaml.YAMLError`: Invalid YAML syntax - validate config file

## Algorithm Details

### Contraction Hierarchies Overview

Contraction Hierarchies is a preprocessing technique that:
1. Assigns levels to nodes (importance)
2. Contracts nodes in order (least important first)
3. Adds shortcuts to preserve shortest paths
4. Uses hierarchical structure for fast queries

### Node Ordering

Nodes are ordered by importance:
- Edge difference: How many edges would be added/removed
- Deleted neighbors: How many neighbors already contracted
- Lower importance = contract earlier

### Shortcut Addition

When contracting a node:
- For each incoming edge (u, v) and outgoing edge (v, w)
- If shortest path u->w goes through v, add shortcut (u, w)
- Shortcut weight = weight(u, v) + weight(v, w)

### Query Algorithm

Bidirectional Dijkstra on contracted graph:
- Forward search: Only follow edges to higher-level nodes
- Backward search: Only follow edges to higher-level nodes
- Meet in the middle for optimal path

### Time Complexity

- Preprocessing: O(V² log V) worst case (simplified version)
- Query: O((V + E) log V) worst case, much faster in practice
- Space: O(V + E + shortcuts)

## Performance Considerations

- Preprocessing time increases with graph size
- More shortcuts = faster queries but more memory
- Node ordering significantly affects performance
- For very large networks, consider:
  - Parallel preprocessing
  - More sophisticated node ordering
  - Hierarchical CH (multi-level)
  - Custom importance metrics

## Real-World Applications

- GPS navigation systems
- Route planning services
- Logistics and delivery optimization
- Traffic analysis
- Network routing
- Game pathfinding for large maps

## Contributing

### Development Setup

1. Clone the repository
2. Create virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Install development dependencies: `pip install pytest pytest-cov`
5. Run tests: `pytest tests/`

### Code Style Guidelines

- Follow PEP 8 strictly
- Maximum line length: 88 characters
- Use type hints for all functions
- Include docstrings for all public functions and classes
- Write tests for all new functionality

### Pull Request Process

1. Create feature branch
2. Implement changes with tests
3. Ensure all tests pass
4. Update documentation if needed
5. Submit pull request with clear description

## References

- Geisberger, R., Sanders, P., Schultes, D., & Delling, D. (2008). Contraction hierarchies: Faster and simpler hierarchical routing in road networks.
- Used in production routing systems like OSRM, GraphHopper, and PTV

## License

This project is part of the python-algorithms collection. See LICENSE file in parent directory for details.
