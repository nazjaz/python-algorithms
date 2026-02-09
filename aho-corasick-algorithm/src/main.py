"""Aho-Corasick Algorithm for Multiple Pattern Matching.

This module provides functionality to implement Aho-Corasick algorithm for
multiple pattern matching with automaton construction. The algorithm achieves
O(n + m + z) time complexity where n is text length, m is total pattern length,
and z is number of matches by building a finite automaton with failure links.
"""

import logging
import logging.handlers
from collections import deque
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class TrieNode:
    """Node in Aho-Corasick automaton."""

    def __init__(self) -> None:
        """Initialize TrieNode."""
        self.children: Dict[str, "TrieNode"] = {}
        self.failure: Optional["TrieNode"] = None
        self.output: Set[str] = set()
        self.is_end: bool = False


class AhoCorasickAlgorithm:
    """Aho-Corasick algorithm for multiple pattern matching."""

    def __init__(
        self, patterns: List[str], config_path: str = "config.yaml"
    ) -> None:
        """Initialize Aho-Corasick algorithm with patterns.

        Args:
            patterns: List of patterns to search for.
            config_path: Path to configuration YAML file.
        """
        if not patterns:
            raise ValueError("Patterns list cannot be empty")

        self.patterns = [p for p in patterns if p]
        if not self.patterns:
            raise ValueError("All patterns are empty")

        self._setup_logging()
        self.config = self._load_config(config_path)

        logger.info(f"Building Aho-Corasick automaton for {len(self.patterns)} patterns")
        self.root = TrieNode()
        self._build_trie()
        self._build_failure_links()
        self._build_output_links()

        logger.info("Aho-Corasick automaton constructed successfully")

    def _setup_logging(self) -> None:
        """Configure logging for the application."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        log_file = log_dir / "aho_corasick_algorithm.log"
        handler = logging.handlers.RotatingFileHandler(
            log_file, maxBytes=10485760, backupCount=5
        )
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)

        logger.setLevel(logging.INFO)
        logger.addHandler(handler)

    def _load_config(self, config_path: str) -> dict:
        """Load configuration from YAML file.

        Args:
            config_path: Path to configuration file.

        Returns:
            Configuration dictionary.
        """
        try:
            with open(config_path, "r") as f:
                config = yaml.safe_load(f)
                logger.info(f"Configuration loaded from {config_path}")
                return config or {}
        except FileNotFoundError:
            logger.warning(f"Configuration file not found: {config_path}")
            return {}

    def _build_trie(self) -> None:
        """Build trie from patterns."""
        for pattern in self.patterns:
            current = self.root
            for char in pattern:
                if char not in current.children:
                    current.children[char] = TrieNode()
                current = current.children[char]
            current.is_end = True
            current.output.add(pattern)

        logger.debug(f"Trie built with {len(self.patterns)} patterns")

    def _build_failure_links(self) -> None:
        """Build failure links using BFS."""
        queue = deque()

        for char, child in self.root.children.items():
            child.failure = self.root
            queue.append(child)

        self.root.failure = self.root

        while queue:
            current = queue.popleft()

            for char, child in current.children.items():
                queue.append(child)

                failure = current.failure
                while failure != self.root and char not in failure.children:
                    failure = failure.failure

                if char in failure.children:
                    child.failure = failure.children[char]
                else:
                    child.failure = self.root

        logger.debug("Failure links built")

    def _build_output_links(self) -> None:
        """Build output links by propagating outputs through failure links."""
        queue = deque([self.root])

        while queue:
            current = queue.popleft()

            for char, child in current.children.items():
                queue.append(child)

                if child.failure:
                    child.output.update(child.failure.output)

        logger.debug("Output links built")

    def search(self, text: str) -> Dict[str, List[int]]:
        """Search for all patterns in text.

        Args:
            text: Text to search in.

        Returns:
            Dictionary mapping pattern to list of occurrence positions.
        """
        if not text:
            return {pattern: [] for pattern in self.patterns}

        logger.info(f"Searching for {len(self.patterns)} patterns in text of length {len(text)}")

        results: Dict[str, List[int]] = {pattern: [] for pattern in self.patterns}
        current = self.root

        for i, char in enumerate(text):
            while current != self.root and char not in current.children:
                current = current.failure

            if char in current.children:
                current = current.children[char]
            else:
                current = self.root

            for pattern in current.output:
                start_pos = i - len(pattern) + 1
                results[pattern].append(start_pos)
                logger.debug(f"Pattern '{pattern}' found at position {start_pos}")

        logger.info(f"Search completed, found matches for {sum(len(v) > 0 for v in results.values())} patterns")
        return results

    def count_occurrences(self, text: str) -> Dict[str, int]:
        """Count occurrences of each pattern in text.

        Args:
            text: Text to search in.

        Returns:
            Dictionary mapping pattern to occurrence count.
        """
        results = self.search(text)
        return {pattern: len(positions) for pattern, positions in results.items()}

    def find_all_occurrences(self, text: str) -> List[Tuple[str, int, int]]:
        """Find all occurrences with pattern, position, and length.

        Args:
            text: Text to search in.

        Returns:
            List of (pattern, position, length) tuples.
        """
        results = self.search(text)
        occurrences: List[Tuple[str, int, int]] = []

        for pattern, positions in results.items():
            for pos in positions:
                occurrences.append((pattern, pos, len(pattern)))

        return sorted(occurrences, key=lambda x: x[1])

    def is_pattern_found(self, text: str, pattern: str) -> bool:
        """Check if specific pattern is found in text.

        Args:
            text: Text to search in.
            pattern: Pattern to check.

        Returns:
            True if pattern found, False otherwise.

        Raises:
            ValueError: If pattern not in automaton.
        """
        if pattern not in self.patterns:
            raise ValueError(f"Pattern '{pattern}' not in automaton")

        results = self.search(text)
        return len(results[pattern]) > 0

    def get_patterns(self) -> List[str]:
        """Get list of patterns.

        Returns:
            List of patterns.
        """
        return self.patterns[:]

    def get_pattern_count(self) -> int:
        """Get number of patterns.

        Returns:
            Number of patterns.
        """
        return len(self.patterns)


def main() -> None:
    """Main function to demonstrate Aho-Corasick algorithm operations."""
    patterns = ["he", "she", "his", "hers"]
    logger.info(f"Creating Aho-Corasick automaton for patterns: {patterns}")

    ac = AhoCorasickAlgorithm(patterns)

    logger.info(f"Pattern count: {ac.get_pattern_count()}")
    logger.info(f"Patterns: {ac.get_patterns()}")

    text = "ushers"
    logger.info(f"Searching in text: {text}")

    results = ac.search(text)
    logger.info("Search results:")
    for pattern, positions in results.items():
        logger.info(f"  Pattern '{pattern}': {positions}")

    counts = ac.count_occurrences(text)
    logger.info("Occurrence counts:")
    for pattern, count in counts.items():
        logger.info(f"  Pattern '{pattern}': {count}")

    all_occurrences = ac.find_all_occurrences(text)
    logger.info("All occurrences:")
    for pattern, pos, length in all_occurrences:
        logger.info(f"  Pattern '{pattern}' at position {pos}, length {length}")


if __name__ == "__main__":
    main()
