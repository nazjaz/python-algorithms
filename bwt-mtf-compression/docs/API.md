# BWT+MTF Compression API Documentation

## Classes

### BurrowsWheelerTransform

Implements Burrows-Wheeler Transform.

#### Methods

##### `__init__()`

Initialize BWT transformer.

**Example:**
```python
bwt = BurrowsWheelerTransform()
```

##### `transform(data: bytes) -> Tuple[bytes, int]`

Apply Burrows-Wheeler Transform to data.

**Parameters:**
- `data` (bytes): Input data to transform

**Returns:**
- `Tuple[bytes, int]`: (transformed_data, original_index)

**Raises:**
- `ValueError`: If data is empty

**Example:**
```python
transformed, index = bwt.transform(b"banana")
```

##### `inverse_transform(transformed: bytes, original_index: int) -> bytes`

Apply inverse Burrows-Wheeler Transform.

**Parameters:**
- `transformed` (bytes): BWT transformed data
- `original_index` (int): Index of original string

**Returns:**
- `bytes`: Original data

**Raises:**
- `ValueError`: If parameters are invalid

**Example:**
```python
original = bwt.inverse_transform(transformed, index)
```

### MoveToFront

Implements Move-to-Front encoding and decoding.

#### Methods

##### `__init__(alphabet_size: int = 256)`

Initialize Move-to-Front encoder/decoder.

**Parameters:**
- `alphabet_size` (int): Size of alphabet (default 256 for bytes)

**Example:**
```python
mtf = MoveToFront(alphabet_size=256)
```

##### `encode(data: bytes) -> List[int]`

Encode data using Move-to-Front.

**Parameters:**
- `data` (bytes): Input data to encode

**Returns:**
- `List[int]`: List of indices (encoded symbols)

**Example:**
```python
encoded = mtf.encode(b"abc")
```

##### `decode(encoded: List[int]) -> bytes`

Decode data using Move-to-Front.

**Parameters:**
- `encoded` (List[int]): List of indices (encoded symbols)

**Returns:**
- `bytes`: Decoded data

**Raises:**
- `ValueError`: If index out of range

**Example:**
```python
decoded = mtf.decode(encoded)
```

### BWTMTFCompressor

Manages BWT+MTF compression operations with configuration.

#### Methods

##### `__init__(config_path: str = "config.yaml")`

Initialize BWTMTFCompressor with configuration.

**Parameters:**
- `config_path` (str): Path to configuration YAML file

**Raises:**
- `FileNotFoundError`: If config file doesn't exist
- `yaml.YAMLError`: If config file is invalid YAML

##### `compress(data: bytes) -> Tuple[List[int], int]`

Compress data using BWT + MTF.

**Parameters:**
- `data` (bytes): Input data to compress

**Returns:**
- `Tuple[List[int], int]`: (mtf_encoded, original_index)

**Raises:**
- `ValueError`: If data is empty

##### `decompress(mtf_encoded: List[int], original_index: int) -> bytes`

Decompress data using BWT + MTF.

**Parameters:**
- `mtf_encoded` (List[int]): MTF encoded indices
- `original_index` (int): BWT original index

**Returns:**
- `bytes`: Decompressed data

**Raises:**
- `ValueError`: If parameters are invalid

##### `get_compression_ratio(original_size: int, compressed_size: int) -> float`

Calculate compression ratio.

**Parameters:**
- `original_size` (int): Size of original data in bytes
- `compressed_size` (int): Size of compressed data (MTF indices)

**Returns:**
- `float`: Compression ratio (original / compressed)

## Configuration

### Configuration File Format

The algorithm uses YAML configuration files with the following structure:

```yaml
bwt_mtf:
  alphabet_size: 256

logging:
  level: "INFO"
  file: "logs/app.log"
```

### Configuration Parameters

- `alphabet_size` (int): Size of alphabet for MTF (256 for bytes)

## Examples

### Basic Compression

```python
from src.main import BWTMTFCompressor

compressor = BWTMTFCompressor()
data = b"abracadabra"

mtf_encoded, original_index = compressor.compress(data)
decompressed = compressor.decompress(mtf_encoded, original_index)
```

### Separate BWT and MTF

```python
from src.main import BurrowsWheelerTransform, MoveToFront

# BWT only
bwt = BurrowsWheelerTransform()
transformed, index = bwt.transform(b"banana")
original = bwt.inverse_transform(transformed, index)

# MTF only
mtf = MoveToFront()
encoded = mtf.encode(b"abc")
decoded = mtf.decode(encoded)
```

### Custom Configuration

```python
compressor = BWTMTFCompressor(config_path="custom_config.yaml")
mtf_encoded, original_index = compressor.compress(data)
```
