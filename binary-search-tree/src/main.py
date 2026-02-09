"""Binary Search Tree with Balancing and Performance Analysis.

This module provides implementation of binary search tree (BST) with AVL tree
balancing. It includes performance analysis comparing balanced vs unbalanced
trees, demonstrating the importance of tree balancing for optimal performance.
"""

import argparse
import logging
import logging.handlers
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class BSTNode:
    """Node class for binary search tree."""

    def __init__(self, value: Any) -> None:
        """Initialize BST node.

        Args:
            value: Value stored in the node.
        """
        self.value = value
        self.left: Optional['BSTNode'] = None
        self.right: Optional['BSTNode'] = None
        self.height: int = 0  # For AVL tree
        logger.debug(f"Created BSTNode with value: {value}")

    def __repr__(self) -> str:
        """String representation of node."""
        return f"BSTNode({self.value})"


class BST:
    """Binary Search Tree (unbalanced) implementation."""

    def __init__(self, config_path: str = "config.yaml") -> None:
        """Initialize BST with configuration.

        Args:
            config_path: Path to configuration YAML file.
        """
        self.root: Optional[BSTNode] = None
        self.config = self._load_config(config_path)
        self._setup_logging()
        self.operation_count: Dict[str, int] = {
            "comparisons": 0,
            "insertions": 0,
            "deletions": 0,
            "searches": 0,
        }
        logger.info("Initialized Binary Search Tree (unbalanced)")

    def _load_config(self, config_path: str) -> dict:
        """Load configuration from YAML file."""
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
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

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

    def _update_height(self, node: Optional[BSTNode]) -> int:
        """Update and return height of node."""
        if node is None:
            return -1
        node.height = 1 + max(
            self._update_height(node.left),
            self._update_height(node.right)
        )
        return node.height

    def insert(self, value: Any) -> bool:
        """Insert value into BST.

        Args:
            value: Value to insert.

        Returns:
            True if inserted, False if duplicate.
        """
        logger.info(f"Inserting value: {value}")
        self.operation_count["insertions"] += 1

        def _insert(node: Optional[BSTNode], val: Any) -> Tuple[Optional[BSTNode], bool]:
            """Recursive helper for insertion."""
            if node is None:
                return BSTNode(val), True

            self.operation_count["comparisons"] += 1
            if val < node.value:
                node.left, inserted = _insert(node.left, val)
            elif val > node.value:
                node.right, inserted = _insert(node.right, val)
            else:
                return node, False  # Duplicate

            return node, inserted

        self.root, inserted = _insert(self.root, value)
        self._update_height(self.root)
        return inserted

    def search(self, value: Any) -> bool:
        """Search for value in BST.

        Args:
            value: Value to search for.

        Returns:
            True if found, False otherwise.
        """
        logger.debug(f"Searching for value: {value}")
        self.operation_count["searches"] += 1

        def _search(node: Optional[BSTNode], val: Any) -> bool:
            """Recursive helper for search."""
            if node is None:
                return False

            self.operation_count["comparisons"] += 1
            if val == node.value:
                return True
            elif val < node.value:
                return _search(node.left, val)
            else:
                return _search(node.right, val)

        return _search(self.root, value)

    def delete(self, value: Any) -> bool:
        """Delete value from BST.

        Args:
            value: Value to delete.

        Returns:
            True if deleted, False if not found.
        """
        logger.info(f"Deleting value: {value}")
        self.operation_count["deletions"] += 1

        def _find_min(node: BSTNode) -> BSTNode:
            """Find minimum node in subtree."""
            while node.left:
                node = node.left
            return node

        def _delete(node: Optional[BSTNode], val: Any) -> Tuple[Optional[BSTNode], bool]:
            """Recursive helper for deletion."""
            if node is None:
                return None, False

            self.operation_count["comparisons"] += 1
            if val < node.value:
                node.left, deleted = _delete(node.left, val)
                return node, deleted
            elif val > node.value:
                node.right, deleted = _delete(node.right, val)
                return node, deleted
            else:
                # Node to delete found
                if node.left is None:
                    return node.right, True
                elif node.right is None:
                    return node.left, True
                else:
                    # Node has two children
                    min_node = _find_min(node.right)
                    node.value = min_node.value
                    node.right, _ = _delete(node.right, min_node.value)
                    return node, True

        self.root, deleted = _delete(self.root, value)
        if deleted:
            self._update_height(self.root)
        return deleted

    def inorder_traversal(self) -> List[Any]:
        """Perform inorder traversal (produces sorted order).

        Returns:
            List of values in sorted order.
        """
        result = []

        def _inorder(node: Optional[BSTNode]) -> None:
            if node:
                _inorder(node.left)
                result.append(node.value)
                _inorder(node.right)

        _inorder(self.root)
        return result

    def height(self) -> int:
        """Calculate height of BST.

        Returns:
            Height of tree.
        """
        def _height(node: Optional[BSTNode]) -> int:
            if node is None:
                return -1
            return 1 + max(_height(node.left), _height(node.right))

        return _height(self.root)

    def size(self) -> int:
        """Calculate number of nodes in BST.

        Returns:
            Number of nodes.
        """
        def _size(node: Optional[BSTNode]) -> int:
            if node is None:
                return 0
            return 1 + _size(node.left) + _size(node.right)

        return _size(self.root)

    def get_statistics(self) -> Dict[str, Any]:
        """Get performance statistics.

        Returns:
            Dictionary with performance statistics.
        """
        return {
            "height": self.height(),
            "size": self.size(),
            "operations": self.operation_count.copy(),
            "avg_comparisons_per_search": (
                self.operation_count["comparisons"] / max(self.operation_count["searches"], 1)
            ),
        }


class AVLTree:
    """AVL Tree (self-balancing BST) implementation."""

    def __init__(self, config_path: str = "config.yaml") -> None:
        """Initialize AVL tree with configuration.

        Args:
            config_path: Path to configuration YAML file.
        """
        self.root: Optional[BSTNode] = None
        self.config = self._load_config(config_path)
        self._setup_logging()
        self.operation_count: Dict[str, int] = {
            "comparisons": 0,
            "insertions": 0,
            "deletions": 0,
            "searches": 0,
            "rotations": 0,
        }
        logger.info("Initialized AVL Tree (balanced)")

    def _load_config(self, config_path: str) -> dict:
        """Load configuration from YAML file."""
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
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

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

    def _height(self, node: Optional[BSTNode]) -> int:
        """Get height of node."""
        if node is None:
            return -1
        return node.height

    def _update_height(self, node: Optional[BSTNode]) -> None:
        """Update height of node."""
        if node:
            node.height = 1 + max(
                self._height(node.left),
                self._height(node.right)
            )

    def _balance_factor(self, node: Optional[BSTNode]) -> int:
        """Calculate balance factor of node."""
        if node is None:
            return 0
        return self._height(node.left) - self._height(node.right)

    def _rotate_right(self, y: BSTNode) -> BSTNode:
        """Right rotation for AVL balancing."""
        self.operation_count["rotations"] += 1
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        self._update_height(y)
        self._update_height(x)

        return x

    def _rotate_left(self, x: BSTNode) -> BSTNode:
        """Left rotation for AVL balancing."""
        self.operation_count["rotations"] += 1
        y = x.right
        T2 = y.left

        y.left = x
        x.right = T2

        self._update_height(x)
        self._update_height(y)

        return y

    def insert(self, value: Any) -> bool:
        """Insert value into AVL tree with automatic balancing.

        Args:
            value: Value to insert.

        Returns:
            True if inserted, False if duplicate.
        """
        logger.info(f"Inserting value: {value} into AVL tree")
        self.operation_count["insertions"] += 1

        def _insert(node: Optional[BSTNode], val: Any) -> Tuple[Optional[BSTNode], bool]:
            """Recursive helper for insertion."""
            if node is None:
                return BSTNode(val), True

            self.operation_count["comparisons"] += 1
            if val < node.value:
                node.left, inserted = _insert(node.left, val)
            elif val > node.value:
                node.right, inserted = _insert(node.right, val)
            else:
                return node, False  # Duplicate

            self._update_height(node)

            # Balance factor
            balance = self._balance_factor(node)

            # Left Left Case
            if balance > 1 and val < node.left.value:
                return self._rotate_right(node), inserted

            # Right Right Case
            if balance < -1 and val > node.right.value:
                return self._rotate_left(node), inserted

            # Left Right Case
            if balance > 1 and val > node.left.value:
                node.left = self._rotate_left(node.left)
                return self._rotate_right(node), inserted

            # Right Left Case
            if balance < -1 and val < node.right.value:
                node.right = self._rotate_right(node.right)
                return self._rotate_left(node), inserted

            return node, inserted

        self.root, inserted = _insert(self.root, value)
        return inserted

    def search(self, value: Any) -> bool:
        """Search for value in AVL tree.

        Args:
            value: Value to search for.

        Returns:
            True if found, False otherwise.
        """
        logger.debug(f"Searching for value: {value} in AVL tree")
        self.operation_count["searches"] += 1

        def _search(node: Optional[BSTNode], val: Any) -> bool:
            """Recursive helper for search."""
            if node is None:
                return False

            self.operation_count["comparisons"] += 1
            if val == node.value:
                return True
            elif val < node.value:
                return _search(node.left, val)
            else:
                return _search(node.right, val)

        return _search(self.root, value)

    def delete(self, value: Any) -> bool:
        """Delete value from AVL tree with automatic balancing.

        Args:
            value: Value to delete.

        Returns:
            True if deleted, False if not found.
        """
        logger.info(f"Deleting value: {value} from AVL tree")
        self.operation_count["deletions"] += 1

        def _find_min(node: BSTNode) -> BSTNode:
            """Find minimum node in subtree."""
            while node.left:
                node = node.left
            return node

        def _delete(node: Optional[BSTNode], val: Any) -> Tuple[Optional[BSTNode], bool]:
            """Recursive helper for deletion."""
            if node is None:
                return None, False

            self.operation_count["comparisons"] += 1
            if val < node.value:
                node.left, deleted = _delete(node.left, val)
            elif val > node.value:
                node.right, deleted = _delete(node.right, val)
            else:
                # Node to delete found
                if node.left is None:
                    return node.right, True
                elif node.right is None:
                    return node.left, True
                else:
                    # Node has two children
                    min_node = _find_min(node.right)
                    node.value = min_node.value
                    node.right, _ = _delete(node.right, min_node.value)
                    deleted = True

            if node is None:
                return None, deleted

            self._update_height(node)

            # Balance factor
            balance = self._balance_factor(node)

            # Left Left Case
            if balance > 1 and self._balance_factor(node.left) >= 0:
                return self._rotate_right(node), deleted

            # Left Right Case
            if balance > 1 and self._balance_factor(node.left) < 0:
                node.left = self._rotate_left(node.left)
                return self._rotate_right(node), deleted

            # Right Right Case
            if balance < -1 and self._balance_factor(node.right) <= 0:
                return self._rotate_left(node), deleted

            # Right Left Case
            if balance < -1 and self._balance_factor(node.right) > 0:
                node.right = self._rotate_right(node.right)
                return self._rotate_left(node), deleted

            return node, deleted

        self.root, deleted = _delete(self.root, value)
        return deleted

    def inorder_traversal(self) -> List[Any]:
        """Perform inorder traversal (produces sorted order).

        Returns:
            List of values in sorted order.
        """
        result = []

        def _inorder(node: Optional[BSTNode]) -> None:
            if node:
                _inorder(node.left)
                result.append(node.value)
                _inorder(node.right)

        _inorder(self.root)
        return result

    def height(self) -> int:
        """Calculate height of AVL tree.

        Returns:
            Height of tree.
        """
        return self._height(self.root)

    def size(self) -> int:
        """Calculate number of nodes in AVL tree.

        Returns:
            Number of nodes.
        """
        def _size(node: Optional[BSTNode]) -> int:
            if node is None:
                return 0
            return 1 + _size(node.left) + _size(node.right)

        return _size(self.root)

    def get_statistics(self) -> Dict[str, Any]:
        """Get performance statistics.

        Returns:
            Dictionary with performance statistics.
        """
        return {
            "height": self.height(),
            "size": self.size(),
            "operations": self.operation_count.copy(),
            "avg_comparisons_per_search": (
                self.operation_count["comparisons"] / max(self.operation_count["searches"], 1)
            ),
            "rotations": self.operation_count["rotations"],
        }


class PerformanceAnalyzer:
    """Performance analyzer for comparing BST vs AVL Tree."""

    def __init__(self) -> None:
        """Initialize performance analyzer."""
        self.results: Dict[str, Any] = {}

    def compare_trees(
        self, values: List[Any], search_values: Optional[List[Any]] = None
    ) -> Dict[str, Any]:
        """Compare performance of BST vs AVL Tree.

        Args:
            values: Values to insert into both trees.
            search_values: Optional values to search for.

        Returns:
            Dictionary with comparison results.
        """
        logger.info("Starting performance comparison")

        # Test BST
        bst = BST()
        bst_start = time.perf_counter()

        for val in values:
            bst.insert(val)

        bst_insert_time = time.perf_counter() - bst_start

        bst_search_time = 0.0
        if search_values:
            bst_start = time.perf_counter()
            for val in search_values:
                bst.search(val)
            bst_search_time = time.perf_counter() - bst_start

        bst_stats = bst.get_statistics()

        # Test AVL Tree
        avl = AVLTree()
        avl_start = time.perf_counter()

        for val in values:
            avl.insert(val)

        avl_insert_time = time.perf_counter() - avl_start

        avl_search_time = 0.0
        if search_values:
            avl_start = time.perf_counter()
            for val in search_values:
                avl.search(val)
            avl_search_time = time.perf_counter() - avl_start

        avl_stats = avl.get_statistics()

        results = {
            "bst": {
                "insert_time": bst_insert_time,
                "search_time": bst_search_time,
                "height": bst_stats["height"],
                "size": bst_stats["size"],
                "comparisons": bst_stats["operations"]["comparisons"],
                "avg_comparisons_per_search": bst_stats["avg_comparisons_per_search"],
            },
            "avl": {
                "insert_time": avl_insert_time,
                "search_time": avl_search_time,
                "height": avl_stats["height"],
                "size": avl_stats["size"],
                "comparisons": avl_stats["operations"]["comparisons"],
                "avg_comparisons_per_search": avl_stats["avg_comparisons_per_search"],
                "rotations": avl_stats["rotations"],
            },
            "improvement": {
                "height_reduction": bst_stats["height"] - avl_stats["height"],
                "height_ratio": (
                    avl_stats["height"] / max(bst_stats["height"], 1)
                ),
                "search_time_improvement": (
                    (bst_search_time - avl_search_time) / max(bst_search_time, 0.000001) * 100
                    if search_values else 0
                ),
            },
        }

        self.results = results
        return results

    def generate_report(self, output_path: Optional[str] = None) -> str:
        """Generate performance analysis report.

        Args:
            output_path: Optional path to save report.

        Returns:
            Report content as string.
        """
        if not self.results:
            return "No performance data available. Run comparison first."

        report_lines = [
            "=" * 80,
            "BINARY SEARCH TREE PERFORMANCE ANALYSIS REPORT",
            "=" * 80,
            "",
            "COMPARISON RESULTS",
            "-" * 80,
            "",
            "BINARY SEARCH TREE (Unbalanced):",
            f"  Height: {self.results['bst']['height']}",
            f"  Size: {self.results['bst']['size']}",
            f"  Insert Time: {self.results['bst']['insert_time']:.10f} seconds",
            f"  Search Time: {self.results['bst']['search_time']:.10f} seconds",
            f"  Total Comparisons: {self.results['bst']['comparisons']}",
            f"  Avg Comparisons per Search: {self.results['bst']['avg_comparisons_per_search']:.2f}",
            "",
            "AVL TREE (Balanced):",
            f"  Height: {self.results['avl']['height']}",
            f"  Size: {self.results['avl']['size']}",
            f"  Insert Time: {self.results['avl']['insert_time']:.10f} seconds",
            f"  Search Time: {self.results['avl']['search_time']:.10f} seconds",
            f"  Total Comparisons: {self.results['avl']['comparisons']}",
            f"  Avg Comparisons per Search: {self.results['avl']['avg_comparisons_per_search']:.2f}",
            f"  Rotations Performed: {self.results['avl']['rotations']}",
            "",
            "IMPROVEMENT METRICS",
            "-" * 80,
            f"  Height Reduction: {self.results['improvement']['height_reduction']} levels",
            f"  Height Ratio (AVL/BST): {self.results['improvement']['height_ratio']:.2f}",
            f"  Search Time Improvement: {self.results['improvement']['search_time_improvement']:.2f}%",
            "",
            "ANALYSIS",
            "-" * 80,
            "BALANCING BENEFITS:",
            "  - AVL tree maintains O(log n) height guarantee",
            "  - Unbalanced BST can degrade to O(n) height in worst case",
            "  - Balanced tree provides consistent O(log n) search time",
            "  - Rotations add overhead but ensure optimal structure",
            "",
            "TIME COMPLEXITY:",
            "  - BST (worst case): O(n) for search, insert, delete",
            "  - BST (average case): O(log n) for search, insert, delete",
            "  - AVL (worst case): O(log n) for search, insert, delete",
            "  - AVL (average case): O(log n) for search, insert, delete",
            "",
            "SPACE COMPLEXITY:",
            "  - Both: O(n) for storing n nodes",
            "  - AVL: Additional O(1) per node for height tracking",
            "",
            "WHEN TO USE:",
            "  - Use BST when data is randomly ordered",
            "  - Use AVL when data may be sorted or sequential",
            "  - Use AVL when guaranteed O(log n) performance is critical",
            "  - Use BST when simplicity is preferred and data is random",
        ]

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
        description="Binary Search Tree with balancing and performance analysis"
    )
    parser.add_argument(
        "-c",
        "--config",
        default="config.yaml",
        help="Path to configuration file (default: config.yaml)",
    )
    parser.add_argument(
        "-i",
        "--insert",
        nargs="+",
        help="Values to insert into tree",
    )
    parser.add_argument(
        "-d",
        "--delete",
        help="Value to delete from tree",
    )
    parser.add_argument(
        "-s",
        "--search",
        help="Value to search for in tree",
    )
    parser.add_argument(
        "--type",
        choices=["bst", "avl", "both"],
        default="both",
        help="Tree type to use (default: both)",
    )
    parser.add_argument(
        "--compare",
        action="store_true",
        help="Compare BST vs AVL performance",
    )
    parser.add_argument(
        "-r",
        "--report",
        help="Output path for analysis report",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run demonstration with example trees",
    )

    args = parser.parse_args()

    try:
        if args.demo:
            print("\n=== Binary Search Tree Demonstration ===\n")

            # Demo values
            demo_values = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45]
            print(f"Inserting values: {demo_values}")

            if args.type in ["bst", "both"]:
                print("\n--- Binary Search Tree (Unbalanced) ---")
                bst = BST(config_path=args.config)
                for val in demo_values:
                    bst.insert(val)

                print(f"Inorder (sorted): {bst.inorder_traversal()}")
                print(f"Height: {bst.height()}")
                print(f"Size: {bst.size()}")
                stats = bst.get_statistics()
                print(f"Statistics: {stats}")

            if args.type in ["avl", "both"]:
                print("\n--- AVL Tree (Balanced) ---")
                avl = AVLTree(config_path=args.config)
                for val in demo_values:
                    avl.insert(val)

                print(f"Inorder (sorted): {avl.inorder_traversal()}")
                print(f"Height: {avl.height()}")
                print(f"Size: {avl.size()}")
                stats = avl.get_statistics()
                print(f"Statistics: {stats}")

            if args.compare or args.type == "both":
                print("\n--- Performance Comparison ---")
                analyzer = PerformanceAnalyzer()
                search_vals = [10, 50, 80, 25, 100]
                results = analyzer.compare_trees(demo_values, search_vals)
                print(f"BST Height: {results['bst']['height']}")
                print(f"AVL Height: {results['avl']['height']}")
                print(f"Height Reduction: {results['improvement']['height_reduction']}")
                print(f"AVL Rotations: {results['avl']['rotations']}")

                if args.report:
                    report = analyzer.generate_report(output_path=args.report)
                    print(f"\nReport saved to {args.report}")

        else:
            print("Use --demo for demonstration")
            print("BST operations available:")
            print("  - insert(value)")
            print("  - delete(value)")
            print("  - search(value)")
            print("  - inorder_traversal()")

    except Exception as e:
        logger.error(f"Error during execution: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
