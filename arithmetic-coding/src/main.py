"""Arithmetic Coding for Lossless Compression.

This module provides functionality to compress and decompress data using
arithmetic coding with precision handling and range updates.
"""

import logging
import logging.handlers
from collections import Counter
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class ProbabilityModel:
    """Manages symbol probabilities for arithmetic coding."""

    def __init__(self, frequencies: Optional[Dict[int, int]] = None) -> None:
        """Initialize probability model.

        Args:
            frequencies: Dictionary mapping symbols to frequencies.
        """
        if frequencies is None:
            frequencies = {}

        self.frequencies = frequencies.copy()
        self.total = sum(self.frequencies.values())
        self._update_cumulative()

    def _update_cumulative(self) -> None:
        """Update cumulative probability ranges."""
        self.cumulative: Dict[int, Tuple[float, float]] = {}
        cumulative = 0.0

        if self.total == 0:
            return

        sorted_symbols = sorted(self.frequencies.keys())
        for symbol in sorted_symbols:
            freq = self.frequencies[symbol]
            prob = freq / self.total
            self.cumulative[symbol] = (cumulative, cumulative + prob)
            cumulative += prob

    def get_range(self, symbol: int) -> Tuple[float, float]:
        """Get probability range for symbol.

        Args:
            symbol: Symbol to get range for.

        Returns:
            Tuple of (low, high) probability range.

        Raises:
            ValueError: If symbol not in model.
        """
        if symbol not in self.cumulative:
            raise ValueError(f"Symbol {symbol} not in probability model")
        return self.cumulative[symbol]

    def get_symbol_for_value(self, value: float) -> int:
        """Get symbol for given probability value.

        Args:
            value: Probability value (0.0 to 1.0).

        Returns:
            Symbol corresponding to value.

        Raises:
            ValueError: If value out of range.
        """
        if value < 0.0 or value > 1.0:
            raise ValueError(f"Value {value} out of range [0.0, 1.0]")

        for symbol, (low, high) in self.cumulative.items():
            if low <= value < high:
                return symbol

        sorted_symbols = sorted(self.cumulative.keys())
        if sorted_symbols:
            return sorted_symbols[-1]

        raise ValueError("No symbols in probability model")

    def update_frequency(self, symbol: int, increment: int = 1) -> None:
        """Update frequency of symbol.

        Args:
            symbol: Symbol to update.
            increment: Amount to increment frequency.
        """
        if symbol not in self.frequencies:
            self.frequencies[symbol] = 0
        self.frequencies[symbol] += increment
        self.total += increment
        self._update_cumulative()


class ArithmeticEncoder:
    """Implements arithmetic coding encoder."""

    def __init__(
        self,
        precision_bits: int = 32,
        model: Optional[ProbabilityModel] = None,
    ) -> None:
        """Initialize arithmetic encoder.

        Args:
            precision_bits: Number of bits for precision (32 or 64).
            model: Probability model (if None, will be built from data).
        """
        self.precision_bits = precision_bits
        self.max_value = (1 << precision_bits) - 1
        self.half = 1 << (precision_bits - 1)
        self.quarter = 1 << (precision_bits - 2)
        self.three_quarters = 3 * self.quarter

        self.model = model
        self.low = 0
        self.high = self.max_value
        self.underflow_bits = 0
        self.output_bits: List[int] = []

    def _scale_range(self, symbol_low: float, symbol_high: float) -> None:
        """Scale current range based on symbol probability.

        Args:
            symbol_low: Lower bound of symbol probability.
            symbol_high: Upper bound of symbol probability.
        """
        range_size = self.high - self.low + 1
        new_low = self.low + int(range_size * symbol_low)
        new_high = self.low + int(range_size * symbol_high) - 1

        self.low = new_low
        self.high = new_high

    def _renormalize(self) -> None:
        """Renormalize range to prevent underflow."""
        while True:
            if self.high < self.half:
                self._output_bit(0)
                for _ in range(self.underflow_bits):
                    self._output_bit(1)
                self.underflow_bits = 0
                self.low = self.low << 1
                self.high = (self.high << 1) | 1
            elif self.low >= self.half:
                self._output_bit(1)
                for _ in range(self.underflow_bits):
                    self._output_bit(0)
                self.underflow_bits = 0
                self.low = (self.low - self.half) << 1
                self.high = ((self.high - self.half) << 1) | 1
            elif self.low >= self.quarter and self.high < self.three_quarters:
                self.underflow_bits += 1
                self.low = (self.low - self.quarter) << 1
                self.high = ((self.high - self.quarter) << 1) | 1
            else:
                break

    def _output_bit(self, bit: int) -> None:
        """Output a bit.

        Args:
            bit: Bit value (0 or 1).
        """
        self.output_bits.append(bit)

    def encode(self, data: bytes, model: Optional[ProbabilityModel] = None) -> Tuple[List[int], ProbabilityModel]:
        """Encode data using arithmetic coding.

        Args:
            data: Input data to encode.
            model: Probability model (if None, built from data).

        Returns:
            Tuple of (encoded_bits, probability_model).
        """
        if model is None:
            if self.model is None:
                frequencies = Counter(data)
                model = ProbabilityModel(frequencies)
            else:
                model = self.model
        else:
            self.model = model

        self.low = 0
        self.high = self.max_value
        self.underflow_bits = 0
        self.output_bits = []

        logger.info(f"Starting arithmetic encoding: {len(data)} bytes")

        for symbol in data:
            symbol_low, symbol_high = model.get_range(symbol)
            self._scale_range(symbol_low, symbol_high)
            self._renormalize()

        self._finish_encoding()

        logger.info(
            f"Encoding complete: {len(self.output_bits)} bits "
            f"({len(self.output_bits)/8:.2f} bytes)"
        )

        return self.output_bits.copy(), model

    def _finish_encoding(self) -> None:
        """Finish encoding by outputting final bits."""
        self.underflow_bits += 1
        if self.low < self.quarter:
            self._output_bit(0)
            for _ in range(self.underflow_bits):
                self._output_bit(1)
        else:
            self._output_bit(1)
            for _ in range(self.underflow_bits):
                self._output_bit(0)


class ArithmeticDecoder:
    """Implements arithmetic coding decoder."""

    def __init__(
        self,
        precision_bits: int = 32,
        model: Optional[ProbabilityModel] = None,
    ) -> None:
        """Initialize arithmetic decoder.

        Args:
            precision_bits: Number of bits for precision (32 or 64).
            model: Probability model.
        """
        self.precision_bits = precision_bits
        self.max_value = (1 << precision_bits) - 1
        self.half = 1 << (precision_bits - 1)
        self.quarter = 1 << (precision_bits - 2)
        self.three_quarters = 3 * self.quarter

        self.model = model
        self.low = 0
        self.high = self.max_value
        self.value = 0
        self.input_bits: List[int] = []
        self.bit_index = 0

    def _scale_range(self, symbol_low: float, symbol_high: float) -> None:
        """Scale current range based on symbol probability.

        Args:
            symbol_low: Lower bound of symbol probability.
            symbol_high: Upper bound of symbol probability.
        """
        range_size = self.high - self.low + 1
        new_low = self.low + int(range_size * symbol_low)
        new_high = self.low + int(range_size * symbol_high) - 1

        self.low = new_low
        self.high = new_high

    def _renormalize(self) -> None:
        """Renormalize range and update value."""
        while True:
            if self.high < self.half:
                self.low = self.low << 1
                self.high = (self.high << 1) | 1
                self.value = (self.value << 1) | self._read_bit()
            elif self.low >= self.half:
                self.low = (self.low - self.half) << 1
                self.high = ((self.high - self.half) << 1) | 1
                self.value = ((self.value - self.half) << 1) | self._read_bit()
            elif self.low >= self.quarter and self.high < self.three_quarters:
                self.low = (self.low - self.quarter) << 1
                self.high = ((self.high - self.quarter) << 1) | 1
                self.value = ((self.value - self.quarter) << 1) | self._read_bit()
            else:
                break

    def _read_bit(self) -> int:
        """Read next bit from input.

        Returns:
            Bit value (0 or 1), or 0 if end of input.
        """
        if self.bit_index < len(self.input_bits):
            bit = self.input_bits[self.bit_index]
            self.bit_index += 1
            return bit
        return 0

    def decode(
        self,
        encoded_bits: List[int],
        model: ProbabilityModel,
        length: int,
    ) -> bytes:
        """Decode data using arithmetic coding.

        Args:
            encoded_bits: Encoded bit sequence.
            model: Probability model used for encoding.
            length: Length of original data.

        Returns:
            Decoded data as bytes.
        """
        self.model = model
        self.input_bits = encoded_bits.copy()
        self.bit_index = 0
        self.low = 0
        self.high = self.max_value
        self.value = 0

        for _ in range(self.precision_bits):
            self.value = (self.value << 1) | self._read_bit()

        decoded = []

        logger.info(f"Starting arithmetic decoding: {length} symbols expected")

        for _ in range(length):
            range_size = self.high - self.low + 1
            value_in_range = (self.value - self.low) / range_size

            symbol = model.get_symbol_for_value(value_in_range)
            decoded.append(symbol)

            symbol_low, symbol_high = model.get_range(symbol)
            self._scale_range(symbol_low, symbol_high)
            self._renormalize()

        logger.info(f"Decoding complete: {len(decoded)} bytes")
        return bytes(decoded)


class ArithmeticCodingManager:
    """Manages arithmetic coding operations with configuration."""

    def __init__(self, config_path: str = "config.yaml") -> None:
        """Initialize ArithmeticCodingManager with configuration.

        Args:
            config_path: Path to configuration YAML file.

        Raises:
            FileNotFoundError: If config file doesn't exist.
            yaml.YAMLError: If config file is invalid YAML.
        """
        self.config = self._load_config(config_path)
        self._setup_logging()
        self._initialize_parameters()

    def _load_config(self, config_path: str) -> dict:
        """Load configuration from YAML file.

        Args:
            config_path: Path to configuration file.

        Returns:
            Dictionary containing configuration settings.

        Raises:
            FileNotFoundError: If config file doesn't exist.
            yaml.YAMLError: If config file is invalid YAML.
        """
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
            if not config:
                raise ValueError("Configuration file is empty")
            return config
        except FileNotFoundError:
            logger.error(f"Configuration file not found: {config_path}")
            raise
        except yaml.YAMLError as e:
            logger.error(f"Invalid YAML in configuration file: {e}")
            raise

    def _setup_logging(self) -> None:
        """Configure logging based on configuration settings."""
        log_level = self.config.get("logging", {}).get("level", "INFO")
        log_file = self.config.get("logging", {}).get("file", "logs/app.log")
        log_format = (
            "%(asctime)s - %(name)s - %(levelname)s - " "%(message)s"
        )

        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        logging.basicConfig(
            level=getattr(logging, log_level.upper()),
            format=log_format,
            handlers=[
                logging.handlers.RotatingFileHandler(
                    log_file, maxBytes=10485760, backupCount=5
                ),
                logging.StreamHandler(),
            ],
        )

    def _initialize_parameters(self) -> None:
        """Initialize algorithm parameters from configuration."""
        ac_config = self.config.get("arithmetic_coding", {})
        self.precision_bits = ac_config.get("precision_bits", 32)

    def compress(
        self,
        data: bytes,
        model: Optional[ProbabilityModel] = None,
    ) -> Tuple[List[int], ProbabilityModel, int]:
        """Compress data using arithmetic coding.

        Args:
            data: Input data to compress.
            model: Optional probability model (if None, built from data).

        Returns:
            Tuple of (encoded_bits, probability_model, original_length).
        """
        encoder = ArithmeticEncoder(
            precision_bits=self.precision_bits, model=model
        )
        encoded_bits, model = encoder.encode(data, model)
        return encoded_bits, model, len(data)

    def decompress(
        self,
        encoded_bits: List[int],
        model: ProbabilityModel,
        length: int,
    ) -> bytes:
        """Decompress data using arithmetic coding.

        Args:
            encoded_bits: Encoded bit sequence.
            model: Probability model used for encoding.
            length: Length of original data.

        Returns:
            Decoded data as bytes.
        """
        decoder = ArithmeticDecoder(
            precision_bits=self.precision_bits, model=model
        )
        return decoder.decode(encoded_bits, model, length)

    def get_compression_ratio(
        self, original_size: int, compressed_bits: int
    ) -> float:
        """Calculate compression ratio.

        Args:
            original_size: Size of original data in bytes.
            compressed_bits: Size of compressed data in bits.

        Returns:
            Compression ratio (original / compressed).
        """
        compressed_bytes = (compressed_bits + 7) // 8
        if compressed_bytes == 0:
            return float("inf")
        return original_size / compressed_bytes


def main() -> None:
    """Main entry point for command-line usage."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Arithmetic Coding for Lossless Compression"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="config.yaml",
        help="Path to configuration file",
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Run test compression",
    )

    args = parser.parse_args()

    manager = ArithmeticCodingManager(config_path=args.config)

    if args.test:
        logger.info("Running test compression")

        test_data = b"abracadabra"
        print(f"\nOriginal data: {test_data}")
        print(f"Original size: {len(test_data)} bytes")

        encoded_bits, model, length = manager.compress(test_data)
        print(f"\nEncoded bits: {len(encoded_bits)} bits ({len(encoded_bits)/8:.2f} bytes)")
        print(f"Compression ratio: {manager.get_compression_ratio(len(test_data), len(encoded_bits)):.2f}")

        decoded = manager.decompress(encoded_bits, model, length)
        print(f"Decoded: {decoded}")
        print(f"Match: {test_data == decoded}")


if __name__ == "__main__":
    main()
