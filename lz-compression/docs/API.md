# LZ77 and LZ78 Compression API Documentation

## Classes

### LZ77Compressor

Implements LZ77 compression algorithm with sliding window.

#### Methods

##### `__init__(window_size=4096, lookahead_size=18, min_match_length=3)`

Initialize LZ77 compressor.

**Parameters:**
- `window_size` (int): Size of search buffer (sliding window)
- `lookahead_size` (int): Size of look-ahead buffer
- `min_match_length` (int): Minimum match length to encode

**Example:**
```python
compressor = LZ77Compressor(window_size=4096, lookahead_size=18)
```

##### `compress(data: bytes) -> List[Tuple[int, int, Optional[int]]]`

Compress data using LZ77 algorithm.

**Parameters:**
- `data` (bytes): Input data to compress

**Returns:**
- `List[Tuple[int, int, Optional[int]]]`: List of (offset, length, next_char) tuples

**Example:**
```python
compressed = compressor.compress(b"abracadabra")
```

##### `decompress(compressed: List[Tuple[int, int, Optional[int]]]) -> bytes`

Decompress data using LZ77 algorithm.

**Parameters:**
- `compressed` (List[Tuple[int, int, Optional[int]]]): Compressed tokens

**Returns:**
- `bytes`: Decompressed data

**Example:**
```python
decompressed = compressor.decompress(compressed)
```

### LZ78Compressor

Implements LZ78 compression algorithm with dictionary management.

#### Methods

##### `__init__(max_dict_size=4096)`

Initialize LZ78 compressor.

**Parameters:**
- `max_dict_size` (int): Maximum dictionary size (0 = unlimited)

**Example:**
```python
compressor = LZ78Compressor(max_dict_size=4096)
```

##### `compress(data: bytes) -> List[Tuple[int, Optional[int]]]`

Compress data using LZ78 algorithm.

**Parameters:**
- `data` (bytes): Input data to compress

**Returns:**
- `List[Tuple[int, Optional[int]]]`: List of (dict_index, next_char) tuples

**Example:**
```python
compressed = compressor.compress(b"abracadabra")
```

##### `decompress(compressed: List[Tuple[int, Optional[int]]]) -> bytes`

Decompress data using LZ78 algorithm.

**Parameters:**
- `compressed` (List[Tuple[int, Optional[int]]]): Compressed tokens

**Returns:**
- `bytes`: Decompressed data

**Example:**
```python
decompressed = compressor.decompress(compressed)
```

### CompressionManager

Manages compression operations with configuration.

#### Methods

##### `__init__(config_path: str = "config.yaml")`

Initialize CompressionManager with configuration.

**Parameters:**
- `config_path` (str): Path to configuration YAML file

**Raises:**
- `FileNotFoundError`: If config file doesn't exist
- `yaml.YAMLError`: If config file is invalid YAML

**Example:**
```python
manager = CompressionManager(config_path="config.yaml")
```

##### `compress_lz77(data: bytes) -> List[Tuple[int, int, Optional[int]]]`

Compress data using LZ77.

**Parameters:**
- `data` (bytes): Input data to compress

**Returns:**
- `List[Tuple[int, int, Optional[int]]]`: Compressed tokens

##### `decompress_lz77(compressed: List[Tuple[int, int, Optional[int]]]) -> bytes`

Decompress data using LZ77.

**Parameters:**
- `compressed` (List[Tuple[int, int, Optional[int]]]): Compressed tokens

**Returns:**
- `bytes`: Decompressed data

##### `compress_lz78(data: bytes) -> List[Tuple[int, Optional[int]]]`

Compress data using LZ78.

**Parameters:**
- `data` (bytes): Input data to compress

**Returns:**
- `List[Tuple[int, Optional[int]]]`: Compressed tokens

##### `decompress_lz78(compressed: List[Tuple[int, Optional[int]]]) -> bytes`

Decompress data using LZ78.

**Parameters:**
- `compressed` (List[Tuple[int, Optional[int]]]): Compressed tokens

**Returns:**
- `bytes`: Decompressed data

##### `get_compression_ratio(original_size: int, compressed_tokens: int, token_size: int = 3) -> float`

Calculate compression ratio.

**Parameters:**
- `original_size` (int): Size of original data
- `compressed_tokens` (int): Number of compressed tokens
- `token_size` (int): Size of each token in bytes

**Returns:**
- `float`: Compression ratio (original / compressed)

## Configuration

### Configuration File Format

The algorithms use YAML configuration files with the following structure:

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

### Configuration Parameters

- `window_size` (int): LZ77 search buffer size
- `lookahead_size` (int): LZ77 look-ahead buffer size
- `min_match_length` (int): LZ77 minimum match length
- `max_dict_size` (int): LZ78 maximum dictionary size (0 = unlimited)

## Examples

### Basic Compression

```python
from src.main import CompressionManager

manager = CompressionManager()
data = b"abracadabra"

# LZ77
compressed_lz77 = manager.compress_lz77(data)
decompressed_lz77 = manager.decompress_lz77(compressed_lz77)

# LZ78
compressed_lz78 = manager.compress_lz78(data)
decompressed_lz78 = manager.decompress_lz78(compressed_lz78)
```

### Custom Configuration

```python
manager = CompressionManager(config_path="custom_config.yaml")
compressed = manager.compress_lz77(data)
```

### Direct Compressor Usage

```python
from src.main import LZ77Compressor, LZ78Compressor

lz77 = LZ77Compressor(window_size=1000, lookahead_size=10)
compressed = lz77.compress(data)
decompressed = lz77.decompress(compressed)

lz78 = LZ78Compressor(max_dict_size=2000)
compressed = lz78.compress(data)
decompressed = lz78.decompress(compressed)
```
