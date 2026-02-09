"""Unit tests for anagram finder module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import AnagramFinder


class TestAnagramFinder:
    """Test cases for AnagramFinder class."""

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
    def finder(self, config_file):
        """Create AnagramFinder instance."""
        return AnagramFinder(config_path=config_file)

    def test_load_config_success(self, temp_dir):
        """Test successful configuration loading."""
        config = {
            "logging": {"level": "DEBUG"},
        }
        config_path = temp_dir / "config.yaml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)

        finder = AnagramFinder(config_path=str(config_path))
        assert finder.config["logging"]["level"] == "DEBUG"

    def test_load_config_file_not_found(self):
        """Test FileNotFoundError when config file doesn't exist."""
        with pytest.raises(FileNotFoundError):
            AnagramFinder(config_path="nonexistent.yaml")

    def test_get_character_frequency(self, finder):
        """Test character frequency calculation."""
        freq = finder._get_character_frequency("hello")
        assert freq["h"] == 1
        assert freq["e"] == 1
        assert freq["l"] == 2
        assert freq["o"] == 1

    def test_get_character_frequency_case_insensitive(self, finder):
        """Test character frequency is case-insensitive."""
        freq1 = finder._get_character_frequency("Hello")
        freq2 = finder._get_character_frequency("hello")
        assert freq1 == freq2

    def test_get_frequency_hash(self, finder):
        """Test frequency hash generation."""
        hash1 = finder._get_frequency_hash("listen")
        hash2 = finder._get_frequency_hash("silent")
        assert hash1 == hash2

    def test_get_frequency_hash_different_words(self, finder):
        """Test different words produce different hashes."""
        hash1 = finder._get_frequency_hash("cat")
        hash2 = finder._get_frequency_hash("dog")
        assert hash1 != hash2

    def test_are_anagrams_true(self, finder):
        """Test anagram detection for anagrams."""
        assert finder._are_anagrams("listen", "silent") is True
        assert finder._are_anagrams("evil", "vile") is True
        assert finder._are_anagrams("cat", "act") is True

    def test_are_anagrams_false(self, finder):
        """Test anagram detection for non-anagrams."""
        assert finder._are_anagrams("cat", "dog") is False
        assert finder._are_anagrams("hello", "world") is False

    def test_are_anagrams_different_lengths(self, finder):
        """Test anagram detection with different lengths."""
        assert finder._are_anagrams("cat", "cats") is False
        assert finder._are_anagrams("a", "aa") is False

    def test_are_anagrams_case_insensitive(self, finder):
        """Test anagram detection is case-insensitive."""
        assert finder._are_anagrams("Listen", "Silent") is True
        assert finder._are_anagrams("CAT", "act") is True

    def test_find_anagrams_simple(self, finder):
        """Test finding anagrams in simple list."""
        words = ["listen", "silent", "enlist"]
        result = finder.find_anagrams(words)
        assert len(result) == 1
        assert len(list(result.values())[0]) == 3

    def test_find_anagrams_multiple_groups(self, finder):
        """Test finding multiple anagram groups."""
        words = ["listen", "silent", "cat", "act", "dog"]
        result = finder.find_anagrams(words)
        assert len(result) == 2
        group_sizes = [len(group) for group in result.values()]
        assert 2 in group_sizes
        assert 2 in group_sizes

    def test_find_anagrams_no_anagrams(self, finder):
        """Test finding anagrams when none exist."""
        words = ["cat", "dog", "bird"]
        result = finder.find_anagrams(words)
        assert len(result) == 0

    def test_find_anagrams_empty_list(self, finder):
        """Test finding anagrams in empty list."""
        result = finder.find_anagrams([])
        assert result == {}

    def test_find_anagrams_single_word(self, finder):
        """Test finding anagrams with single word."""
        result = finder.find_anagrams(["cat"])
        assert len(result) == 0

    def test_find_anagrams_case_sensitive(self, finder):
        """Test finding anagrams with case sensitivity."""
        words = ["Listen", "silent", "LISTEN"]
        result = finder.find_anagrams(words, case_sensitive=False)
        assert len(result) == 1

        result = finder.find_anagrams(words, case_sensitive=True)
        # With case sensitivity, "Listen" and "LISTEN" are different
        assert len(result) >= 1

    def test_find_anagrams_empty_strings(self, finder):
        """Test finding anagrams with empty strings."""
        words = ["cat", "", "act", ""]
        result = finder.find_anagrams(words)
        # Empty strings should be ignored
        assert len(result) == 1

    def test_find_anagrams_duplicates(self, finder):
        """Test finding anagrams with duplicate words."""
        words = ["listen", "silent", "listen", "silent"]
        result = finder.find_anagrams(words)
        assert len(result) == 1
        group = list(result.values())[0]
        assert "listen" in group
        assert "silent" in group

    def test_find_anagrams_detailed(self, finder):
        """Test detailed anagram finding."""
        words = ["listen", "silent", "cat", "act"]
        result = finder.find_anagrams_detailed(words)
        assert "groups" in result
        assert "statistics" in result
        assert "character_frequencies" in result
        assert result["statistics"]["total_words"] == 4
        assert result["statistics"]["total_anagram_groups"] == 2

    def test_find_anagrams_detailed_statistics(self, finder):
        """Test detailed statistics calculation."""
        words = ["listen", "silent", "enlist", "cat", "act"]
        result = finder.find_anagrams_detailed(words)
        stats = result["statistics"]
        assert stats["total_words"] == 5
        assert stats["total_anagram_groups"] == 2
        assert stats["total_words_in_groups"] == 5
        assert stats["words_without_anagrams"] == 0
        assert stats["largest_group_size"] == 3

    def test_find_anagrams_for_word(self, finder):
        """Test finding anagrams for specific word."""
        word_list = ["listen", "silent", "enlist", "cat", "act"]
        anagrams = finder.find_anagrams_for_word("listen", word_list)
        assert "silent" in anagrams
        assert "enlist" in anagrams
        assert "listen" not in anagrams
        assert "cat" not in anagrams

    def test_find_anagrams_for_word_no_anagrams(self, finder):
        """Test finding anagrams when none exist."""
        word_list = ["cat", "dog", "bird"]
        anagrams = finder.find_anagrams_for_word("cat", word_list)
        assert len(anagrams) == 0

    def test_get_character_frequency_analysis(self, finder):
        """Test character frequency analysis."""
        analysis = finder.get_character_frequency_analysis("hello")
        assert analysis["word"] == "hello"
        assert analysis["total_characters"] == 5
        assert analysis["unique_characters"] == 4
        assert "h" in analysis["frequencies"]
        assert analysis["frequencies"]["l"] == 2
        assert "hash_key" in analysis

    def test_generate_report(self, finder, temp_dir):
        """Test report generation."""
        words = ["listen", "silent", "cat", "act"]
        result = finder.find_anagrams_detailed(words)
        report_path = temp_dir / "report.txt"
        report = finder.generate_report(result, output_path=str(report_path))

        assert report_path.exists()
        assert "ANAGRAM FINDER REPORT" in report
        assert "STATISTICS" in report
        assert "ANAGRAM GROUPS" in report

    def test_generate_report_no_groups(self, finder):
        """Test report generation with no anagram groups."""
        words = ["cat", "dog", "bird"]
        result = finder.find_anagrams_detailed(words)
        report = finder.generate_report(result)
        assert "No anagram groups found" in report

    def test_hash_based_grouping(self, finder):
        """Test that hash-based grouping works correctly."""
        words = ["listen", "silent", "enlist", "inlets"]
        result = finder.find_anagrams(words)
        # All should be in same group
        assert len(result) == 1
        group = list(result.values())[0]
        assert len(group) == 4
        assert all(word in group for word in words)

    def test_character_frequency_comparison(self, finder):
        """Test character frequency comparison method."""
        # Same frequencies
        assert finder._are_anagrams("aabb", "bbaa") is True
        assert finder._are_anagrams("aabb", "abab") is True

        # Different frequencies
        assert finder._are_anagrams("aabb", "aab") is False
        assert finder._are_anagrams("aabb", "aaab") is False

    def test_large_word_list(self, finder):
        """Test with large word list."""
        words = ["listen", "silent", "enlist"] * 10 + ["cat", "act"] * 5
        result = finder.find_anagrams(words)
        assert len(result) == 2

    def test_special_characters(self, finder):
        """Test with special characters."""
        words = ["a!b", "b!a", "ab!"]
        result = finder.find_anagrams(words)
        # Should group anagrams with special characters
        assert len(result) >= 1

    def test_numbers_in_words(self, finder):
        """Test with numbers in words."""
        words = ["a1b", "b1a", "ab1"]
        result = finder.find_anagrams(words)
        # Should handle numbers
        assert len(result) >= 1

    def test_unicode_characters(self, finder):
        """Test with unicode characters."""
        words = ["café", "éfac"]
        result = finder.find_anagrams(words)
        # Should handle unicode
        assert isinstance(result, dict)
