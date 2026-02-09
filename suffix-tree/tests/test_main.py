"""Unit tests for suffix tree module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import SuffixTree, SuffixTreeNode


class TestSuffixTreeNode:
    """Test cases for SuffixTreeNode class."""

    def test_suffix_tree_node_creation(self):
        """Test SuffixTreeNode creation."""
        node = SuffixTreeNode(start=0, end=5)
        assert node.start == 0
        assert node.end == 5
        assert node.suffix_link is None
        assert len(node.children) == 0

    def test_edge_length(self):
        """Test edge length calculation."""
        node = SuffixTreeNode(start=0, end=5)
        assert node.edge_length(10) == 5

        node_end = SuffixTreeNode(start=0, end=-1)
        assert node_end.edge_length(10) == 10

    def test_get_edge_label(self):
        """Test getting edge label."""
        text = "banana"
        node = SuffixTreeNode(start=0, end=3)
        assert node.get_edge_label(text) == "ban"

        node_end = SuffixTreeNode(start=0, end=-1)
        assert node_end.get_edge_label(text) == "banana"


class TestSuffixTree:
    """Test cases for SuffixTree class."""

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

    def test_suffix_tree_creation(self, config_file):
        """Test SuffixTree creation."""
        tree = SuffixTree("banana", config_path=config_file)
        assert tree.text == "banana$"
        assert tree.root is not None
        assert tree.get_tree_size() > 0

    def test_suffix_tree_empty_text(self):
        """Test SuffixTree creation with empty text."""
        with pytest.raises(ValueError):
            SuffixTree("")

    def test_search_existing_pattern(self, config_file):
        """Test searching for existing pattern."""
        tree = SuffixTree("banana", config_path=config_file)
        assert tree.search("ban") is True
        assert tree.search("ana") is True
        assert tree.search("nan") is True
        assert tree.search("a") is True

    def test_search_nonexistent_pattern(self, config_file):
        """Test searching for nonexistent pattern."""
        tree = SuffixTree("banana", config_path=config_file)
        assert tree.search("xyz") is False
        assert tree.search("banx") is False

    def test_search_empty_pattern(self, config_file):
        """Test searching for empty pattern."""
        tree = SuffixTree("banana", config_path=config_file)
        assert tree.search("") is True

    def test_find_all_occurrences(self, config_file):
        """Test finding all occurrences."""
        tree = SuffixTree("banana", config_path=config_file)
        occurrences = tree.find_all_occurrences("ana")
        assert len(occurrences) > 0
        assert all(
            tree.text[occ:occ + 3] == "ana" for occ in occurrences
        )

    def test_find_all_occurrences_nonexistent(self, config_file):
        """Test finding occurrences of nonexistent pattern."""
        tree = SuffixTree("banana", config_path=config_file)
        occurrences = tree.find_all_occurrences("xyz")
        assert len(occurrences) == 0

    def test_find_all_occurrences_single_char(self, config_file):
        """Test finding occurrences of single character."""
        tree = SuffixTree("banana", config_path=config_file)
        occurrences = tree.find_all_occurrences("a")
        assert len(occurrences) >= 3

    def test_get_substring_count(self, config_file):
        """Test counting substring occurrences."""
        tree = SuffixTree("banana", config_path=config_file)
        count = tree.get_substring_count("ana")
        assert count > 0

        count_nonexistent = tree.get_substring_count("xyz")
        assert count_nonexistent == 0

    def test_is_suffix(self, config_file):
        """Test checking if pattern is suffix."""
        tree = SuffixTree("banana", config_path=config_file)
        assert tree.is_suffix("ana") is True
        assert tree.is_suffix("banana") is True
        assert tree.is_suffix("ban") is False
        assert tree.is_suffix("") is True

    def test_get_longest_repeated_substring(self, config_file):
        """Test finding longest repeated substring."""
        tree = SuffixTree("banana", config_path=config_file)
        longest = tree.get_longest_repeated_substring()
        assert len(longest) > 0
        assert longest in "banana"

    def test_get_all_suffixes(self, config_file):
        """Test getting all suffixes."""
        tree = SuffixTree("banana", config_path=config_file)
        suffixes = tree.get_all_suffixes()
        assert len(suffixes) > 0
        assert "" in suffixes or "$" in "".join(suffixes)

    def test_get_tree_size(self, config_file):
        """Test getting tree size."""
        tree = SuffixTree("banana", config_path=config_file)
        size = tree.get_tree_size()
        assert size > 0

    def test_is_valid(self, config_file):
        """Test tree validation."""
        tree = SuffixTree("banana", config_path=config_file)
        assert tree.is_valid() is True

    def test_simple_text(self, config_file):
        """Test with simple text."""
        tree = SuffixTree("abc", config_path=config_file)
        assert tree.search("a") is True
        assert tree.search("b") is True
        assert tree.search("c") is True
        assert tree.search("ab") is True
        assert tree.search("bc") is True
        assert tree.search("abc") is True

    def test_repeated_characters(self, config_file):
        """Test with repeated characters."""
        tree = SuffixTree("aaa", config_path=config_file)
        assert tree.search("a") is True
        assert tree.search("aa") is True
        assert tree.search("aaa") is True

    def test_long_text(self, config_file):
        """Test with longer text."""
        text = "mississippi"
        tree = SuffixTree(text, config_path=config_file)
        assert tree.search("miss") is True
        assert tree.search("issi") is True
        assert tree.search("ssi") is True
        assert tree.search("ppi") is True

    def test_find_occurrences_long_text(self, config_file):
        """Test finding occurrences in long text."""
        text = "mississippi"
        tree = SuffixTree(text, config_path=config_file)
        occurrences = tree.find_all_occurrences("ssi")
        assert len(occurrences) == 2

    def test_all_substrings_exist(self, config_file):
        """Test that all substrings can be found."""
        text = "abc"
        tree = SuffixTree(text, config_path=config_file)
        substrings = ["a", "b", "c", "ab", "bc", "abc"]
        for substring in substrings:
            assert tree.search(substring) is True

    def test_single_character_text(self, config_file):
        """Test with single character."""
        tree = SuffixTree("a", config_path=config_file)
        assert tree.search("a") is True
        assert tree.search("") is True
        assert tree.is_suffix("a") is True

    def test_no_repeated_substring(self, config_file):
        """Test text with no repeated substrings."""
        tree = SuffixTree("abcdef", config_path=config_file)
        longest = tree.get_longest_repeated_substring()
        assert longest == ""

    def test_multiple_occurrences(self, config_file):
        """Test pattern with multiple occurrences."""
        tree = SuffixTree("ababab", config_path=config_file)
        occurrences = tree.find_all_occurrences("ab")
        assert len(occurrences) == 3

    def test_overlapping_patterns(self, config_file):
        """Test overlapping patterns."""
        tree = SuffixTree("aaaa", config_path=config_file)
        occurrences = tree.find_all_occurrences("aa")
        assert len(occurrences) == 3

    def test_tree_structure(self, config_file):
        """Test tree structure validity."""
        tree = SuffixTree("banana", config_path=config_file)
        assert tree.root is not None
        assert len(tree.root.children) > 0
        assert tree.is_valid() is True
