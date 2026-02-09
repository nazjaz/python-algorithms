"""Wavelet Tree for Range Queries and Rank/Select Operations on Sequences.

This module provides functionality to implement wavelet tree data structure
that efficiently supports range queries, rank, and select operations on
sequences. Wavelet trees achieve O(log σ) time complexity for queries where
σ is the alphabet size.
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


class BitVector:
    """Bit vector with rank and select support."""

    def __init__(self, bits: List[bool]) -> None:
        """Initialize bit vector.

        Args:
            bits: List of boolean values.
        """
        self.bits = bits
        self.n = len(bits)
        self._build_rank_table()

    def _build_rank_table(self) -> None:
        """Build rank table for fast rank queries."""
        self.rank_table: List[int] = [0] * (self.n + 1)
        for i in range(self.n):
            self.rank_table[i + 1] = self.rank_table[i] + (1 if self.bits[i] else 0)

    def rank(self, pos: int, bit: bool) -> int:
        """Compute rank of bit up to position.

        Args:
            pos: Position (0-indexed, inclusive).
            bit: Bit value to rank.

        Returns:
            Number of occurrences of bit up to position.
        """
        if pos < 0:
            return 0
        if pos >= self.n:
            pos = self.n - 1

        if bit:
            return self.rank_table[pos + 1]
        return (pos + 1) - self.rank_table[pos + 1]

    def select(self, k: int, bit: bool) -> Optional[int]:
        """Find position of k-th occurrence of bit.

        Args:
            k: Occurrence number (1-indexed).
            bit: Bit value to select.

        Returns:
            Position of k-th occurrence or None if not found.
        """
        if k <= 0:
            return None

        if bit:
            if k > self.rank_table[self.n]:
                return None
            for i in range(self.n):
                if self.rank_table[i + 1] == k:
                    return i
        else:
            total_zeros = self.n - self.rank_table[self.n]
            if k > total_zeros:
                return None
            for i in range(self.n):
                zeros = (i + 1) - self.rank_table[i + 1]
                if zeros == k:
                    return i

        return None

    def access(self, pos: int) -> bool:
        """Access bit at position.

        Args:
            pos: Position.

        Returns:
            Bit value at position.
        """
        if 0 <= pos < self.n:
            return self.bits[pos]
        return False


class WaveletNode:
    """Node in wavelet tree."""

    def __init__(
        self,
        sequence: List[int],
        alphabet_min: int,
        alphabet_max: int,
        level: int = 0,
    ) -> None:
        """Initialize wavelet node.

        Args:
            sequence: Sequence of integers.
            alphabet_min: Minimum value in alphabet.
            alphabet_max: Maximum value in alphabet.
            level: Current level in tree.
        """
        self.sequence = sequence
        self.alphabet_min = alphabet_min
        self.alphabet_max = alphabet_max
        self.level = level
        self.bitvector: Optional[BitVector] = None
        self.left: Optional["WaveletNode"] = None
        self.right: Optional["WaveletNode"] = None
        self._build()

    def _build(self) -> None:
        """Build wavelet node."""
        if self.alphabet_min == self.alphabet_max:
            return

        mid = (self.alphabet_min + self.alphabet_max) // 2
        bits: List[bool] = []

        for value in self.sequence:
            bits.append(value > mid)

        self.bitvector = BitVector(bits)

        left_sequence: List[int] = []
        right_sequence: List[int] = []

        for value in self.sequence:
            if value <= mid:
                left_sequence.append(value)
            else:
                right_sequence.append(value)

        if left_sequence:
            self.left = WaveletNode(
                left_sequence, self.alphabet_min, mid, self.level + 1
            )

        if right_sequence:
            self.right = WaveletNode(
                right_sequence, mid + 1, self.alphabet_max, self.level + 1
            )


class WaveletTree:
    """Wavelet tree for range queries and rank/select operations."""

    def __init__(
        self, sequence: List[int], config_path: str = "config.yaml"
    ) -> None:
        """Initialize wavelet tree.

        Args:
            sequence: Sequence of integers.
            config_path: Path to configuration file.
        """
        if not sequence:
            raise ValueError("Sequence cannot be empty")

        self.sequence = sequence
        self.n = len(sequence)
        self.alphabet_min = min(sequence)
        self.alphabet_max = max(sequence)
        self._setup_logging()
        self._load_config(config_path)
        self.root = WaveletNode(sequence, self.alphabet_min, self.alphabet_max)
        logger.info(
            f"Built wavelet tree for sequence of length {self.n}, "
            f"alphabet [{self.alphabet_min}, {self.alphabet_max}]"
        )

    def _setup_logging(self) -> None:
        """Configure logging for wavelet tree operations."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        handler = logging.handlers.RotatingFileHandler(
            log_dir / "wavelet_tree.log",
            maxBytes=10485760,
            backupCount=5,
        )
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    def _load_config(self, config_path: str) -> None:
        """Load configuration from YAML file.

        Args:
            config_path: Path to configuration file.
        """
        try:
            config_file = Path(config_path)
            if config_file.exists():
                with open(config_file, "r") as f:
                    config = yaml.safe_load(f)
                    if config and "logging" in config:
                        log_level = config["logging"].get("level", "INFO")
                        logger.setLevel(getattr(logging, log_level))
        except Exception as e:
            logger.warning(f"Could not load config: {e}")

    def _rank_recursive(
        self, node: Optional[WaveletNode], pos: int, value: int
    ) -> int:
        """Recursively compute rank.

        Args:
            node: Current node.
            pos: Position in current node's sequence.
            value: Value to rank.

        Returns:
            Rank of value up to position.
        """
        if node is None:
            return 0

        if node.alphabet_min == node.alphabet_max:
            if value == node.alphabet_min and pos >= 0:
                count = 0
                for i in range(min(pos + 1, len(node.sequence))):
                    if node.sequence[i] == value:
                        count += 1
                return count
            return 0

        if node.bitvector is None:
            return 0

        mid = (node.alphabet_min + node.alphabet_max) // 2

        if value <= mid:
            zeros = node.bitvector.rank(pos, False)
            if node.left:
                return self._rank_recursive(node.left, zeros - 1, value)
            return 0
        else:
            ones = node.bitvector.rank(pos, True)
            if node.right:
                return self._rank_recursive(node.right, ones - 1, value)
            return 0

    def rank(self, pos: int, value: int) -> int:
        """Compute rank of value up to position.

        Args:
            pos: Position in sequence (0-indexed, inclusive).
            value: Value to rank.

        Returns:
            Number of occurrences of value up to position.

        Raises:
            ValueError: If position is out of bounds.
        """
        if pos < 0 or pos >= self.n:
            raise ValueError(f"Position {pos} out of bounds [0, {self.n-1}]")

        if value < self.alphabet_min or value > self.alphabet_max:
            return 0

        result = self._rank_recursive(self.root, pos, value)
        logger.info(f"Rank of {value} up to position {pos}: {result}")
        return result

    def _select_recursive(
        self, node: Optional[WaveletNode], k: int, value: int
    ) -> Optional[int]:
        """Recursively compute select.

        Args:
            node: Current node.
            k: Occurrence number (1-indexed) in current node's sequence.
            value: Value to select.

        Returns:
            Position in current node's sequence or None.
        """
        if node is None:
            return None

        if node.alphabet_min == node.alphabet_max:
            if value == node.alphabet_min and node.sequence:
                count = 0
                for i, v in enumerate(node.sequence):
                    if v == value:
                        count += 1
                        if count == k:
                            return i
            return None

        if node.bitvector is None:
            return None

        mid = (node.alphabet_min + node.alphabet_max) // 2

        if value <= mid:
            pos_in_left = self._select_recursive(node.left, k, value)
            if pos_in_left is None:
                return None

            return node.bitvector.select(pos_in_left + 1, False)
        else:
            pos_in_right = self._select_recursive(node.right, k, value)
            if pos_in_right is None:
                return None

            return node.bitvector.select(pos_in_right + 1, True)

    def select(self, k: int, value: int) -> Optional[int]:
        """Find position of k-th occurrence of value.

        Args:
            k: Occurrence number (1-indexed).
            value: Value to select.

        Returns:
            Position of k-th occurrence or None if not found.

        Raises:
            ValueError: If k <= 0.
        """
        if k <= 0:
            raise ValueError("k must be positive")

        if value < self.alphabet_min or value > self.alphabet_max:
            return None

        result = self._select_recursive(self.root, k, value)
        if result is not None:
            logger.info(f"Select {k}-th occurrence of {value}: position {result}")
        else:
            logger.info(f"Select {k}-th occurrence of {value}: not found")
        return result

    def _range_count_recursive(
        self, node: Optional[WaveletNode], left: int, right: int, min_val: int, max_val: int
    ) -> int:
        """Recursively count elements in range.

        Args:
            node: Current node.
            left: Left position in current node's sequence.
            right: Right position in current node's sequence.
            min_val: Minimum value in range.
            max_val: Maximum value in range.

        Returns:
            Count of elements in range.
        """
        if node is None or left > right:
            return 0

        if node.alphabet_min == node.alphabet_max:
            if min_val <= node.alphabet_min <= max_val:
                count = 0
                for i in range(max(0, left), min(right + 1, len(node.sequence))):
                    if node.sequence[i] == node.alphabet_min:
                        count += 1
                return count
            return 0

        if node.bitvector is None:
            return 0

        mid = (node.alphabet_min + node.alphabet_max) // 2

        if max_val <= mid:
            left_zeros = node.bitvector.rank(left - 1, False) if left > 0 else 0
            right_zeros = node.bitvector.rank(right, False)
            if right_zeros > left_zeros:
                return self._range_count_recursive(
                    node.left, left_zeros, right_zeros - 1, min_val, max_val
                )
            return 0
        elif min_val > mid:
            left_ones = node.bitvector.rank(left - 1, True) if left > 0 else 0
            right_ones = node.bitvector.rank(right, True)
            if right_ones > left_ones:
                return self._range_count_recursive(
                    node.right, left_ones, right_ones - 1, min_val, max_val
                )
            return 0
        else:
            left_zeros = node.bitvector.rank(left - 1, False) if left > 0 else 0
            right_zeros = node.bitvector.rank(right, False)
            count_left = 0
            if right_zeros > left_zeros and node.left:
                count_left = self._range_count_recursive(
                    node.left, left_zeros, right_zeros - 1, min_val, mid
                )

            left_ones = node.bitvector.rank(left - 1, True) if left > 0 else 0
            right_ones = node.bitvector.rank(right, True)
            count_right = 0
            if right_ones > left_ones and node.right:
                count_right = self._range_count_recursive(
                    node.right, left_ones, right_ones - 1, mid + 1, max_val
                )

            return count_left + count_right

    def range_count(self, left: int, right: int, min_val: int, max_val: int) -> int:
        """Count elements in range [left, right] with values in [min_val, max_val].

        Args:
            left: Left position (0-indexed, inclusive).
            right: Right position (0-indexed, inclusive).
            min_val: Minimum value.
            max_val: Maximum value.

        Returns:
            Count of elements in range.

        Raises:
            ValueError: If positions are invalid.
        """
        if left < 0 or right >= self.n or left > right:
            raise ValueError(f"Invalid range [{left}, {right}]")

        if min_val > max_val:
            return 0

        result = self._range_count_recursive(
            self.root, left, right, min_val, max_val
        )
        logger.info(
            f"Range count [{left}, {right}] with values [{min_val}, {max_val}]: {result}"
        )
        return result

    def access(self, pos: int) -> int:
        """Access element at position.

        Args:
            pos: Position in sequence.

        Returns:
            Element at position.

        Raises:
            ValueError: If position is out of bounds.
        """
        if pos < 0 or pos >= self.n:
            raise ValueError(f"Position {pos} out of bounds [0, {self.n-1}]")

        return self.sequence[pos]

    def get_sequence(self) -> List[int]:
        """Get original sequence.

        Returns:
            Original sequence.
        """
        return self.sequence[:]


def main() -> None:
    """Main function to demonstrate wavelet tree operations."""
    sequence = [1, 2, 3, 1, 2, 3, 1, 2, 3, 4, 5]
    tree = WaveletTree(sequence)

    print("Wavelet Tree Operations Demo")
    print("=" * 50)

    print(f"\nSequence: {sequence}")
    print(f"Alphabet: [{tree.alphabet_min}, {tree.alphabet_max}]")

    print("\nRank operations:")
    for value in [1, 2, 3]:
        rank = tree.rank(5, value)
        print(f"Rank of {value} up to position 5: {rank}")

    print("\nSelect operations:")
    for value in [1, 2, 3]:
        for k in [1, 2, 3]:
            pos = tree.select(k, value)
            if pos is not None:
                print(f"Select {k}-th occurrence of {value}: position {pos}")

    print("\nRange count operations:")
    count = tree.range_count(0, 5, 1, 2)
    print(f"Count of values [1, 2] in positions [0, 5]: {count}")

    count = tree.range_count(0, 10, 3, 5)
    print(f"Count of values [3, 5] in positions [0, 10]: {count}")


if __name__ == "__main__":
    main()
