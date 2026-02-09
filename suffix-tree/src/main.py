"""Suffix Tree Construction Using Ukkonen's Algorithm.

This module provides functionality to construct suffix trees using Ukkonen's
algorithm for efficient substring matching. Ukkonen's algorithm builds a
suffix tree in O(n) time for a string of length n, enabling O(m) substring
queries where m is the pattern length.
"""

import logging
import logging.handlers
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class SuffixTreeNode:
    """Node in suffix tree."""

    def __init__(
        self,
        start: Optional[int] = None,
        end: Optional[int] = None,
        suffix_link: Optional["SuffixTreeNode"] = None,
    ) -> None:
        """Initialize SuffixTreeNode.

        Args:
            start: Start index of edge label (None for root).
            end: End index of edge label (None for root).
            suffix_link: Suffix link to another node.
        """
        self.start = start
        self.end = end
        self.suffix_link = suffix_link
        self.children: Dict[str, "SuffixTreeNode"] = {}
        self.leaf_count = 0

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"SuffixTreeNode(start={self.start}, end={self.end}, "
            f"children={len(self.children)})"
        )

    def edge_length(self, string_end: int) -> int:
        """Calculate edge length.

        Args:
            string_end: End index of the string.

        Returns:
            Length of edge label.
        """
        if self.end is None:
            return 0
        return (self.end if self.end != -1 else string_end) - self.start

    def get_edge_label(self, text: str) -> str:
        """Get edge label from text.

        Args:
            text: The input string.

        Returns:
            Edge label substring.
        """
        if self.start is None or self.end is None:
            return ""
        end_idx = self.end if self.end != -1 else len(text)
        return text[self.start:end_idx]


class SuffixTree:
    """Suffix tree constructed using Ukkonen's algorithm."""

    def __init__(self, text: str, config_path: str = "config.yaml") -> None:
        """Initialize SuffixTree with text.

        Args:
            text: Input string to build suffix tree for.
            config_path: Path to configuration YAML file.
        """
        if not text:
            raise ValueError("Text cannot be empty")
        self.text = text + "$"
        self._setup_logging()
        self.config = self._load_config(config_path)
        self.root = SuffixTreeNode()
        self.active_node = self.root
        self.active_edge = -1
        self.active_length = 0
        self.remaining = 0
        self.last_new_node: Optional[SuffixTreeNode] = None
        self.string_end = -1
        self._build_tree()
        logger.info(f"Suffix tree constructed for text of length {len(text)}")

    def _setup_logging(self) -> None:
        """Configure logging for the application."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        log_file = log_dir / "suffix_tree.log"
        handler = logging.handlers.RotatingFileHandler(
            log_file, maxBytes=10485760, backupCount=5
        )
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)

        logger.setLevel(logging.INFO)
        logger.addHandler(handler)

    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file.

        Args:
            config_path: Path to configuration file.

        Returns:
            Configuration dictionary.

        Raises:
            FileNotFoundError: If configuration file does not exist.
        """
        try:
            with open(config_path, "r") as f:
                config = yaml.safe_load(f)
                logger.info(f"Configuration loaded from {config_path}")
                return config or {}
        except FileNotFoundError:
            logger.warning(f"Configuration file not found: {config_path}")
            return {}

    def _build_tree(self) -> None:
        """Build suffix tree using Ukkonen's algorithm."""
        n = len(self.text)
        self.string_end = -1

        for i in range(n):
            self._extend_suffix_tree(i)

    def _extend_suffix_tree(self, pos: int) -> None:
        """Extend suffix tree for character at position pos.

        Args:
            pos: Current position in text.
        """
        self.string_end = pos
        self.remaining += 1
        self.last_new_node = None

        while self.remaining > 0:
            if self.active_length == 0:
                self.active_edge = pos

            active_char = self.text[self.active_edge]

            if active_char not in self.active_node.children:
                child = SuffixTreeNode(start=pos, end=-1)
                self.active_node.children[active_char] = child
                self._rule_2_new_leaf()
            else:
                next_node = self.active_node.children[active_char]
                edge_length = next_node.edge_length(self.string_end)

                if self.active_length >= edge_length:
                    self.active_node = next_node
                    self.active_length -= edge_length
                    self.active_edge += edge_length
                    continue

                if self.text[next_node.start + self.active_length] == self.text[pos]:
                    self._rule_3_extension()
                    break

                self._rule_2_split(next_node, pos)

            self.remaining -= 1

            if (
                self.active_node == self.root
                and self.active_length > 0
            ):
                self.active_length -= 1
                self.active_edge = pos - self.remaining + 1
            elif self.active_node != self.root:
                if self.active_node.suffix_link:
                    self.active_node = self.active_node.suffix_link
                else:
                    self.active_node = self.root

    def _rule_2_new_leaf(self) -> None:
        """Rule 2: Create new leaf node."""
        if self.last_new_node:
            self.last_new_node.suffix_link = self.active_node
            self.last_new_node = None

    def _rule_2_split(
        self, node: SuffixTreeNode, pos: int
    ) -> None:
        """Rule 2: Split edge and create new internal node.

        Args:
            node: Node to split.
            pos: Current position.
        """
        split_node = SuffixTreeNode(
            start=node.start,
            end=node.start + self.active_length
        )
        self.active_node.children[self.text[self.active_edge]] = split_node

        node.start += self.active_length
        split_node.children[self.text[node.start]] = node

        new_leaf = SuffixTreeNode(start=pos, end=-1)
        split_node.children[self.text[pos]] = new_leaf

        if self.last_new_node:
            self.last_new_node.suffix_link = split_node

        self.last_new_node = split_node

    def _rule_3_extension(self) -> None:
        """Rule 3: Suffix already exists, no extension needed."""
        if self.last_new_node:
            self.last_new_node.suffix_link = self.active_node
            self.last_new_node = None

        self.active_length += 1

    def search(self, pattern: str) -> bool:
        """Search for pattern in suffix tree.

        Args:
            pattern: Pattern to search for.

        Returns:
            True if pattern found, False otherwise.
        """
        if not pattern:
            return True

        logger.info(f"Searching for pattern: {pattern}")
        current = self.root
        i = 0

        while i < len(pattern):
            char = pattern[i]
            if char not in current.children:
                logger.info(f"Pattern '{pattern}' not found")
                return False

            node = current.children[char]
            edge_label = node.get_edge_label(self.text)
            j = 0

            while j < len(edge_label) and i < len(pattern):
                if edge_label[j] != pattern[i]:
                    logger.info(f"Pattern '{pattern}' not found")
                    return False
                j += 1
                i += 1

            if i < len(pattern):
                current = node
            else:
                logger.info(f"Pattern '{pattern}' found")
                return True

        logger.info(f"Pattern '{pattern}' found")
        return True

    def find_all_occurrences(self, pattern: str) -> List[int]:
        """Find all occurrences of pattern in text.

        Args:
            pattern: Pattern to search for.

        Returns:
            List of starting positions where pattern occurs.
        """
        if not pattern:
            return list(range(len(self.text) - 1))

        logger.info(f"Finding all occurrences of pattern: {pattern}")

        node = self._find_pattern_node(pattern)
        if node is None:
            return []

        occurrences: List[int] = []
        self._collect_leaf_indices(node, occurrences, pattern)

        logger.info(
            f"Found {len(occurrences)} occurrences of pattern '{pattern}'"
        )
        return sorted(occurrences)

    def _find_pattern_node(self, pattern: str) -> Optional[SuffixTreeNode]:
        """Find node corresponding to pattern.

        Args:
            pattern: Pattern to find.

        Returns:
            Node if found, None otherwise.
        """
        current = self.root
        i = 0

        while i < len(pattern):
            char = pattern[i]
            if char not in current.children:
                return None

            node = current.children[char]
            edge_label = node.get_edge_label(self.text)
            j = 0

            while j < len(edge_label) and i < len(pattern):
                if edge_label[j] != pattern[i]:
                    return None
                j += 1
                i += 1

            if i < len(pattern):
                current = node
            else:
                return node

        return current

    def _collect_leaf_indices(
        self,
        node: SuffixTreeNode,
        occurrences: List[int],
        pattern: str,
    ) -> None:
        """Collect all leaf indices from subtree.

        Args:
            node: Current node.
            occurrences: List to append indices to.
            pattern: Pattern being searched.
        """
        if not node.children:
            start = node.start - len(pattern) + 1
            if start >= 0:
                occurrences.append(start)
            return

        for child in node.children.values():
            self._collect_leaf_indices(child, occurrences, pattern)

    def get_longest_repeated_substring(self) -> str:
        """Find longest repeated substring.

        Returns:
            Longest repeated substring.
        """
        result: List[str] = [""]
        self._find_longest_repeated(self.root, "", result)
        return result[0]

    def _find_longest_repeated(
        self,
        node: SuffixTreeNode,
        current: str,
        result: List[str],
    ) -> None:
        """Helper to find longest repeated substring.

        Args:
            node: Current node.
            current: Current path string.
            result: List to store result.
        """
        if len(node.children) > 1:
            if len(current) > len(result[0]):
                result[0] = current

        for char, child in node.children.items():
            edge_label = child.get_edge_label(self.text)
            self._find_longest_repeated(child, current + edge_label, result)

    def get_all_suffixes(self) -> List[str]:
        """Get all suffixes of the text.

        Returns:
            List of all suffixes.
        """
        suffixes: List[str] = []
        self._collect_suffixes(self.root, "", suffixes)
        return sorted(suffixes)

    def _collect_suffixes(
        self,
        node: SuffixTreeNode,
        current: str,
        suffixes: List[str],
    ) -> None:
        """Helper to collect all suffixes.

        Args:
            node: Current node.
            current: Current path string.
            suffixes: List to append suffixes to.
        """
        if not node.children:
            suffixes.append(current)
            return

        for char, child in node.children.items():
            edge_label = child.get_edge_label(self.text)
            self._collect_suffixes(child, current + edge_label, suffixes)

    def get_substring_count(self, pattern: str) -> int:
        """Count occurrences of pattern.

        Args:
            pattern: Pattern to count.

        Returns:
            Number of occurrences.
        """
        return len(self.find_all_occurrences(pattern))

    def is_suffix(self, pattern: str) -> bool:
        """Check if pattern is a suffix of text.

        Args:
            pattern: Pattern to check.

        Returns:
            True if pattern is suffix, False otherwise.
        """
        if not pattern:
            return True

        text_without_sentinel = self.text[:-1]
        if len(pattern) > len(text_without_sentinel):
            return False

        return text_without_sentinel.endswith(pattern)

    def get_tree_size(self) -> int:
        """Get number of nodes in tree.

        Returns:
            Number of nodes.
        """
        return self._count_nodes(self.root)

    def _count_nodes(self, node: SuffixTreeNode) -> int:
        """Helper to count nodes.

        Args:
            node: Current node.

        Returns:
            Number of nodes in subtree.
        """
        count = 1
        for child in node.children.values():
            count += self._count_nodes(child)
        return count

    def is_valid(self) -> bool:
        """Validate suffix tree structure.

        Returns:
            True if tree is valid, False otherwise.
        """
        return self._validate_tree(self.root, 0)

    def _validate_tree(
        self, node: SuffixTreeNode, depth: int
    ) -> bool:
        """Helper to validate tree.

        Args:
            node: Current node.
            depth: Current depth.

        Returns:
            True if valid, False otherwise.
        """
        for char, child in node.children.items():
            if child.start is None:
                logger.error("Child node has None start")
                return False

            if child.end is not None and child.end != -1:
                if child.end <= child.start:
                    logger.error(
                        f"Invalid edge: start={child.start}, end={child.end}"
                    )
                    return False

            if not self._validate_tree(child, depth + 1):
                return False

        return True


def main() -> None:
    """Main function to demonstrate suffix tree operations."""
    text = "banana"
    logger.info(f"Building suffix tree for text: {text}")

    tree = SuffixTree(text)

    logger.info(f"Tree size: {tree.get_tree_size()} nodes")
    logger.info(f"Tree is valid: {tree.is_valid()}")

    patterns = ["ana", "nan", "ban", "xyz"]
    for pattern in patterns:
        found = tree.search(pattern)
        logger.info(f"Pattern '{pattern}': {'found' if found else 'not found'}")

    pattern = "ana"
    occurrences = tree.find_all_occurrences(pattern)
    logger.info(f"Occurrences of '{pattern}': {occurrences}")

    longest_repeated = tree.get_longest_repeated_substring()
    logger.info(f"Longest repeated substring: '{longest_repeated}'")

    substring_count = tree.get_substring_count("an")
    logger.info(f"Count of 'an': {substring_count}")


if __name__ == "__main__":
    main()
