"""Fenwick Tree (Binary Indexed Tree) for Range Sum Queries.

This module provides functionality to implement Fenwick tree (Binary Indexed Tree)
data structure for efficient range sum queries and point updates. Fenwick trees
support O(log n) point updates and O(log n) range sum queries.
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


class FenwickTree:
    """Fenwick tree (Binary Indexed Tree) for range sum queries."""

    def __init__(
        self, size: Optional[int] = None, array: Optional[List[int]] = None,
        config_path: str = "config.yaml"
    ) -> None:
        """Initialize Fenwick tree.

        Args:
            size: Size of the tree (if creating empty tree).
            array: Initial array values (if constructing from array).
            config_path: Path to configuration YAML file.

        Raises:
            ValueError: If neither size nor array provided, or both provided.
        """
        if size is None and array is None:
            raise ValueError("Either size or array must be provided")
        if size is not None and array is not None:
            raise ValueError("Provide either size or array, not both")

        self._setup_logging()
        self.config = self._load_config(config_path)

        if array is not None:
            self.n = len(array)
            self.original = array[:]
            self.tree = [0] * (self.n + 1)
            self._build_tree(array)
            logger.info(f"Fenwick tree constructed from array of size {self.n}")
        else:
            if size < 1:
                raise ValueError("Size must be at least 1")
            self.n = size
            self.original = [0] * size
            self.tree = [0] * (self.n + 1)
            logger.info(f"Fenwick tree initialized with size {self.n}")

    def _setup_logging(self) -> None:
        """Configure logging for the application."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        log_file = log_dir / "fenwick_tree.log"
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

    def _build_tree(self, array: List[int]) -> None:
        """Build Fenwick tree from array.

        Args:
            array: Input array.
        """
        for i in range(self.n):
            self.update(i, array[i])

    def _lsb(self, index: int) -> int:
        """Get least significant bit of index.

        Args:
            index: Index value.

        Returns:
            Least significant bit value.
        """
        return index & (-index)

    def update(self, index: int, delta: int) -> None:
        """Update element at index by adding delta.

        Args:
            index: Index to update (0-indexed).
            delta: Value to add to element at index.

        Raises:
            ValueError: If index is out of bounds.
        """
        if index < 0 or index >= self.n:
            raise ValueError(f"Index {index} out of bounds [0, {self.n-1}]")

        logger.debug(f"Updating index {index} with delta {delta}")
        self.original[index] += delta
        index += 1

        while index <= self.n:
            self.tree[index] += delta
            index += self._lsb(index)

    def set_value(self, index: int, value: int) -> None:
        """Set element at index to specific value.

        Args:
            index: Index to set (0-indexed).
            value: New value for element at index.

        Raises:
            ValueError: If index is out of bounds.
        """
        if index < 0 or index >= self.n:
            raise ValueError(f"Index {index} out of bounds [0, {self.n-1}]")

        current_value = self.original[index]
        delta = value - current_value
        self.update(index, delta)

    def prefix_sum(self, index: int) -> int:
        """Get prefix sum from index 0 to index (inclusive).

        Args:
            index: End index (0-indexed, inclusive).

        Returns:
            Sum of elements from index 0 to index.

        Raises:
            ValueError: If index is out of bounds.
        """
        if index < 0 or index >= self.n:
            raise ValueError(f"Index {index} out of bounds [0, {self.n-1}]")

        index += 1
        result = 0

        while index > 0:
            result += self.tree[index]
            index -= self._lsb(index)

        logger.debug(f"Prefix sum up to index {index-1}: {result}")
        return result

    def range_sum(self, left: int, right: int) -> int:
        """Get sum of elements from left to right (inclusive).

        Args:
            left: Start index (0-indexed, inclusive).
            right: End index (0-indexed, inclusive).

        Returns:
            Sum of elements from left to right.

        Raises:
            ValueError: If indices are out of bounds or left > right.
        """
        if left < 0 or left >= self.n:
            raise ValueError(f"Left index {left} out of bounds [0, {self.n-1}]")
        if right < 0 or right >= self.n:
            raise ValueError(f"Right index {right} out of bounds [0, {self.n-1}]")
        if left > right:
            raise ValueError(f"Left index {left} must be <= right index {right}")

        if left == 0:
            result = self.prefix_sum(right)
        else:
            result = self.prefix_sum(right) - self.prefix_sum(left - 1)

        logger.debug(f"Range sum [{left}, {right}]: {result}")
        return result

    def get_value(self, index: int) -> int:
        """Get value at specific index.

        Args:
            index: Index to query (0-indexed).

        Returns:
            Value at index.

        Raises:
            ValueError: If index is out of bounds.
        """
        if index < 0 or index >= self.n:
            raise ValueError(f"Index {index} out of bounds [0, {self.n-1}]")
        return self.original[index]

    def get_size(self) -> int:
        """Get size of the tree.

        Returns:
            Number of elements in the tree.
        """
        return self.n

    def get_all_values(self) -> List[int]:
        """Get all values in the tree.

        Returns:
            List of all values.
        """
        return self.original[:]

    def get_tree_array(self) -> List[int]:
        """Get internal tree array (for debugging).

        Returns:
            Internal tree array (1-indexed).
        """
        return self.tree[:]

    def is_valid(self) -> bool:
        """Validate tree structure.

        Returns:
            True if tree is valid, False otherwise.
        """
        if len(self.tree) != self.n + 1:
            logger.error(f"Tree size mismatch: {len(self.tree)} != {self.n + 1}")
            return False

        if len(self.original) != self.n:
            logger.error(
                f"Original array size mismatch: "
                f"{len(self.original)} != {self.n}"
            )
            return False

        for i in range(self.n):
            prefix = self.prefix_sum(i)
            expected = sum(self.original[:i + 1])
            if prefix != expected:
                logger.error(
                    f"Prefix sum mismatch at index {i}: "
                    f"got {prefix}, expected {expected}"
                )
                return False

        return True


def main() -> None:
    """Main function to demonstrate Fenwick tree operations."""
    array = [1, 3, 5, 7, 9, 11]
    logger.info(f"Creating Fenwick tree from array: {array}")

    tree = FenwickTree(array=array)

    logger.info(f"Tree size: {tree.get_size()}")
    logger.info(f"Tree is valid: {tree.is_valid()}")

    logger.info("Prefix sums:")
    for i in range(tree.get_size()):
        prefix = tree.prefix_sum(i)
        logger.info(f"  Prefix sum [0, {i}]: {prefix}")

    logger.info("Range sums:")
    ranges = [(0, 2), (1, 4), (2, 5), (0, 5)]
    for left, right in ranges:
        range_sum = tree.range_sum(left, right)
        logger.info(f"  Range sum [{left}, {right}]: {range_sum}")

    logger.info("Updating index 2 by adding 5:")
    tree.update(2, 5)
    logger.info(f"Value at index 2: {tree.get_value(2)}")
    logger.info(f"Range sum [0, 2]: {tree.range_sum(0, 2)}")

    logger.info("Setting index 3 to 20:")
    tree.set_value(3, 20)
    logger.info(f"Value at index 3: {tree.get_value(3)}")
    logger.info(f"Range sum [0, 3]: {tree.range_sum(0, 3)}")

    logger.info(f"Tree is valid after updates: {tree.is_valid()}")


if __name__ == "__main__":
    main()
