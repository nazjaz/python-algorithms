"""Queue Data Structure - Array and linked list implementations.

This module provides queue data structure implementations using both
array-based and linked list approaches with performance analysis.
"""

import logging
import logging.handlers
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class Node:
    """Node for linked list implementation."""

    def __init__(self, data: Any) -> None:
        """Initialize node with data.

        Args:
            data: Data to store in node.
        """
        self.data = data
        self.next: Optional["Node"] = None


class ArrayQueue:
    """Queue implementation using array (list)."""

    def __init__(self) -> None:
        """Initialize empty queue."""
        self._items: List[Any] = []
        logger.debug("ArrayQueue initialized")

    def enqueue(self, item: Any) -> None:
        """Add item to rear of queue.

        Args:
            item: Item to add to queue.
        """
        self._items.append(item)
        logger.debug(f"Enqueued {item}. Queue: {self._items}")

    def dequeue(self) -> Any:
        """Remove and return item from front of queue.

        Returns:
            Item from front of queue.

        Raises:
            IndexError: If queue is empty.
        """
        if self.is_empty():
            logger.error("Attempted to dequeue from empty queue")
            raise IndexError("Queue is empty")

        item = self._items.pop(0)
        logger.debug(f"Dequeued {item}. Queue: {self._items}")
        return item

    def front(self) -> Any:
        """Get front item without removing it.

        Returns:
            Item at front of queue.

        Raises:
            IndexError: If queue is empty.
        """
        if self.is_empty():
            logger.error("Attempted to peek at empty queue")
            raise IndexError("Queue is empty")

        item = self._items[0]
        logger.debug(f"Front item: {item}. Queue: {self._items}")
        return item

    def rear(self) -> Any:
        """Get rear item without removing it.

        Returns:
            Item at rear of queue.

        Raises:
            IndexError: If queue is empty.
        """
        if self.is_empty():
            logger.error("Attempted to peek at rear of empty queue")
            raise IndexError("Queue is empty")

        item = self._items[-1]
        logger.debug(f"Rear item: {item}. Queue: {self._items}")
        return item

    def is_empty(self) -> bool:
        """Check if queue is empty.

        Returns:
            True if queue is empty, False otherwise.
        """
        return len(self._items) == 0

    def size(self) -> int:
        """Get size of queue.

        Returns:
            Number of items in queue.
        """
        return len(self._items)

    def __str__(self) -> str:
        """String representation of queue.

        Returns:
            String representation showing queue contents.
        """
        return f"ArrayQueue({self._items})"

    def __repr__(self) -> str:
        """Representation of queue.

        Returns:
            Representation string.
        """
        return f"ArrayQueue({self._items!r})"


class LinkedListQueue:
    """Queue implementation using linked list."""

    def __init__(self) -> None:
        """Initialize empty queue."""
        self._front: Optional[Node] = None
        self._rear: Optional[Node] = None
        self._size = 0
        logger.debug("LinkedListQueue initialized")

    def enqueue(self, item: Any) -> None:
        """Add item to rear of queue.

        Args:
            item: Item to add to queue.
        """
        new_node = Node(item)

        if self._rear is None:
            self._front = self._rear = new_node
        else:
            self._rear.next = new_node
            self._rear = new_node

        self._size += 1
        logger.debug(f"Enqueued {item}. Size: {self._size}")

    def dequeue(self) -> Any:
        """Remove and return item from front of queue.

        Returns:
            Item from front of queue.

        Raises:
            IndexError: If queue is empty.
        """
        if self.is_empty():
            logger.error("Attempted to dequeue from empty queue")
            raise IndexError("Queue is empty")

        item = self._front.data
        self._front = self._front.next

        if self._front is None:
            self._rear = None

        self._size -= 1
        logger.debug(f"Dequeued {item}. Size: {self._size}")
        return item

    def front(self) -> Any:
        """Get front item without removing it.

        Returns:
            Item at front of queue.

        Raises:
            IndexError: If queue is empty.
        """
        if self.is_empty():
            logger.error("Attempted to peek at empty queue")
            raise IndexError("Queue is empty")

        item = self._front.data
        logger.debug(f"Front item: {item}")
        return item

    def rear(self) -> Any:
        """Get rear item without removing it.

        Returns:
            Item at rear of queue.

        Raises:
            IndexError: If queue is empty.
        """
        if self.is_empty():
            logger.error("Attempted to peek at rear of empty queue")
            raise IndexError("Queue is empty")

        item = self._rear.data
        logger.debug(f"Rear item: {item}")
        return item

    def is_empty(self) -> bool:
        """Check if queue is empty.

        Returns:
            True if queue is empty, False otherwise.
        """
        return self._front is None

    def size(self) -> int:
        """Get size of queue.

        Returns:
            Number of items in queue.
        """
        return self._size

    def __str__(self) -> str:
        """String representation of queue.

        Returns:
            String representation showing queue contents.
        """
        items = []
        current = self._front
        while current:
            items.append(str(current.data))
            current = current.next
        return f"LinkedListQueue({items})"

    def __repr__(self) -> str:
        """Representation of queue.

        Returns:
            Representation string.
        """
        items = []
        current = self._front
        while current:
            items.append(repr(current.data))
            current = current.next
        return f"LinkedListQueue({items!r})"


class QueuePerformanceAnalyzer:
    """Analyzes performance of different queue implementations."""

    def __init__(self, config_path: str = "config.yaml") -> None:
        """Initialize QueuePerformanceAnalyzer with configuration.

        Args:
            config_path: Path to configuration YAML file.

        Raises:
            FileNotFoundError: If config file doesn't exist.
            yaml.YAMLError: If config file is invalid YAML.
        """
        self.config = self._load_config(config_path)
        self._setup_logging()

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

    def compare_implementations(
        self, operations: List[str], iterations: int = 1
    ) -> Dict[str, any]:
        """Compare performance of array and linked list queue implementations.

        Args:
            operations: List of operations to perform (format: "enqueue X" or "dequeue").
            iterations: Number of iterations for timing (default: 1).

        Returns:
            Dictionary containing performance comparison data.
        """
        logger.info(
            f"Comparing queue implementations with {len(operations)} operations"
        )

        results = {
            "operations_count": len(operations),
            "iterations": iterations,
            "array_queue": {},
            "linked_list_queue": {},
        }

        # Array queue performance
        try:
            start_time = time.perf_counter()
            for _ in range(iterations):
                array_queue = ArrayQueue()
                for op in operations:
                    if op.startswith("enqueue"):
                        value = op.split()[1] if len(op.split()) > 1 else None
                        array_queue.enqueue(value)
                    elif op == "dequeue":
                        if not array_queue.is_empty():
                            array_queue.dequeue()
            array_time = time.perf_counter() - start_time

            results["array_queue"] = {
                "time_seconds": array_time / iterations,
                "time_milliseconds": (array_time / iterations) * 1000,
                "success": True,
            }
        except Exception as e:
            logger.error(f"Array queue failed: {e}")
            results["array_queue"] = {"success": False, "error": str(e)}

        # Linked list queue performance
        try:
            start_time = time.perf_counter()
            for _ in range(iterations):
                linked_queue = LinkedListQueue()
                for op in operations:
                    if op.startswith("enqueue"):
                        value = op.split()[1] if len(op.split()) > 1 else None
                        linked_queue.enqueue(value)
                    elif op == "dequeue":
                        if not linked_queue.is_empty():
                            linked_queue.dequeue()
            linked_time = time.perf_counter() - start_time

            results["linked_list_queue"] = {
                "time_seconds": linked_time / iterations,
                "time_milliseconds": (linked_time / iterations) * 1000,
                "success": True,
            }
        except Exception as e:
            logger.error(f"Linked list queue failed: {e}")
            results["linked_list_queue"] = {"success": False, "error": str(e)}

        # Determine fastest
        successful_results = [
            (name, data)
            for name, data in [
                ("array_queue", results["array_queue"]),
                ("linked_list_queue", results["linked_list_queue"]),
            ]
            if data.get("success", False)
        ]

        if successful_results:
            fastest = min(successful_results, key=lambda x: x[1]["time_seconds"])
            results["fastest"] = fastest[0]
            results["fastest_time"] = fastest[1]["time_seconds"]

            # Calculate speedup
            if len(successful_results) == 2:
                times = [r[1]["time_seconds"] for r in successful_results]
                speedup = max(times) / min(times)
                results["speedup"] = speedup

        return results

    def generate_report(
        self, comparison_data: Dict[str, any], output_path: Optional[str] = None
    ) -> str:
        """Generate performance comparison report.

        Args:
            comparison_data: Performance comparison data from compare_implementations().
            output_path: Optional path to save report file.

        Returns:
            Report content as string.
        """
        report_lines = [
            "=" * 80,
            "QUEUE IMPLEMENTATION PERFORMANCE COMPARISON REPORT",
            "=" * 80,
            "",
            f"Operations count: {comparison_data['operations_count']}",
            f"Iterations: {comparison_data['iterations']}",
            "",
            "RESULTS",
            "-" * 80,
        ]

        methods = [
            ("array_queue", "Array Queue"),
            ("linked_list_queue", "Linked List Queue"),
        ]

        for method_key, method_name in methods:
            data = comparison_data[method_key]
            report_lines.append(f"\n{method_name}:")
            if data.get("success", False):
                report_lines.append(
                    f"  Time: {data['time_milliseconds']:.4f} ms "
                    f"({data['time_seconds']:.6f} seconds)"
                )
            else:
                report_lines.append(f"  Status: Failed")
                report_lines.append(f"  Error: {data.get('error', 'Unknown error')}")

        if "fastest" in comparison_data:
            report_lines.extend([
                "",
                "PERFORMANCE SUMMARY",
                "-" * 80,
                f"Fastest implementation: {comparison_data['fastest']}",
                f"Fastest time: {comparison_data['fastest_time']*1000:.4f} ms",
            ])

        if "speedup" in comparison_data:
            report_lines.append(
                f"Speedup: {comparison_data['speedup']:.2f}x"
            )

        report_lines.extend([
            "",
            "ALGORITHM COMPLEXITY",
            "-" * 80,
            "Array Queue:",
            "  Enqueue: O(1) amortized, O(n) worst case (list resizing)",
            "  Dequeue: O(n) - requires shifting all elements",
            "  Front/Rear: O(1)",
            "  Space: O(n)",
            "",
            "Linked List Queue:",
            "  Enqueue: O(1) - constant time",
            "  Dequeue: O(1) - constant time",
            "  Front/Rear: O(1)",
            "  Space: O(n) - one node per element",
            "",
            "PERFORMANCE ANALYSIS",
            "-" * 80,
            "Array Queue:",
            "  - Fast enqueue (append is O(1) amortized)",
            "  - Slow dequeue (pop(0) is O(n))",
            "  - Better for mostly enqueue operations",
            "",
            "Linked List Queue:",
            "  - Fast enqueue (O(1))",
            "  - Fast dequeue (O(1))",
            "  - Better for mixed operations",
            "  - More memory overhead per element",
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
    import argparse

    parser = argparse.ArgumentParser(
        description="Queue data structure with array and linked list implementations"
    )
    parser.add_argument(
        "-c",
        "--config",
        default="config.yaml",
        help="Path to configuration file (default: config.yaml)",
    )
    parser.add_argument(
        "-i",
        "--implementation",
        choices=["array", "linked", "both", "compare"],
        default="both",
        help="Queue implementation to use (default: both)",
    )
    parser.add_argument(
        "--operations",
        nargs="+",
        help="Operations to perform (e.g., 'enqueue 1' 'enqueue 2' 'dequeue')",
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=1,
        help="Number of iterations for performance testing (default: 1)",
    )
    parser.add_argument(
        "-r",
        "--report",
        help="Output path for performance report",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run queue operations demonstration",
    )

    args = parser.parse_args()

    try:
        if args.demo:
            # Demonstrate queue operations
            print("\n=== Queue Operations Demonstration ===\n")

            print("--- Array Queue ---")
            array_queue = ArrayQueue()
            print(f"Initial queue: {array_queue}")
            print(f"Is empty: {array_queue.is_empty()}")
            print(f"Size: {array_queue.size()}")

            print("\n--- Enqueuing items ---")
            for item in [10, 20, 30, 40, 50]:
                array_queue.enqueue(item)
                print(f"After enqueuing {item}: {array_queue}")
                print(f"  Front: {array_queue.front()}, Rear: {array_queue.rear()}")

            print("\n--- Dequeuing items ---")
            while not array_queue.is_empty():
                item = array_queue.dequeue()
                print(f"Dequeued {item}, remaining: {array_queue}")

            print("\n--- Linked List Queue ---")
            linked_queue = LinkedListQueue()
            print(f"Initial queue: {linked_queue}")
            print(f"Is empty: {linked_queue.is_empty()}")
            print(f"Size: {linked_queue.size()}")

            print("\n--- Enqueuing items ---")
            for item in [10, 20, 30, 40, 50]:
                linked_queue.enqueue(item)
                print(f"After enqueuing {item}: {linked_queue}")
                print(f"  Front: {linked_queue.front()}, Rear: {linked_queue.rear()}")

            print("\n--- Dequeuing items ---")
            while not linked_queue.is_empty():
                item = linked_queue.dequeue()
                print(f"Dequeued {item}, remaining: {linked_queue}")

        elif args.implementation == "compare" or args.operations:
            analyzer = QueuePerformanceAnalyzer(config_path=args.config)

            if args.operations:
                operations = args.operations
            else:
                # Default operations for comparison
                operations = [f"enqueue {i}" for i in range(100)] + ["dequeue"] * 50

            comparison = analyzer.compare_implementations(operations, args.iterations)

            print(f"\nQueue Implementation Performance Comparison:")
            print(f"Operations: {len(operations)}")
            print(f"Iterations: {args.iterations}")
            print("-" * 60)

            methods = [
                ("array_queue", "Array Queue"),
                ("linked_list_queue", "Linked List Queue"),
            ]

            for method_key, method_name in methods:
                data = comparison[method_key]
                if data.get("success", False):
                    print(
                        f"{method_name:25s}: {data['time_milliseconds']:8.4f} ms"
                    )
                else:
                    print(
                        f"{method_name:25s}: Failed - {data.get('error', 'Unknown')}"
                    )

            if "fastest" in comparison:
                print(f"\nFastest: {comparison['fastest']}")
            if "speedup" in comparison:
                print(f"Speedup: {comparison['speedup']:.2f}x")

            if args.report:
                report = analyzer.generate_report(comparison, output_path=args.report)
                print(f"\nReport saved to {args.report}")

        else:
            # Interactive mode
            if args.implementation in ["array", "both"]:
                print("\n=== Array Queue ===")
                queue = ArrayQueue()
                print(f"Queue: {queue}")
                print(f"Is empty: {queue.is_empty()}")

                for i in [1, 2, 3, 4, 5]:
                    queue.enqueue(i)
                    print(f"After enqueue {i}: {queue}")

                print(f"Front: {queue.front()}, Rear: {queue.rear()}")

                while not queue.is_empty():
                    item = queue.dequeue()
                    print(f"Dequeued {item}: {queue}")

            if args.implementation in ["linked", "both"]:
                print("\n=== Linked List Queue ===")
                queue = LinkedListQueue()
                print(f"Queue: {queue}")
                print(f"Is empty: {queue.is_empty()}")

                for i in [1, 2, 3, 4, 5]:
                    queue.enqueue(i)
                    print(f"After enqueue {i}: {queue}")

                print(f"Front: {queue.front()}, Rear: {queue.rear()}")

                while not queue.is_empty():
                    item = queue.dequeue()
                    print(f"Dequeued {item}: {queue}")

    except Exception as e:
        logger.error(f"Error during execution: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
