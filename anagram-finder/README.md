# Anagram Finder

A Python implementation of an anagram finder that uses character frequency comparison and hash-based grouping to efficiently find all anagrams in a list of strings. This tool groups words that are anagrams of each other, making it ideal for word puzzles, text analysis, and linguistic research.

## Project Title and Description

The Anagram Finder provides an efficient solution for detecting and grouping anagrams in a list of strings. It uses character frequency comparison to determine if two words are anagrams and hash-based grouping to efficiently organize words into anagram groups.

This tool solves the problem of quickly identifying all anagram relationships in a collection of words, which is useful for word games, text analysis, cryptography, and linguistic research.

**Target Audience**: Students learning algorithms and data structures, developers working with text processing, educators teaching string manipulation, word game enthusiasts, and anyone interested in anagram detection.

## Features

- Character frequency comparison for anagram detection
- Hash-based grouping for efficient anagram organization
- Case-sensitive and case-insensitive modes
- Detailed analysis with statistics
- Character frequency analysis for individual words
- Find anagrams for specific target words
- File input support (one word per line)
- Comprehensive logging
- Detailed analysis reports
- Error handling for edge cases
- Command-line interface
- Demonstration mode with examples

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

### Step 1: Navigate to Project Directory

```bash
cd /path/to/python-algorithms/anagram-finder
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

### Basic Anagram Finding

Find anagrams in a list of words:

```bash
python src/main.py listen silent enlist inlets
```

### Detailed Analysis

Show detailed analysis with statistics:

```bash
python src/main.py listen silent cat act --detailed
```

### Case-Sensitive Mode

Consider case when comparing words:

```bash
python src/main.py Listen silent LISTEN --case-sensitive
```

### Find Anagrams for Specific Word

Find all anagrams of a target word:

```bash
python src/main.py listen silent enlist cat --target listen
```

### Character Frequency Analysis

Show character frequency for a specific word:

```bash
python src/main.py --frequency hello
```

### Input from File

Read words from a file (one word per line):

```bash
python src/main.py --file words.txt
```

### Generate Report

Generate detailed analysis report:

```bash
python src/main.py listen silent cat act --detailed --report report.txt
```

### Demonstration Mode

Run demonstration with example words:

```bash
python src/main.py --demo
```

### Command-Line Arguments

- `words`: (Optional) Words to analyze (space-separated)
- `-c, --config`: Path to configuration file (default: config.yaml)
- `-f, --file`: Path to file containing words (one per line)
- `-d, --detailed`: Show detailed analysis with statistics
- `-s, --case-sensitive`: Consider case when comparing words
- `-t, --target`: Find anagrams for a specific target word
- `-r, --report`: Output path for analysis report
- `--frequency`: Show character frequency for a specific word
- `--demo`: Run demonstration with example words

### Common Use Cases

**Find Anagram Groups:**
1. Run: `python src/main.py listen silent enlist inlets`
2. Review anagram groups
3. Understand hash-based grouping

**Analyze Word List:**
1. Run: `python src/main.py --file words.txt --detailed`
2. Review statistics
3. Identify largest anagram groups

**Find Anagrams for Word:**
1. Run: `python src/main.py listen silent enlist --target listen`
2. Review anagram matches
3. Understand character frequency matching

**Character Analysis:**
1. Run: `python src/main.py --frequency hello`
2. Review character frequencies
3. Understand hash key generation

## Project Structure

```
anagram-finder/
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

- `src/main.py`: Contains the `AnagramFinder` class with character frequency and hash-based grouping
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `docs/API.md`: API documentation for the finder
- `logs/`: Directory for application log files

## Algorithm Details

### Character Frequency Comparison

The algorithm determines if two words are anagrams by comparing their character frequencies:

1. **Count Characters**: Count frequency of each character in each word
2. **Normalize**: Convert to lowercase for case-insensitive comparison
3. **Compare**: Two words are anagrams if they have identical character frequencies

**Example:**
```
"listen" -> {'l': 1, 'i': 1, 's': 1, 't': 1, 'e': 1, 'n': 1}
"silent" -> {'s': 1, 'i': 1, 'l': 1, 'e': 1, 'n': 1, 't': 1}
Same frequencies → Anagrams
```

### Hash-Based Grouping

The algorithm groups anagrams efficiently using hash keys:

1. **Generate Hash**: Create hash key from sorted character frequencies
2. **Group by Hash**: Words with same hash key are grouped together
3. **Filter Groups**: Only return groups with more than one word

**Hash Key Format:**
- Sort characters alphabetically
- Create string: `char1count1char2count2...`
- Example: "listen" → "e1i1l1n1s1t1"

**Example:**
```
"listen" → hash: "e1i1l1n1s1t1"
"silent" → hash: "e1i1l1n1s1t1"
Same hash → Same group
```

### Time Complexity

- **O(n * m)** where:
  - n = number of words
  - m = average word length
- Each word is processed once
- Character frequency calculation: O(m)
- Hash generation: O(m log m) for sorting
- Grouping: O(n) with hash-based lookup

### Space Complexity

- **O(n * m)** for storing:
  - Groups dictionary
  - Character frequency data
  - Hash keys

### Properties

- **Efficient**: Hash-based grouping provides O(1) average lookup
- **Case-insensitive**: Default behavior (configurable)
- **Handles duplicates**: Correctly handles duplicate words
- **Scalable**: Works well with large word lists

## Examples

### Example 1: Basic Anagram Finding

```bash
$ python src/main.py listen silent enlist inlets
Found 1 anagram groups:
  ['listen', 'silent', 'enlist', 'inlets']
```

### Example 2: Multiple Groups

```bash
$ python src/main.py listen silent cat act dog
Found 2 anagram groups:
  ['listen', 'silent']
  ['cat', 'act']
```

### Example 3: Detailed Analysis

```bash
$ python src/main.py listen silent cat act --detailed

Anagram Analysis:
  Total words: 4
  Anagram groups: 2
  Words in groups: 4

Anagram Groups:
  ['listen', 'silent']
  ['cat', 'act']
```

### Example 4: Character Frequency

```bash
$ python src/main.py --frequency hello

Character Frequency Analysis for 'hello':
  Total characters: 5
  Unique characters: 4
  Hash key: e1h1l2o1
  Frequencies: {'h': 1, 'e': 1, 'l': 2, 'o': 1}
```

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
- Character frequency calculation
- Hash key generation
- Anagram detection
- Hash-based grouping
- Case sensitivity handling
- Edge cases (empty lists, single words, duplicates)
- Detailed analysis
- Report generation

## Troubleshooting

### Common Issues

**No anagram groups found:**
- Words may not have anagrams in the list
- Check case sensitivity settings
- Verify words are spelled correctly

**Import Errors:**
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (requires 3.8+)
- Verify virtual environment is activated

**File not found:**
- Check file path is correct
- Verify file exists and is readable
- Check file permissions

### Error Messages

**"Configuration file not found"**: Config file doesn't exist at specified path. Check file path or create config.yaml.

**"Invalid YAML in configuration file"**: Config file has syntax errors. Verify YAML format.

**"File not found"**: Input file doesn't exist. Check file path.

**"Failed to save report"**: Cannot write report file. Check file permissions and path.

### Best Practices

1. **Use detailed mode** for comprehensive analysis: `--detailed`
2. **Generate reports** for documentation: `--report report.txt`
3. **Check logs** to understand processing
4. **Use file input** for large word lists: `--file words.txt`
5. **Consider case sensitivity** when needed: `--case-sensitive`
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
