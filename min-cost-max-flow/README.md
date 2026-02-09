# Min-Cost Max-Flow Algorithm using Successive Shortest Paths and Cycle Canceling

A Python implementation of min-cost max-flow algorithms using two different approaches: successive shortest paths and cycle canceling. These algorithms find the maximum flow with minimum cost in a flow network with edge capacities and costs.

## Project Title and Description

The Min-Cost Max-Flow tool implements algorithms to solve the minimum cost maximum flow problem in a flow network. Given a directed graph with edge capacities and costs, the algorithms find the maximum flow from source to sink while minimizing the total cost.

This tool solves the problem of efficiently finding maximum flow with minimum cost, which is fundamental in many applications including network optimization, resource allocation, transportation problems, and supply chain management. The implementation provides two algorithms: successive shortest paths (using Dijkstra with potentials) and cycle canceling (using Bellman-Ford).

**Target Audience**: Algorithm students, competitive programmers, data structure researchers, software engineers, and anyone interested in understanding network flow algorithms and optimization.

## Features

- Min-cost max-flow implementation with two algorithms
- Successive shortest paths algorithm (Dijkstra with potentials)
- Cycle canceling algorithm (Bellman-Ford)
- O(V^2 E) time complexity for cycle canceling
- O(V E log V) time complexity for successive shortest paths
- Flow network representation with residual graphs
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
cd /path/to/python-algorithms/min-cost-max-flow
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
- `logging.file`: Path to log file (default: "logs/min_cost_max_flow.log")

### Example Configuration

```yaml
logging:
  level: "INFO"
  file: "logs/min_cost_max_flow.log"
```

### Environment Variables

No environment variables are currently required. All configuration is managed through the `config.yaml` file.

## Usage

### Basic Usage

Run the main script to see a demonstration of min-cost max-flow algorithms:

```bash
python src/main.py
```

This will:
1. Create a flow network
2. Run successive shortest paths algorithm
3. Run cycle canceling algorithm
4. Display results

### Programmatic Usage

```python
from src.main import FlowNetwork, MinCostMaxFlow

# Create flow network
network = FlowNetwork(4)
network.add_edge(0, 1, 10.0, 1.0)  # from, to, capacity, cost
network.add_edge(0, 2, 5.0, 2.0)
network.add_edge(1, 2, 15.0, 1.0)
network.add_edge(1, 3, 10.0, 3.0)
network.add_edge(2, 3, 10.0, 1.0)

# Successive shortest paths
solver = MinCostMaxFlow(network)
flow, cost = solver.successive_shortest_paths(0, 3)
print(f"Max Flow: {flow}, Min Cost: {cost}")

# Cycle canceling
solver2 = MinCostMaxFlow(network)
flow2, cost2 = solver2.cycle_canceling(0, 3)
print(f"Max Flow: {flow2}, Min Cost: {cost2}")
```

### Common Use Cases

**Network Optimization:**
1. Transportation problems
2. Resource allocation
3. Network routing

**Competitive Programming:**
1. Min-cost flow problems
2. Network flow optimization
3. Graph algorithms

**Operations Research:**
1. Supply chain optimization
2. Assignment problems
3. Flow optimization

## Project Structure

```
min-cost-max-flow/
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

- `src/main.py`: Contains `FlowNetwork`, `Edge`, and `MinCostMaxFlow` classes
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `logs/`: Directory for application log files

## Algorithm Details

### Min-Cost Max-Flow Problem

**Definition:**
Given a directed graph with edge capacities and costs, find the maximum flow from source to sink that minimizes the total cost.

**Properties:**
1. Each edge has capacity and cost
2. Flow must satisfy capacity constraints
3. Flow must satisfy conservation constraints
4. Goal: maximize flow, minimize cost

### Successive Shortest Paths

**Algorithm:**
1. Initialize potentials using Bellman-Ford
2. While augmenting path exists:
   - Find shortest path using Dijkstra with reduced costs
   - Update potentials
   - Augment flow along path
3. Return max flow and min cost

**Time Complexity:** O(V E log V) with Dijkstra

**Advantages:**
- Faster for sparse graphs
- Uses potentials for efficiency
- Good for non-negative costs

### Cycle Canceling

**Algorithm:**
1. Find max flow using Bellman-Ford
2. While negative cycle exists:
   - Find negative cycle
   - Cancel cycle by augmenting flow
3. Return max flow and min cost

**Time Complexity:** O(V^2 E)

**Advantages:**
- Handles negative costs
- Simpler implementation
- Good for dense graphs

### Operations

**Add Edge:**
- Creates forward and backward edges
- Sets capacity and cost
- Initializes flow to zero

**Find Path:**
- Uses shortest path algorithm
- Finds path with minimum cost
- Returns path and flow amount

**Augment Path:**
- Increases flow along path
- Updates residual capacities
- Maintains flow conservation

### Edge Cases Handled

- Empty networks
- Single edge networks
- Networks with no path
- Negative cost edges
- Multiple paths
- Cycles in network

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
- Edge creation and operations
- FlowNetwork creation and operations
- Successive shortest paths algorithm
- Cycle canceling algorithm
- Flow retrieval
- Edge cases (empty, single edge, invalid inputs)
- Multiple network configurations

## Troubleshooting

### Common Issues

**Incorrect flow/cost results:**
- Verify network structure is correct
- Check that capacities and costs are valid
- Ensure source and sink are correct

**Performance issues:**
- Successive shortest paths is faster for sparse graphs
- Cycle canceling may be faster for dense graphs
- Consider graph structure when choosing algorithm

**Memory issues:**
- Flow networks use O(V + E) space
- For very large networks, consider optimizations
- Monitor memory usage

### Error Messages

**"Index out of bounds"**: Invalid vertex index.

**"No path found"**: No path from source to sink.

### Best Practices

1. **Choose appropriate algorithm** - Successive shortest paths for sparse graphs
2. **Validate network** - Ensure network is valid before solving
3. **Monitor performance** - Track algorithm times for your network
4. **Check results** - Verify flow conservation and capacity constraints
5. **Consider alternatives** - For simple cases, other algorithms may be better

## Performance Characteristics

### Time Complexity

| Algorithm | Time Complexity |
|-----------|----------------|
| Successive Shortest Paths | O(V E log V) |
| Cycle Canceling | O(V^2 E) |

Where V is number of vertices and E is number of edges.

### Space Complexity

- Network storage: O(V + E)
- Algorithm overhead: O(V)
- Total: O(V + E)

### Query Performance

- Successive shortest paths: O(V E log V) - faster for sparse graphs
- Cycle canceling: O(V^2 E) - handles negative costs
- Optimal for network flow optimization

## Applications

- **Network Optimization**: Transportation and routing problems
- **Resource Allocation**: Optimal resource distribution
- **Competitive Programming**: Min-cost flow problems
- **Operations Research**: Supply chain and assignment problems
- **Graph Algorithms**: Network flow optimization

## Comparison with Other Methods

**Successive Shortest Paths:**
- O(V E log V) time
- Faster for sparse graphs
- Requires non-negative reduced costs
- Uses Dijkstra with potentials

**Cycle Canceling:**
- O(V^2 E) time
- Handles negative costs
- Simpler implementation
- Uses Bellman-Ford

**Push-Relabel:**
- O(V^2 E) time
- Different approach
- Good for max flow
- Less efficient for min-cost

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
