"""AVL Tree (Self-Balancing Binary Search Tree).

This module provides functionality to implement AVL tree data structure
with rotation operations for self-balancing. AVL trees maintain balance
by ensuring the height difference between left and right subtrees is at
most 1 for all nodes.
"""

import logging
import logging.handlers
import time
from pathlib import Path
from typing import Dict, List, Optional

import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class AVLNode:
    """Node in AVL tree."""

    def __init__(self, key: float) -> None:
        """Initialize AVLNode.

        Args:
            key: Node key value.
        """
        self.key = key
        self.left: Optional["AVLNode"] = None
        self.right: Optional["AVLNode"] = None
        self.height = 1

    def __repr__(self) -> str:
        """String representation."""
        return f"AVLNode(key={self.key}, height={self.height})"


class AVLTree:
    """AVL tree (self-balancing binary search tree)."""

    def __init__(self, config_path: str = "config.yaml") -> None:
        """Initialize AVLTree with configuration.

        Args:
            config_path: Path to configuration YAML file.

        Raises:
            FileNotFoundError: If config file doesn't exist.
            yaml.YAMLError: If config file is invalid YAML.
        """
        self.root: Optional[AVLNode] = None
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

    def _get_height(self, node: Optional[AVLNode]) -> int:
        """Get height of node.

        Args:
            node: Node to get height for.

        Returns:
            Height of node (0 if None).
        """
        if node is None:
            return 0
        return node.height

    def _get_balance(self, node: Optional[AVLNode]) -> int:
        """Get balance factor of node.

        Args:
            node: Node to get balance factor for.

        Returns:
            Balance factor (height difference).
        """
        if node is None:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _update_height(self, node: AVLNode) -> None:
        """Update height of node.

        Args:
            node: Node to update height for.
        """
        node.height = 1 + max(
            self._get_height(node.left), self._get_height(node.right)
        )

    def _rotate_right(self, y: AVLNode) -> AVLNode:
        """Right rotation.

        Args:
            y: Root of subtree to rotate.

        Returns:
            New root after rotation.
        """
        x = y.left
        T2 = x.right if x else None

        # Perform rotation
        x.right = y
        y.left = T2

        # Update heights
        self._update_height(y)
        if x:
            self._update_height(x)

        logger.debug(f"Right rotation at node {y.key}")
        return x

    def _rotate_left(self, x: AVLNode) -> AVLNode:
        """Left rotation.

        Args:
            x: Root of subtree to rotate.

        Returns:
            New root after rotation.
        """
        y = x.right
        T2 = y.left if y else None

        # Perform rotation
        y.left = x
        x.right = T2

        # Update heights
        self._update_height(x)
        if y:
            self._update_height(y)

        logger.debug(f"Left rotation at node {x.key}")
        return y

    def _insert_node(self, node: Optional[AVLNode], key: float) -> AVLNode:
        """Insert node recursively with balancing.

        Args:
            node: Current node.
            key: Key to insert.

        Returns:
            Root of subtree after insertion and balancing.
        """
        # Perform standard BST insert
        if node is None:
            new_node = AVLNode(key)
            logger.debug(f"  Inserted new node with key {key}")
            return new_node

        if key < node.key:
            node.left = self._insert_node(node.left, key)
        elif key > node.key:
            node.right = self._insert_node(node.right, key)
        else:
            # Duplicate keys not allowed
            logger.debug(f"  Key {key} already exists")
            return node

        # Update height
        self._update_height(node)

        # Get balance factor
        balance = self._get_balance(node)

        # Left Left Case
        if balance > 1 and key < node.left.key:
            logger.debug(f"  Left-Left case at node {node.key}")
            return self._rotate_right(node)

        # Right Right Case
        if balance < -1 and key > node.right.key:
            logger.debug(f"  Right-Right case at node {node.key}")
            return self._rotate_left(node)

        # Left Right Case
        if balance > 1 and key > node.left.key:
            logger.debug(f"  Left-Right case at node {node.key}")
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        # Right Left Case
        if balance < -1 and key < node.right.key:
            logger.debug(f"  Right-Left case at node {node.key}")
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def insert(self, key: float) -> None:
        """Insert key into AVL tree.

        Args:
            key: Key to insert.
        """
        logger.info(f"Inserting key: {key}")
        self.root = self._insert_node(self.root, key)
        logger.info(f"Insertion complete, tree height: {self._get_height(self.root)}")

    def _min_value_node(self, node: AVLNode) -> AVLNode:
        """Find node with minimum value in subtree.

        Args:
            node: Root of subtree.

        Returns:
            Node with minimum value.
        """
        current = node
        while current.left is not None:
            current = current.left
        return current

    def _delete_node(self, node: Optional[AVLNode], key: float) -> Optional[AVLNode]:
        """Delete node recursively with balancing.

        Args:
            node: Current node.
            key: Key to delete.

        Returns:
            Root of subtree after deletion and balancing.
        """
        # Perform standard BST delete
        if node is None:
            return node

        if key < node.key:
            node.left = self._delete_node(node.left, key)
        elif key > node.key:
            node.right = self._delete_node(node.right, key)
        else:
            # Node to delete found
            logger.debug(f"  Deleting node with key {key}")

            # Node with one child or no child
            if node.left is None:
                temp = node.right
                node = None
                return temp
            elif node.right is None:
                temp = node.left
                node = None
                return temp

            # Node with two children: get inorder successor
            temp = self._min_value_node(node.right)
            node.key = temp.key
            node.right = self._delete_node(node.right, temp.key)

        # If tree had only one node, return
        if node is None:
            return node

        # Update height
        self._update_height(node)

        # Get balance factor
        balance = self._get_balance(node)

        # Left Left Case
        if balance > 1 and self._get_balance(node.left) >= 0:
            logger.debug(f"  Left-Left case at node {node.key}")
            return self._rotate_right(node)

        # Left Right Case
        if balance > 1 and self._get_balance(node.left) < 0:
            logger.debug(f"  Left-Right case at node {node.key}")
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        # Right Right Case
        if balance < -1 and self._get_balance(node.right) <= 0:
            logger.debug(f"  Right-Right case at node {node.key}")
            return self._rotate_left(node)

        # Right Left Case
        if balance < -1 and self._get_balance(node.right) > 0:
            logger.debug(f"  Right-Left case at node {node.key}")
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def delete(self, key: float) -> bool:
        """Delete key from AVL tree.

        Args:
            key: Key to delete.

        Returns:
            True if key was deleted, False if not found.
        """
        logger.info(f"Deleting key: {key}")
        if self.search(key):
            self.root = self._delete_node(self.root, key)
            logger.info(f"Deletion complete, tree height: {self._get_height(self.root)}")
            return True
        else:
            logger.warning(f"Key {key} not found for deletion")
            return False

    def search(self, key: float) -> bool:
        """Search for key in AVL tree.

        Args:
            key: Key to search for.

        Returns:
            True if key exists, False otherwise.
        """
        return self._search_node(self.root, key)

    def _search_node(self, node: Optional[AVLNode], key: float) -> bool:
        """Search for key recursively.

        Args:
            node: Current node.
            key: Key to search for.

        Returns:
            True if key exists, False otherwise.
        """
        if node is None:
            return False

        if key == node.key:
            return True
        elif key < node.key:
            return self._search_node(node.left, key)
        else:
            return self._search_node(node.right, key)

    def inorder_traversal(self) -> List[float]:
        """Get inorder traversal of tree.

        Returns:
            List of keys in inorder (sorted order).
        """
        result: List[float] = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node: Optional[AVLNode], result: List[float]) -> None:
        """Inorder traversal helper.

        Args:
            node: Current node.
            result: List to append keys to.
        """
        if node is not None:
            self._inorder(node.left, result)
            result.append(node.key)
            self._inorder(node.right, result)

    def preorder_traversal(self) -> List[float]:
        """Get preorder traversal of tree.

        Returns:
            List of keys in preorder.
        """
        result: List[float] = []
        self._preorder(self.root, result)
        return result

    def _preorder(self, node: Optional[AVLNode], result: List[float]) -> None:
        """Preorder traversal helper.

        Args:
            node: Current node.
            result: List to append keys to.
        """
        if node is not None:
            result.append(node.key)
            self._preorder(node.left, result)
            self._preorder(node.right, result)

    def postorder_traversal(self) -> List[float]:
        """Get postorder traversal of tree.

        Returns:
            List of keys in postorder.
        """
        result: List[float] = []
        self._postorder(self.root, result)
        return result

    def _postorder(self, node: Optional[AVLNode], result: List[float]) -> None:
        """Postorder traversal helper.

        Args:
            node: Current node.
            result: List to append keys to.
        """
        if node is not None:
            self._postorder(node.left, result)
            self._postorder(node.right, result)
            result.append(node.key)

    def get_height(self) -> int:
        """Get height of tree.

        Returns:
            Height of tree.
        """
        return self._get_height(self.root)

    def is_balanced(self) -> bool:
        """Check if tree is balanced.

        Returns:
            True if tree is balanced, False otherwise.
        """
        return self._is_balanced_node(self.root)

    def _is_balanced_node(self, node: Optional[AVLNode]) -> bool:
        """Check if node and its subtrees are balanced.

        Args:
            node: Node to check.

        Returns:
            True if balanced, False otherwise.
        """
        if node is None:
            return True

        balance = self._get_balance(node)
        if abs(balance) > 1:
            return False

        return self._is_balanced_node(node.left) and self._is_balanced_node(
            node.right
        )

    def build_from_list(self, keys: List[float]) -> None:
        """Build AVL tree from list of keys.

        Args:
            keys: List of keys to insert.
        """
        logger.info(f"Building AVL tree from {len(keys)} keys")
        for key in keys:
            self.insert(key)
        logger.info(f"Tree built with height: {self.get_height()}")

    def compare_performance(
        self, keys: List[float], search_keys: List[float], iterations: int = 1
    ) -> Dict[str, any]:
        """Compare performance of AVL tree operations.

        Args:
            keys: List of keys to insert.
            search_keys: List of keys to search for.
            iterations: Number of iterations for timing (default: 1).

        Returns:
            Dictionary containing performance data.
        """
        logger.info(
            f"Performance comparison: {len(keys)} insertions, "
            f"{len(search_keys)} searches, iterations={iterations}"
        )

        results = {
            "num_keys": len(keys),
            "num_searches": len(search_keys),
            "iterations": iterations,
            "insert": {},
            "search": {},
            "delete": {},
        }

        # Insert operations
        try:
            start_time = time.perf_counter()
            for _ in range(iterations):
                tree = AVLTree(config_path=self.config.get("config_path", "config.yaml"))
                for key in keys:
                    tree.insert(key)
            insert_time = time.perf_counter() - start_time

            results["insert"] = {
                "time_seconds": insert_time / iterations,
                "time_milliseconds": (insert_time / iterations) * 1000,
                "time_per_insert_microseconds": (
                    (insert_time / iterations) / len(keys) * 1000000
                ),
                "final_height": self.get_height(),
                "success": True,
            }
        except Exception as e:
            logger.error(f"Insert operations failed: {e}")
            results["insert"] = {"success": False, "error": str(e)}

        # Build tree for search and delete operations
        tree = AVLTree(config_path=self.config.get("config_path", "config.yaml"))
        for key in keys:
            tree.insert(key)

        # Search operations
        try:
            start_time = time.perf_counter()
            for _ in range(iterations):
                for key in search_keys:
                    tree.search(key)
            search_time = time.perf_counter() - start_time

            results["search"] = {
                "operations": len(search_keys) * iterations,
                "time_seconds": search_time / iterations,
                "time_milliseconds": (search_time / iterations) * 1000,
                "time_per_search_microseconds": (
                    (search_time / iterations) / len(search_keys) * 1000000
                ),
                "success": True,
            }
        except Exception as e:
            logger.error(f"Search operations failed: {e}")
            results["search"] = {"success": False, "error": str(e)}

        # Delete operations
        try:
            delete_keys = keys[: min(10, len(keys))]
            start_time = time.perf_counter()
            for _ in range(iterations):
                temp_tree = AVLTree(
                    config_path=self.config.get("config_path", "config.yaml")
                )
                for key in keys:
                    temp_tree.insert(key)
                for key in delete_keys:
                    temp_tree.delete(key)
            delete_time = time.perf_counter() - start_time

            results["delete"] = {
                "operations": len(delete_keys) * iterations,
                "time_seconds": delete_time / iterations,
                "time_milliseconds": (delete_time / iterations) * 1000,
                "time_per_delete_microseconds": (
                    (delete_time / iterations) / len(delete_keys) * 1000000
                ),
                "success": True,
            }
        except Exception as e:
            logger.error(f"Delete operations failed: {e}")
            results["delete"] = {"success": False, "error": str(e)}

        return results

    def generate_report(
        self,
        performance_data: Dict[str, any],
        output_path: Optional[str] = None,
    ) -> str:
        """Generate performance report for AVL tree operations.

        Args:
            performance_data: Performance data from compare_performance().
            output_path: Optional path to save report file.

        Returns:
            Report content as string.
        """
        report_lines = [
            "=" * 80,
            "AVL TREE PERFORMANCE REPORT",
            "=" * 80,
            "",
            f"Number of keys: {performance_data['num_keys']}",
            f"Number of searches: {performance_data['num_searches']}",
            f"Iterations: {performance_data['iterations']}",
            "",
            "RESULTS",
            "-" * 80,
        ]

        # Insert
        report_lines.append("\ninsert():")
        insert_data = performance_data["insert"]
        if insert_data.get("success", False):
            report_lines.append(
                f"  Time: {insert_data['time_milliseconds']:.4f} ms "
                f"({insert_data['time_seconds']:.6f} seconds)"
            )
            report_lines.append(
                f"  Time per insert: "
                f"{insert_data['time_per_insert_microseconds']:.2f} μs"
            )
            report_lines.append(f"  Final tree height: {insert_data['final_height']}")
        else:
            report_lines.append(f"  Status: Failed")
            report_lines.append(f"  Error: {insert_data.get('error', 'Unknown')}")

        # Search
        report_lines.append("\nsearch():")
        search_data = performance_data["search"]
        if search_data.get("success", False):
            report_lines.append(f"  Operations: {search_data['operations']}")
            report_lines.append(
                f"  Time: {search_data['time_milliseconds']:.4f} ms "
                f"({search_data['time_seconds']:.6f} seconds)"
            )
            report_lines.append(
                f"  Time per search: "
                f"{search_data['time_per_search_microseconds']:.2f} μs"
            )
        else:
            report_lines.append(f"  Status: Failed")
            report_lines.append(f"  Error: {search_data.get('error', 'Unknown')}")

        # Delete
        report_lines.append("\ndelete():")
        delete_data = performance_data["delete"]
        if delete_data.get("success", False):
            report_lines.append(f"  Operations: {delete_data['operations']}")
            report_lines.append(
                f"  Time: {delete_data['time_milliseconds']:.4f} ms "
                f"({delete_data['time_seconds']:.6f} seconds)"
            )
            report_lines.append(
                f"  Time per delete: "
                f"{delete_data['time_per_delete_microseconds']:.2f} μs"
            )
        else:
            report_lines.append(f"  Status: Failed")
            report_lines.append(f"  Error: {delete_data.get('error', 'Unknown')}")

        report_lines.extend([
            "",
            "ALGORITHM COMPLEXITY",
            "-" * 80,
            "AVL Tree Operations:",
            "  Insert: O(log n) where n=number of nodes",
            "  Delete: O(log n) where n=number of nodes",
            "  Search: O(log n) where n=number of nodes",
            "  Space Complexity: O(n) for storing nodes",
            "",
            "Rotation Operations:",
            "  Left Rotation: O(1)",
            "  Right Rotation: O(1)",
            "  Left-Right Rotation: O(1)",
            "  Right-Left Rotation: O(1)",
            "",
            "Key Features:",
            "  - Self-balancing binary search tree",
            "  - Height difference at most 1 for all nodes",
            "  - Guaranteed O(log n) operations",
            "  - Maintains sorted order",
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
        description="AVL tree (self-balancing binary search tree) with "
        "rotation operations"
    )
    parser.add_argument(
        "keys",
        nargs="+",
        type=float,
        help="Keys to insert into AVL tree",
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
        choices=["insert", "search", "delete", "traverse", "compare", "all"],
        default="all",
        help="Operation to perform (default: all)",
    )
    parser.add_argument(
        "-k",
        "--key",
        type=float,
        help="Key for search or delete operation",
    )
    parser.add_argument(
        "-t",
        "--traversal",
        choices=["inorder", "preorder", "postorder"],
        default="inorder",
        help="Traversal type (default: inorder)",
    )
    parser.add_argument(
        "-i",
        "--iterations",
        type=int,
        default=1,
        help="Number of iterations for timing (default: 1)",
    )
    parser.add_argument(
        "-r",
        "--report",
        help="Output path for performance report",
    )

    args = parser.parse_args()

    try:
        avl = AVLTree(config_path=args.config)

        keys = args.keys

        logger.info(f"Input: {len(keys)} keys")

        if args.operation == "insert":
            avl.build_from_list(keys)
            print(f"Inserted {len(keys)} keys into AVL tree")
            print(f"Tree height: {avl.get_height()}")
            print(f"Tree is balanced: {avl.is_balanced()}")

        elif args.operation == "search":
            avl.build_from_list(keys)
            if args.key is not None:
                result = avl.search(args.key)
                print(f"Search for {args.key}: {result}")
            else:
                print("No key specified for search. Use --key option")

        elif args.operation == "delete":
            avl.build_from_list(keys)
            if args.key is not None:
                result = avl.delete(args.key)
                print(f"Delete {args.key}: {result}")
                print(f"Tree height: {avl.get_height()}")
                print(f"Tree is balanced: {avl.is_balanced()}")
            else:
                print("No key specified for delete. Use --key option")

        elif args.operation == "traverse":
            avl.build_from_list(keys)
            if args.traversal == "inorder":
                traversal = avl.inorder_traversal()
            elif args.traversal == "preorder":
                traversal = avl.preorder_traversal()
            else:
                traversal = avl.postorder_traversal()
            print(f"{args.traversal.capitalize()} traversal: {traversal}")

        elif args.operation == "compare":
            search_keys = keys[: min(10, len(keys))]
            performance = avl.compare_performance(keys, search_keys, args.iterations)

            print(f"\nAVL Tree Performance Comparison:")
            print(f"Keys: {performance['num_keys']}")
            print(f"Searches: {performance['num_searches']}")
            print("-" * 60)

            methods = [
                ("insert", "insert()"),
                ("search", "search()"),
                ("delete", "delete()"),
            ]

            for method_key, method_name in methods:
                data = performance[method_key]
                if data.get("success", False):
                    if method_key == "insert":
                        print(
                            f"{method_name:20s}: "
                            f"{data['time_milliseconds']:8.4f} ms "
                            f"({data['time_per_insert_microseconds']:.2f} μs/insert) "
                            f"height={data['final_height']}"
                        )
                    elif method_key == "search":
                        print(
                            f"{method_name:20s}: "
                            f"{data['time_milliseconds']:8.4f} ms "
                            f"({data['time_per_search_microseconds']:.2f} μs/search)"
                        )
                    else:
                        print(
                            f"{method_name:20s}: "
                            f"{data['time_milliseconds']:8.4f} ms "
                            f"({data['time_per_delete_microseconds']:.2f} μs/delete)"
                        )
                else:
                    print(
                        f"{method_name:20s}: Failed - "
                        f"{data.get('error', 'Unknown')}"
                    )

            if args.report:
                report = avl.generate_report(
                    performance, output_path=args.report
                )
                print(f"\nReport saved to {args.report}")

        elif args.operation == "all":
            avl.build_from_list(keys)
            print(f"AVL Tree Statistics:")
            print(f"  Number of keys: {len(keys)}")
            print(f"  Tree height: {avl.get_height()}")
            print(f"  Tree is balanced: {avl.is_balanced()}")
            print(f"  Inorder traversal: {avl.inorder_traversal()}")

            if args.key is not None:
                result = avl.search(args.key)
                print(f"\nSearch for {args.key}: {result}")

    except Exception as e:
        logger.error(f"Error during execution: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
