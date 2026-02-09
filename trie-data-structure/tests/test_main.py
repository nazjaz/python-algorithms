"""Unit tests for trie data structure module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import Trie, TrieNode


class TestTrieNode:
    """Test cases for TrieNode class."""

    def test_trie_node_creation(self):
        """Test TrieNode creation."""
        node = TrieNode()
        assert len(node.children) == 0
        assert node.is_end_of_word is False
        assert node.word_count == 0


class TestTrie:
    """Test cases for Trie class."""

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
    def trie(self, config_file):
        """Create Trie instance."""
        return Trie(config_path=config_file)

    def test_insert_word(self, trie):
        """Test inserting a word."""
        trie.insert("apple")
        assert trie.count_words() == 1
        assert trie.search("apple") is True

    def test_insert_multiple_words(self, trie):
        """Test inserting multiple words."""
        words = ["apple", "apply", "application"]
        for word in words:
            trie.insert(word)
        assert trie.count_words() == 3

    def test_insert_empty_word(self, trie):
        """Test inserting empty word."""
        trie.insert("")
        assert trie.count_words() == 0

    def test_insert_duplicate_word(self, trie):
        """Test inserting duplicate word."""
        trie.insert("apple")
        trie.insert("apple")
        assert trie.count_words() == 1

    def test_search_existing_word(self, trie):
        """Test searching for existing word."""
        trie.insert("apple")
        assert trie.search("apple") is True

    def test_search_nonexistent_word(self, trie):
        """Test searching for nonexistent word."""
        trie.insert("apple")
        assert trie.search("app") is False
        assert trie.search("orange") is False

    def test_search_empty_word(self, trie):
        """Test searching for empty word."""
        assert trie.search("") is False

    def test_starts_with_existing_prefix(self, trie):
        """Test checking existing prefix."""
        trie.insert("apple")
        trie.insert("apply")
        assert trie.starts_with("app") is True

    def test_starts_with_nonexistent_prefix(self, trie):
        """Test checking nonexistent prefix."""
        trie.insert("apple")
        assert trie.starts_with("ora") is False

    def test_starts_with_empty_prefix(self, trie):
        """Test checking empty prefix."""
        trie.insert("apple")
        assert trie.starts_with("") is True

    def test_autocomplete_with_prefix(self, trie):
        """Test autocomplete with prefix."""
        words = ["apple", "apply", "application", "app"]
        for word in words:
            trie.insert(word)
        suggestions = trie.autocomplete("app")
        assert len(suggestions) == 4
        assert "apple" in suggestions
        assert "apply" in suggestions

    def test_autocomplete_with_limit(self, trie):
        """Test autocomplete with limit."""
        words = ["apple", "apply", "application", "app"]
        for word in words:
            trie.insert(word)
        suggestions = trie.autocomplete("app", limit=2)
        assert len(suggestions) <= 2

    def test_autocomplete_empty_prefix(self, trie):
        """Test autocomplete with empty prefix."""
        words = ["apple", "apply", "application"]
        for word in words:
            trie.insert(word)
        suggestions = trie.autocomplete("")
        assert len(suggestions) == 3

    def test_autocomplete_nonexistent_prefix(self, trie):
        """Test autocomplete with nonexistent prefix."""
        trie.insert("apple")
        suggestions = trie.autocomplete("ora")
        assert len(suggestions) == 0

    def test_delete_existing_word(self, trie):
        """Test deleting existing word."""
        trie.insert("apple")
        result = trie.delete("apple")
        assert result is True
        assert trie.count_words() == 0
        assert trie.search("apple") is False

    def test_delete_nonexistent_word(self, trie):
        """Test deleting nonexistent word."""
        trie.insert("apple")
        result = trie.delete("orange")
        assert result is False
        assert trie.count_words() == 1

    def test_delete_empty_word(self, trie):
        """Test deleting empty word."""
        result = trie.delete("")
        assert result is False

    def test_count_words(self, trie):
        """Test counting words."""
        words = ["apple", "apply", "application"]
        for word in words:
            trie.insert(word)
        assert trie.count_words() == 3

    def test_count_words_with_prefix(self, trie):
        """Test counting words with prefix."""
        words = ["apple", "apply", "application", "app"]
        for word in words:
            trie.insert(word)
        count = trie.count_words_with_prefix("app")
        assert count >= 4

    def test_count_words_with_nonexistent_prefix(self, trie):
        """Test counting words with nonexistent prefix."""
        trie.insert("apple")
        count = trie.count_words_with_prefix("ora")
        assert count == 0

    def test_get_all_words(self, trie):
        """Test getting all words."""
        words = ["apple", "apply", "application"]
        for word in words:
            trie.insert(word)
        all_words = trie.get_all_words()
        assert len(all_words) == 3
        assert "apple" in all_words
        assert "apply" in all_words
        assert "application" in all_words

    def test_longest_common_prefix(self, trie):
        """Test finding longest common prefix."""
        words = ["apple", "apply", "application"]
        for word in words:
            trie.insert(word)
        prefix = trie.longest_common_prefix()
        assert prefix == "app"

    def test_longest_common_prefix_no_common(self, trie):
        """Test longest common prefix with no common prefix."""
        words = ["apple", "banana", "cherry"]
        for word in words:
            trie.insert(word)
        prefix = trie.longest_common_prefix()
        assert prefix == ""

    def test_longest_common_prefix_single_word(self, trie):
        """Test longest common prefix with single word."""
        trie.insert("apple")
        prefix = trie.longest_common_prefix()
        assert prefix == ""

    def test_build_from_list(self, trie):
        """Test building trie from list."""
        words = ["apple", "apply", "application"]
        trie.build_from_list(words)
        assert trie.count_words() == 3

    def test_build_from_empty_list(self, trie):
        """Test building trie from empty list."""
        trie.build_from_list([])
        assert trie.count_words() == 0

    def test_compare_performance(self, trie):
        """Test performance comparison."""
        words = ["apple", "apply", "application", "app"]
        performance = trie.compare_performance(words, "app", iterations=1)
        assert performance["num_words"] == 4
        assert performance["prefix"] == "app"
        assert performance["insert"]["success"] is True
        assert performance["search"]["success"] is True
        assert performance["autocomplete"]["success"] is True

    def test_compare_performance_with_iterations(self, trie):
        """Test performance comparison with multiple iterations."""
        words = ["apple", "apply", "application"]
        performance = trie.compare_performance(words, "app", iterations=10)
        assert performance["iterations"] == 10
        assert performance["insert"]["success"] is True

    def test_generate_report_success(self, trie, temp_dir):
        """Test report generation."""
        words = ["apple", "apply", "application"]
        performance = trie.compare_performance(words, "app")
        report_path = temp_dir / "report.txt"

        report = trie.generate_report(performance, output_path=str(report_path))

        assert "TRIE DATA STRUCTURE" in report
        assert "insert()" in report
        assert "search()" in report
        assert "autocomplete()" in report
        assert report_path.exists()

    def test_generate_report_no_output(self, trie):
        """Test report generation without saving to file."""
        words = ["apple", "apply", "application"]
        performance = trie.compare_performance(words, "app")
        report = trie.generate_report(performance)

        assert "TRIE DATA STRUCTURE" in report
        assert "insert()" in report
        assert "search()" in report

    def test_single_character_words(self, trie):
        """Test with single character words."""
        words = ["a", "b", "c"]
        for word in words:
            trie.insert(word)
        assert trie.count_words() == 3
        assert trie.search("a") is True

    def test_words_with_common_prefix(self, trie):
        """Test with words sharing common prefix."""
        words = ["cat", "car", "card", "care"]
        for word in words:
            trie.insert(word)
        suggestions = trie.autocomplete("ca")
        assert len(suggestions) == 4

    def test_words_with_no_common_prefix(self, trie):
        """Test with words having no common prefix."""
        words = ["apple", "banana", "cherry"]
        for word in words:
            trie.insert(word)
        assert trie.count_words() == 3
        assert trie.longest_common_prefix() == ""

    def test_delete_with_shared_prefix(self, trie):
        """Test deleting word with shared prefix."""
        words = ["apple", "apply"]
        for word in words:
            trie.insert(word)
        trie.delete("apple")
        assert trie.search("apple") is False
        assert trie.search("apply") is True

    def test_autocomplete_ordering(self, trie):
        """Test autocomplete returns words in order."""
        words = ["apple", "apply", "application", "app"]
        for word in words:
            trie.insert(word)
        suggestions = trie.autocomplete("app")
        assert len(suggestions) == 4
