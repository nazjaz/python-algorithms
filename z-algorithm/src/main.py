"""Z-Algorithm for Pattern Matching with Linear Time Complexity.

This module provides functionality to implement Z-algorithm for pattern matching
with O(n + m) time complexity where n is text length and m is pattern length.
The Z-algorithm supports both single and multiple pattern matching operations.
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


class ZAlgorithm:
    """Z-algorithm for efficient pattern matching."""

    def __init__(self, text: str, config_path: str = "config.yaml") -> None:
        """Initialize Z-algorithm with text.

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
        logger.info(f"Z-algorithm initialized with text of length {self.n}")

    def _setup_logging(self) -> None:
        """Configure logging for the application."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        log_file = log_dir / "z_algorithm.log"
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

    def _compute_z_array(self, string: str) -> List[int]:
        """Compute Z-array for given string.

        Z[i] is the length of the longest substring starting at i that
        matches the prefix of the string.

        Args:
            string: Input string.

        Returns:
            Z-array.
        """
        n = len(string)
        z = [0] * n

        left = 0
        right = 0

        for i in range(1, n):
            if i > right:
                left = right = i
                while right < n and string[right - left] == string[right]:
                    right += 1
                z[i] = right - left
                right -= 1
            else:
                k = i - left
                if z[k] < right - i + 1:
                    z[i] = z[k]
                else:
                    left = i
                    while right < n and string[right - left] == string[right]:
                        right += 1
                    z[i] = right - left
                    right -= 1

        return z

    def search(self, pattern: str) -> List[int]:
        """Search for pattern in text using Z-algorithm.

        Args:
            pattern: Pattern to search for.

        Returns:
            List of starting positions where pattern occurs.

        Raises:
            ValueError: If pattern is empty.
        """
        if not pattern:
            raise ValueError("Pattern cannot be empty")

        logger.info(f"Searching for pattern: {pattern}")

        if len(pattern) > self.n:
            logger.info(f"Pattern '{pattern}' longer than text, not found")
            return []

        combined = pattern + "$" + self.text
        z_array = self._compute_z_array(combined)

        pattern_len = len(pattern)
        occurrences = []

        for i in range(pattern_len + 1, len(z_array)):
            if z_array[i] == pattern_len:
                position = i - pattern_len - 1
                occurrences.append(position)

        logger.info(
            f"Found {len(occurrences)} occurrences of pattern '{pattern}'"
        )
        return occurrences

    def search_all(self, patterns: List[str]) -> Dict[str, List[int]]:
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

        results: Dict[str, List[int]] = {}

        for pattern in patterns:
            if pattern:
                occurrences = self.search(pattern)
                results[pattern] = occurrences
            else:
                logger.warning("Empty pattern skipped")
                results[pattern] = []

        logger.info(f"Completed search for {len(patterns)} patterns")
        return results

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

    def find_all_occurrences(self, pattern: str) -> List[Tuple[int, int]]:
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

    def get_z_array(self, pattern: str) -> List[int]:
        """Get Z-array for pattern concatenated with text.

        Args:
            pattern: Pattern to compute Z-array for.

        Returns:
            Z-array for pattern + separator + text.

        Raises:
            ValueError: If pattern is empty.
        """
        if not pattern:
            raise ValueError("Pattern cannot be empty")

        combined = pattern + "$" + self.text
        z_array = self._compute_z_array(combined)
        return z_array

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

    def get_longest_prefix_match(self, position: int) -> int:
        """Get length of longest prefix match starting at position.

        Args:
            position: Starting position in text.

        Returns:
            Length of longest prefix match.

        Raises:
            ValueError: If position is invalid.
        """
        if position < 0 or position >= self.n:
            raise ValueError(f"Position {position} out of range [0, {self.n-1}]")

        z_array = self._compute_z_array(self.text)
        return z_array[position] if position < len(z_array) else 0

    def find_longest_repeated_substring(self) -> str:
        """Find longest repeated substring using Z-array.

        Returns:
            Longest repeated substring.
        """
        max_length = 0
        max_position = 0

        z_array = self._compute_z_array(self.text)

        for i in range(1, len(z_array)):
            if z_array[i] > max_length:
                max_length = z_array[i]
                max_position = i

        if max_length == 0:
            return ""

        return self.text[max_position:max_position + max_length]

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
    """Main function to demonstrate Z-algorithm operations."""
    text = "banana"
    logger.info(f"Creating Z-algorithm for text: {text}")

    z_algo = ZAlgorithm(text)

    logger.info(f"Text length: {z_algo.get_length()}")

    patterns = ["ana", "nan", "ban", "xyz"]
    logger.info("Searching for single patterns:")
    for pattern in patterns:
        occurrences = z_algo.search(pattern)
        count = z_algo.count_occurrences(pattern)
        is_sub = z_algo.is_substring(pattern)
        logger.info(
            f"  Pattern '{pattern}': "
            f"occurrences={occurrences}, count={count}, found={is_sub}"
        )

    logger.info("Searching for multiple patterns:")
    all_patterns = ["ana", "nan", "ban"]
    results = z_algo.search_all(all_patterns)
    for pattern, occurrences in results.items():
        logger.info(f"  Pattern '{pattern}': {occurrences}")

    logger.info("Finding longest repeated substring:")
    longest = z_algo.find_longest_repeated_substring()
    logger.info(f"  Longest repeated substring: '{longest}'")

    logger.info("Z-array for pattern 'ana':")
    z_array = z_algo.get_z_array("ana")
    logger.info(f"  Z-array: {z_array[:20]}... (showing first 20)")


if __name__ == "__main__":
    main()
