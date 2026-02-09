"""R-Tree for Spatial Indexing and Geometric Range Queries.

This module provides functionality to implement R-tree data structure
that efficiently stores spatial objects (rectangles) and supports
geometric range queries. R-trees use bounding boxes to organize
spatial data hierarchically.
"""

import logging
import logging.handlers
from pathlib import Path
from typing import List, Optional, Tuple, Union

import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class Rectangle:
    """Represents a rectangle (bounding box) in 2D space."""

    def __init__(
        self, min_x: float, min_y: float, max_x: float, max_y: float
    ) -> None:
        """Initialize rectangle.

        Args:
            min_x: Minimum x coordinate.
            min_y: Minimum y coordinate.
            max_x: Maximum x coordinate.
            max_y: Maximum y coordinate.

        Raises:
            ValueError: If min_x > max_x or min_y > max_y.
        """
        if min_x > max_x or min_y > max_y:
            raise ValueError("Invalid rectangle: min > max")
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y

    def area(self) -> float:
        """Calculate area of rectangle.

        Returns:
            Area of rectangle.
        """
        return (self.max_x - self.min_x) * (self.max_y - self.min_y)

    def intersects(self, other: "Rectangle") -> bool:
        """Check if this rectangle intersects with another.

        Args:
            other: Other rectangle to check.

        Returns:
            True if rectangles intersect, False otherwise.
        """
        return not (
            self.max_x < other.min_x
            or self.min_x > other.max_x
            or self.max_y < other.min_y
            or self.min_y > other.max_y
        )

    def contains(self, other: "Rectangle") -> bool:
        """Check if this rectangle contains another.

        Args:
            other: Other rectangle to check.

        Returns:
            True if this rectangle contains other, False otherwise.
        """
        return (
            self.min_x <= other.min_x
            and self.max_x >= other.max_x
            and self.min_y <= other.min_y
            and self.max_y >= other.max_y
        )

    def union(self, other: "Rectangle") -> "Rectangle":
        """Create union rectangle with another.

        Args:
            other: Other rectangle.

        Returns:
            Union rectangle.
        """
        return Rectangle(
            min(self.min_x, other.min_x),
            min(self.min_y, other.min_y),
            max(self.max_x, other.max_x),
            max(self.max_y, other.max_y),
        )

    def expansion_area(self, other: "Rectangle") -> float:
        """Calculate area increase needed to include other rectangle.

        Args:
            other: Other rectangle.

        Returns:
            Area increase.
        """
        union_rect = self.union(other)
        return union_rect.area() - self.area()

    def __repr__(self) -> str:
        """String representation."""
        return f"Rectangle({self.min_x}, {self.min_y}, {self.max_x}, {self.max_y})"


class RTreeNode:
    """Node in R-tree."""

    def __init__(self, is_leaf: bool = True) -> None:
        """Initialize R-tree node.

        Args:
            is_leaf: Whether this node is a leaf node.
        """
        self.is_leaf = is_leaf
        self.entries: List[Tuple[Rectangle, Optional["RTreeNode"], Optional[object]]] = []
        self.mbr: Optional[Rectangle] = None

    def update_mbr(self) -> None:
        """Update minimum bounding rectangle from entries."""
        if not self.entries:
            self.mbr = None
            return

        mbr = self.entries[0][0]
        for entry_mbr, _, _ in self.entries:
            mbr = mbr.union(entry_mbr)
        self.mbr = mbr

    def __repr__(self) -> str:
        """String representation."""
        node_type = "Leaf" if self.is_leaf else "Internal"
        return f"RTreeNode({node_type}, entries={len(self.entries)})"


class RTree:
    """R-tree for spatial indexing and geometric range queries."""

    def __init__(
        self, max_entries: int = 4, min_entries: int = 2, config_path: str = "config.yaml"
    ) -> None:
        """Initialize R-tree.

        Args:
            max_entries: Maximum number of entries per node.
            min_entries: Minimum number of entries per node.
            config_path: Path to configuration file.
        """
        if min_entries < 1 or max_entries < min_entries:
            raise ValueError("Invalid min/max entries configuration")

        self.max_entries = max_entries
        self.min_entries = min_entries
        self.root: Optional[RTreeNode] = None
        self.size = 0
        self._setup_logging()
        self._load_config(config_path)

    def _setup_logging(self) -> None:
        """Configure logging for R-tree operations."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        handler = logging.handlers.RotatingFileHandler(
            log_dir / "r_tree.log",
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

    def _choose_subtree(
        self, node: RTreeNode, rectangle: Rectangle
    ) -> Tuple[Rectangle, RTreeNode]:
        """Choose best subtree for inserting rectangle.

        Args:
            node: Current node.
            rectangle: Rectangle to insert.

        Returns:
            Tuple of (entry MBR, child node).
        """
        if node.is_leaf:
            return (node.mbr, node) if node.mbr else (rectangle, node)

        best_entry = None
        min_expansion = float("inf")

        for entry_mbr, child, _ in node.entries:
            expansion = entry_mbr.expansion_area(rectangle)
            if expansion < min_expansion or (
                expansion == min_expansion
                and entry_mbr.area() < (best_entry[0].area() if best_entry else float("inf"))
            ):
                min_expansion = expansion
                best_entry = (entry_mbr, child, _)

        return (best_entry[0], best_entry[1])

    def _split_node(self, node: RTreeNode) -> Tuple[RTreeNode, RTreeNode]:
        """Split overflowing node using quadratic split.

        Args:
            node: Node to split.

        Returns:
            Tuple of (left node, right node).
        """
        entries = node.entries[:]
        left_node = RTreeNode(is_leaf=node.is_leaf)
        right_node = RTreeNode(is_leaf=node.is_leaf)

        if not entries:
            return left_node, right_node

        seed1, seed2 = self._pick_seeds(entries)
        left_node.entries.append(entries[seed1])
        right_node.entries.append(entries[seed2])

        remaining = [
            e for i, e in enumerate(entries) if i not in (seed1, seed2)
        ]

        while remaining:
            if (
                len(left_node.entries) + len(remaining) <= self.min_entries
            ):
                left_node.entries.extend(remaining)
                break
            if (
                len(right_node.entries) + len(remaining) <= self.min_entries
            ):
                right_node.entries.extend(remaining)
                break

            next_entry, next_group = self._pick_next(
                remaining, left_node, right_node
            )
            if next_group == 0:
                left_node.entries.append(next_entry)
            else:
                right_node.entries.append(next_entry)
            remaining.remove(next_entry)

        left_node.update_mbr()
        right_node.update_mbr()
        return left_node, right_node

    def _pick_seeds(
        self, entries: List[Tuple[Rectangle, Optional[RTreeNode], Optional[object]]]
    ) -> Tuple[int, int]:
        """Pick two seed entries for splitting.

        Args:
            entries: List of entries.

        Returns:
            Tuple of (seed1 index, seed2 index).
        """
        max_waste = -1
        seed1, seed2 = 0, 1

        for i in range(len(entries)):
            for j in range(i + 1, len(entries)):
                mbr1 = entries[i][0]
                mbr2 = entries[j][0]
                union_mbr = mbr1.union(mbr2)
                waste = union_mbr.area() - mbr1.area() - mbr2.area()

                if waste > max_waste:
                    max_waste = waste
                    seed1, seed2 = i, j

        return seed1, seed2

    def _pick_next(
        self,
        remaining: List[Tuple[Rectangle, Optional[RTreeNode], Optional[object]]],
        group1: RTreeNode,
        group2: RTreeNode,
    ) -> Tuple[Tuple[Rectangle, Optional[RTreeNode], Optional[object]], int]:
        """Pick next entry to assign to a group.

        Args:
            remaining: Remaining entries.
            group1: First group.
            group2: Second group.

        Returns:
            Tuple of (entry, group index).
        """
        max_diff = -1
        best_entry = remaining[0]
        best_group = 0

        group1_mbr = group1.mbr if group1.mbr else Rectangle(0, 0, 0, 0)
        group2_mbr = group2.mbr if group2.mbr else Rectangle(0, 0, 0, 0)

        for entry in remaining:
            entry_mbr = entry[0]
            diff1 = group1_mbr.expansion_area(entry_mbr)
            diff2 = group2_mbr.expansion_area(entry_mbr)
            diff = abs(diff1 - diff2)

            if diff > max_diff:
                max_diff = diff
                best_entry = entry
                best_group = 0 if diff1 < diff2 else 1

        return best_entry, best_group

    def _insert_recursive(
        self, node: RTreeNode, rectangle: Rectangle, data: Optional[object] = None
    ) -> Optional[Union[Tuple[RTreeNode, RTreeNode], RTreeNode]]:
        """Recursively insert rectangle into tree.

        Args:
            node: Current node.
            rectangle: Rectangle to insert.
            data: Optional data associated with rectangle.

        Returns:
            Tuple of (left_node, right_node) if split occurred at non-root,
            new RTreeNode if split occurred at root, None otherwise.
        """
        if node.is_leaf:
            node.entries.append((rectangle, None, data))
            node.update_mbr()
            self.size += 1

            if len(node.entries) > self.max_entries:
                left_node, right_node = self._split_node(node)
                if node == self.root:
                    new_root = RTreeNode(is_leaf=False)
                    new_root.entries.append((left_node.mbr, left_node, None))
                    new_root.entries.append((right_node.mbr, right_node, None))
                    new_root.update_mbr()
                    return new_root
                return (left_node, right_node)
            return None

        entry_mbr, child = self._choose_subtree(node, rectangle)
        split_result = self._insert_recursive(child, rectangle, data)

        if split_result is not None:
            for i, (mbr, c, d) in enumerate(node.entries):
                if c == child:
                    node.entries.pop(i)
                    break
            left_node, right_node = split_result
            node.entries.append((left_node.mbr, left_node, None))
            node.entries.append((right_node.mbr, right_node, None))
        else:
            for i, (mbr, c, d) in enumerate(node.entries):
                if c == child:
                    node.entries[i] = (child.mbr, child, d)
                    break

        node.update_mbr()

        if len(node.entries) > self.max_entries:
            left_node, right_node = self._split_node(node)
            if node == self.root:
                new_root = RTreeNode(is_leaf=False)
                new_root.entries.append((left_node.mbr, left_node, None))
                new_root.entries.append((right_node.mbr, right_node, None))
                new_root.update_mbr()
                return new_root
            return (left_node, right_node)

        return None

    def insert(
        self, min_x: float, min_y: float, max_x: float, max_y: float, data: Optional[object] = None
    ) -> None:
        """Insert rectangle into tree.

        Args:
            min_x: Minimum x coordinate.
            min_y: Minimum y coordinate.
            max_x: Maximum x coordinate.
            max_y: Maximum y coordinate.
            data: Optional data associated with rectangle.

        Raises:
            ValueError: If rectangle is invalid.
        """
        try:
            rectangle = Rectangle(min_x, min_y, max_x, max_y)
        except ValueError as e:
            logger.error(f"Invalid rectangle: {e}")
            raise

        if self.root is None:
            self.root = RTreeNode(is_leaf=True)
            self.root.entries.append((rectangle, None, data))
            self.root.update_mbr()
            self.size = 1
            logger.info(f"Inserted root rectangle: {rectangle}")
            return

        split_result = self._insert_recursive(self.root, rectangle, data)
        if split_result is not None:
            if isinstance(split_result, tuple):
                left_node, right_node = split_result
                new_root = RTreeNode(is_leaf=False)
                new_root.entries.append((left_node.mbr, left_node, None))
                new_root.entries.append((right_node.mbr, right_node, None))
                new_root.update_mbr()
                self.root = new_root
            else:
                self.root = split_result
        logger.info(f"Inserted rectangle: {rectangle}")

    def _range_query_recursive(
        self,
        node: Optional[RTreeNode],
        query_rect: Rectangle,
        results: List[Tuple[Rectangle, Optional[object]]],
    ) -> None:
        """Recursively search for rectangles in range.

        Args:
            node: Current node.
            query_rect: Query rectangle.
            results: List to collect results.
        """
        if node is None:
            return

        if not node.mbr or not node.mbr.intersects(query_rect):
            return

        if node.is_leaf:
            for entry_mbr, _, data in node.entries:
                if entry_mbr.intersects(query_rect):
                    results.append((entry_mbr, data))
        else:
            for entry_mbr, child, _ in node.entries:
                if entry_mbr.intersects(query_rect):
                    self._range_query_recursive(child, query_rect, results)

    def range_query(
        self, min_x: float, min_y: float, max_x: float, max_y: float
    ) -> List[Tuple[Rectangle, Optional[object]]]:
        """Find all rectangles intersecting with query rectangle.

        Args:
            min_x: Minimum x coordinate of query.
            min_y: Minimum y coordinate of query.
            max_x: Maximum x coordinate of query.
            max_y: Maximum y coordinate of query.

        Returns:
            List of (rectangle, data) tuples.

        Raises:
            ValueError: If query rectangle is invalid.
        """
        try:
            query_rect = Rectangle(min_x, min_y, max_x, max_y)
        except ValueError as e:
            logger.error(f"Invalid query rectangle: {e}")
            raise

        results: List[Tuple[Rectangle, Optional[object]]] = []
        self._range_query_recursive(self.root, query_rect, results)
        logger.info(f"Range query found {len(results)} rectangles")
        return results

    def get_all_rectangles(self) -> List[Tuple[Rectangle, Optional[object]]]:
        """Get all rectangles in tree.

        Returns:
            List of (rectangle, data) tuples.
        """
        results: List[Tuple[Rectangle, Optional[object]]] = []

        def _traverse(node: Optional[RTreeNode]) -> None:
            if node is None:
                return
            if node.is_leaf:
                results.extend([(mbr, data) for mbr, _, data in node.entries])
            else:
                for _, child, _ in node.entries:
                    _traverse(child)

        _traverse(self.root)
        return results

    def is_empty(self) -> bool:
        """Check if tree is empty.

        Returns:
            True if empty, False otherwise.
        """
        return self.root is None

    def get_size(self) -> int:
        """Get number of rectangles in tree.

        Returns:
            Number of rectangles.
        """
        return self.size

    def clear(self) -> None:
        """Clear all rectangles from tree."""
        self.root = None
        self.size = 0
        logger.info("Tree cleared")


def main() -> None:
    """Main function to demonstrate R-tree operations."""
    tree = RTree(max_entries=4, min_entries=2)

    print("R-Tree Operations Demo")
    print("=" * 50)

    rectangles = [
        (1, 1, 3, 3),
        (2, 2, 4, 4),
        (5, 5, 7, 7),
        (6, 6, 8, 8),
        (1, 5, 3, 7),
        (5, 1, 7, 3),
    ]

    print(f"\nInserting rectangles: {rectangles}")
    for min_x, min_y, max_x, max_y in rectangles:
        tree.insert(min_x, min_y, max_x, max_y)

    print(f"\nTree size: {tree.get_size()}")

    print("\nRange query [2, 2] to [6, 6]:")
    results = tree.range_query(2, 2, 6, 6)
    for rect, data in results:
        print(f"  {rect}")

    print("\nAll rectangles in tree:")
    all_rects = tree.get_all_rectangles()
    for rect, data in all_rects:
        print(f"  {rect}")


if __name__ == "__main__":
    main()
