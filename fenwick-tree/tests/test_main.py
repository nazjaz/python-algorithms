"""Unit tests for Fenwick tree module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import FenwickTree


class TestFenwickTree:
    """Test cases for FenwickTree class."""

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

    def test_creation_from_array(self, config_file):
        """Test creating tree from array."""
        array = [1, 2, 3, 4, 5]
        tree = FenwickTree(array=array, config_path=config_file)
        assert tree.get_size() == 5
        assert tree.get_all_values() == array

    def test_creation_from_size(self, config_file):
        """Test creating empty tree from size."""
        tree = FenwickTree(size=10, config_path=config_file)
        assert tree.get_size() == 10
        assert all(v == 0 for v in tree.get_all_values())

    def test_creation_no_args(self):
        """Test creation with no arguments."""
        with pytest.raises(ValueError):
            FenwickTree()

    def test_creation_both_args(self):
        """Test creation with both size and array."""
        with pytest.raises(ValueError):
            FenwickTree(size=5, array=[1, 2, 3])

    def test_creation_invalid_size(self):
        """Test creation with invalid size."""
        with pytest.raises(ValueError):
            FenwickTree(size=0)

    def test_prefix_sum(self, config_file):
        """Test prefix sum queries."""
        array = [1, 3, 5, 7, 9]
        tree = FenwickTree(array=array, config_path=config_file)
        assert tree.prefix_sum(0) == 1
        assert tree.prefix_sum(1) == 4
        assert tree.prefix_sum(2) == 9
        assert tree.prefix_sum(4) == 25

    def test_prefix_sum_single_element(self, config_file):
        """Test prefix sum with single element."""
        tree = FenwickTree(array=[10], config_path=config_file)
        assert tree.prefix_sum(0) == 10

    def test_prefix_sum_invalid_index(self, config_file):
        """Test prefix sum with invalid index."""
        tree = FenwickTree(array=[1, 2, 3], config_path=config_file)
        with pytest.raises(ValueError):
            tree.prefix_sum(-1)
        with pytest.raises(ValueError):
            tree.prefix_sum(10)

    def test_range_sum(self, config_file):
        """Test range sum queries."""
        array = [1, 3, 5, 7, 9, 11]
        tree = FenwickTree(array=array, config_path=config_file)
        assert tree.range_sum(0, 0) == 1
        assert tree.range_sum(0, 2) == 9
        assert tree.range_sum(1, 4) == 24
        assert tree.range_sum(0, 5) == 36

    def test_range_sum_single_element(self, config_file):
        """Test range sum with single element."""
        tree = FenwickTree(array=[5], config_path=config_file)
        assert tree.range_sum(0, 0) == 5

    def test_range_sum_invalid_indices(self, config_file):
        """Test range sum with invalid indices."""
        tree = FenwickTree(array=[1, 2, 3], config_path=config_file)
        with pytest.raises(ValueError):
            tree.range_sum(-1, 1)
        with pytest.raises(ValueError):
            tree.range_sum(0, 10)
        with pytest.raises(ValueError):
            tree.range_sum(2, 1)

    def test_update(self, config_file):
        """Test point updates."""
        tree = FenwickTree(array=[1, 2, 3, 4, 5], config_path=config_file)
        tree.update(2, 5)
        assert tree.get_value(2) == 8
        assert tree.prefix_sum(2) == 11
        assert tree.range_sum(0, 4) == 20

    def test_update_multiple(self, config_file):
        """Test multiple updates."""
        tree = FenwickTree(array=[1, 1, 1, 1], config_path=config_file)
        tree.update(0, 2)
        tree.update(1, 3)
        tree.update(2, 4)
        tree.update(3, 5)
        assert tree.get_value(0) == 3
        assert tree.get_value(1) == 4
        assert tree.get_value(2) == 5
        assert tree.get_value(3) == 6
        assert tree.range_sum(0, 3) == 18

    def test_update_invalid_index(self, config_file):
        """Test update with invalid index."""
        tree = FenwickTree(array=[1, 2, 3], config_path=config_file)
        with pytest.raises(ValueError):
            tree.update(-1, 5)
        with pytest.raises(ValueError):
            tree.update(10, 5)

    def test_set_value(self, config_file):
        """Test setting value."""
        tree = FenwickTree(array=[1, 2, 3, 4, 5], config_path=config_file)
        tree.set_value(2, 10)
        assert tree.get_value(2) == 10
        assert tree.prefix_sum(2) == 13

    def test_set_value_multiple(self, config_file):
        """Test setting multiple values."""
        tree = FenwickTree(array=[0, 0, 0, 0], config_path=config_file)
        tree.set_value(0, 1)
        tree.set_value(1, 2)
        tree.set_value(2, 3)
        tree.set_value(3, 4)
        assert tree.range_sum(0, 3) == 10

    def test_set_value_invalid_index(self, config_file):
        """Test set_value with invalid index."""
        tree = FenwickTree(array=[1, 2, 3], config_path=config_file)
        with pytest.raises(ValueError):
            tree.set_value(-1, 5)
        with pytest.raises(ValueError):
            tree.set_value(10, 5)

    def test_get_value(self, config_file):
        """Test getting value."""
        array = [1, 2, 3, 4, 5]
        tree = FenwickTree(array=array, config_path=config_file)
        for i in range(len(array)):
            assert tree.get_value(i) == array[i]

    def test_get_value_invalid_index(self, config_file):
        """Test get_value with invalid index."""
        tree = FenwickTree(array=[1, 2, 3], config_path=config_file)
        with pytest.raises(ValueError):
            tree.get_value(-1)
        with pytest.raises(ValueError):
            tree.get_value(10)

    def test_get_all_values(self, config_file):
        """Test getting all values."""
        array = [1, 2, 3, 4, 5]
        tree = FenwickTree(array=array, config_path=config_file)
        assert tree.get_all_values() == array

    def test_get_size(self, config_file):
        """Test getting size."""
        tree = FenwickTree(array=[1, 2, 3, 4, 5], config_path=config_file)
        assert tree.get_size() == 5

    def test_large_array(self, config_file):
        """Test with large array."""
        array = list(range(1, 101))
        tree = FenwickTree(array=array, config_path=config_file)
        assert tree.range_sum(0, 99) == sum(array)
        assert tree.range_sum(0, 49) == sum(array[:50])
        assert tree.range_sum(50, 99) == sum(array[50:])

    def test_all_zeros(self, config_file):
        """Test with all zeros."""
        tree = FenwickTree(array=[0, 0, 0, 0, 0], config_path=config_file)
        assert tree.range_sum(0, 4) == 0
        tree.update(2, 5)
        assert tree.get_value(2) == 5
        assert tree.range_sum(0, 4) == 5

    def test_negative_values(self, config_file):
        """Test with negative values."""
        array = [-1, -2, -3, -4, -5]
        tree = FenwickTree(array=array, config_path=config_file)
        assert tree.range_sum(0, 4) == -15
        tree.update(2, 10)
        assert tree.get_value(2) == 7
        assert tree.range_sum(0, 4) == -5

    def test_update_negative_delta(self, config_file):
        """Test update with negative delta."""
        tree = FenwickTree(array=[10, 20, 30, 40], config_path=config_file)
        tree.update(1, -5)
        assert tree.get_value(1) == 15
        assert tree.range_sum(0, 3) == 95

    def test_sequential_updates(self, config_file):
        """Test sequential updates and queries."""
        tree = FenwickTree(size=10, config_path=config_file)
        for i in range(10):
            tree.update(i, i + 1)
        assert tree.range_sum(0, 9) == 55
        for i in range(10):
            assert tree.get_value(i) == i + 1

    def test_range_sum_after_updates(self, config_file):
        """Test range sum after multiple updates."""
        tree = FenwickTree(array=[0] * 10, config_path=config_file)
        tree.update(0, 1)
        tree.update(5, 5)
        tree.update(9, 9)
        assert tree.range_sum(0, 9) == 15
        assert tree.range_sum(1, 4) == 0
        assert tree.range_sum(5, 8) == 5

    def test_is_valid(self, config_file):
        """Test tree validation."""
        array = [1, 2, 3, 4, 5]
        tree = FenwickTree(array=array, config_path=config_file)
        assert tree.is_valid() is True

    def test_is_valid_after_updates(self, config_file):
        """Test validation after updates."""
        tree = FenwickTree(array=[1, 2, 3, 4, 5], config_path=config_file)
        tree.update(2, 5)
        tree.set_value(0, 10)
        assert tree.is_valid() is True

    def test_prefix_sum_consistency(self, config_file):
        """Test prefix sum consistency."""
        array = [1, 3, 5, 7, 9]
        tree = FenwickTree(array=array, config_path=config_file)
        for i in range(len(array)):
            expected = sum(array[:i + 1])
            assert tree.prefix_sum(i) == expected

    def test_range_sum_consistency(self, config_file):
        """Test range sum consistency."""
        array = [1, 3, 5, 7, 9, 11]
        tree = FenwickTree(array=array, config_path=config_file)
        for left in range(len(array)):
            for right in range(left, len(array)):
                expected = sum(array[left:right + 1])
                assert tree.range_sum(left, right) == expected
