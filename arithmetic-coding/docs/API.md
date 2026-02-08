# Arithmetic Coding API Documentation

## Classes

### ProbabilityModel

Manages symbol probabilities for arithmetic coding.

#### Methods

##### `__init__(frequencies: Optional[Dict[int, int]] = None)`

Initialize probability model.

**Parameters:**
- `frequencies` (Optional[Dict[int, int]]): Dictionary mapping symbols to frequencies

**Example:**
```python
frequencies = {97: 5, 98: 2, 99: 1}
model = ProbabilityModel(frequencies)
```

##### `get_range(symbol: int) -> Tuple[float, float]`

Get probability range for symbol.

**Parameters:**
- `symbol` (int): Symbol to get range for

**Returns:**
- `Tuple[float, float]`: (low, high) probability range

**Raises:**
- `ValueError`: If symbol not in model

##### `get_symbol_for_value(value: float) -> int`

Get symbol for given probability value.

**Parameters:**
- `value` (float): Probability value (0.0 to 1.0)

**Returns:**
- `int`: Symbol corresponding to value

**Raises:**
- `ValueError`: If value out of range

##### `update_frequency(symbol: int, increment: int = 1) -> None`

Update frequency of symbol.

**Parameters:**
- `symbol` (int): Symbol to update
- `increment` (int): Amount to increment frequency

### ArithmeticEncoder

Implements arithmetic coding encoder.

#### Methods

##### `__init__(precision_bits: int = 32, model: Optional[ProbabilityModel] = None)`

Initialize arithmetic encoder.

**Parameters:**
- `precision_bits` (int): Number of bits for precision (32 or 64)
- `model` (Optional[ProbabilityModel]): Probability model

**Example:**
```python
encoder = ArithmeticEncoder(precision_bits=32)
```

##### `encode(data: bytes, model: Optional[ProbabilityModel] = None) -> Tuple[List[int], ProbabilityModel]`

Encode data using arithmetic coding.

**Parameters:**
- `data` (bytes): Input data to encode
- `model` (Optional[ProbabilityModel]): Probability model (if None, built from data)

**Returns:**
- `Tuple[List[int], ProbabilityModel]`: (encoded_bits, probability_model)

**Example:**
```python
encoded, model = encoder.encode(b"abc", model)
```

### ArithmeticDecoder

Implements arithmetic coding decoder.

#### Methods

##### `__init__(precision_bits: int = 32, model: Optional[ProbabilityModel] = None)`

Initialize arithmetic decoder.

**Parameters:**
- `precision_bits` (int): Number of bits for precision (32 or 64)
- `model` (Optional[ProbabilityModel]): Probability model

**Example:**
```python
decoder = ArithmeticDecoder(precision_bits=32)
```

##### `decode(encoded_bits: List[int], model: ProbabilityModel, length: int) -> bytes`

Decode data using arithmetic coding.

**Parameters:**
- `encoded_bits` (List[int]): Encoded bit sequence
- `model` (ProbabilityModel): Probability model used for encoding
- `length` (int): Length of original data

**Returns:**
- `bytes`: Decoded data

**Example:**
```python
decoded = decoder.decode(encoded, model, len(data))
```

### ArithmeticCodingManager

Manages arithmetic coding operations with configuration.

#### Methods

##### `__init__(config_path: str = "config.yaml")`

Initialize ArithmeticCodingManager with configuration.

**Parameters:**
- `config_path` (str): Path to configuration YAML file

**Raises:**
- `FileNotFoundError`: If config file doesn't exist
- `yaml.YAMLError`: If config file is invalid YAML

##### `compress(data: bytes, model: Optional[ProbabilityModel] = None) -> Tuple[List[int], ProbabilityModel, int]`

Compress data using arithmetic coding.

**Parameters:**
- `data` (bytes): Input data to compress
- `model` (Optional[ProbabilityModel]): Optional probability model

**Returns:**
- `Tuple[List[int], ProbabilityModel, int]`: (encoded_bits, model, original_length)

##### `decompress(encoded_bits: List[int], model: ProbabilityModel, length: int) -> bytes`

Decompress data using arithmetic coding.

**Parameters:**
- `encoded_bits` (List[int]): Encoded bit sequence
- `model` (ProbabilityModel): Probability model used for encoding
- `length` (int): Length of original data

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

The algorithm uses YAML configuration files with the following structure:

```yaml
arithmetic_coding:
  precision_bits: 32

logging:
  level: "INFO"
  file: "logs/app.log"
```

### Configuration Parameters

- `precision_bits` (int): Number of bits for precision (32 or 64)

## Examples

### Basic Compression

```python
from src.main import ArithmeticCodingManager

manager = ArithmeticCodingManager()
data = b"abracadabra"

encoded_bits, model, length = manager.compress(data)
decoded = manager.decompress(encoded_bits, model, length)
```

### Custom Probability Model

```python
from src.main import ArithmeticCodingManager, ProbabilityModel

frequencies = {97: 5, 98: 2, 99: 1}
model = ProbabilityModel(frequencies)

manager = ArithmeticCodingManager()
encoded_bits, model, length = manager.compress(data, model=model)
decoded = manager.decompress(encoded_bits, model, length)
```

### Direct Class Usage

```python
from src.main import ArithmeticEncoder, ArithmeticDecoder, ProbabilityModel
from collections import Counter

data = b"abracadabra"
frequencies = Counter(data)
model = ProbabilityModel(frequencies)

encoder = ArithmeticEncoder(precision_bits=32)
encoded, model = encoder.encode(data, model)

decoder = ArithmeticDecoder(precision_bits=32)
decoded = decoder.decode(encoded, model, len(data))
```
