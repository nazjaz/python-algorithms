"""Unit tests for suffix array module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import SuffixArray


class TestSuffixArray:
    """Test cases for SuffixArray class."""

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

    def test_suffix_array_creation(self, config_file):
        """Test SuffixArray creation."""
        sa = SuffixArray("banana", config_path=config_file)
        assert sa.get_size() == 7
        assert len(sa.get_suffix_array()) == 7
        assert len(sa.get_lcp_array()) == 7

    def test_suffix_array_empty_text(self):
        """Test creation with empty text."""
        with pytest.raises(ValueError):
            SuffixArray("")

    def test_get_suffix_array(self, config_file):
        """Test getting suffix array."""
        sa = SuffixArray("abc", config_path=config_file)
        suffix_array = sa.get_suffix_array()
        assert len(suffix_array) == 4
        assert isinstance(suffix_array, list)

    def test_get_lcp_array(self, config_file):
        """Test getting LCP array."""
        sa = SuffixArray("banana", config_path=config_file)
        lcp_array = sa.get_lcp_array()
        assert len(lcp_array) == 7
        assert all(isinstance(x, int) for x in lcp_array)

    def test_get_inverse_suffix_array(self, config_file):
        """Test getting inverse suffix array."""
        sa = SuffixArray("abc", config_path=config_file)
        inverse = sa.get_inverse_suffix_array()
        assert len(inverse) == 4

    def test_get_suffix(self, config_file):
        """Test getting suffix at index."""
        sa = SuffixArray("abc", config_path=config_file)
        suffix = sa.get_suffix(0)
        assert isinstance(suffix, str)
        assert len(suffix) > 0

    def test_get_suffix_invalid_index(self, config_file):
        """Test getting suffix with invalid index."""
        sa = SuffixArray("abc", config_path=config_file)
        with pytest.raises(ValueError):
            sa.get_suffix(-1)
        with pytest.raises(ValueError):
            sa.get_suffix(10)

    def test_get_all_suffixes(self, config_file):
        """Test getting all suffixes."""
        sa = SuffixArray("abc", config_path=config_file)
        suffixes = sa.get_all_suffixes()
        assert len(suffixes) == 4
        assert all(isinstance(s, str) for s in suffixes)

    def test_search_existing_pattern(self, config_file):
        """Test searching for existing pattern."""
        sa = SuffixArray("banana", config_path=config_file)
        occurrences = sa.search("ana")
        assert len(occurrences) > 0
        assert all(isinstance(pos, int) for pos in occurrences)

    def test_search_nonexistent_pattern(self, config_file):
        """Test searching for nonexistent pattern."""
        sa = SuffixArray("banana", config_path=config_file)
        occurrences = sa.search("xyz")
        assert len(occurrences) == 0

    def test_search_empty_pattern(self, config_file):
        """Test searching for empty pattern."""
        sa = SuffixArray("abc", config_path=config_file)
        occurrences = sa.search("")
        assert len(occurrences) == 3

    def test_get_lcp(self, config_file):
        """Test getting LCP between two suffixes."""
        sa = SuffixArray("banana", config_path=config_file)
        lcp = sa.get_lcp(0, 1)
        assert isinstance(lcp, int)
        assert lcp >= 0

    def test_get_lcp_same_index(self, config_file):
        """Test getting LCP with same index."""
        sa = SuffixArray("banana", config_path=config_file)
        lcp = sa.get_lcp(0, 0)
        assert lcp > 0

    def test_get_lcp_invalid_indices(self, config_file):
        """Test getting LCP with invalid indices."""
        sa = SuffixArray("abc", config_path=config_file)
        with pytest.raises(ValueError):
            sa.get_lcp(-1, 0)
        with pytest.raises(ValueError):
            sa.get_lcp(0, 10)

    def test_get_longest_common_substring(self, config_file):
        """Test finding longest common substring."""
        sa = SuffixArray("banana", config_path=config_file)
        longest = sa.get_longest_common_substring()
        assert isinstance(longest, str)
        assert len(longest) > 0

    def test_get_all_longest_common_substrings(self, config_file):
        """Test finding all longest common substrings."""
        sa = SuffixArray("banana", config_path=config_file)
        all_longest = sa.get_all_longest_common_substrings()
        assert isinstance(all_longest, list)
        assert all(isinstance(s, str) for s in all_longest)

    def test_get_size(self, config_file):
        """Test getting size."""
        sa = SuffixArray("abc", config_path=config_file)
        assert sa.get_size() == 4

    def test_get_text(self, config_file):
        """Test getting original text."""
        text = "banana"
        sa = SuffixArray(text, config_path=config_file)
        assert sa.get_text() == text

    def test_is_valid(self, config_file):
        """Test validation."""
        sa = SuffixArray("banana", config_path=config_file)
        assert sa.is_valid() is True

    def test_simple_text(self, config_file):
        """Test with simple text."""
        sa = SuffixArray("abc", config_path=config_file)
        assert sa.is_valid() is True
        occurrences = sa.search("a")
        assert len(occurrences) > 0

    def test_single_character(self, config_file):
        """Test with single character."""
        sa = SuffixArray("a", config_path=config_file)
        assert sa.get_size() == 2
        assert sa.is_valid() is True

    def test_repeated_characters(self, config_file):
        """Test with repeated characters."""
        sa = SuffixArray("aaa", config_path=config_file)
        assert sa.is_valid() is True
        occurrences = sa.search("a")
        assert len(occurrences) > 0

    def test_long_text(self, config_file):
        """Test with longer text."""
        text = "mississippi"
        sa = SuffixArray(text, config_path=config_file)
        assert sa.is_valid() is True
        occurrences = sa.search("ssi")
        assert len(occurrences) == 2

    def test_suffix_array_sorted(self, config_file):
        """Test that suffixes are sorted."""
        sa = SuffixArray("banana", config_path=config_file)
        suffixes = sa.get_all_suffixes()
        for i in range(len(suffixes) - 1):
            assert suffixes[i] <= suffixes[i + 1]

    def test_lcp_array_properties(self, config_file):
        """Test LCP array properties."""
        sa = SuffixArray("banana", config_path=config_file)
        lcp_array = sa.get_lcp_array()
        assert lcp_array[0] == 0
        assert all(x >= 0 for x in lcp_array)

    def test_search_all_occurrences(self, config_file):
        """Test finding all occurrences."""
        sa = SuffixArray("banana", config_path=config_file)
        occurrences = sa.search("ana")
        assert len(occurrences) == 2
        assert 1 in occurrences
        assert 3 in occurrences

    def test_get_lcp_consistency(self, config_file):
        """Test LCP consistency."""
        sa = SuffixArray("banana", config_path=config_file)
        lcp_array = sa.get_lcp_array()

        for i in range(1, sa.get_size()):
            suffix_i = sa.get_suffix(i - 1)
            suffix_j = sa.get_suffix(i)
            common = 0
            while (
                common < len(suffix_i)
                and common < len(suffix_j)
                and suffix_i[common] == suffix_j[common]
            ):
                common += 1
            assert lcp_array[i] == common

    def test_longest_common_substring_length(self, config_file):
        """Test longest common substring length."""
        sa = SuffixArray("banana", config_path=config_file)
        longest = sa.get_longest_common_substring()
        lcp_array = sa.get_lcp_array()
        max_lcp = max(lcp_array)
        assert len(longest) == max_lcp
