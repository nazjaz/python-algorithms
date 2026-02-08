"""Burrows-Wheeler Transform with Move-to-Front Encoding.

This module provides functionality to compress data using Burrows-Wheeler
Transform (BWT) combined with Move-to-Front (MTF) encoding.
"""

import logging
import logging.handlers
from pathlib import Path
from typing import List, Optional, Tuple

import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class BurrowsWheelerTransform:
    """Implements Burrows-Wheeler Transform."""

    def __init__(self) -> None:
        """Initialize BWT transformer."""
        pass

    def transform(self, data: bytes) -> Tuple[bytes, int]:
        """Apply Burrows-Wheeler Transform to data.

        Args:
            data: Input data to transform.

        Returns:
            Tuple of (transformed_data, original_index) where:
                - transformed_data: BWT output
                - original_index: Index of original string in sorted rotations

        Raises:
            ValueError: If data is empty.
        """
        if not data:
            raise ValueError("Cannot transform empty data")

        data_list = list(data)
        rotations = []

        for i in range(len(data_list)):
            rotation = data_list[i:] + data_list[:i]
            rotations.append((rotation, i))

        rotations.sort(key=lambda x: tuple(x[0]))

        transformed = bytearray()
        original_index = -1

        for i, (rotation, orig_idx) in enumerate(rotations):
            transformed.append(rotation[-1])
            if orig_idx == 0:
                original_index = i

        logger.debug(
            f"BWT transform: input_length={len(data)}, "
            f"original_index={original_index}"
        )

        return bytes(transformed), original_index

    def inverse_transform(self, transformed: bytes, original_index: int) -> bytes:
        """Apply inverse Burrows-Wheeler Transform.

        Uses the last-first property for efficient reconstruction.

        Args:
            transformed: BWT transformed data.
            original_index: Index of original string in sorted rotations.

        Returns:
            Original data.

        Raises:
            ValueError: If parameters are invalid.
        """
        if not transformed:
            raise ValueError("Cannot inverse transform empty data")
        if original_index < 0 or original_index >= len(transformed):
            raise ValueError(
                f"Original index {original_index} out of range "
                f"[0, {len(transformed)})"
            )

        if len(transformed) == 1:
            return transformed

        first_column = sorted(transformed)
        last_column = list(transformed)

        next_index = {}
        first_occurrence = {}
        for i, char in enumerate(first_column):
            if char not in first_occurrence:
                first_occurrence[char] = i

        char_counts = {}
        for i, char in enumerate(last_column):
            if char not in char_counts:
                char_counts[char] = 0
            next_index[i] = first_occurrence[char] + char_counts[char]
            char_counts[char] += 1

        original = bytearray()
        current_index = original_index

        for _ in range(len(transformed)):
            original.append(first_column[current_index])
            current_index = next_index[current_index]

        original.reverse()

        logger.debug(
            f"BWT inverse transform: output_length={len(original)}, "
            f"original_index={original_index}"
        )

        return bytes(original)


class MoveToFront:
    """Implements Move-to-Front encoding and decoding."""

    def __init__(self, alphabet_size: int = 256) -> None:
        """Initialize Move-to-Front encoder/decoder.

        Args:
            alphabet_size: Size of alphabet (default 256 for bytes).
        """
        self.alphabet_size = alphabet_size
        self.alphabet = list(range(alphabet_size))

    def encode(self, data: bytes) -> List[int]:
        """Encode data using Move-to-Front.

        Args:
            data: Input data to encode.

        Returns:
            List of indices (encoded symbols).
        """
        encoded = []
        alphabet = self.alphabet.copy()

        for symbol in data:
            index = alphabet.index(symbol)
            encoded.append(index)

            alphabet.pop(index)
            alphabet.insert(0, symbol)

        logger.debug(
            f"MTF encode: input_length={len(data)}, "
            f"output_length={len(encoded)}"
        )

        return encoded

    def decode(self, encoded: List[int]) -> bytes:
        """Decode data using Move-to-Front.

        Args:
            encoded: List of indices (encoded symbols).

        Returns:
            Decoded data as bytes.
        """
        decoded = bytearray()
        alphabet = self.alphabet.copy()

        for index in encoded:
            if index < 0 or index >= len(alphabet):
                raise ValueError(
                    f"Index {index} out of range [0, {len(alphabet)})"
                )

            symbol = alphabet[index]
            decoded.append(symbol)

            alphabet.pop(index)
            alphabet.insert(0, symbol)

        logger.debug(
            f"MTF decode: input_length={len(encoded)}, "
            f"output_length={len(decoded)}"
        )

        return bytes(decoded)


class BWTMTFCompressor:
    """Implements compression using BWT + MTF."""

    def __init__(self, config_path: str = "config.yaml") -> None:
        """Initialize BWT+MTF compressor with configuration.

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
        bwt_mtf_config = self.config.get("bwt_mtf", {})
        self.alphabet_size = bwt_mtf_config.get("alphabet_size", 256)

        self.bwt = BurrowsWheelerTransform()
        self.mtf = MoveToFront(alphabet_size=self.alphabet_size)

    def compress(self, data: bytes) -> Tuple[List[int], int]:
        """Compress data using BWT + MTF.

        Args:
            data: Input data to compress.

        Returns:
            Tuple of (mtf_encoded, original_index) where:
                - mtf_encoded: MTF encoded indices
                - original_index: BWT original index

        Raises:
            ValueError: If data is empty.
        """
        if not data:
            raise ValueError("Cannot compress empty data")

        logger.info(f"Starting BWT+MTF compression: {len(data)} bytes")

        bwt_output, original_index = self.bwt.transform(data)
        mtf_encoded = self.mtf.encode(bwt_output)

        logger.info(
            f"Compression complete: mtf_length={len(mtf_encoded)}, "
            f"original_index={original_index}"
        )

        return mtf_encoded, original_index

    def decompress(self, mtf_encoded: List[int], original_index: int) -> bytes:
        """Decompress data using BWT + MTF.

        Args:
            mtf_encoded: MTF encoded indices.
            original_index: BWT original index.

        Returns:
            Decompressed data as bytes.

        Raises:
            ValueError: If parameters are invalid.
        """
        if not mtf_encoded:
            raise ValueError("Cannot decompress empty data")

        logger.info(
            f"Starting BWT+MTF decompression: mtf_length={len(mtf_encoded)}, "
            f"original_index={original_index}"
        )

        bwt_output = self.mtf.decode(mtf_encoded)
        original = self.bwt.inverse_transform(bwt_output, original_index)

        logger.info(f"Decompression complete: {len(original)} bytes")

        return original

    def get_compression_ratio(
        self, original_size: int, compressed_size: int
    ) -> float:
        """Calculate compression ratio.

        Args:
            original_size: Size of original data in bytes.
            compressed_size: Size of compressed data (MTF indices).

        Returns:
            Compression ratio (original / compressed).
        """
        if compressed_size == 0:
            return float("inf")
        return original_size / compressed_size


def main() -> None:
    """Main entry point for command-line usage."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Burrows-Wheeler Transform with Move-to-Front Encoding"
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

    compressor = BWTMTFCompressor(config_path=args.config)

    if args.test:
        logger.info("Running test compression")

        test_data = b"abracadabra"
        print(f"\nOriginal data: {test_data}")
        print(f"Original size: {len(test_data)} bytes")

        mtf_encoded, original_index = compressor.compress(test_data)
        print(f"\nCompression Results:")
        print(f"MTF encoded length: {len(mtf_encoded)}")
        print(f"Original index: {original_index}")
        print(f"Compression ratio: {compressor.get_compression_ratio(len(test_data), len(mtf_encoded)):.2f}")

        decompressed = compressor.decompress(mtf_encoded, original_index)
        print(f"\nDecompressed: {decompressed}")
        print(f"Match: {test_data == decompressed}")


if __name__ == "__main__":
    main()
