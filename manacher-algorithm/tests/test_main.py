"""Unit tests for Manacher's algorithm module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import ManacherAlgorithm


class TestManacherAlgorithm:
    """Test cases for ManacherAlgorithm class."""

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

    def test_manacher_algorithm_creation(self, config_file):
        """Test ManacherAlgorithm creation."""
        manacher = ManacherAlgorithm("babad", config_path=config_file)
        assert manacher.get_length() == 5
        assert manacher.get_text() == "babad"

    def test_manacher_algorithm_empty_text(self):
        """Test creation with empty text."""
        with pytest.raises(ValueError):
            ManacherAlgorithm("")

    def test_get_longest_palindrome(self, config_file):
        """Test getting longest palindrome."""
        manacher = ManacherAlgorithm("babad", config_path=config_file)
        longest = manacher.get_longest_palindrome()
        assert len(longest) > 0
        assert longest == longest[::-1]

    def test_get_longest_palindrome_simple(self, config_file):
        """Test longest palindrome for simple cases."""
        manacher = ManacherAlgorithm("racecar", config_path=config_file)
        longest = manacher.get_longest_palindrome()
        assert longest == "racecar"

    def test_get_longest_palindrome_even(self, config_file):
        """Test longest palindrome with even length."""
        manacher = ManacherAlgorithm("cbbd", config_path=config_file)
        longest = manacher.get_longest_palindrome()
        assert longest in ["bb", "c", "b", "d"]

    def test_get_longest_palindrome_info(self, config_file):
        """Test getting longest palindrome info."""
        manacher = ManacherAlgorithm("babad", config_path=config_file)
        longest = manacher.get_longest_palindrome()
        info = manacher.get_longest_palindrome_info()
        assert len(info) == 3
        palindrome, start, length = info
        assert palindrome == longest
        assert length == len(palindrome)
        assert start >= 0

    def test_get_all_palindromes(self, config_file):
        """Test getting all palindromes."""
        manacher = ManacherAlgorithm("babad", config_path=config_file)
        all_palindromes = manacher.get_all_palindromes()
        assert len(all_palindromes) > 0
        assert all(isinstance(p[0], str) for p in all_palindromes)

    def test_count_palindromes(self, config_file):
        """Test counting palindromes."""
        manacher = ManacherAlgorithm("babad", config_path=config_file)
        count = manacher.count_palindromes()
        assert count > 0

    def test_is_palindrome_at(self, config_file):
        """Test checking if substring is palindrome."""
        manacher = ManacherAlgorithm("racecar", config_path=config_file)
        assert manacher.is_palindrome_at(0, 7) is True
        assert manacher.is_palindrome_at(1, 5) is True
        assert manacher.is_palindrome_at(0, 3) is False

    def test_is_palindrome_at_invalid_position(self, config_file):
        """Test is_palindrome_at with invalid position."""
        manacher = ManacherAlgorithm("abc", config_path=config_file)
        with pytest.raises(ValueError):
            manacher.is_palindrome_at(-1, 1)
        with pytest.raises(ValueError):
            manacher.is_palindrome_at(10, 1)

    def test_is_palindrome_at_invalid_length(self, config_file):
        """Test is_palindrome_at with invalid length."""
        manacher = ManacherAlgorithm("abc", config_path=config_file)
        with pytest.raises(ValueError):
            manacher.is_palindrome_at(0, 0)
        with pytest.raises(ValueError):
            manacher.is_palindrome_at(0, 10)

    def test_get_palindrome_radii(self, config_file):
        """Test getting palindrome radii."""
        manacher = ManacherAlgorithm("babad", config_path=config_file)
        radii = manacher.get_palindrome_radii()
        assert isinstance(radii, list)
        assert len(radii) > 0

    def test_get_text(self, config_file):
        """Test getting text."""
        text = "babad"
        manacher = ManacherAlgorithm(text, config_path=config_file)
        assert manacher.get_text() == text

    def test_get_length(self, config_file):
        """Test getting length."""
        manacher = ManacherAlgorithm("babad", config_path=config_file)
        assert manacher.get_length() == 5

    def test_is_valid(self, config_file):
        """Test validation."""
        manacher = ManacherAlgorithm("babad", config_path=config_file)
        assert manacher.is_valid() is True

    def test_single_character(self, config_file):
        """Test with single character."""
        manacher = ManacherAlgorithm("a", config_path=config_file)
        longest = manacher.get_longest_palindrome()
        assert longest == "a"

    def test_all_same_characters(self, config_file):
        """Test with all same characters."""
        manacher = ManacherAlgorithm("aaa", config_path=config_file)
        longest = manacher.get_longest_palindrome()
        assert longest == "aaa"

    def test_no_palindrome_longer_than_one(self, config_file):
        """Test with no palindrome longer than one character."""
        manacher = ManacherAlgorithm("abc", config_path=config_file)
        longest = manacher.get_longest_palindrome()
        assert len(longest) == 1
        assert longest in ["a", "b", "c"]

    def test_even_length_palindrome(self, config_file):
        """Test with even length palindrome."""
        manacher = ManacherAlgorithm("abba", config_path=config_file)
        longest = manacher.get_longest_palindrome()
        assert longest == "abba"

    def test_odd_length_palindrome(self, config_file):
        """Test with odd length palindrome."""
        manacher = ManacherAlgorithm("aba", config_path=config_file)
        longest = manacher.get_longest_palindrome()
        assert longest == "aba"

    def test_multiple_palindromes(self, config_file):
        """Test with multiple palindromes."""
        manacher = ManacherAlgorithm("banana", config_path=config_file)
        longest = manacher.get_longest_palindrome()
        assert longest in ["anana", "ana", "a", "n", "b"]

    def test_long_text(self, config_file):
        """Test with longer text."""
        text = "racecarracecar"
        manacher = ManacherAlgorithm(text, config_path=config_file)
        longest = manacher.get_longest_palindrome()
        assert len(longest) >= 7

    def test_palindrome_validation(self, config_file):
        """Test that longest palindrome is actually a palindrome."""
        texts = ["babad", "cbbd", "racecar", "banana", "abc"]
        for text in texts:
            manacher = ManacherAlgorithm(text, config_path=config_file)
            longest = manacher.get_longest_palindrome()
            assert longest == longest[::-1]

    def test_all_palindromes_sorted(self, config_file):
        """Test that all palindromes are sorted by length."""
        manacher = ManacherAlgorithm("babad", config_path=config_file)
        all_palindromes = manacher.get_all_palindromes()
        lengths = [len(p[0]) for p in all_palindromes]
        assert lengths == sorted(lengths, reverse=True)

    def test_palindrome_info_consistency(self, config_file):
        """Test consistency of palindrome info."""
        manacher = ManacherAlgorithm("babad", config_path=config_file)
        longest = manacher.get_longest_palindrome()
        info = manacher.get_longest_palindrome_info()
        assert info[0] == longest
        assert info[2] == len(longest)

    def test_count_palindromes_consistency(self, config_file):
        """Test palindrome count consistency."""
        manacher = ManacherAlgorithm("aaa", config_path=config_file)
        count = manacher.count_palindromes()
        all_palindromes = manacher.get_all_palindromes()
        assert count >= len(all_palindromes)
