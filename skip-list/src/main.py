"""Skip List Data Structure with Probabilistic Balancing.

This module provides functionality to implement skip list data structure as an
alternative to balanced trees. Skip lists use probabilistic balancing to achieve
O(log n) average-case performance for search, insertion, and deletion operations.
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


class SkipListNode:
    """Node in skip list."""

    def __init__(self, key: int, value: Optional[int] = None, level: int = 0) -> None:
        """Initialize SkipListNode.

        Args:
            key: Node key value.
            value: Node value (optional).
            level: Maximum level for this node.
        """
        self.key = key
        self.value = value
        self.level = level
        self.forward: List[Optional["SkipListNode"]] = [None] * (level + 1)

    def __repr__(self) -> str:
        """String representation."""
        return f"SkipListNode(key={self.key}, level={self.level})"


class SkipList:
    """Skip list with probabilistic balancing."""

    def __init__(
        self,
        max_level: int = 16,
        probability: float = 0.5,
        config_path: str = "config.yaml",
    ) -> None:
        """Initialize skip list.

        Args:
            max_level: Maximum level for skip list.
            probability: Probability for level assignment (default: 0.5).
            config_path: Path to configuration YAML file.
        """
        if max_level < 1:
            raise ValueError("Max level must be at least 1")
        if not 0 < probability < 1:
            raise ValueError("Probability must be between 0 and 1")

        self.max_level = max_level
        self.probability = probability
        self.current_level = 0
        self._setup_logging()
        self.config = self._load_config(config_path)

        self.head = SkipListNode(-1, None, max_level)
        self.size = 0

        logger.info(
            f"Skip list initialized: max_level={max_level}, "
            f"probability={probability}"
        )

    def _setup_logging(self) -> None:
        """Configure logging for the application."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        log_file = log_dir / "skip_list.log"
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

    def _random_level(self) -> int:
        """Generate random level using probability.

        Returns:
            Random level (0 to max_level).
        """
        level = 0
        while random.random() < self.probability and level < self.max_level:
            level += 1
        return level

    def search(self, key: int) -> Tuple[bool, Optional[int]]:
        """Search for key in skip list.

        Args:
            key: Key to search for.

        Returns:
            Tuple of (found, value) where found is True if key exists.
        """
        logger.info(f"Searching for key: {key}")

        current = self.head

        for i in range(self.current_level, -1, -1):
            while (
                current.forward[i] is not None
                and current.forward[i].key < key
            ):
                current = current.forward[i]

        current = current.forward[0]

        if current is not None and current.key == key:
            logger.info(f"Key {key} found with value: {current.value}")
            return True, current.value

        logger.info(f"Key {key} not found")
        return False, None

    def insert(self, key: int, value: Optional[int] = None) -> bool:
        """Insert key-value pair into skip list.

        Args:
            key: Key to insert.
            value: Value to associate with key.

        Returns:
            True if insertion successful, False if key already exists.
        """
        logger.info(f"Inserting key: {key}, value: {value}")

        update: List[Optional[SkipListNode]] = [None] * (self.max_level + 1)
        current = self.head

        for i in range(self.current_level, -1, -1):
            while (
                current.forward[i] is not None
                and current.forward[i].key < key
            ):
                current = current.forward[i]
            update[i] = current

        current = current.forward[0]

        if current is not None and current.key == key:
            logger.warning(f"Key {key} already exists")
            return False

        new_level = self._random_level()

        if new_level > self.current_level:
            for i in range(self.current_level + 1, new_level + 1):
                update[i] = self.head
            self.current_level = new_level

        new_node = SkipListNode(key, value, new_level)

        for i in range(new_level + 1):
            new_node.forward[i] = update[i].forward[i]
            update[i].forward[i] = new_node

        self.size += 1
        logger.info(f"Successfully inserted key: {key} at level {new_level}")
        return True

    def delete(self, key: int) -> bool:
        """Delete key from skip list.

        Args:
            key: Key to delete.

        Returns:
            True if deletion successful, False if key not found.
        """
        logger.info(f"Deleting key: {key}")

        update: List[Optional[SkipListNode]] = [None] * (self.max_level + 1)
        current = self.head

        for i in range(self.current_level, -1, -1):
            while (
                current.forward[i] is not None
                and current.forward[i].key < key
            ):
                current = current.forward[i]
            update[i] = current

        current = current.forward[0]

        if current is None or current.key != key:
            logger.warning(f"Key {key} not found for deletion")
            return False

        for i in range(self.current_level + 1):
            if update[i].forward[i] != current:
                break
            update[i].forward[i] = current.forward[i]

        while (
            self.current_level > 0
            and self.head.forward[self.current_level] is None
        ):
            self.current_level -= 1

        self.size -= 1
        logger.info(f"Successfully deleted key: {key}")
        return True

    def get_size(self) -> int:
        """Get number of elements in skip list.

        Returns:
            Number of elements.
        """
        return self.size

    def get_current_level(self) -> int:
        """Get current maximum level.

        Returns:
            Current maximum level.
        """
        return self.current_level

    def is_empty(self) -> bool:
        """Check if skip list is empty.

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
        current = self.head.forward[0]

        while current is not None:
            keys.append(current.key)
            current = current.forward[0]

        return keys

    def get_all_items(self) -> List[Tuple[int, Optional[int]]]:
        """Get all key-value pairs in sorted order.

        Returns:
            List of (key, value) tuples.
        """
        items: List[Tuple[int, Optional[int]]] = []
        current = self.head.forward[0]

        while current is not None:
            items.append((current.key, current.value))
            current = current.forward[0]

        return items

    def get_range(
        self, start_key: int, end_key: int
    ) -> List[Tuple[int, Optional[int]]]:
        """Get all items with keys in range [start_key, end_key].

        Args:
            start_key: Start key (inclusive).
            end_key: End key (inclusive).

        Returns:
            List of (key, value) tuples in range.
        """
        if start_key > end_key:
            return []

        items: List[Tuple[int, Optional[int]]] = []
        current = self.head

        for i in range(self.current_level, -1, -1):
            while (
                current.forward[i] is not None
                and current.forward[i].key < start_key
            ):
                current = current.forward[i]

        current = current.forward[0]

        while current is not None and current.key <= end_key:
            items.append((current.key, current.value))
            current = current.forward[0]

        return items

    def get_min_key(self) -> Optional[int]:
        """Get minimum key.

        Returns:
            Minimum key, None if empty.
        """
        if self.is_empty():
            return None
        return self.head.forward[0].key

    def get_max_key(self) -> Optional[int]:
        """Get maximum key.

        Returns:
            Maximum key, None if empty.
        """
        if self.is_empty():
            return None

        current = self.head
        for i in range(self.current_level, -1, -1):
            while current.forward[i] is not None:
                current = current.forward[i]

        return current.key

    def clear(self) -> None:
        """Clear all elements from skip list."""
        self.head = SkipListNode(-1, None, self.max_level)
        self.current_level = 0
        self.size = 0
        logger.info("Skip list cleared")

    def is_valid(self) -> bool:
        """Validate skip list structure.

        Returns:
            True if valid, False otherwise.
        """
        if self.size == 0:
            return self.head.forward[0] is None

        keys = self.get_all_keys()
        if len(keys) != self.size:
            logger.error(f"Size mismatch: {len(keys)} != {self.size}")
            return False

        for i in range(len(keys) - 1):
            if keys[i] >= keys[i + 1]:
                logger.error(f"Keys not sorted: {keys[i]} >= {keys[i + 1]}")
                return False

        return True


def main() -> None:
    """Main function to demonstrate skip list operations."""
    skip_list = SkipList(max_level=4, probability=0.5)

    keys = [10, 20, 30, 40, 50, 25, 35, 15]
    logger.info("Inserting keys into skip list")
    for key in keys:
        skip_list.insert(key, key * 2)

    logger.info(f"Skip list size: {skip_list.get_size()}")
    logger.info(f"Current level: {skip_list.get_current_level()}")
    logger.info(f"Skip list is valid: {skip_list.is_valid()}")

    all_keys = skip_list.get_all_keys()
    logger.info(f"All keys: {all_keys}")

    logger.info("Searching for keys:")
    for key in [10, 25, 50, 100]:
        found, value = skip_list.search(key)
        logger.info(f"Key {key}: {'found' if found else 'not found'}")

    logger.info("Range query [20, 40]:")
    range_items = skip_list.get_range(20, 40)
    logger.info(f"Items: {range_items}")

    logger.info("Deleting key 30:")
    skip_list.delete(30)

    logger.info(f"Size after deletion: {skip_list.get_size()}")
    logger.info(f"All keys after deletion: {skip_list.get_all_keys()}")

    logger.info(f"Min key: {skip_list.get_min_key()}")
    logger.info(f"Max key: {skip_list.get_max_key()}")


if __name__ == "__main__":
    main()
