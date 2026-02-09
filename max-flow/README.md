# Maximum Flow Algorithm Using Ford-Fulkerson Method

A Python implementation of maximum flow algorithms using Ford-Fulkerson method with Edmonds-Karp and Dinic's optimizations. This tool computes the maximum flow from source to sink in a directed graph with edge capacities.

## Project Title and Description

The Maximum Flow tool implements three algorithms for computing maximum flow in flow networks: Ford-Fulkerson (DFS-based), Edmonds-Karp (BFS-based), and Dinic's algorithm (layered network). These algorithms solve the problem of finding the maximum amount of flow that can be sent from a source vertex to a sink vertex in a directed graph with capacity constraints.

This tool solves the maximum flow problem, which has applications in network routing, bipartite matching, image segmentation, and resource allocation. The implementation provides three algorithms with different time complexities, allowing users to choose the most appropriate one for their use case.

**Target Audience**: Network engineers, algorithm students, competitive programmers, operations researchers, graph algorithm researchers, and anyone interested in understanding flow networks and maximum flow algorithms.

## Features

- Ford-Fulkerson algorithm (DFS-based path finding)
- Edmonds-Karp algorithm (BFS-based shortest path)
- Dinic's algorithm (layered network with blocking flow)
- Flow network representation with residual graphs
- Minimum cut computation
- Flow dictionary output
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
cd /path/to/python-algorithms/max-flow
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

### Basic Usage

Run the main script to see a demonstration of maximum flow algorithms:

```bash
python src/main.py
```

This will:
1. Create a flow network
2. Compute maximum flow using all three algorithms
3. Display results and flow distributions
4. Compute minimum cut

### Programmatic Usage

```python
from src.main import FlowNetwork, MaxFlowSolver

# Create flow network
network = FlowNetwork(6)

# Add edges with capacities
network.add_edge(0, 1, 16)
network.add_edge(0, 2, 13)
network.add_edge(1, 2, 10)
network.add_edge(1, 3, 12)
network.add_edge(2, 4, 14)
network.add_edge(3, 5, 20)
network.add_edge(4, 5, 4)

# Create solver
solver = MaxFlowSolver(network)

# Compute maximum flow using different algorithms
max_flow_ff, flow_dict_ff = solver.ford_fulkerson(0, 5)
max_flow_ek, flow_dict_ek = solver.edmonds_karp(0, 5)
max_flow_dinic, flow_dict_dinic = solver.dinic(0, 5)

# Find minimum cut
source_side, sink_side = solver.get_min_cut(0, 5)
```

### Common Use Cases

**Network Routing:**
1. Model network as flow graph
2. Set edge capacities to bandwidth
3. Compute maximum flow for routing

**Bipartite Matching:**
1. Convert matching problem to flow network
2. Add source connected to left partition
3. Add sink connected to right partition
4. Maximum flow equals maximum matching

**Resource Allocation:**
1. Model resources as flow network
2. Set capacities based on constraints
3. Compute maximum flowable resources

## Project Structure

```
max-flow/
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

- `src/main.py`: Contains `FlowNetwork` and `MaxFlowSolver` classes with all algorithms
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `logs/`: Directory for application log files

## Algorithm Details

### Maximum Flow Problem

**Definition:**
Given a directed graph with edge capacities, find the maximum amount of flow that can be sent from a source vertex to a sink vertex, respecting capacity constraints and flow conservation.

**Properties:**
1. Flow conservation: Incoming flow equals outgoing flow (except source/sink)
2. Capacity constraint: Flow on edge cannot exceed capacity
3. Maximum flow equals minimum cut (Max-Flow Min-Cut Theorem)

### Ford-Fulkerson Algorithm

**Overview:**
Basic algorithm that repeatedly finds augmenting paths using DFS and increases flow along them.

**Steps:**
1. Initialize flow to 0
2. While augmenting path exists:
   - Find path from source to sink using DFS
   - Find minimum residual capacity along path
   - Increase flow by that amount
   - Update residual graph
3. Return maximum flow

**Time Complexity:** O(E * max_flow) where E is edges
- Worst case: Exponential if capacities are large integers
- Best case: O(E) if optimal path found first

**Advantages:**
- Simple to understand and implement
- Works with any path-finding method

**Disadvantages:**
- Can be slow with large capacities
- No guarantee on number of iterations

### Edmonds-Karp Algorithm

**Overview:**
Optimization of Ford-Fulkerson that uses BFS to find shortest augmenting paths.

**Steps:**
1. Initialize flow to 0
2. While augmenting path exists:
   - Find shortest path from source to sink using BFS
   - Find minimum residual capacity along path
   - Increase flow by that amount
   - Update residual graph
3. Return maximum flow

**Time Complexity:** O(V * E^2) where V is vertices, E is edges
- Guaranteed polynomial time
- Always finds shortest augmenting path

**Advantages:**
- Polynomial time guarantee
- Simple BFS implementation
- Good for most practical cases

**Disadvantages:**
- Slower than Dinic's for dense graphs
- Still O(V * E^2) which can be slow

### Dinic's Algorithm

**Overview:**
Advanced algorithm using layered networks and blocking flows for efficiency.

**Steps:**
1. Initialize flow to 0
2. While sink is reachable:
   - Build layered network using BFS
   - While blocking flow exists:
     - Send blocking flow using DFS
     - Update residual graph
3. Return maximum flow

**Time Complexity:** O(V^2 * E)
- Faster than Edmonds-Karp for many cases
- Particularly efficient for dense graphs

**Advantages:**
- Best time complexity of the three
- Efficient for large graphs
- Uses layered network optimization

**Disadvantages:**
- More complex implementation
- Requires careful layered network construction

### Operations

**Add Edge:**
- Time Complexity: O(1)
- Add edge with capacity to network

**Compute Maximum Flow:**
- Time Complexity: Varies by algorithm
- Returns maximum flow value and flow distribution

**Find Minimum Cut:**
- Time Complexity: Same as flow computation
- Returns vertices on source side and sink side

### Edge Cases Handled

- Empty network
- Single edge network
- No path from source to sink
- Parallel edges
- Reverse edges
- Large networks
- Invalid vertices
- Negative capacities (rejected)

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
- Flow network creation and edge addition
- All three algorithms (Ford-Fulkerson, Edmonds-Karp, Dinic's)
- Maximum flow computation
- Minimum cut computation
- Edge cases (no path, single edge, parallel edges)
- Invalid input handling
- Flow dictionary structure

## Troubleshooting

### Common Issues

**Maximum flow is 0:**
- Check if path exists from source to sink
- Verify edge capacities are positive
- Ensure source and sink are different vertices

**Algorithm is slow:**
- Use Edmonds-Karp or Dinic's instead of Ford-Fulkerson
- Consider graph size and density
- Check for very large capacities

**Invalid flow results:**
- Verify all algorithms produce same result
- Check residual graph updates
- Validate flow conservation

### Error Messages

**"Network must have at least 2 vertices"**: Flow network requires at least source and sink vertices.

**"Invalid source/sink vertex"**: Source or sink index is out of bounds.

**"Source and sink must be different"**: Source and sink cannot be the same vertex.

**"Capacity must be non-negative"**: Edge capacities must be non-negative integers.

### Best Practices

1. **Choose appropriate algorithm** - Use Dinic's for large graphs, Edmonds-Karp for most cases
2. **Validate input** - Ensure network is properly constructed
3. **Check results** - All algorithms should produce same maximum flow
4. **Use minimum cut** - Verify max-flow equals min-cut value
5. **Monitor performance** - Consider graph size when choosing algorithm

## Performance Characteristics

### Time Complexity

| Algorithm | Time Complexity | Best For |
|-----------|----------------|----------|
| Ford-Fulkerson | O(E * max_flow) | Small graphs, educational |
| Edmonds-Karp | O(V * E^2) | General purpose |
| Dinic's | O(V^2 * E) | Large/dense graphs |

Where:
- V = number of vertices
- E = number of edges
- max_flow = maximum flow value

### Space Complexity

- Network storage: O(V + E)
- Residual graph: O(V + E)
- Auxiliary space: O(V) for algorithms
- Total: O(V + E)

## Applications

- **Network Routing**: Maximum bandwidth routing
- **Bipartite Matching**: Maximum matching in bipartite graphs
- **Image Segmentation**: Min-cut for image processing
- **Resource Allocation**: Optimal resource distribution
- **Supply Chain**: Maximum flow in supply networks
- **Sports Scheduling**: Tournament scheduling problems

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
