"""Rabin-Karp Algorithm for Multiple Pattern Matching with Rolling Hash.

This module provides functionality to implement Rabin-Karp algorithm for pattern
matching using rolling hash with collision handling. The algorithm achieves
O(n + m) average-case time complexity where n is text length and m is pattern
length by using rolling hash to efficiently compute hash values.
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


class RabinKarpAlgorithm:
    """Rabin-Karp algorithm for efficient pattern matching with rolling hash."""

    def __init__(
        self,
        text: str,
        base: int = 256,
        modulus: int = 101,
        config_path: str = "config.yaml",
    ) -> None:
        """Initialize Rabin-Karp algorithm with text.

        Args:
            text: Input text to search in.
            base: Base for hash computation (default: 256).
            modulus: Modulus for hash computation (default: 101).
            config_path: Path to configuration YAML file.
        """
        if not text:
            raise ValueError("Text cannot be empty")
        if base < 2:
            raise ValueError("Base must be at least 2")
        if modulus < 2:
            raise ValueError("Modulus must be at least 2")

        self.text = text
        self.n = len(text)
        self.base = base
        self.modulus = modulus
        self._setup_logging()
        self.config = self._load_config(config_path)

        logger.info(
            f"Rabin-Karp algorithm initialized: text_length={self.n}, "
            f"base={base}, modulus={modulus}"
        )

    def _setup_logging(self) -> None:
        """Configure logging for the application."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        log_file = log_dir / "rabin_karp_algorithm.log"
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

    def _compute_hash(self, string: str, start: int = 0, length: Optional[int] = None) -> int:
        """Compute hash value for substring.

        Args:
            string: Input string.
            start: Start position (default: 0).
            length: Length of substring (default: len(string)).

        Returns:
            Hash value.
        """
        if length is None:
            length = len(string) - start

        hash_value = 0
        for i in range(start, start + length):
            hash_value = (hash_value * self.base + ord(string[i])) % self.modulus

        return hash_value

    def _compute_power(self, exponent: int) -> int:
        """Compute base^exponent mod modulus.

        Args:
            exponent: Exponent value.

        Returns:
            base^exponent mod modulus.
        """
        result = 1
        for _ in range(exponent):
            result = (result * self.base) % self.modulus
        return result

    def search(
        self, pattern: str, verify_collisions: bool = True
    ) -> List[int]:
        """Search for pattern in text using Rabin-Karp algorithm.

        Args:
            pattern: Pattern to search for.
            verify_collisions: Whether to verify hash collisions (default: True).

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

        m = len(pattern)
        pattern_hash = self._compute_hash(pattern)
        occurrences: List[int] = []

        if m == 0:
            return occurrences

        text_hash = self._compute_hash(self.text, 0, m)
        power = self._compute_power(m - 1)

        for i in range(self.n - m + 1):
            if pattern_hash == text_hash:
                if not verify_collisions or self.text[i:i + m] == pattern:
                    occurrences.append(i)
                    logger.debug(f"Pattern found at position {i}")

            if i < self.n - m:
                text_hash = (
                    (text_hash - ord(self.text[i]) * power) * self.base
                    + ord(self.text[i + m])
                ) % self.modulus

                if text_hash < 0:
                    text_hash += self.modulus

        logger.info(
            f"Found {len(occurrences)} occurrences of pattern '{pattern}'"
        )
        return occurrences

    def search_all(
        self,
        patterns: List[str],
        verify_collisions: bool = True,
    ) -> Dict[str, List[int]]:
        """Search for multiple patterns in text.

        Args:
            patterns: List of patterns to search for.
            verify_collisions: Whether to verify hash collisions (default: True).

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
                occurrences = self.search(pattern, verify_collisions)
                results[pattern] = occurrences
            else:
                logger.warning("Empty pattern skipped")
                results[pattern] = []

        logger.info(f"Completed search for {len(patterns)} patterns")
        return results

    def count_occurrences(
        self, pattern: str, verify_collisions: bool = True
    ) -> int:
        """Count occurrences of pattern in text.

        Args:
            pattern: Pattern to count.
            verify_collisions: Whether to verify hash collisions (default: True).

        Returns:
            Number of occurrences.

        Raises:
            ValueError: If pattern is empty.
        """
        occurrences = self.search(pattern, verify_collisions)
        return len(occurrences)

    def find_all_occurrences(
        self, pattern: str, verify_collisions: bool = True
    ) -> List[Tuple[int, int]]:
        """Find all occurrences with their positions and lengths.

        Args:
            pattern: Pattern to search for.
            verify_collisions: Whether to verify hash collisions (default: True).

        Returns:
            List of (position, length) tuples.

        Raises:
            ValueError: If pattern is empty.
        """
        occurrences = self.search(pattern, verify_collisions)
        pattern_len = len(pattern)
        return [(pos, pattern_len) for pos in occurrences]

    def is_substring(
        self, pattern: str, verify_collisions: bool = True
    ) -> bool:
        """Check if pattern is a substring of text.

        Args:
            pattern: Pattern to check.
            verify_collisions: Whether to verify hash collisions (default: True).

        Returns:
            True if pattern found, False otherwise.

        Raises:
            ValueError: If pattern is empty.
        """
        occurrences = self.search(pattern, verify_collisions)
        return len(occurrences) > 0

    def get_hash(self, pattern: str) -> int:
        """Get hash value for pattern.

        Args:
            pattern: Pattern to hash.

        Returns:
            Hash value.

        Raises:
            ValueError: If pattern is empty.
        """
        if not pattern:
            raise ValueError("Pattern cannot be empty")

        return self._compute_hash(pattern)

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

    def get_base(self) -> int:
        """Get hash base.

        Returns:
            Hash base value.
        """
        return self.base

    def get_modulus(self) -> int:
        """Get hash modulus.

        Returns:
            Hash modulus value.
        """
        return self.modulus


def main() -> None:
    """Main function to demonstrate Rabin-Karp algorithm operations."""
    text = "ABABDABACDABABCABCAB"
    logger.info(f"Creating Rabin-Karp algorithm for text: {text}")

    rk = RabinKarpAlgorithm(text, base=256, modulus=101)

    logger.info(f"Text length: {rk.get_length()}")
    logger.info(f"Hash base: {rk.get_base()}, modulus: {rk.get_modulus()}")

    patterns = ["ABABCABCAB", "ABAB", "ABC", "XYZ"]
    logger.info("Searching for patterns with collision verification:")
    for pattern in patterns:
        occurrences = rk.search(pattern, verify_collisions=True)
        count = rk.count_occurrences(pattern, verify_collisions=True)
        is_sub = rk.is_substring(pattern, verify_collisions=True)
        pattern_hash = rk.get_hash(pattern)
        logger.info(
            f"  Pattern '{pattern}': occurrences={occurrences}, "
            f"count={count}, found={is_sub}, hash={pattern_hash}"
        )

    logger.info("Searching for multiple patterns:")
    all_patterns = ["ABAB", "ABC", "AB"]
    results = rk.search_all(all_patterns, verify_collisions=True)
    for pattern, occurrences in results.items():
        logger.info(f"  Pattern '{pattern}': {occurrences}")


if __name__ == "__main__":
    main()
