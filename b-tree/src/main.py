"""B-Tree Data Structure Optimized for Disk-Based Storage.

This module provides functionality to implement B-tree data structure with
split and merge operations optimized for disk-based storage. B-trees are
self-balancing tree data structures that maintain sorted data and allow
efficient insertion, deletion, and search operations with minimal disk I/O.
"""

import logging
import logging.handlers
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class BTreeNode:
    """Node in B-tree."""

    def __init__(self, is_leaf: bool = False) -> None:
        """Initialize BTreeNode.

        Args:
            is_leaf: Whether this node is a leaf node.
        """
        self.keys: List[float] = []
        self.children: List[Optional["BTreeNode"]] = []
        self.is_leaf = is_leaf
        self.parent: Optional["BTreeNode"] = None

    def __repr__(self) -> str:
        """String representation."""
        return f"BTreeNode(keys={len(self.keys)}, is_leaf={self.is_leaf})"

    def is_full(self, min_degree: int) -> bool:
        """Check if node is full.

        Args:
            min_degree: Minimum degree of B-tree.

        Returns:
            True if node has maximum keys, False otherwise.
        """
        return len(self.keys) >= 2 * min_degree - 1

    def is_underfull(self, min_degree: int) -> bool:
        """Check if node is underfull.

        Args:
            min_degree: Minimum degree of B-tree.

        Returns:
            True if node has fewer than minimum keys, False otherwise.
        """
        return len(self.keys) < min_degree - 1


class BTree:
    """B-tree optimized for disk-based storage."""

    def __init__(
        self, min_degree: int = 3, config_path: str = "config.yaml"
    ) -> None:
        """Initialize BTree with configuration.

        Args:
            min_degree: Minimum degree of B-tree (default: 3).
            config_path: Path to configuration YAML file.
        """
        if min_degree < 2:
            raise ValueError("Minimum degree must be at least 2")
        self.min_degree = min_degree
        self._setup_logging()
        self.config = self._load_config(config_path)
        self.root: Optional[BTreeNode] = None
        self._disk_reads = 0
        self._disk_writes = 0
        logger.info(f"B-tree initialized with min_degree={min_degree}")

    def _setup_logging(self) -> None:
        """Configure logging for the application."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        log_file = log_dir / "b_tree.log"
        handler = logging.handlers.RotatingFileHandler(
            log_file, maxBytes=10485760, backupCount=5
        )
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)

        logger.setLevel(logging.INFO)
        logger.addHandler(handler)

    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file.

        Args:
            config_path: Path to configuration file.

        Returns:
            Configuration dictionary.

        Raises:
            FileNotFoundError: If configuration file does not exist.
        """
        try:
            with open(config_path, "r") as f:
                config = yaml.safe_load(f)
                logger.info(f"Configuration loaded from {config_path}")
                return config or {}
        except FileNotFoundError:
            logger.warning(f"Configuration file not found: {config_path}")
            return {}

    def _simulate_disk_read(self, node: Optional[BTreeNode]) -> None:
        """Simulate disk read operation.

        Args:
            node: Node being read from disk.
        """
        self._disk_reads += 1
        logger.debug(f"Disk read: {node}")

    def _simulate_disk_write(self, node: Optional[BTreeNode]) -> None:
        """Simulate disk write operation.

        Args:
            node: Node being written to disk.
        """
        self._disk_writes += 1
        logger.debug(f"Disk write: {node}")

    def get_disk_io_stats(self) -> Dict[str, int]:
        """Get disk I/O statistics.

        Returns:
            Dictionary with disk_reads and disk_writes counts.
        """
        return {
            "disk_reads": self._disk_reads,
            "disk_writes": self._disk_writes,
        }

    def reset_disk_io_stats(self) -> None:
        """Reset disk I/O statistics."""
        self._disk_reads = 0
        self._disk_writes = 0

    def search(self, key: float) -> Tuple[Optional[BTreeNode], Optional[int]]:
        """Search for key in B-tree.

        Args:
            key: Key value to search for.

        Returns:
            Tuple of (node, index) if found, (None, None) otherwise.
        """
        if self.root is None:
            return None, None

        return self._search_helper(self.root, key)

    def _search_helper(
        self, node: Optional[BTreeNode], key: float
    ) -> Tuple[Optional[BTreeNode], Optional[int]]:
        """Helper for search operation.

        Args:
            node: Current node.
            key: Key to search for.

        Returns:
            Tuple of (node, index) if found, (None, None) otherwise.
        """
        if node is None:
            return None, None

        self._simulate_disk_read(node)

        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1

        if i < len(node.keys) and key == node.keys[i]:
            return node, i

        if node.is_leaf:
            return None, None

        return self._search_helper(node.children[i], key)

    def insert(self, key: float) -> bool:
        """Insert key into B-tree.

        Args:
            key: Key value to insert.

        Returns:
            True if insertion successful, False if key already exists.
        """
        logger.info(f"Inserting key: {key}")

        if self.root is None:
            self.root = BTreeNode(is_leaf=True)
            self.root.keys.append(key)
            self._simulate_disk_write(self.root)
            logger.info(f"Successfully inserted key: {key} (root)")
            return True

        node, index = self.search(key)
        if node is not None:
            logger.warning(f"Key {key} already exists in tree")
            return False

        if self.root.is_full(self.min_degree):
            old_root = self.root
            self.root = BTreeNode(is_leaf=False)
            self.root.children.append(old_root)
            old_root.parent = self.root
            self._split_child(self.root, 0)
            self._simulate_disk_write(self.root)

        self._insert_non_full(self.root, key)
        logger.info(f"Successfully inserted key: {key}")
        return True

    def _insert_non_full(self, node: BTreeNode, key: float) -> None:
        """Insert key into non-full node.

        Args:
            node: Node to insert into.
            key: Key value to insert.
        """
        i = len(node.keys) - 1

        if node.is_leaf:
            while i >= 0 and key < node.keys[i]:
                i -= 1
            node.keys.insert(i + 1, key)
            self._simulate_disk_write(node)
        else:
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1

            self._simulate_disk_read(node.children[i])
            if node.children[i].is_full(self.min_degree):
                self._split_child(node, i)
                if key > node.keys[i]:
                    i += 1

            self._insert_non_full(node.children[i], key)

    def _split_child(self, parent: BTreeNode, index: int) -> None:
        """Split full child node.

        Args:
            parent: Parent node.
            index: Index of child to split.
        """
        full_child = parent.children[index]
        new_child = BTreeNode(is_leaf=full_child.is_leaf)
        new_child.parent = parent

        mid_key = full_child.keys[self.min_degree - 1]
        new_child.keys = full_child.keys[self.min_degree:]
        full_child.keys = full_child.keys[: self.min_degree - 1]

        if not full_child.is_leaf:
            new_child.children = full_child.children[self.min_degree:]
            full_child.children = full_child.children[: self.min_degree]
            for child in new_child.children:
                if child:
                    child.parent = new_child

        parent.keys.insert(index, mid_key)
        parent.children.insert(index + 1, new_child)

        self._simulate_disk_write(full_child)
        self._simulate_disk_write(new_child)
        self._simulate_disk_write(parent)

        logger.debug(
            f"Split child at index {index}, "
            f"mid_key={mid_key}, "
            f"parent_keys={len(parent.keys)}"
        )

    def delete(self, key: float) -> bool:
        """Delete key from B-tree.

        Args:
            key: Key value to delete.

        Returns:
            True if deletion successful, False if key not found.
        """
        logger.info(f"Deleting key: {key}")

        if self.root is None:
            logger.warning(f"Key {key} not found in empty tree")
            return False

        node, index = self.search(key)
        if node is None:
            logger.warning(f"Key {key} not found in tree")
            return False

        self._delete_key(node, key)

        if len(self.root.keys) == 0:
            if self.root.is_leaf:
                self.root = None
            else:
                self.root = self.root.children[0]
                if self.root:
                    self.root.parent = None
            self._simulate_disk_write(self.root)

        logger.info(f"Successfully deleted key: {key}")
        return True

    def _delete_key(self, node: BTreeNode, key: float) -> None:
        """Delete key from node.

        Args:
            node: Node containing key.
            key: Key to delete.
        """
        index = node.keys.index(key)

        if node.is_leaf:
            node.keys.remove(key)
            self._simulate_disk_write(node)
        else:
            left_child = node.children[index]
            right_child = node.children[index + 1]

            self._simulate_disk_read(left_child)
            self._simulate_disk_read(right_child)

            if len(left_child.keys) >= self.min_degree:
                predecessor = self._get_predecessor(left_child)
                node.keys[index] = predecessor
                self._delete_key(left_child, predecessor)
            elif len(right_child.keys) >= self.min_degree:
                successor = self._get_successor(right_child)
                node.keys[index] = successor
                self._delete_key(right_child, successor)
            else:
                self._merge_children(node, index)
                merged_child = node.children[index]
                self._simulate_disk_read(merged_child)
                self._delete_key(merged_child, key)

    def _get_predecessor(self, node: BTreeNode) -> float:
        """Get predecessor key (largest key in left subtree).

        Args:
            node: Starting node.

        Returns:
            Predecessor key value.
        """
        while not node.is_leaf:
            node = node.children[-1]
            self._simulate_disk_read(node)
        return node.keys[-1]

    def _get_successor(self, node: BTreeNode) -> float:
        """Get successor key (smallest key in right subtree).

        Args:
            node: Starting node.

        Returns:
            Successor key value.
        """
        while not node.is_leaf:
            node = node.children[0]
            self._simulate_disk_read(node)
        return node.keys[0]

    def _merge_children(self, parent: BTreeNode, index: int) -> None:
        """Merge two children nodes.

        Args:
            parent: Parent node.
            index: Index of left child to merge.
        """
        left_child = parent.children[index]
        right_child = parent.children[index + 1]

        left_child.keys.append(parent.keys[index])
        left_child.keys.extend(right_child.keys)

        if not left_child.is_leaf:
            left_child.children.extend(right_child.children)
            for child in right_child.children:
                if child:
                    child.parent = left_child

        parent.keys.pop(index)
        parent.children.pop(index + 1)

        self._simulate_disk_write(left_child)
        self._simulate_disk_write(parent)

        logger.debug(
            f"Merged children at index {index}, "
            f"parent_keys={len(parent.keys)}"
        )

    def _borrow_from_left_sibling(
        self, parent: BTreeNode, index: int
    ) -> None:
        """Borrow key from left sibling.

        Args:
            parent: Parent node.
            index: Index of child needing key.
        """
        child = parent.children[index]
        left_sibling = parent.children[index - 1]

        child.keys.insert(0, parent.keys[index - 1])
        parent.keys[index - 1] = left_sibling.keys.pop()

        if not child.is_leaf:
            child.children.insert(0, left_sibling.children.pop())
            if child.children[0]:
                child.children[0].parent = child

        self._simulate_disk_write(child)
        self._simulate_disk_write(left_sibling)
        self._simulate_disk_write(parent)

    def _borrow_from_right_sibling(
        self, parent: BTreeNode, index: int
    ) -> None:
        """Borrow key from right sibling.

        Args:
            parent: Parent node.
            index: Index of child needing key.
        """
        child = parent.children[index]
        right_sibling = parent.children[index + 1]

        child.keys.append(parent.keys[index])
        parent.keys[index] = right_sibling.keys.pop(0)

        if not child.is_leaf:
            child.children.append(right_sibling.children.pop(0))
            if child.children[-1]:
                child.children[-1].parent = child

        self._simulate_disk_write(child)
        self._simulate_disk_write(right_sibling)
        self._simulate_disk_write(parent)

    def _ensure_minimum_keys(self, node: BTreeNode, index: int) -> None:
        """Ensure node has minimum keys by borrowing or merging.

        Args:
            node: Parent node.
            index: Index of child to check.
        """
        child = node.children[index]

        if child.is_underfull(self.min_degree):
            left_sibling = (
                node.children[index - 1] if index > 0 else None
            )
            right_sibling = (
                node.children[index + 1]
                if index < len(node.children) - 1
                else None
            )

            if (
                left_sibling
                and len(left_sibling.keys) >= self.min_degree
            ):
                self._borrow_from_left_sibling(node, index)
            elif (
                right_sibling
                and len(right_sibling.keys) >= self.min_degree
            ):
                self._borrow_from_right_sibling(node, index)
            elif left_sibling:
                self._merge_children(node, index - 1)
            elif right_sibling:
                self._merge_children(node, index)

    def inorder_traversal(self) -> List[float]:
        """Perform inorder traversal of tree.

        Returns:
            List of keys in sorted order.
        """
        result: List[float] = []
        if self.root:
            self._inorder_helper(self.root, result)
        return result

    def _inorder_helper(
        self, node: BTreeNode, result: List[float]
    ) -> None:
        """Helper for inorder traversal.

        Args:
            node: Current node.
            result: List to append keys to.
        """
        self._simulate_disk_read(node)

        for i in range(len(node.keys)):
            if not node.is_leaf:
                self._inorder_helper(node.children[i], result)
            result.append(node.keys[i])

        if not node.is_leaf:
            self._inorder_helper(node.children[-1], result)

    def get_height(self) -> int:
        """Calculate tree height.

        Returns:
            Height of tree (number of levels).
        """
        if self.root is None:
            return 0
        return self._height_helper(self.root)

    def _height_helper(self, node: BTreeNode) -> int:
        """Helper to calculate height.

        Args:
            node: Current node.

        Returns:
            Height of subtree.
        """
        if node.is_leaf:
            return 1
        return 1 + self._height_helper(node.children[0])

    def get_size(self) -> int:
        """Get number of keys in tree.

        Returns:
            Number of keys.
        """
        if self.root is None:
            return 0
        return self._size_helper(self.root)

    def _size_helper(self, node: BTreeNode) -> int:
        """Helper to count keys.

        Args:
            node: Current node.

        Returns:
            Number of keys in subtree.
        """
        count = len(node.keys)
        if not node.is_leaf:
            for child in node.children:
                if child:
                    count += self._size_helper(child)
        return count

    def is_valid(self) -> bool:
        """Validate B-tree properties.

        Returns:
            True if tree satisfies all B-tree properties.
        """
        if self.root is None:
            return True

        valid, _ = self._check_leaf_levels(self.root, 0)
        return (
            self._check_root_property()
            and self._check_node_properties(self.root)
            and valid
        )

    def _check_root_property(self) -> bool:
        """Check root has at least one key (unless empty).

        Returns:
            True if root property satisfied.
        """
        if self.root is None:
            return True
        if len(self.root.keys) == 0 and not self.root.is_leaf:
            logger.error("Root has no keys and is not leaf")
            return False
        return True

    def _check_node_properties(self, node: BTreeNode) -> bool:
        """Check node properties.

        Args:
            node: Node to check.

        Returns:
            True if properties satisfied.
        """
        if node is None:
            return True

        if node != self.root:
            if node.is_underfull(self.min_degree):
                logger.error(
                    f"Node has {len(node.keys)} keys, "
                    f"minimum is {self.min_degree - 1}"
                )
                return False

        if len(node.keys) > 2 * self.min_degree - 1:
            logger.error(
                f"Node has {len(node.keys)} keys, "
                f"maximum is {2 * self.min_degree - 1}"
            )
            return False

        if not node.is_leaf:
            if len(node.children) != len(node.keys) + 1:
                logger.error(
                    f"Node has {len(node.keys)} keys but "
                    f"{len(node.children)} children"
                )
                return False

            for child in node.children:
                if child:
                    if not self._check_node_properties(child):
                        return False

        return True

    def _check_leaf_levels(
        self, node: BTreeNode, level: int
    ) -> Tuple[bool, int]:
        """Check all leaves are at same level.

        Args:
            node: Current node.
            level: Current level.

        Returns:
            Tuple of (is_valid, leaf_level).
        """
        if node.is_leaf:
            return True, level

        leaf_levels: List[int] = []
        for child in node.children:
            if child:
                valid, leaf_level = self._check_leaf_levels(
                    child, level + 1
                )
                if not valid:
                    return False, -1
                leaf_levels.append(leaf_level)

        if len(set(leaf_levels)) > 1:
            logger.error(
                f"Leaves at different levels: {set(leaf_levels)}"
            )
            return False, -1

        return True, leaf_levels[0] if leaf_levels else level


def main() -> None:
    """Main function to demonstrate B-tree operations."""
    tree = BTree(min_degree=3)

    keys = [
        10, 20, 5, 6, 12, 30, 7, 17, 3, 8, 15, 25, 35, 40, 50, 60, 70, 80,
        90, 100,
    ]
    logger.info("Inserting keys into B-tree")
    for key in keys:
        tree.insert(key)

    logger.info(f"Tree size: {tree.get_size()}")
    logger.info(f"Tree height: {tree.get_height()}")
    logger.info(f"Tree is valid: {tree.is_valid()}")

    io_stats = tree.get_disk_io_stats()
    logger.info(
        f"Disk I/O: reads={io_stats['disk_reads']}, "
        f"writes={io_stats['disk_writes']}"
    )

    logger.info("Inorder traversal:")
    inorder = tree.inorder_traversal()
    logger.info(f"Keys: {inorder[:10]}... (showing first 10)")

    logger.info("Searching for key 25:")
    node, index = tree.search(25)
    found = node is not None
    logger.info(f"Found: {found}")

    logger.info("Deleting key 25:")
    tree.delete(25)

    logger.info(f"Tree size after deletion: {tree.get_size()}")
    logger.info(f"Tree is valid after deletion: {tree.is_valid()}")

    final_io_stats = tree.get_disk_io_stats()
    logger.info(
        f"Final Disk I/O: reads={final_io_stats['disk_reads']}, "
        f"writes={final_io_stats['disk_writes']}"
    )


if __name__ == "__main__":
    main()
