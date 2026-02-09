"""Unit tests for rope data structure module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import Rope, RopeNode


class TestRopeNode:
    """Test cases for RopeNode class."""

    def test_node_creation_leaf(self):
        """Test RopeNode creation as leaf."""
        node = RopeNode(data="hello")
        assert node.data == "hello"
        assert node.length == 5
        assert node.weight == 0
        assert node.is_leaf() is True

    def test_node_creation_internal(self):
        """Test RopeNode creation as internal node."""
        left = RopeNode(data="hello")
        right = RopeNode(data="world")
        node = RopeNode(left=left, right=right)
        node.update_weight()

        assert node.left == left
        assert node.right == right
        assert node.weight == 5
        assert node.length == 10
        assert node.is_leaf() is False

    def test_node_repr(self):
        """Test RopeNode string representation."""
        node = RopeNode(data="test")
        assert "RopeNode" in repr(node)


class TestRope:
    """Test cases for Rope class."""

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
    def rope(self, config_file):
        """Create Rope instance."""
        return Rope("Hello World", config_path=config_file)

    def test_rope_creation(self, config_file):
        """Test Rope creation."""
        rope = Rope("test", config_path=config_file)
        assert rope.get_length() == 4
        assert rope.to_string() == "test"

    def test_empty_rope_creation(self, config_file):
        """Test empty Rope creation."""
        rope = Rope("", config_path=config_file)
        assert rope.get_length() == 0
        assert rope.to_string() == ""

    def test_concatenate(self, config_file):
        """Test concatenate operation."""
        rope1 = Rope("Hello", config_path=config_file)
        rope2 = Rope(" World", config_path=config_file)

        rope3 = rope1.concatenate(rope2)
        assert rope3.to_string() == "Hello World"
        assert rope1.to_string() == "Hello"
        assert rope2.to_string() == " World"

    def test_concatenate_empty(self, config_file):
        """Test concatenate with empty rope."""
        rope1 = Rope("Hello", config_path=config_file)
        rope2 = Rope("", config_path=config_file)

        rope3 = rope1.concatenate(rope2)
        assert rope3.to_string() == "Hello"

    def test_substring(self, rope):
        """Test substring operation."""
        substr = rope.substring(0, 5)
        assert substr.to_string() == "Hello"

        substr = rope.substring(6, 11)
        assert substr.to_string() == "World"

    def test_substring_invalid_indices(self, rope):
        """Test substring with invalid indices."""
        with pytest.raises(IndexError):
            rope.substring(-1, 5)

        with pytest.raises(IndexError):
            rope.substring(5, 3)

        with pytest.raises(IndexError):
            rope.substring(0, 100)

    def test_substring_empty_rope(self, config_file):
        """Test substring on empty rope."""
        rope = Rope("", config_path=config_file)
        substr = rope.substring(0, 0)
        assert substr.to_string() == ""

    def test_insert(self, rope):
        """Test insert operation."""
        new_rope = rope.insert(5, " Beautiful")
        assert new_rope.to_string() == "Hello Beautiful World"
        assert rope.to_string() == "Hello World"

    def test_insert_at_start(self, rope):
        """Test insert at start."""
        new_rope = rope.insert(0, "Say ")
        assert new_rope.to_string() == "Say Hello World"

    def test_insert_at_end(self, rope):
        """Test insert at end."""
        new_rope = rope.insert(11, "!")
        assert new_rope.to_string() == "Hello World!"

    def test_insert_invalid_index(self, rope):
        """Test insert with invalid index."""
        with pytest.raises(IndexError):
            rope.insert(-1, "test")

        with pytest.raises(IndexError):
            rope.insert(100, "test")

    def test_delete(self, rope):
        """Test delete operation."""
        new_rope = rope.delete(5, 11)
        assert new_rope.to_string() == "Hello"
        assert rope.to_string() == "Hello World"

    def test_delete_at_start(self, rope):
        """Test delete at start."""
        new_rope = rope.delete(0, 6)
        assert new_rope.to_string() == "World"

    def test_delete_at_end(self, rope):
        """Test delete at end."""
        new_rope = rope.delete(5, 11)
        assert new_rope.to_string() == "Hello"

    def test_delete_invalid_indices(self, rope):
        """Test delete with invalid indices."""
        with pytest.raises(IndexError):
            rope.delete(-1, 5)

        with pytest.raises(IndexError):
            rope.delete(5, 3)

        with pytest.raises(IndexError):
            rope.delete(0, 100)

    def test_get_char(self, rope):
        """Test get_char operation."""
        assert rope.get_char(0) == "H"
        assert rope.get_char(6) == "W"
        assert rope.get_char(10) == "d"

    def test_get_char_invalid_index(self, rope):
        """Test get_char with invalid index."""
        with pytest.raises(IndexError):
            rope.get_char(-1)

        with pytest.raises(IndexError):
            rope.get_char(100)

    def test_get_char_empty_rope(self, config_file):
        """Test get_char on empty rope."""
        rope = Rope("", config_path=config_file)
        with pytest.raises(IndexError):
            rope.get_char(0)

    def test_get_length(self, rope):
        """Test get_length operation."""
        assert rope.get_length() == 11

    def test_to_string(self, rope):
        """Test to_string operation."""
        assert rope.to_string() == "Hello World"

    def test_complex_operations(self, config_file):
        """Test complex sequence of operations."""
        rope = Rope("Hello", config_path=config_file)

        rope = rope.concatenate(Rope(" World", config_path=config_file))
        assert rope.to_string() == "Hello World"

        rope = rope.insert(5, " Beautiful")
        assert rope.to_string() == "Hello Beautiful World"

        rope = rope.delete(5, 15)
        assert rope.to_string() == "Hello World"

    def test_multiple_concatenations(self, config_file):
        """Test multiple concatenations."""
        rope1 = Rope("A", config_path=config_file)
        rope2 = Rope("B", config_path=config_file)
        rope3 = Rope("C", config_path=config_file)

        rope = rope1.concatenate(rope2).concatenate(rope3)
        assert rope.to_string() == "ABC"

    def test_large_string(self, config_file):
        """Test with large string."""
        large_string = "A" * 1000
        rope = Rope(large_string, config_path=config_file)

        assert rope.get_length() == 1000
        assert rope.to_string() == large_string

        substr = rope.substring(0, 100)
        assert substr.to_string() == "A" * 100
