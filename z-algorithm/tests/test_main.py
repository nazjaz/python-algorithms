"""Unit tests for Z-algorithm module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import ZAlgorithm


class TestZAlgorithm:
    """Test cases for ZAlgorithm class."""

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
    def z_algo(self, config_file):
        """Create ZAlgorithm instance."""
        return ZAlgorithm("banana", config_path=config_file)

    def test_z_algorithm_creation(self, config_file):
        """Test ZAlgorithm creation."""
        z_algo = ZAlgorithm("banana", config_path=config_file)
        assert z_algo.get_length() == 6
        assert z_algo.get_text() == "banana"

    def test_z_algorithm_empty_text(self):
        """Test creation with empty text."""
        with pytest.raises(ValueError):
            ZAlgorithm("")

    def test_search_existing_pattern(self, z_algo):
        """Test searching for existing pattern."""
        occurrences = z_algo.search("ana")
        assert len(occurrences) == 2
        assert 1 in occurrences
        assert 3 in occurrences

    def test_search_nonexistent_pattern(self, z_algo):
        """Test searching for nonexistent pattern."""
        occurrences = z_algo.search("xyz")
        assert len(occurrences) == 0

    def test_search_empty_pattern(self, z_algo):
        """Test searching for empty pattern."""
        with pytest.raises(ValueError):
            z_algo.search("")

    def test_search_pattern_longer_than_text(self, config_file):
        """Test searching for pattern longer than text."""
        z_algo = ZAlgorithm("abc", config_path=config_file)
        occurrences = z_algo.search("abcd")
        assert len(occurrences) == 0

    def test_count_occurrences(self, z_algo):
        """Test counting occurrences."""
        count = z_algo.count_occurrences("ana")
        assert count == 2

        count_nonexistent = z_algo.count_occurrences("xyz")
        assert count_nonexistent == 0

    def test_find_all_occurrences(self, z_algo):
        """Test finding all occurrences with positions."""
        occurrences = z_algo.find_all_occurrences("ana")
        assert len(occurrences) == 2
        assert (1, 3) in occurrences
        assert (3, 3) in occurrences

    def test_is_substring(self, z_algo):
        """Test checking if pattern is substring."""
        assert z_algo.is_substring("ana") is True
        assert z_algo.is_substring("ban") is True
        assert z_algo.is_substring("xyz") is False

    def test_search_all_single_pattern(self, z_algo):
        """Test searching for single pattern in multiple patterns."""
        results = z_algo.search_all(["ana"])
        assert "ana" in results
        assert len(results["ana"]) == 2

    def test_search_all_multiple_patterns(self, z_algo):
        """Test searching for multiple patterns."""
        patterns = ["ana", "nan", "ban"]
        results = z_algo.search_all(patterns)

        assert len(results) == 3
        assert "ana" in results
        assert "nan" in results
        assert "ban" in results
        assert len(results["ana"]) == 2
        assert len(results["nan"]) == 1
        assert len(results["ban"]) == 1

    def test_search_all_empty_patterns(self, z_algo):
        """Test searching with empty patterns list."""
        with pytest.raises(ValueError):
            z_algo.search_all([])

    def test_search_all_with_empty_pattern(self, z_algo):
        """Test searching with empty pattern in list."""
        results = z_algo.search_all(["ana", ""])
        assert "ana" in results
        assert "" in results
        assert len(results[""]) == 0

    def test_get_z_array(self, z_algo):
        """Test getting Z-array."""
        z_array = z_algo.get_z_array("ana")
        assert isinstance(z_array, list)
        assert len(z_array) > 0

    def test_get_z_array_empty_pattern(self, z_algo):
        """Test getting Z-array with empty pattern."""
        with pytest.raises(ValueError):
            z_algo.get_z_array("")

    def test_get_longest_prefix_match(self, config_file):
        """Test getting longest prefix match."""
        z_algo = ZAlgorithm("banana", config_path=config_file)
        match_length = z_algo.get_longest_prefix_match(1)
        assert match_length >= 0

    def test_get_longest_prefix_match_invalid_position(self, z_algo):
        """Test getting longest prefix match with invalid position."""
        with pytest.raises(ValueError):
            z_algo.get_longest_prefix_match(-1)
        with pytest.raises(ValueError):
            z_algo.get_longest_prefix_match(10)

    def test_find_longest_repeated_substring(self, config_file):
        """Test finding longest repeated substring."""
        z_algo = ZAlgorithm("banana", config_path=config_file)
        longest = z_algo.find_longest_repeated_substring()
        assert isinstance(longest, str)
        assert len(longest) > 0

    def test_find_longest_repeated_substring_no_repeat(self, config_file):
        """Test finding longest repeated substring with no repeats."""
        z_algo = ZAlgorithm("abc", config_path=config_file)
        longest = z_algo.find_longest_repeated_substring()
        assert isinstance(longest, str)

    def test_get_text(self, z_algo):
        """Test getting text."""
        assert z_algo.get_text() == "banana"

    def test_get_length(self, z_algo):
        """Test getting length."""
        assert z_algo.get_length() == 6

    def test_simple_text(self, config_file):
        """Test with simple text."""
        z_algo = ZAlgorithm("abc", config_path=config_file)
        occurrences = z_algo.search("a")
        assert len(occurrences) > 0

    def test_single_character(self, config_file):
        """Test with single character."""
        z_algo = ZAlgorithm("a", config_path=config_file)
        assert z_algo.get_length() == 1

    def test_repeated_characters(self, config_file):
        """Test with repeated characters."""
        z_algo = ZAlgorithm("aaa", config_path=config_file)
        occurrences = z_algo.search("aa")
        assert len(occurrences) == 2

    def test_long_text(self, config_file):
        """Test with longer text."""
        text = "mississippi"
        z_algo = ZAlgorithm(text, config_path=config_file)
        occurrences = z_algo.search("ssi")
        assert len(occurrences) == 2

    def test_overlapping_patterns(self, config_file):
        """Test with overlapping patterns."""
        z_algo = ZAlgorithm("aaaa", config_path=config_file)
        occurrences = z_algo.search("aa")
        assert len(occurrences) == 3

    def test_multiple_patterns_all_found(self, config_file):
        """Test multiple patterns all found."""
        z_algo = ZAlgorithm("banana", config_path=config_file)
        patterns = ["ban", "ana", "nan"]
        results = z_algo.search_all(patterns)

        for pattern in patterns:
            assert len(results[pattern]) > 0

    def test_multiple_patterns_some_found(self, config_file):
        """Test multiple patterns with some not found."""
        z_algo = ZAlgorithm("banana", config_path=config_file)
        patterns = ["ban", "xyz", "ana"]
        results = z_algo.search_all(patterns)

        assert len(results["ban"]) > 0
        assert len(results["xyz"]) == 0
        assert len(results["ana"]) > 0

    def test_z_array_properties(self, config_file):
        """Test Z-array properties."""
        z_algo = ZAlgorithm("banana", config_path=config_file)
        z_array = z_algo.get_z_array("ana")
        assert z_array[0] == len("ana")

    def test_all_occurrences_positions(self, config_file):
        """Test that all occurrences have correct positions."""
        z_algo = ZAlgorithm("banana", config_path=config_file)
        occurrences = z_algo.search("ana")

        for pos in occurrences:
            assert z_algo.get_text()[pos:pos + 3] == "ana"
