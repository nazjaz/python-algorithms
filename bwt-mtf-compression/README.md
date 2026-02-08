# Burrows-Wheeler Transform with Move-to-Front Encoding

A Python implementation of Burrows-Wheeler Transform (BWT) combined with Move-to-Front (MTF) encoding for data compression. This tool provides a reversible transformation that makes data more compressible by grouping similar characters together.

## Project Title and Description

The BWT+MTF Compression tool implements the Burrows-Wheeler Transform, a reversible block-sorting algorithm that rearranges characters to group similar ones together, followed by Move-to-Front encoding which converts the BWT output into a sequence of small integers that are highly compressible.

This tool solves the problem of preprocessing data to make it more compressible. BWT groups similar characters together, and MTF converts the result into a sequence that can be efficiently compressed with run-length encoding or entropy coders. Together, they form the basis of the bzip2 compression algorithm.

**Target Audience**: Students learning compression algorithms, developers implementing compression systems, researchers studying data transformation techniques, and anyone interested in understanding BWT and MTF encoding.

## Features

- Burrows-Wheeler Transform (forward and inverse)
- Move-to-Front encoding and decoding
- Combined BWT+MTF compression pipeline
- Efficient inverse BWT using last-first property
- Configurable alphabet size
- Lossless transformation (perfect reconstruction)
- Compression ratio calculation
- Comprehensive logging and performance tracking
- Configurable algorithm parameters via YAML
- Support for binary data

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

### Step 1: Navigate to Project Directory

```bash
cd /path/to/python-algorithms/bwt-mtf-compression
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
bwt_mtf:
  alphabet_size: 256

logging:
  level: "INFO"
  file: "logs/app.log"
```

### Algorithm Parameters

- `alphabet_size`: Size of alphabet for MTF (256 for bytes)

## Usage

### Basic Usage

```python
from src.main import BWTMTFCompressor

compressor = BWTMTFCompressor()

# Compress
data = b"abracadabra"
mtf_encoded, original_index = compressor.compress(data)

# Decompress
decompressed = compressor.decompress(mtf_encoded, original_index)
assert data == decompressed
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
from src.main import BurrowsWheelerTransform, MoveToFront

# BWT only
bwt = BurrowsWheelerTransform()
data = b"abracadabra"
transformed, index = bwt.transform(data)
original = bwt.inverse_transform(transformed, index)

# MTF only
mtf = MoveToFront()
encoded = mtf.encode(b"abracadabra")
decoded = mtf.decode(encoded)
```

### Compression Ratio

```python
from src.main import BWTMTFCompressor

compressor = BWTMTFCompressor()
data = b"abracadabra"

mtf_encoded, original_index = compressor.compress(data)
ratio = compressor.get_compression_ratio(len(data), len(mtf_encoded))
print(f"Compression ratio: {ratio:.2f}")
```

## Project Structure

```
bwt-mtf-compression/
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

- `src/main.py`: Core implementation containing `BurrowsWheelerTransform`, `MoveToFront`, and `BWTMTFCompressor` classes
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
- Burrows-Wheeler Transform (forward and inverse)
- Move-to-Front encoding and decoding
- Combined BWT+MTF compression
- Edge cases (empty data, single character, etc.)
- Compression ratio calculations
- Configuration loading and validation

## Troubleshooting

### Common Issues

**Issue**: Compression ratio is less than 1.0

**Solution**: BWT+MTF is a preprocessing step. For actual compression, combine with run-length encoding or entropy coding (Huffman, arithmetic).

**Issue**: Decompressed data doesn't match original

**Solution**: 
- Check that original_index is correct
- Verify MTF encoded data is not corrupted
- Ensure same alphabet_size is used

**Issue**: BWT is slow for large data

**Solution**: 
- BWT has O(n² log n) complexity for naive implementation
- Consider using suffix arrays for O(n log n) implementation
- Process data in blocks

**Issue**: Memory usage is high

**Solution**:
- Process data in smaller blocks
- Consider streaming implementation
- Use more efficient BWT algorithms

### Error Messages

- `FileNotFoundError`: Configuration file missing - check file path
- `ValueError`: Invalid data, index, or parameters
- `yaml.YAMLError`: Invalid YAML syntax - validate config file

## Algorithm Details

### Burrows-Wheeler Transform Overview

BWT is a reversible block-sorting algorithm:
1. Create all cyclic rotations of the string
2. Sort rotations lexicographically
3. Output last column of sorted rotations
4. Track original string's position

**Key Property**: Groups similar characters together, making data more compressible.

**Time Complexity**: O(n² log n) for naive implementation, O(n log n) with suffix arrays

**Space Complexity**: O(n²) for naive, O(n) for efficient implementations

### Inverse BWT

Inverse BWT reconstructs original string:
1. Use last-first property: characters in first column appear in same order as last column
2. Build next array mapping positions
3. Follow chain from original index
4. Reverse to get original string

**Time Complexity**: O(n) using last-first property

### Move-to-Front Encoding

MTF converts symbols to indices:
1. Maintain list of symbols in order of recent use
2. For each symbol, output its position in list
3. Move symbol to front of list
4. Small indices for recently used symbols

**Time Complexity**: O(n * k) where k = alphabet size

**Space Complexity**: O(k) for alphabet list

### Combined BWT+MTF

The combination works well because:
1. BWT groups similar characters together
2. MTF converts runs of same character to runs of zeros
3. Result is highly compressible with run-length encoding
4. Used in bzip2 compression

### Compression Pipeline

Typical compression pipeline:
1. BWT: Transform data
2. MTF: Encode BWT output
3. Run-length encoding: Compress runs of zeros
4. Entropy coding: Final compression (Huffman, arithmetic)

## Performance Considerations

- BWT: O(n² log n) for naive, can be optimized to O(n log n)
- MTF: O(n * k) where k is alphabet size
- For large files, consider:
  - Processing in blocks
  - Using efficient BWT algorithms (suffix arrays)
  - Combining with other compression techniques
  - Using streaming implementations

## Real-World Applications

- bzip2 compression (uses BWT + MTF + RLE + Huffman)
- Bioinformatics (sequence alignment)
- Data preprocessing for compression
- Text compression systems
- Research in compression algorithms

## Comparison with Other Techniques

### BWT vs LZ77/LZ78

- BWT: Block-based, groups similar characters
- LZ77/LZ78: Dictionary-based, finds repeated patterns
- Often combined in practice

### MTF vs Other Encodings

- MTF: Simple, works well with BWT output
- Delta encoding: Differences between values
- Run-length encoding: Compresses runs

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

- Burrows, M., & Wheeler, D. J. (1994). A block-sorting lossless data compression algorithm.
- Move-to-Front encoding for efficient compression
- Used in bzip2 compression algorithm
- Foundation for many modern compression systems

## License

This project is part of the python-algorithms collection. See LICENSE file in parent directory for details.
