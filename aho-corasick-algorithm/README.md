# Aho-Corasick Algorithm for Multiple Pattern Matching

A Python implementation of the Aho-Corasick algorithm for multiple pattern matching with automaton construction. The algorithm achieves O(n + m + z) time complexity where n is text length, m is total pattern length, and z is number of matches by building a finite automaton with failure links.

## Project Title and Description

The Aho-Corasick Algorithm tool implements the Aho-Corasick algorithm for efficient multiple pattern matching. Unlike algorithms that search for patterns one at a time, Aho-Corasick builds a finite automaton (trie with failure links) that allows searching for all patterns simultaneously in a single pass through the text.

This tool solves the problem of efficiently matching multiple patterns in text. The algorithm is particularly useful when you need to search for many patterns in the same text, as it builds the automaton once and then searches in linear time regardless of the number of patterns.

**Target Audience**: Algorithm students, competitive programmers, text processing engineers, string algorithm researchers, bioinformatics researchers, intrusion detection system developers, and anyone interested in understanding automaton-based pattern matching algorithms.

## Features

- Aho-Corasick algorithm implementation with O(n + m + z) time complexity
- Finite automaton construction (trie with failure links)
- Multiple pattern matching in single pass
- Failure link construction using BFS
- Output link propagation for pattern matching
- Occurrence counting for all patterns
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
cd /path/to/python-algorithms/aho-corasick-algorithm
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

Run the main script to see a demonstration of Aho-Corasick algorithm operations:

```bash
python src/main.py
```

This will:
1. Build automaton from patterns
2. Search for all patterns in text
3. Display occurrence counts
4. Show all occurrences with positions

### Programmatic Usage

```python
from src.main import AhoCorasickAlgorithm

# Create Aho-Corasick automaton with patterns
patterns = ["he", "she", "his", "hers"]
ac = AhoCorasickAlgorithm(patterns)

# Search for all patterns in text
text = "ushers"
results = ac.search(text)
# Returns {"he": [2], "she": [1], "his": [], "hers": [2]}

# Count occurrences
counts = ac.count_occurrences(text)
# Returns {"he": 1, "she": 1, "his": 0, "hers": 1}

# Find all occurrences with positions
occurrences = ac.find_all_occurrences(text)
# Returns [("she", 1, 3), ("he", 2, 2), ("hers", 2, 4)]

# Check if specific pattern found
found = ac.is_pattern_found(text, "he")  # Returns True
```

### Common Use Cases

**Multiple Pattern Matching:**
1. Build automaton from patterns
2. Search text once for all patterns
3. Get results for all patterns simultaneously

**Text Analysis:**
1. Define keyword patterns
2. Search text for all keywords
3. Analyze occurrence patterns

**Intrusion Detection:**
1. Define attack signature patterns
2. Monitor text streams
3. Detect all signatures in real-time

## Project Structure

```
aho-corasick-algorithm/
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

- `src/main.py`: Contains `AhoCorasickAlgorithm` and `TrieNode` classes
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `logs/`: Directory for application log files

## Algorithm Details

### Aho-Corasick Algorithm

**Definition:**
The Aho-Corasick algorithm builds a finite automaton (trie with failure links) from multiple patterns, then searches text in a single pass to find all pattern occurrences simultaneously.

**Properties:**
1. O(n + m + z) time complexity where:
   - n = text length
   - m = total pattern length
   - z = number of matches
2. O(m) space for automaton
3. Single pass through text
4. Finds all patterns simultaneously

**Key Insight:**
Failure links (similar to KMP failure function) allow the automaton to continue matching even after a mismatch, enabling efficient pattern matching.

### Automaton Construction

**Step 1: Build Trie**
- Insert all patterns into a trie
- Mark pattern endings

**Step 2: Build Failure Links (BFS)**
- Root's children point to root
- For each node, follow failure links until finding matching character
- Similar to KMP failure function but for trie

**Step 3: Build Output Links**
- Propagate outputs through failure links
- Mark all patterns ending at each node

**Example (patterns = ["he", "she", "his", "hers"]):**
```
Trie structure with failure links (→):
        root
       /  |  \
      h   s   i
     /    |    \
    e     h     s
   /      |      \
  r       e       (end)
  |
  s (end)
```

### Pattern Matching Process

1. **Start at root**
2. **For each character in text**:
   - Follow edge if exists
   - Otherwise, follow failure link
   - Collect all outputs at current node
3. **Continue until text ends**

**Time Complexity:** O(n + m + z) - linear in text length plus matches

### Operations

**Build Automaton:**
- Time Complexity: O(m) where m is total pattern length
- Space Complexity: O(m)
- Builds trie, failure links, and output links

**Search:**
- Time Complexity: O(n + m + z)
- Space Complexity: O(1) additional
- Finds all pattern occurrences

**Count Occurrences:**
- Time Complexity: O(n + m + z)
- Returns count for each pattern

### Edge Cases Handled

- Empty patterns list (rejected)
- All empty patterns (rejected)
- Empty text (returns empty results)
- Single pattern
- Overlapping patterns
- Duplicate patterns
- Patterns at boundaries
- No matches found

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
- Automaton construction
- Pattern matching
- Occurrence counting
- Edge cases (empty, single pattern, overlapping, duplicates)
- Invalid input handling
- Result structure validation

## Troubleshooting

### Common Issues

**Pattern not found:**
- Verify pattern exists in text
- Check for case sensitivity
- Ensure pattern is in automaton

**Incorrect results:**
- Verify automaton construction
- Check failure link computation
- Validate output link propagation

**Performance issues:**
- Aho-Corasick is O(n + m + z) - should be fast
- Large number of patterns increases automaton size
- Check for excessive logging

### Error Messages

**"Patterns list cannot be empty"**: Must provide at least one pattern.

**"All patterns are empty"**: Must provide at least one non-empty pattern.

**"Pattern not in automaton"**: Pattern must be in original patterns list.

### Best Practices

1. **Build once, search many** - Build automaton once, search multiple texts
2. **Leverage linear time** - O(n + m + z) is optimal for multiple patterns
3. **Handle empty patterns** - Filter empty patterns before building automaton
4. **Use for multiple patterns** - Most efficient when searching many patterns
5. **Consider space** - O(m) space for automaton

## Performance Characteristics

### Time Complexity

| Operation | Time Complexity |
|-----------|----------------|
| Build Automaton | O(m) |
| Search | O(n + m + z) |
| Count Occurrences | O(n + m + z) |
| Find All Occurrences | O(n + m + z) |

Where:
- n = text length
- m = total pattern length
- z = number of matches

### Space Complexity

- Automaton: O(m)
- Text: O(n)
- Total: O(n + m)

## Applications

- **Intrusion Detection**: Multiple attack signature matching
- **Text Processing**: Keyword extraction from documents
- **Bioinformatics**: Multiple sequence pattern matching
- **Search Engines**: Multi-keyword search
- **Data Mining**: Pattern discovery in text
- **Competitive Programming**: Multiple pattern matching problems
- **Network Security**: Signature-based detection

## Comparison with Other Algorithms

**vs. Naive Multiple Pattern Matching:**
- Aho-Corasick: O(n + m + z) time
- Naive: O(knm) time where k is number of patterns

**vs. KMP for Each Pattern:**
- Aho-Corasick: O(n + m + z) total
- KMP: O(k(n + m)) total

**vs. Rabin-Karp for Each Pattern:**
- Aho-Corasick: Deterministic O(n + m + z)
- Rabin-Karp: O(k(n + m)) average, O(knm) worst

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
