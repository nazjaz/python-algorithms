"""Hash Table Implementation - Chaining and Open Addressing.

This module provides hash table implementations with two collision handling
methods: chaining (separate chaining) and open addressing (linear probing).
It includes comprehensive operations and performance comparison.
"""

import argparse
import logging
import logging.handlers
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class HashTableChaining:
    """Hash table implementation using chaining for collision resolution."""

    def __init__(self, initial_capacity: int = 11) -> None:
        """Initialize hash table with chaining.

        Args:
            initial_capacity: Initial capacity of hash table.
        """
        self.capacity = initial_capacity
        self.size = 0
        self.buckets: List[List[Tuple[Any, Any]]] = [[] for _ in range(self.capacity)]
        self.load_factor_threshold = 0.75
        logger.debug(f"Initialized hash table with chaining (capacity: {self.capacity})")

    def _hash(self, key: Any) -> int:
        """Compute hash value for key.

        Args:
            key: Key to hash.

        Returns:
            Hash value (index in table).
        """
        # Use Python's built-in hash function and modulo
        return hash(key) % self.capacity

    def _resize(self) -> None:
        """Resize hash table when load factor exceeds threshold."""
        logger.info(f"Resizing hash table (current size: {self.size}, capacity: {self.capacity})")
        old_buckets = self.buckets
        self.capacity *= 2
        self.size = 0
        self.buckets = [[] for _ in range(self.capacity)]

        # Rehash all existing key-value pairs
        for bucket in old_buckets:
            for key, value in bucket:
                self.insert(key, value)

        logger.debug(f"Resized to capacity: {self.capacity}")

    def insert(self, key: Any, value: Any) -> None:
        """Insert key-value pair into hash table.

        Args:
            key: Key to insert.
            value: Value to associate with key.
        """
        logger.debug(f"Inserting key: {key}, value: {value}")

        index = self._hash(key)
        bucket = self.buckets[index]

        # Check if key already exists
        for i, (k, v) in enumerate(bucket):
            if k == key:
                # Update existing key
                bucket[i] = (key, value)
                logger.debug(f"Updated existing key: {key}")
                return

        # Add new key-value pair
        bucket.append((key, value))
        self.size += 1
        logger.debug(f"Inserted new key: {key}")

        # Check load factor and resize if necessary
        load_factor = self.size / self.capacity
        if load_factor > self.load_factor_threshold:
            self._resize()

    def get(self, key: Any) -> Optional[Any]:
        """Get value associated with key.

        Args:
            key: Key to search for.

        Returns:
            Value associated with key, or None if not found.
        """
        logger.debug(f"Getting value for key: {key}")

        index = self._hash(key)
        bucket = self.buckets[index]

        for k, v in bucket:
            if k == key:
                logger.debug(f"Found key: {key}, value: {v}")
                return v

        logger.debug(f"Key not found: {key}")
        return None

    def delete(self, key: Any) -> bool:
        """Delete key-value pair from hash table.

        Args:
            key: Key to delete.

        Returns:
            True if key was deleted, False if not found.
        """
        logger.debug(f"Deleting key: {key}")

        index = self._hash(key)
        bucket = self.buckets[index]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self.size -= 1
                logger.debug(f"Deleted key: {key}")
                return True

        logger.debug(f"Key not found for deletion: {key}")
        return False

    def contains(self, key: Any) -> bool:
        """Check if key exists in hash table.

        Args:
            key: Key to check.

        Returns:
            True if key exists, False otherwise.
        """
        return self.get(key) is not None

    def get_load_factor(self) -> float:
        """Get current load factor.

        Returns:
            Load factor (size / capacity).
        """
        return self.size / self.capacity if self.capacity > 0 else 0.0

    def visualize(self) -> str:
        """Generate visual representation of hash table.

        Returns:
            String representation of hash table structure.
        """
        lines = []
        lines.append("Hash Table (Chaining):")
        lines.append("=" * 50)

        for i, bucket in enumerate(self.buckets):
            if bucket:
                bucket_str = " -> ".join(f"({k}:{v})" for k, v in bucket)
                lines.append(f"Index {i}: {bucket_str}")
            else:
                lines.append(f"Index {i}: (empty)")

        lines.append("=" * 50)
        lines.append(f"Size: {self.size}, Capacity: {self.capacity}, "
                    f"Load Factor: {self.get_load_factor():.2f}")

        return "\n".join(lines)


class HashTableOpenAddressing:
    """Hash table implementation using open addressing (linear probing)."""

    def __init__(self, initial_capacity: int = 11) -> None:
        """Initialize hash table with open addressing.

        Args:
            initial_capacity: Initial capacity of hash table.
        """
        self.capacity = initial_capacity
        self.size = 0
        self.buckets: List[Optional[Tuple[Any, Any]]] = [None] * self.capacity
        self.deleted_marker = object()  # Marker for deleted entries
        self.load_factor_threshold = 0.75
        logger.debug(
            f"Initialized hash table with open addressing "
            f"(capacity: {self.capacity})"
        )

    def _hash(self, key: Any) -> int:
        """Compute hash value for key.

        Args:
            key: Key to hash.

        Returns:
            Hash value (index in table).
        """
        return hash(key) % self.capacity

    def _probe(self, key: Any, start_index: int) -> int:
        """Linear probing to find next available slot.

        Args:
            key: Key to probe for.
            start_index: Starting index.

        Returns:
            Index of available slot or slot with matching key.
        """
        index = start_index
        while True:
            if (
                self.buckets[index] is None
                or self.buckets[index][0] == key
                or self.buckets[index] is self.deleted_marker
            ):
                return index
            index = (index + 1) % self.capacity
            if index == start_index:
                # Table is full (should not happen with proper resizing)
                raise RuntimeError("Hash table is full")

    def _resize(self) -> None:
        """Resize hash table when load factor exceeds threshold."""
        logger.info(
            f"Resizing hash table (current size: {self.size}, "
            f"capacity: {self.capacity})"
        )
        old_buckets = self.buckets
        self.capacity *= 2
        self.size = 0
        self.buckets = [None] * self.capacity

        # Rehash all existing key-value pairs
        for entry in old_buckets:
            if entry is not None and entry is not self.deleted_marker:
                key, value = entry
                self.insert(key, value)

        logger.debug(f"Resized to capacity: {self.capacity}")

    def insert(self, key: Any, value: Any) -> None:
        """Insert key-value pair into hash table.

        Args:
            key: Key to insert.
            value: Value to associate with key.
        """
        logger.debug(f"Inserting key: {key}, value: {value}")

        index = self._hash(key)
        probe_index = self._probe(key, index)

        # Check if key already exists
        if (
            self.buckets[probe_index] is not None
            and self.buckets[probe_index] is not self.deleted_marker
            and self.buckets[probe_index][0] == key
        ):
            # Update existing key
            self.buckets[probe_index] = (key, value)
            logger.debug(f"Updated existing key: {key}")
            return

        # Insert new key-value pair
        self.buckets[probe_index] = (key, value)
        self.size += 1
        logger.debug(f"Inserted new key: {key}")

        # Check load factor and resize if necessary
        load_factor = self.size / self.capacity
        if load_factor > self.load_factor_threshold:
            self._resize()

    def get(self, key: Any) -> Optional[Any]:
        """Get value associated with key.

        Args:
            key: Key to search for.

        Returns:
            Value associated with key, or None if not found.
        """
        logger.debug(f"Getting value for key: {key}")

        index = self._hash(key)
        start_index = index

        while True:
            entry = self.buckets[index]

            if entry is None:
                # Empty slot, key not found
                logger.debug(f"Key not found: {key}")
                return None

            if entry is not self.deleted_marker and entry[0] == key:
                # Found key
                logger.debug(f"Found key: {key}, value: {entry[1]}")
                return entry[1]

            index = (index + 1) % self.capacity
            if index == start_index:
                # Searched entire table, key not found
                logger.debug(f"Key not found: {key}")
                return None

    def delete(self, key: Any) -> bool:
        """Delete key-value pair from hash table.

        Args:
            key: Key to delete.

        Returns:
            True if key was deleted, False if not found.
        """
        logger.debug(f"Deleting key: {key}")

        index = self._hash(key)
        start_index = index

        while True:
            entry = self.buckets[index]

            if entry is None:
                # Empty slot, key not found
                logger.debug(f"Key not found for deletion: {key}")
                return False

            if entry is not self.deleted_marker and entry[0] == key:
                # Found key, mark as deleted
                self.buckets[index] = self.deleted_marker
                self.size -= 1
                logger.debug(f"Deleted key: {key}")
                return True

            index = (index + 1) % self.capacity
            if index == start_index:
                # Searched entire table, key not found
                logger.debug(f"Key not found for deletion: {key}")
                return False

    def contains(self, key: Any) -> bool:
        """Check if key exists in hash table.

        Args:
            key: Key to check.

        Returns:
            True if key exists, False otherwise.
        """
        return self.get(key) is not None

    def get_load_factor(self) -> float:
        """Get current load factor.

        Returns:
            Load factor (size / capacity).
        """
        return self.size / self.capacity if self.capacity > 0 else 0.0

    def visualize(self) -> str:
        """Generate visual representation of hash table.

        Returns:
            String representation of hash table structure.
        """
        lines = []
        lines.append("Hash Table (Open Addressing - Linear Probing):")
        lines.append("=" * 50)

        for i, entry in enumerate(self.buckets):
            if entry is None:
                lines.append(f"Index {i}: (empty)")
            elif entry is self.deleted_marker:
                lines.append(f"Index {i}: (deleted)")
            else:
                key, value = entry
                lines.append(f"Index {i}: ({key}:{value})")

        lines.append("=" * 50)
        lines.append(
            f"Size: {self.size}, Capacity: {self.capacity}, "
            f"Load Factor: {self.get_load_factor():.2f}"
        )

        return "\n".join(lines)


class HashTableVisualizer:
    """Visualizer for hash table operations and comparison."""

    def __init__(self, config_path: str = "config.yaml") -> None:
        """Initialize visualizer with configuration.

        Args:
            config_path: Path to configuration YAML file.

        Raises:
            FileNotFoundError: If config file doesn't exist.
            yaml.YAMLError: If config file is invalid YAML.
        """
        self.config = self._load_config(config_path)
        self._setup_logging()
        self.operation_history: List[Dict[str, Any]] = []

    def _load_config(self, config_path: str) -> dict:
        """Load configuration from YAML file.

        Args:
            config_path: Path to configuration file.

        Returns:
            Dictionary containing configuration settings.

        Raises:
            FileNotFoundError: If config file doesn't exist.
            yaml.YAMLError: If config file is invalid YAML.
        """
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
            if not config:
                raise ValueError("Configuration file is empty")
            return config
        except FileNotFoundError:
            logger.error(f"Configuration file not found: {config_path}")
            raise
        except yaml.YAMLError as e:
            logger.error(f"Invalid YAML in configuration file: {e}")
            raise

    def _setup_logging(self) -> None:
        """Configure logging based on configuration settings."""
        log_level = self.config.get("logging", {}).get("level", "INFO")
        log_file = self.config.get("logging", {}).get("file", "logs/app.log")
        log_format = (
            "%(asctime)s - %(name)s - %(levelname)s - "
            "%(message)s"
        )

        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        logging.basicConfig(
            level=getattr(logging, log_level.upper()),
            format=log_format,
            handlers=[
                logging.handlers.RotatingFileHandler(
                    log_file, maxBytes=10485760, backupCount=5
                ),
                logging.StreamHandler(),
            ],
        )

    def compare_methods(
        self, operations: List[Tuple[str, Any, Optional[Any]]]
    ) -> Dict[str, Dict[str, Any]]:
        """Compare chaining and open addressing methods.

        Args:
            operations: List of operations as (operation, key, value) tuples.
                Operation can be 'insert', 'get', 'delete'.

        Returns:
            Dictionary with performance comparison.
        """
        logger.info("Comparing hash table methods")

        chaining_table = HashTableChaining()
        open_addressing_table = HashTableOpenAddressing()

        results = {
            "chaining": {"operations": 0, "resizes": 0},
            "open_addressing": {"operations": 0, "resizes": 0},
        }

        initial_capacity = chaining_table.capacity

        # Execute operations on both tables
        for op, key, value in operations:
            if op == "insert":
                chaining_table.insert(key, value)
                open_addressing_table.insert(key, value)
                results["chaining"]["operations"] += 1
                results["open_addressing"]["operations"] += 1

                # Track resizes
                if chaining_table.capacity > initial_capacity:
                    results["chaining"]["resizes"] = (
                        chaining_table.capacity // initial_capacity - 1
                    )
                if open_addressing_table.capacity > initial_capacity:
                    results["open_addressing"]["resizes"] = (
                        open_addressing_table.capacity // initial_capacity - 1
                    )

            elif op == "get":
                chaining_table.get(key)
                open_addressing_table.get(key)
                results["chaining"]["operations"] += 1
                results["open_addressing"]["operations"] += 1

            elif op == "delete":
                chaining_table.delete(key)
                open_addressing_table.delete(key)
                results["chaining"]["operations"] += 1
                results["open_addressing"]["operations"] += 1

        results["chaining"]["table"] = chaining_table
        results["chaining"]["size"] = chaining_table.size
        results["chaining"]["capacity"] = chaining_table.capacity
        results["chaining"]["load_factor"] = chaining_table.get_load_factor()

        results["open_addressing"]["table"] = open_addressing_table
        results["open_addressing"]["size"] = open_addressing_table.size
        results["open_addressing"]["capacity"] = open_addressing_table.capacity
        results["open_addressing"]["load_factor"] = (
            open_addressing_table.get_load_factor()
        )

        logger.info("Comparison complete")
        return results

    def generate_report(
        self,
        comparison_results: Dict[str, Dict[str, Any]],
        output_path: Optional[str] = None,
    ) -> str:
        """Generate detailed comparison report.

        Args:
            comparison_results: Results from compare_methods.
            output_path: Optional path to save report file.

        Returns:
            Report content as string.
        """
        report_lines = [
            "=" * 80,
            "HASH TABLE COLLISION HANDLING COMPARISON REPORT",
            "=" * 80,
            "",
            "METHOD COMPARISON",
            "-" * 80,
        ]

        for method_name in ["chaining", "open_addressing"]:
            result = comparison_results[method_name]
            report_lines.append(f"\n{method_name.upper().replace('_', ' ')}:")
            report_lines.append(f"  Size: {result['size']}")
            report_lines.append(f"  Capacity: {result['capacity']}")
            report_lines.append(f"  Load Factor: {result['load_factor']:.2f}")
            report_lines.append(f"  Resizes: {result['resizes']}")

        report_lines.extend([
            "",
            "COLLISION HANDLING METHODS",
            "-" * 80,
            "CHAINING (Separate Chaining):",
            "  - Each bucket contains a list of key-value pairs",
            "  - Collisions are handled by adding to the list",
            "  - No probing needed",
            "  - Can handle unlimited collisions per bucket",
            "",
            "OPEN ADDRESSING (Linear Probing):",
            "  - All elements stored directly in table",
            "  - Collisions handled by probing to next available slot",
            "  - Linear probing: next slot = (index + 1) % capacity",
            "  - Requires careful load factor management",
            "",
            "ALGORITHM COMPLEXITY",
            "-" * 80,
            "CHAINING:",
            "  - Insert: O(1) average, O(n) worst (all in one bucket)",
            "  - Get: O(1) average, O(n) worst",
            "  - Delete: O(1) average, O(n) worst",
            "  - Space: O(n + m) where m is capacity",
            "",
            "OPEN ADDRESSING:",
            "  - Insert: O(1) average, O(n) worst (clustering)",
            "  - Get: O(1) average, O(n) worst",
            "  - Delete: O(1) average, O(n) worst",
            "  - Space: O(m) where m is capacity",
            "",
            "ADVANTAGES AND DISADVANTAGES",
            "-" * 80,
            "CHAINING Advantages:",
            "  - Simple implementation",
            "  - No clustering issues",
            "  - Can handle high load factors",
            "  - Easy to delete",
            "",
            "CHAINING Disadvantages:",
            "  - Extra memory for pointers/lists",
            "  - Cache performance not optimal",
            "  - Worst case: all keys hash to same bucket",
            "",
            "OPEN ADDRESSING Advantages:",
            "  - Better cache performance",
            "  - No extra memory for pointers",
            "  - Predictable memory usage",
            "",
            "OPEN ADDRESSING Disadvantages:",
            "  - Clustering can degrade performance",
            "  - More complex deletion (tombstone markers)",
            "  - Requires careful load factor management",
            "  - Worst case: long probe sequences",
        ])

        report_content = "\n".join(report_lines)

        if output_path:
            try:
                output_file = Path(output_path)
                output_file.parent.mkdir(parents=True, exist_ok=True)
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(report_content)
                logger.info(f"Report saved to {output_path}")
            except (IOError, PermissionError) as e:
                logger.error(f"Failed to save report: {e}")
                raise

        return report_content


def main() -> None:
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Hash table implementation with chaining and open addressing"
    )
    parser.add_argument(
        "-c",
        "--config",
        default="config.yaml",
        help="Path to configuration file (default: config.yaml)",
    )
    parser.add_argument(
        "-m",
        "--method",
        choices=["chaining", "open_addressing", "both"],
        default="both",
        help="Collision handling method (default: both)",
    )
    parser.add_argument(
        "-v",
        "--visualize",
        action="store_true",
        help="Show hash table visualization",
    )
    parser.add_argument(
        "-r",
        "--report",
        help="Output path for comparison report",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run demonstration with example operations",
    )

    args = parser.parse_args()

    try:
        visualizer = HashTableVisualizer(config_path=args.config)

        if args.demo:
            # Run demonstration
            print("\n=== Hash Table Demonstration ===\n")

            # Example operations
            operations = [
                ("insert", "apple", 10),
                ("insert", "banana", 20),
                ("insert", "cherry", 30),
                ("insert", "date", 40),
                ("insert", "elderberry", 50),
            ]

            if args.method in ["chaining", "both"]:
                print("--- Chaining Method ---")
                chaining_table = HashTableChaining()
                for op, key, value in operations:
                    chaining_table.insert(key, value)
                    print(f"Inserted: {key} -> {value}")

                if args.visualize:
                    print("\n" + chaining_table.visualize())

                print(f"\nGet 'banana': {chaining_table.get('banana')}")
                print(f"Contains 'cherry': {chaining_table.contains('cherry')}")
                print(f"Delete 'date': {chaining_table.delete('date')}")
                print(f"Size: {chaining_table.size}, "
                      f"Load Factor: {chaining_table.get_load_factor():.2f}")

            if args.method in ["open_addressing", "both"]:
                print("\n--- Open Addressing Method ---")
                open_table = HashTableOpenAddressing()
                for op, key, value in operations:
                    open_table.insert(key, value)
                    print(f"Inserted: {key} -> {value}")

                if args.visualize:
                    print("\n" + open_table.visualize())

                print(f"\nGet 'banana': {open_table.get('banana')}")
                print(f"Contains 'cherry': {open_table.contains('cherry')}")
                print(f"Delete 'date': {open_table.delete('date')}")
                print(f"Size: {open_table.size}, "
                      f"Load Factor: {open_table.get_load_factor():.2f}")

            if args.method == "both":
                print("\n--- Method Comparison ---")
                comparison = visualizer.compare_methods(operations)
                print(f"Chaining - Size: {comparison['chaining']['size']}, "
                      f"Load Factor: {comparison['chaining']['load_factor']:.2f}")
                print(
                    f"Open Addressing - Size: {comparison['open_addressing']['size']}, "
                    f"Load Factor: {comparison['open_addressing']['load_factor']:.2f}"
                )

                if args.report:
                    report = visualizer.generate_report(
                        comparison, output_path=args.report
                    )
                    print(f"\nReport saved to {args.report}")

        else:
            print("Use --demo for demonstration or provide operations interactively")
            print("Hash table operations available:")
            print("  - insert(key, value)")
            print("  - get(key)")
            print("  - delete(key)")
            print("  - contains(key)")

    except Exception as e:
        logger.error(f"Error during execution: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
