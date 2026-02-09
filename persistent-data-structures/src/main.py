"""Persistent Data Structures (Persistent Arrays, Lists) with Path Copying Technique.

This module provides functionality to implement persistent arrays and lists using
path copying technique. Persistent data structures maintain all previous versions
when modified, enabling efficient time-travel queries and undo operations.
Path copying achieves O(log n) time and space complexity per operation.
"""

import logging
import logging.handlers
from pathlib import Path
from typing import Any, List, Optional

import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class PersistentNode:
    """Node in persistent tree structure."""

    def __init__(
        self,
        left: Optional["PersistentNode"] = None,
        right: Optional["PersistentNode"] = None,
        value: Any = None,
        size: int = 0,
    ) -> None:
        """Initialize persistent node.

        Args:
            left: Left child node.
            right: Right child node.
            value: Value stored in leaf node.
            size: Size of subtree.
        """
        self.left = left
        self.right = right
        self.value = value
        self.size = size

    def is_leaf(self) -> bool:
        """Check if node is a leaf.

        Returns:
            True if leaf, False otherwise.
        """
        return self.left is None and self.right is None

    def copy(self) -> "PersistentNode":
        """Create a copy of this node.

        Returns:
            New node with same structure.
        """
        return PersistentNode(
            left=self.left,
            right=self.right,
            value=self.value,
            size=self.size,
        )


class PersistentArray:
    """Persistent array with path copying technique."""

    def __init__(
        self, initial_data: Optional[List[Any]] = None, config_path: str = "config.yaml"
    ) -> None:
        """Initialize persistent array.

        Args:
            initial_data: Initial array data.
            config_path: Path to configuration file.
        """
        self.versions: List[PersistentNode] = []
        self._setup_logging()
        self._load_config(config_path)

        if initial_data:
            self.versions.append(self._build_tree(initial_data, 0, len(initial_data)))
            logger.info(f"Created persistent array with {len(initial_data)} elements")
        else:
            self.versions.append(None)
            logger.info("Created empty persistent array")

    def _setup_logging(self) -> None:
        """Configure logging for persistent array operations."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        handler = logging.handlers.RotatingFileHandler(
            log_dir / "persistent_data_structures.log",
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

    def _build_tree(
        self, data: List[Any], left: int, right: int
    ) -> Optional[PersistentNode]:
        """Build tree from array data.

        Args:
            data: Array data.
            left: Left index.
            right: Right index.

        Returns:
            Root node of tree.
        """
        if left >= right:
            return None

        if left == right - 1:
            return PersistentNode(value=data[left], size=1)

        mid = (left + right) // 2
        left_node = self._build_tree(data, left, mid)
        right_node = self._build_tree(data, mid, right)

        size = (left_node.size if left_node else 0) + (
            right_node.size if right_node else 0
        )

        return PersistentNode(left=left_node, right=right_node, size=size)

    def _get_recursive(self, node: Optional[PersistentNode], index: int, left: int, right: int) -> Any:
        """Recursively get value at index.

        Args:
            node: Current node.
            index: Target index.
            left: Left bound of current range.
            right: Right bound of current range.

        Returns:
            Value at index.

        Raises:
            IndexError: If index is out of bounds.
        """
        if node is None:
            raise IndexError(f"Index {index} out of bounds")

        if node.is_leaf():
            if left == index:
                return node.value
            raise IndexError(f"Index {index} out of bounds")

        mid = (left + right) // 2
        left_size = node.left.size if node.left else 0

        if index < left + left_size:
            return self._get_recursive(node.left, index, left, mid)
        else:
            return self._get_recursive(node.right, index, mid, right)

    def get(self, version: int, index: int) -> Any:
        """Get value at index in specific version.

        Args:
            version: Version number.
            index: Index to get.

        Returns:
            Value at index.

        Raises:
            IndexError: If version or index is invalid.
        """
        if version < 0 or version >= len(self.versions):
            raise IndexError(f"Version {version} does not exist")

        root = self.versions[version]
        if root is None:
            raise IndexError("Array is empty")

        size = root.size
        result = self._get_recursive(root, index, 0, size)
        logger.info(f"Get version {version}, index {index}: {result}")
        return result

    def _set_recursive(
        self,
        node: Optional[PersistentNode],
        index: int,
        value: Any,
        left: int,
        right: int,
    ) -> PersistentNode:
        """Recursively set value at index with path copying.

        Args:
            node: Current node.
            index: Target index.
            value: New value.
            left: Left bound of current range.
            right: Right bound of current range.

        Returns:
            New node with updated value.
        """
        if node is None:
            raise IndexError(f"Index {index} out of bounds")

        if node.is_leaf():
            if left == index:
                new_node = node.copy()
                new_node.value = value
                return new_node
            raise IndexError(f"Index {index} out of bounds")

        new_node = node.copy()
        mid = (left + right) // 2
        left_size = node.left.size if node.left else 0

        if index < left + left_size:
            new_node.left = self._set_recursive(node.left, index, value, left, mid)
        else:
            new_node.right = self._set_recursive(
                node.right, index, value, mid, right
            )

        return new_node

    def set(self, version: int, index: int, value: Any) -> int:
        """Set value at index in specific version, creating new version.

        Args:
            version: Version number to base on.
            index: Index to set.
            value: New value.

        Returns:
            New version number.

        Raises:
            IndexError: If version or index is invalid.
        """
        if version < 0 or version >= len(self.versions):
            raise IndexError(f"Version {version} does not exist")

        root = self.versions[version]
        if root is None:
            raise IndexError("Array is empty")

        size = root.size
        new_root = self._set_recursive(root, index, value, 0, size)
        self.versions.append(new_root)
        new_version = len(self.versions) - 1
        logger.info(f"Set version {version}, index {index} = {value}, new version: {new_version}")
        return new_version

    def get_current_version(self) -> int:
        """Get current version number.

        Returns:
            Current version number.
        """
        return len(self.versions) - 1

    def get_size(self, version: int) -> int:
        """Get size of array in specific version.

        Args:
            version: Version number.

        Returns:
            Size of array.

        Raises:
            IndexError: If version is invalid.
        """
        if version < 0 or version >= len(self.versions):
            raise IndexError(f"Version {version} does not exist")

        root = self.versions[version]
        return root.size if root else 0


class PersistentList:
    """Persistent list with path copying technique."""

    def __init__(
        self, initial_data: Optional[List[Any]] = None, config_path: str = "config.yaml"
    ) -> None:
        """Initialize persistent list.

        Args:
            initial_data: Initial list data.
            config_path: Path to configuration file.
        """
        self.versions: List[PersistentNode] = []
        self._setup_logging()
        self._load_config(config_path)

        if initial_data:
            self.versions.append(self._build_tree(initial_data, 0, len(initial_data)))
            logger.info(f"Created persistent list with {len(initial_data)} elements")
        else:
            self.versions.append(None)
            logger.info("Created empty persistent list")

    def _setup_logging(self) -> None:
        """Configure logging for persistent list operations."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        handler = logging.handlers.RotatingFileHandler(
            log_dir / "persistent_data_structures.log",
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

    def _build_tree(
        self, data: List[Any], left: int, right: int
    ) -> Optional[PersistentNode]:
        """Build tree from list data.

        Args:
            data: List data.
            left: Left index.
            right: Right index.

        Returns:
            Root node of tree.
        """
        if left >= right:
            return None

        if left == right - 1:
            return PersistentNode(value=data[left], size=1)

        mid = (left + right) // 2
        left_node = self._build_tree(data, left, mid)
        right_node = self._build_tree(data, mid, right)

        size = (left_node.size if left_node else 0) + (
            right_node.size if right_node else 0
        )

        return PersistentNode(left=left_node, right=right_node, size=size)

    def _get_recursive(
        self, node: Optional[PersistentNode], index: int, left: int, right: int
    ) -> Any:
        """Recursively get value at index.

        Args:
            node: Current node.
            index: Target index.
            left: Left bound of current range.
            right: Right bound of current range.

        Returns:
            Value at index.

        Raises:
            IndexError: If index is out of bounds.
        """
        if node is None:
            raise IndexError(f"Index {index} out of bounds")

        if node.is_leaf():
            if left == index:
                return node.value
            raise IndexError(f"Index {index} out of bounds")

        mid = (left + right) // 2
        left_size = node.left.size if node.left else 0

        if index < left + left_size:
            return self._get_recursive(node.left, index, left, mid)
        else:
            return self._get_recursive(node.right, index, mid, right)

    def get(self, version: int, index: int) -> Any:
        """Get value at index in specific version.

        Args:
            version: Version number.
            index: Index to get.

        Returns:
            Value at index.

        Raises:
            IndexError: If version or index is invalid.
        """
        if version < 0 or version >= len(self.versions):
            raise IndexError(f"Version {version} does not exist")

        root = self.versions[version]
        if root is None:
            raise IndexError("List is empty")

        size = root.size
        result = self._get_recursive(root, index, 0, size)
        logger.info(f"Get version {version}, index {index}: {result}")
        return result

    def _set_recursive(
        self,
        node: Optional[PersistentNode],
        index: int,
        value: Any,
        left: int,
        right: int,
    ) -> PersistentNode:
        """Recursively set value at index with path copying.

        Args:
            node: Current node.
            index: Target index.
            value: New value.
            left: Left bound of current range.
            right: Right bound of current range.

        Returns:
            New node with updated value.
        """
        if node is None:
            raise IndexError(f"Index {index} out of bounds")

        if node.is_leaf():
            if left == index:
                new_node = node.copy()
                new_node.value = value
                return new_node
            raise IndexError(f"Index {index} out of bounds")

        new_node = node.copy()
        mid = (left + right) // 2
        left_size = node.left.size if node.left else 0

        if index < left + left_size:
            new_node.left = self._set_recursive(node.left, index, value, left, mid)
        else:
            new_node.right = self._set_recursive(
                node.right, index, value, mid, right
            )

        return new_node

    def set(self, version: int, index: int, value: Any) -> int:
        """Set value at index in specific version, creating new version.

        Args:
            version: Version number to base on.
            index: Index to set.
            value: New value.

        Returns:
            New version number.

        Raises:
            IndexError: If version or index is invalid.
        """
        if version < 0 or version >= len(self.versions):
            raise IndexError(f"Version {version} does not exist")

        root = self.versions[version]
        if root is None:
            raise IndexError("List is empty")

        size = root.size
        new_root = self._set_recursive(root, index, value, 0, size)
        self.versions.append(new_root)
        new_version = len(self.versions) - 1
        logger.info(f"Set version {version}, index {index} = {value}, new version: {new_version}")
        return new_version

    def _append_recursive(
        self, node: Optional[PersistentNode], value: Any, left: int, right: int
    ) -> PersistentNode:
        """Recursively append value with path copying.

        Args:
            node: Current node.
            value: Value to append.
            left: Left bound of current range.
            right: Right bound of current range.

        Returns:
            New node with appended value.
        """
        if node is None:
            return PersistentNode(value=value, size=1)

        if node.is_leaf():
            new_node = PersistentNode(
                left=node.copy(),
                right=PersistentNode(value=value, size=1),
                size=node.size + 1,
            )
            return new_node

        new_node = node.copy()
        mid = (left + right) // 2
        new_node.right = self._append_recursive(node.right, value, mid, right)
        new_node.size = (new_node.left.size if new_node.left else 0) + (
            new_node.right.size if new_node.right else 0
        )
        return new_node

    def append(self, version: int, value: Any) -> int:
        """Append value to list in specific version, creating new version.

        Args:
            version: Version number to base on.
            value: Value to append.

        Returns:
            New version number.

        Raises:
            IndexError: If version is invalid.
        """
        if version < 0 or version >= len(self.versions):
            raise IndexError(f"Version {version} does not exist")

        root = self.versions[version]
        if root is None:
            new_root = PersistentNode(value=value, size=1)
        else:
            size = root.size
            new_root = self._append_recursive(root, value, 0, size)

        self.versions.append(new_root)
        new_version = len(self.versions) - 1
        logger.info(f"Append to version {version}, value {value}, new version: {new_version}")
        return new_version

    def get_current_version(self) -> int:
        """Get current version number.

        Returns:
            Current version number.
        """
        return len(self.versions) - 1

    def get_size(self, version: int) -> int:
        """Get size of list in specific version.

        Args:
            version: Version number.

        Returns:
            Size of list.

        Raises:
            IndexError: If version is invalid.
        """
        if version < 0 or version >= len(self.versions):
            raise IndexError(f"Version {version} does not exist")

        root = self.versions[version]
        return root.size if root else 0


def main() -> None:
    """Main function to demonstrate persistent data structures."""
    print("Persistent Data Structures Demo")
    print("=" * 50)

    print("\n=== Persistent Array ===")
    arr = PersistentArray([1, 2, 3, 4, 5])
    v0 = arr.get_current_version()

    print(f"Version {v0}: {[arr.get(v0, i) for i in range(arr.get_size(v0))]}")

    v1 = arr.set(v0, 2, 10)
    print(f"Version {v1}: {[arr.get(v1, i) for i in range(arr.get_size(v1))]}")

    v2 = arr.set(v1, 0, 20)
    print(f"Version {v2}: {[arr.get(v2, i) for i in range(arr.get_size(v2))]}")

    print(f"Original version {v0} still intact: {[arr.get(v0, i) for i in range(arr.get_size(v0))]}")

    print("\n=== Persistent List ===")
    lst = PersistentList([10, 20, 30])
    v0 = lst.get_current_version()

    print(f"Version {v0}: {[lst.get(v0, i) for i in range(lst.get_size(v0))]}")

    v1 = lst.append(v0, 40)
    print(f"Version {v1}: {[lst.get(v1, i) for i in range(lst.get_size(v1))]}")

    v2 = lst.set(v1, 1, 25)
    print(f"Version {v2}: {[lst.get(v2, i) for i in range(lst.get_size(v2))]}")

    print(f"Version {v0} still intact: {[lst.get(v0, i) for i in range(lst.get_size(v0))]}")
    print(f"Version {v1} still intact: {[lst.get(v1, i) for i in range(lst.get_size(v1))]}")


if __name__ == "__main__":
    main()
