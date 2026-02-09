# R-Tree for Spatial Indexing and Geometric Range Queries

A Python implementation of R-tree data structure that efficiently stores spatial objects (rectangles) and supports geometric range queries. R-trees use bounding boxes to organize spatial data hierarchically, achieving O(log n) average time complexity for queries.

## Project Title and Description

The R-Tree tool implements a spatial indexing data structure designed to store rectangles (bounding boxes) and efficiently answer queries about overlapping rectangles. Each node in the tree contains multiple entries, and each entry has a minimum bounding rectangle (MBR) that encompasses all rectangles in its subtree.

This tool solves the problem of efficiently managing and querying spatial data, which is fundamental in many applications including geographic information systems, computer graphics, and database systems. The R-tree provides O(log n) average time complexity for insertion and range queries.

**Target Audience**: Algorithm students, competitive programmers, data structure researchers, software engineers, GIS developers, and anyone interested in understanding spatial indexing and geometric data structures.

## Features

- R-tree implementation with hierarchical bounding boxes
- O(log n) average time complexity for insert and query operations
- Efficient range queries for overlapping rectangles
- Quadratic split algorithm for node overflow handling
- Minimum bounding rectangle (MBR) tracking
- Support for arbitrary data association with rectangles
- Configurable node capacity (min/max entries)
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
cd /path/to/python-algorithms/r-tree
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
- `logging.file`: Path to log file (default: "logs/r_tree.log")

### Example Configuration

```yaml
logging:
  level: "INFO"
  file: "logs/r_tree.log"
```

### Environment Variables

No environment variables are currently required. All configuration is managed through the `config.yaml` file.

## Usage

### Basic Usage

Run the main script to see a demonstration of R-tree operations:

```bash
python src/main.py
```

This will:
1. Create an R-tree
2. Insert rectangles
3. Perform range queries
4. Display results

### Programmatic Usage

```python
from src.main import RTree

# Create R-tree
tree = RTree(max_entries=4, min_entries=2)

# Insert rectangles
tree.insert(1, 1, 3, 3)
tree.insert(2, 2, 4, 4)
tree.insert(5, 5, 7, 7)

# Range query
results = tree.range_query(2, 2, 6, 6)
for rect, data in results:
    print(f"Rectangle: {rect}, Data: {data}")

# Insert with data
tree.insert(10, 10, 12, 12, data="location_A")

# Get all rectangles
all_rects = tree.get_all_rectangles()
```

### Common Use Cases

**Geographic Information Systems:**
1. Store geographic regions (bounding boxes)
2. Query for regions overlapping a search area
3. Efficient spatial indexing

**Computer Graphics:**
1. Store object bounding boxes
2. Query for objects in view frustum
3. Collision detection optimization

**Database Systems:**
1. Index spatial data
2. Range queries on geographic coordinates
3. Efficient spatial joins

## Project Structure

```
r-tree/
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

- `src/main.py`: Contains `RTree`, `RTreeNode`, and `Rectangle` classes
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `logs/`: Directory for application log files

## Algorithm Details

### R-Tree

**Definition:**
An R-tree is a tree data structure used for spatial indexing. Each node contains multiple entries, and each entry has a minimum bounding rectangle (MBR) that encompasses all rectangles in its subtree. Leaf nodes contain actual data rectangles, while internal nodes contain child nodes with their MBRs.

**Properties:**
1. Hierarchical structure with multiple entries per node
2. Minimum bounding rectangles (MBR) for efficient pruning
3. O(log n) average height
4. Efficient for spatial range queries

**Structure:**
```
        Root (Internal)
       /      |      \
   Node1    Node2   Node3
   /  | \   /  | \  /  | \
  R1 R2 R3 R4 R5 R6 R7 R8 R9
```

Each node has:
- Multiple entries (up to max_entries)
- Each entry: (MBR, child_node, data)
- MBR encompasses all entries in subtree

### Minimum Bounding Rectangle (MBR)

**Purpose:**
Each node maintains an MBR that encompasses all rectangles in its subtree. This allows efficient pruning during queries - if a query rectangle doesn't intersect a node's MBR, the entire subtree can be skipped.

**Calculation:**
MBR is the union of all entry MBRs in the node, updated after each insertion or deletion.

### Insertion Algorithm

**Steps:**
1. Choose best subtree using expansion area heuristic
2. Recursively insert into chosen subtree
3. Update MBR along path to root
4. If node overflows, split using quadratic split
5. Propagate split upward if necessary

**Subtree Selection:**
- Choose subtree that requires minimum area expansion
- If tie, choose subtree with smaller area

### Quadratic Split Algorithm

**Purpose:**
When a node overflows (exceeds max_entries), it must be split into two nodes.

**Algorithm:**
1. Pick two seed entries that maximize waste (area of union - sum of areas)
2. Assign remaining entries to group requiring minimum expansion
3. Ensure both groups have at least min_entries entries

**Waste Calculation:**
waste = union_area - area1 - area2

Higher waste indicates better separation between groups.

### Range Query Algorithm

**Steps:**
1. Start at root
2. For each entry in current node:
   - If entry MBR intersects query rectangle:
     - If leaf node: add rectangle to results if it intersects
     - If internal node: recursively search child
3. Return all intersecting rectangles

**Pruning:**
- If entry MBR doesn't intersect query, skip entire subtree
- This optimization significantly reduces search space

### Operations

**Insert:**
- Time Complexity: O(log n) average
- Choose best subtree, insert recursively
- Handle overflow with splitting
- Update MBRs along path

**Range Query:**
- Time Complexity: O(log n + m) average where m is results
- Traverse tree using MBR intersection
- Prune subtrees that don't intersect query

**Get All Rectangles:**
- Time Complexity: O(n)
- Traverse entire tree collecting rectangles

### Edge Cases Handled

- Empty tree
- Single rectangle
- Invalid rectangles (min > max)
- Node overflow and splitting
- Root node splitting
- Overlapping rectangles
- Nested rectangles
- Adjacent rectangles
- Point rectangles

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
- Rectangle creation and operations
- RTreeNode creation and MBR updates
- RTree creation and configuration
- Insert operations
- Range queries
- Node splitting
- Edge cases (empty, invalid inputs, large datasets)
- Different node capacity configurations

## Troubleshooting

### Common Issues

**Performance worse than expected:**
- R-trees work best for low-dimensional spaces (2D, 3D)
- High-dimensional spaces suffer from curse of dimensionality
- Consider tuning max_entries/min_entries for your data

**Incorrect query results:**
- Verify rectangles are inserted correctly
- Check that MBRs are updated after insertions
- Ensure split algorithm maintains tree structure

**Memory issues with large datasets:**
- R-trees require O(n) space
- Consider using bulk loading for initial construction
- Monitor node capacity settings

### Error Messages

**"Invalid rectangle: min > max"**: Attempted to create rectangle with invalid coordinates.

**"Invalid min/max entries configuration"**: min_entries must be >= 1 and <= max_entries.

### Best Practices

1. **Tune node capacity** - Adjust max_entries/min_entries for your data distribution
2. **Use appropriate data** - R-trees work best for 2D/3D spatial data
3. **Bulk loading** - For initial construction, consider bulk loading algorithms
4. **Monitor performance** - Track query times for your specific use case
5. **Consider alternatives** - For high dimensions, consider other structures

## Performance Characteristics

### Time Complexity

| Operation | Average Case | Worst Case |
|-----------|--------------|------------|
| Insert | O(log n) | O(n) |
| Range Query | O(log n + m) | O(n) |
| Get All Rectangles | O(n) | O(n) |

Where n is the number of rectangles and m is the number of results.

### Space Complexity

- Node storage: O(n)
- Total: O(n)

### Node Capacity

**Typical Values:**
- max_entries: 4-50 (common: 4-10)
- min_entries: 1 to max_entries/2 (common: 2-5)

**Trade-offs:**
- Higher max_entries: fewer nodes, larger nodes, more overlap
- Lower max_entries: more nodes, smaller nodes, less overlap

## Applications

- **Geographic Information Systems**: Index geographic regions, query overlapping areas
- **Computer Graphics**: Object culling, view frustum queries, collision detection
- **Database Systems**: Spatial indexing, range queries on coordinates
- **Computer Vision**: Object detection, region queries
- **Robotics**: Path planning, obstacle avoidance
- **Game Development**: Spatial partitioning, collision detection

## Comparison with Other Data Structures

**R-Tree:**
- O(log n) queries
- Good for rectangles
- Handles overlap well
- Hierarchical structure

**K-D Tree:**
- O(log n) queries
- Better for points
- Poor for rectangles
- Simpler structure

**Quadtree:**
- O(log n) queries
- Fixed partitioning
- Good for uniform distribution
- Less flexible

**Grid Index:**
- O(1) queries
- Fixed cell size
- Poor for non-uniform data
- Simple implementation

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
