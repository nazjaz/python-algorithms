"""K-D Tree for Multidimensional Range Queries and Nearest Neighbor Search.

This module provides functionality to implement k-d tree (k-dimensional tree)
data structure that efficiently stores points in k-dimensional space and
supports range queries and nearest neighbor search. K-d trees achieve
O(log n) average time complexity for queries.
"""

import logging
import logging.handlers
import math
from pathlib import Path
from typing import List, Optional, Tuple

import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class KDNode:
    """Node in k-d tree."""

    def __init__(self, point: List[float], dimension: int = 0) -> None:
        """Initialize KDNode.

        Args:
            point: Point coordinates in k-dimensional space.
            dimension: Dimension used for splitting at this node.
        """
        self.point = point
        self.dimension = dimension
        self.left: Optional["KDNode"] = None
        self.right: Optional["KDNode"] = None

    def __repr__(self) -> str:
        """String representation."""
        return f"KDNode(point={self.point}, dim={self.dimension})"


class KDTree:
    """K-d tree for multidimensional range queries and nearest neighbor search."""

    def __init__(self, points: Optional[List[List[float]]] = None, config_path: str = "config.yaml") -> None:
        """Initialize k-d tree.

        Args:
            points: Optional list of points to build tree from.
            config_path: Path to configuration file.
        """
        self.root: Optional[KDNode] = None
        self.k = 0
        self.size = 0
        self._setup_logging()
        self._load_config(config_path)

        if points:
            self.build_tree(points)

    def _setup_logging(self) -> None:
        """Configure logging for k-d tree operations."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        handler = logging.handlers.RotatingFileHandler(
            log_dir / "kd_tree.log",
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

    def _validate_point(self, point: List[float]) -> None:
        """Validate point dimensions.

        Args:
            point: Point to validate.

        Raises:
            ValueError: If point dimensions don't match tree dimension.
        """
        if self.k == 0:
            self.k = len(point)
        elif len(point) != self.k:
            raise ValueError(
                f"Point dimension {len(point)} doesn't match tree dimension {self.k}"
            )

    def _build_tree_recursive(
        self, points: List[List[float]], depth: int = 0
    ) -> Optional[KDNode]:
        """Recursively build k-d tree from points.

        Args:
            points: List of points to build tree from.
            depth: Current depth in tree.

        Returns:
            Root node of subtree.
        """
        if not points:
            return None

        k = len(points[0])
        dimension = depth % k

        sorted_points = sorted(points, key=lambda p: p[dimension])
        median_idx = len(sorted_points) // 2

        node = KDNode(sorted_points[median_idx], dimension)
        node.left = self._build_tree_recursive(
            sorted_points[:median_idx], depth + 1
        )
        node.right = self._build_tree_recursive(
            sorted_points[median_idx + 1 :], depth + 1
        )

        return node

    def build_tree(self, points: List[List[float]]) -> None:
        """Build k-d tree from list of points.

        Args:
            points: List of points, each point is a list of coordinates.

        Raises:
            ValueError: If points have inconsistent dimensions.
        """
        if not points:
            logger.warning("Cannot build tree from empty point list")
            return

        if not all(len(p) == len(points[0]) for p in points):
            raise ValueError("All points must have the same dimension")

        self.k = len(points[0])
        self.root = self._build_tree_recursive(points)
        self.size = len(points)
        logger.info(f"Built k-d tree with {self.size} points in {self.k} dimensions")

    def _insert_recursive(
        self, node: Optional[KDNode], point: List[float], depth: int = 0
    ) -> KDNode:
        """Recursively insert point into tree.

        Args:
            node: Current node in recursion.
            point: Point to insert.
            depth: Current depth in tree.

        Returns:
            Root of subtree after insertion.
        """
        if node is None:
            dimension = depth % self.k
            new_node = KDNode(point, dimension)
            logger.debug(f"Inserted point: {point}")
            return new_node

        dimension = node.dimension
        if point[dimension] < node.point[dimension]:
            node.left = self._insert_recursive(node.left, point, depth + 1)
        else:
            node.right = self._insert_recursive(node.right, point, depth + 1)

        return node

    def insert(self, point: List[float]) -> None:
        """Insert point into tree.

        Args:
            point: Point coordinates to insert.

        Raises:
            ValueError: If point dimensions don't match tree dimension.
        """
        self._validate_point(point)

        if self.root is None:
            self.k = len(point)
            self.root = KDNode(point, 0)
            self.size = 1
            logger.info(f"Inserted root point: {point}")
            return

        self._insert_recursive(self.root, point)
        self.size += 1
        logger.info(f"Inserted point: {point}")

    def _point_in_range(
        self, point: List[float], min_range: List[float], max_range: List[float]
    ) -> bool:
        """Check if point is within range.

        Args:
            point: Point to check.
            min_range: Minimum bounds for each dimension.
            max_range: Maximum bounds for each dimension.

        Returns:
            True if point is in range, False otherwise.
        """
        return all(
            min_range[i] <= point[i] <= max_range[i] for i in range(len(point))
        )

    def _range_query_recursive(
        self,
        node: Optional[KDNode],
        min_range: List[float],
        max_range: List[float],
        results: List[List[float]],
    ) -> None:
        """Recursively search for points in range.

        Args:
            node: Current node in recursion.
            min_range: Minimum bounds for each dimension.
            max_range: Maximum bounds for each dimension.
            results: List to collect points in range.
        """
        if node is None:
            return

        if self._point_in_range(node.point, min_range, max_range):
            results.append(node.point)

        dimension = node.dimension
        split_value = node.point[dimension]

        if min_range[dimension] <= split_value:
            self._range_query_recursive(node.left, min_range, max_range, results)

        if max_range[dimension] >= split_value:
            self._range_query_recursive(node.right, min_range, max_range, results)

    def range_query(
        self, min_range: List[float], max_range: List[float]
    ) -> List[List[float]]:
        """Find all points within given range.

        Args:
            min_range: Minimum bounds for each dimension.
            max_range: Maximum bounds for each dimension.

        Returns:
            List of points within range.

        Raises:
            ValueError: If range dimensions don't match tree dimension.
        """
        if self.root is None:
            logger.info("Range query on empty tree")
            return []

        if len(min_range) != self.k or len(max_range) != self.k:
            raise ValueError(
                f"Range dimensions don't match tree dimension {self.k}"
            )

        if not all(min_range[i] <= max_range[i] for i in range(self.k)):
            raise ValueError("min_range values must be <= max_range values")

        results: List[List[float]] = []
        self._range_query_recursive(self.root, min_range, max_range, results)
        logger.info(f"Range query found {len(results)} points")
        return results

    def _euclidean_distance(
        self, point1: List[float], point2: List[float]
    ) -> float:
        """Calculate Euclidean distance between two points.

        Args:
            point1: First point.
            point2: Second point.

        Returns:
            Euclidean distance.
        """
        return math.sqrt(
            sum((point1[i] - point2[i]) ** 2 for i in range(len(point1)))
        )

    def _nearest_neighbor_recursive(
        self,
        node: Optional[KDNode],
        query_point: List[float],
        best: Tuple[Optional[List[float]], float],
    ) -> Tuple[Optional[List[float]], float]:
        """Recursively find nearest neighbor.

        Args:
            node: Current node in recursion.
            query_point: Query point.
            best: Tuple of (best point, best distance).

        Returns:
            Tuple of (nearest point, distance).
        """
        if node is None:
            return best

        distance = self._euclidean_distance(node.point, query_point)
        best_point, best_distance = best

        if best_point is None or distance < best_distance:
            best_point = node.point
            best_distance = distance

        dimension = node.dimension
        split_value = node.point[dimension]
        query_value = query_point[dimension]

        if query_value < split_value:
            best = self._nearest_neighbor_recursive(
                node.left, query_point, (best_point, best_distance)
            )
            if abs(query_value - split_value) < best[1]:
                best = self._nearest_neighbor_recursive(
                    node.right, query_point, best
                )
        else:
            best = self._nearest_neighbor_recursive(
                node.right, query_point, (best_point, best_distance)
            )
            if abs(query_value - split_value) < best[1]:
                best = self._nearest_neighbor_recursive(
                    node.left, query_point, best
                )

        return best

    def nearest_neighbor(self, query_point: List[float]) -> Optional[List[float]]:
        """Find nearest neighbor to query point.

        Args:
            query_point: Query point coordinates.

        Returns:
            Nearest point or None if tree is empty.

        Raises:
            ValueError: If query point dimension doesn't match tree dimension.
        """
        if self.root is None:
            logger.info("Nearest neighbor query on empty tree")
            return None

        if len(query_point) != self.k:
            raise ValueError(
                f"Query point dimension {len(query_point)} doesn't match tree dimension {self.k}"
            )

        best_point, _ = self._nearest_neighbor_recursive(
            self.root, query_point, (None, float("inf"))
        )
        logger.info(f"Found nearest neighbor: {best_point}")
        return best_point

    def _k_nearest_neighbors_recursive(
        self,
        node: Optional[KDNode],
        query_point: List[float],
        k: int,
        neighbors: List[Tuple[List[float], float]],
    ) -> None:
        """Recursively find k nearest neighbors.

        Args:
            node: Current node in recursion.
            query_point: Query point.
            k: Number of neighbors to find.
            neighbors: List of (point, distance) tuples, sorted by distance.
        """
        if node is None:
            return

        distance = self._euclidean_distance(node.point, query_point)

        if len(neighbors) < k:
            neighbors.append((node.point, distance))
            neighbors.sort(key=lambda x: x[1])
        elif distance < neighbors[-1][1]:
            neighbors[-1] = (node.point, distance)
            neighbors.sort(key=lambda x: x[1])

        dimension = node.dimension
        split_value = node.point[dimension]
        query_value = query_point[dimension]

        if query_value < split_value:
            self._k_nearest_neighbors_recursive(
                node.left, query_point, k, neighbors
            )
            if len(neighbors) < k or abs(query_value - split_value) < neighbors[-1][1]:
                self._k_nearest_neighbors_recursive(
                    node.right, query_point, k, neighbors
                )
        else:
            self._k_nearest_neighbors_recursive(
                node.right, query_point, k, neighbors
            )
            if len(neighbors) < k or abs(query_value - split_value) < neighbors[-1][1]:
                self._k_nearest_neighbors_recursive(
                    node.left, query_point, k, neighbors
                )

    def k_nearest_neighbors(
        self, query_point: List[float], k: int
    ) -> List[List[float]]:
        """Find k nearest neighbors to query point.

        Args:
            query_point: Query point coordinates.
            k: Number of neighbors to find.

        Returns:
            List of k nearest points.

        Raises:
            ValueError: If query point dimension doesn't match tree dimension or k <= 0.
        """
        if self.root is None:
            logger.info("K-nearest neighbors query on empty tree")
            return []

        if k <= 0:
            raise ValueError("k must be positive")

        if len(query_point) != self.k:
            raise ValueError(
                f"Query point dimension {len(query_point)} doesn't match tree dimension {self.k}"
            )

        neighbors: List[Tuple[List[float], float]] = []
        self._k_nearest_neighbors_recursive(self.root, query_point, k, neighbors)
        result = [point for point, _ in neighbors]
        logger.info(f"Found {len(result)} nearest neighbors")
        return result

    def get_all_points(self) -> List[List[float]]:
        """Get all points in tree.

        Returns:
            List of all points.
        """
        results: List[List[float]] = []

        def _traverse(node: Optional[KDNode]) -> None:
            if node:
                _traverse(node.left)
                results.append(node.point)
                _traverse(node.right)

        _traverse(self.root)
        return results

    def is_empty(self) -> bool:
        """Check if tree is empty.

        Returns:
            True if empty, False otherwise.
        """
        return self.root is None

    def get_size(self) -> int:
        """Get number of points in tree.

        Returns:
            Number of points.
        """
        return self.size

    def get_dimension(self) -> int:
        """Get dimension of points in tree.

        Returns:
            Dimension of points.
        """
        return self.k

    def clear(self) -> None:
        """Clear all points from tree."""
        self.root = None
        self.size = 0
        self.k = 0
        logger.info("Tree cleared")


def main() -> None:
    """Main function to demonstrate k-d tree operations."""
    points = [[2, 3], [5, 4], [9, 6], [4, 7], [8, 1], [7, 2]]
    tree = KDTree(points)

    print("K-D Tree Operations Demo")
    print("=" * 50)

    print(f"\nBuilt tree with {tree.get_size()} points in {tree.get_dimension()}D")
    print(f"All points: {tree.get_all_points()}")

    print("\nRange query [3, 3] to [7, 7]:")
    results = tree.range_query([3, 3], [7, 7])
    for point in results:
        print(f"  {point}")

    print("\nNearest neighbor to [6, 5]:")
    nearest = tree.nearest_neighbor([6, 5])
    print(f"  {nearest}")

    print("\n3 nearest neighbors to [6, 5]:")
    k_nearest = tree.k_nearest_neighbors([6, 5], 3)
    for point in k_nearest:
        print(f"  {point}")


if __name__ == "__main__":
    main()
