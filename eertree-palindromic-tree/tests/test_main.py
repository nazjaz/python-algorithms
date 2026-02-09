"""Test suite for eertree (palindromic tree) implementation."""

import pytest

from src.main import Eertree, EertreeNode


class TestEertreeNode:
    """Test cases for EertreeNode class."""

    def test_node_initialization(self) -> None:
        """Test that a node is initialized correctly."""
        node = EertreeNode(5)
        assert node.length == 5
        assert node.edges == {}
        assert node.suffix_link is None
        assert node.count == 0


class TestEertree:
    """Test cases for Eertree class."""

    def test_empty_tree_initialization(self) -> None:
        """Test that an empty eertree is initialized correctly."""
        tree = Eertree()
        assert tree.imaginary_root.length == -1
        assert tree.empty_root.length == 0
        assert tree.current_node == tree.empty_root
        assert tree.string == ""
        assert len(tree.nodes) == 2

    def test_build_single_character(self) -> None:
        """Test building eertree with a single character."""
        tree = Eertree()
        tree.build("a")
        palindromes = tree.get_all_palindromes()
        assert "a" in palindromes
        assert len(palindromes) == 1

    def test_build_simple_palindrome(self) -> None:
        """Test building eertree with a simple palindrome."""
        tree = Eertree()
        tree.build("aba")
        palindromes = tree.get_all_palindromes()
        assert "a" in palindromes
        assert "b" in palindromes
        assert "aba" in palindromes
        assert len(palindromes) == 3

    def test_build_repeated_characters(self) -> None:
        """Test building eertree with repeated characters."""
        tree = Eertree()
        tree.build("aaa")
        palindromes = tree.get_all_palindromes()
        assert "a" in palindromes
        assert "aa" in palindromes
        assert "aaa" in palindromes
        assert len(palindromes) == 3

    def test_build_complex_string(self) -> None:
        """Test building eertree with a complex string."""
        tree = Eertree()
        tree.build("abacaba")
        palindromes = tree.get_all_palindromes()
        expected = {"a", "b", "c", "aba", "aca", "bacab", "abacaba"}
        assert expected.issubset(palindromes)

    def test_count_distinct_palindromes(self) -> None:
        """Test counting distinct palindromes."""
        tree = Eertree()
        tree.build("aba")
        assert tree.count_distinct_palindromes() == 3

        tree.build("aaa")
        assert tree.count_distinct_palindromes() == 3

        tree.build("abacaba")
        assert tree.count_distinct_palindromes() == 7

    def test_count_total_palindromes(self) -> None:
        """Test counting total palindromes including duplicates."""
        tree = Eertree()
        tree.build("aaa")
        total = tree.count_total_palindromes()
        assert total >= 3

    def test_get_palindrome_count_existing(self) -> None:
        """Test getting count of an existing palindrome."""
        tree = Eertree()
        tree.build("aba")
        assert tree.get_palindrome_count("a") > 0
        assert tree.get_palindrome_count("b") > 0
        assert tree.get_palindrome_count("aba") > 0

    def test_get_palindrome_count_nonexistent(self) -> None:
        """Test getting count of a non-existent palindrome."""
        tree = Eertree()
        tree.build("aba")
        assert tree.get_palindrome_count("c") == 0
        assert tree.get_palindrome_count("ab") == 0

    def test_get_palindrome_count_invalid(self) -> None:
        """Test getting count of a non-palindrome string."""
        tree = Eertree()
        tree.build("aba")
        assert tree.get_palindrome_count("ab") == 0

    def test_is_palindrome_substring_valid(self) -> None:
        """Test checking valid palindrome substrings."""
        tree = Eertree()
        tree.build("abacaba")
        assert tree.is_palindrome_substring("a") is True
        assert tree.is_palindrome_substring("aba") is True
        assert tree.is_palindrome_substring("abacaba") is True

    def test_is_palindrome_substring_invalid(self) -> None:
        """Test checking invalid palindrome substrings."""
        tree = Eertree()
        tree.build("abacaba")
        assert tree.is_palindrome_substring("ab") is False
        assert tree.is_palindrome_substring("abc") is False
        assert tree.is_palindrome_substring("xyz") is False

    def test_get_longest_palindrome(self) -> None:
        """Test finding the longest palindrome."""
        tree = Eertree()
        tree.build("abacaba")
        longest = tree.get_longest_palindrome()
        assert longest == "abacaba"

        tree.build("racecar")
        longest = tree.get_longest_palindrome()
        assert longest == "racecar"

    def test_get_longest_palindrome_single_char(self) -> None:
        """Test finding longest palindrome in single character string."""
        tree = Eertree()
        tree.build("a")
        longest = tree.get_longest_palindrome()
        assert longest == "a"

    def test_add_char_incremental(self) -> None:
        """Test adding characters incrementally."""
        tree = Eertree()
        tree.add_char("a")
        tree.add_char("b")
        tree.add_char("a")
        palindromes = tree.get_all_palindromes()
        assert "a" in palindromes
        assert "b" in palindromes
        assert "aba" in palindromes

    def test_rebuild_tree(self) -> None:
        """Test rebuilding the tree with a new string."""
        tree = Eertree()
        tree.build("aba")
        assert tree.count_distinct_palindromes() == 3

        tree.build("xyz")
        assert tree.count_distinct_palindromes() == 3
        palindromes = tree.get_all_palindromes()
        assert "x" in palindromes
        assert "y" in palindromes
        assert "z" in palindromes

    def test_empty_string(self) -> None:
        """Test handling of empty string."""
        tree = Eertree()
        tree.build("")
        assert tree.count_distinct_palindromes() == 0
        assert tree.get_longest_palindrome() == ""

    def test_special_characters(self) -> None:
        """Test handling of special characters."""
        tree = Eertree()
        tree.build("a!a")
        palindromes = tree.get_all_palindromes()
        assert "a" in palindromes
        assert "!" in palindromes
        assert "a!a" in palindromes

    def test_numeric_string(self) -> None:
        """Test handling of numeric strings."""
        tree = Eertree()
        tree.build("121")
        palindromes = tree.get_all_palindromes()
        assert "1" in palindromes
        assert "2" in palindromes
        assert "121" in palindromes

    def test_mixed_case(self) -> None:
        """Test handling of mixed case strings."""
        tree = Eertree()
        tree.build("aBa")
        palindromes = tree.get_all_palindromes()
        assert "a" in palindromes
        assert "B" in palindromes
        assert "aBa" in palindromes

    def test_long_string(self) -> None:
        """Test handling of longer strings."""
        tree = Eertree()
        long_string = "a" * 100
        tree.build(long_string)
        distinct = tree.count_distinct_palindromes()
        assert distinct == 100

    def test_palindrome_count_accuracy(self) -> None:
        """Test that palindrome counts are accurate."""
        tree = Eertree()
        tree.build("aaa")
        assert tree.get_palindrome_count("a") >= 3
        assert tree.get_palindrome_count("aa") >= 2
        assert tree.get_palindrome_count("aaa") >= 1

    def test_all_palindromes_sorted(self) -> None:
        """Test that get_all_palindromes returns all expected palindromes."""
        tree = Eertree()
        tree.build("abacaba")
        palindromes = tree.get_all_palindromes()
        assert len(palindromes) == 7
        assert all(tree._is_palindrome(p) for p in palindromes)
