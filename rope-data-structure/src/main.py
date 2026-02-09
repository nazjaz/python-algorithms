"""Rope Data Structure for Efficient String Concatenation and Substring Operations.

This module provides functionality to implement rope data structure that efficiently
supports string concatenation, substring extraction, insertion, and deletion operations.
Ropes achieve O(log n) time complexity for most operations using a balanced binary tree.
"""

import logging
import logging.handlers
from pathlib import Path
from typing import Optional

import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class RopeNode:
    """Node in rope tree structure."""

    def __init__(
        self,
        data: Optional[str] = None,
        left: Optional["RopeNode"] = None,
        right: Optional["RopeNode"] = None,
        weight: int = 0,
    ) -> None:
        """Initialize rope node.

        Args:
            data: String data (for leaf nodes).
            left: Left child node.
            right: Right child node.
            weight: Weight (length of left subtree).
        """
        self.data = data
        self.left = left
        self.right = right
        self.weight = weight
        self.length = self._compute_length()

    def _compute_length(self) -> int:
        """Compute total length of subtree.

        Returns:
            Total length.
        """
        if self.data is not None:
            return len(self.data)
        left_len = self.left.length if self.left else 0
        right_len = self.right.length if self.right else 0
        return left_len + right_len

    def is_leaf(self) -> bool:
        """Check if node is a leaf.

        Returns:
            True if leaf, False otherwise.
        """
        return self.data is not None

    def update_weight(self) -> None:
        """Update weight based on left subtree."""
        if self.left:
            self.weight = self.left.length
        else:
            self.weight = 0

    def __repr__(self) -> str:
        """String representation."""
        if self.is_leaf():
            return f"RopeNode(data='{self.data[:20]}...' if len(self.data) > 20 else self.data)"
        return f"RopeNode(weight={self.weight}, length={self.length})"


class Rope:
    """Rope data structure for efficient string operations."""

    MAX_LEAF_LENGTH = 10

    def __init__(self, initial_string: str = "", config_path: str = "config.yaml") -> None:
        """Initialize rope.

        Args:
            initial_string: Initial string.
            config_path: Path to configuration file.
        """
        self.root: Optional[RopeNode] = None
        self._setup_logging()
        self._load_config(config_path)

        if initial_string:
            self.root = self._create_leaf(initial_string)
            logger.info(f"Created rope with string of length {len(initial_string)}")
        else:
            logger.info("Created empty rope")

    def _setup_logging(self) -> None:
        """Configure logging for rope operations."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        handler = logging.handlers.RotatingFileHandler(
            log_dir / "rope_data_structure.log",
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

    def _create_leaf(self, data: str) -> RopeNode:
        """Create a leaf node.

        Args:
            data: String data.

        Returns:
            Leaf node.
        """
        return RopeNode(data=data, weight=0)

    def _split(self, node: Optional[RopeNode], index: int) -> tuple[Optional[RopeNode], Optional[RopeNode]]:
        """Split rope at index.

        Args:
            node: Current node.
            index: Split index.

        Returns:
            Tuple of (left part, right part).
        """
        if node is None:
            return None, None

        if node.is_leaf():
            if index <= 0:
                return None, node
            if index >= len(node.data):
                return node, None

            left_data = node.data[:index]
            right_data = node.data[index:]
            return self._create_leaf(left_data), self._create_leaf(right_data)

        if index < node.weight:
            left_left, left_right = self._split(node.left, index)
            right_part = self._concatenate_nodes(left_right, node.right)
            return left_left, right_part
        else:
            right_left, right_right = self._split(node.right, index - node.weight)
            left_part = self._concatenate_nodes(node.left, right_left)
            return left_part, right_right

    def _concatenate_nodes(
        self, left: Optional[RopeNode], right: Optional[RopeNode]
    ) -> Optional[RopeNode]:
        """Concatenate two rope nodes.

        Args:
            left: Left node.
            right: Right node.

        Returns:
            Concatenated node.
        """
        if left is None:
            return right
        if right is None:
            return left

        if left.is_leaf() and right.is_leaf():
            combined = left.data + right.data
            if len(combined) <= self.MAX_LEAF_LENGTH:
                return self._create_leaf(combined)

        new_node = RopeNode(left=left, right=right)
        new_node.update_weight()
        return new_node

    def concatenate(self, other: "Rope") -> "Rope":
        """Concatenate this rope with another rope.

        Args:
            other: Other rope to concatenate.

        Returns:
            New rope containing concatenated result.
        """
        new_rope = Rope()
        new_rope.root = self._concatenate_nodes(self.root, other.root)
        logger.info("Concatenated two ropes")
        return new_rope

    def substring(self, start: int, end: int) -> "Rope":
        """Extract substring from rope.

        Args:
            start: Start index (inclusive).
            end: End index (exclusive).

        Returns:
            New rope containing substring.

        Raises:
            IndexError: If indices are invalid.
        """
        if start < 0 or end < 0 or start > end:
            raise IndexError(f"Invalid indices: [{start}, {end})")

        if self.root is None:
            if start == 0 and end == 0:
                return Rope()
            raise IndexError("Rope is empty")

        length = self.root.length
        if end > length:
            raise IndexError(f"End index {end} exceeds rope length {length}")

        left_part, middle_right = self._split(self.root, start)
        middle_part, right_part = self._split(middle_right, end - start)

        new_rope = Rope()
        new_rope.root = middle_part
        logger.info(f"Extracted substring [{start}, {end})")
        return new_rope

    def insert(self, index: int, string: str) -> "Rope":
        """Insert string at index.

        Args:
            index: Insertion index.
            string: String to insert.

        Returns:
            New rope with inserted string.

        Raises:
            IndexError: If index is invalid.
        """
        if index < 0:
            raise IndexError(f"Invalid index: {index}")

        if self.root is None:
            if index == 0:
                new_rope = Rope()
                new_rope.root = self._create_leaf(string)
                logger.info(f"Inserted string at index {index}")
                return new_rope
            raise IndexError(f"Index {index} out of bounds for empty rope")

        length = self.root.length
        if index > length:
            raise IndexError(f"Index {index} exceeds rope length {length}")

        left_part, right_part = self._split(self.root, index)
        new_node = self._create_leaf(string)
        new_root = self._concatenate_nodes(left_part, new_node)
        new_root = self._concatenate_nodes(new_root, right_part)

        new_rope = Rope()
        new_rope.root = new_root
        logger.info(f"Inserted string at index {index}")
        return new_rope

    def delete(self, start: int, end: int) -> "Rope":
        """Delete substring from rope.

        Args:
            start: Start index (inclusive).
            end: End index (exclusive).

        Returns:
            New rope with deleted substring.

        Raises:
            IndexError: If indices are invalid.
        """
        if start < 0 or end < 0 or start > end:
            raise IndexError(f"Invalid indices: [{start}, {end})")

        if self.root is None:
            if start == 0 and end == 0:
                return Rope()
            raise IndexError("Rope is empty")

        length = self.root.length
        if end > length:
            raise IndexError(f"End index {end} exceeds rope length {length}")

        left_part, middle_right = self._split(self.root, start)
        _, right_part = self._split(middle_right, end - start)

        new_rope = Rope()
        new_rope.root = self._concatenate_nodes(left_part, right_part)
        logger.info(f"Deleted substring [{start}, {end})")
        return new_rope

    def _to_string_recursive(self, node: Optional[RopeNode]) -> str:
        """Recursively convert rope to string.

        Args:
            node: Current node.

        Returns:
            String representation.
        """
        if node is None:
            return ""

        if node.is_leaf():
            return node.data

        left_str = self._to_string_recursive(node.left)
        right_str = self._to_string_recursive(node.right)
        return left_str + right_str

    def to_string(self) -> str:
        """Convert rope to string.

        Returns:
            String representation of rope.
        """
        result = self._to_string_recursive(self.root)
        logger.info(f"Converted rope to string (length: {len(result)})")
        return result

    def get_length(self) -> int:
        """Get length of rope.

        Returns:
            Length of rope.
        """
        if self.root is None:
            return 0
        return self.root.length

    def get_char(self, index: int) -> str:
        """Get character at index.

        Args:
            index: Character index.

        Returns:
            Character at index.

        Raises:
            IndexError: If index is invalid.
        """
        if self.root is None:
            raise IndexError("Rope is empty")

        if index < 0 or index >= self.root.length:
            raise IndexError(f"Index {index} out of bounds")

        node = self.root
        current_index = index

        while not node.is_leaf():
            if current_index < node.weight:
                node = node.left
            else:
                current_index -= node.weight
                node = node.right

        return node.data[current_index]


def main() -> None:
    """Main function to demonstrate rope data structure operations."""
    print("Rope Data Structure Operations Demo")
    print("=" * 50)

    print("\n=== Creating Ropes ===")
    rope1 = Rope("Hello")
    rope2 = Rope(" World")
    print(f"Rope1: '{rope1.to_string()}'")
    print(f"Rope2: '{rope2.to_string()}'")

    print("\n=== Concatenation ===")
    rope3 = rope1.concatenate(rope2)
    print(f"Concatenated: '{rope3.to_string()}'")

    print("\n=== Substring ===")
    substring = rope3.substring(0, 5)
    print(f"Substring [0, 5): '{substring.to_string()}'")

    print("\n=== Insert ===")
    rope4 = rope3.insert(5, " Beautiful")
    print(f"After insert: '{rope4.to_string()}'")

    print("\n=== Delete ===")
    rope5 = rope4.delete(5, 15)
    print(f"After delete: '{rope5.to_string()}'")

    print("\n=== Get Character ===")
    char = rope3.get_char(0)
    print(f"Character at index 0: '{char}'")


if __name__ == "__main__":
    main()
