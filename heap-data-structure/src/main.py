"""Heap Data Structure - Min-Heap and Max-Heap with Heapify and Heap Sort.

This module provides functionality to implement heap data structures
(min-heap and max-heap) with heapify operations and heap sort algorithm.
A heap is a complete binary tree that satisfies the heap property.
"""

import logging
import logging.handlers
import time
from pathlib import Path
from typing import Dict, List, Optional, TypeVar

import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

T = TypeVar("T", int, float)


class MinHeap:
    """Min-Heap implementation with heapify operations.

    In a min-heap, the parent node is always smaller than or equal to
    its children. The minimum element is always at the root.
    """

    def __init__(self, items: Optional[List[T]] = None) -> None:
        """Initialize MinHeap.

        Args:
            items: Optional list of items to build heap from.
        """
        self.heap: List[T] = []
        if items:
            self.build_heap(items)
            logger.debug(f"MinHeap initialized with {len(items)} items")

    def _parent(self, index: int) -> int:
        """Get parent index of given index.

        Args:
            index: Current index.

        Returns:
            Parent index.
        """
        return (index - 1) // 2

    def _left_child(self, index: int) -> int:
        """Get left child index of given index.

        Args:
            index: Current index.

        Returns:
            Left child index.
        """
        return 2 * index + 1

    def _right_child(self, index: int) -> int:
        """Get right child index of given index.

        Args:
            index: Current index.

        Returns:
            Right child index.
        """
        return 2 * index + 2

    def _has_parent(self, index: int) -> bool:
        """Check if index has a parent.

        Args:
            index: Current index.

        Returns:
            True if has parent, False otherwise.
        """
        return index > 0

    def _has_left_child(self, index: int) -> bool:
        """Check if index has a left child.

        Args:
            index: Current index.

        Returns:
            True if has left child, False otherwise.
        """
        return self._left_child(index) < len(self.heap)

    def _has_right_child(self, index: int) -> bool:
        """Check if index has a right child.

        Args:
            index: Current index.

        Returns:
            True if has right child, False otherwise.
        """
        return self._right_child(index) < len(self.heap)

    def _swap(self, i: int, j: int) -> None:
        """Swap elements at indices i and j.

        Args:
            i: First index.
            j: Second index.
        """
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def heapify_up(self, index: int) -> None:
        """Heapify up from given index to maintain min-heap property.

        Moves element up the tree by swapping with parent if parent
        is larger, until heap property is satisfied.

        Args:
            index: Index to start heapify up from.
        """
        while (
            self._has_parent(index)
            and self.heap[self._parent(index)] > self.heap[index]
        ):
            parent_idx = self._parent(index)
            self._swap(parent_idx, index)
            index = parent_idx
            logger.debug(f"  Swapped with parent, new index: {index}")

    def heapify_down(self, index: int) -> None:
        """Heapify down from given index to maintain min-heap property.

        Moves element down the tree by swapping with smaller child,
        until heap property is satisfied.

        Args:
            index: Index to start heapify down from.
        """
        while self._has_left_child(index):
            smaller_child_idx = self._left_child(index)

            if (
                self._has_right_child(index)
                and self.heap[self._right_child(index)]
                < self.heap[smaller_child_idx]
            ):
                smaller_child_idx = self._right_child(index)

            if self.heap[index] < self.heap[smaller_child_idx]:
                break

            self._swap(index, smaller_child_idx)
            index = smaller_child_idx
            logger.debug(f"  Swapped with child, new index: {index}")

    def insert(self, item: T) -> None:
        """Insert item into heap.

        Args:
            item: Item to insert.
        """
        self.heap.append(item)
        self.heapify_up(len(self.heap) - 1)
        logger.debug(f"Inserted {item}, heap size: {len(self.heap)}")

    def extract_min(self) -> Optional[T]:
        """Extract and return minimum element.

        Returns:
            Minimum element, or None if heap is empty.
        """
        if not self.heap:
            logger.warning("Attempted to extract from empty heap")
            return None

        if len(self.heap) == 1:
            return self.heap.pop()

        min_item = self.heap[0]
        self.heap[0] = self.heap.pop()
        self.heapify_down(0)
        logger.debug(f"Extracted min: {min_item}, heap size: {len(self.heap)}")
        return min_item

    def peek(self) -> Optional[T]:
        """Peek at minimum element without removing it.

        Returns:
            Minimum element, or None if heap is empty.
        """
        return self.heap[0] if self.heap else None

    def build_heap(self, items: List[T]) -> None:
        """Build heap from list of items using heapify operations.

        Args:
            items: List of items to build heap from.
        """
        self.heap = items[:]
        logger.info(f"Building min-heap from {len(items)} items")

        # Start from last non-leaf node and heapify down
        for i in range(len(self.heap) // 2 - 1, -1, -1):
            self.heapify_down(i)
            logger.debug(f"  Heapified down from index {i}")

        logger.info(f"Min-heap built with {len(self.heap)} items")

    def size(self) -> int:
        """Get heap size.

        Returns:
            Number of elements in heap.
        """
        return len(self.heap)

    def is_empty(self) -> bool:
        """Check if heap is empty.

        Returns:
            True if heap is empty, False otherwise.
        """
        return len(self.heap) == 0


class MaxHeap:
    """Max-Heap implementation with heapify operations.

    In a max-heap, the parent node is always larger than or equal to
    its children. The maximum element is always at the root.
    """

    def __init__(self, items: Optional[List[T]] = None) -> None:
        """Initialize MaxHeap.

        Args:
            items: Optional list of items to build heap from.
        """
        self.heap: List[T] = []
        if items:
            self.build_heap(items)
            logger.debug(f"MaxHeap initialized with {len(items)} items")

    def _parent(self, index: int) -> int:
        """Get parent index of given index.

        Args:
            index: Current index.

        Returns:
            Parent index.
        """
        return (index - 1) // 2

    def _left_child(self, index: int) -> int:
        """Get left child index of given index.

        Args:
            index: Current index.

        Returns:
            Left child index.
        """
        return 2 * index + 1

    def _right_child(self, index: int) -> int:
        """Get right child index of given index.

        Args:
            index: Current index.

        Returns:
            Right child index.
        """
        return 2 * index + 2

    def _has_parent(self, index: int) -> bool:
        """Check if index has a parent.

        Args:
            index: Current index.

        Returns:
            True if has parent, False otherwise.
        """
        return index > 0

    def _has_left_child(self, index: int) -> bool:
        """Check if index has a left child.

        Args:
            index: Current index.

        Returns:
            True if has left child, False otherwise.
        """
        return self._left_child(index) < len(self.heap)

    def _has_right_child(self, index: int) -> bool:
        """Check if index has a right child.

        Args:
            index: Current index.

        Returns:
            True if has right child, False otherwise.
        """
        return self._right_child(index) < len(self.heap)

    def _swap(self, i: int, j: int) -> None:
        """Swap elements at indices i and j.

        Args:
            i: First index.
            j: Second index.
        """
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def heapify_up(self, index: int) -> None:
        """Heapify up from given index to maintain max-heap property.

        Moves element up the tree by swapping with parent if parent
        is smaller, until heap property is satisfied.

        Args:
            index: Index to start heapify up from.
        """
        while (
            self._has_parent(index)
            and self.heap[self._parent(index)] < self.heap[index]
        ):
            parent_idx = self._parent(index)
            self._swap(parent_idx, index)
            index = parent_idx
            logger.debug(f"  Swapped with parent, new index: {index}")

    def heapify_down(self, index: int) -> None:
        """Heapify down from given index to maintain max-heap property.

        Moves element down the tree by swapping with larger child,
        until heap property is satisfied.

        Args:
            index: Index to start heapify down from.
        """
        while self._has_left_child(index):
            larger_child_idx = self._left_child(index)

            if (
                self._has_right_child(index)
                and self.heap[self._right_child(index)]
                > self.heap[larger_child_idx]
            ):
                larger_child_idx = self._right_child(index)

            if self.heap[index] > self.heap[larger_child_idx]:
                break

            self._swap(index, larger_child_idx)
            index = larger_child_idx
            logger.debug(f"  Swapped with child, new index: {index}")

    def insert(self, item: T) -> None:
        """Insert item into heap.

        Args:
            item: Item to insert.
        """
        self.heap.append(item)
        self.heapify_up(len(self.heap) - 1)
        logger.debug(f"Inserted {item}, heap size: {len(self.heap)}")

    def extract_max(self) -> Optional[T]:
        """Extract and return maximum element.

        Returns:
            Maximum element, or None if heap is empty.
        """
        if not self.heap:
            logger.warning("Attempted to extract from empty heap")
            return None

        if len(self.heap) == 1:
            return self.heap.pop()

        max_item = self.heap[0]
        self.heap[0] = self.heap.pop()
        self.heapify_down(0)
        logger.debug(f"Extracted max: {max_item}, heap size: {len(self.heap)}")
        return max_item

    def peek(self) -> Optional[T]:
        """Peek at maximum element without removing it.

        Returns:
            Maximum element, or None if heap is empty.
        """
        return self.heap[0] if self.heap else None

    def build_heap(self, items: List[T]) -> None:
        """Build heap from list of items using heapify operations.

        Args:
            items: List of items to build heap from.
        """
        self.heap = items[:]
        logger.info(f"Building max-heap from {len(items)} items")

        # Start from last non-leaf node and heapify down
        for i in range(len(self.heap) // 2 - 1, -1, -1):
            self.heapify_down(i)
            logger.debug(f"  Heapified down from index {i}")

        logger.info(f"Max-heap built with {len(self.heap)} items")

    def size(self) -> int:
        """Get heap size.

        Returns:
            Number of elements in heap.
        """
        return len(self.heap)

    def is_empty(self) -> bool:
        """Check if heap is empty.

        Returns:
            True if heap is empty, False otherwise.
        """
        return len(self.heap) == 0


class HeapSort:
    """Heap sort algorithm implementation using heap data structure."""

    def __init__(self, config_path: str = "config.yaml") -> None:
        """Initialize HeapSort with configuration.

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

    def _heapify_down(
        self, arr: List[T], n: int, i: int, is_max_heap: bool = False
    ) -> None:
        """Heapify down for heap sort (in-place).

        Args:
            arr: Array to heapify.
            n: Size of heap.
            i: Index to start heapify from.
            is_max_heap: If True, use max-heap, else min-heap.
        """
        largest_or_smallest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if is_max_heap:
            if left < n and arr[left] > arr[largest_or_smallest]:
                largest_or_smallest = left
            if right < n and arr[right] > arr[largest_or_smallest]:
                largest_or_smallest = right
        else:
            if left < n and arr[left] < arr[largest_or_smallest]:
                largest_or_smallest = left
            if right < n and arr[right] < arr[largest_or_smallest]:
                largest_or_smallest = right

        if largest_or_smallest != i:
            arr[i], arr[largest_or_smallest] = arr[largest_or_smallest], arr[i]
            self._heapify_down(arr, n, largest_or_smallest, is_max_heap)

    def sort_ascending(self, arr: List[T]) -> List[T]:
        """Sort array in ascending order using heap sort.

        Uses max-heap to sort in ascending order.

        Args:
            arr: Array to sort.

        Returns:
            Sorted array in ascending order.
        """
        if not arr:
            logger.info("Empty array: returning empty list")
            return []

        arr = arr[:]
        n = len(arr)

        logger.info(f"Heap sort (ascending): {n} elements")

        # Build max-heap
        for i in range(n // 2 - 1, -1, -1):
            self._heapify_down(arr, n, i, is_max_heap=True)
            logger.debug(f"  Built heap from index {i}")

        # Extract elements one by one
        for i in range(n - 1, 0, -1):
            arr[0], arr[i] = arr[i], arr[0]
            self._heapify_down(arr, i, 0, is_max_heap=True)
            logger.debug(f"  Extracted element at index {i}")

        logger.info(f"Array sorted in ascending order")
        return arr

    def sort_descending(self, arr: List[T]) -> List[T]:
        """Sort array in descending order using heap sort.

        Uses min-heap to sort in descending order.

        Args:
            arr: Array to sort.

        Returns:
            Sorted array in descending order.
        """
        if not arr:
            logger.info("Empty array: returning empty list")
            return []

        arr = arr[:]
        n = len(arr)

        logger.info(f"Heap sort (descending): {n} elements")

        # Build min-heap
        for i in range(n // 2 - 1, -1, -1):
            self._heapify_down(arr, n, i, is_max_heap=False)
            logger.debug(f"  Built heap from index {i}")

        # Extract elements one by one
        for i in range(n - 1, 0, -1):
            arr[0], arr[i] = arr[i], arr[0]
            self._heapify_down(arr, i, 0, is_max_heap=False)
            logger.debug(f"  Extracted element at index {i}")

        logger.info(f"Array sorted in descending order")
        return arr

    def compare_with_builtin(
        self, arr: List[T], iterations: int = 1
    ) -> Dict[str, any]:
        """Compare heap sort performance with built-in sorted().

        Args:
            arr: Array to sort.
            iterations: Number of iterations for timing (default: 1).

        Returns:
            Dictionary containing performance comparison data.
        """
        logger.info(
            f"Comparing heap sort with built-in: {len(arr)} elements, "
            f"iterations={iterations}"
        )

        results = {
            "array_length": len(arr),
            "iterations": iterations,
            "heap_sort_asc": {},
            "heap_sort_desc": {},
            "builtin_sorted": {},
        }

        # Heap sort ascending
        try:
            start_time = time.perf_counter()
            for _ in range(iterations):
                sorted_arr = self.sort_ascending(arr)
            heap_asc_time = time.perf_counter() - start_time

            results["heap_sort_asc"] = {
                "result": sorted_arr,
                "time_seconds": heap_asc_time / iterations,
                "time_milliseconds": (heap_asc_time / iterations) * 1000,
                "success": True,
            }
        except Exception as e:
            logger.error(f"Heap sort ascending failed: {e}")
            results["heap_sort_asc"] = {"success": False, "error": str(e)}

        # Heap sort descending
        try:
            start_time = time.perf_counter()
            for _ in range(iterations):
                sorted_arr = self.sort_descending(arr)
            heap_desc_time = time.perf_counter() - start_time

            results["heap_sort_desc"] = {
                "result": sorted_arr,
                "time_seconds": heap_desc_time / iterations,
                "time_milliseconds": (heap_desc_time / iterations) * 1000,
                "success": True,
            }
        except Exception as e:
            logger.error(f"Heap sort descending failed: {e}")
            results["heap_sort_desc"] = {"success": False, "error": str(e)}

        # Built-in sorted
        try:
            start_time = time.perf_counter()
            for _ in range(iterations):
                sorted_arr = sorted(arr)
            builtin_time = time.perf_counter() - start_time

            results["builtin_sorted"] = {
                "result": sorted_arr,
                "time_seconds": builtin_time / iterations,
                "time_milliseconds": (builtin_time / iterations) * 1000,
                "success": True,
            }
        except Exception as e:
            logger.error(f"Built-in sorted failed: {e}")
            results["builtin_sorted"] = {"success": False, "error": str(e)}

        return results


def main() -> None:
    """Main entry point for the script."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Heap data structure implementation with min-heap, "
        "max-heap, heapify operations, and heap sort"
    )
    parser.add_argument(
        "numbers",
        nargs="+",
        type=float,
        help="Numbers to operate on",
    )
    parser.add_argument(
        "-c",
        "--config",
        default="config.yaml",
        help="Path to configuration file (default: config.yaml)",
    )
    parser.add_argument(
        "-o",
        "--operation",
        choices=["minheap", "maxheap", "heapsort", "compare"],
        default="compare",
        help="Operation to perform (default: compare)",
    )
    parser.add_argument(
        "-d",
        "--direction",
        choices=["asc", "desc"],
        default="asc",
        help="Sort direction for heap sort (default: asc)",
    )
    parser.add_argument(
        "-i",
        "--iterations",
        type=int,
        default=1,
        help="Number of iterations for timing (default: 1)",
    )

    args = parser.parse_args()

    try:
        numbers = args.numbers

        logger.info(f"Input: {len(numbers)} numbers")

        if args.operation == "minheap":
            min_heap = MinHeap(numbers)
            print(f"Min-Heap built: {min_heap.heap}")
            print(f"Min element: {min_heap.peek()}")
            print("\nExtracting elements:")
            while not min_heap.is_empty():
                print(f"  {min_heap.extract_min()}")

        elif args.operation == "maxheap":
            max_heap = MaxHeap(numbers)
            print(f"Max-Heap built: {max_heap.heap}")
            print(f"Max element: {max_heap.peek()}")
            print("\nExtracting elements:")
            while not max_heap.is_empty():
                print(f"  {max_heap.extract_max()}")

        elif args.operation == "heapsort":
            heap_sort = HeapSort(config_path=args.config)
            if args.direction == "asc":
                sorted_arr = heap_sort.sort_ascending(numbers)
                print(f"Sorted (ascending): {sorted_arr}")
            else:
                sorted_arr = heap_sort.sort_descending(numbers)
                print(f"Sorted (descending): {sorted_arr}")

        elif args.operation == "compare":
            heap_sort = HeapSort(config_path=args.config)
            comparison = heap_sort.compare_with_builtin(
                numbers, args.iterations
            )

            print(f"\nHeap Sort Comparison:")
            print(f"Array length: {comparison['array_length']}")
            print(f"Iterations: {comparison['iterations']}")
            print("-" * 60)

            methods = [
                ("heap_sort_asc", "Heap Sort (Asc)"),
                ("heap_sort_desc", "Heap Sort (Desc)"),
                ("builtin_sorted", "Built-in sorted()"),
            ]

            for method_key, method_name in methods:
                data = comparison[method_key]
                if data.get("success", False):
                    result = data["result"]
                    result_str = (
                        f"{result[:5]}..." if len(result) > 5 else str(result)
                    )
                    print(
                        f"{method_name:20s}: {result_str:30s} "
                        f"({data['time_milliseconds']:8.4f} ms)"
                    )
                else:
                    print(
                        f"{method_name:20s}: Failed - "
                        f"{data.get('error', 'Unknown')}"
                    )

    except Exception as e:
        logger.error(f"Error during execution: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
