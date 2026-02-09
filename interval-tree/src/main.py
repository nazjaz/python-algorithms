"""Interval Tree for Efficient Range Overlap Queries and Interval Management.

This module provides functionality to implement interval tree data structure
that efficiently stores intervals and supports range overlap queries. Interval
trees use binary search tree structure with max endpoint tracking to achieve
O(log n) time complexity for queries.
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


class Interval:
    """Represents an interval [low, high]."""

    def __init__(self, low: int, high: int) -> None:
        """Initialize interval.

        Args:
            low: Lower endpoint of interval.
            high: Upper endpoint of interval.

        Raises:
            ValueError: If low > high.
        """
        if low > high:
            raise ValueError(f"Invalid interval: low ({low}) > high ({high})")
        self.low = low
        self.high = high

    def overlaps(self, other: "Interval") -> bool:
        """Check if this interval overlaps with another interval.

        Args:
            other: Other interval to check.

        Returns:
            True if intervals overlap, False otherwise.
        """
        return self.low <= other.high and other.low <= self.high

    def overlaps_point(self, point: int) -> bool:
        """Check if this interval contains a point.

        Args:
            point: Point to check.

        Returns:
            True if point is in interval, False otherwise.
        """
        return self.low <= point <= self.high

    def __repr__(self) -> str:
        """String representation."""
        return f"Interval({self.low}, {self.high})"

    def __eq__(self, other: object) -> bool:
        """Check equality."""
        if not isinstance(other, Interval):
            return False
        return self.low == other.low and self.high == other.high


class IntervalNode:
    """Node in interval tree."""

    def __init__(self, interval: Interval) -> None:
        """Initialize IntervalNode.

        Args:
            interval: Interval stored in this node.
        """
        self.interval = interval
        self.max_endpoint = interval.high
        self.left: Optional["IntervalNode"] = None
        self.right: Optional["IntervalNode"] = None

    def update_max_endpoint(self) -> None:
        """Update max endpoint based on subtree."""
        self.max_endpoint = self.interval.high
        if self.left:
            self.max_endpoint = max(self.max_endpoint, self.left.max_endpoint)
        if self.right:
            self.max_endpoint = max(self.max_endpoint, self.right.max_endpoint)

    def __repr__(self) -> str:
        """String representation."""
        return f"IntervalNode({self.interval}, max={self.max_endpoint})"


class IntervalTree:
    """Interval tree for efficient range overlap queries."""

    def __init__(self, config_path: str = "config.yaml") -> None:
        """Initialize interval tree.

        Args:
            config_path: Path to configuration file.
        """
        self.root: Optional[IntervalNode] = None
        self.size = 0
        self._setup_logging()
        self._load_config(config_path)

    def _setup_logging(self) -> None:
        """Configure logging for interval tree operations."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        handler = logging.handlers.RotatingFileHandler(
            log_dir / "interval_tree.log",
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

    def _search_interval(
        self, node: Optional[IntervalNode], interval: Interval
    ) -> bool:
        """Search for interval in tree.

        Args:
            node: Current node in recursion.
            interval: Interval to search for.

        Returns:
            True if interval exists, False otherwise.
        """
        if node is None:
            return False

        if interval == node.interval:
            return True

        if interval.low < node.interval.low:
            return self._search_interval(node.left, interval)
        else:
            return self._search_interval(node.right, interval)

    def _insert_node(
        self, node: Optional[IntervalNode], interval: Interval
    ) -> IntervalNode:
        """Recursively insert interval into tree.

        Args:
            node: Current node in recursion.
            interval: Interval to insert.

        Returns:
            Root of subtree after insertion.
        """
        if node is None:
            new_node = IntervalNode(interval)
            logger.debug(f"Inserted interval: {interval}")
            return new_node

        if interval.low < node.interval.low:
            node.left = self._insert_node(node.left, interval)
        elif interval.low > node.interval.low:
            node.right = self._insert_node(node.right, interval)
        else:
            if interval.high < node.interval.high:
                node.left = self._insert_node(node.left, interval)
            elif interval.high > node.interval.high:
                node.right = self._insert_node(node.right, interval)
            else:
                logger.info(f"Interval {interval} already exists")
                return node

        node.update_max_endpoint()
        return node

    def insert(self, low: int, high: int) -> bool:
        """Insert interval into tree.

        Args:
            low: Lower endpoint of interval.
            high: Upper endpoint of interval.

        Returns:
            True if inserted, False if already exists.

        Raises:
            ValueError: If low > high.
        """
        try:
            interval = Interval(low, high)
        except ValueError as e:
            logger.error(f"Invalid interval: {e}")
            raise

        if self._search_interval(self.root, interval):
            logger.info(f"Interval {interval} already exists")
            return False

        self.root = self._insert_node(self.root, interval)
        self.size += 1
        logger.info(f"Inserted interval: {interval}")
        return True

    def _find_min_node(self, node: IntervalNode) -> IntervalNode:
        """Find node with minimum low endpoint in subtree.

        Args:
            node: Root of subtree.

        Returns:
            Node with minimum low endpoint.
        """
        while node.left:
            node = node.left
        return node

    def _delete_node(
        self, node: Optional[IntervalNode], interval: Interval
    ) -> Optional[IntervalNode]:
        """Recursively delete interval from tree.

        Args:
            node: Current node in recursion.
            interval: Interval to delete.

        Returns:
            Root of subtree after deletion.
        """
        if node is None:
            return None

        if interval.low < node.interval.low:
            node.left = self._delete_node(node.left, interval)
        elif interval.low > node.interval.low:
            node.right = self._delete_node(node.right, interval)
        else:
            if interval.high < node.interval.high:
                node.left = self._delete_node(node.left, interval)
            elif interval.high > node.interval.high:
                node.right = self._delete_node(node.right, interval)
            else:
                if node.left is None:
                    return node.right
                if node.right is None:
                    return node.left

                min_node = self._find_min_node(node.right)
                node.interval = min_node.interval
                node.right = self._delete_node(node.right, min_node.interval)

        node.update_max_endpoint()
        return node

    def delete(self, low: int, high: int) -> bool:
        """Delete interval from tree.

        Args:
            low: Lower endpoint of interval.
            high: Upper endpoint of interval.

        Returns:
            True if deleted, False if not found.

        Raises:
            ValueError: If low > high.
        """
        try:
            interval = Interval(low, high)
        except ValueError as e:
            logger.error(f"Invalid interval: {e}")
            raise

        if self.root is None:
            logger.info(f"Delete failed: tree is empty")
            return False

        if not self._search_interval(self.root, interval):
            logger.info(f"Delete failed: interval {interval} not found")
            return False

        self.root = self._delete_node(self.root, interval)
        self.size -= 1
        logger.info(f"Deleted interval: {interval}")
        return True

    def _search_overlapping_intervals(
        self, node: Optional[IntervalNode], query: Interval, result: List[Interval]
    ) -> None:
        """Recursively search for intervals overlapping query.

        Args:
            node: Current node in recursion.
            query: Query interval.
            result: List to collect overlapping intervals.
        """
        if node is None:
            return

        if node.interval.overlaps(query):
            result.append(node.interval)

        if node.left and node.left.max_endpoint >= query.low:
            self._search_overlapping_intervals(node.left, query, result)

        if node.right and node.interval.low <= query.high:
            self._search_overlapping_intervals(node.right, query, result)

    def find_overlapping_intervals(
        self, low: int, high: int
    ) -> List[Interval]:
        """Find all intervals overlapping with given interval.

        Args:
            low: Lower endpoint of query interval.
            high: Upper endpoint of query interval.

        Returns:
            List of overlapping intervals.

        Raises:
            ValueError: If low > high.
        """
        try:
            query = Interval(low, high)
        except ValueError as e:
            logger.error(f"Invalid query interval: {e}")
            raise

        result: List[Interval] = []
        self._search_overlapping_intervals(self.root, query, result)
        logger.info(f"Found {len(result)} intervals overlapping [{low}, {high}]")
        return result

    def _search_overlapping_point(
        self, node: Optional[IntervalNode], point: int, result: List[Interval]
    ) -> None:
        """Recursively search for intervals containing point.

        Args:
            node: Current node in recursion.
            point: Query point.
            result: List to collect overlapping intervals.
        """
        if node is None:
            return

        if node.interval.overlaps_point(point):
            result.append(node.interval)

        if node.left and node.left.max_endpoint >= point:
            self._search_overlapping_point(node.left, point, result)

        if node.right and node.interval.low <= point:
            self._search_overlapping_point(node.right, point, result)

    def find_intervals_containing_point(self, point: int) -> List[Interval]:
        """Find all intervals containing a point.

        Args:
            point: Query point.

        Returns:
            List of intervals containing the point.
        """
        result: List[Interval] = []
        self._search_overlapping_point(self.root, point, result)
        logger.info(f"Found {len(result)} intervals containing point {point}")
        return result

    def _inorder_traversal(
        self, node: Optional[IntervalNode], result: List[Interval]
    ) -> None:
        """Perform inorder traversal.

        Args:
            node: Current node.
            result: List to collect intervals.
        """
        if node:
            self._inorder_traversal(node.left, result)
            result.append(node.interval)
            self._inorder_traversal(node.right, result)

    def get_all_intervals(self) -> List[Interval]:
        """Get all intervals in sorted order by low endpoint.

        Returns:
            List of all intervals sorted by low endpoint.
        """
        result: List[Interval] = []
        self._inorder_traversal(self.root, result)
        return result

    def is_empty(self) -> bool:
        """Check if tree is empty.

        Returns:
            True if empty, False otherwise.
        """
        return self.root is None

    def get_size(self) -> int:
        """Get number of intervals in tree.

        Returns:
            Number of intervals.
        """
        return self.size

    def clear(self) -> None:
        """Clear all intervals from tree."""
        self.root = None
        self.size = 0
        logger.info("Tree cleared")


def main() -> None:
    """Main function to demonstrate interval tree operations."""
    tree = IntervalTree()

    print("Interval Tree Operations Demo")
    print("=" * 50)

    intervals = [(15, 20), (10, 30), (17, 19), (5, 20), (12, 15), (30, 40)]
    print(f"\nInserting intervals: {intervals}")
    for low, high in intervals:
        tree.insert(low, high)

    print(f"\nTree size: {tree.get_size()}")
    print(f"All intervals: {tree.get_all_intervals()}")

    print("\nFinding intervals overlapping [14, 16]:")
    overlapping = tree.find_overlapping_intervals(14, 16)
    for interval in overlapping:
        print(f"  {interval}")

    print("\nFinding intervals containing point 18:")
    containing = tree.find_intervals_containing_point(18)
    for interval in containing:
        print(f"  {interval}")

    print("\nDeleting interval [15, 20]:")
    tree.delete(15, 20)
    print(f"Tree size after deletion: {tree.get_size()}")
    print(f"All intervals: {tree.get_all_intervals()}")


if __name__ == "__main__":
    main()
