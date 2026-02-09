"""Unit tests for Rabin-Karp algorithm module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import RabinKarpAlgorithm


class TestRabinKarpAlgorithm:
    """Test cases for RabinKarpAlgorithm class."""

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
    def rk(self, config_file):
        """Create RabinKarpAlgorithm instance."""
        return RabinKarpAlgorithm(
            "ABABDABACDABABCABCAB", base=256, modulus=101, config_path=config_file
        )

    def test_rabin_karp_algorithm_creation(self, config_file):
        """Test RabinKarpAlgorithm creation."""
        rk = RabinKarpAlgorithm("banana", config_path=config_file)
        assert rk.get_length() == 6
        assert rk.get_text() == "banana"

    def test_rabin_karp_algorithm_empty_text(self):
        """Test creation with empty text."""
        with pytest.raises(ValueError):
            RabinKarpAlgorithm("")

    def test_rabin_karp_algorithm_invalid_base(self):
        """Test creation with invalid base."""
        with pytest.raises(ValueError):
            RabinKarpAlgorithm("text", base=1)

    def test_rabin_karp_algorithm_invalid_modulus(self):
        """Test creation with invalid modulus."""
        with pytest.raises(ValueError):
            RabinKarpAlgorithm("text", modulus=1)

    def test_search_existing_pattern(self, rk):
        """Test searching for existing pattern."""
        occurrences = rk.search("ABAB")
        assert len(occurrences) > 0
        assert all(isinstance(pos, int) for pos in occurrences)

    def test_search_nonexistent_pattern(self, rk):
        """Test searching for nonexistent pattern."""
        occurrences = rk.search("XYZ")
        assert len(occurrences) == 0

    def test_search_empty_pattern(self, rk):
        """Test searching for empty pattern."""
        with pytest.raises(ValueError):
            rk.search("")

    def test_search_pattern_longer_than_text(self, config_file):
        """Test searching for pattern longer than text."""
        rk = RabinKarpAlgorithm("abc", config_path=config_file)
        occurrences = rk.search("abcd")
        assert len(occurrences) == 0

    def test_search_with_collision_verification(self, rk):
        """Test search with collision verification."""
        occurrences = rk.search("ABAB", verify_collisions=True)
        assert len(occurrences) > 0

    def test_search_without_collision_verification(self, rk):
        """Test search without collision verification."""
        occurrences = rk.search("ABAB", verify_collisions=False)
        assert len(occurrences) > 0

    def test_count_occurrences(self, rk):
        """Test counting occurrences."""
        count = rk.count_occurrences("ABAB")
        assert count > 0

        count_nonexistent = rk.count_occurrences("XYZ")
        assert count_nonexistent == 0

    def test_find_all_occurrences(self, rk):
        """Test finding all occurrences with positions."""
        occurrences = rk.find_all_occurrences("ABAB")
        assert len(occurrences) > 0
        assert all(isinstance(occ, tuple) for occ in occurrences)

    def test_is_substring(self, rk):
        """Test checking if pattern is substring."""
        assert rk.is_substring("ABAB") is True
        assert rk.is_substring("XYZ") is False

    def test_get_hash(self, rk):
        """Test getting hash value."""
        pattern_hash = rk.get_hash("ABAB")
        assert isinstance(pattern_hash, int)
        assert pattern_hash >= 0

    def test_get_hash_empty_pattern(self, rk):
        """Test getting hash with empty pattern."""
        with pytest.raises(ValueError):
            rk.get_hash("")

    def test_search_all_single_pattern(self, rk):
        """Test searching for single pattern in multiple patterns."""
        results = rk.search_all(["ABAB"])
        assert "ABAB" in results
        assert len(results["ABAB"]) > 0

    def test_search_all_multiple_patterns(self, rk):
        """Test searching for multiple patterns."""
        patterns = ["ABAB", "ABC", "AB"]
        results = rk.search_all(patterns)

        assert len(results) == 3
        assert "ABAB" in results
        assert "ABC" in results
        assert "AB" in results

    def test_search_all_empty_patterns(self, rk):
        """Test searching with empty patterns list."""
        with pytest.raises(ValueError):
            rk.search_all([])

    def test_get_text(self, rk):
        """Test getting text."""
        assert rk.get_text() == "ABABDABACDABABCABCAB"

    def test_get_length(self, rk):
        """Test getting length."""
        assert rk.get_length() == 20

    def test_get_base(self, rk):
        """Test getting base."""
        assert rk.get_base() == 256

    def test_get_modulus(self, rk):
        """Test getting modulus."""
        assert rk.get_modulus() == 101

    def test_simple_text(self, config_file):
        """Test with simple text."""
        rk = RabinKarpAlgorithm("abc", config_path=config_file)
        occurrences = rk.search("a")
        assert len(occurrences) > 0

    def test_single_character(self, config_file):
        """Test with single character."""
        rk = RabinKarpAlgorithm("a", config_path=config_file)
        assert rk.get_length() == 1

    def test_repeated_characters(self, config_file):
        """Test with repeated characters."""
        rk = RabinKarpAlgorithm("aaa", config_path=config_file)
        occurrences = rk.search("aa")
        assert len(occurrences) == 2

    def test_overlapping_patterns(self, config_file):
        """Test with overlapping patterns."""
        rk = RabinKarpAlgorithm("aaaa", config_path=config_file)
        occurrences = rk.search("aa")
        assert len(occurrences) == 3

    def test_long_text(self, config_file):
        """Test with longer text."""
        text = "mississippi"
        rk = RabinKarpAlgorithm(text, config_path=config_file)
        occurrences = rk.search("ssi")
        assert len(occurrences) == 2

    def test_custom_base_and_modulus(self, config_file):
        """Test with custom base and modulus."""
        rk = RabinKarpAlgorithm(
            "banana", base=31, modulus=1000000007, config_path=config_file
        )
        occurrences = rk.search("ana")
        assert len(occurrences) == 2

    def test_hash_consistency(self, config_file):
        """Test hash consistency."""
        rk = RabinKarpAlgorithm("text", config_path=config_file)
        pattern = "ab"
        hash1 = rk.get_hash(pattern)
        hash2 = rk.get_hash(pattern)
        assert hash1 == hash2

    def test_all_occurrences_positions(self, config_file):
        """Test that all occurrences have correct positions."""
        rk = RabinKarpAlgorithm("banana", config_path=config_file)
        occurrences = rk.search("ana", verify_collisions=True)

        for pos in occurrences:
            assert rk.get_text()[pos:pos + 3] == "ana"

    def test_multiple_patterns_all_found(self, config_file):
        """Test multiple patterns all found."""
        rk = RabinKarpAlgorithm("banana", config_path=config_file)
        patterns = ["ban", "ana", "nan"]
        results = rk.search_all(patterns, verify_collisions=True)

        for pattern in patterns:
            assert len(results[pattern]) > 0

    def test_multiple_patterns_some_found(self, config_file):
        """Test multiple patterns with some not found."""
        rk = RabinKarpAlgorithm("banana", config_path=config_file)
        patterns = ["ban", "xyz", "ana"]
        results = rk.search_all(patterns, verify_collisions=True)

        assert len(results["ban"]) > 0
        assert len(results["xyz"]) == 0
        assert len(results["ana"]) > 0

    def test_collision_handling(self, config_file):
        """Test collision handling."""
        rk = RabinKarpAlgorithm("abc", config_path=config_file)

        occurrences_with_verify = rk.search("a", verify_collisions=True)
        occurrences_without_verify = rk.search("a", verify_collisions=False)

        assert len(occurrences_with_verify) == len(occurrences_without_verify)

    def test_hash_properties(self, config_file):
        """Test hash properties."""
        rk = RabinKarpAlgorithm("text", base=256, modulus=101, config_path=config_file)

        hash_a = rk.get_hash("a")
        hash_b = rk.get_hash("b")

        assert hash_a != hash_b
        assert 0 <= hash_a < 101
        assert 0 <= hash_b < 101
