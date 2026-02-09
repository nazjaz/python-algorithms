"""Unit tests for van Emde Boas tree module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import VEBNode, VanEmdeBoasTree


class TestVEBNode:
    """Test cases for VEBNode class."""

    def test_node_creation_power_of_2(self):
        """Test VEBNode creation with power of 2."""
        node = VEBNode(2)
        assert node.universe_size == 2
        assert node.min is None
        assert node.max is None

    def test_node_creation_larger(self):
        """Test VEBNode creation with larger universe."""
        node = VEBNode(16)
        assert node.universe_size == 16
        assert node.clusters is not None
        assert node.summary is not None

    def test_node_creation_not_power_of_2(self):
        """Test VEBNode creation with non-power of 2."""
        with pytest.raises(ValueError):
            VEBNode(3)

        with pytest.raises(ValueError):
            VEBNode(10)

    def test_is_empty(self):
        """Test is_empty method."""
        node = VEBNode(2)
        assert node.is_empty() is True

        node.min = 0
        assert node.is_empty() is False

    def test_high_low_index(self):
        """Test high, low, and index methods."""
        node = VEBNode(16)
        x = 10

        high = node.high(x)
        low = node.low(x)
        reconstructed = node.index(high, low)

        assert reconstructed == x

    def test_node_repr(self):
        """Test VEBNode string representation."""
        node = VEBNode(4)
        assert "VEBNode" in repr(node)


class TestVanEmdeBoasTree:
    """Test cases for VanEmdeBoasTree class."""

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
    def tree(self, config_file):
        """Create VanEmdeBoasTree instance."""
        return VanEmdeBoasTree(universe_size=16, config_path=config_file)

    def test_tree_creation(self, config_file):
        """Test VanEmdeBoasTree creation."""
        tree = VanEmdeBoasTree(universe_size=16, config_path=config_file)
        assert tree.universe_size == 16
        assert tree.size == 0
        assert tree.is_empty() is True

    def test_tree_creation_not_power_of_2(self, config_file):
        """Test tree creation with non-power of 2."""
        with pytest.raises(ValueError):
            VanEmdeBoasTree(universe_size=10, config_path=config_file)

    def test_insert_operation(self, tree):
        """Test insert operation."""
        result = tree.insert(5)
        assert result is True
        assert tree.size == 1
        assert tree.contains(5) is True

    def test_insert_duplicate(self, tree):
        """Test inserting duplicate value."""
        tree.insert(5)
        result = tree.insert(5)
        assert result is False
        assert tree.size == 1

    def test_insert_out_of_bounds(self, tree):
        """Test inserting value out of universe."""
        with pytest.raises(ValueError):
            tree.insert(-1)

        with pytest.raises(ValueError):
            tree.insert(16)

    def test_delete_operation(self, tree):
        """Test delete operation."""
        tree.insert(5)
        result = tree.delete(5)
        assert result is True
        assert tree.size == 0
        assert tree.contains(5) is False

    def test_delete_not_found(self, tree):
        """Test deleting non-existent value."""
        result = tree.delete(5)
        assert result is False

    def test_delete_out_of_bounds(self, tree):
        """Test deleting value out of universe."""
        with pytest.raises(ValueError):
            tree.delete(-1)

        with pytest.raises(ValueError):
            tree.delete(16)

    def test_contains_operation(self, tree):
        """Test contains operation."""
        tree.insert(5)
        assert tree.contains(5) is True
        assert tree.contains(3) is False

    def test_contains_out_of_bounds(self, tree):
        """Test contains with value out of universe."""
        with pytest.raises(ValueError):
            tree.contains(-1)

        with pytest.raises(ValueError):
            tree.contains(16)

    def test_get_min_empty(self, tree):
        """Test get_min on empty tree."""
        assert tree.get_min() is None

    def test_get_min(self, tree):
        """Test get_min operation."""
        tree.insert(5)
        tree.insert(3)
        tree.insert(7)
        assert tree.get_min() == 3

    def test_get_max_empty(self, tree):
        """Test get_max on empty tree."""
        assert tree.get_max() is None

    def test_get_max(self, tree):
        """Test get_max operation."""
        tree.insert(5)
        tree.insert(3)
        tree.insert(7)
        assert tree.get_max() == 7

    def test_predecessor_operation(self, tree):
        """Test predecessor operation."""
        tree.insert(2)
        tree.insert(5)
        tree.insert(7)

        pred = tree.predecessor(5)
        assert pred == 2

        pred = tree.predecessor(7)
        assert pred == 5

        pred = tree.predecessor(2)
        assert pred is None

    def test_predecessor_out_of_bounds(self, tree):
        """Test predecessor with value out of universe."""
        with pytest.raises(ValueError):
            tree.predecessor(-1)

        with pytest.raises(ValueError):
            tree.predecessor(16)

    def test_successor_operation(self, tree):
        """Test successor operation."""
        tree.insert(2)
        tree.insert(5)
        tree.insert(7)

        succ = tree.successor(2)
        assert succ == 5

        succ = tree.successor(5)
        assert succ == 7

        succ = tree.successor(7)
        assert succ is None

    def test_successor_out_of_bounds(self, tree):
        """Test successor with value out of universe."""
        with pytest.raises(ValueError):
            tree.successor(-1)

        with pytest.raises(ValueError):
            tree.successor(16)

    def test_complex_operations(self, tree):
        """Test complex sequence of operations."""
        values = [2, 3, 5, 7, 11, 13]
        for value in values:
            tree.insert(value)

        assert tree.get_min() == 2
        assert tree.get_max() == 13
        assert tree.size == 6

        pred = tree.predecessor(7)
        assert pred == 5

        succ = tree.successor(7)
        assert succ == 11

        tree.delete(7)
        assert tree.size == 5
        assert tree.contains(7) is False

        pred = tree.predecessor(11)
        assert pred == 5

    def test_universe_size_2(self, config_file):
        """Test with universe size 2."""
        tree = VanEmdeBoasTree(universe_size=2, config_path=config_file)
        tree.insert(0)
        tree.insert(1)

        assert tree.get_min() == 0
        assert tree.get_max() == 1
        assert tree.contains(0) is True
        assert tree.contains(1) is True

    def test_large_universe(self, config_file):
        """Test with larger universe."""
        tree = VanEmdeBoasTree(universe_size=256, config_path=config_file)
        tree.insert(100)
        tree.insert(200)
        tree.insert(50)

        assert tree.get_min() == 50
        assert tree.get_max() == 200
        assert tree.contains(100) is True

    def test_insert_delete_sequence(self, tree):
        """Test insert and delete sequence."""
        for i in range(8):
            tree.insert(i)

        assert tree.size == 8

        for i in range(0, 8, 2):
            tree.delete(i)

        assert tree.size == 4
        assert tree.get_min() == 1
        assert tree.get_max() == 7

    def test_predecessor_successor_consistency(self, tree):
        """Test consistency between predecessor and successor."""
        tree.insert(2)
        tree.insert(5)
        tree.insert(7)

        pred = tree.predecessor(7)
        succ = tree.successor(pred) if pred is not None else None
        assert succ == 7

        succ = tree.successor(2)
        pred = tree.predecessor(succ) if succ is not None else None
        assert pred == 2
