"""Linked List Data Structure - Implementation with Visualization.

This module provides a complete linked list implementation with insertion,
deletion, and traversal operations. It includes visualization capabilities
to show the structure and operations of the linked list.
"""

import argparse
import logging
import logging.handlers
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class Node:
    """Node class for linked list elements."""

    def __init__(self, data: Any) -> None:
        """Initialize node with data.

        Args:
            data: Data to store in node.
        """
        self.data = data
        self.next: Optional["Node"] = None
        logger.debug(f"Created node with data: {data}")

    def __repr__(self) -> str:
        """String representation of node.

        Returns:
            String representation.
        """
        return f"Node({self.data})"


class LinkedList:
    """Linked list implementation with insertion, deletion, and traversal."""

    def __init__(self) -> None:
        """Initialize empty linked list."""
        self.head: Optional[Node] = None
        self._size = 0
        logger.debug("Initialized empty linked list")

    def is_empty(self) -> bool:
        """Check if linked list is empty.

        Returns:
            True if list is empty, False otherwise.
        """
        return self.head is None

    def size(self) -> int:
        """Get size of linked list.

        Returns:
            Number of nodes in the list.
        """
        return self._size

    def insert_at_beginning(self, data: Any) -> None:
        """Insert node at the beginning of the list.

        Args:
            data: Data to insert.
        """
        logger.info(f"Inserting {data} at beginning")
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self._size += 1
        logger.debug(f"List size: {self._size}")

    def insert_at_end(self, data: Any) -> None:
        """Insert node at the end of the list.

        Args:
            data: Data to insert.
        """
        logger.info(f"Inserting {data} at end")
        new_node = Node(data)

        if self.is_empty():
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node

        self._size += 1
        logger.debug(f"List size: {self._size}")

    def insert_at_position(self, data: Any, position: int) -> bool:
        """Insert node at a specific position.

        Args:
            data: Data to insert.
            position: Position to insert at (0-indexed).

        Returns:
            True if insertion successful, False otherwise.
        """
        logger.info(f"Inserting {data} at position {position}")

        if position < 0 or position > self._size:
            logger.warning(f"Invalid position: {position}")
            return False

        if position == 0:
            self.insert_at_beginning(data)
            return True

        new_node = Node(data)
        current = self.head
        for _ in range(position - 1):
            if current is None:
                return False
            current = current.next

        if current is None:
            return False

        new_node.next = current.next
        current.next = new_node
        self._size += 1
        logger.debug(f"List size: {self._size}")
        return True

    def delete_at_beginning(self) -> Optional[Any]:
        """Delete node at the beginning of the list.

        Returns:
            Data of deleted node, or None if list is empty.
        """
        logger.info("Deleting node at beginning")

        if self.is_empty():
            logger.warning("Cannot delete from empty list")
            return None

        data = self.head.data
        self.head = self.head.next
        self._size -= 1
        logger.debug(f"Deleted {data}, list size: {self._size}")
        return data

    def delete_at_end(self) -> Optional[Any]:
        """Delete node at the end of the list.

        Returns:
            Data of deleted node, or None if list is empty.
        """
        logger.info("Deleting node at end")

        if self.is_empty():
            logger.warning("Cannot delete from empty list")
            return None

        if self.head.next is None:
            data = self.head.data
            self.head = None
            self._size = 0
            logger.debug(f"Deleted {data}, list size: {self._size}")
            return data

        current = self.head
        while current.next.next is not None:
            current = current.next

        data = current.next.data
        current.next = None
        self._size -= 1
        logger.debug(f"Deleted {data}, list size: {self._size}")
        return data

    def delete_at_position(self, position: int) -> Optional[Any]:
        """Delete node at a specific position.

        Args:
            position: Position to delete from (0-indexed).

        Returns:
            Data of deleted node, or None if deletion failed.
        """
        logger.info(f"Deleting node at position {position}")

        if self.is_empty():
            logger.warning("Cannot delete from empty list")
            return None

        if position < 0 or position >= self._size:
            logger.warning(f"Invalid position: {position}")
            return None

        if position == 0:
            return self.delete_at_beginning()

        current = self.head
        for _ in range(position - 1):
            if current is None:
                return None
            current = current.next

        if current is None or current.next is None:
            return None

        data = current.next.data
        current.next = current.next.next
        self._size -= 1
        logger.debug(f"Deleted {data}, list size: {self._size}")
        return data

    def delete_by_value(self, value: Any) -> bool:
        """Delete first node with given value.

        Args:
            value: Value to delete.

        Returns:
            True if deletion successful, False otherwise.
        """
        logger.info(f"Deleting node with value {value}")

        if self.is_empty():
            logger.warning("Cannot delete from empty list")
            return False

        if self.head.data == value:
            self.delete_at_beginning()
            return True

        current = self.head
        while current.next is not None:
            if current.next.data == value:
                current.next = current.next.next
                self._size -= 1
                logger.debug(f"Deleted {value}, list size: {self._size}")
                return True
            current = current.next

        logger.warning(f"Value {value} not found in list")
        return False

    def search(self, value: Any) -> Optional[int]:
        """Search for a value in the list.

        Args:
            value: Value to search for.

        Returns:
            Position of value if found, None otherwise.
        """
        logger.info(f"Searching for value {value}")

        current = self.head
        position = 0

        while current is not None:
            if current.data == value:
                logger.debug(f"Found {value} at position {position}")
                return position
            current = current.next
            position += 1

        logger.debug(f"Value {value} not found")
        return None

    def get(self, position: int) -> Optional[Any]:
        """Get value at a specific position.

        Args:
            position: Position to get value from (0-indexed).

        Returns:
            Value at position, or None if invalid position.
        """
        if position < 0 or position >= self._size:
            return None

        current = self.head
        for _ in range(position):
            if current is None:
                return None
            current = current.next

        return current.data if current else None

    def traverse(self) -> List[Any]:
        """Traverse the linked list and return all values.

        Returns:
            List of all values in the linked list.
        """
        logger.info("Traversing linked list")
        values = []
        current = self.head

        while current is not None:
            values.append(current.data)
            current = current.next

        logger.debug(f"Traversed {len(values)} nodes")
        return values

    def visualize(self) -> str:
        """Generate visual representation of the linked list.

        Returns:
            String representation of the linked list structure.
        """
        if self.is_empty():
            return "Empty List: NULL"

        visualization = []
        current = self.head
        position = 0

        while current is not None:
            arrow = " -> " if current.next is not None else " -> NULL"
            visualization.append(f"[{position}] {current.data}{arrow}")
            current = current.next
            position += 1

        return "\n".join(visualization)

    def visualize_detailed(self) -> str:
        """Generate detailed visual representation with node details.

        Returns:
            Detailed string representation of the linked list.
        """
        if self.is_empty():
            return "Empty List: NULL\nSize: 0"

        lines = [
            "Linked List Structure:",
            "=" * 50,
        ]

        current = self.head
        position = 0

        while current is not None:
            next_data = current.next.data if current.next else "NULL"
            lines.append(
                f"Position {position}: Node(data={current.data}, next={next_data})"
            )
            current = current.next
            position += 1

        lines.append("=" * 50)
        lines.append(f"Size: {self._size}")
        lines.append(f"Head: {self.head.data if self.head else 'NULL'}")

        return "\n".join(lines)

    def to_list(self) -> List[Any]:
        """Convert linked list to Python list.

        Returns:
            List containing all values in order.
        """
        return self.traverse()

    def from_list(self, data_list: List[Any]) -> None:
        """Create linked list from Python list.

        Args:
            data_list: List of values to insert.
        """
        logger.info(f"Creating linked list from list: {data_list}")
        self.head = None
        self._size = 0

        for data in data_list:
            self.insert_at_end(data)

    def reverse(self) -> None:
        """Reverse the linked list in-place."""
        logger.info("Reversing linked list")

        if self.is_empty() or self.head.next is None:
            return

        prev = None
        current = self.head

        while current is not None:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node

        self.head = prev
        logger.debug("Linked list reversed")

    def __repr__(self) -> str:
        """String representation of linked list.

        Returns:
            String representation.
        """
        values = self.traverse()
        return f"LinkedList({values})"

    def __len__(self) -> int:
        """Get length of linked list.

        Returns:
            Size of the list.
        """
        return self._size


class LinkedListVisualizer:
    """Visualizer for linked list operations."""

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
        self.linked_list = LinkedList()
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

    def _record_operation(self, operation: str, **kwargs) -> None:
        """Record an operation in history.

        Args:
            operation: Operation name.
            **kwargs: Additional operation parameters.
        """
        self.operation_history.append({
            "operation": operation,
            "list_state": self.linked_list.traverse(),
            "size": self.linked_list.size(),
            **kwargs,
        })

    def insert_at_beginning(self, data: Any) -> None:
        """Insert at beginning and record operation."""
        self.linked_list.insert_at_beginning(data)
        self._record_operation("insert_at_beginning", data=data)

    def insert_at_end(self, data: Any) -> None:
        """Insert at end and record operation."""
        self.linked_list.insert_at_end(data)
        self._record_operation("insert_at_end", data=data)

    def insert_at_position(self, data: Any, position: int) -> bool:
        """Insert at position and record operation."""
        result = self.linked_list.insert_at_position(data, position)
        self._record_operation(
            "insert_at_position", data=data, position=position, success=result
        )
        return result

    def delete_at_beginning(self) -> Optional[Any]:
        """Delete at beginning and record operation."""
        result = self.linked_list.delete_at_beginning()
        self._record_operation("delete_at_beginning", deleted=result)
        return result

    def delete_at_end(self) -> Optional[Any]:
        """Delete at end and record operation."""
        result = self.linked_list.delete_at_end()
        self._record_operation("delete_at_end", deleted=result)
        return result

    def delete_at_position(self, position: int) -> Optional[Any]:
        """Delete at position and record operation."""
        result = self.linked_list.delete_at_position(position)
        self._record_operation(
            "delete_at_position", position=position, deleted=result
        )
        return result

    def delete_by_value(self, value: Any) -> bool:
        """Delete by value and record operation."""
        result = self.linked_list.delete_by_value(value)
        self._record_operation("delete_by_value", value=value, success=result)
        return result

    def print_visualization(self, detailed: bool = False) -> None:
        """Print visualization of linked list.

        Args:
            detailed: If True, print detailed visualization.
        """
        if detailed:
            print(self.linked_list.visualize_detailed())
        else:
            print(self.linked_list.visualize())

    def generate_report(self, output_path: Optional[str] = None) -> str:
        """Generate detailed operation report.

        Args:
            output_path: Optional path to save report file.

        Returns:
            Report content as string.
        """
        report_lines = [
            "=" * 80,
            "LINKED LIST OPERATIONS REPORT",
            "=" * 80,
            "",
            "CURRENT STATE",
            "-" * 80,
            self.linked_list.visualize_detailed(),
            "",
            "OPERATION HISTORY",
            "-" * 80,
            "",
        ]

        for idx, op in enumerate(self.operation_history, 1):
            report_lines.append(f"Operation {idx}: {op['operation']}")
            report_lines.append(f"  List state: {op['list_state']}")
            report_lines.append(f"  Size: {op['size']}")
            if "data" in op:
                report_lines.append(f"  Data: {op['data']}")
            if "position" in op:
                report_lines.append(f"  Position: {op['position']}")
            if "deleted" in op:
                report_lines.append(f"  Deleted: {op['deleted']}")
            if "value" in op:
                report_lines.append(f"  Value: {op['value']}")
            report_lines.append("")

        report_lines.extend([
            "LINKED LIST PROPERTIES",
            "-" * 80,
            "Data Structure: Singly Linked List",
            "Node Structure: data + next pointer",
            "Head Pointer: Points to first node",
            "NULL Terminator: Last node points to NULL",
            "",
            "OPERATIONS COMPLEXITY",
            "-" * 80,
            "Insert at beginning: O(1)",
            "Insert at end: O(n)",
            "Insert at position: O(n)",
            "Delete at beginning: O(1)",
            "Delete at end: O(n)",
            "Delete at position: O(n)",
            "Delete by value: O(n)",
            "Search: O(n)",
            "Traverse: O(n)",
            "",
            "ADVANTAGES",
            "-" * 80,
            "- Dynamic size (no fixed capacity)",
            "- Efficient insertion/deletion at beginning",
            "- Memory efficient (only uses needed space)",
            "- Easy to implement",
            "",
            "DISADVANTAGES",
            "-" * 80,
            "- No random access (must traverse)",
            "- Extra memory for pointers",
            "- Cache performance not optimal",
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
        description="Linked list implementation with visualization"
    )
    parser.add_argument(
        "-c",
        "--config",
        default="config.yaml",
        help="Path to configuration file (default: config.yaml)",
    )
    parser.add_argument(
        "-v",
        "--visualize",
        action="store_true",
        help="Show visualization of linked list",
    )
    parser.add_argument(
        "-d",
        "--detailed",
        action="store_true",
        help="Show detailed visualization",
    )
    parser.add_argument(
        "-r",
        "--report",
        help="Output path for operations report",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run demonstration with example operations",
    )

    args = parser.parse_args()

    try:
        visualizer = LinkedListVisualizer(config_path=args.config)

        if args.demo:
            # Run demonstration
            print("\n=== Linked List Demonstration ===\n")

            print("1. Inserting at beginning: 10, 20, 30")
            visualizer.insert_at_beginning(10)
            visualizer.insert_at_beginning(20)
            visualizer.insert_at_beginning(30)
            visualizer.print_visualization(detailed=args.detailed)
            print()

            print("2. Inserting at end: 40, 50")
            visualizer.insert_at_end(40)
            visualizer.insert_at_end(50)
            visualizer.print_visualization(detailed=args.detailed)
            print()

            print("3. Inserting at position 2: 25")
            visualizer.insert_at_position(25, 2)
            visualizer.print_visualization(detailed=args.detailed)
            print()

            print("4. Deleting at beginning")
            visualizer.delete_at_beginning()
            visualizer.print_visualization(detailed=args.detailed)
            print()

            print("5. Deleting at end")
            visualizer.delete_at_end()
            visualizer.print_visualization(detailed=args.detailed)
            print()

            print("6. Deleting at position 1")
            visualizer.delete_at_position(1)
            visualizer.print_visualization(detailed=args.detailed)
            print()

            print("7. Deleting by value: 25")
            visualizer.delete_by_value(25)
            visualizer.print_visualization(detailed=args.detailed)
            print()

            print("8. Traversing list")
            values = visualizer.linked_list.traverse()
            print(f"Values: {values}")
            print()

            print("9. Reversing list")
            visualizer.linked_list.reverse()
            visualizer.print_visualization(detailed=args.detailed)
            print()

        else:
            # Interactive mode - show current state
            if args.visualize or args.detailed:
                visualizer.print_visualization(detailed=args.detailed)
            else:
                print("Use --demo for demonstration or --visualize to see list")
                print("Linked list operations available:")
                print("  - insert_at_beginning(data)")
                print("  - insert_at_end(data)")
                print("  - insert_at_position(data, position)")
                print("  - delete_at_beginning()")
                print("  - delete_at_end()")
                print("  - delete_at_position(position)")
                print("  - delete_by_value(value)")
                print("  - traverse()")
                print("  - reverse()")

        if args.report:
            report = visualizer.generate_report(output_path=args.report)
            print(f"\nReport saved to {args.report}")

    except Exception as e:
        logger.error(f"Error during execution: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
