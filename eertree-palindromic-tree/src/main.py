"""Eertree (Palindromic Tree) implementation for efficient palindrome queries.

This module implements an eertree data structure that efficiently stores all
distinct palindromic substrings of a string and supports various query operations
including counting palindromes, finding all palindromes, and checking if a
substring is a palindrome.
"""

import logging
import sys
from typing import Dict, List, Optional, Set

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class EertreeNode:
    """Node in the eertree representing a palindrome.

    Each node stores information about a palindrome including its length,
    edges to child nodes, and a suffix link to another palindrome node.
    """

    def __init__(self, length: int) -> None:
        """Initialize an eertree node.

        Args:
            length: Length of the palindrome represented by this node.
        """
        self.length: int = length
        self.edges: Dict[str, "EertreeNode"] = {}
        self.suffix_link: Optional["EertreeNode"] = None
        self.count: int = 0


class Eertree:
    """Eertree (Palindromic Tree) data structure.

    Efficiently stores all distinct palindromic substrings of a string.
    Supports O(n) time construction and various query operations.
    """

    def __init__(self) -> None:
        """Initialize an empty eertree."""
        self.imaginary_root: EertreeNode = EertreeNode(-1)
        self.empty_root: EertreeNode = EertreeNode(0)
        self.imaginary_root.suffix_link = self.imaginary_root
        self.empty_root.suffix_link = self.imaginary_root
        self.current_node: EertreeNode = self.empty_root
        self.string: str = ""
        self.nodes: List[EertreeNode] = [
            self.imaginary_root,
            self.empty_root,
        ]

    def _get_suffix_link(
        self, node: EertreeNode, char: str, position: int
    ) -> EertreeNode:
        """Find the suffix link for a node when adding a character.

        Traverses suffix links until finding a palindrome that can be extended
        by the given character, or returns the imaginary root.

        Args:
            node: Current node to find suffix link for.
            char: Character being added.
            position: Current position in the string.

        Returns:
            Node that represents the longest palindromic suffix that can be
            extended by the given character.
        """
        while True:
            start_pos = position - node.length - 1
            if start_pos >= 0 and self.string[start_pos] == char:
                return node
            if node == self.imaginary_root:
                return self.empty_root
            node = node.suffix_link

    def add_char(self, char: str) -> Optional[EertreeNode]:
        """Add a character to the eertree and update current node.

        Args:
            char: Character to add to the string.

        Returns:
            New node created if a new palindrome was found, None otherwise.
        """
        self.string += char
        position = len(self.string) - 1

        suffix_node = self._get_suffix_link(
            self.current_node, char, position
        )

        if char in suffix_node.edges:
            self.current_node = suffix_node.edges[char]
            self.current_node.count += 1
            return None

        new_node = EertreeNode(suffix_node.length + 2)
        suffix_node.edges[char] = new_node
        self.nodes.append(new_node)

        if new_node.length == 1:
            new_node.suffix_link = self.empty_root
        else:
            next_suffix = self._get_suffix_link(
                suffix_node.suffix_link, char, position
            )
            new_node.suffix_link = next_suffix.edges.get(
                char, self.empty_root
            )

        new_node.count = 1
        self.current_node = new_node
        return new_node

    def build(self, text: str) -> None:
        """Build the eertree from a given string.

        Args:
            text: Input string to build the eertree from.
        """
        logger.info(f"Building eertree for string of length {len(text)}")
        self.string = ""
        self.current_node = self.empty_root
        self.nodes = [self.imaginary_root, self.empty_root]
        self.imaginary_root.edges.clear()
        self.empty_root.edges.clear()

        for char in text:
            self.add_char(char)

        self._update_counts()

    def _update_counts(self) -> None:
        """Update palindrome counts by propagating counts through suffix links.

        Counts are updated in reverse order to ensure all suffix links are
        processed after their parent nodes.
        """
        for i in range(len(self.nodes) - 1, 1, -1):
            node = self.nodes[i]
            if node.suffix_link:
                node.suffix_link.count += node.count

    def get_all_palindromes(self) -> Set[str]:
        """Get all distinct palindromic substrings in the string.

        Returns:
            Set of all distinct palindromic substrings.
        """
        palindromes: Set[str] = set()
        self._collect_palindromes(
            self.imaginary_root, "", palindromes
        )
        self._collect_palindromes(
            self.empty_root, "", palindromes
        )
        return palindromes

    def _collect_palindromes(
        self,
        node: EertreeNode,
        current: str,
        palindromes: Set[str],
    ) -> None:
        """Recursively collect all palindromes from the tree.

        Args:
            node: Current node being processed.
            current: Current palindrome string being built.
            palindromes: Set to collect palindromes into.
        """
        if node.length > 0:
            palindromes.add(current)

        for char, child in node.edges.items():
            if node == self.imaginary_root:
                new_palindrome = char
            elif node == self.empty_root:
                new_palindrome = char + char
            else:
                new_palindrome = char + current + char
            self._collect_palindromes(child, new_palindrome, palindromes)

    def count_distinct_palindromes(self) -> int:
        """Count the number of distinct palindromic substrings.

        Returns:
            Number of distinct palindromic substrings.
        """
        return len(self.get_all_palindromes())

    def count_total_palindromes(self) -> int:
        """Count the total number of palindromic substrings (with duplicates).

        Returns:
            Total count of all palindromic substrings including duplicates.
        """
        total = 0
        for node in self.nodes[2:]:
            total += node.count
        return total

    def get_palindrome_count(self, palindrome: str) -> int:
        """Get the count of occurrences of a specific palindrome.

        Args:
            palindrome: The palindrome string to count.

        Returns:
            Number of times the palindrome appears as a substring, or 0 if
            it's not a palindrome or doesn't exist.
        """
        if not self._is_palindrome(palindrome):
            return 0

        node = self._find_node(palindrome)
        if node:
            return node.count
        return 0

    def _is_palindrome(self, text: str) -> bool:
        """Check if a string is a palindrome.

        Args:
            text: String to check.

        Returns:
            True if the string is a palindrome, False otherwise.
        """
        return text == text[::-1]

    def _find_node(self, palindrome: str) -> Optional[EertreeNode]:
        """Find the node representing a specific palindrome.

        Uses the stored string to efficiently locate the node by checking
        if the palindrome exists and finding the corresponding node.

        Args:
            palindrome: Palindrome string to find.

        Returns:
            Node representing the palindrome, or None if not found.
        """
        if not palindrome:
            return self.empty_root

        if palindrome not in self.string:
            return None

        all_palindromes = self.get_all_palindromes()
        if palindrome not in all_palindromes:
            return None

        for node in self.nodes[2:]:
            if node.length == len(palindrome):
                if self._node_matches_palindrome(node, palindrome):
                    return node
        return None

    def _node_matches_palindrome(
        self, node: EertreeNode, palindrome: str
    ) -> bool:
        """Check if a node represents the given palindrome.

        Verifies by checking if the palindrome can be found in the string
        at positions that would create this node during tree construction.

        Args:
            node: Node to check.
            palindrome: Palindrome string to match.

        Returns:
            True if the node represents the palindrome, False otherwise.
        """
        if node.length != len(palindrome):
            return False

        for i in range(len(self.string) - len(palindrome) + 1):
            substr = self.string[i : i + len(palindrome)]
            if substr == palindrome and self._is_palindrome(substr):
                return True
        return False

    def is_palindrome_substring(self, substring: str) -> bool:
        """Check if a substring exists in the string and is a palindrome.

        Args:
            substring: Substring to check.

        Returns:
            True if the substring is a palindrome and exists in the string,
            False otherwise.
        """
        if not self._is_palindrome(substring):
            return False
        if substring not in self.string:
            return False
        all_palindromes = self.get_all_palindromes()
        return substring in all_palindromes

    def get_longest_palindrome(self) -> str:
        """Get the longest palindromic substring.

        Returns:
            Longest palindromic substring, or empty string if none exists.
        """
        longest = ""
        max_length = 0

        for palindrome in self.get_all_palindromes():
            if len(palindrome) > max_length:
                max_length = len(palindrome)
                longest = palindrome

        return longest


def main() -> None:
    """Main function to run the eertree CLI interface."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Eertree (Palindromic Tree) for palindrome queries"
    )
    parser.add_argument(
        "text",
        type=str,
        help="Input string to build eertree from",
    )
    parser.add_argument(
        "--count-distinct",
        action="store_true",
        help="Count distinct palindromic substrings",
    )
    parser.add_argument(
        "--count-total",
        action="store_true",
        help="Count total palindromic substrings (with duplicates)",
    )
    parser.add_argument(
        "--list-all",
        action="store_true",
        help="List all distinct palindromic substrings",
    )
    parser.add_argument(
        "--longest",
        action="store_true",
        help="Find the longest palindromic substring",
    )
    parser.add_argument(
        "--query",
        type=str,
        help="Check if a substring is a palindrome and get its count",
    )

    args = parser.parse_args()

    try:
        eertree = Eertree()
        eertree.build(args.text)

        if args.count_distinct:
            count = eertree.count_distinct_palindromes()
            print(f"Distinct palindromes: {count}")

        if args.count_total:
            count = eertree.count_total_palindromes()
            print(f"Total palindromes: {count}")

        if args.list_all:
            palindromes = sorted(eertree.get_all_palindromes())
            print(f"All distinct palindromes ({len(palindromes)}):")
            for p in palindromes:
                print(f"  {p}")

        if args.longest:
            longest = eertree.get_longest_palindrome()
            print(f"Longest palindrome: {longest}")

        if args.query:
            count = eertree.get_palindrome_count(args.query)
            is_pal = eertree.is_palindrome_substring(args.query)
            if is_pal:
                print(
                    f"'{args.query}' is a palindrome "
                    f"appearing {count} time(s)"
                )
            else:
                print(f"'{args.query}' is not a palindrome substring")

        if not any(
            [
                args.count_distinct,
                args.count_total,
                args.list_all,
                args.longest,
                args.query,
            ]
        ):
            distinct = eertree.count_distinct_palindromes()
            total = eertree.count_total_palindromes()
            longest = eertree.get_longest_palindrome()
            print(f"Input string: {args.text}")
            print(f"Distinct palindromes: {distinct}")
            print(f"Total palindromes: {total}")
            print(f"Longest palindrome: {longest}")

    except Exception as e:
        logger.error(f"Error processing string: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
