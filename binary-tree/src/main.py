"""Binary Tree Data Structure - Insertion, Deletion, and Traversals.

This module provides implementation of a binary tree data structure
with insertion, deletion, and three traversal methods: inorder, preorder, and postorder.
The binary tree maintains the property that each node has at most two children.
"""

import argparse
import logging
import logging.handlers
from pathlib import Path
from typing import Any, List, Optional

import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class TreeNode:
    """Node class for binary tree."""

    def __init__(self, value: Any) -> None:
        """Initialize tree node.

        Args:
            value: Value stored in the node.
        """
        self.value = value
        self.left: Optional['TreeNode'] = None
        self.right: Optional['TreeNode'] = None
        logger.debug(f"Created TreeNode with value: {value}")

    def __repr__(self) -> str:
        """String representation of node."""
        return f"TreeNode({self.value})"


class BinaryTree:
    """Binary tree data structure with insertion, deletion, and traversal methods."""

    def __init__(self, config_path: str = "config.yaml") -> None:
        """Initialize binary tree with configuration.

        Args:
            config_path: Path to configuration YAML file.

        Raises:
            FileNotFoundError: If config file doesn't exist.
            yaml.YAMLError: If config file is invalid YAML.
        """
        self.root: Optional[TreeNode] = None
        self.config = self._load_config(config_path)
        self._setup_logging()
        logger.info("Initialized BinaryTree")

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

    def insert(self, value: Any) -> None:
        """Insert value into binary tree.

        Inserts value using level-order insertion (breadth-first).
        Finds first available position to maintain complete tree structure.

        Args:
            value: Value to insert.
        """
        logger.info(f"Inserting value: {value}")

        new_node = TreeNode(value)

        if self.root is None:
            self.root = new_node
            logger.debug(f"Inserted {value} as root")
            return

        # Level-order insertion: find first available position
        queue = [self.root]

        while queue:
            current = queue.pop(0)

            if current.left is None:
                current.left = new_node
                logger.debug(f"Inserted {value} as left child of {current.value}")
                return
            elif current.right is None:
                current.right = new_node
                logger.debug(f"Inserted {value} as right child of {current.value}")
                return
            else:
                queue.append(current.left)
                queue.append(current.right)

    def delete(self, value: Any) -> bool:
        """Delete value from binary tree.

        Deletes the node containing the value and replaces it with the
        rightmost node at the deepest level to maintain tree structure.

        Args:
            value: Value to delete.

        Returns:
            True if value was found and deleted, False otherwise.
        """
        logger.info(f"Deleting value: {value}")

        if self.root is None:
            logger.warning("Cannot delete from empty tree")
            return False

        # Find node to delete and rightmost deepest node
        node_to_delete = None
        rightmost_node = None
        rightmost_parent = None

        queue = [(self.root, None)]

        while queue:
            current, parent = queue.pop(0)

            if current.value == value:
                node_to_delete = current

            # Track rightmost node at deepest level
            rightmost_node = current
            rightmost_parent = parent

            if current.left:
                queue.append((current.left, current))
            if current.right:
                queue.append((current.right, current))

        if node_to_delete is None:
            logger.warning(f"Value {value} not found in tree")
            return False

        # Replace node_to_delete with rightmost_node
        node_to_delete.value = rightmost_node.value

        # Remove rightmost_node
        if rightmost_parent is None:
            # Rightmost node is root
            self.root = None
        elif rightmost_parent.right == rightmost_node:
            rightmost_parent.right = None
        else:
            rightmost_parent.left = None

        logger.info(f"Deleted value: {value}")
        return True

    def search(self, value: Any) -> bool:
        """Search for value in binary tree.

        Args:
            value: Value to search for.

        Returns:
            True if value found, False otherwise.
        """
        logger.debug(f"Searching for value: {value}")

        if self.root is None:
            return False

        queue = [self.root]

        while queue:
            current = queue.pop(0)

            if current.value == value:
                logger.debug(f"Found value: {value}")
                return True

            if current.left:
                queue.append(current.left)
            if current.right:
                queue.append(current.right)

        logger.debug(f"Value {value} not found")
        return False

    def inorder_traversal(self) -> List[Any]:
        """Perform inorder traversal (Left, Root, Right).

        Returns:
            List of values in inorder traversal order.
        """
        logger.info("Performing inorder traversal")
        result = []

        def _inorder(node: Optional[TreeNode]) -> None:
            """Recursive helper for inorder traversal."""
            if node is None:
                return

            _inorder(node.left)
            result.append(node.value)
            _inorder(node.right)

        _inorder(self.root)
        logger.debug(f"Inorder traversal: {result}")
        return result

    def preorder_traversal(self) -> List[Any]:
        """Perform preorder traversal (Root, Left, Right).

        Returns:
            List of values in preorder traversal order.
        """
        logger.info("Performing preorder traversal")
        result = []

        def _preorder(node: Optional[TreeNode]) -> None:
            """Recursive helper for preorder traversal."""
            if node is None:
                return

            result.append(node.value)
            _preorder(node.left)
            _preorder(node.right)

        _preorder(self.root)
        logger.debug(f"Preorder traversal: {result}")
        return result

    def postorder_traversal(self) -> List[Any]:
        """Perform postorder traversal (Left, Right, Root).

        Returns:
            List of values in postorder traversal order.
        """
        logger.info("Performing postorder traversal")
        result = []

        def _postorder(node: Optional[TreeNode]) -> None:
            """Recursive helper for postorder traversal."""
            if node is None:
                return

            _postorder(node.left)
            _postorder(node.right)
            result.append(node.value)

        _postorder(self.root)
        logger.debug(f"Postorder traversal: {result}")
        return result

    def level_order_traversal(self) -> List[Any]:
        """Perform level-order traversal (breadth-first).

        Returns:
            List of values in level-order traversal order.
        """
        logger.info("Performing level-order traversal")
        result = []

        if self.root is None:
            return result

        queue = [self.root]

        while queue:
            current = queue.pop(0)
            result.append(current.value)

            if current.left:
                queue.append(current.left)
            if current.right:
                queue.append(current.right)

        logger.debug(f"Level-order traversal: {result}")
        return result

    def height(self) -> int:
        """Calculate height of binary tree.

        Returns:
            Height of tree (number of edges in longest path from root to leaf).
        """
        def _height(node: Optional[TreeNode]) -> int:
            """Recursive helper to calculate height."""
            if node is None:
                return -1

            left_height = _height(node.left)
            right_height = _height(node.right)

            return 1 + max(left_height, right_height)

        tree_height = _height(self.root)
        logger.debug(f"Tree height: {tree_height}")
        return tree_height

    def size(self) -> int:
        """Calculate number of nodes in binary tree.

        Returns:
            Number of nodes in tree.
        """
        def _size(node: Optional[TreeNode]) -> int:
            """Recursive helper to calculate size."""
            if node is None:
                return 0

            return 1 + _size(node.left) + _size(node.right)

        tree_size = _size(self.root)
        logger.debug(f"Tree size: {tree_size}")
        return tree_size

    def visualize(self) -> str:
        """Generate visual representation of binary tree.

        Returns:
            String representation of tree structure.
        """
        if self.root is None:
            return "Tree is empty"

        lines = []
        lines.append("Binary Tree Structure:")
        lines.append("=" * 50)

        def _visualize(node: Optional[TreeNode], prefix: str = "", is_last: bool = True) -> None:
            """Recursive helper for tree visualization."""
            if node is None:
                return

            lines.append(prefix + ("└── " if is_last else "├── ") + str(node.value))

            if node.left or node.right:
                extension = prefix + ("    " if is_last else "│   ")
                if node.right:
                    _visualize(node.left, extension, node.right is None)
                    _visualize(node.right, extension, True)
                else:
                    _visualize(node.left, extension, True)

        _visualize(self.root)
        lines.append("=" * 50)
        lines.append(f"Size: {self.size()}")
        lines.append(f"Height: {self.height()}")

        return "\n".join(lines)

    def generate_report(
        self,
        output_path: Optional[str] = None,
    ) -> str:
        """Generate detailed binary tree analysis report.

        Args:
            output_path: Optional path to save report file.

        Returns:
            Report content as string.
        """
        report_lines = [
            "=" * 80,
            "BINARY TREE ANALYSIS REPORT",
            "=" * 80,
            "",
        ]

        if self.root is None:
            report_lines.append("Tree is empty")
        else:
            report_lines.extend([
                "TREE STRUCTURE",
                "-" * 80,
                self.visualize(),
                "",
                "TRAVERSAL RESULTS",
                "-" * 80,
                f"Inorder (Left, Root, Right): {self.inorder_traversal()}",
                f"Preorder (Root, Left, Right): {self.preorder_traversal()}",
                f"Postorder (Left, Right, Root): {self.postorder_traversal()}",
                f"Level-order (Breadth-first): {self.level_order_traversal()}",
                "",
                "TREE PROPERTIES",
                "-" * 80,
                f"Size (number of nodes): {self.size()}",
                f"Height (longest path): {self.height()}",
                "",
                "TRAVERSAL EXPLANATIONS",
                "-" * 80,
                "INORDER:",
                "  - Visit left subtree",
                "  - Visit root",
                "  - Visit right subtree",
                "  - For BST: produces sorted order",
                "",
                "PREORDER:",
                "  - Visit root",
                "  - Visit left subtree",
                "  - Visit right subtree",
                "  - Useful for copying tree structure",
                "",
                "POSTORDER:",
                "  - Visit left subtree",
                "  - Visit right subtree",
                "  - Visit root",
                "  - Useful for deleting tree",
                "",
                "LEVEL-ORDER:",
                "  - Visit nodes level by level",
                "  - Left to right at each level",
                "  - Breadth-first traversal",
                "",
                "APPLICATIONS",
                "-" * 80,
                "1. Expression trees (arithmetic expressions)",
                "2. Binary Search Trees (BST)",
                "3. Heap data structures",
                "4. Decision trees",
                "5. File system hierarchies",
                "6. Parse trees (compilers)",
                "7. Game trees",
                "8. Organizational hierarchies",
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
        description="Binary tree data structure with insertion, deletion, and traversals"
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
        "--inorder",
        action="store_true",
        help="Perform inorder traversal",
    )
    parser.add_argument(
        "--preorder",
        action="store_true",
        help="Perform preorder traversal",
    )
    parser.add_argument(
        "--postorder",
        action="store_true",
        help="Perform postorder traversal",
    )
    parser.add_argument(
        "--levelorder",
        action="store_true",
        help="Perform level-order traversal",
    )
    parser.add_argument(
        "-v",
        "--visualize",
        action="store_true",
        help="Show tree visualization",
    )
    parser.add_argument(
        "-r",
        "--report",
        help="Output path for analysis report",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run demonstration with example tree",
    )

    args = parser.parse_args()

    try:
        tree = BinaryTree(config_path=args.config)

        if args.demo:
            # Run demonstration
            print("\n=== Binary Tree Demonstration ===\n")

            # Insert values
            demo_values = [10, 5, 15, 3, 7, 12, 18, 2, 4, 6, 8]
            print(f"Inserting values: {demo_values}")
            for value in demo_values:
                tree.insert(value)

            if args.visualize:
                print("\n" + tree.visualize())

            print("\nTraversal Results:")
            print(f"  Inorder: {tree.inorder_traversal()}")
            print(f"  Preorder: {tree.preorder_traversal()}")
            print(f"  Postorder: {tree.postorder_traversal()}")
            print(f"  Level-order: {tree.level_order_traversal()}")

            print(f"\nTree Properties:")
            print(f"  Size: {tree.size()}")
            print(f"  Height: {tree.height()}")

            # Search demonstration
            search_value = 7
            found = tree.search(search_value)
            print(f"\nSearch for {search_value}: {'Found' if found else 'Not found'}")

            # Delete demonstration
            delete_value = 5
            print(f"\nDeleting value: {delete_value}")
            deleted = tree.delete(delete_value)
            if deleted:
                print(f"Value {delete_value} deleted successfully")
                if args.visualize:
                    print("\n" + tree.visualize())
                print(f"\nAfter deletion - Inorder: {tree.inorder_traversal()}")

            if args.report:
                report = tree.generate_report(output_path=args.report)
                print(f"\nReport saved to {args.report}")

        else:
            # Interactive mode
            if args.insert:
                for value in args.insert:
                    try:
                        # Try to convert to int, fallback to string
                        try:
                            val = int(value)
                        except ValueError:
                            val = value
                        tree.insert(val)
                        print(f"Inserted: {val}")
                    except Exception as e:
                        logger.error(f"Error inserting {value}: {e}")

            if args.delete:
                try:
                    try:
                        val = int(args.delete)
                    except ValueError:
                        val = args.delete
                    if tree.delete(val):
                        print(f"Deleted: {val}")
                    else:
                        print(f"Value {val} not found in tree")
                except Exception as e:
                    logger.error(f"Error deleting {args.delete}: {e}")

            if args.search:
                try:
                    try:
                        val = int(args.search)
                    except ValueError:
                        val = args.search
                    if tree.search(val):
                        print(f"Found: {val}")
                    else:
                        print(f"Not found: {val}")
                except Exception as e:
                    logger.error(f"Error searching {args.search}: {e}")

            if args.inorder:
                print(f"Inorder: {tree.inorder_traversal()}")

            if args.preorder:
                print(f"Preorder: {tree.preorder_traversal()}")

            if args.postorder:
                print(f"Postorder: {tree.postorder_traversal()}")

            if args.levelorder:
                print(f"Level-order: {tree.level_order_traversal()}")

            if args.visualize:
                print("\n" + tree.visualize())

            if args.report:
                report = tree.generate_report(output_path=args.report)
                print(f"\nReport saved to {args.report}")

            if not any([args.insert, args.delete, args.search, args.inorder,
                       args.preorder, args.postorder, args.levelorder,
                       args.visualize, args.report]):
                print("Use --demo for demonstration")
                print("Binary tree operations available:")
                print("  - insert(value)")
                print("  - delete(value)")
                print("  - search(value)")
                print("  - inorder_traversal()")
                print("  - preorder_traversal()")
                print("  - postorder_traversal()")
                print("  - level_order_traversal()")

    except Exception as e:
        logger.error(f"Error during execution: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
