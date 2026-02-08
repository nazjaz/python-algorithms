# Bidirectional Dijkstra Algorithm for Shortest Path Finding

A Python implementation of bidirectional Dijkstra's algorithm for finding shortest paths with forward and backward searches. This tool provides optimal pathfinding with reduced search space compared to standard unidirectional Dijkstra.

## Project Title and Description

The Bidirectional Dijkstra tool implements a variant of Dijkstra's algorithm that runs two searches simultaneously - one from the start node and one from the goal node. The searches meet in the middle, significantly reducing the search space and improving performance for large graphs.

This tool solves the problem of finding shortest paths in weighted graphs with improved efficiency. It offers the same optimality guarantees as standard Dijkstra while exploring fewer nodes, making it ideal for large-scale pathfinding problems, network routing, and graph analysis.

**Target Audience**: Network engineers implementing routing algorithms, game developers working with large maps, researchers analyzing graph structures, students learning shortest path algorithms, and developers implementing efficient pathfinding solutions.

## Features

- Bidirectional search with forward and backward exploration
- Support for weighted graphs via adjacency lists
- Support for grid-based graphs with obstacles
- Configurable movement costs for grid graphs
- Meeting point detection and optimal path reconstruction
- Comprehensive logging and performance tracking
- Configurable algorithm parameters via YAML
- Detailed performance metrics (nodes explored in each direction)
- Support for 4-directional and 8-directional movement in grids
- Optimal path guarantees

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

### Step 1: Navigate to Project Directory

```bash
cd /path/to/python-algorithms/bidirectional-dijkstra
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
bidirectional_dijkstra:
  max_iterations: 10000

logging:
  level: "INFO"
  file: "logs/app.log"
```

### Algorithm Overview

Bidirectional Dijkstra works by:
1. Running two Dijkstra searches simultaneously
2. Forward search from start node
3. Backward search from goal node
4. Detecting when searches meet (node visited by both)
5. Reconstructing optimal path through meeting point
6. Stopping when optimal path is guaranteed

### Performance Benefits

Compared to unidirectional Dijkstra:
- Explores approximately half the nodes
- Reduces search space from O(V) to O(V/2) in best case
- Faster convergence for long paths
- Same optimality guarantees

## Usage

### Basic Usage with Grid

```python
from src.main import BidirectionalDijkstra, Graph
import numpy as np

# Create grid (0 = walkable, 1 = obstacle)
grid = np.array([
    [0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
])

# Initialize
dijkstra = BidirectionalDijkstra(config_path="config.yaml")
graph = Graph(grid=grid, allow_diagonal=True)

# Find path
start = (0, 0)
goal = (4, 3)
result = dijkstra.search(graph, start, goal)

if result['found']:
    print(f"Path found: {result['path']}")
    print(f"Cost: {result['cost']}")
    print(f"Nodes explored (forward): {result['nodes_explored_forward']}")
    print(f"Nodes explored (backward): {result['nodes_explored_backward']}")
```

### Usage with Adjacency List

```python
from src.main import BidirectionalDijkstra, Graph

# Create graph from adjacency list
adjacency_list = {
    0: [(1, 4.0), (2, 1.0)],
    1: [(2, 2.0), (3, 5.0)],
    2: [(1, 2.0), (3, 8.0)],
    3: [(4, 3.0)],
    4: []
}

graph = Graph(adjacency_list=adjacency_list)
dijkstra = BidirectionalDijkstra()

result = dijkstra.search(graph, 0, 4)

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

### Advanced Example: Custom Movement Costs

```python
import numpy as np
from src.main import BidirectionalDijkstra, Graph

grid = np.zeros((10, 10))
graph = Graph(
    grid=grid,
    allow_diagonal=True,
    movement_cost={'straight': 1.0, 'diagonal': 1.5}
)

dijkstra = BidirectionalDijkstra()
result = dijkstra.search(graph, (0, 0), (9, 9))
```

### Large Graph Example

```python
import numpy as np
from src.main import BidirectionalDijkstra, Graph

# Large grid to demonstrate efficiency
grid = np.zeros((50, 50))
graph = Graph(grid=grid, allow_diagonal=True)

dijkstra = BidirectionalDijkstra()
result = dijkstra.search(graph, (0, 0), (49, 49))

print(f"Total nodes explored: {result['nodes_explored']}")
print(f"Forward: {result['nodes_explored_forward']}")
print(f"Backward: {result['nodes_explored_backward']}")
```

## Project Structure

```
bidirectional-dijkstra/
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

- `src/main.py`: Core implementation containing `BidirectionalDijkstra` and `Graph` classes
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
- Bidirectional search algorithm
- Forward and backward search
- Meeting point detection
- Path reconstruction
- Grid-based graphs
- Adjacency list graphs
- Edge cases and error handling
- Configuration loading and validation

## Troubleshooting

### Common Issues

**Issue**: `ValueError: Start node is not in graph`

**Solution**: Ensure start node exists in graph (for grids, must be walkable)

**Issue**: `ValueError: Goal node is not in graph`

**Solution**: Ensure goal node exists in graph (for grids, must be walkable)

**Issue**: No path found

**Solution**: 
- Check if path exists (nodes are connected)
- Verify graph connectivity
- Check for obstacles blocking all routes (for grids)

**Issue**: Algorithm is slow

**Solution**:
- Use bidirectional search (already implemented)
- Reduce graph size if possible
- Check for unnecessary edges
- Consider graph preprocessing

**Issue**: Path is suboptimal

**Solution**:
- Verify edge weights are non-negative
- Check for negative cycles (Dijkstra doesn't handle these)
- Ensure graph is properly connected

### Error Messages

- `FileNotFoundError`: Configuration file missing - check file path
- `ValueError`: Invalid node or graph structure
- `yaml.YAMLError`: Invalid YAML syntax - validate config file

## Bidirectional vs Unidirectional Dijkstra

### Search Space
- **Unidirectional**: Explores all nodes within distance d from start
- **Bidirectional**: Explores nodes within d/2 from both start and goal

### Time Complexity
- **Both**: O((V + E) log V) worst case
- **Bidirectional**: Often explores fewer nodes in practice

### Memory Usage
- **Both**: O(V) for distance and predecessor maps
- **Bidirectional**: Maintains two sets (forward and backward)

### When to Use Bidirectional
- Large graphs with long paths
- When start and goal are far apart
- Network routing problems
- When search space reduction is important

### When to Use Unidirectional
- Small graphs
- When start and goal are close
- Simple pathfinding problems
- When memory is extremely constrained

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

## Algorithm Details

### Bidirectional Dijkstra Overview

Bidirectional Dijkstra is a variant that:
1. Maintains two priority queues (forward and backward)
2. Alternates between forward and backward searches
3. Tracks distances from both directions
4. Detects when a node is visited by both searches
5. Reconstructs path through meeting point
6. Stops when optimal path is guaranteed

### Meeting Point Detection

The algorithm detects meeting when:
- A node is visited by both forward and backward searches
- Total cost = dist_forward[node] + dist_backward[node]
- This represents a candidate shortest path

### Stopping Condition

The algorithm can stop early when:
- Best meeting cost found
- Next nodes in both queues have distance >= best_cost / 2
- Guarantees optimality of found path

### Path Reconstruction

Path is reconstructed by:
1. Following predecessors from meeting node to start (forward)
2. Following predecessors from meeting node to goal (backward)
3. Combining both paths

## Performance Considerations

- Algorithm complexity: O((V + E) log V) worst case
- Memory usage: O(V) for distance and predecessor maps
- For large graphs, consider:
  - Using bidirectional search (already implemented)
  - Graph preprocessing and simplification
  - Hierarchical pathfinding for very large graphs
  - Caching frequently used paths

## License

This project is part of the python-algorithms collection. See LICENSE file in parent directory for details.
