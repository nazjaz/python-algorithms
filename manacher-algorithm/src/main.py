"""Manacher's Algorithm for Finding Longest Palindromic Substring.

This module provides functionality to implement Manacher's algorithm for finding
the longest palindromic substring in a string with O(n) time complexity. The
algorithm uses center expansion and mirroring to efficiently find palindromes.
"""

import logging
import logging.handlers
from pathlib import Path
from typing import List, Optional, Tuple

import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class ManacherAlgorithm:
    """Manacher's algorithm for longest palindromic substring."""

    def __init__(self, text: str, config_path: str = "config.yaml") -> None:
        """Initialize Manacher's algorithm with text.

        Args:
            text: Input string to analyze.
            config_path: Path to configuration YAML file.
        """
        if not text:
            raise ValueError("Text cannot be empty")

        self.text = text
        self.n = len(text)
        self._setup_logging()
        self.config = self._load_config(config_path)

        logger.info(f"Manacher's algorithm initialized for text of length {self.n}")
        self.transformed_text = self._transform_text()
        self.palindrome_radii = self._compute_palindrome_radii()
        self.longest_palindrome = self._find_longest_palindrome()

        logger.info(
            f"Longest palindromic substring found: '{self.longest_palindrome}'"
        )

    def _setup_logging(self) -> None:
        """Configure logging for the application."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        log_file = log_dir / "manacher_algorithm.log"
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

    def _transform_text(self) -> str:
        """Transform text to handle both odd and even length palindromes.

        Inserts separators between characters and at boundaries.

        Returns:
            Transformed string with separators.
        """
        if self.n == 0:
            return "^$"

        transformed = ["^"]
        for char in self.text:
            transformed.append("#")
            transformed.append(char)
        transformed.append("#")
        transformed.append("$")

        result = "".join(transformed)
        logger.debug(f"Transformed text length: {len(result)}")
        return result

    def _compute_palindrome_radii(self) -> List[int]:
        """Compute palindrome radii using Manacher's algorithm.

        Returns:
            List of palindrome radii for each position.
        """
        n = len(self.transformed_text)
        radii = [0] * n
        center = 0
        right = 0

        for i in range(1, n - 1):
            mirror = 2 * center - i

            if i < right:
                radii[i] = min(right - i, radii[mirror])

            while (
                self.transformed_text[i + radii[i] + 1]
                == self.transformed_text[i - radii[i] - 1]
            ):
                radii[i] += 1

            if i + radii[i] > right:
                center = i
                right = i + radii[i]

        logger.debug(f"Computed palindrome radii for {n} positions")
        return radii

    def _find_longest_palindrome(self) -> str:
        """Find longest palindromic substring.

        Returns:
            Longest palindromic substring.
        """
        max_radius = 0
        max_center = 0

        for i in range(len(self.palindrome_radii)):
            if self.palindrome_radii[i] > max_radius:
                max_radius = self.palindrome_radii[i]
                max_center = i

        if max_radius == 0:
            return self.text[0] if self.n > 0 else ""

        start = (max_center - max_radius) // 2
        length = max_radius

        return self.text[start:start + length]

    def get_longest_palindrome(self) -> str:
        """Get longest palindromic substring.

        Returns:
            Longest palindromic substring.
        """
        return self.longest_palindrome

    def get_longest_palindrome_info(self) -> Tuple[str, int, int]:
        """Get longest palindrome with position and length.

        Returns:
            Tuple of (palindrome, start_position, length).
        """
        max_radius = 0
        max_center = 0

        for i in range(len(self.palindrome_radii)):
            if self.palindrome_radii[i] > max_radius:
                max_radius = self.palindrome_radii[i]
                max_center = i

        if max_radius == 0:
            return (self.text[0], 0, 1) if self.n > 0 else ("", 0, 0)

        start = (max_center - max_radius) // 2
        length = max_radius
        palindrome = self.text[start:start + length]

        return (palindrome, start, length)

    def get_all_palindromes(self) -> List[Tuple[str, int, int]]:
        """Get all palindromic substrings with positions and lengths.

        Returns:
            List of (palindrome, start_position, length) tuples.
        """
        palindromes: List[Tuple[str, int, int]] = []

        for i in range(len(self.palindrome_radii)):
            radius = self.palindrome_radii[i]
            if radius > 0:
                start = (i - radius) // 2
                length = radius
                palindrome = self.text[start:start + length]
                palindromes.append((palindrome, start, length))

        return sorted(palindromes, key=lambda x: len(x[0]), reverse=True)

    def count_palindromes(self) -> int:
        """Count total number of palindromic substrings.

        Returns:
            Number of palindromic substrings.
        """
        count = 0
        for radius in self.palindrome_radii:
            if radius > 0:
                count += radius
        return count + self.n

    def is_palindrome_at(self, start: int, length: int) -> bool:
        """Check if substring at position is palindrome.

        Args:
            start: Start position in original text.
            length: Length of substring.

        Returns:
            True if palindrome, False otherwise.

        Raises:
            ValueError: If position or length is invalid.
        """
        if start < 0 or start >= self.n:
            raise ValueError(f"Start position {start} out of range [0, {self.n-1}]")
        if length < 1 or start + length > self.n:
            raise ValueError(f"Invalid length {length} for start {start}")

        substring = self.text[start:start + length]
        return substring == substring[::-1]

    def get_palindrome_radii(self) -> List[int]:
        """Get palindrome radii array.

        Returns:
            Copy of palindrome radii array.
        """
        return self.palindrome_radii[:]

    def get_text(self) -> str:
        """Get original text.

        Returns:
            Original text string.
        """
        return self.text

    def get_length(self) -> int:
        """Get text length.

        Returns:
            Length of text.
        """
        return self.n

    def is_valid(self) -> bool:
        """Validate algorithm results.

        Returns:
            True if valid, False otherwise.
        """
        longest = self.get_longest_palindrome()
        if not longest:
            return True

        if longest != longest[::-1]:
            logger.error(f"Longest palindrome '{longest}' is not a palindrome")
            return False

        info = self.get_longest_palindrome_info()
        if info[0] != longest:
            logger.error("Palindrome mismatch between methods")
            return False

        return True


def main() -> None:
    """Main function to demonstrate Manacher's algorithm operations."""
    texts = ["babad", "cbbd", "racecar", "banana", "a"]

    for text in texts:
        logger.info(f"\nAnalyzing text: {text}")

        manacher = ManacherAlgorithm(text)

        longest = manacher.get_longest_palindrome()
        logger.info(f"Longest palindromic substring: '{longest}'")

        info = manacher.get_longest_palindrome_info()
        logger.info(
            f"Longest palindrome info: '{info[0]}' at position {info[1]}, "
            f"length {info[2]}"
        )

        count = manacher.count_palindromes()
        logger.info(f"Total palindromic substrings: {count}")

        all_palindromes = manacher.get_all_palindromes()
        logger.info(f"All palindromes (top 5): {all_palindromes[:5]}")

        logger.info(f"Algorithm is valid: {manacher.is_valid()}")


if __name__ == "__main__":
    main()
