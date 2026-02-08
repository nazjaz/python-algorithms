# Arithmetic Coding for Lossless Compression

A Python implementation of arithmetic coding for lossless data compression with precision handling and range updates. This tool provides optimal compression by encoding entire messages into a single number rather than encoding symbols separately.

## Project Title and Description

The Arithmetic Coding tool implements arithmetic coding, an advanced lossless compression algorithm that can achieve compression ratios very close to the entropy limit. It encodes the entire message into a single number between 0 and 1, using probability ranges and precision handling to manage finite precision arithmetic.

This tool solves the problem of achieving near-optimal compression for data with known or learnable symbol probabilities. It offers better compression than Huffman coding in many cases, especially when symbol probabilities are not powers of 1/2. The implementation handles precision issues through renormalization and scaling.

**Target Audience**: Students learning advanced compression algorithms, developers implementing high-performance compression systems, researchers studying information theory, and anyone interested in understanding arithmetic coding.

## Features

- Arithmetic coding encoder with range updates
- Arithmetic coding decoder with range reconstruction
- Precision handling using renormalization
- Probability model management
- Automatic frequency calculation
- Lossless compression (perfect reconstruction)
- Configurable precision (32 or 64 bits)
- Compression ratio calculation
- Comprehensive logging and performance tracking
- Support for binary data compression

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

### Step 1: Navigate to Project Directory

```bash
cd /path/to/python-algorithms/arithmetic-coding
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
arithmetic_coding:
  precision_bits: 32

logging:
  level: "INFO"
  file: "logs/app.log"
```

### Precision Bits

- `precision_bits`: Number of bits for precision (32 or 64)
  - 32 bits: Faster, good for most cases
  - 64 bits: Better precision, slower but more accurate

## Usage

### Basic Usage

```python
from src.main import ArithmeticCodingManager

manager = ArithmeticCodingManager()

# Compress
data = b"abracadabra"
encoded_bits, model, length = manager.compress(data)

# Decompress
decoded = manager.decompress(encoded_bits, model, length)
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

### Custom Probability Model

```python
from src.main import ArithmeticCodingManager, ProbabilityModel

# Create custom probability model
frequencies = {97: 5, 98: 2, 99: 1, 100: 1}
model = ProbabilityModel(frequencies)

manager = ArithmeticCodingManager()
data = b"abcd"

encoded_bits, model, length = manager.compress(data, model=model)
decoded = manager.decompress(encoded_bits, model, length)
```

### Direct Class Usage

```python
from src.main import (
    ArithmeticEncoder,
    ArithmeticDecoder,
    ProbabilityModel,
)
from collections import Counter

data = b"abracadabra"
frequencies = Counter(data)
model = ProbabilityModel(frequencies)

# Encode
encoder = ArithmeticEncoder(precision_bits=32)
encoded_bits, model = encoder.encode(data, model)

# Decode
decoder = ArithmeticDecoder(precision_bits=32)
decoded = decoder.decode(encoded_bits, model, len(data))
```

### Compression Ratio

```python
from src.main import ArithmeticCodingManager

manager = ArithmeticCodingManager()
data = b"abracadabra"

encoded_bits, model, length = manager.compress(data)
ratio = manager.get_compression_ratio(len(data), len(encoded_bits))
print(f"Compression ratio: {ratio:.2f}")
```

## Project Structure

```
arithmetic-coding/
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

- `src/main.py`: Core implementation containing `ProbabilityModel`, `ArithmeticEncoder`, `ArithmeticDecoder`, and `ArithmeticCodingManager` classes
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
- Probability model creation and updates
- Arithmetic encoding and decoding
- Range updates and scaling
- Precision handling and renormalization
- Edge cases (empty data, single symbol, etc.)
- Compression ratio calculations
- Configuration loading and validation

## Troubleshooting

### Common Issues

**Issue**: Compression ratio is less than 1.0

**Solution**: This is normal for data with uniform symbol distribution. Arithmetic coding works best when symbol probabilities vary significantly.

**Issue**: Decompressed data doesn't match original

**Solution**: 
- Check that same probability model is used for encoding and decoding
- Verify encoded bits are not corrupted
- Ensure length parameter matches original data length
- Check precision settings match

**Issue**: Precision errors or overflow

**Solution**:
- Increase `precision_bits` to 64
- Check that probability model is valid
- Verify renormalization is working correctly

**Issue**: Memory usage is high

**Solution**:
- Process data in chunks
- Use lower precision (32 bits)
- Consider adaptive probability models

### Error Messages

- `FileNotFoundError`: Configuration file missing - check file path
- `ValueError`: Invalid symbol, probability model, or value out of range
- `yaml.YAMLError`: Invalid YAML syntax - validate config file

## Algorithm Details

### Arithmetic Coding Overview

Arithmetic coding encodes the entire message into a single number:
1. Start with range [0, 1)
2. For each symbol, narrow range based on probability
3. Output bits as range narrows (renormalization)
4. Final number represents entire message

### Range Updates

For each symbol:
- Current range is [low, high)
- Symbol probability range is [symbol_low, symbol_high)
- New range = [low + range_size * symbol_low, low + range_size * symbol_high)

### Precision Handling

Since we can't use infinite precision:
- Use fixed-point arithmetic (32 or 64 bits)
- Renormalize when range gets too small
- Output bits during renormalization
- Handle underflow for range near boundaries

### Renormalization

Renormalization prevents precision loss:
- If range < 0.5: output 0, scale range
- If range >= 0.5: output 1, scale range
- If range in [0.25, 0.75): track underflow, scale range
- Continue until range is large enough

### Probability Model

Probability model manages symbol frequencies:
- Calculates cumulative probability ranges
- Updates frequencies dynamically
- Provides range lookup for encoding/decoding

### Time Complexity

- Encoding: O(n) where n = message length
- Decoding: O(n) where n = message length
- Model building: O(k log k) where k = alphabet size

### Space Complexity

- O(k) for probability model
- O(n) for encoded bits (in worst case)
- O(1) for range state (constant precision)

## Performance Considerations

- Precision bits: 32 is faster, 64 is more accurate
- For large files, consider:
  - Processing in blocks
  - Using adaptive probability models
  - Combining with other compression (LZ77, etc.)
- Arithmetic coding is typically slower than Huffman but achieves better compression

## Real-World Applications

- JPEG image compression (uses arithmetic coding)
- H.264 video compression
- High-performance compression libraries
- Information theory research
- Data compression systems
- Archival storage systems

## Comparison with Huffman Coding

### Advantages

- Better compression ratio (closer to entropy limit)
- Handles any probability distribution optimally
- No need for code lengths to be integers

### Disadvantages

- More complex implementation
- Slower encoding/decoding
- Requires probability model transmission
- More sensitive to precision issues

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

- Witten, I. H., Neal, R. M., & Cleary, J. G. (1987). Arithmetic coding for data compression.
- Used in JPEG, H.264, and other compression standards
- Foundation for many modern compression algorithms

## License

This project is part of the python-algorithms collection. See LICENSE file in parent directory for details.
