"""Splay Tree with Amortized Analysis and Self-Adjusting Operations.

This module provides functionality to implement splay tree data structure
that automatically moves recently accessed elements to the root through
splay operations. Splay trees achieve O(log n) amortized time complexity
for all operations through self-adjusting rotations.
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


class SplayNode:
    """Node in splay tree."""

    def __init__(self, key: int) -> None:
        """Initialize SplayNode.

        Args:
            key: Node key value.
        """
        self.key = key
        self.left: Optional["SplayNode"] = None
        self.right: Optional["SplayNode"] = None
        self.parent: Optional["SplayNode"] = None

    def __repr__(self) -> str:
        """String representation."""
        return f"SplayNode(key={self.key})"


class SplayTree:
    """Splay tree with amortized analysis and self-adjusting operations."""

    def __init__(self, config_path: str = "config.yaml") -> None:
        """Initialize splay tree.

        Args:
            config_path: Path to configuration file.
        """
        self.root: Optional[SplayNode] = None
        self.operation_count = 0
        self.total_rotations = 0
        self.total_splay_operations = 0
        self._setup_logging()
        self._load_config(config_path)

    def _setup_logging(self) -> None:
        """Configure logging for splay tree operations."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        handler = logging.handlers.RotatingFileHandler(
            log_dir / "splay_tree.log",
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

    def _zig(self, node: SplayNode) -> None:
        """Perform zig rotation (single right rotation).

        Args:
            node: Node to rotate.
        """
        parent = node.parent
        if parent is None:
            return

        if parent.left == node:
            parent.left = node.right
            if node.right:
                node.right.parent = parent
            node.right = parent
        else:
            parent.right = node.left
            if node.left:
                node.left.parent = parent
            node.left = parent

        grandparent = parent.parent
        parent.parent = node
        node.parent = grandparent

        if grandparent:
            if grandparent.left == parent:
                grandparent.left = node
            else:
                grandparent.right = node
        else:
            self.root = node

        self.total_rotations += 1

    def _zig_zig(self, node: SplayNode) -> None:
        """Perform zig-zig rotation (two same-direction rotations).

        Args:
            node: Node to rotate.
        """
        parent = node.parent
        if parent is None:
            return

        grandparent = parent.parent
        if grandparent is None:
            return

        if parent.left == node and grandparent.left == parent:
            grandparent.left = parent.right
            if parent.right:
                parent.right.parent = grandparent

            parent.right = grandparent
            parent.left = node.right
            if node.right:
                node.right.parent = parent

            node.right = parent
        else:
            grandparent.right = parent.left
            if parent.left:
                parent.left.parent = grandparent

            parent.left = grandparent
            parent.right = node.left
            if node.left:
                node.left.parent = parent

            node.left = parent

        parent.parent = node
        node.parent = grandparent.parent

        if grandparent.parent:
            if grandparent.parent.left == grandparent:
                grandparent.parent.left = node
            else:
                grandparent.parent.right = node
        else:
            self.root = node

        grandparent.parent = parent
        self.total_rotations += 2

    def _zig_zag(self, node: SplayNode) -> None:
        """Perform zig-zag rotation (two opposite-direction rotations).

        Args:
            node: Node to rotate.
        """
        parent = node.parent
        if parent is None:
            return

        grandparent = parent.parent
        if grandparent is None:
            return

        if parent.right == node and grandparent.left == parent:
            grandparent.left = node.right
            if node.right:
                node.right.parent = grandparent

            parent.right = node.left
            if node.left:
                node.left.parent = parent

            node.left = parent
            node.right = grandparent
        else:
            grandparent.right = node.left
            if node.left:
                node.left.parent = grandparent

            parent.left = node.right
            if node.right:
                node.right.parent = parent

            node.right = parent
            node.left = grandparent

        parent.parent = node
        grandparent.parent = node
        node.parent = grandparent.parent

        if grandparent.parent:
            if grandparent.parent.left == grandparent:
                grandparent.parent.left = node
            else:
                grandparent.parent.right = node
        else:
            self.root = node

        self.total_rotations += 2

    def _splay(self, node: SplayNode) -> None:
        """Splay node to root using appropriate rotations.

        Args:
            node: Node to splay to root.
        """
        self.total_splay_operations += 1

        while node.parent is not None:
            parent = node.parent
            grandparent = parent.parent

            if grandparent is None:
                self._zig(node)
            elif (parent.left == node and grandparent.left == parent) or (
                parent.right == node and grandparent.right == parent
            ):
                self._zig_zig(node)
            else:
                self._zig_zag(node)

            logger.debug(f"Splayed node {node.key}")

    def insert(self, key: int) -> bool:
        """Insert key into splay tree.

        Args:
            key: Key to insert.

        Returns:
            True if inserted, False if already exists.
        """
        self.operation_count += 1

        if self.root is None:
            self.root = SplayNode(key)
            logger.info(f"Inserted root node: {key}")
            return True

        current = self.root
        parent = None

        while current:
            if current.key == key:
                self._splay(current)
                logger.info(f"Key {key} already exists, splayed to root")
                return False

            parent = current
            if key < current.key:
                current = current.left
            else:
                current = current.right

        new_node = SplayNode(key)
        new_node.parent = parent

        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        self._splay(new_node)
        logger.info(f"Inserted and splayed node: {key}")
        return True

    def search(self, key: int) -> Optional[SplayNode]:
        """Search for key in splay tree and splay to root.

        Args:
            key: Key to search for.

        Returns:
            Node if found, None otherwise.
        """
        self.operation_count += 1

        if self.root is None:
            logger.info(f"Search failed: tree is empty")
            return None

        current = self.root
        last_visited = None

        while current:
            last_visited = current
            if current.key == key:
                self._splay(current)
                logger.info(f"Found and splayed key: {key}")
                return current
            elif key < current.key:
                current = current.left
            else:
                current = current.right

        if last_visited:
            self._splay(last_visited)
            logger.info(f"Key {key} not found, splayed last visited node")

        return None

    def _find_max(self, node: SplayNode) -> SplayNode:
        """Find maximum node in subtree.

        Args:
            node: Root of subtree.

        Returns:
            Maximum node.
        """
        while node.right:
            node = node.right
        return node

    def _find_min(self, node: SplayNode) -> SplayNode:
        """Find minimum node in subtree.

        Args:
            node: Root of subtree.

        Returns:
            Minimum node.
        """
        while node.left:
            node = node.left
        return node

    def delete(self, key: int) -> bool:
        """Delete key from splay tree.

        Args:
            key: Key to delete.

        Returns:
            True if deleted, False if not found.
        """
        self.operation_count += 1

        node = self.search(key)
        if node is None:
            logger.info(f"Delete failed: key {key} not found")
            return False

        if node.left is None:
            self.root = node.right
            if self.root:
                self.root.parent = None
        elif node.right is None:
            self.root = node.left
            if self.root:
                self.root.parent = None
        else:
            left_subtree = node.left
            right_subtree = node.right

            max_left = self._find_max(left_subtree)
            self._splay(max_left)

            self.root.right = right_subtree
            if right_subtree:
                right_subtree.parent = self.root

        logger.info(f"Deleted key: {key}")
        return True

    def find_min(self) -> Optional[int]:
        """Find minimum key in tree.

        Returns:
            Minimum key or None if tree is empty.
        """
        if self.root is None:
            return None

        min_node = self._find_min(self.root)
        self._splay(min_node)
        logger.info(f"Found minimum: {min_node.key}")
        return min_node.key

    def find_max(self) -> Optional[int]:
        """Find maximum key in tree.

        Returns:
            Maximum key or None if tree is empty.
        """
        if self.root is None:
            return None

        max_node = self._find_max(self.root)
        self._splay(max_node)
        logger.info(f"Found maximum: {max_node.key}")
        return max_node.key

    def inorder_traversal(self) -> List[int]:
        """Perform inorder traversal of tree.

        Returns:
            List of keys in sorted order.
        """
        result = []

        def _inorder(node: Optional[SplayNode]) -> None:
            if node:
                _inorder(node.left)
                result.append(node.key)
                _inorder(node.right)

        _inorder(self.root)
        return result

    def preorder_traversal(self) -> List[int]:
        """Perform preorder traversal of tree.

        Returns:
            List of keys in preorder.
        """
        result = []

        def _preorder(node: Optional[SplayNode]) -> None:
            if node:
                result.append(node.key)
                _preorder(node.left)
                _preorder(node.right)

        _preorder(self.root)
        return result

    def postorder_traversal(self) -> List[int]:
        """Perform postorder traversal of tree.

        Returns:
            List of keys in postorder.
        """
        result = []

        def _postorder(node: Optional[SplayNode]) -> None:
            if node:
                _postorder(node.left)
                _postorder(node.right)
                result.append(node.key)

        _postorder(self.root)
        return result

    def get_amortized_analysis(self) -> dict:
        """Get amortized analysis statistics.

        Returns:
            Dictionary with analysis metrics.
        """
        avg_rotations = (
            self.total_rotations / self.total_splay_operations
            if self.total_splay_operations > 0
            else 0
        )

        return {
            "total_operations": self.operation_count,
            "total_splay_operations": self.total_splay_operations,
            "total_rotations": self.total_rotations,
            "average_rotations_per_splay": round(avg_rotations, 2),
            "amortized_cost_per_operation": round(
                self.total_rotations / self.operation_count
                if self.operation_count > 0
                else 0,
                2,
            ),
        }

    def reset_statistics(self) -> None:
        """Reset all operation statistics."""
        self.operation_count = 0
        self.total_rotations = 0
        self.total_splay_operations = 0
        logger.info("Statistics reset")

    def size(self) -> int:
        """Get number of nodes in tree.

        Returns:
            Number of nodes.
        """
        return len(self.inorder_traversal())

    def is_empty(self) -> bool:
        """Check if tree is empty.

        Returns:
            True if empty, False otherwise.
        """
        return self.root is None


def main() -> None:
    """Main function to demonstrate splay tree operations."""
    tree = SplayTree()

    print("Splay Tree Operations Demo")
    print("=" * 50)

    keys = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45]
    print(f"\nInserting keys: {keys}")
    for key in keys:
        tree.insert(key)

    print(f"\nInorder traversal: {tree.inorder_traversal()}")
    print(f"Tree size: {tree.size()}")

    print("\nSearching for key 25:")
    result = tree.search(25)
    if result:
        print(f"Found: {result.key}")

    print("\nFinding min and max:")
    print(f"Minimum: {tree.find_min()}")
    print(f"Maximum: {tree.find_max()}")

    print("\nDeleting key 30:")
    tree.delete(30)
    print(f"Inorder traversal after deletion: {tree.inorder_traversal()}")

    print("\nAmortized Analysis:")
    analysis = tree.get_amortized_analysis()
    for key, value in analysis.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
