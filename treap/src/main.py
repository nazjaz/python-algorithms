"""Treap (Tree + Heap) Data Structure with Randomized Balancing.

This module provides functionality to implement treap data structure that
combines binary search tree and heap properties. Treaps use randomized
priorities to maintain balanced structure, achieving O(log n) expected
time complexity for all operations.
"""

import logging
import logging.handlers
import random
from pathlib import Path
from typing import List, Optional, Tuple

import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class TreapNode:
    """Node in treap."""

    def __init__(self, key: int, priority: Optional[int] = None) -> None:
        """Initialize TreapNode.

        Args:
            key: Node key value.
            priority: Node priority (random if None).
        """
        self.key = key
        self.priority = priority if priority is not None else random.randint(1, 10**9)
        self.left: Optional["TreapNode"] = None
        self.right: Optional["TreapNode"] = None

    def __repr__(self) -> str:
        """String representation."""
        return f"TreapNode(key={self.key}, priority={self.priority})"


class Treap:
    """Treap (tree + heap) with randomized balancing."""

    def __init__(self, config_path: str = "config.yaml") -> None:
        """Initialize treap.

        Args:
            config_path: Path to configuration YAML file.
        """
        self.root: Optional[TreapNode] = None
        self.size = 0
        self._setup_logging()
        self.config = self._load_config(config_path)
        logger.info("Treap initialized")

    def _setup_logging(self) -> None:
        """Configure logging for the application."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        log_file = log_dir / "treap.log"
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

    def _right_rotate(self, node: TreapNode) -> TreapNode:
        """Perform right rotation.

        Args:
            node: Node to rotate.

        Returns:
            New root after rotation.
        """
        left_child = node.left
        node.left = left_child.right
        left_child.right = node
        return left_child

    def _left_rotate(self, node: TreapNode) -> TreapNode:
        """Perform left rotation.

        Args:
            node: Node to rotate.

        Returns:
            New root after rotation.
        """
        right_child = node.right
        node.right = right_child.left
        right_child.left = node
        return right_child

    def _insert_node(
        self, node: Optional[TreapNode], key: int, priority: Optional[int] = None
    ) -> TreapNode:
        """Insert node recursively.

        Args:
            node: Current node.
            key: Key to insert.
            priority: Priority for new node (random if None).

        Returns:
            Root of subtree after insertion.
        """
        if node is None:
            return TreapNode(key, priority)

        if key < node.key:
            node.left = self._insert_node(node.left, key, priority)
            if node.left.priority > node.priority:
                node = self._right_rotate(node)
        elif key > node.key:
            node.right = self._insert_node(node.right, key, priority)
            if node.right.priority > node.priority:
                node = self._left_rotate(node)
        else:
            logger.warning(f"Key {key} already exists, updating priority")
            node.priority = priority if priority is not None else node.priority

        return node

    def insert(self, key: int, priority: Optional[int] = None) -> bool:
        """Insert key into treap.

        Args:
            key: Key to insert.
            priority: Priority for new node (random if None).

        Returns:
            True if insertion successful, False if key already exists.
        """
        logger.info(f"Inserting key: {key}")

        if self.search(key):
            logger.warning(f"Key {key} already exists")
            return False

        self.root = self._insert_node(self.root, key, priority)
        self.size += 1
        logger.info(f"Successfully inserted key: {key}")
        return True

    def _delete_node(self, node: Optional[TreapNode], key: int) -> Optional[TreapNode]:
        """Delete node recursively.

        Args:
            node: Current node.
            key: Key to delete.

        Returns:
            Root of subtree after deletion.
        """
        if node is None:
            return None

        if key < node.key:
            node.left = self._delete_node(node.left, key)
        elif key > node.key:
            node.right = self._delete_node(node.right, key)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            else:
                if node.left.priority > node.right.priority:
                    node = self._right_rotate(node)
                    node.right = self._delete_node(node.right, key)
                else:
                    node = self._left_rotate(node)
                    node.left = self._delete_node(node.left, key)

        return node

    def delete(self, key: int) -> bool:
        """Delete key from treap.

        Args:
            key: Key to delete.

        Returns:
            True if deletion successful, False if key not found.
        """
        logger.info(f"Deleting key: {key}")

        if not self.search(key):
            logger.warning(f"Key {key} not found for deletion")
            return False

        self.root = self._delete_node(self.root, key)
        self.size -= 1
        logger.info(f"Successfully deleted key: {key}")
        return True

    def _search_node(self, node: Optional[TreapNode], key: int) -> Optional[TreapNode]:
        """Search for key recursively.

        Args:
            node: Current node.
            key: Key to search for.

        Returns:
            Node if found, None otherwise.
        """
        if node is None or node.key == key:
            return node

        if key < node.key:
            return self._search_node(node.left, key)
        else:
            return self._search_node(node.right, key)

    def search(self, key: int) -> bool:
        """Search for key in treap.

        Args:
            key: Key to search for.

        Returns:
            True if key found, False otherwise.
        """
        node = self._search_node(self.root, key)
        return node is not None

    def _split(
        self, node: Optional[TreapNode], key: int
    ) -> Tuple[Optional[TreapNode], Optional[TreapNode]]:
        """Split treap at key.

        Args:
            node: Root of treap to split.
            key: Split key.

        Returns:
            Tuple of (left_treap, right_treap).
        """
        if node is None:
            return None, None

        if key < node.key:
            left, node.left = self._split(node.left, key)
            return left, node
        else:
            node.right, right = self._split(node.right, key)
            return node, right

    def split(self, key: int) -> Tuple["Treap", "Treap"]:
        """Split treap into two treaps at key.

        Args:
            key: Split key.

        Returns:
            Tuple of (left_treap, right_treap).
        """
        logger.info(f"Splitting treap at key: {key}")
        left_root, right_root = self._split(self.root, key)

        left_treap = Treap()
        left_treap.root = left_root
        left_treap.size = self._count_nodes(left_root)

        right_treap = Treap()
        right_treap.root = right_root
        right_treap.size = self._count_nodes(right_root)

        return left_treap, right_treap

    def _merge(
        self, left: Optional[TreapNode], right: Optional[TreapNode]
    ) -> Optional[TreapNode]:
        """Merge two treaps.

        Args:
            left: Root of left treap.
            right: Root of right treap.

        Returns:
            Root of merged treap.
        """
        if left is None:
            return right
        if right is None:
            return left

        if left.priority > right.priority:
            left.right = self._merge(left.right, right)
            return left
        else:
            right.left = self._merge(left, right.left)
            return right

    def merge(self, other: "Treap") -> "Treap":
        """Merge this treap with another treap.

        Args:
            other: Treap to merge with.

        Returns:
            New merged treap.
        """
        logger.info("Merging two treaps")
        merged = Treap()
        merged.root = self._merge(self.root, other.root)
        merged.size = self.size + other.size
        return merged

    def _count_nodes(self, node: Optional[TreapNode]) -> int:
        """Count nodes in subtree.

        Args:
            node: Root of subtree.

        Returns:
            Number of nodes.
        """
        if node is None:
            return 0
        return 1 + self._count_nodes(node.left) + self._count_nodes(node.right)

    def get_size(self) -> int:
        """Get number of elements in treap.

        Returns:
            Number of elements.
        """
        return self.size

    def is_empty(self) -> bool:
        """Check if treap is empty.

        Returns:
            True if empty, False otherwise.
        """
        return self.size == 0

    def get_all_keys(self) -> List[int]:
        """Get all keys in sorted order.

        Returns:
            List of all keys.
        """
        keys: List[int] = []

        def inorder(node: Optional[TreapNode]) -> None:
            if node:
                inorder(node.left)
                keys.append(node.key)
                inorder(node.right)

        inorder(self.root)
        return keys

    def get_min_key(self) -> Optional[int]:
        """Get minimum key.

        Returns:
            Minimum key, None if empty.
        """
        if self.is_empty():
            return None

        node = self.root
        while node.left:
            node = node.left
        return node.key

    def get_max_key(self) -> Optional[int]:
        """Get maximum key.

        Returns:
            Maximum key, None if empty.
        """
        if self.is_empty():
            return None

        node = self.root
        while node.right:
            node = node.right
        return node.key

    def clear(self) -> None:
        """Clear all elements from treap."""
        self.root = None
        self.size = 0
        logger.info("Treap cleared")

    def is_valid(self) -> bool:
        """Validate treap structure.

        Returns:
            True if valid, False otherwise.
        """
        def validate(node: Optional[TreapNode], min_val: int, max_val: int) -> bool:
            if node is None:
                return True

            if not (min_val < node.key < max_val):
                logger.error(f"BST property violated at key {node.key}")
                return False

            if node.left and node.left.priority > node.priority:
                logger.error(f"Heap property violated: left child priority > node priority")
                return False

            if node.right and node.right.priority > node.priority:
                logger.error(f"Heap property violated: right child priority > node priority")
                return False

            return (validate(node.left, min_val, node.key) and
                    validate(node.right, node.key, max_val))

        return validate(self.root, float('-inf'), float('inf'))


def main() -> None:
    """Main function to demonstrate treap operations."""
    treap = Treap()

    keys = [10, 20, 30, 40, 50, 25, 35, 15]
    logger.info("Inserting keys into treap")
    for key in keys:
        treap.insert(key)

    logger.info(f"Treap size: {treap.get_size()}")
    logger.info(f"Treap is valid: {treap.is_valid()}")

    all_keys = treap.get_all_keys()
    logger.info(f"All keys: {all_keys}")

    logger.info("Searching for keys:")
    for key in [10, 25, 50, 100]:
        found = treap.search(key)
        logger.info(f"Key {key}: {'found' if found else 'not found'}")

    logger.info("Splitting treap at key 30:")
    left, right = treap.split(30)
    logger.info(f"Left treap keys: {left.get_all_keys()}")
    logger.info(f"Right treap keys: {right.get_all_keys()}")

    logger.info("Merging treaps:")
    merged = left.merge(right)
    logger.info(f"Merged treap keys: {merged.get_all_keys()}")

    logger.info("Deleting key 30:")
    treap.delete(30)

    logger.info(f"Size after deletion: {treap.get_size()}")
    logger.info(f"All keys after deletion: {treap.get_all_keys()}")

    logger.info(f"Min key: {treap.get_min_key()}")
    logger.info(f"Max key: {treap.get_max_key()}")


if __name__ == "__main__":
    main()
