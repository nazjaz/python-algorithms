"""Unit tests for arithmetic coding implementation."""

import tempfile
from collections import Counter
from pathlib import Path

import pytest
import yaml

from src.main import (
    ArithmeticCodingManager,
    ArithmeticDecoder,
    ArithmeticEncoder,
    ProbabilityModel,
)


class TestProbabilityModel:
    """Test probability model functionality."""

    def test_model_initialization(self):
        """Test model initialization with frequencies."""
        frequencies = {97: 5, 98: 2, 99: 1}
        model = ProbabilityModel(frequencies)
        assert model.total == 8
        assert len(model.cumulative) == 3

    def test_model_empty(self):
        """Test model initialization with empty frequencies."""
        model = ProbabilityModel()
        assert model.total == 0
        assert len(model.cumulative) == 0

    def test_get_range(self):
        """Test getting probability range for symbol."""
        frequencies = {97: 5, 98: 2, 99: 1}
        model = ProbabilityModel(frequencies)
        low, high = model.get_range(97)
        assert 0.0 <= low < high <= 1.0

    def test_get_range_invalid_symbol(self):
        """Test getting range for invalid symbol raises error."""
        frequencies = {97: 5}
        model = ProbabilityModel(frequencies)
        with pytest.raises(ValueError, match="not in probability model"):
            model.get_range(98)

    def test_get_symbol_for_value(self):
        """Test getting symbol for probability value."""
        frequencies = {97: 5, 98: 2, 99: 1}
        model = ProbabilityModel(frequencies)
        symbol = model.get_symbol_for_value(0.1)
        assert symbol in frequencies

    def test_get_symbol_for_value_boundary(self):
        """Test getting symbol at boundary values."""
        frequencies = {97: 5, 98: 2, 99: 1}
        model = ProbabilityModel(frequencies)
        symbol0 = model.get_symbol_for_value(0.0)
        symbol1 = model.get_symbol_for_value(0.99)
        assert symbol0 in frequencies
        assert symbol1 in frequencies

    def test_get_symbol_for_value_invalid(self):
        """Test getting symbol for invalid value raises error."""
        frequencies = {97: 5}
        model = ProbabilityModel(frequencies)
        with pytest.raises(ValueError, match="out of range"):
            model.get_symbol_for_value(1.5)

    def test_update_frequency(self):
        """Test updating symbol frequency."""
        frequencies = {97: 5}
        model = ProbabilityModel(frequencies)
        initial_total = model.total

        model.update_frequency(97, 2)
        assert model.frequencies[97] == 7
        assert model.total == initial_total + 2

    def test_update_frequency_new_symbol(self):
        """Test updating frequency for new symbol."""
        frequencies = {97: 5}
        model = ProbabilityModel(frequencies)
        model.update_frequency(98, 3)
        assert model.frequencies[98] == 3
        assert 98 in model.cumulative


class TestArithmeticEncoder:
    """Test arithmetic encoder functionality."""

    def test_encoder_initialization(self):
        """Test encoder initialization."""
        encoder = ArithmeticEncoder(precision_bits=32)
        assert encoder.precision_bits == 32
        assert encoder.low == 0

    def test_encode_simple(self):
        """Test simple encoding."""
        encoder = ArithmeticEncoder(precision_bits=32)
        data = b"ab"
        frequencies = Counter(data)
        model = ProbabilityModel(frequencies)

        encoded, result_model = encoder.encode(data, model)
        assert len(encoded) > 0
        assert result_model is not None

    def test_encode_empty(self):
        """Test encoding empty data."""
        encoder = ArithmeticEncoder(precision_bits=32)
        data = b""
        frequencies = Counter(data)
        model = ProbabilityModel(frequencies)

        encoded, result_model = encoder.encode(data, model)
        assert len(encoded) >= 0

    def test_encode_single_symbol(self):
        """Test encoding single symbol."""
        encoder = ArithmeticEncoder(precision_bits=32)
        data = b"a"
        frequencies = Counter(data)
        model = ProbabilityModel(frequencies)

        encoded, result_model = encoder.encode(data, model)
        assert len(encoded) > 0

    def test_encode_repetitive(self):
        """Test encoding repetitive data."""
        encoder = ArithmeticEncoder(precision_bits=32)
        data = b"aaaa"
        frequencies = Counter(data)
        model = ProbabilityModel(frequencies)

        encoded, result_model = encoder.encode(data, model)
        assert len(encoded) > 0

    def test_encode_with_model(self):
        """Test encoding with provided model."""
        encoder = ArithmeticEncoder(precision_bits=32)
        data = b"abracadabra"
        frequencies = {97: 5, 98: 2, 99: 1, 100: 1, 114: 2}
        model = ProbabilityModel(frequencies)

        encoded, result_model = encoder.encode(data, model)
        assert len(encoded) > 0

    def test_precision_32_vs_64(self):
        """Test encoding with different precision."""
        data = b"abracadabra"
        frequencies = Counter(data)
        model = ProbabilityModel(frequencies)

        encoder32 = ArithmeticEncoder(precision_bits=32)
        encoded32, _ = encoder32.encode(data, model)

        encoder64 = ArithmeticEncoder(precision_bits=64)
        encoded64, _ = encoder64.encode(data, model)

        assert len(encoded32) > 0
        assert len(encoded64) > 0


class TestArithmeticDecoder:
    """Test arithmetic decoder functionality."""

    def test_decoder_initialization(self):
        """Test decoder initialization."""
        decoder = ArithmeticDecoder(precision_bits=32)
        assert decoder.precision_bits == 32

    def test_decode_simple(self):
        """Test simple decoding."""
        encoder = ArithmeticEncoder(precision_bits=32)
        decoder = ArithmeticDecoder(precision_bits=32)

        data = b"ab"
        frequencies = Counter(data)
        model = ProbabilityModel(frequencies)

        encoded, model = encoder.encode(data, model)
        decoded = decoder.decode(encoded, model, len(data))
        assert decoded == data

    def test_decode_empty(self):
        """Test decoding empty data."""
        encoder = ArithmeticEncoder(precision_bits=32)
        decoder = ArithmeticDecoder(precision_bits=32)

        data = b""
        frequencies = Counter(data)
        model = ProbabilityModel(frequencies)

        encoded, model = encoder.encode(data, model)
        decoded = decoder.decode(encoded, model, len(data))
        assert decoded == data

    def test_decode_single_symbol(self):
        """Test decoding single symbol."""
        encoder = ArithmeticEncoder(precision_bits=32)
        decoder = ArithmeticDecoder(precision_bits=32)

        data = b"a"
        frequencies = Counter(data)
        model = ProbabilityModel(frequencies)

        encoded, model = encoder.encode(data, model)
        decoded = decoder.decode(encoded, model, len(data))
        assert decoded == data

    def test_decode_repetitive(self):
        """Test decoding repetitive data."""
        encoder = ArithmeticEncoder(precision_bits=32)
        decoder = ArithmeticDecoder(precision_bits=32)

        data = b"aaaa"
        frequencies = Counter(data)
        model = ProbabilityModel(frequencies)

        encoded, model = encoder.encode(data, model)
        decoded = decoder.decode(encoded, model, len(data))
        assert decoded == data

    def test_round_trip(self):
        """Test complete round trip encoding and decoding."""
        encoder = ArithmeticEncoder(precision_bits=32)
        decoder = ArithmeticDecoder(precision_bits=32)

        test_cases = [
            b"ab",
            b"abracadabra",
            b"hello world",
            b"a" * 10,
            bytes(range(10)),
        ]

        for data in test_cases:
            frequencies = Counter(data)
            model = ProbabilityModel(frequencies)

            encoded, model = encoder.encode(data, model)
            decoded = decoder.decode(encoded, model, len(data))
            assert decoded == data, f"Failed for data: {data}"

    def test_precision_mismatch(self):
        """Test that precision mismatch may cause issues."""
        encoder = ArithmeticEncoder(precision_bits=32)
        decoder32 = ArithmeticDecoder(precision_bits=32)
        decoder64 = ArithmeticDecoder(precision_bits=64)

        data = b"abracadabra"
        frequencies = Counter(data)
        model = ProbabilityModel(frequencies)

        encoded, model = encoder.encode(data, model)
        decoded32 = decoder32.decode(encoded, model, len(data))
        decoded64 = decoder64.decode(encoded, model, len(data))

        assert decoded32 == data
        assert decoded64 == data


class TestArithmeticCodingManager:
    """Test ArithmeticCodingManager functionality."""

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
        manager = ArithmeticCodingManager()
        assert manager.precision_bits > 0

    def test_initialization_with_custom_config(self):
        """Test initialization with custom config file."""
        config = {
            "arithmetic_coding": {"precision_bits": 64},
            "logging": {"level": "INFO", "file": "logs/test.log"},
        }

        config_path = self.create_temp_config(config)
        try:
            manager = ArithmeticCodingManager(config_path=config_path)
            assert manager.precision_bits == 64
        finally:
            Path(config_path).unlink()

    def test_compress(self):
        """Test compression through manager."""
        manager = ArithmeticCodingManager()
        data = b"abracadabra"
        encoded_bits, model, length = manager.compress(data)
        assert len(encoded_bits) > 0
        assert model is not None
        assert length == len(data)

    def test_decompress(self):
        """Test decompression through manager."""
        manager = ArithmeticCodingManager()
        data = b"abracadabra"
        encoded_bits, model, length = manager.compress(data)
        decoded = manager.decompress(encoded_bits, model, length)
        assert decoded == data

    def test_compress_with_model(self):
        """Test compression with provided model."""
        manager = ArithmeticCodingManager()
        data = b"abracadabra"
        frequencies = Counter(data)
        model = ProbabilityModel(frequencies)

        encoded_bits, result_model, length = manager.compress(data, model=model)
        assert len(encoded_bits) > 0
        assert length == len(data)

    def test_compression_ratio(self):
        """Test compression ratio calculation."""
        manager = ArithmeticCodingManager()
        data = b"abracadabra"
        encoded_bits, model, length = manager.compress(data)
        ratio = manager.get_compression_ratio(len(data), len(encoded_bits))
        assert ratio > 0

    def test_compression_ratio_zero(self):
        """Test compression ratio with zero compressed size."""
        manager = ArithmeticCodingManager()
        ratio = manager.get_compression_ratio(10, 0)
        assert ratio == float("inf")

    def test_config_file_not_found(self):
        """Test that missing config file raises error."""
        with pytest.raises(FileNotFoundError):
            ArithmeticCodingManager(config_path="nonexistent.yaml")

    def test_round_trip(self):
        """Test complete round trip compression."""
        manager = ArithmeticCodingManager()
        test_cases = [
            b"ab",
            b"abracadabra",
            b"hello world",
            b"a" * 10,
            bytes(range(10)),
        ]

        for data in test_cases:
            encoded_bits, model, length = manager.compress(data)
            decoded = manager.decompress(encoded_bits, model, length)
            assert decoded == data, f"Failed for data: {data}"

    def test_large_data(self):
        """Test compression on larger data."""
        manager = ArithmeticCodingManager()
        data = b"hello world " * 100
        encoded_bits, model, length = manager.compress(data)
        decoded = manager.decompress(encoded_bits, model, length)
        assert decoded == data

    def test_binary_data(self):
        """Test compression on binary data."""
        manager = ArithmeticCodingManager()
        data = bytes(range(50))
        encoded_bits, model, length = manager.compress(data)
        decoded = manager.decompress(encoded_bits, model, length)
        assert decoded == data

    def test_repetitive_data(self):
        """Test compression on highly repetitive data."""
        manager = ArithmeticCodingManager()
        data = b"a" * 100
        encoded_bits, model, length = manager.compress(data)
        decoded = manager.decompress(encoded_bits, model, length)
        assert decoded == data

    def test_different_precisions(self):
        """Test compression with different precision settings."""
        config32 = {
            "arithmetic_coding": {"precision_bits": 32},
            "logging": {"level": "WARNING", "file": "logs/test.log"},
        }
        config64 = {
            "arithmetic_coding": {"precision_bits": 64},
            "logging": {"level": "WARNING", "file": "logs/test.log"},
        }

        config_path32 = self.create_temp_config(config32)
        config_path64 = self.create_temp_config(config64)

        try:
            manager32 = ArithmeticCodingManager(config_path=config_path32)
            manager64 = ArithmeticCodingManager(config_path=config_path64)

            data = b"abracadabra"

            encoded32, model32, length = manager32.compress(data)
            decoded32 = manager32.decompress(encoded32, model32, length)

            encoded64, model64, length = manager64.compress(data)
            decoded64 = manager64.decompress(encoded64, model64, length)

            assert decoded32 == data
            assert decoded64 == data
        finally:
            Path(config_path32).unlink()
            Path(config_path64).unlink()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
