# Huffman Coding with Adaptive and Canonical Variants

A Python implementation of Huffman coding with standard, adaptive, and canonical variants. This tool provides lossless data compression using variable-length codes optimized for symbol frequencies.

## Project Title and Description

The Huffman Coding tool implements three variants of Huffman coding: standard (tree-based), adaptive (FGK algorithm), and canonical (efficient code representation). These algorithms provide optimal prefix codes for lossless data compression based on symbol frequencies.

This tool solves the problem of compressing data by assigning shorter codes to more frequent symbols. It offers three approaches: standard Huffman for known frequencies, adaptive Huffman for streaming data, and canonical Huffman for efficient code storage and transmission.

**Target Audience**: Students learning compression algorithms, developers implementing compression systems, researchers studying entropy coding, and anyone interested in understanding how Huffman coding works.

## Features

- Standard Huffman coding with tree building
- Adaptive Huffman coding (FGK algorithm) for streaming
- Canonical Huffman coding for efficient code representation
- Automatic frequency calculation
- Lossless compression (perfect reconstruction)
- Compression ratio calculation
- Comprehensive logging and performance tracking
- Configurable algorithm parameters via YAML
- Support for binary data compression
- Tree visualization support

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

### Step 1: Navigate to Project Directory

```bash
cd /path/to/python-algorithms/huffman-coding
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

The algorithms are configured via `config.yaml`:

```yaml
logging:
  level: "INFO"
  file: "logs/app.log"
```

## Usage

### Basic Usage - Standard Huffman

```python
from src.main import HuffmanCodingManager

manager = HuffmanCodingManager()

# Compress
data = b"abracadabra"
encoded, codes = manager.compress_standard(data)

# Decompress
decoded = manager.decompress_standard(encoded, codes)
assert data == decoded
```

### Canonical Huffman

```python
from src.main import HuffmanCodingManager

manager = HuffmanCodingManager()

# Compress
data = b"abracadabra"
encoded, code_lengths = manager.compress_canonical(data)

# Decompress (only need code lengths, not full codes)
decoded = manager.decompress_canonical(encoded, code_lengths)
assert data == decoded
```

### Adaptive Huffman

```python
from src.main import HuffmanCodingManager

manager = HuffmanCodingManager()

# Compress (no need for frequencies)
data = b"abracadabra"
encoded = manager.compress_adaptive(data)

# Decompress
decoded = manager.decompress_adaptive(encoded)
assert data == decoded
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

### Direct Class Usage

```python
from src.main import StandardHuffman, CanonicalHuffman, AdaptiveHuffman
from collections import Counter

# Standard Huffman
data = b"test data"
frequencies = Counter(data)
huffman = StandardHuffman()
huffman.build_tree(frequencies)
encoded, codes = huffman.encode(data)
decoded = huffman.decode(encoded)

# Canonical Huffman
canonical = CanonicalHuffman()
canonical.build_from_standard(huffman)
encoded, lengths = canonical.encode(data)
decoded = canonical.decode(encoded)

# Adaptive Huffman
adaptive = AdaptiveHuffman()
encoded = adaptive.encode(data)
decoded = adaptive.decode(encoded)
```

### Compression Ratio

```python
from src.main import HuffmanCodingManager

manager = HuffmanCodingManager()
data = b"abracadabra"

encoded, _ = manager.compress_standard(data)
ratio = manager.get_compression_ratio(len(data), len(encoded))
print(f"Compression ratio: {ratio:.2f}")
```

## Project Structure

```
huffman-coding/
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

- `src/main.py`: Core implementation containing `StandardHuffman`, `CanonicalHuffman`, `AdaptiveHuffman`, and `HuffmanCodingManager` classes
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
- Standard Huffman compression and decompression
- Canonical Huffman compression and decompression
- Adaptive Huffman compression and decompression
- Tree building and code generation
- Edge cases (empty data, single symbol, etc.)
- Compression ratio calculations
- Configuration loading and validation

## Troubleshooting

### Common Issues

**Issue**: Compression ratio is less than 1.0

**Solution**: This is normal for data with uniform symbol distribution. Huffman coding works best when symbol frequencies vary significantly.

**Issue**: Decompressed data doesn't match original

**Solution**: 
- Check that you're using the same algorithm variant
- Verify codes/code_lengths are correct
- Ensure encoded bits are not corrupted

**Issue**: Adaptive Huffman is slow

**Solution**: 
- Adaptive Huffman is slower than standard but doesn't require pre-processing
- Use standard or canonical for better performance if frequencies are known

**Issue**: Memory usage is high

**Solution**:
- Process data in chunks
- Use canonical Huffman (stores only code lengths)
- Consider streaming compression

### Error Messages

- `FileNotFoundError`: Configuration file missing - check file path
- `ValueError`: Invalid parameter values or tree not built
- `yaml.YAMLError`: Invalid YAML syntax - validate config file

## Algorithm Details

### Standard Huffman Coding

Standard Huffman coding:
1. Calculate symbol frequencies
2. Build Huffman tree using priority queue
3. Generate codes by traversing tree
4. Encode data using generated codes

**Time Complexity**: O(n log n) for tree building, O(n) for encoding

**Space Complexity**: O(k) where k = number of unique symbols

### Canonical Huffman Coding

Canonical Huffman coding:
1. Build standard Huffman tree
2. Extract code lengths
3. Generate canonical codes from lengths
4. Same compression ratio, more efficient storage

**Advantages**:
- Only need to store code lengths, not full codes
- Faster decoding
- More efficient for transmission

**Time Complexity**: O(k log k) for code generation

### Adaptive Huffman Coding

Adaptive Huffman (FGK algorithm):
1. Start with empty tree (NYT node)
2. For each symbol:
   - If new: output NYT code + symbol
   - If seen: output symbol code
   - Update tree frequencies
   - Rebalance tree if needed
3. No need for pre-processing

**Advantages**:
- No need to know frequencies in advance
- Works for streaming data
- Adapts to changing symbol frequencies

**Time Complexity**: O(n log k) where k = alphabet size

**Disadvantages**:
- Slower than standard
- More complex implementation

### Code Generation

**Standard**: Codes generated by tree traversal (left=0, right=1)

**Canonical**: Codes generated from lengths:
- Sort symbols by length
- Assign codes in order
- First code of length L is 0...0 (L bits)
- Next codes increment by 1

**Adaptive**: Codes generated dynamically as tree updates

## Performance Considerations

- Standard Huffman: Best for known frequencies
- Canonical Huffman: Best for transmission (smaller metadata)
- Adaptive Huffman: Best for streaming/unknown frequencies
- For large files, consider:
  - Processing in blocks
  - Using canonical for smaller metadata
  - Combining with other compression (LZ77, etc.)

## Real-World Applications

- ZIP file format (DEFLATE uses Huffman)
- JPEG image compression
- MP3 audio compression
- PNG image format
- HTTP compression (gzip)
- Database compression
- Text compression systems

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

- Huffman, D. A. (1952). A method for the construction of minimum-redundancy codes.
- Faller, N. (1973). Adaptive variable-length coding for independent sources.
- Gallager, R. G. (1978). Variations on a theme by Huffman.
- Canonical Huffman codes for efficient storage and transmission.

## License

This project is part of the python-algorithms collection. See LICENSE file in parent directory for details.
