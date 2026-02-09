"""Unit tests for Aho-Corasick algorithm module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import AhoCorasickAlgorithm, TrieNode


class TestTrieNode:
    """Test cases for TrieNode class."""

    def test_trie_node_creation(self):
        """Test TrieNode creation."""
        node = TrieNode()
        assert node.children == {}
        assert node.failure is None
        assert node.output == set()
        assert node.is_end is False


class TestAhoCorasickAlgorithm:
    """Test cases for AhoCorasickAlgorithm class."""

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
    def ac(self, config_file):
        """Create AhoCorasickAlgorithm instance."""
        return AhoCorasickAlgorithm(
            ["he", "she", "his", "hers"], config_path=config_file
        )

    def test_aho_corasick_algorithm_creation(self, config_file):
        """Test AhoCorasickAlgorithm creation."""
        ac = AhoCorasickAlgorithm(["he", "she"], config_path=config_file)
        assert ac.get_pattern_count() == 2

    def test_aho_corasick_algorithm_empty_patterns(self):
        """Test creation with empty patterns list."""
        with pytest.raises(ValueError):
            AhoCorasickAlgorithm([])

    def test_aho_corasick_algorithm_all_empty_patterns(self):
        """Test creation with all empty patterns."""
        with pytest.raises(ValueError):
            AhoCorasickAlgorithm(["", "", ""])

    def test_search_existing_patterns(self, ac):
        """Test searching for existing patterns."""
        results = ac.search("ushers")
        assert "he" in results
        assert "she" in results
        assert len(results["he"]) > 0
        assert len(results["she"]) > 0

    def test_search_nonexistent_patterns(self, ac):
        """Test searching when patterns not found."""
        results = ac.search("xyz")
        assert all(len(positions) == 0 for positions in results.values())

    def test_search_empty_text(self, ac):
        """Test searching in empty text."""
        results = ac.search("")
        assert all(len(positions) == 0 for positions in results.values())

    def test_count_occurrences(self, ac):
        """Test counting occurrences."""
        counts = ac.count_occurrences("ushers")
        assert isinstance(counts, dict)
        assert "he" in counts
        assert counts["he"] > 0

    def test_find_all_occurrences(self, ac):
        """Test finding all occurrences."""
        occurrences = ac.find_all_occurrences("ushers")
        assert isinstance(occurrences, list)
        assert all(isinstance(occ, tuple) for occ in occurrences)

    def test_is_pattern_found(self, ac):
        """Test checking if pattern is found."""
        assert ac.is_pattern_found("ushers", "he") is True
        assert ac.is_pattern_found("xyz", "he") is False

    def test_is_pattern_found_invalid_pattern(self, ac):
        """Test is_pattern_found with invalid pattern."""
        with pytest.raises(ValueError):
            ac.is_pattern_found("text", "invalid")

    def test_get_patterns(self, ac):
        """Test getting patterns."""
        patterns = ac.get_patterns()
        assert isinstance(patterns, list)
        assert len(patterns) == 4

    def test_get_pattern_count(self, ac):
        """Test getting pattern count."""
        assert ac.get_pattern_count() == 4

    def test_single_pattern(self, config_file):
        """Test with single pattern."""
        ac = AhoCorasickAlgorithm(["abc"], config_path=config_file)
        results = ac.search("abc")
        assert len(results["abc"]) == 1

    def test_overlapping_patterns(self, config_file):
        """Test with overlapping patterns."""
        ac = AhoCorasickAlgorithm(["a", "aa", "aaa"], config_path=config_file)
        results = ac.search("aaa")
        assert len(results["a"]) == 3
        assert len(results["aa"]) == 2
        assert len(results["aaa"]) == 1

    def test_duplicate_patterns(self, config_file):
        """Test with duplicate patterns."""
        ac = AhoCorasickAlgorithm(
            ["abc", "abc", "def"], config_path=config_file
        )
        assert ac.get_pattern_count() == 3
        results = ac.search("abcdef")
        assert len(results["abc"]) > 0

    def test_long_text(self, config_file):
        """Test with longer text."""
        patterns = ["he", "she", "his", "hers"]
        ac = AhoCorasickAlgorithm(patterns, config_path=config_file)
        text = "ushers" * 10
        results = ac.search(text)
        assert all(len(positions) > 0 for pattern, positions in results.items() if pattern in ["he", "she"])

    def test_multiple_occurrences(self, config_file):
        """Test with multiple occurrences."""
        ac = AhoCorasickAlgorithm(["ab"], config_path=config_file)
        results = ac.search("ababab")
        assert len(results["ab"]) == 3

    def test_pattern_at_start(self, config_file):
        """Test pattern at start of text."""
        ac = AhoCorasickAlgorithm(["abc"], config_path=config_file)
        results = ac.search("abcdef")
        assert 0 in results["abc"]

    def test_pattern_at_end(self, config_file):
        """Test pattern at end of text."""
        ac = AhoCorasickAlgorithm(["abc"], config_path=config_file)
        results = ac.search("defabc")
        assert 3 in results["abc"]

    def test_single_character_patterns(self, config_file):
        """Test with single character patterns."""
        ac = AhoCorasickAlgorithm(["a", "b", "c"], config_path=config_file)
        results = ac.search("abc")
        assert len(results["a"]) == 1
        assert len(results["b"]) == 1
        assert len(results["c"]) == 1

    def test_all_occurrences_sorted(self, config_file):
        """Test that all occurrences are sorted by position."""
        ac = AhoCorasickAlgorithm(["ab"], config_path=config_file)
        occurrences = ac.find_all_occurrences("ababab")
        positions = [occ[1] for occ in occurrences]
        assert positions == sorted(positions)

    def test_count_occurrences_consistency(self, config_file):
        """Test count occurrences consistency."""
        ac = AhoCorasickAlgorithm(["ab"], config_path=config_file)
        results = ac.search("ababab")
        counts = ac.count_occurrences("ababab")
        assert counts["ab"] == len(results["ab"])

    def test_search_results_structure(self, ac):
        """Test search results structure."""
        results = ac.search("ushers")
        assert isinstance(results, dict)
        assert all(isinstance(positions, list) for positions in results.values())
        assert all(isinstance(pos, int) for positions in results.values() for pos in positions)

    def test_find_all_occurrences_structure(self, ac):
        """Test find_all_occurrences structure."""
        occurrences = ac.find_all_occurrences("ushers")
        assert all(len(occ) == 3 for occ in occurrences)
        assert all(isinstance(occ[0], str) for occ in occurrences)
        assert all(isinstance(occ[1], int) for occ in occurrences)
        assert all(isinstance(occ[2], int) for occ in occurrences)

    def test_pattern_not_in_text(self, config_file):
        """Test when pattern not in text."""
        ac = AhoCorasickAlgorithm(["xyz"], config_path=config_file)
        results = ac.search("abc")
        assert len(results["xyz"]) == 0

    def test_empty_pattern_in_list(self, config_file):
        """Test with empty pattern in list."""
        ac = AhoCorasickAlgorithm(["abc", "def"], config_path=config_file)
        assert ac.get_pattern_count() == 2
