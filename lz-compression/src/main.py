"""LZ77 and LZ78 Compression Algorithms with Dictionary Management.

This module provides functionality to compress and decompress data using
LZ77 and LZ78 algorithms with configurable dictionary management.
"""

import logging
import logging.handlers
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class LZ77Compressor:
    """Implements LZ77 compression algorithm with sliding window."""

    def __init__(
        self,
        window_size: int = 4096,
        lookahead_size: int = 18,
        min_match_length: int = 3,
    ) -> None:
        """Initialize LZ77 compressor.

        Args:
            window_size: Size of search buffer (sliding window).
            lookahead_size: Size of look-ahead buffer.
            min_match_length: Minimum match length to encode.
        """
        self.window_size = window_size
        self.lookahead_size = lookahead_size
        self.min_match_length = min_match_length

    def compress(self, data: bytes) -> List[Tuple[int, int, Optional[int]]]:
        """Compress data using LZ77 algorithm.

        Args:
            data: Input data to compress.

        Returns:
            List of tuples (offset, length, next_char) where:
                - offset: Distance back in search buffer
                - length: Length of match
                - next_char: Next character after match (None if end)
        """
        compressed = []
        i = 0
        data_len = len(data)

        logger.info(f"Starting LZ77 compression: {data_len} bytes")

        while i < data_len:
            search_start = max(0, i - self.window_size)
            search_end = i
            lookahead_end = min(i + self.lookahead_size, data_len)

            search_buffer = data[search_start:search_end]
            lookahead_buffer = data[i:lookahead_end]

            best_match = self._find_longest_match(
                search_buffer, lookahead_buffer, search_start
            )

            if best_match and best_match[1] >= self.min_match_length:
                offset, length = best_match
                next_char_pos = i + length
                next_char = data[next_char_pos] if next_char_pos < data_len else None

                compressed.append((offset, length, next_char))
                i += length + 1

                logger.debug(
                    f"Match at position {i-length-1}: offset={offset}, "
                    f"length={length}, next_char={next_char}"
                )
            else:
                compressed.append((0, 0, data[i]))
                i += 1

        logger.info(f"Compression complete: {len(compressed)} tokens")
        return compressed

    def _find_longest_match(
        self, search_buffer: bytes, lookahead_buffer: bytes, search_start: int
    ) -> Optional[Tuple[int, int]]:
        """Find longest match in search buffer.

        Args:
            search_buffer: Search buffer to look in.
            lookahead_buffer: Look-ahead buffer to match.
            search_start: Start position of search buffer in original data.

        Returns:
            Tuple (offset, length) of best match, or None.
        """
        if not lookahead_buffer or not search_buffer:
            return None

        best_offset = 0
        best_length = 0

        for offset in range(len(search_buffer) - 1, -1, -1):
            length = 0
            while (
                length < len(lookahead_buffer)
                and offset + length < len(search_buffer)
                and search_buffer[offset + length] == lookahead_buffer[length]
            ):
                length += 1

            if length > best_length:
                best_length = length
                best_offset = len(search_buffer) - offset

        if best_length > 0:
            return (best_offset, best_length)
        return None

    def decompress(
        self, compressed: List[Tuple[int, int, Optional[int]]]
    ) -> bytes:
        """Decompress data using LZ77 algorithm.

        Args:
            compressed: List of (offset, length, next_char) tuples.

        Returns:
            Decompressed data as bytes.
        """
        decompressed = bytearray()
        data_len = 0

        logger.info(f"Starting LZ77 decompression: {len(compressed)} tokens")

        for offset, length, next_char in compressed:
            if length > 0:
                start_pos = len(decompressed) - offset
                for i in range(length):
                    if start_pos + i < len(decompressed):
                        decompressed.append(decompressed[start_pos + i])
                    else:
                        break

            if next_char is not None:
                decompressed.append(next_char)

            data_len += length + (1 if next_char is not None else 0)

        logger.info(f"Decompression complete: {len(decompressed)} bytes")
        return bytes(decompressed)


class LZ78Compressor:
    """Implements LZ78 compression algorithm with dictionary management."""

    def __init__(self, max_dict_size: int = 4096) -> None:
        """Initialize LZ78 compressor.

        Args:
            max_dict_size: Maximum dictionary size (0 = unlimited).
        """
        self.max_dict_size = max_dict_size

    def compress(self, data: bytes) -> List[Tuple[int, Optional[int]]]:
        """Compress data using LZ78 algorithm.

        Args:
            data: Input data to compress.

        Returns:
            List of tuples (dict_index, next_char) where:
                - dict_index: Index in dictionary (0 = empty string)
                - next_char: Next character (None if end)
        """
        compressed = []
        dictionary: Dict[bytes, int] = {b"": 0}
        current_string = b""
        next_index = 1
        i = 0
        data_len = len(data)

        logger.info(f"Starting LZ78 compression: {data_len} bytes")

        while i < data_len:
            current_string += bytes([data[i]])

            if current_string not in dictionary:
                parent_index = dictionary.get(current_string[:-1], 0)
                compressed.append((parent_index, data[i]))

                if (
                    self.max_dict_size == 0
                    or len(dictionary) < self.max_dict_size
                ):
                    dictionary[current_string] = next_index
                    next_index += 1

                logger.debug(
                    f"Position {i}: dict_index={parent_index}, "
                    f"next_char={data[i]}, new_dict_entry={current_string}"
                )

                current_string = b""
            i += 1

        if current_string:
            parent_index = dictionary.get(current_string[:-1], 0)
            if len(current_string) > 1:
                compressed.append((parent_index, current_string[-1]))
            else:
                compressed.append((0, current_string[0]))

        logger.info(
            f"Compression complete: {len(compressed)} tokens, "
            f"dictionary size={len(dictionary)}"
        )
        return compressed

    def decompress(
        self, compressed: List[Tuple[int, Optional[int]]]
    ) -> bytes:
        """Decompress data using LZ78 algorithm.

        Args:
            compressed: List of (dict_index, next_char) tuples.

        Returns:
            Decompressed data as bytes.
        """
        decompressed = bytearray()
        dictionary: Dict[int, bytes] = {0: b""}
        next_index = 1

        logger.info(f"Starting LZ78 decompression: {len(compressed)} tokens")

        for dict_index, next_char in compressed:
            if next_char is None:
                break

            if dict_index in dictionary:
                entry = dictionary[dict_index]
            else:
                entry = b""

            new_entry = entry + bytes([next_char])
            decompressed.extend(new_entry)

            if (
                self.max_dict_size == 0
                or len(dictionary) < self.max_dict_size
            ):
                dictionary[next_index] = new_entry
                next_index += 1

            logger.debug(
                f"dict_index={dict_index}, next_char={next_char}, "
                f"entry={new_entry}"
            )

        logger.info(
            f"Decompression complete: {len(decompressed)} bytes, "
            f"dictionary size={len(dictionary)}"
        )
        return bytes(decompressed)


class CompressionManager:
    """Manages compression operations with configuration."""

    def __init__(self, config_path: str = "config.yaml") -> None:
        """Initialize CompressionManager with configuration.

        Args:
            config_path: Path to configuration YAML file.

        Raises:
            FileNotFoundError: If config file doesn't exist.
            yaml.YAMLError: If config file is invalid YAML.
        """
        self.config = self._load_config(config_path)
        self._setup_logging()
        self._initialize_compressors()

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

    def _initialize_compressors(self) -> None:
        """Initialize compressors from configuration."""
        lz77_config = self.config.get("lz77", {})
        lz78_config = self.config.get("lz78", {})

        self.lz77 = LZ77Compressor(
            window_size=lz77_config.get("window_size", 4096),
            lookahead_size=lz77_config.get("lookahead_size", 18),
            min_match_length=lz77_config.get("min_match_length", 3),
        )

        self.lz78 = LZ78Compressor(
            max_dict_size=lz78_config.get("max_dict_size", 4096)
        )

    def compress_lz77(self, data: bytes) -> List[Tuple[int, int, Optional[int]]]:
        """Compress data using LZ77.

        Args:
            data: Input data to compress.

        Returns:
            Compressed tokens.
        """
        return self.lz77.compress(data)

    def decompress_lz77(
        self, compressed: List[Tuple[int, int, Optional[int]]]
    ) -> bytes:
        """Decompress data using LZ77.

        Args:
            compressed: Compressed tokens.

        Returns:
            Decompressed data.
        """
        return self.lz77.decompress(compressed)

    def compress_lz78(self, data: bytes) -> List[Tuple[int, Optional[int]]]:
        """Compress data using LZ78.

        Args:
            data: Input data to compress.

        Returns:
            Compressed tokens.
        """
        return self.lz78.compress(data)

    def decompress_lz78(
        self, compressed: List[Tuple[int, Optional[int]]]
    ) -> bytes:
        """Decompress data using LZ78.

        Args:
            compressed: Compressed tokens.

        Returns:
            Decompressed data.
        """
        return self.lz78.decompress(compressed)

    def get_compression_ratio(
        self, original_size: int, compressed_tokens: int, token_size: int = 3
    ) -> float:
        """Calculate compression ratio.

        Args:
            original_size: Size of original data.
            compressed_tokens: Number of compressed tokens.
            token_size: Size of each token in bytes.

        Returns:
            Compression ratio (original / compressed).
        """
        compressed_size = compressed_tokens * token_size
        if compressed_size == 0:
            return float("inf")
        return original_size / compressed_size


def main() -> None:
    """Main entry point for command-line usage."""
    import argparse

    parser = argparse.ArgumentParser(
        description="LZ77 and LZ78 Compression Algorithms"
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

    manager = CompressionManager(config_path=args.config)

    if args.test:
        logger.info("Running test compression")

        test_data = b"abracadabraabracadabra"
        print(f"\nOriginal data: {test_data}")
        print(f"Original size: {len(test_data)} bytes")

        print("\n=== LZ77 Compression ===")
        compressed_lz77 = manager.compress_lz77(test_data)
        print(f"Compressed tokens: {len(compressed_lz77)}")
        print(f"Compression ratio: {manager.get_compression_ratio(len(test_data), len(compressed_lz77)):.2f}")

        decompressed_lz77 = manager.decompress_lz77(compressed_lz77)
        print(f"Decompressed: {decompressed_lz77}")
        print(f"Match: {test_data == decompressed_lz77}")

        print("\n=== LZ78 Compression ===")
        compressed_lz78 = manager.compress_lz78(test_data)
        print(f"Compressed tokens: {len(compressed_lz78)}")
        print(f"Compression ratio: {manager.get_compression_ratio(len(test_data), len(compressed_lz78), 2):.2f}")

        decompressed_lz78 = manager.decompress_lz78(compressed_lz78)
        print(f"Decompressed: {decompressed_lz78}")
        print(f"Match: {test_data == decompressed_lz78}")


if __name__ == "__main__":
    main()
