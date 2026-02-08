"""Unit tests for Huffman coding implementation."""

import tempfile
from collections import Counter
from pathlib import Path

import pytest
import yaml

from src.main import (
    AdaptiveHuffman,
    CanonicalHuffman,
    HuffmanCodingManager,
    HuffmanNode,
    StandardHuffman,
)


class TestHuffmanNode:
    """Test HuffmanNode functionality."""

    def test_node_initialization(self):
        """Test node initialization."""
        node = HuffmanNode(symbol=65, frequency=10)
        assert node.symbol == 65
        assert node.frequency == 10
        assert node.left is None
        assert node.right is None

    def test_node_is_leaf(self):
        """Test leaf node detection."""
        leaf = HuffmanNode(symbol=65, frequency=10)
        assert leaf.is_leaf() is True

        internal = HuffmanNode(
            frequency=20,
            left=HuffmanNode(symbol=65, frequency=10),
            right=HuffmanNode(symbol=66, frequency=10),
        )
        assert internal.is_leaf() is False

    def test_node_comparison(self):
        """Test node comparison for priority queue."""
        node1 = HuffmanNode(symbol=65, frequency=10)
        node2 = HuffmanNode(symbol=66, frequency=20)
        assert node1 < node2


class TestStandardHuffman:
    """Test standard Huffman coding."""

    def test_build_tree_simple(self):
        """Test building tree from simple frequencies."""
        huffman = StandardHuffman()
        frequencies = {65: 5, 66: 2, 67: 1}
        huffman.build_tree(frequencies)
        assert huffman.root is not None
        assert len(huffman.codes) == 3

    def test_build_tree_single_symbol(self):
        """Test building tree with single symbol."""
        huffman = StandardHuffman()
        frequencies = {65: 10}
        huffman.build_tree(frequencies)
        assert huffman.root is not None
        assert 65 in huffman.codes
        assert huffman.codes[65] == "0"

    def test_build_tree_empty(self):
        """Test building tree with empty frequencies."""
        huffman = StandardHuffman()
        huffman.build_tree({})
        assert huffman.root is None

    def test_encode_decode(self):
        """Test encoding and decoding."""
        huffman = StandardHuffman()
        frequencies = {97: 5, 98: 2, 99: 1}
        huffman.build_tree(frequencies)

        data = b"abc"
        encoded, codes = huffman.encode(data)
        assert len(encoded) > 0
        assert len(codes) == 3

        decoded = huffman.decode(encoded)
        assert decoded == data

    def test_encode_empty(self):
        """Test encoding empty data."""
        huffman = StandardHuffman()
        frequencies = {97: 1}
        huffman.build_tree(frequencies)

        data = b""
        encoded, codes = huffman.encode(data)
        assert encoded == ""

    def test_decode_empty(self):
        """Test decoding empty data."""
        huffman = StandardHuffman()
        frequencies = {97: 1}
        huffman.build_tree(frequencies)

        decoded = huffman.decode("")
        assert decoded == b""

    def test_encode_before_build(self):
        """Test that encoding before building tree raises error."""
        huffman = StandardHuffman()
        with pytest.raises(ValueError, match="not built"):
            huffman.encode(b"test")

    def test_decode_before_build(self):
        """Test that decoding before building tree raises error."""
        huffman = StandardHuffman()
        with pytest.raises(ValueError, match="not built"):
            huffman.decode("010")

    def test_round_trip(self):
        """Test complete round trip compression."""
        huffman = StandardHuffman()
        data = b"abracadabra"
        frequencies = Counter(data)
        huffman.build_tree(frequencies)

        encoded, codes = huffman.encode(data)
        decoded = huffman.decode(encoded)
        assert decoded == data


class TestCanonicalHuffman:
    """Test canonical Huffman coding."""

    def test_build_from_lengths(self):
        """Test building canonical codes from lengths."""
        canonical = CanonicalHuffman()
        code_lengths = {97: 2, 98: 2, 99: 2}
        canonical.build_from_lengths(code_lengths)
        assert len(canonical.codes) == 3

    def test_build_from_standard(self):
        """Test building canonical from standard Huffman."""
        standard = StandardHuffman()
        frequencies = {97: 5, 98: 2, 99: 1}
        standard.build_tree(frequencies)

        canonical = CanonicalHuffman()
        canonical.build_from_standard(standard)
        assert len(canonical.codes) == 3

    def test_encode_decode(self):
        """Test encoding and decoding."""
        canonical = CanonicalHuffman()
        code_lengths = {97: 2, 98: 2, 99: 2}
        canonical.build_from_lengths(code_lengths)

        data = b"abc"
        encoded, lengths = canonical.encode(data)
        assert len(encoded) > 0

        decoded = canonical.decode(encoded)
        assert decoded == data

    def test_encode_before_build(self):
        """Test that encoding before building raises error."""
        canonical = CanonicalHuffman()
        with pytest.raises(ValueError, match="not built"):
            canonical.encode(b"test")

    def test_decode_before_build(self):
        """Test that decoding before building raises error."""
        canonical = CanonicalHuffman()
        with pytest.raises(ValueError, match="not built"):
            canonical.decode("010")

    def test_round_trip(self):
        """Test complete round trip compression."""
        standard = StandardHuffman()
        data = b"abracadabra"
        frequencies = Counter(data)
        standard.build_tree(frequencies)

        canonical = CanonicalHuffman()
        canonical.build_from_standard(standard)

        encoded, lengths = canonical.encode(data)
        decoded = canonical.decode(encoded)
        assert decoded == data


class TestAdaptiveHuffman:
    """Test adaptive Huffman coding."""

    def test_encode_decode_simple(self):
        """Test simple adaptive encoding and decoding."""
        adaptive = AdaptiveHuffman()
        data = b"abc"
        encoded = adaptive.encode(data)
        assert len(encoded) > 0

        decoded = adaptive.decode(encoded)
        assert decoded == data

    def test_encode_decode_repetitive(self):
        """Test adaptive encoding on repetitive data."""
        adaptive = AdaptiveHuffman()
        data = b"abracadabra"
        encoded = adaptive.encode(data)
        decoded = adaptive.decode(encoded)
        assert decoded == data

    def test_encode_decode_empty(self):
        """Test adaptive encoding on empty data."""
        adaptive = AdaptiveHuffman()
        data = b""
        encoded = adaptive.encode(data)
        decoded = adaptive.decode(encoded)
        assert decoded == data

    def test_encode_decode_single_char(self):
        """Test adaptive encoding on single character."""
        adaptive = AdaptiveHuffman()
        data = b"a"
        encoded = adaptive.encode(data)
        decoded = adaptive.decode(encoded)
        assert decoded == data

    def test_encode_decode_repeated_char(self):
        """Test adaptive encoding on repeated character."""
        adaptive = AdaptiveHuffman()
        data = b"aaaa"
        encoded = adaptive.encode(data)
        decoded = adaptive.decode(encoded)
        assert decoded == data

    def test_round_trip(self):
        """Test complete round trip compression."""
        adaptive = AdaptiveHuffman()
        test_cases = [
            b"hello",
            b"abracadabra",
            b"test data",
            bytes(range(10)),
        ]

        for data in test_cases:
            encoded = adaptive.encode(data)
            decoded = adaptive.decode(encoded)
            assert decoded == data, f"Failed for data: {data}"


class TestHuffmanCodingManager:
    """Test HuffmanCodingManager functionality."""

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
        manager = HuffmanCodingManager()
        assert manager.config is not None

    def test_initialization_with_custom_config(self):
        """Test initialization with custom config file."""
        config = {
            "logging": {"level": "INFO", "file": "logs/test.log"},
        }

        config_path = self.create_temp_config(config)
        try:
            manager = HuffmanCodingManager(config_path=config_path)
            assert manager.config is not None
        finally:
            Path(config_path).unlink()

    def test_compress_standard(self):
        """Test standard compression through manager."""
        manager = HuffmanCodingManager()
        data = b"abracadabra"
        encoded, codes = manager.compress_standard(data)
        assert len(encoded) > 0
        assert len(codes) > 0

    def test_decompress_standard(self):
        """Test standard decompression through manager."""
        manager = HuffmanCodingManager()
        data = b"abracadabra"
        encoded, codes = manager.compress_standard(data)
        decoded = manager.decompress_standard(encoded, codes)
        assert decoded == data

    def test_compress_canonical(self):
        """Test canonical compression through manager."""
        manager = HuffmanCodingManager()
        data = b"abracadabra"
        encoded, lengths = manager.compress_canonical(data)
        assert len(encoded) > 0
        assert len(lengths) > 0

    def test_decompress_canonical(self):
        """Test canonical decompression through manager."""
        manager = HuffmanCodingManager()
        data = b"abracadabra"
        encoded, lengths = manager.compress_canonical(data)
        decoded = manager.decompress_canonical(encoded, lengths)
        assert decoded == data

    def test_compress_adaptive(self):
        """Test adaptive compression through manager."""
        manager = HuffmanCodingManager()
        data = b"abracadabra"
        encoded = manager.compress_adaptive(data)
        assert len(encoded) > 0

    def test_decompress_adaptive(self):
        """Test adaptive decompression through manager."""
        manager = HuffmanCodingManager()
        data = b"abracadabra"
        encoded = manager.compress_adaptive(data)
        decoded = manager.decompress_adaptive(encoded)
        assert decoded == data

    def test_compression_ratio(self):
        """Test compression ratio calculation."""
        manager = HuffmanCodingManager()
        data = b"abracadabra"
        encoded, _ = manager.compress_standard(data)
        ratio = manager.get_compression_ratio(len(data), len(encoded))
        assert ratio > 0

    def test_compression_ratio_zero(self):
        """Test compression ratio with zero compressed size."""
        manager = HuffmanCodingManager()
        ratio = manager.get_compression_ratio(10, 0)
        assert ratio == float("inf")

    def test_config_file_not_found(self):
        """Test that missing config file raises error."""
        with pytest.raises(FileNotFoundError):
            HuffmanCodingManager(config_path="nonexistent.yaml")

    def test_round_trip_all_variants(self):
        """Test round trip for all variants."""
        manager = HuffmanCodingManager()
        data = b"abracadabra"

        encoded, codes = manager.compress_standard(data)
        decoded = manager.decompress_standard(encoded, codes)
        assert decoded == data

        encoded, lengths = manager.compress_canonical(data)
        decoded = manager.decompress_canonical(encoded, lengths)
        assert decoded == data

        encoded = manager.compress_adaptive(data)
        decoded = manager.decompress_adaptive(encoded)
        assert decoded == data

    def test_large_data(self):
        """Test compression on larger data."""
        manager = HuffmanCodingManager()
        data = b"hello world " * 100

        encoded, codes = manager.compress_standard(data)
        decoded = manager.decompress_standard(encoded, codes)
        assert decoded == data

        encoded = manager.compress_adaptive(data)
        decoded = manager.decompress_adaptive(encoded)
        assert decoded == data

    def test_binary_data(self):
        """Test compression on binary data."""
        manager = HuffmanCodingManager()
        data = bytes(range(256))

        encoded, codes = manager.compress_standard(data)
        decoded = manager.decompress_standard(encoded, codes)
        assert decoded == data

        encoded = manager.compress_adaptive(data)
        decoded = manager.decompress_adaptive(encoded)
        assert decoded == data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
