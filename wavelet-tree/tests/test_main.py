"""Unit tests for wavelet tree module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import BitVector, WaveletTree


class TestBitVector:
    """Test cases for BitVector class."""

    def test_bitvector_creation(self):
        """Test BitVector creation."""
        bits = [True, False, True, True, False]
        bv = BitVector(bits)
        assert bv.n == 5
        assert len(bv.bits) == 5

    def test_rank_operation(self):
        """Test rank operation."""
        bits = [True, False, True, True, False]
        bv = BitVector(bits)

        assert bv.rank(0, True) == 1
        assert bv.rank(1, True) == 1
        assert bv.rank(2, True) == 2
        assert bv.rank(4, True) == 3

        assert bv.rank(0, False) == 0
        assert bv.rank(1, False) == 1
        assert bv.rank(4, False) == 2

    def test_select_operation(self):
        """Test select operation."""
        bits = [True, False, True, True, False]
        bv = BitVector(bits)

        assert bv.select(1, True) == 0
        assert bv.select(2, True) == 2
        assert bv.select(3, True) == 3
        assert bv.select(4, True) is None

        assert bv.select(1, False) == 1
        assert bv.select(2, False) == 4
        assert bv.select(3, False) is None

    def test_access_operation(self):
        """Test access operation."""
        bits = [True, False, True, True, False]
        bv = BitVector(bits)

        assert bv.access(0) is True
        assert bv.access(1) is False
        assert bv.access(4) is False

    def test_select_invalid_k(self):
        """Test select with invalid k."""
        bits = [True, False, True]
        bv = BitVector(bits)

        assert bv.select(0, True) is None
        assert bv.select(-1, True) is None


class TestWaveletTree:
    """Test cases for WaveletTree class."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for testing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.fixture
    def config_file(self, temp_dir):
        """Create temporary config file."""
        config = {
            "logging": {"level": "INFO", "file": str(temp_dir / "app.log")},
        }
        config_path = temp_dir / "config.yaml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)
        return str(config_path)

    @pytest.fixture
    def simple_sequence(self):
        """Create simple sequence for testing."""
        return [1, 2, 3, 1, 2, 3]

    @pytest.fixture
    def complex_sequence(self):
        """Create complex sequence for testing."""
        return [1, 2, 3, 1, 2, 3, 1, 2, 3, 4, 5]

    def test_tree_creation(self, simple_sequence, config_file):
        """Test WaveletTree creation."""
        tree = WaveletTree(simple_sequence, config_path=config_file)
        assert tree.n == len(simple_sequence)
        assert tree.alphabet_min == 1
        assert tree.alphabet_max == 3

    def test_tree_creation_empty(self, config_file):
        """Test WaveletTree creation with empty sequence."""
        with pytest.raises(ValueError):
            WaveletTree([], config_path=config_file)

    def test_rank_operation(self, simple_sequence, config_file):
        """Test rank operation."""
        tree = WaveletTree(simple_sequence, config_path=config_file)

        rank = tree.rank(0, 1)
        assert rank == 1

        rank = tree.rank(3, 1)
        assert rank == 2

        rank = tree.rank(5, 2)
        assert rank == 2

    def test_rank_out_of_bounds(self, simple_sequence, config_file):
        """Test rank with out of bounds position."""
        tree = WaveletTree(simple_sequence, config_path=config_file)

        with pytest.raises(ValueError):
            tree.rank(-1, 1)

        with pytest.raises(ValueError):
            tree.rank(10, 1)

    def test_rank_value_not_in_alphabet(self, simple_sequence, config_file):
        """Test rank with value not in alphabet."""
        tree = WaveletTree(simple_sequence, config_path=config_file)

        rank = tree.rank(5, 0)
        assert rank == 0

        rank = tree.rank(5, 10)
        assert rank == 0

    def test_select_operation(self, simple_sequence, config_file):
        """Test select operation."""
        tree = WaveletTree(simple_sequence, config_path=config_file)

        pos = tree.select(1, 1)
        assert pos == 0

        pos = tree.select(2, 1)
        assert pos == 3

        pos = tree.select(1, 2)
        assert pos == 1

    def test_select_invalid_k(self, simple_sequence, config_file):
        """Test select with invalid k."""
        tree = WaveletTree(simple_sequence, config_path=config_file)

        with pytest.raises(ValueError):
            tree.select(0, 1)

        with pytest.raises(ValueError):
            tree.select(-1, 1)

    def test_select_value_not_found(self, simple_sequence, config_file):
        """Test select with value not in sequence."""
        tree = WaveletTree(simple_sequence, config_path=config_file)

        pos = tree.select(1, 10)
        assert pos is None

    def test_range_count(self, complex_sequence, config_file):
        """Test range count operation."""
        tree = WaveletTree(complex_sequence, config_path=config_file)

        count = tree.range_count(0, 5, 1, 2)
        assert count >= 0

        count = tree.range_count(0, 10, 3, 5)
        assert count >= 0

    def test_range_count_invalid_range(self, simple_sequence, config_file):
        """Test range count with invalid range."""
        tree = WaveletTree(simple_sequence, config_path=config_file)

        with pytest.raises(ValueError):
            tree.range_count(-1, 5, 1, 3)

        with pytest.raises(ValueError):
            tree.range_count(0, 10, 1, 3)

        with pytest.raises(ValueError):
            tree.range_count(5, 0, 1, 3)

    def test_range_count_invalid_values(self, simple_sequence, config_file):
        """Test range count with invalid value range."""
        tree = WaveletTree(simple_sequence, config_path=config_file)

        count = tree.range_count(0, 5, 5, 1)
        assert count == 0

    def test_access_operation(self, simple_sequence, config_file):
        """Test access operation."""
        tree = WaveletTree(simple_sequence, config_path=config_file)

        assert tree.access(0) == 1
        assert tree.access(1) == 2
        assert tree.access(5) == 3

    def test_access_out_of_bounds(self, simple_sequence, config_file):
        """Test access with out of bounds position."""
        tree = WaveletTree(simple_sequence, config_path=config_file)

        with pytest.raises(ValueError):
            tree.access(-1)

        with pytest.raises(ValueError):
            tree.access(10)

    def test_get_sequence(self, simple_sequence, config_file):
        """Test getting original sequence."""
        tree = WaveletTree(simple_sequence, config_path=config_file)
        sequence = tree.get_sequence()
        assert sequence == simple_sequence

    def test_single_value_sequence(self, config_file):
        """Test with single value sequence."""
        sequence = [5, 5, 5, 5]
        tree = WaveletTree(sequence, config_path=config_file)

        rank = tree.rank(3, 5)
        assert rank == 4

        pos = tree.select(2, 5)
        assert pos == 1

    def test_single_element_sequence(self, config_file):
        """Test with single element sequence."""
        sequence = [42]
        tree = WaveletTree(sequence, config_path=config_file)

        rank = tree.rank(0, 42)
        assert rank == 1

        pos = tree.select(1, 42)
        assert pos == 0

    def test_large_sequence(self, config_file):
        """Test with larger sequence."""
        sequence = list(range(1, 21)) * 2
        tree = WaveletTree(sequence, config_path=config_file)

        rank = tree.rank(19, 10)
        assert rank >= 0

        count = tree.range_count(0, 19, 5, 15)
        assert count >= 0

    def test_rank_select_consistency(self, complex_sequence, config_file):
        """Test consistency between rank and select."""
        tree = WaveletTree(complex_sequence, config_path=config_file)

        for value in [1, 2, 3]:
            for k in range(1, 4):
                pos = tree.select(k, value)
                if pos is not None:
                    rank = tree.rank(pos, value)
                    assert rank >= k
