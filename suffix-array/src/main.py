"""Suffix Array Construction with Longest Common Prefix (LCP) Array.

This module provides functionality to construct suffix arrays and compute
longest common prefix (LCP) arrays for efficient string processing. Suffix
arrays enable efficient substring queries and pattern matching.
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


class SuffixArray:
    """Suffix array with LCP array computation."""

    def __init__(self, text: str, config_path: str = "config.yaml") -> None:
        """Initialize suffix array.

        Args:
            text: Input string to build suffix array for.
            config_path: Path to configuration YAML file.
        """
        if not text:
            raise ValueError("Text cannot be empty")

        self.text = text + "$"
        self.n = len(self.text)
        self._setup_logging()
        self.config = self._load_config(config_path)

        logger.info(f"Building suffix array for text of length {len(text)}")
        self.suffix_array = self._build_suffix_array()
        self.inverse_suffix_array = self._build_inverse_suffix_array()
        self.lcp_array = self._build_lcp_array()

        logger.info("Suffix array and LCP array constructed successfully")

    def _setup_logging(self) -> None:
        """Configure logging for the application."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        log_file = log_dir / "suffix_array.log"
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

    def _build_suffix_array(self) -> List[int]:
        """Build suffix array using sorting.

        Returns:
            Suffix array where suffix_array[i] is starting index of
            i-th smallest suffix.
        """
        suffixes = []
        for i in range(self.n):
            suffixes.append((i, self.text[i:]))

        suffixes.sort(key=lambda x: x[1])

        suffix_array = [suffix[0] for suffix in suffixes]
        logger.debug(f"Suffix array built with {len(suffix_array)} entries")
        return suffix_array

    def _build_inverse_suffix_array(self) -> List[int]:
        """Build inverse suffix array.

        Returns:
            Inverse suffix array where inverse_suffix_array[i] is the
            rank of suffix starting at index i.
        """
        inverse = [0] * self.n
        for i in range(self.n):
            inverse[self.suffix_array[i]] = i
        return inverse

    def _build_lcp_array(self) -> List[int]:
        """Build LCP array using Kasai's algorithm.

        Returns:
            LCP array where lcp_array[i] is the longest common prefix
            between suffix_array[i] and suffix_array[i-1].
        """
        lcp = [0] * self.n
        k = 0

        for i in range(self.n):
            if self.inverse_suffix_array[i] == self.n - 1:
                k = 0
                continue

            j = self.suffix_array[self.inverse_suffix_array[i] + 1]

            while (
                i + k < self.n
                and j + k < self.n
                and self.text[i + k] == self.text[j + k]
            ):
                k += 1

            lcp[self.inverse_suffix_array[i]] = k

            if k > 0:
                k -= 1

        logger.debug("LCP array built using Kasai's algorithm")
        return lcp

    def get_suffix_array(self) -> List[int]:
        """Get suffix array.

        Returns:
            Copy of suffix array.
        """
        return self.suffix_array[:]

    def get_lcp_array(self) -> List[int]:
        """Get LCP array.

        Returns:
            Copy of LCP array.
        """
        return self.lcp_array[:]

    def get_inverse_suffix_array(self) -> List[int]:
        """Get inverse suffix array.

        Returns:
            Copy of inverse suffix array.
        """
        return self.inverse_suffix_array[:]

    def get_suffix(self, index: int) -> str:
        """Get suffix at given index in suffix array.

        Args:
            index: Index in suffix array.

        Returns:
            Suffix string.

        Raises:
            ValueError: If index is invalid.
        """
        if index < 0 or index >= len(self.suffix_array):
            raise ValueError(f"Index {index} out of range [0, {len(self.suffix_array)-1}]")

        start = self.suffix_array[index]
        return self.text[start:]

    def get_all_suffixes(self) -> List[str]:
        """Get all suffixes in suffix array order.

        Returns:
            List of all suffixes in sorted order.
        """
        suffixes = []
        for i in range(self.n):
            suffixes.append(self.get_suffix(i))
        return suffixes

    def search(self, pattern: str) -> List[int]:
        """Search for pattern in text using suffix array.

        Args:
            pattern: Pattern to search for.

        Returns:
            List of starting positions where pattern occurs.
        """
        if not pattern:
            return list(range(self.n - 1))

        logger.info(f"Searching for pattern: {pattern}")

        left = self._binary_search_left(pattern)
        right = self._binary_search_right(pattern)

        if left > right:
            logger.info(f"Pattern '{pattern}' not found")
            return []

        occurrences = []
        for i in range(left, right + 1):
            occurrences.append(self.suffix_array[i])

        logger.info(f"Found {len(occurrences)} occurrences of pattern '{pattern}'")
        return sorted(occurrences)

    def _binary_search_left(self, pattern: str) -> int:
        """Binary search for leftmost occurrence of pattern.

        Args:
            pattern: Pattern to search for.

        Returns:
            Leftmost index in suffix array where pattern occurs.
        """
        left = 0
        right = self.n - 1
        result = self.n

        while left <= right:
            mid = (left + right) // 2
            suffix = self.get_suffix(mid)

            if suffix.startswith(pattern):
                result = mid
                right = mid - 1
            elif suffix < pattern:
                left = mid + 1
            else:
                right = mid - 1

        return result

    def _binary_search_right(self, pattern: str) -> int:
        """Binary search for rightmost occurrence of pattern.

        Args:
            pattern: Pattern to search for.

        Returns:
            Rightmost index in suffix array where pattern occurs.
        """
        left = 0
        right = self.n - 1
        result = -1

        while left <= right:
            mid = (left + right) // 2
            suffix = self.get_suffix(mid)

            if suffix.startswith(pattern):
                result = mid
                left = mid + 1
            elif suffix < pattern:
                left = mid + 1
            else:
                right = mid - 1

        return result

    def get_lcp(self, i: int, j: int) -> int:
        """Get longest common prefix between two suffixes.

        Args:
            i: First suffix index in suffix array.
            j: Second suffix index in suffix array.

        Returns:
            Length of longest common prefix.

        Raises:
            ValueError: If indices are invalid.
        """
        if i < 0 or i >= self.n or j < 0 or j >= self.n:
            raise ValueError(f"Indices out of range: i={i}, j={j}")

        if i == j:
            return self.n - self.suffix_array[i]

        if i > j:
            i, j = j, i

        min_lcp = self.lcp_array[i + 1]
        for k in range(i + 2, j + 1):
            min_lcp = min(min_lcp, self.lcp_array[k])

        return min_lcp

    def get_longest_common_substring(self) -> str:
        """Find longest common substring using LCP array.

        Returns:
            Longest common substring.
        """
        if self.n <= 1:
            return ""

        max_lcp = max(self.lcp_array)
        if max_lcp == 0:
            return ""

        max_index = self.lcp_array.index(max_lcp)
        start = self.suffix_array[max_index]
        return self.text[start:start + max_lcp]

    def get_all_longest_common_substrings(self) -> List[str]:
        """Find all longest common substrings.

        Returns:
            List of all longest common substrings.
        """
        if self.n <= 1:
            return []

        max_lcp = max(self.lcp_array)
        if max_lcp == 0:
            return []

        substrings = []
        for i in range(1, self.n):
            if self.lcp_array[i] == max_lcp:
                start = self.suffix_array[i]
                substring = self.text[start:start + max_lcp]
                if substring not in substrings:
                    substrings.append(substring)

        return substrings

    def get_size(self) -> int:
        """Get size of suffix array.

        Returns:
            Number of suffixes.
        """
        return self.n

    def get_text(self) -> str:
        """Get original text (without sentinel).

        Returns:
            Original text string.
        """
        return self.text[:-1]

    def is_valid(self) -> bool:
        """Validate suffix array structure.

        Returns:
            True if valid, False otherwise.
        """
        if len(self.suffix_array) != self.n:
            logger.error(
                f"Suffix array size mismatch: {len(self.suffix_array)} != {self.n}"
            )
            return False

        if len(self.lcp_array) != self.n:
            logger.error(
                f"LCP array size mismatch: {len(self.lcp_array)} != {self.n}"
            )
            return False

        for i in range(self.n - 1):
            suffix_i = self.get_suffix(i)
            suffix_j = self.get_suffix(i + 1)
            if suffix_i >= suffix_j:
                logger.error(
                    f"Suffixes not sorted: {suffix_i} >= {suffix_j}"
                )
                return False

        return True


def main() -> None:
    """Main function to demonstrate suffix array operations."""
    text = "banana"
    logger.info(f"Building suffix array for text: {text}")

    sa = SuffixArray(text)

    logger.info(f"Suffix array size: {sa.get_size()}")
    logger.info(f"Suffix array is valid: {sa.is_valid()}")

    suffix_array = sa.get_suffix_array()
    logger.info(f"Suffix array: {suffix_array}")

    lcp_array = sa.get_lcp_array()
    logger.info(f"LCP array: {lcp_array}")

    logger.info("All suffixes in sorted order:")
    suffixes = sa.get_all_suffixes()
    for i, suffix in enumerate(suffixes):
        logger.info(f"  [{i}] {suffix} (LCP: {lcp_array[i]})")

    logger.info("Searching for patterns:")
    patterns = ["ana", "nan", "ban", "xyz"]
    for pattern in patterns:
        occurrences = sa.search(pattern)
        logger.info(f"  Pattern '{pattern}': {occurrences}")

    longest_common = sa.get_longest_common_substring()
    logger.info(f"Longest common substring: '{longest_common}'")

    all_longest = sa.get_all_longest_common_substrings()
    logger.info(f"All longest common substrings: {all_longest}")


if __name__ == "__main__":
    main()
