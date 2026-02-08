"""Unit tests for LZ77 and LZ78 compression implementation."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import (
    CompressionManager,
    LZ77Compressor,
    LZ78Compressor,
)


class TestLZ77Compressor:
    """Test LZ77 compression functionality."""

    def test_compression_simple(self):
        """Test simple LZ77 compression."""
        compressor = LZ77Compressor(window_size=10, lookahead_size=5)
        data = b"hello"
        compressed = compressor.compress(data)
        assert len(compressed) > 0

    def test_decompression_simple(self):
        """Test simple LZ77 decompression."""
        compressor = LZ77Compressor(window_size=10, lookahead_size=5)
        data = b"hello"
        compressed = compressor.compress(data)
        decompressed = compressor.decompress(compressed)
        assert decompressed == data

    def test_compression_repetitive(self):
        """Test LZ77 compression on repetitive data."""
        compressor = LZ77Compressor(window_size=20, lookahead_size=10)
        data = b"abracadabraabracadabra"
        compressed = compressor.compress(data)
        decompressed = compressor.decompress(compressed)
        assert decompressed == data

    def test_compression_empty(self):
        """Test LZ77 compression on empty data."""
        compressor = LZ77Compressor()
        data = b""
        compressed = compressor.compress(data)
        decompressed = compressor.decompress(compressed)
        assert decompressed == data

    def test_compression_single_char(self):
        """Test LZ77 compression on single character."""
        compressor = LZ77Compressor()
        data = b"a"
        compressed = compressor.compress(data)
        decompressed = compressor.decompress(compressed)
        assert decompressed == data

    def test_compression_no_repetition(self):
        """Test LZ77 compression on non-repetitive data."""
        compressor = LZ77Compressor()
        data = b"abcdefghijklmnopqrstuvwxyz"
        compressed = compressor.compress(data)
        decompressed = compressor.decompress(compressed)
        assert decompressed == data

    def test_compression_long_match(self):
        """Test LZ77 compression with long matches."""
        compressor = LZ77Compressor(window_size=100, lookahead_size=50)
        data = b"hello" * 10
        compressed = compressor.compress(data)
        decompressed = compressor.decompress(compressed)
        assert decompressed == data

    def test_min_match_length(self):
        """Test LZ77 with different min_match_length."""
        compressor = LZ77Compressor(min_match_length=5)
        data = b"ababababab"
        compressed = compressor.compress(data)
        decompressed = compressor.decompress(compressed)
        assert decompressed == data

    def test_window_size_limits(self):
        """Test LZ77 with different window sizes."""
        for window_size in [10, 100, 1000]:
            compressor = LZ77Compressor(window_size=window_size)
            data = b"test data with repetition test data"
            compressed = compressor.compress(data)
            decompressed = compressor.decompress(compressed)
            assert decompressed == data

    def test_binary_data(self):
        """Test LZ77 compression on binary data."""
        compressor = LZ77Compressor()
        data = bytes(range(256))
        compressed = compressor.compress(data)
        decompressed = compressor.decompress(compressed)
        assert decompressed == data


class TestLZ78Compressor:
    """Test LZ78 compression functionality."""

    def test_compression_simple(self):
        """Test simple LZ78 compression."""
        compressor = LZ78Compressor()
        data = b"hello"
        compressed = compressor.compress(data)
        assert len(compressed) > 0

    def test_decompression_simple(self):
        """Test simple LZ78 decompression."""
        compressor = LZ78Compressor()
        data = b"hello"
        compressed = compressor.compress(data)
        decompressed = compressor.decompress(compressed)
        assert decompressed == data

    def test_compression_repetitive(self):
        """Test LZ78 compression on repetitive data."""
        compressor = LZ78Compressor()
        data = b"abracadabra"
        compressed = compressor.compress(data)
        decompressed = compressor.decompress(compressed)
        assert decompressed == data

    def test_compression_empty(self):
        """Test LZ78 compression on empty data."""
        compressor = LZ78Compressor()
        data = b""
        compressed = compressor.compress(data)
        decompressed = compressor.decompress(compressed)
        assert decompressed == data

    def test_compression_single_char(self):
        """Test LZ78 compression on single character."""
        compressor = LZ78Compressor()
        data = b"a"
        compressed = compressor.compress(data)
        decompressed = compressor.decompress(compressed)
        assert decompressed == data

    def test_compression_no_repetition(self):
        """Test LZ78 compression on non-repetitive data."""
        compressor = LZ78Compressor()
        data = b"abcdefghijklmnopqrstuvwxyz"
        compressed = compressor.compress(data)
        decompressed = compressor.decompress(compressed)
        assert decompressed == data

    def test_max_dict_size(self):
        """Test LZ78 with max_dict_size limit."""
        compressor = LZ78Compressor(max_dict_size=10)
        data = b"abracadabraabracadabra"
        compressed = compressor.compress(data)
        decompressed = compressor.decompress(compressed)
        assert decompressed == data

    def test_unlimited_dict(self):
        """Test LZ78 with unlimited dictionary."""
        compressor = LZ78Compressor(max_dict_size=0)
        data = b"abracadabraabracadabra"
        compressed = compressor.compress(data)
        decompressed = compressor.decompress(compressed)
        assert decompressed == data

    def test_dictionary_building(self):
        """Test that LZ78 builds dictionary correctly."""
        compressor = LZ78Compressor()
        data = b"abababab"
        compressed = compressor.compress(data)
        decompressed = compressor.decompress(compressed)
        assert decompressed == data

    def test_binary_data(self):
        """Test LZ78 compression on binary data."""
        compressor = LZ78Compressor()
        data = bytes(range(256))
        compressed = compressor.compress(data)
        decompressed = compressor.decompress(compressed)
        assert decompressed == data


class TestCompressionManager:
    """Test CompressionManager functionality."""

    def create_temp_config(self, config_dict: dict) -> str:
        """Create temporary config file for testing."""
        temp_file = tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False
        )
        yaml.dump(config_dict, temp_file)
        temp_file.close()
        return temp_file.name

    def test_initialization_with_default_config(self):
        """Test initialization with default config file."""
        manager = CompressionManager()
        assert manager.lz77 is not None
        assert manager.lz78 is not None

    def test_initialization_with_custom_config(self):
        """Test initialization with custom config file."""
        config = {
            "lz77": {
                "window_size": 1000,
                "lookahead_size": 10,
                "min_match_length": 2,
            },
            "lz78": {"max_dict_size": 2000},
            "logging": {"level": "INFO", "file": "logs/test.log"},
        }

        config_path = self.create_temp_config(config)
        try:
            manager = CompressionManager(config_path=config_path)
            assert manager.lz77.window_size == 1000
            assert manager.lz77.lookahead_size == 10
            assert manager.lz77.min_match_length == 2
            assert manager.lz78.max_dict_size == 2000
        finally:
            Path(config_path).unlink()

    def test_compress_lz77(self):
        """Test LZ77 compression through manager."""
        manager = CompressionManager()
        data = b"test data"
        compressed = manager.compress_lz77(data)
        assert len(compressed) > 0

    def test_decompress_lz77(self):
        """Test LZ77 decompression through manager."""
        manager = CompressionManager()
        data = b"test data"
        compressed = manager.compress_lz77(data)
        decompressed = manager.decompress_lz77(compressed)
        assert decompressed == data

    def test_compress_lz78(self):
        """Test LZ78 compression through manager."""
        manager = CompressionManager()
        data = b"test data"
        compressed = manager.compress_lz78(data)
        assert len(compressed) > 0

    def test_decompress_lz78(self):
        """Test LZ78 decompression through manager."""
        manager = CompressionManager()
        data = b"test data"
        compressed = manager.compress_lz78(data)
        decompressed = manager.decompress_lz78(compressed)
        assert decompressed == data

    def test_compression_ratio(self):
        """Test compression ratio calculation."""
        manager = CompressionManager()
        data = b"abracadabraabracadabra"
        compressed = manager.compress_lz77(data)
        ratio = manager.get_compression_ratio(len(data), len(compressed), 3)
        assert ratio > 0

    def test_compression_ratio_zero_size(self):
        """Test compression ratio with zero compressed size."""
        manager = CompressionManager()
        ratio = manager.get_compression_ratio(10, 0, 3)
        assert ratio == float("inf")

    def test_config_file_not_found(self):
        """Test that missing config file raises error."""
        with pytest.raises(FileNotFoundError):
            CompressionManager(config_path="nonexistent.yaml")

    def test_round_trip_lz77(self):
        """Test complete round trip with LZ77."""
        manager = CompressionManager()
        test_cases = [
            b"hello",
            b"abracadabra",
            b"test data with repetition",
            b"a" * 100,
            bytes(range(50)),
        ]

        for data in test_cases:
            compressed = manager.compress_lz77(data)
            decompressed = manager.decompress_lz77(compressed)
            assert decompressed == data, f"Failed for data: {data}"

    def test_round_trip_lz78(self):
        """Test complete round trip with LZ78."""
        manager = CompressionManager()
        test_cases = [
            b"hello",
            b"abracadabra",
            b"test data with repetition",
            b"a" * 100,
            bytes(range(50)),
        ]

        for data in test_cases:
            compressed = manager.compress_lz78(data)
            decompressed = manager.decompress_lz78(compressed)
            assert decompressed == data, f"Failed for data: {data}"

    def test_large_data_lz77(self):
        """Test LZ77 on larger data."""
        manager = CompressionManager()
        data = b"hello world " * 1000
        compressed = manager.compress_lz77(data)
        decompressed = manager.decompress_lz77(compressed)
        assert decompressed == data

    def test_large_data_lz78(self):
        """Test LZ78 on larger data."""
        manager = CompressionManager()
        data = b"hello world " * 1000
        compressed = manager.compress_lz78(data)
        decompressed = manager.decompress_lz78(compressed)
        assert decompressed == data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
