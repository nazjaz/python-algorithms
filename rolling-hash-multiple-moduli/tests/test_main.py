"""Test suite for rolling hash with multiple moduli implementation."""

import pytest

from src.main import RollingHash


class TestRollingHash:
    """Test cases for RollingHash class."""

    def test_initialization_default(self) -> None:
        """Test default initialization."""
        rh = RollingHash()
        assert len(rh.moduli) == 3
        assert rh.base == 256
        assert rh.num_moduli == 3

    def test_initialization_custom(self) -> None:
        """Test initialization with custom moduli and base."""
        moduli = [1000000007, 1000000009]
        base = 131
        rh = RollingHash(moduli=moduli, base=base)
        assert rh.moduli == moduli
        assert rh.base == base
        assert rh.num_moduli == 2

    def test_initialization_empty_moduli(self) -> None:
        """Test that empty moduli list raises ValueError."""
        with pytest.raises(ValueError, match="At least one modulus"):
            RollingHash(moduli=[])

    def test_initialization_invalid_base(self) -> None:
        """Test that invalid base raises ValueError."""
        with pytest.raises(ValueError, match="Base must be at least 2"):
            RollingHash(base=1)

    def test_hash_string_empty(self) -> None:
        """Test hashing empty string."""
        rh = RollingHash()
        hashes = rh.hash_string("")
        assert hashes == (0, 0, 0)

    def test_hash_string_single_char(self) -> None:
        """Test hashing single character."""
        rh = RollingHash()
        hashes = rh.hash_string("a")
        assert len(hashes) == 3
        assert all(h > 0 for h in hashes)

    def test_hash_string_consistency(self) -> None:
        """Test that same string produces same hash."""
        rh = RollingHash()
        text = "hello"
        hash1 = rh.hash_string(text)
        hash2 = rh.hash_string(text)
        assert hash1 == hash2

    def test_hash_string_different_strings(self) -> None:
        """Test that different strings produce different hashes."""
        rh = RollingHash()
        hash1 = rh.hash_string("hello")
        hash2 = rh.hash_string("world")
        assert hash1 != hash2

    def test_hash_substring_valid(self) -> None:
        """Test hashing valid substring."""
        rh = RollingHash()
        text = "hello world"
        substring_hash = rh.hash_substring(text, 0, 5)
        full_hash = rh.hash_string("hello")
        assert substring_hash == full_hash

    def test_hash_substring_middle(self) -> None:
        """Test hashing substring from middle of string."""
        rh = RollingHash()
        text = "hello world"
        substring_hash = rh.hash_substring(text, 6, 5)
        expected_hash = rh.hash_string("world")
        assert substring_hash == expected_hash

    def test_hash_substring_empty(self) -> None:
        """Test hashing empty substring."""
        rh = RollingHash()
        text = "hello"
        hash_result = rh.hash_substring(text, 0, 0)
        assert hash_result == (0, 0, 0)

    def test_hash_substring_out_of_bounds(self) -> None:
        """Test that out of bounds substring raises IndexError."""
        rh = RollingHash()
        text = "hello"
        with pytest.raises(IndexError):
            rh.hash_substring(text, 0, 10)
        with pytest.raises(IndexError):
            rh.hash_substring(text, -1, 3)
        with pytest.raises(IndexError):
            rh.hash_substring(text, 3, 5)

    def test_build_prefix_hashes(self) -> None:
        """Test building prefix hash array."""
        rh = RollingHash()
        text = "abc"
        prefix_hashes = rh.build_prefix_hashes(text)
        assert len(prefix_hashes) == 3
        assert len(prefix_hashes[0]) == len(text) + 1

    def test_build_prefix_hashes_empty(self) -> None:
        """Test building prefix hashes for empty string."""
        rh = RollingHash()
        prefix_hashes = rh.build_prefix_hashes("")
        assert len(prefix_hashes) == 3
        assert prefix_hashes[0] == [0]

    def test_get_substring_hash_from_prefix(self) -> None:
        """Test getting substring hash from prefix array."""
        rh = RollingHash()
        text = "hello world"
        prefix_hashes = rh.build_prefix_hashes(text)

        substring_hash = rh.get_substring_hash_from_prefix(
            prefix_hashes, 0, 5
        )
        direct_hash = rh.hash_string("hello")
        assert substring_hash == direct_hash

    def test_get_substring_hash_from_prefix_middle(self) -> None:
        """Test getting middle substring hash from prefix array."""
        rh = RollingHash()
        text = "hello world"
        prefix_hashes = rh.build_prefix_hashes(text)

        substring_hash = rh.get_substring_hash_from_prefix(
            prefix_hashes, 6, 5
        )
        direct_hash = rh.hash_string("world")
        assert substring_hash == direct_hash

    def test_get_substring_hash_from_prefix_invalid(self) -> None:
        """Test invalid prefix hash structure."""
        rh = RollingHash()
        with pytest.raises(ValueError):
            rh.get_substring_hash_from_prefix([], 0, 1)

    def test_find_pattern_single_occurrence(self) -> None:
        """Test finding pattern with single occurrence."""
        rh = RollingHash()
        text = "hello world"
        pattern = "world"
        occurrences = rh.find_pattern(text, pattern)
        assert occurrences == [6]

    def test_find_pattern_multiple_occurrences(self) -> None:
        """Test finding pattern with multiple occurrences."""
        rh = RollingHash()
        text = "abababab"
        pattern = "ab"
        occurrences = rh.find_pattern(text, pattern)
        assert occurrences == [0, 2, 4, 6]

    def test_find_pattern_no_occurrence(self) -> None:
        """Test finding pattern that doesn't exist."""
        rh = RollingHash()
        text = "hello world"
        pattern = "xyz"
        occurrences = rh.find_pattern(text, pattern)
        assert occurrences == []

    def test_find_pattern_empty_pattern(self) -> None:
        """Test finding empty pattern."""
        rh = RollingHash()
        text = "hello"
        occurrences = rh.find_pattern(text, "")
        assert len(occurrences) == len(text) + 1

    def test_find_pattern_pattern_longer_than_text(self) -> None:
        """Test finding pattern longer than text."""
        rh = RollingHash()
        text = "hello"
        pattern = "hello world"
        occurrences = rh.find_pattern(text, pattern)
        assert occurrences == []

    def test_find_pattern_exact_match(self) -> None:
        """Test finding pattern that matches entire text."""
        rh = RollingHash()
        text = "hello"
        pattern = "hello"
        occurrences = rh.find_pattern(text, pattern)
        assert occurrences == [0]

    def test_compare_substrings_equal(self) -> None:
        """Test comparing equal substrings."""
        rh = RollingHash()
        text1 = "hello world"
        text2 = "hello world"
        result = rh.compare_substrings(text1, 0, text2, 0, 5)
        assert result is True

    def test_compare_substrings_different(self) -> None:
        """Test comparing different substrings."""
        rh = RollingHash()
        text1 = "hello world"
        text2 = "world hello"
        result = rh.compare_substrings(text1, 0, text2, 0, 5)
        assert result is False

    def test_compare_substrings_same_text_different_positions(self) -> None:
        """Test comparing substrings at different positions."""
        rh = RollingHash()
        text = "ababab"
        result = rh.compare_substrings(text, 0, text, 2, 2)
        assert result is True

    def test_compare_substrings_out_of_bounds(self) -> None:
        """Test comparing substrings with out of bounds indices."""
        rh = RollingHash()
        text = "hello"
        with pytest.raises(IndexError):
            rh.compare_substrings(text, 0, text, 0, 10)

    def test_longest_common_prefix_hash_same(self) -> None:
        """Test longest common prefix of identical strings."""
        rh = RollingHash()
        text = "hello world"
        result = rh.longest_common_prefix_hash(text, 0, text, 0)
        assert result == len(text)

    def test_longest_common_prefix_hash_different(self) -> None:
        """Test longest common prefix of different strings."""
        rh = RollingHash()
        text1 = "hello world"
        text2 = "hello there"
        result = rh.longest_common_prefix_hash(text1, 0, text2, 0)
        assert result == 6

    def test_longest_common_prefix_hash_no_common(self) -> None:
        """Test longest common prefix with no common characters."""
        rh = RollingHash()
        text1 = "hello"
        text2 = "world"
        result = rh.longest_common_prefix_hash(text1, 0, text2, 0)
        assert result == 0

    def test_longest_common_prefix_hash_partial(self) -> None:
        """Test longest common prefix with partial match."""
        rh = RollingHash()
        text1 = "abcde"
        text2 = "abcfg"
        result = rh.longest_common_prefix_hash(text1, 0, text2, 0)
        assert result == 3

    def test_roll_hash_consistency(self) -> None:
        """Test that rolling hash produces consistent results."""
        rh = RollingHash()
        text = "abcdef"
        pattern = "bcd"

        pattern_hash = rh.hash_string(pattern)

        window_hash = rh.hash_substring(text, 1, 3)
        assert window_hash == pattern_hash

    def test_multiple_moduli_collision_resistance(self) -> None:
        """Test that multiple moduli reduce hash collisions."""
        rh = RollingHash(moduli=[1000000007, 1000000009, 1000000021])
        text1 = "hello"
        text2 = "world"

        hash1 = rh.hash_string(text1)
        hash2 = rh.hash_string(text2)

        assert hash1 != hash2

    def test_large_string(self) -> None:
        """Test hashing large string."""
        rh = RollingHash()
        large_text = "a" * 1000
        hashes = rh.hash_string(large_text)
        assert len(hashes) == 3
        assert all(h >= 0 for h in hashes)

    def test_special_characters(self) -> None:
        """Test hashing strings with special characters."""
        rh = RollingHash()
        text = "hello!@#$%^&*()world"
        hashes = rh.hash_string(text)
        assert len(hashes) == 3

    def test_unicode_characters(self) -> None:
        """Test hashing strings with unicode characters."""
        rh = RollingHash()
        text = "hello 世界"
        hashes = rh.hash_string(text)
        assert len(hashes) == 3

    def test_prefix_hash_consistency(self) -> None:
        """Test that prefix hash method matches direct hashing."""
        rh = RollingHash()
        text = "hello world"
        prefix_hashes = rh.build_prefix_hashes(text)

        for i in range(len(text)):
            for length in range(1, len(text) - i + 1):
                hash1 = rh.get_substring_hash_from_prefix(
                    prefix_hashes, i, length
                )
                hash2 = rh.hash_substring(text, i, length)
                assert hash1 == hash2
