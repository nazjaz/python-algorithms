"""Persistent Segment Tree for Range Queries Across Multiple Versions.

This module provides functionality to implement persistent segment tree data
structure that supports range queries across multiple versions of an array.
Each update creates a new version while preserving all previous versions.
"""

import logging
import logging.handlers
import sys
from copy import deepcopy
from pathlib import Path
from typing import List, Optional, Tuple

import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class SegmentTreeNode:
    """Node in persistent segment tree."""

    def __init__(
        self,
        left: Optional["SegmentTreeNode"] = None,
        right: Optional["SegmentTreeNode"] = None,
        value: int = 0,
    ) -> None:
        """Initialize SegmentTreeNode.

        Args:
            left: Left child node.
            right: Right child node.
            value: Node value (sum/min/max depending on operation).
        """
        self.left = left
        self.right = right
        self.value = value

    def __repr__(self) -> str:
        """String representation."""
        return f"SegmentTreeNode(value={self.value})"

    def copy(self) -> "SegmentTreeNode":
        """Create a copy of this node.

        Returns:
            Copy of the node.
        """
        return SegmentTreeNode(
            left=self.left, right=self.right, value=self.value
        )


class PersistentSegmentTree:
    """Persistent segment tree for range queries across versions."""

    def __init__(
        self, array: List[int], config_path: str = "config.yaml"
    ) -> None:
        """Initialize persistent segment tree.

        Args:
            array: Initial array values.
            config_path: Path to configuration YAML file.
        """
        if not array:
            raise ValueError("Array cannot be empty")

        self.n = len(array)
        self._setup_logging()
        self.config = self._load_config(config_path)
        self.versions: List[Optional[SegmentTreeNode]] = []
        self.version_count = 0

        root = self._build_tree(0, self.n - 1, array)
        self.versions.append(root)
        self.version_count = 1

        logger.info(
            f"Persistent segment tree initialized with {self.n} elements, "
            f"version 0 created"
        )

    def _setup_logging(self) -> None:
        """Configure logging for the application."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        log_file = log_dir / "persistent_segment_tree.log"
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

    def _build_tree(
        self, start: int, end: int, array: List[int]
    ) -> SegmentTreeNode:
        """Build initial segment tree.

        Args:
            start: Start index of segment.
            end: End index of segment.
            array: Input array.

        Returns:
            Root node of segment tree.
        """
        if start == end:
            return SegmentTreeNode(value=array[start])

        mid = (start + end) // 2
        left = self._build_tree(start, mid, array)
        right = self._build_tree(mid + 1, end, array)

        return SegmentTreeNode(
            left=left, right=right, value=left.value + right.value
        )

    def _update_node(
        self,
        node: SegmentTreeNode,
        start: int,
        end: int,
        index: int,
        value: int,
    ) -> SegmentTreeNode:
        """Update node and create new version.

        Args:
            node: Current node.
            start: Start index of segment.
            end: End index of segment.
            index: Index to update.
            value: New value.

        Returns:
            New node with update applied.
        """
        if start == end:
            new_node = SegmentTreeNode(value=value)
            return new_node

        mid = (start + end) // 2
        new_node = node.copy()

        if index <= mid:
            new_node.left = self._update_node(
                node.left, start, mid, index, value
            )
        else:
            new_node.right = self._update_node(
                node.right, mid + 1, end, index, value
            )

        new_node.value = new_node.left.value + new_node.right.value
        return new_node

    def update(self, version: int, index: int, value: int) -> int:
        """Update element at index in specified version, creating new version.

        Args:
            version: Version to update from.
            index: Index to update (0-indexed).
            value: New value.

        Returns:
            New version number.

        Raises:
            ValueError: If version or index is invalid.
        """
        if version < 0 or version >= self.version_count:
            raise ValueError(
                f"Version {version} out of range [0, {self.version_count-1}]"
            )
        if index < 0 or index >= self.n:
            raise ValueError(f"Index {index} out of range [0, {self.n-1}]")

        logger.info(
            f"Updating version {version}, index {index} to value {value}"
        )

        old_root = self.versions[version]
        new_root = self._update_node(old_root, 0, self.n - 1, index, value)
        self.versions.append(new_root)
        self.version_count += 1

        logger.info(f"New version {self.version_count - 1} created")
        return self.version_count - 1

    def _query_sum(
        self,
        node: SegmentTreeNode,
        start: int,
        end: int,
        left: int,
        right: int,
    ) -> int:
        """Query sum in range [left, right].

        Args:
            node: Current node.
            start: Start index of segment.
            end: End index of segment.
            left: Query start index.
            right: Query end index.

        Returns:
            Sum in range.
        """
        if right < start or left > end:
            return 0

        if left <= start and end <= right:
            return node.value

        mid = (start + end) // 2
        left_sum = self._query_sum(node.left, start, mid, left, right)
        right_sum = self._query_sum(node.right, mid + 1, end, left, right)

        return left_sum + right_sum

    def query_sum(self, version: int, left: int, right: int) -> int:
        """Query sum in range [left, right] for specified version.

        Args:
            version: Version to query.
            left: Start index (0-indexed, inclusive).
            right: End index (0-indexed, inclusive).

        Returns:
            Sum of elements in range.

        Raises:
            ValueError: If version or indices are invalid.
        """
        if version < 0 or version >= self.version_count:
            raise ValueError(
                f"Version {version} out of range [0, {self.version_count-1}]"
            )
        if left < 0 or left >= self.n:
            raise ValueError(f"Left index {left} out of range [0, {self.n-1}]")
        if right < 0 or right >= self.n:
            raise ValueError(
                f"Right index {right} out of range [0, {self.n-1}]"
            )
        if left > right:
            raise ValueError(f"Left index {left} must be <= right index {right}")

        logger.debug(f"Querying sum in version {version}, range [{left}, {right}]")

        root = self.versions[version]
        result = self._query_sum(root, 0, self.n - 1, left, right)
        logger.debug(f"Sum: {result}")
        return result

    def _query_min(
        self,
        node: SegmentTreeNode,
        start: int,
        end: int,
        left: int,
        right: int,
    ) -> int:
        """Query minimum in range [left, right].

        Args:
            node: Current node.
            start: Start index of segment.
            end: End index of segment.
            left: Query start index.
            right: Query end index.

        Returns:
            Minimum value in range.
        """
        if right < start or left > end:
            return sys.maxsize

        if start == end:
            return node.value

        mid = (start + end) // 2
        left_min = self._query_min(node.left, start, mid, left, right)
        right_min = self._query_min(node.right, mid + 1, end, left, right)

        return min(left_min, right_min)

    def query_min(self, version: int, left: int, right: int) -> int:
        """Query minimum in range [left, right] for specified version.

        Args:
            version: Version to query.
            left: Start index (0-indexed, inclusive).
            right: End index (0-indexed, inclusive).

        Returns:
            Minimum value in range.

        Raises:
            ValueError: If version or indices are invalid.
        """
        if version < 0 or version >= self.version_count:
            raise ValueError(
                f"Version {version} out of range [0, {self.version_count-1}]"
            )
        if left < 0 or left >= self.n:
            raise ValueError(f"Left index {left} out of range [0, {self.n-1}]")
        if right < 0 or right >= self.n:
            raise ValueError(
                f"Right index {right} out of range [0, {self.n-1}]"
            )
        if left > right:
            raise ValueError(f"Left index {left} must be <= right index {right}")

        logger.debug(
            f"Querying min in version {version}, range [{left}, {right}]"
        )

        root = self.versions[version]
        result = self._query_min(root, 0, self.n - 1, left, right)
        logger.debug(f"Min: {result}")
        return result

    def _query_max(
        self,
        node: SegmentTreeNode,
        start: int,
        end: int,
        left: int,
        right: int,
    ) -> int:
        """Query maximum in range [left, right].

        Args:
            node: Current node.
            start: Start index of segment.
            end: End index of segment.
            left: Query start index.
            right: Query end index.

        Returns:
            Maximum value in range.
        """
        if right < start or left > end:
            return -sys.maxsize

        if start == end:
            return node.value

        mid = (start + end) // 2
        left_max = self._query_max(node.left, start, mid, left, right)
        right_max = self._query_max(node.right, mid + 1, end, left, right)

        return max(left_max, right_max)

    def query_max(self, version: int, left: int, right: int) -> int:
        """Query maximum in range [left, right] for specified version.

        Args:
            version: Version to query.
            left: Start index (0-indexed, inclusive).
            right: End index (0-indexed, inclusive).

        Returns:
            Maximum value in range.

        Raises:
            ValueError: If version or indices are invalid.
        """
        if version < 0 or version >= self.version_count:
            raise ValueError(
                f"Version {version} out of range [0, {self.version_count-1}]"
            )
        if left < 0 or left >= self.n:
            raise ValueError(f"Left index {left} out of range [0, {self.n-1}]")
        if right < 0 or right >= self.n:
            raise ValueError(
                f"Right index {right} out of range [0, {self.n-1}]"
            )
        if left > right:
            raise ValueError(f"Left index {left} must be <= right index {right}")

        logger.debug(
            f"Querying max in version {version}, range [{left}, {right}]"
        )

        root = self.versions[version]
        result = self._query_max(root, 0, self.n - 1, left, right)
        logger.debug(f"Max: {result}")
        return result

    def get_version_count(self) -> int:
        """Get number of versions.

        Returns:
            Number of versions.
        """
        return self.version_count

    def get_size(self) -> int:
        """Get size of array.

        Returns:
            Number of elements.
        """
        return self.n

    def _reconstruct_array(
        self, node: SegmentTreeNode, start: int, end: int, array: List[int]
    ) -> None:
        """Reconstruct array from tree node.

        Args:
            node: Current node.
            start: Start index of segment.
            end: End index of segment.
            array: Array to fill.
        """
        if start == end:
            array[start] = node.value
            return

        mid = (start + end) // 2
        self._reconstruct_array(node.left, start, mid, array)
        self._reconstruct_array(node.right, mid + 1, end, array)

    def get_version_array(self, version: int) -> List[int]:
        """Get array representation of specified version.

        Args:
            version: Version to reconstruct.

        Returns:
            Array values for specified version.

        Raises:
            ValueError: If version is invalid.
        """
        if version < 0 or version >= self.version_count:
            raise ValueError(
                f"Version {version} out of range [0, {self.version_count-1}]"
            )

        array = [0] * self.n
        root = self.versions[version]
        self._reconstruct_array(root, 0, self.n - 1, array)
        return array


def main() -> None:
    """Main function to demonstrate persistent segment tree operations."""
    array = [1, 3, 5, 7, 9, 11]
    logger.info(f"Creating persistent segment tree from array: {array}")

    tree = PersistentSegmentTree(array)

    logger.info(f"Tree size: {tree.get_size()}")
    logger.info(f"Initial version count: {tree.get_version_count()}")

    logger.info("Querying version 0:")
    sum_0_2 = tree.query_sum(0, 0, 2)
    logger.info(f"Sum [0, 2] in version 0: {sum_0_2}")

    min_0_5 = tree.query_min(0, 0, 5)
    logger.info(f"Min [0, 5] in version 0: {min_0_5}")

    max_0_5 = tree.query_max(0, 0, 5)
    logger.info(f"Max [0, 5] in version 0: {max_0_5}")

    logger.info("Creating version 1 by updating index 2 to 10:")
    version_1 = tree.update(0, 2, 10)
    logger.info(f"Version 1 created: {version_1}")

    logger.info("Querying version 1:")
    sum_0_2_v1 = tree.query_sum(1, 0, 2)
    logger.info(f"Sum [0, 2] in version 1: {sum_0_2_v1}")

    logger.info("Querying version 0 (should be unchanged):")
    sum_0_2_v0 = tree.query_sum(0, 0, 2)
    logger.info(f"Sum [0, 2] in version 0: {sum_0_2_v0}")

    logger.info("Creating version 2 by updating index 4 to 20:")
    version_2 = tree.update(1, 4, 20)
    logger.info(f"Version 2 created: {version_2}")

    logger.info("Querying all versions:")
    for v in range(tree.get_version_count()):
        arr = tree.get_version_array(v)
        total = tree.query_sum(v, 0, tree.get_size() - 1)
        logger.info(f"Version {v}: {arr}, total sum: {total}")


if __name__ == "__main__":
    main()
