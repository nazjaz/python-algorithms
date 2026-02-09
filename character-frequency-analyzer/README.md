# Character Frequency Analyzer

A Python implementation of character frequency analysis using dictionary data structure. This tool counts occurrences of each character in a string and provides comprehensive frequency analysis with detailed statistics.

## Project Title and Description

The Character Frequency Analyzer tool counts occurrences of each character in a string using dictionary data structures. It supports multiple implementation approaches (standard dictionary, defaultdict, Counter) and provides detailed frequency analysis including most/least common characters, percentages, and distribution statistics.

This tool solves the problem of analyzing character distribution in text by providing efficient counting algorithms and comprehensive analysis capabilities.

**Target Audience**: Students learning data structures, developers studying text analysis, educators teaching computer science concepts, and anyone interested in understanding character frequency analysis and dictionary usage.

## Features

- Multiple counting methods: standard dictionary, defaultdict, Counter
- Comprehensive frequency analysis
- Most and least common character identification
- Character percentage calculations
- Top N most frequent characters
- Detailed character information (Unicode, properties)
- Frequency distribution statistics
- Comprehensive analysis reports

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

### Step 1: Navigate to Project Directory

```bash
cd /path/to/python-algorithms/character-frequency-analyzer
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

### Basic Usage

Analyze character frequency:

```bash
python src/main.py "Hello World"
```

### Using Different Methods

Use specific counting method:

```bash
python src/main.py "Hello World" --method dict
python src/main.py "Hello World" --method defaultdict
python src/main.py "Hello World" --method counter
python src/main.py "Hello World" --method all
```

### Show Top Characters

Show top N most frequent characters:

```bash
python src/main.py "Hello World" --top 5
```

### Search Specific Character

Get detailed information about a character:

```bash
python src/main.py "Hello World" --search "l"
```

### Generate Report

Generate comprehensive analysis report:

```bash
python src/main.py "Hello World" --report report.txt
```

### Command-Line Arguments

- `text`: (Required) String to analyze
- `-c, --config`: Path to configuration file (default: config.yaml)
- `-m, --method`: Counting method - dict, defaultdict, counter, or all (default: dict)
- `-t, --top`: Show top N most frequent characters
- `-s, --search`: Get detailed info for specific character
- `-r, --report`: Output path for analysis report

### Common Use Cases

**Basic Analysis:**
1. Run: `python src/main.py "Hello World"`
2. Review character frequencies
3. See distribution statistics

**Find Most Common:**
1. Use top option: `python src/main.py "text" --top 10`
2. Identify most frequent characters
3. Analyze text patterns

**Detailed Analysis:**
1. Generate report: `python src/main.py "text" --report analysis.txt`
2. Review comprehensive statistics
3. Study character distribution

## Project Structure

```
character-frequency-analyzer/
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

- `src/main.py`: Contains the `CharacterFrequencyAnalyzer` class and main logic
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `logs/`: Directory for application log files

## Algorithm Details

### Dictionary-Based Counting

The tool uses dictionary data structure to efficiently count character occurrences.

**Standard Dictionary Method:**
- Manually checks if key exists before incrementing
- Time Complexity: O(n)
- Space Complexity: O(k) where k is number of unique characters

**DefaultDict Method:**
- Uses defaultdict(int) for automatic initialization
- Cleaner code, same performance
- Time Complexity: O(n)
- Space Complexity: O(k)

**Counter Method:**
- Uses collections.Counter for optimized counting
- Most Pythonic approach
- Time Complexity: O(n)
- Space Complexity: O(k)

**All Methods:**
- Produce identical results
- Same time and space complexity
- Different code styles and readability

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
- Character counting with various inputs
- Edge cases (empty string, single character, special characters)
- All three counting methods
- Frequency analysis functionality
- Report generation
- Error handling

## Troubleshooting

### Common Issues

**Empty String:**
- Empty strings return empty frequency dictionary
- Analysis statistics reflect zero characters

**Special Characters:**
- All characters including whitespace, newlines, tabs are counted
- Use repr() for display of special characters

**Import Errors:**
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (requires 3.8+)
- Verify virtual environment is activated

### Error Messages

**"Configuration file not found"**: The config.yaml file doesn't exist. Create it or specify path with `-c` option.

**"Failed to save report"**: Cannot write to output directory. Check permissions and disk space.

### Best Practices

1. **Use Counter method** for production code (most Pythonic)
2. **Use defaultdict** for cleaner code when learning
3. **Generate reports** for comprehensive analysis
4. **Use top N option** to focus on most frequent characters
5. **Review character info** to understand text composition

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
