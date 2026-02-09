# K-D Tree for Multidimensional Range Queries and Nearest Neighbor Search

A Python implementation of k-d tree (k-dimensional tree) data structure that efficiently stores points in k-dimensional space and supports range queries and nearest neighbor search. K-d trees achieve O(log n) average time complexity for queries.

## Project Title and Description

The K-D Tree tool implements a space-partitioning data structure for organizing points in a k-dimensional space. Each node in the tree represents a point and splits the space along alternating dimensions, enabling efficient range queries and nearest neighbor search.

This tool solves the problem of efficiently querying multidimensional data, which is fundamental in many applications including machine learning, computational geometry, and spatial databases. The k-d tree provides O(log n) average time complexity for insertion, deletion, and queries.

**Target Audience**: Algorithm students, competitive programmers, data structure researchers, software engineers, machine learning practitioners, and anyone interested in understanding multidimensional data structures and spatial algorithms.

## Features

- K-d tree implementation with dimension-based splitting
- O(log n) average time complexity for queries
- Efficient range queries for multidimensional hyperrectangles
- Nearest neighbor search with pruning optimization
- K-nearest neighbors search
- Support for arbitrary dimensions (2D, 3D, nD)
- Automatic tree building from point lists
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
cd /path/to/python-algorithms/kd-tree
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
- `logging.file`: Path to log file (default: "logs/kd_tree.log")

### Example Configuration

```yaml
logging:
  level: "INFO"
  file: "logs/kd_tree.log"
```

### Environment Variables

No environment variables are currently required. All configuration is managed through the `config.yaml` file.

## Usage

### Basic Usage

Run the main script to see a demonstration of k-d tree operations:

```bash
python src/main.py
```

This will:
1. Create a k-d tree from points
2. Perform range queries
3. Find nearest neighbors
4. Find k-nearest neighbors

### Programmatic Usage

```python
from src.main import KDTree

# Create k-d tree from points
points = [[2, 3], [5, 4], [9, 6], [4, 7], [8, 1], [7, 2]]
tree = KDTree(points)

# Range query
results = tree.range_query([3, 3], [7, 7])
for point in results:
    print(f"Point in range: {point}")

# Nearest neighbor
nearest = tree.nearest_neighbor([6, 5])
print(f"Nearest neighbor: {nearest}")

# K-nearest neighbors
k_nearest = tree.k_nearest_neighbors([6, 5], 3)
for point in k_nearest:
    print(f"Neighbor: {point}")

# Insert new point
tree.insert([10, 10])

# Get all points
all_points = tree.get_all_points()
```

### Common Use Cases

**Machine Learning:**
1. Store training data points
2. Find nearest neighbors for k-NN classification
3. Efficient similarity search in feature space

**Computational Geometry:**
1. Store points in 2D/3D space
2. Query points in rectangular regions
3. Find closest points for collision detection

**Spatial Databases:**
1. Index geographic coordinates
2. Query points within bounding boxes
3. Find nearest locations to a query point

**Image Processing:**
1. Store pixel coordinates
2. Query regions of interest
3. Find similar image patches

## Project Structure

```
kd-tree/
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

- `src/main.py`: Contains `KDTree` and `KDNode` classes
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `logs/`: Directory for application log files

## Algorithm Details

### K-D Tree

**Definition:**
A k-d tree is a binary tree where each node represents a point in k-dimensional space. The tree recursively partitions the space by splitting along alternating dimensions. At each level, the dimension cycles through all k dimensions.

**Properties:**
1. Binary tree structure
2. Dimension-based splitting (alternates at each level)
3. O(log n) average height
4. Efficient for low-dimensional spaces (typically k <= 20)

**Structure (2D example):**
```
        [7, 2] (split on x)
       /        \
  [5, 4]      [9, 6] (split on y)
   /    \       /    \
[2,3] [4,7]  [8,1]  ...
```

### Dimension Cycling

**Splitting Strategy:**
- Level 0: Split on dimension 0
- Level 1: Split on dimension 1
- Level 2: Split on dimension 2
- ...
- Level k: Split on dimension 0 (cycles back)

**Formula:** dimension = depth % k

### Range Query

**Algorithm:**
1. Start at root
2. Check if current point is in range
3. Recursively search left subtree if range overlaps left region
4. Recursively search right subtree if range overlaps right region
5. Prune subtrees that cannot contain points in range

**Time Complexity:** O(n^(1-1/k) + m) where m is number of results

### Nearest Neighbor Search

**Algorithm:**
1. Start at root, traverse to leaf (like binary search)
2. Update best distance if current point is closer
3. Backtrack and check other subtrees if necessary
4. Prune subtrees that cannot contain closer points

**Pruning:**
- If distance to splitting plane > current best distance, skip subtree
- This optimization significantly reduces search space

**Time Complexity:** O(log n) average, O(n) worst case

### K-Nearest Neighbors

**Algorithm:**
1. Maintain list of k best points
2. Traverse tree similar to nearest neighbor
3. Update list when finding closer points
4. Prune based on k-th best distance

**Time Complexity:** O(k log n) average

### Operations

**Build Tree:**
- Time Complexity: O(n log n)
- Uses median selection for balanced tree
- Recursively builds tree

**Insert:**
- Time Complexity: O(log n) average
- Inserts point maintaining tree structure
- May unbalance tree (no rebalancing implemented)

**Range Query:**
- Time Complexity: O(n^(1-1/k) + m) where m is results
- Efficient for low dimensions
- Performance degrades in high dimensions

**Nearest Neighbor:**
- Time Complexity: O(log n) average, O(n) worst case
- Uses backtracking with pruning
- Efficient for low dimensions

### Edge Cases Handled

- Empty tree
- Single point
- Points with inconsistent dimensions
- Invalid range queries
- Invalid k values
- High-dimensional spaces
- Large datasets
- Exact point matches

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
- KDNode creation
- KDTree creation and building
- Insert operations
- Range queries (2D, 3D, high-D)
- Nearest neighbor search
- K-nearest neighbors search
- Edge cases (empty, single point, invalid inputs)
- Large datasets
- Dimension validation

## Troubleshooting

### Common Issues

**Performance worse than expected:**
- K-d trees work best for low dimensions (k <= 20)
- High-dimensional spaces suffer from curse of dimensionality
- Consider alternative structures for high dimensions (LSH, ball trees)

**Incorrect query results:**
- Verify point dimensions match tree dimension
- Check that range bounds are valid (min <= max)
- Ensure points are inserted correctly

**Memory issues with large datasets:**
- K-d trees require O(n) space
- Consider using approximate nearest neighbor methods
- Use batch building instead of incremental insertion

### Error Messages

**"Point dimension X doesn't match tree dimension Y"**: Attempted to insert/query point with wrong dimension.

**"All points must have the same dimension"**: Points provided to build_tree have inconsistent dimensions.

**"Range dimensions don't match tree dimension"**: Range query bounds have wrong dimension.

**"k must be positive"**: Invalid k value for k-nearest neighbors.

### Best Practices

1. **Use for low dimensions** - K-d trees excel in 2D-20D spaces
2. **Build from sorted data** - Building tree from list is more efficient than incremental insertion
3. **Validate dimensions** - Always ensure point dimensions match
4. **Consider alternatives** - For high dimensions, consider LSH or ball trees
5. **Monitor performance** - Track query times for your specific use case

## Performance Characteristics

### Time Complexity

| Operation | Average Case | Worst Case |
|-----------|--------------|------------|
| Build Tree | O(n log n) | O(n log n) |
| Insert | O(log n) | O(n) |
| Range Query | O(n^(1-1/k) + m) | O(n) |
| Nearest Neighbor | O(log n) | O(n) |
| K-Nearest Neighbors | O(k log n) | O(kn) |

Where n is the number of points, k is the dimension, and m is the number of results.

### Space Complexity

- Node storage: O(n)
- Total: O(n)

### Dimension Considerations

**Low Dimensions (k <= 10):**
- Excellent performance
- O(log n) queries typical
- Recommended use case

**Medium Dimensions (10 < k <= 20):**
- Good performance
- Some degradation
- Still usable

**High Dimensions (k > 20):**
- Poor performance
- Approaches O(n) queries
- Consider alternatives

## Applications

- **Machine Learning**: k-NN classification, similarity search
- **Computational Geometry**: Point location, range searching
- **Spatial Databases**: Geographic queries, location services
- **Image Processing**: Patch matching, feature search
- **Computer Graphics**: Collision detection, spatial queries
- **Data Mining**: Clustering, outlier detection
- **Robotics**: Path planning, obstacle avoidance

## Comparison with Other Data Structures

**K-D Tree:**
- O(log n) average queries
- Good for low dimensions
- Simple implementation
- Poor for high dimensions

**R-Tree:**
- O(log n) queries
- Better for rectangles
- More complex
- Good for spatial databases

**Ball Tree:**
- O(log n) queries
- Better for high dimensions
- More memory
- Good for machine learning

**LSH (Locality Sensitive Hashing):**
- O(1) approximate queries
- Probabilistic
- Good for high dimensions
- Approximate results

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
