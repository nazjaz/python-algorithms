# Huffman Coding API Documentation

## Classes

### StandardHuffman

Implements standard Huffman coding with tree building.

#### Methods

##### `__init__()`

Initialize standard Huffman coder.

**Example:**
```python
huffman = StandardHuffman()
```

##### `build_tree(frequencies: Dict[int, int]) -> None`

Build Huffman tree from symbol frequencies.

**Parameters:**
- `frequencies` (Dict[int, int]): Dictionary mapping symbols to frequencies

**Example:**
```python
frequencies = {97: 5, 98: 2, 99: 1}
huffman.build_tree(frequencies)
```

##### `encode(data: bytes) -> Tuple[str, Dict[int, str]]`

Encode data using Huffman codes.

**Parameters:**
- `data` (bytes): Input data to encode

**Returns:**
- `Tuple[str, Dict[int, str]]`: (encoded_bits, codes_dict)

**Raises:**
- `ValueError`: If tree not built or symbol not in tree

**Example:**
```python
encoded, codes = huffman.encode(b"abc")
```

##### `decode(encoded_bits: str) -> bytes`

Decode data using Huffman codes.

**Parameters:**
- `encoded_bits` (str): Encoded bit string

**Returns:**
- `bytes`: Decoded data

**Raises:**
- `ValueError`: If tree not built or invalid code

**Example:**
```python
decoded = huffman.decode(encoded)
```

### CanonicalHuffman

Implements canonical Huffman coding.

#### Methods

##### `__init__()`

Initialize canonical Huffman coder.

**Example:**
```python
canonical = CanonicalHuffman()
```

##### `build_from_lengths(code_lengths: Dict[int, int]) -> None`

Build canonical codes from code lengths.

**Parameters:**
- `code_lengths` (Dict[int, int]): Dictionary mapping symbols to code lengths

**Example:**
```python
code_lengths = {97: 2, 98: 2, 99: 2}
canonical.build_from_lengths(code_lengths)
```

##### `build_from_standard(standard_huffman: StandardHuffman) -> None`

Build canonical codes from standard Huffman tree.

**Parameters:**
- `standard_huffman` (StandardHuffman): StandardHuffman instance with built tree

**Example:**
```python
canonical.build_from_standard(huffman)
```

##### `encode(data: bytes) -> Tuple[str, Dict[int, int]]`

Encode data using canonical Huffman codes.

**Parameters:**
- `data` (bytes): Input data to encode

**Returns:**
- `Tuple[str, Dict[int, int]]`: (encoded_bits, code_lengths_dict)

**Raises:**
- `ValueError`: If codes not built or symbol not in codes

##### `decode(encoded_bits: str) -> bytes`

Decode data using canonical Huffman codes.

**Parameters:**
- `encoded_bits` (str): Encoded bit string

**Returns:**
- `bytes`: Decoded data

**Raises:**
- `ValueError`: If codes not built or invalid code

### AdaptiveHuffman

Implements adaptive Huffman coding (FGK algorithm).

#### Methods

##### `__init__()`

Initialize adaptive Huffman coder.

**Example:**
```python
adaptive = AdaptiveHuffman()
```

##### `encode(data: bytes) -> str`

Encode data using adaptive Huffman coding.

**Parameters:**
- `data` (bytes): Input data to encode

**Returns:**
- `str`: Encoded bit string

**Example:**
```python
encoded = adaptive.encode(b"abc")
```

##### `decode(encoded_bits: str) -> bytes`

Decode data using adaptive Huffman coding.

**Parameters:**
- `encoded_bits` (str): Encoded bit string

**Returns:**
- `bytes`: Decoded data

**Example:**
```python
decoded = adaptive.decode(encoded)
```

### HuffmanCodingManager

Manages Huffman coding operations with configuration.

#### Methods

##### `__init__(config_path: str = "config.yaml")`

Initialize HuffmanCodingManager with configuration.

**Parameters:**
- `config_path` (str): Path to configuration YAML file

**Raises:**
- `FileNotFoundError`: If config file doesn't exist
- `yaml.YAMLError`: If config file is invalid YAML

##### `compress_standard(data: bytes) -> Tuple[str, Dict[int, str]]`

Compress data using standard Huffman coding.

**Parameters:**
- `data` (bytes): Input data to compress

**Returns:**
- `Tuple[str, Dict[int, str]]`: (encoded_bits, codes_dict)

##### `decompress_standard(encoded_bits: str, codes: Dict[int, str]) -> bytes`

Decompress data using standard Huffman coding.

**Parameters:**
- `encoded_bits` (str): Encoded bit string
- `codes` (Dict[int, str]): Huffman codes dictionary

**Returns:**
- `bytes`: Decoded data

##### `compress_canonical(data: bytes) -> Tuple[str, Dict[int, int]]`

Compress data using canonical Huffman coding.

**Parameters:**
- `data` (bytes): Input data to compress

**Returns:**
- `Tuple[str, Dict[int, int]]`: (encoded_bits, code_lengths_dict)

##### `decompress_canonical(encoded_bits: str, code_lengths: Dict[int, int]) -> bytes`

Decompress data using canonical Huffman coding.

**Parameters:**
- `encoded_bits` (str): Encoded bit string
- `code_lengths` (Dict[int, int]): Code lengths dictionary

**Returns:**
- `bytes`: Decoded data

##### `compress_adaptive(data: bytes) -> str`

Compress data using adaptive Huffman coding.

**Parameters:**
- `data` (bytes): Input data to compress

**Returns:**
- `str`: Encoded bit string

##### `decompress_adaptive(encoded_bits: str) -> bytes`

Decompress data using adaptive Huffman coding.

**Parameters:**
- `encoded_bits` (str): Encoded bit string

**Returns:**
- `bytes`: Decoded data

##### `get_compression_ratio(original_size: int, compressed_bits: int) -> float`

Calculate compression ratio.

**Parameters:**
- `original_size` (int): Size of original data in bytes
- `compressed_bits` (int): Size of compressed data in bits

**Returns:**
- `float`: Compression ratio (original / compressed)

## Configuration

### Configuration File Format

The algorithms use YAML configuration files with the following structure:

```yaml
logging:
  level: "INFO"
  file: "logs/app.log"
```

## Examples

### Standard Huffman

```python
from src.main import HuffmanCodingManager

manager = HuffmanCodingManager()
data = b"abracadabra"

encoded, codes = manager.compress_standard(data)
decoded = manager.decompress_standard(encoded, codes)
```

### Canonical Huffman

```python
encoded, lengths = manager.compress_canonical(data)
decoded = manager.decompress_canonical(encoded, lengths)
```

### Adaptive Huffman

```python
encoded = manager.compress_adaptive(data)
decoded = manager.decompress_adaptive(encoded)
```
