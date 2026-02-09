"""Unit tests for skip list module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import SkipList, SkipListNode


class TestSkipListNode:
    """Test cases for SkipListNode class."""

    def test_skip_list_node_creation(self):
        """Test SkipListNode creation."""
        node = SkipListNode(10, 20, 3)
        assert node.key == 10
        assert node.value == 20
        assert node.level == 3
        assert len(node.forward) == 4

    def test_skip_list_node_defaults(self):
        """Test SkipListNode with default values."""
        node = SkipListNode(10)
        assert node.key == 10
        assert node.value is None
        assert node.level == 0
        assert len(node.forward) == 1


class TestSkipList:
    """Test cases for SkipList class."""

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
    def skip_list(self, config_file):
        """Create SkipList instance."""
        return SkipList(max_level=4, probability=0.5, config_path=config_file)

    def test_skip_list_creation(self, skip_list):
        """Test SkipList creation."""
        assert skip_list.max_level == 4
        assert skip_list.probability == 0.5
        assert skip_list.get_size() == 0
        assert skip_list.is_empty() is True

    def test_skip_list_invalid_max_level(self):
        """Test creation with invalid max level."""
        with pytest.raises(ValueError):
            SkipList(max_level=0)

    def test_skip_list_invalid_probability(self):
        """Test creation with invalid probability."""
        with pytest.raises(ValueError):
            SkipList(probability=0)
        with pytest.raises(ValueError):
            SkipList(probability=1)
        with pytest.raises(ValueError):
            SkipList(probability=-0.1)
        with pytest.raises(ValueError):
            SkipList(probability=1.1)

    def test_insert_single_key(self, skip_list):
        """Test inserting single key."""
        result = skip_list.insert(10, 20)
        assert result is True
        assert skip_list.get_size() == 1
        assert skip_list.is_empty() is False

    def test_insert_multiple_keys(self, skip_list):
        """Test inserting multiple keys."""
        keys = [10, 20, 30, 40, 50]
        for key in keys:
            result = skip_list.insert(key)
            assert result is True
        assert skip_list.get_size() == len(keys)

    def test_insert_duplicate(self, skip_list):
        """Test inserting duplicate key."""
        skip_list.insert(10)
        result = skip_list.insert(10)
        assert result is False
        assert skip_list.get_size() == 1

    def test_search_existing(self, skip_list):
        """Test searching for existing key."""
        skip_list.insert(10, 20)
        skip_list.insert(20, 40)
        found, value = skip_list.search(10)
        assert found is True
        assert value == 20

    def test_search_nonexistent(self, skip_list):
        """Test searching for nonexistent key."""
        skip_list.insert(10)
        found, value = skip_list.search(20)
        assert found is False
        assert value is None

    def test_search_empty(self, skip_list):
        """Test searching in empty skip list."""
        found, value = skip_list.search(10)
        assert found is False
        assert value is None

    def test_delete_existing(self, skip_list):
        """Test deleting existing key."""
        skip_list.insert(10)
        skip_list.insert(20)
        result = skip_list.delete(10)
        assert result is True
        assert skip_list.get_size() == 1
        found, _ = skip_list.search(10)
        assert found is False

    def test_delete_nonexistent(self, skip_list):
        """Test deleting nonexistent key."""
        skip_list.insert(10)
        result = skip_list.delete(20)
        assert result is False
        assert skip_list.get_size() == 1

    def test_delete_empty(self, skip_list):
        """Test deleting from empty skip list."""
        result = skip_list.delete(10)
        assert result is False

    def test_get_all_keys(self, skip_list):
        """Test getting all keys."""
        keys = [30, 10, 50, 20, 40]
        for key in keys:
            skip_list.insert(key)
        all_keys = skip_list.get_all_keys()
        assert all_keys == sorted(keys)

    def test_get_all_items(self, skip_list):
        """Test getting all items."""
        skip_list.insert(10, 20)
        skip_list.insert(20, 40)
        items = skip_list.get_all_items()
        assert len(items) == 2
        assert (10, 20) in items
        assert (20, 40) in items

    def test_get_range(self, skip_list):
        """Test getting range of items."""
        for i in range(1, 11):
            skip_list.insert(i * 10, i * 20)
        range_items = skip_list.get_range(30, 70)
        assert len(range_items) == 5
        keys = [item[0] for item in range_items]
        assert keys == [30, 40, 50, 60, 70]

    def test_get_range_empty(self, skip_list):
        """Test getting range with no matches."""
        skip_list.insert(10)
        skip_list.insert(20)
        range_items = skip_list.get_range(50, 100)
        assert len(range_items) == 0

    def test_get_range_invalid(self, skip_list):
        """Test getting range with invalid bounds."""
        skip_list.insert(10)
        range_items = skip_list.get_range(20, 10)
        assert len(range_items) == 0

    def test_get_min_key(self, skip_list):
        """Test getting minimum key."""
        assert skip_list.get_min_key() is None
        skip_list.insert(30)
        skip_list.insert(10)
        skip_list.insert(20)
        assert skip_list.get_min_key() == 10

    def test_get_max_key(self, skip_list):
        """Test getting maximum key."""
        assert skip_list.get_max_key() is None
        skip_list.insert(10)
        skip_list.insert(30)
        skip_list.insert(20)
        assert skip_list.get_max_key() == 30

    def test_clear(self, skip_list):
        """Test clearing skip list."""
        skip_list.insert(10)
        skip_list.insert(20)
        skip_list.clear()
        assert skip_list.get_size() == 0
        assert skip_list.is_empty() is True

    def test_is_valid(self, skip_list):
        """Test skip list validation."""
        assert skip_list.is_valid() is True
        skip_list.insert(10)
        skip_list.insert(20)
        assert skip_list.is_valid() is True

    def test_is_valid_after_deletions(self, skip_list):
        """Test validation after deletions."""
        for i in range(10):
            skip_list.insert(i * 10)
        assert skip_list.is_valid() is True
        skip_list.delete(50)
        assert skip_list.is_valid() is True

    def test_large_insertions(self, config_file):
        """Test with large number of insertions."""
        skip_list = SkipList(max_level=8, config_path=config_file)
        for i in range(100):
            skip_list.insert(i)
        assert skip_list.get_size() == 100
        assert skip_list.is_valid() is True

    def test_sequential_operations(self, skip_list):
        """Test sequential insert and delete operations."""
        for i in range(20):
            skip_list.insert(i)
        assert skip_list.get_size() == 20

        for i in range(0, 20, 2):
            skip_list.delete(i)
        assert skip_list.get_size() == 10

        for i in range(1, 20, 2):
            found, _ = skip_list.search(i)
            assert found is True

    def test_get_current_level(self, skip_list):
        """Test getting current level."""
        level = skip_list.get_current_level()
        assert level >= 0
        assert level <= skip_list.max_level

    def test_level_increases_with_insertions(self, config_file):
        """Test that level may increase with insertions."""
        skip_list = SkipList(max_level=4, probability=0.5, config_path=config_file)
        initial_level = skip_list.get_current_level()

        for i in range(50):
            skip_list.insert(i)

        assert skip_list.get_current_level() >= initial_level

    def test_sorted_order(self, skip_list):
        """Test that keys remain in sorted order."""
        keys = [50, 10, 30, 20, 40, 5, 15, 25, 35, 45]
        for key in keys:
            skip_list.insert(key)

        all_keys = skip_list.get_all_keys()
        assert all_keys == sorted(keys)

    def test_search_after_deletion(self, skip_list):
        """Test search after deletion."""
        skip_list.insert(10)
        skip_list.insert(20)
        skip_list.insert(30)

        skip_list.delete(20)
        found, _ = skip_list.search(20)
        assert found is False

        found, _ = skip_list.search(10)
        assert found is True
        found, _ = skip_list.search(30)
        assert found is True
