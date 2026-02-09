"""Unit tests for KMP algorithm module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import KMPAlgorithm


class TestKMPAlgorithm:
    """Test cases for KMPAlgorithm class."""

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
    def kmp(self, config_file):
        """Create KMPAlgorithm instance."""
        return KMPAlgorithm("ABABDABACDABABCABCAB", config_path=config_file)

    def test_kmp_algorithm_creation(self, config_file):
        """Test KMPAlgorithm creation."""
        kmp = KMPAlgorithm("banana", config_path=config_file)
        assert kmp.get_length() == 6
        assert kmp.get_text() == "banana"

    def test_kmp_algorithm_empty_text(self):
        """Test creation with empty text."""
        with pytest.raises(ValueError):
            KMPAlgorithm("")

    def test_search_existing_pattern(self, kmp):
        """Test searching for existing pattern."""
        occurrences = kmp.search("ABAB")
        assert len(occurrences) > 0
        assert all(isinstance(pos, int) for pos in occurrences)

    def test_search_nonexistent_pattern(self, kmp):
        """Test searching for nonexistent pattern."""
        occurrences = kmp.search("XYZ")
        assert len(occurrences) == 0

    def test_search_empty_pattern(self, kmp):
        """Test searching for empty pattern."""
        with pytest.raises(ValueError):
            kmp.search("")

    def test_search_pattern_longer_than_text(self, config_file):
        """Test searching for pattern longer than text."""
        kmp = KMPAlgorithm("abc", config_path=config_file)
        occurrences = kmp.search("abcd")
        assert len(occurrences) == 0

    def test_count_occurrences(self, kmp):
        """Test counting occurrences."""
        count = kmp.count_occurrences("ABAB")
        assert count > 0

        count_nonexistent = kmp.count_occurrences("XYZ")
        assert count_nonexistent == 0

    def test_find_all_occurrences(self, kmp):
        """Test finding all occurrences with positions."""
        occurrences = kmp.find_all_occurrences("ABAB")
        assert len(occurrences) > 0
        assert all(isinstance(occ, tuple) for occ in occurrences)

    def test_is_substring(self, kmp):
        """Test checking if pattern is substring."""
        assert kmp.is_substring("ABAB") is True
        assert kmp.is_substring("XYZ") is False

    def test_get_failure_function(self, kmp):
        """Test getting failure function."""
        lps = kmp.get_failure_function("ABABCABCAB")
        assert isinstance(lps, list)
        assert len(lps) == len("ABABCABCAB")
        assert all(isinstance(x, int) for x in lps)

    def test_get_failure_function_empty_pattern(self, kmp):
        """Test getting failure function with empty pattern."""
        with pytest.raises(ValueError):
            kmp.get_failure_function("")

    def test_search_all_single_pattern(self, kmp):
        """Test searching for single pattern in multiple patterns."""
        results = kmp.search_all(["ABAB"])
        assert "ABAB" in results
        assert len(results["ABAB"]) > 0

    def test_search_all_multiple_patterns(self, kmp):
        """Test searching for multiple patterns."""
        patterns = ["ABAB", "ABC", "AB"]
        results = kmp.search_all(patterns)

        assert len(results) == 3
        assert "ABAB" in results
        assert "ABC" in results
        assert "AB" in results

    def test_search_all_empty_patterns(self, kmp):
        """Test searching with empty patterns list."""
        with pytest.raises(ValueError):
            kmp.search_all([])

    def test_get_text(self, kmp):
        """Test getting text."""
        assert kmp.get_text() == "ABABDABACDABABCABCAB"

    def test_get_length(self, kmp):
        """Test getting length."""
        assert kmp.get_length() == 20

    def test_simple_text(self, config_file):
        """Test with simple text."""
        kmp = KMPAlgorithm("abc", config_path=config_file)
        occurrences = kmp.search("a")
        assert len(occurrences) > 0

    def test_single_character(self, config_file):
        """Test with single character."""
        kmp = KMPAlgorithm("a", config_path=config_file)
        assert kmp.get_length() == 1

    def test_repeated_characters(self, config_file):
        """Test with repeated characters."""
        kmp = KMPAlgorithm("aaa", config_path=config_file)
        occurrences = kmp.search("aa")
        assert len(occurrences) == 2

    def test_overlapping_patterns(self, config_file):
        """Test with overlapping patterns."""
        kmp = KMPAlgorithm("aaaa", config_path=config_file)
        occurrences = kmp.search("aa")
        assert len(occurrences) == 3

    def test_long_text(self, config_file):
        """Test with longer text."""
        text = "mississippi"
        kmp = KMPAlgorithm(text, config_path=config_file)
        occurrences = kmp.search("ssi")
        assert len(occurrences) == 2

    def test_failure_function_properties(self, config_file):
        """Test failure function properties."""
        kmp = KMPAlgorithm("banana", config_path=config_file)
        pattern = "abab"
        lps = kmp.get_failure_function(pattern)

        assert lps[0] == 0
        assert len(lps) == len(pattern)
        assert all(0 <= x < len(pattern) for x in lps)

    def test_failure_function_correctness(self, config_file):
        """Test failure function correctness."""
        kmp = KMPAlgorithm("text", config_path=config_file)
        pattern = "abab"
        lps = kmp.get_failure_function(pattern)

        assert lps == [0, 0, 1, 2]

    def test_all_occurrences_positions(self, config_file):
        """Test that all occurrences have correct positions."""
        kmp = KMPAlgorithm("banana", config_path=config_file)
        occurrences = kmp.search("ana")

        for pos in occurrences:
            assert kmp.get_text()[pos:pos + 3] == "ana"

    def test_multiple_patterns_all_found(self, config_file):
        """Test multiple patterns all found."""
        kmp = KMPAlgorithm("banana", config_path=config_file)
        patterns = ["ban", "ana", "nan"]
        results = kmp.search_all(patterns)

        for pattern in patterns:
            assert len(results[pattern]) > 0

    def test_multiple_patterns_some_found(self, config_file):
        """Test multiple patterns with some not found."""
        kmp = KMPAlgorithm("banana", config_path=config_file)
        patterns = ["ban", "xyz", "ana"]
        results = kmp.search_all(patterns)

        assert len(results["ban"]) > 0
        assert len(results["xyz"]) == 0
        assert len(results["ana"]) > 0

    def test_failure_function_edge_cases(self, config_file):
        """Test failure function with edge cases."""
        kmp = KMPAlgorithm("text", config_path=config_file)

        lps_single = kmp.get_failure_function("a")
        assert lps_single == [0]

        lps_all_same = kmp.get_failure_function("aaa")
        assert lps_all_same == [0, 1, 2]

        lps_no_repeat = kmp.get_failure_function("abc")
        assert lps_no_repeat == [0, 0, 0]
