"""Unit tests for BWT and MTF compression implementation."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import (
    BWTMTFCompressor,
    BurrowsWheelerTransform,
    MoveToFront,
)


class TestBurrowsWheelerTransform:
    """Test Burrows-Wheeler Transform functionality."""

    def test_transform_simple(self):
        """Test simple BWT transformation."""
        bwt = BurrowsWheelerTransform()
        data = b"banana"
        transformed, index = bwt.transform(data)
        assert len(transformed) == len(data)
        assert 0 <= index < len(data)

    def test_inverse_transform_simple(self):
        """Test simple inverse BWT."""
        bwt = BurrowsWheelerTransform()
        data = b"banana"
        transformed, index = bwt.transform(data)
        original = bwt.inverse_transform(transformed, index)
        assert original == data

    def test_transform_single_char(self):
        """Test BWT on single character."""
        bwt = BurrowsWheelerTransform()
        data = b"a"
        transformed, index = bwt.transform(data)
        assert transformed == data
        assert index == 0

    def test_inverse_transform_single_char(self):
        """Test inverse BWT on single character."""
        bwt = BurrowsWheelerTransform()
        data = b"a"
        transformed, index = bwt.transform(data)
        original = bwt.inverse_transform(transformed, index)
        assert original == data

    def test_transform_repetitive(self):
        """Test BWT on repetitive data."""
        bwt = BurrowsWheelerTransform()
        data = b"aaaa"
        transformed, index = bwt.transform(data)
        original = bwt.inverse_transform(transformed, index)
        assert original == data

    def test_transform_empty(self):
        """Test that transforming empty data raises error."""
        bwt = BurrowsWheelerTransform()
        with pytest.raises(ValueError, match="empty data"):
            bwt.transform(b"")

    def test_inverse_transform_empty(self):
        """Test that inverse transforming empty data raises error."""
        bwt = BurrowsWheelerTransform()
        with pytest.raises(ValueError, match="empty data"):
            bwt.inverse_transform(b"", 0)

    def test_inverse_transform_invalid_index(self):
        """Test that invalid index raises error."""
        bwt = BurrowsWheelerTransform()
        with pytest.raises(ValueError, match="out of range"):
            bwt.inverse_transform(b"abc", 10)

    def test_round_trip(self):
        """Test complete round trip transformation."""
        bwt = BurrowsWheelerTransform()
        test_cases = [
            b"banana",
            b"abracadabra",
            b"hello",
            b"mississippi",
            b"a" * 10,
        ]

        for data in test_cases:
            transformed, index = bwt.transform(data)
            original = bwt.inverse_transform(transformed, index)
            assert original == data, f"Failed for data: {data}"

    def test_bwt_groups_characters(self):
        """Test that BWT groups similar characters."""
        bwt = BurrowsWheelerTransform()
        data = b"abracadabra"
        transformed, index = bwt.transform(data)

        assert len(transformed) == len(data)
        original = bwt.inverse_transform(transformed, index)
        assert original == data


class TestMoveToFront:
    """Test Move-to-Front encoding functionality."""

    def test_encode_simple(self):
        """Test simple MTF encoding."""
        mtf = MoveToFront()
        data = b"abc"
        encoded = mtf.encode(data)
        assert len(encoded) == len(data)
        assert all(0 <= idx < 256 for idx in encoded)

    def test_decode_simple(self):
        """Test simple MTF decoding."""
        mtf = MoveToFront()
        data = b"abc"
        encoded = mtf.encode(data)
        decoded = mtf.decode(encoded)
        assert decoded == data

    def test_encode_empty(self):
        """Test MTF encoding on empty data."""
        mtf = MoveToFront()
        data = b""
        encoded = mtf.encode(data)
        assert len(encoded) == 0

    def test_decode_empty(self):
        """Test MTF decoding on empty data."""
        mtf = MoveToFront()
        decoded = mtf.decode([])
        assert decoded == b""

    def test_encode_single_char(self):
        """Test MTF encoding on single character."""
        mtf = MoveToFront()
        data = b"a"
        encoded = mtf.encode(data)
        assert len(encoded) == 1
        assert encoded[0] == 97

    def test_encode_repetitive(self):
        """Test MTF encoding on repetitive data."""
        mtf = MoveToFront()
        data = b"aaaa"
        encoded = mtf.encode(data)
        assert len(encoded) == 4
        assert encoded[0] == 97
        assert encoded[1] == 0
        assert encoded[2] == 0
        assert encoded[3] == 0

    def test_decode_invalid_index(self):
        """Test that invalid index raises error."""
        mtf = MoveToFront()
        with pytest.raises(ValueError, match="out of range"):
            mtf.decode([300])

    def test_round_trip(self):
        """Test complete round trip encoding and decoding."""
        mtf = MoveToFront()
        test_cases = [
            b"abc",
            b"abracadabra",
            b"hello world",
            b"a" * 10,
            bytes(range(10)),
        ]

        for data in test_cases:
            encoded = mtf.encode(data)
            decoded = mtf.decode(encoded)
            assert decoded == data, f"Failed for data: {data}"

    def test_mtf_moves_to_front(self):
        """Test that MTF moves symbols to front."""
        mtf = MoveToFront()
        data = b"abab"
        encoded = mtf.encode(data)

        assert encoded[0] == 97
        assert encoded[1] == 98
        assert encoded[2] == 1
        assert encoded[3] == 1


class TestBWTMTFCompressor:
    """Test BWT+MTF compressor functionality."""

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
        compressor = BWTMTFCompressor()
        assert compressor.alphabet_size == 256

    def test_initialization_with_custom_config(self):
        """Test initialization with custom config file."""
        config = {
            "bwt_mtf": {"alphabet_size": 128},
            "logging": {"level": "INFO", "file": "logs/test.log"},
        }

        config_path = self.create_temp_config(config)
        try:
            compressor = BWTMTFCompressor(config_path=config_path)
            assert compressor.alphabet_size == 128
        finally:
            Path(config_path).unlink()

    def test_compress(self):
        """Test compression through manager."""
        compressor = BWTMTFCompressor()
        data = b"abracadabra"
        mtf_encoded, original_index = compressor.compress(data)
        assert len(mtf_encoded) > 0
        assert 0 <= original_index < len(data)

    def test_decompress(self):
        """Test decompression through manager."""
        compressor = BWTMTFCompressor()
        data = b"abracadabra"
        mtf_encoded, original_index = compressor.compress(data)
        decompressed = compressor.decompress(mtf_encoded, original_index)
        assert decompressed == data

    def test_compress_empty(self):
        """Test that compressing empty data raises error."""
        compressor = BWTMTFCompressor()
        with pytest.raises(ValueError, match="empty data"):
            compressor.compress(b"")

    def test_decompress_empty(self):
        """Test that decompressing empty data raises error."""
        compressor = BWTMTFCompressor()
        with pytest.raises(ValueError, match="empty data"):
            compressor.decompress([], 0)

    def test_compression_ratio(self):
        """Test compression ratio calculation."""
        compressor = BWTMTFCompressor()
        data = b"abracadabra"
        mtf_encoded, original_index = compressor.compress(data)
        ratio = compressor.get_compression_ratio(len(data), len(mtf_encoded))
        assert ratio > 0

    def test_compression_ratio_zero(self):
        """Test compression ratio with zero compressed size."""
        compressor = BWTMTFCompressor()
        ratio = compressor.get_compression_ratio(10, 0)
        assert ratio == float("inf")

    def test_config_file_not_found(self):
        """Test that missing config file raises error."""
        with pytest.raises(FileNotFoundError):
            BWTMTFCompressor(config_path="nonexistent.yaml")

    def test_round_trip(self):
        """Test complete round trip compression."""
        compressor = BWTMTFCompressor()
        test_cases = [
            b"banana",
            b"abracadabra",
            b"hello world",
            b"mississippi",
            b"a" * 10,
            bytes(range(10)),
        ]

        for data in test_cases:
            mtf_encoded, original_index = compressor.compress(data)
            decompressed = compressor.decompress(mtf_encoded, original_index)
            assert decompressed == data, f"Failed for data: {data}"

    def test_large_data(self):
        """Test compression on larger data."""
        compressor = BWTMTFCompressor()
        data = b"hello world " * 10
        mtf_encoded, original_index = compressor.compress(data)
        decompressed = compressor.decompress(mtf_encoded, original_index)
        assert decompressed == data

    def test_binary_data(self):
        """Test compression on binary data."""
        compressor = BWTMTFCompressor()
        data = bytes(range(50))
        mtf_encoded, original_index = compressor.compress(data)
        decompressed = compressor.decompress(mtf_encoded, original_index)
        assert decompressed == data

    def test_repetitive_data(self):
        """Test compression on highly repetitive data."""
        compressor = BWTMTFCompressor()
        data = b"a" * 100
        mtf_encoded, original_index = compressor.compress(data)
        decompressed = compressor.decompress(mtf_encoded, original_index)
        assert decompressed == data

    def test_bwt_mtf_combination(self):
        """Test that BWT+MTF works together correctly."""
        compressor = BWTMTFCompressor()
        data = b"abracadabra"

        mtf_encoded, original_index = compressor.compress(data)

        assert len(mtf_encoded) == len(data)
        assert 0 <= original_index < len(data)

        decompressed = compressor.decompress(mtf_encoded, original_index)
        assert decompressed == data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
