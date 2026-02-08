# LZ77 and LZ78 Compression Algorithms

A Python implementation of LZ77 and LZ78 compression algorithms with dictionary management and encoding. This tool provides lossless data compression capabilities with configurable parameters for both algorithms.

## Project Title and Description

The LZ Compression tool implements two foundational lossless compression algorithms: LZ77 and LZ78. These algorithms form the basis for many modern compression formats including ZIP, GIF, PNG, and DEFLATE. The implementation provides both compression and decompression with configurable dictionary management.

This tool solves the problem of compressing data by identifying and encoding repeated patterns. LZ77 uses a sliding window approach while LZ78 builds a dictionary incrementally. Both algorithms are useful for text compression, file compression, and understanding compression fundamentals.

**Target Audience**: Students learning compression algorithms, developers implementing compression systems, researchers studying data compression, and anyone interested in understanding how compression works.

## Features

- LZ77 compression with sliding window and look-ahead buffer
- LZ77 decompression with pattern reconstruction
- LZ78 compression with incremental dictionary building
- LZ78 decompression with dictionary reconstruction
- Configurable window sizes and dictionary limits
- Compression ratio calculation
- Comprehensive logging and performance tracking
- Configurable algorithm parameters via YAML
- Support for binary data compression
- Lossless compression (perfect reconstruction)

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

### Step 1: Navigate to Project Directory

```bash
cd /path/to/python-algorithms/lz-compression
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
lz77:
  window_size: 4096
  lookahead_size: 18
  min_match_length: 3

lz78:
  max_dict_size: 4096

logging:
  level: "INFO"
  file: "logs/app.log"
```

### LZ77 Parameters

- `window_size`: Size of search buffer (sliding window) in bytes
- `lookahead_size`: Size of look-ahead buffer in bytes
- `min_match_length`: Minimum match length to encode (reduces overhead)

### LZ78 Parameters

- `max_dict_size`: Maximum dictionary size (0 = unlimited)

## Usage

### Basic Usage

```python
from src.main import CompressionManager

# Initialize manager
manager = CompressionManager(config_path="config.yaml")

# Compress data
data = b"abracadabraabracadabra"
compressed = manager.compress_lz77(data)

# Decompress
decompressed = manager.decompress_lz77(compressed)
assert data == decompressed
```

### LZ77 Compression

```python
from src.main import LZ77Compressor

compressor = LZ77Compressor(
    window_size=4096,
    lookahead_size=18,
    min_match_length=3
)

data = b"hello hello world"
compressed = compressor.compress(data)
decompressed = compressor.decompress(compressed)
```

### LZ78 Compression

```python
from src.main import LZ78Compressor

compressor = LZ78Compressor(max_dict_size=4096)

data = b"abracadabra"
compressed = compressor.compress(data)
decompressed = compressor.decompress(compressed)
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

### Compression Ratio

```python
from src.main import CompressionManager

manager = CompressionManager()
data = b"repeated text repeated text"

compressed_lz77 = manager.compress_lz77(data)
ratio_lz77 = manager.get_compression_ratio(
    len(data), len(compressed_lz77), token_size=3
)
print(f"LZ77 compression ratio: {ratio_lz77:.2f}")

compressed_lz78 = manager.compress_lz78(data)
ratio_lz78 = manager.get_compression_ratio(
    len(data), len(compressed_lz78), token_size=2
)
print(f"LZ78 compression ratio: {ratio_lz78:.2f}")
```

## Project Structure

```
lz-compression/
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

- `src/main.py`: Core implementation containing `LZ77Compressor`, `LZ78Compressor`, and `CompressionManager` classes
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
- LZ77 compression and decompression
- LZ78 compression and decompression
- Dictionary management
- Edge cases (empty data, single character, etc.)
- Compression ratio calculations
- Configuration loading and validation

## Troubleshooting

### Common Issues

**Issue**: Compression ratio is less than 1.0

**Solution**: This is normal for data with little repetition. Compression works best on repetitive data.

**Issue**: Decompressed data doesn't match original

**Solution**: 
- Check that you're using the same algorithm for compression and decompression
- Verify data is not corrupted
- Check for encoding issues

**Issue**: Memory usage is high

**Solution**:
- Reduce `window_size` for LZ77
- Reduce `max_dict_size` for LZ78
- Process data in chunks

**Issue**: Compression is slow

**Solution**:
- Reduce `window_size` and `lookahead_size` for LZ77
- Reduce `max_dict_size` for LZ78
- Increase `min_match_length` for LZ77

### Error Messages

- `FileNotFoundError`: Configuration file missing - check file path
- `ValueError`: Invalid parameter values - check config.yaml
- `yaml.YAMLError`: Invalid YAML syntax - validate config file

## Algorithm Details

### LZ77 Algorithm

LZ77 uses a sliding window approach:
1. Maintains a search buffer (already processed data)
2. Maintains a look-ahead buffer (data to process)
3. Finds longest match in search buffer
4. Encodes as (offset, length, next_char)
5. Slides window forward

**Encoding Format**: (offset, length, next_char)
- Offset: Distance back in search buffer
- Length: Length of matched string
- Next char: Character after match

**Time Complexity**: O(n * w) where n = data length, w = window size

### LZ78 Algorithm

LZ78 builds a dictionary incrementally:
1. Starts with empty dictionary
2. For each character, extends current string
3. If string not in dictionary, add it
4. Encode as (dict_index, next_char)
5. Reset current string

**Encoding Format**: (dict_index, next_char)
- Dict index: Index of longest prefix in dictionary
- Next char: Character that extends the prefix

**Time Complexity**: O(n) where n = data length

### Dictionary Management

**LZ77**: Uses sliding window (fixed size, oldest data discarded)

**LZ78**: Builds dictionary incrementally (can be limited by max_dict_size)

### Compression Efficiency

- **LZ77**: Best for data with local repetition
- **LZ78**: Best for data with global patterns
- Both are lossless (perfect reconstruction)
- Compression ratio depends on data characteristics

## Performance Considerations

- LZ77: Memory usage O(window_size + lookahead_size)
- LZ78: Memory usage O(max_dict_size)
- For large files, consider:
  - Processing in chunks
  - Adjusting window/dictionary sizes
  - Using streaming compression
  - Combining with entropy coding (Huffman, arithmetic)

## Real-World Applications

- ZIP file format (uses DEFLATE, based on LZ77)
- GIF image format (uses LZW, variant of LZ78)
- PNG image format (uses DEFLATE)
- HTTP compression (gzip, deflate)
- Database compression
- Backup systems

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

- Ziv, J., & Lempel, A. (1977). A universal algorithm for sequential data compression.
- Ziv, J., & Lempel, A. (1978). Compression of individual sequences via variable-rate coding.
- Foundation for modern compression formats (ZIP, GIF, PNG, etc.)

## License

This project is part of the python-algorithms collection. See LICENSE file in parent directory for details.
