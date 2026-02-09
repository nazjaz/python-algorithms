"""Unit tests for treap module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import Treap, TreapNode


class TestTreapNode:
    """Test cases for TreapNode class."""

    def test_treap_node_creation(self):
        """Test TreapNode creation."""
        node = TreapNode(10, 5)
        assert node.key == 10
        assert node.priority == 5
        assert node.left is None
        assert node.right is None

    def test_treap_node_random_priority(self):
        """Test TreapNode with random priority."""
        node = TreapNode(10)
        assert node.key == 10
        assert node.priority is not None
        assert 1 <= node.priority <= 10**9


class TestTreap:
    """Test cases for Treap class."""

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
    def treap(self, config_file):
        """Create Treap instance."""
        return Treap(config_path=config_file)

    def test_treap_creation(self, treap):
        """Test Treap creation."""
        assert treap.get_size() == 0
        assert treap.is_empty() is True
        assert treap.root is None

    def test_insert_single_key(self, treap):
        """Test inserting single key."""
        result = treap.insert(10)
        assert result is True
        assert treap.get_size() == 1
        assert treap.is_empty() is False

    def test_insert_multiple_keys(self, treap):
        """Test inserting multiple keys."""
        keys = [10, 20, 30, 40, 50]
        for key in keys:
            result = treap.insert(key)
            assert result is True
        assert treap.get_size() == len(keys)

    def test_insert_duplicate(self, treap):
        """Test inserting duplicate key."""
        treap.insert(10)
        result = treap.insert(10)
        assert result is False
        assert treap.get_size() == 1

    def test_search_existing(self, treap):
        """Test searching for existing key."""
        treap.insert(10)
        treap.insert(20)
        assert treap.search(10) is True
        assert treap.search(20) is True

    def test_search_nonexistent(self, treap):
        """Test searching for nonexistent key."""
        treap.insert(10)
        assert treap.search(20) is False

    def test_search_empty(self, treap):
        """Test searching in empty treap."""
        assert treap.search(10) is False

    def test_delete_existing(self, treap):
        """Test deleting existing key."""
        treap.insert(10)
        treap.insert(20)
        result = treap.delete(10)
        assert result is True
        assert treap.get_size() == 1
        assert treap.search(10) is False

    def test_delete_nonexistent(self, treap):
        """Test deleting nonexistent key."""
        treap.insert(10)
        result = treap.delete(20)
        assert result is False
        assert treap.get_size() == 1

    def test_delete_empty(self, treap):
        """Test deleting from empty treap."""
        result = treap.delete(10)
        assert result is False

    def test_get_all_keys(self, treap):
        """Test getting all keys."""
        keys = [30, 10, 50, 20, 40]
        for key in keys:
            treap.insert(key)
        all_keys = treap.get_all_keys()
        assert all_keys == sorted(keys)

    def test_get_min_key(self, treap):
        """Test getting minimum key."""
        assert treap.get_min_key() is None
        treap.insert(30)
        treap.insert(10)
        treap.insert(20)
        assert treap.get_min_key() == 10

    def test_get_max_key(self, treap):
        """Test getting maximum key."""
        assert treap.get_max_key() is None
        treap.insert(10)
        treap.insert(30)
        treap.insert(20)
        assert treap.get_max_key() == 30

    def test_clear(self, treap):
        """Test clearing treap."""
        treap.insert(10)
        treap.insert(20)
        treap.clear()
        assert treap.get_size() == 0
        assert treap.is_empty() is True

    def test_is_valid(self, treap):
        """Test treap validation."""
        assert treap.is_valid() is True
        treap.insert(10)
        treap.insert(20)
        assert treap.is_valid() is True

    def test_is_valid_after_deletions(self, treap):
        """Test validation after deletions."""
        for i in range(10):
            treap.insert(i * 10)
        assert treap.is_valid() is True
        treap.delete(50)
        assert treap.is_valid() is True

    def test_large_insertions(self, config_file):
        """Test with large number of insertions."""
        treap = Treap(config_path=config_file)
        for i in range(100):
            treap.insert(i)
        assert treap.get_size() == 100
        assert treap.is_valid() is True

    def test_sequential_operations(self, treap):
        """Test sequential insert and delete operations."""
        for i in range(20):
            treap.insert(i)
        assert treap.get_size() == 20

        for i in range(0, 20, 2):
            treap.delete(i)
        assert treap.get_size() == 10

        for i in range(1, 20, 2):
            assert treap.search(i) is True

    def test_split(self, treap):
        """Test splitting treap."""
        for i in range(1, 11):
            treap.insert(i * 10)

        left, right = treap.split(50)
        assert left.get_size() > 0
        assert right.get_size() > 0
        assert left.is_valid() is True
        assert right.is_valid() is True

        left_keys = left.get_all_keys()
        right_keys = right.get_all_keys()

        assert all(k < 50 for k in left_keys)
        assert all(k >= 50 for k in right_keys)

    def test_merge(self, treap):
        """Test merging treaps."""
        for i in range(1, 6):
            treap.insert(i * 10)

        left, right = treap.split(30)
        merged = left.merge(right)

        assert merged.get_size() == 5
        assert merged.is_valid() is True
        assert merged.get_all_keys() == [10, 20, 30, 40, 50]

    def test_split_empty(self, treap):
        """Test splitting empty treap."""
        left, right = treap.split(50)
        assert left.get_size() == 0
        assert right.get_size() == 0

    def test_merge_with_empty(self, treap):
        """Test merging with empty treap."""
        treap.insert(10)
        empty = Treap()
        merged = treap.merge(empty)
        assert merged.get_size() == 1

    def test_sorted_order(self, treap):
        """Test that keys remain in sorted order."""
        keys = [50, 10, 30, 20, 40, 5, 15, 25, 35, 45]
        for key in keys:
            treap.insert(key)

        all_keys = treap.get_all_keys()
        assert all_keys == sorted(keys)

    def test_search_after_deletion(self, treap):
        """Test search after deletion."""
        treap.insert(10)
        treap.insert(20)
        treap.insert(30)

        treap.delete(20)
        assert treap.search(20) is False

        assert treap.search(10) is True
        assert treap.search(30) is True
