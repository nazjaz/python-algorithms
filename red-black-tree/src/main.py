"""Red-Black Tree Data Structure.

This module provides functionality to implement red-black tree data structure
with insertion, deletion, and rebalancing operations. Red-black trees are
self-balancing binary search trees that maintain balance through color coding
and rotation operations, ensuring O(log n) operations for all operations.
"""

import logging
import logging.handlers
import time
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional

import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class Color(Enum):
    """Node color enumeration."""

    RED = "RED"
    BLACK = "BLACK"


class RedBlackNode:
    """Node in red-black tree."""

    def __init__(
        self,
        key: float,
        color: Color = Color.RED,
        parent: Optional["RedBlackNode"] = None,
    ) -> None:
        """Initialize RedBlackNode.

        Args:
            key: Node key value.
            color: Node color (default: RED).
            parent: Parent node reference.
        """
        self.key = key
        self.color = color
        self.parent = parent
        self.left: Optional["RedBlackNode"] = None
        self.right: Optional["RedBlackNode"] = None

    def __repr__(self) -> str:
        """String representation."""
        return f"RedBlackNode(key={self.key}, color={self.color.value})"

    def is_red(self) -> bool:
        """Check if node is red.

        Returns:
            True if node is red, False otherwise.
        """
        return self.color == Color.RED

    def is_black(self) -> bool:
        """Check if node is black.

        Returns:
            True if node is black, False otherwise.
        """
        return self.color == Color.BLACK


class RedBlackTree:
    """Red-black tree (self-balancing binary search tree)."""

    def __init__(self, config_path: str = "config.yaml") -> None:
        """Initialize RedBlackTree with configuration.

        Args:
            config_path: Path to configuration YAML file.
        """
        self._setup_logging()
        self.config = self._load_config(config_path)
        self.root: Optional[RedBlackNode] = None
        self.nil = RedBlackNode(0, Color.BLACK)
        self.nil.left = self.nil
        self.nil.right = self.nil
        self.nil.parent = self.nil
        logger.info("Red-black tree initialized")

    def _setup_logging(self) -> None:
        """Configure logging for the application."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        log_file = log_dir / "red_black_tree.log"
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

    def insert(self, key: float) -> bool:
        """Insert key into red-black tree.

        Args:
            key: Key value to insert.

        Returns:
            True if insertion successful, False if key already exists.
        """
        logger.info(f"Inserting key: {key}")
        new_node = RedBlackNode(key, Color.RED, self.nil)
        new_node.left = self.nil
        new_node.right = self.nil

        parent = self.nil
        current = self.root

        while current != self.nil and current is not None:
            parent = current
            if key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
            else:
                logger.warning(f"Key {key} already exists in tree")
                return False

        new_node.parent = parent

        if parent == self.nil:
            self.root = new_node
        elif key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        self._insert_fixup(new_node)
        logger.info(f"Successfully inserted key: {key}")
        return True

    def _insert_fixup(self, node: RedBlackNode) -> None:
        """Fix red-black tree properties after insertion.

        Args:
            node: Newly inserted node to fix.
        """
        while node.parent.is_red():
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right
                if uncle.is_red():
                    node.parent.color = Color.BLACK
                    uncle.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self._left_rotate(node)
                    node.parent.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    self._right_rotate(node.parent.parent)
            else:
                uncle = node.parent.parent.left
                if uncle.is_red():
                    node.parent.color = Color.BLACK
                    uncle.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self._right_rotate(node)
                    node.parent.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    self._left_rotate(node.parent.parent)

        self.root.color = Color.BLACK

    def delete(self, key: float) -> bool:
        """Delete key from red-black tree.

        Args:
            key: Key value to delete.

        Returns:
            True if deletion successful, False if key not found.
        """
        logger.info(f"Deleting key: {key}")
        node = self._search_node(key)
        if node == self.nil or node is None:
            logger.warning(f"Key {key} not found in tree")
            return False

        original_color = node.color
        fixup_node: Optional[RedBlackNode] = None

        if node.left == self.nil:
            fixup_node = node.right
            self._transplant(node, node.right)
        elif node.right == self.nil:
            fixup_node = node.left
            self._transplant(node, node.left)
        else:
            successor = self._minimum(node.right)
            original_color = successor.color
            fixup_node = successor.right

            if successor.parent == node:
                if fixup_node:
                    fixup_node.parent = successor
            else:
                self._transplant(successor, successor.right)
                successor.right = node.right
                if successor.right:
                    successor.right.parent = successor

            self._transplant(node, successor)
            successor.left = node.left
            if successor.left:
                successor.left.parent = successor
            successor.color = node.color

        if original_color == Color.BLACK and fixup_node:
            self._delete_fixup(fixup_node)

        logger.info(f"Successfully deleted key: {key}")
        return True

    def _delete_fixup(self, node: RedBlackNode) -> None:
        """Fix red-black tree properties after deletion.

        Args:
            node: Node to fix up.
        """
        while node != self.root and node.is_black():
            if node == node.parent.left:
                sibling = node.parent.right
                if sibling.is_red():
                    sibling.color = Color.BLACK
                    node.parent.color = Color.RED
                    self._left_rotate(node.parent)
                    sibling = node.parent.right

                if (
                    sibling
                    and sibling.left
                    and sibling.right
                    and sibling.left.is_black()
                    and sibling.right.is_black()
                ):
                    sibling.color = Color.RED
                    node = node.parent
                else:
                    if sibling and sibling.right and sibling.right.is_black():
                        if sibling.left:
                            sibling.left.color = Color.BLACK
                        sibling.color = Color.RED
                        self._right_rotate(sibling)
                        sibling = node.parent.right

                    if sibling:
                        sibling.color = node.parent.color
                    node.parent.color = Color.BLACK
                    if sibling and sibling.right:
                        sibling.right.color = Color.BLACK
                    self._left_rotate(node.parent)
                    node = self.root
            else:
                sibling = node.parent.left
                if sibling and sibling.is_red():
                    sibling.color = Color.BLACK
                    node.parent.color = Color.RED
                    self._right_rotate(node.parent)
                    sibling = node.parent.left

                if (
                    sibling
                    and sibling.left
                    and sibling.right
                    and sibling.left.is_black()
                    and sibling.right.is_black()
                ):
                    if sibling:
                        sibling.color = Color.RED
                    node = node.parent
                else:
                    if sibling and sibling.left and sibling.left.is_black():
                        if sibling.right:
                            sibling.right.color = Color.BLACK
                        if sibling:
                            sibling.color = Color.RED
                        self._left_rotate(sibling)
                        sibling = node.parent.left

                    if sibling:
                        sibling.color = node.parent.color
                    node.parent.color = Color.BLACK
                    if sibling and sibling.left:
                        sibling.left.color = Color.BLACK
                    self._right_rotate(node.parent)
                    node = self.root

        node.color = Color.BLACK

    def _transplant(
        self, u: RedBlackNode, v: Optional[RedBlackNode]
    ) -> None:
        """Replace subtree rooted at u with subtree rooted at v.

        Args:
            u: Node to be replaced.
            v: Node to replace u.
        """
        if v is None:
            v = self.nil

        if u.parent == self.nil:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v

        v.parent = u.parent

    def _left_rotate(self, node: RedBlackNode) -> None:
        """Perform left rotation around node.

        Args:
            node: Node to rotate around.
        """
        right_child = node.right
        if right_child is None:
            return

        node.right = right_child.left
        if right_child.left != self.nil:
            right_child.left.parent = node

        right_child.parent = node.parent

        if node.parent == self.nil:
            self.root = right_child
        elif node == node.parent.left:
            node.parent.left = right_child
        else:
            node.parent.right = right_child

        right_child.left = node
        node.parent = right_child

    def _right_rotate(self, node: RedBlackNode) -> None:
        """Perform right rotation around node.

        Args:
            node: Node to rotate around.
        """
        left_child = node.left
        if left_child is None:
            return

        node.left = left_child.right
        if left_child.right != self.nil:
            left_child.right.parent = node

        left_child.parent = node.parent

        if node.parent == self.nil:
            self.root = left_child
        elif node == node.parent.right:
            node.parent.right = left_child
        else:
            node.parent.left = left_child

        left_child.right = node
        node.parent = left_child

    def search(self, key: float) -> bool:
        """Search for key in red-black tree.

        Args:
            key: Key value to search for.

        Returns:
            True if key found, False otherwise.
        """
        node = self._search_node(key)
        found = node != self.nil and node is not None
        logger.info(f"Search for key {key}: {'found' if found else 'not found'}")
        return found

    def _search_node(self, key: float) -> Optional[RedBlackNode]:
        """Search for node with given key.

        Args:
            key: Key value to search for.

        Returns:
            Node if found, None or nil otherwise.
        """
        current = self.root
        while current != self.nil and current is not None:
            if key == current.key:
                return current
            elif key < current.key:
                current = current.left
            else:
                current = current.right
        return self.nil

    def _minimum(self, node: RedBlackNode) -> RedBlackNode:
        """Find minimum node in subtree.

        Args:
            node: Root of subtree.

        Returns:
            Minimum node.
        """
        while node.left != self.nil and node.left is not None:
            node = node.left
        return node

    def inorder_traversal(self) -> List[float]:
        """Perform inorder traversal of tree.

        Returns:
            List of keys in sorted order.
        """
        result: List[float] = []
        self._inorder_helper(self.root, result)
        return result

    def _inorder_helper(
        self, node: Optional[RedBlackNode], result: List[float]
    ) -> None:
        """Helper for inorder traversal.

        Args:
            node: Current node.
            result: List to append keys to.
        """
        if node != self.nil and node is not None:
            self._inorder_helper(node.left, result)
            result.append(node.key)
            self._inorder_helper(node.right, result)

    def preorder_traversal(self) -> List[float]:
        """Perform preorder traversal of tree.

        Returns:
            List of keys in preorder.
        """
        result: List[float] = []
        self._preorder_helper(self.root, result)
        return result

    def _preorder_helper(
        self, node: Optional[RedBlackNode], result: List[float]
    ) -> None:
        """Helper for preorder traversal.

        Args:
            node: Current node.
            result: List to append keys to.
        """
        if node != self.nil and node is not None:
            result.append(node.key)
            self._preorder_helper(node.left, result)
            self._preorder_helper(node.right, result)

    def postorder_traversal(self) -> List[float]:
        """Perform postorder traversal of tree.

        Returns:
            List of keys in postorder.
        """
        result: List[float] = []
        self._postorder_helper(self.root, result)
        return result

    def _postorder_helper(
        self, node: Optional[RedBlackNode], result: List[float]
    ) -> None:
        """Helper for postorder traversal.

        Args:
            node: Current node.
            result: List to append keys to.
        """
        if node != self.nil and node is not None:
            self._postorder_helper(node.left, result)
            self._postorder_helper(node.right, result)
            result.append(node.key)

    def height(self) -> int:
        """Calculate tree height.

        Returns:
            Height of tree.
        """
        return self._height_helper(self.root)

    def _height_helper(self, node: Optional[RedBlackNode]) -> int:
        """Helper to calculate height.

        Args:
            node: Current node.

        Returns:
            Height of subtree.
        """
        if node == self.nil or node is None:
            return 0
        return 1 + max(
            self._height_helper(node.left), self._height_helper(node.right)
        )

    def is_valid(self) -> bool:
        """Validate red-black tree properties.

        Returns:
            True if tree satisfies all red-black properties.
        """
        if self.root is None:
            return True

        if self.root.is_red():
            logger.error("Root node must be black")
            return False

        return (
            self._check_black_height(self.root) != -1
            and self._check_no_double_red(self.root)
        )

    def _check_black_height(self, node: Optional[RedBlackNode]) -> int:
        """Check black height property.

        Args:
            node: Current node.

        Returns:
            Black height if valid, -1 otherwise.
        """
        if node == self.nil or node is None:
            return 1

        left_height = self._check_black_height(node.left)
        right_height = self._check_black_height(node.right)

        if left_height == -1 or right_height == -1:
            return -1

        if left_height != right_height:
            logger.error(
                f"Black height mismatch at node {node.key}: "
                f"left={left_height}, right={right_height}"
            )
            return -1

        return left_height + (1 if node.is_black() else 0)

    def _check_no_double_red(self, node: Optional[RedBlackNode]) -> bool:
        """Check no double red property.

        Args:
            node: Current node.

        Returns:
            True if no double red violations.
        """
        if node == self.nil or node is None:
            return True

        if node.is_red():
            if (
                (node.left and node.left.is_red())
                or (node.right and node.right.is_red())
            ):
                logger.error(f"Double red violation at node {node.key}")
                return False

        return self._check_no_double_red(node.left) and self._check_no_double_red(
            node.right
        )

    def get_size(self) -> int:
        """Get number of nodes in tree.

        Returns:
            Number of nodes.
        """
        return self._size_helper(self.root)

    def _size_helper(self, node: Optional[RedBlackNode]) -> int:
        """Helper to count nodes.

        Args:
            node: Current node.

        Returns:
            Number of nodes in subtree.
        """
        if node == self.nil or node is None:
            return 0
        return (
            1
            + self._size_helper(node.left)
            + self._size_helper(node.right)
        )


def main() -> None:
    """Main function to demonstrate red-black tree operations."""
    tree = RedBlackTree()

    keys = [7, 3, 18, 10, 22, 8, 11, 26, 2, 6, 13]
    logger.info("Inserting keys into red-black tree")
    for key in keys:
        tree.insert(key)

    logger.info(f"Tree size: {tree.get_size()}")
    logger.info(f"Tree height: {tree.height()}")
    logger.info(f"Tree is valid: {tree.is_valid()}")

    logger.info("Inorder traversal:")
    inorder = tree.inorder_traversal()
    logger.info(f"Keys: {inorder}")

    logger.info("Searching for key 10:")
    found = tree.search(10)
    logger.info(f"Found: {found}")

    logger.info("Deleting key 18:")
    tree.delete(18)

    logger.info(f"Tree size after deletion: {tree.get_size()}")
    logger.info(f"Tree is valid after deletion: {tree.is_valid()}")

    logger.info("Inorder traversal after deletion:")
    inorder_after = tree.inorder_traversal()
    logger.info(f"Keys: {inorder_after}")


if __name__ == "__main__":
    main()
