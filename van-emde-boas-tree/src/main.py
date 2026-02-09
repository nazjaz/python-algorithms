"""Van Emde Boas Tree for Integer Priority Queues with O(log log U) Operations.

This module provides functionality to implement van Emde Boas (vEB) tree data
structure that efficiently supports priority queue operations on integers from
universe [0, U-1]. Van Emde Boas trees achieve O(log log U) time complexity
for insert, delete, and search operations.
"""

import logging
import logging.handlers
import math
from pathlib import Path
from typing import List, Optional

import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class VEBNode:
    """Node in van Emde Boas tree."""

    def __init__(self, universe_size: int) -> None:
        """Initialize vEB node.

        Args:
            universe_size: Size of universe (must be power of 2).

        Raises:
            ValueError: If universe_size is not a power of 2.
        """
        if universe_size <= 0 or (universe_size & (universe_size - 1)) != 0:
            raise ValueError(f"Universe size {universe_size} must be a power of 2")

        self.universe_size = universe_size
        self.min: Optional[int] = None
        self.max: Optional[int] = None

        if universe_size == 2:
            self.clusters: Optional[List["VEBNode"]] = None
            self.summary: Optional["VEBNode"] = None
        else:
            upper_sqrt = int(math.sqrt(universe_size))
            lower_sqrt = universe_size // upper_sqrt

            self.clusters = [VEBNode(lower_sqrt) for _ in range(upper_sqrt)]
            self.summary = VEBNode(upper_sqrt)

    def is_empty(self) -> bool:
        """Check if node is empty.

        Returns:
            True if empty, False otherwise.
        """
        return self.min is None

    def high(self, x: int) -> int:
        """Get high bits (cluster index).

        Args:
            x: Value.

        Returns:
            Cluster index.
        """
        sqrt_u = int(math.sqrt(self.universe_size))
        return x // sqrt_u

    def low(self, x: int) -> int:
        """Get low bits (position in cluster).

        Args:
            x: Value.

        Returns:
            Position in cluster.
        """
        sqrt_u = int(math.sqrt(self.universe_size))
        return x % sqrt_u

    def index(self, high: int, low: int) -> int:
        """Combine high and low to get value.

        Args:
            high: Cluster index.
            low: Position in cluster.

        Returns:
            Combined value.
        """
        sqrt_u = int(math.sqrt(self.universe_size))
        return high * sqrt_u + low

    def __repr__(self) -> str:
        """String representation."""
        return f"VEBNode(U={self.universe_size}, min={self.min}, max={self.max})"


class VanEmdeBoasTree:
    """Van Emde Boas tree for integer priority queues."""

    def __init__(self, universe_size: int, config_path: str = "config.yaml") -> None:
        """Initialize van Emde Boas tree.

        Args:
            universe_size: Size of universe [0, U-1] (must be power of 2).
            config_path: Path to configuration file.

        Raises:
            ValueError: If universe_size is not a power of 2.
        """
        if universe_size <= 0 or (universe_size & (universe_size - 1)) != 0:
            raise ValueError(f"Universe size {universe_size} must be a power of 2")

        self.universe_size = universe_size
        self.root = VEBNode(universe_size)
        self.size = 0
        self._setup_logging()
        self._load_config(config_path)
        logger.info(f"Created vEB tree with universe size {universe_size}")

    def _setup_logging(self) -> None:
        """Configure logging for vEB tree operations."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        handler = logging.handlers.RotatingFileHandler(
            log_dir / "van_emde_boas_tree.log",
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

    def _insert_empty(self, node: VEBNode, x: int) -> None:
        """Insert into empty node.

        Args:
            node: Node to insert into.
            x: Value to insert.
        """
        node.min = x
        node.max = x

    def _insert_recursive(self, node: VEBNode, x: int) -> None:
        """Recursively insert value.

        Args:
            node: Current node.
            x: Value to insert.
        """
        if node.is_empty():
            self._insert_empty(node, x)
            return

        if x < node.min:
            x, node.min = node.min, x

        if node.universe_size > 2:
            high = node.high(x)
            low = node.low(x)

            if node.clusters[high].is_empty():
                if node.summary:
                    self._insert_recursive(node.summary, high)
                self._insert_empty(node.clusters[high], low)
            else:
                self._insert_recursive(node.clusters[high], low)

            if x > node.max:
                node.max = x
        else:
            if x > node.max:
                node.max = x

    def insert(self, x: int) -> bool:
        """Insert value into tree.

        Args:
            x: Value to insert.

        Returns:
            True if inserted, False if already exists.

        Raises:
            ValueError: If value is out of universe range.
        """
        if x < 0 or x >= self.universe_size:
            raise ValueError(f"Value {x} out of universe range [0, {self.universe_size-1}]")

        if self.contains(x):
            logger.info(f"Value {x} already exists")
            return False

        self._insert_recursive(self.root, x)
        self.size += 1
        logger.info(f"Inserted value: {x}")
        return True

    def _delete_recursive(self, node: VEBNode, x: int) -> None:
        """Recursively delete value.

        Args:
            node: Current node.
            x: Value to delete.
        """
        if node.min == node.max:
            node.min = None
            node.max = None
            return

        if node.universe_size == 2:
            if x == 0:
                node.min = 1
            else:
                node.min = 0
            node.max = node.min
            return

        if x == node.min:
            first_cluster = node.summary.min if node.summary else None
            if first_cluster is None:
                node.min = None
                node.max = None
                return

            x = node.index(first_cluster, node.clusters[first_cluster].min)
            node.min = x

        high = node.high(x)
        low = node.low(x)

        self._delete_recursive(node.clusters[high], low)

        if node.clusters[high].is_empty():
            if node.summary:
                self._delete_recursive(node.summary, high)

        if x == node.max:
            if node.summary and not node.summary.is_empty():
                summary_max = node.summary.max
                cluster_max = node.clusters[summary_max].max
                node.max = node.index(summary_max, cluster_max)
            else:
                node.max = node.min

    def delete(self, x: int) -> bool:
        """Delete value from tree.

        Args:
            x: Value to delete.

        Returns:
            True if deleted, False if not found.

        Raises:
            ValueError: If value is out of universe range.
        """
        if x < 0 or x >= self.universe_size:
            raise ValueError(f"Value {x} out of universe range [0, {self.universe_size-1}]")

        if not self.contains(x):
            logger.info(f"Value {x} not found")
            return False

        self._delete_recursive(self.root, x)
        self.size -= 1
        logger.info(f"Deleted value: {x}")
        return True

    def _contains_recursive(self, node: VEBNode, x: int) -> bool:
        """Recursively check if value exists.

        Args:
            node: Current node.
            x: Value to check.

        Returns:
            True if exists, False otherwise.
        """
        if x == node.min or x == node.max:
            return True

        if node.is_empty() or node.universe_size == 2:
            return False

        high = node.high(x)
        low = node.low(x)

        return self._contains_recursive(node.clusters[high], low)

    def contains(self, x: int) -> bool:
        """Check if value exists in tree.

        Args:
            x: Value to check.

        Returns:
            True if exists, False otherwise.

        Raises:
            ValueError: If value is out of universe range.
        """
        if x < 0 or x >= self.universe_size:
            raise ValueError(f"Value {x} out of universe range [0, {self.universe_size-1}]")

        if self.root.is_empty():
            return False

        return self._contains_recursive(self.root, x)

    def get_min(self) -> Optional[int]:
        """Get minimum value in tree.

        Returns:
            Minimum value or None if empty.

        Time Complexity: O(1)
        """
        if self.root.is_empty():
            return None

        result = self.root.min
        logger.info(f"Minimum value: {result}")
        return result

    def get_max(self) -> Optional[int]:
        """Get maximum value in tree.

        Returns:
            Maximum value or None if empty.

        Time Complexity: O(1)
        """
        if self.root.is_empty():
            return None

        result = self.root.max
        logger.info(f"Maximum value: {result}")
        return result

    def _predecessor_recursive(self, node: VEBNode, x: int) -> Optional[int]:
        """Recursively find predecessor.

        Args:
            node: Current node.
            x: Value to find predecessor for.

        Returns:
            Predecessor or None.
        """
        if node.is_empty():
            return None

        if node.min is not None and x <= node.min:
            return None

        if node.universe_size == 2:
            if x == 1 and node.min == 0:
                return 0
            return None

        high = node.high(x)
        low = node.low(x)

        if not node.clusters[high].is_empty() and low > node.clusters[high].min:
            offset = self._predecessor_recursive(node.clusters[high], low)
            if offset is not None:
                return node.index(high, offset)
            return node.index(high, node.clusters[high].min)

        pred_cluster = None
        if node.summary and not node.summary.is_empty():
            pred_cluster = self._predecessor_recursive(node.summary, high)

        if pred_cluster is not None:
            offset = node.clusters[pred_cluster].max
            return node.index(pred_cluster, offset)

        if node.min is not None and x > node.min:
            return node.min

        return None

    def predecessor(self, x: int) -> Optional[int]:
        """Find predecessor of value.

        Args:
            x: Value to find predecessor for.

        Returns:
            Predecessor or None if not found.

        Raises:
            ValueError: If value is out of universe range.

        Time Complexity: O(log log U)
        """
        if x < 0 or x >= self.universe_size:
            raise ValueError(f"Value {x} out of universe range [0, {self.universe_size-1}]")

        if self.root.is_empty():
            return None

        result = self._predecessor_recursive(self.root, x)
        if result is not None:
            logger.info(f"Predecessor of {x}: {result}")
        else:
            logger.info(f"Predecessor of {x}: not found")
        return result

    def _successor_recursive(self, node: VEBNode, x: int) -> Optional[int]:
        """Recursively find successor.

        Args:
            node: Current node.
            x: Value to find successor for.

        Returns:
            Successor or None.
        """
        if node.is_empty():
            return None

        if node.max is not None and x >= node.max:
            return None

        if node.universe_size == 2:
            if x == 0 and node.max == 1:
                return 1
            return None

        high = node.high(x)
        low = node.low(x)

        if not node.clusters[high].is_empty() and low < node.clusters[high].max:
            offset = self._successor_recursive(node.clusters[high], low)
            if offset is not None:
                return node.index(high, offset)
            return node.index(high, node.clusters[high].max)

        succ_cluster = None
        if node.summary and not node.summary.is_empty():
            succ_cluster = self._successor_recursive(node.summary, high)

        if succ_cluster is not None:
            offset = node.clusters[succ_cluster].min
            return node.index(succ_cluster, offset)

        if node.max is not None and x < node.max:
            return node.max

        return None

    def successor(self, x: int) -> Optional[int]:
        """Find successor of value.

        Args:
            x: Value to find successor for.

        Returns:
            Successor or None if not found.

        Raises:
            ValueError: If value is out of universe range.

        Time Complexity: O(log log U)
        """
        if x < 0 or x >= self.universe_size:
            raise ValueError(f"Value {x} out of universe range [0, {self.universe_size-1}]")

        if self.root.is_empty():
            return None

        result = self._successor_recursive(self.root, x)
        if result is not None:
            logger.info(f"Successor of {x}: {result}")
        else:
            logger.info(f"Successor of {x}: not found")
        return result

    def is_empty(self) -> bool:
        """Check if tree is empty.

        Returns:
            True if empty, False otherwise.
        """
        return self.root.is_empty()

    def get_size(self) -> int:
        """Get number of elements in tree.

        Returns:
            Number of elements.
        """
        return self.size


def main() -> None:
    """Main function to demonstrate van Emde Boas tree operations."""
    tree = VanEmdeBoasTree(universe_size=16)

    print("Van Emde Boas Tree Operations Demo")
    print("=" * 50)

    values = [2, 3, 4, 5, 7, 14, 15]
    print(f"\nInserting values: {values}")
    for value in values:
        tree.insert(value)

    print(f"\nTree size: {tree.get_size()}")
    print(f"Minimum: {tree.get_min()}")
    print(f"Maximum: {tree.get_max()}")

    print("\nSearch operations:")
    for value in [3, 6, 7]:
        exists = tree.contains(value)
        print(f"Contains {value}: {exists}")

    print("\nPredecessor operations:")
    for value in [4, 6, 15]:
        pred = tree.predecessor(value)
        print(f"Predecessor of {value}: {pred}")

    print("\nSuccessor operations:")
    for value in [4, 6, 15]:
        succ = tree.successor(value)
        print(f"Successor of {value}: {succ}")

    print("\nDeleting value 5:")
    tree.delete(5)
    print(f"Tree size after deletion: {tree.get_size()}")
    print(f"Contains 5: {tree.contains(5)}")


if __name__ == "__main__":
    main()
