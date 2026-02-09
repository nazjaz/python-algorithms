"""KMP (Knuth-Morris-Pratt) Algorithm for Pattern Matching.

This module provides functionality to implement KMP algorithm for pattern
matching with failure function optimization. The KMP algorithm achieves
O(n + m) time complexity where n is text length and m is pattern length
by using a failure function to avoid unnecessary character comparisons.
"""

import logging
import logging.handlers
from pathlib import Path
from typing import List, Optional

import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class KMPAlgorithm:
    """KMP algorithm for efficient pattern matching."""

    def __init__(
        self, text: str, config_path: str = "config.yaml"
    ) -> None:
        """Initialize KMP algorithm with text.

        Args:
            text: Input text to search in.
            config_path: Path to configuration YAML file.
        """
        if not text:
            raise ValueError("Text cannot be empty")

        self.text = text
        self.n = len(text)
        self._setup_logging()
        self.config = self._load_config(config_path)
        logger.info(f"KMP algorithm initialized with text of length {self.n}")

    def _setup_logging(self) -> None:
        """Configure logging for the application."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        log_file = log_dir / "kmp_algorithm.log"
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

    def _build_failure_function(self, pattern: str) -> List[int]:
        """Build failure function (LPS array) for pattern.

        LPS[i] is the length of the longest proper prefix which is also
        a suffix for pattern[0..i].

        Args:
            pattern: Pattern to build failure function for.

        Returns:
            Failure function (LPS array).
        """
        m = len(pattern)
        lps = [0] * m
        length = 0
        i = 1

        while i < m:
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1

        logger.debug(f"Failure function built for pattern of length {m}")
        return lps

    def search(self, pattern: str) -> List[int]:
        """Search for pattern in text using KMP algorithm.

        Args:
            pattern: Pattern to search for.

        Returns:
            List of starting positions where pattern occurs.

        Raises:
            ValueError: If pattern is empty.
        """
        if not pattern:
            raise ValueError("Pattern cannot be empty")

        if len(pattern) > self.n:
            logger.info(f"Pattern '{pattern}' longer than text, not found")
            return []

        logger.info(f"Searching for pattern: {pattern}")

        lps = self._build_failure_function(pattern)
        occurrences: List[int] = []

        i = 0
        j = 0
        m = len(pattern)

        while i < self.n:
            if self.text[i] == pattern[j]:
                i += 1
                j += 1

            if j == m:
                occurrences.append(i - j)
                j = lps[j - 1]
            elif i < self.n and self.text[i] != pattern[j]:
                if j != 0:
                    j = lps[j - 1]
                else:
                    i += 1

        logger.info(
            f"Found {len(occurrences)} occurrences of pattern '{pattern}'"
        )
        return occurrences

    def count_occurrences(self, pattern: str) -> int:
        """Count occurrences of pattern in text.

        Args:
            pattern: Pattern to count.

        Returns:
            Number of occurrences.

        Raises:
            ValueError: If pattern is empty.
        """
        occurrences = self.search(pattern)
        return len(occurrences)

    def find_all_occurrences(self, pattern: str) -> List[tuple]:
        """Find all occurrences with their positions and lengths.

        Args:
            pattern: Pattern to search for.

        Returns:
            List of (position, length) tuples.

        Raises:
            ValueError: If pattern is empty.
        """
        occurrences = self.search(pattern)
        pattern_len = len(pattern)
        return [(pos, pattern_len) for pos in occurrences]

    def is_substring(self, pattern: str) -> bool:
        """Check if pattern is a substring of text.

        Args:
            pattern: Pattern to check.

        Returns:
            True if pattern found, False otherwise.

        Raises:
            ValueError: If pattern is empty.
        """
        occurrences = self.search(pattern)
        return len(occurrences) > 0

    def get_failure_function(self, pattern: str) -> List[int]:
        """Get failure function (LPS array) for pattern.

        Args:
            pattern: Pattern to get failure function for.

        Returns:
            Failure function (LPS array).

        Raises:
            ValueError: If pattern is empty.
        """
        if not pattern:
            raise ValueError("Pattern cannot be empty")

        return self._build_failure_function(pattern)

    def search_all(self, patterns: List[str]) -> dict:
        """Search for multiple patterns in text.

        Args:
            patterns: List of patterns to search for.

        Returns:
            Dictionary mapping pattern to list of occurrences.

        Raises:
            ValueError: If patterns list is empty.
        """
        if not patterns:
            raise ValueError("Patterns list cannot be empty")

        logger.info(f"Searching for {len(patterns)} patterns")

        results: dict = {}

        for pattern in patterns:
            if pattern:
                occurrences = self.search(pattern)
                results[pattern] = occurrences
            else:
                logger.warning("Empty pattern skipped")
                results[pattern] = []

        logger.info(f"Completed search for {len(patterns)} patterns")
        return results

    def get_text(self) -> str:
        """Get text string.

        Returns:
            Text string.
        """
        return self.text

    def get_length(self) -> int:
        """Get text length.

        Returns:
            Length of text.
        """
        return self.n


def main() -> None:
    """Main function to demonstrate KMP algorithm operations."""
    text = "ABABDABACDABABCABCAB"
    logger.info(f"Creating KMP algorithm for text: {text}")

    kmp = KMPAlgorithm(text)

    logger.info(f"Text length: {kmp.get_length()}")

    patterns = ["ABABCABCAB", "ABAB", "ABC", "XYZ"]
    logger.info("Searching for patterns:")
    for pattern in patterns:
        occurrences = kmp.search(pattern)
        count = kmp.count_occurrences(pattern)
        is_sub = kmp.is_substring(pattern)
        logger.info(
            f"  Pattern '{pattern}': "
            f"occurrences={occurrences}, count={count}, found={is_sub}"
        )

        lps = kmp.get_failure_function(pattern)
        logger.info(f"    Failure function: {lps}")

    logger.info("Searching for multiple patterns:")
    all_patterns = ["ABAB", "ABC", "AB"]
    results = kmp.search_all(all_patterns)
    for pattern, occurrences in results.items():
        logger.info(f"  Pattern '{pattern}': {occurrences}")


if __name__ == "__main__":
    main()
