"""Link-Cut Tree (Dynamic Tree) for Maintaining Forests with Link and Cut Operations.

This module provides functionality to implement link-cut tree data structure
that maintains a forest of trees and supports efficient link, cut, and path
operations. Link-cut trees achieve O(log n) amortized time complexity for
all operations using splay trees.
"""

import logging
import logging.handlers
from pathlib import Path
from typing import List, Optional

import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class LinkCutNode:
    """Node in link-cut tree."""

    def __init__(self, value: int, data: float = 0.0) -> None:
        """Initialize link-cut node.

        Args:
            value: Node value/identifier.
            data: Data stored in node.
        """
        self.value = value
        self.data = data
        self.path_parent: Optional["LinkCutNode"] = None
        self.left: Optional["LinkCutNode"] = None
        self.right: Optional["LinkCutNode"] = None
        self.parent: Optional["LinkCutNode"] = None
        self.reversed = False

    def is_root(self) -> bool:
        """Check if node is root of its splay tree.

        Returns:
            True if root, False otherwise.
        """
        return self.parent is None or (
            self.parent.left != self and self.parent.right != self
        )

    def __repr__(self) -> str:
        """String representation."""
        return f"LinkCutNode({self.value}, data={self.data})"


class LinkCutTree:
    """Link-cut tree for maintaining dynamic forests."""

    def __init__(self, config_path: str = "config.yaml") -> None:
        """Initialize link-cut tree.

        Args:
            config_path: Path to configuration file.
        """
        self.nodes: List[LinkCutNode] = []
        self._setup_logging()
        self._load_config(config_path)

    def _setup_logging(self) -> None:
        """Configure logging for link-cut tree operations."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        handler = logging.handlers.RotatingFileHandler(
            log_dir / "link_cut_tree.log",
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

    def create_node(self, value: int, data: float = 0.0) -> LinkCutNode:
        """Create a new node.

        Args:
            value: Node value.
            data: Node data.

        Returns:
            Created node.
        """
        node = LinkCutNode(value, data)
        self.nodes.append(node)
        logger.info(f"Created node: {node.value}")
        return node

    def _push_reverse(self, node: Optional[LinkCutNode]) -> None:
        """Push reverse flag to children.

        Args:
            node: Node to push reverse flag from.
        """
        if node and node.reversed:
            node.reversed = False
            node.left, node.right = node.right, node.left
            if node.left:
                node.left.reversed = not node.left.reversed
            if node.right:
                node.right.reversed = not node.right.reversed

    def _rotate(self, node: LinkCutNode) -> None:
        """Rotate node in splay tree.

        Args:
            node: Node to rotate.
        """
        parent = node.parent
        if parent is None:
            return

        self._push_reverse(parent)
        self._push_reverse(node)

        grandparent = parent.parent

        if parent.left == node:
            parent.left = node.right
            if node.right:
                node.right.parent = parent
            node.right = parent
        else:
            parent.right = node.left
            if node.left:
                node.left.parent = parent
            node.left = parent

        parent.parent = node
        node.parent = grandparent

        if grandparent:
            if grandparent.left == parent:
                grandparent.left = node
            elif grandparent.right == parent:
                grandparent.right = node

    def _splay(self, node: LinkCutNode) -> None:
        """Splay node to root of its splay tree.

        Args:
            node: Node to splay.
        """
        while not node.is_root():
            parent = node.parent
            if parent.is_root():
                self._rotate(node)
            else:
                grandparent = parent.parent
                if (parent.left == node) == (grandparent.left == parent):
                    self._rotate(parent)
                    self._rotate(node)
                else:
                    self._rotate(node)
                    self._rotate(node)

    def _access(self, node: LinkCutNode) -> None:
        """Access node, making it root of its auxiliary tree.

        Args:
            node: Node to access.
        """
        self._splay(node)
        self._push_reverse(node)

        if node.right:
            node.right.path_parent = node
            node.right.parent = None
            node.right = None

        while node.path_parent:
            parent_path = node.path_parent
            self._splay(parent_path)
            self._push_reverse(parent_path)

            if parent_path.right:
                parent_path.right.path_parent = parent_path
                parent_path.right.parent = None

            parent_path.right = node
            node.parent = parent_path
            node.path_parent = None
            self._splay(node)

    def find_root(self, node: LinkCutNode) -> LinkCutNode:
        """Find root of tree containing node.

        Args:
            node: Node to find root for.

        Returns:
            Root node.
        """
        self._access(node)
        while node.left:
            node = node.left
        self._splay(node)
        logger.info(f"Found root for node {node.value}: {node.value}")
        return node

    def link(self, child: LinkCutNode, parent: LinkCutNode) -> bool:
        """Link child to parent.

        Args:
            child: Child node.
            parent: Parent node.

        Returns:
            True if linked, False if already connected.

        Raises:
            ValueError: If nodes are in same tree.
        """
        if self.find_root(child) == self.find_root(parent):
            logger.warning(f"Nodes {child.value} and {parent.value} already connected")
            return False

        self._access(child)
        self._access(parent)

        child.left = parent
        parent.parent = child
        logger.info(f"Linked node {child.value} to {parent.value}")
        return True

    def cut(self, node: LinkCutNode) -> bool:
        """Cut edge from node to its parent.

        Args:
            node: Node to cut from parent.

        Returns:
            True if cut, False if node is root.
        """
        self._access(node)

        if node.left is None:
            logger.warning(f"Node {node.value} has no parent to cut")
            return False

        node.left.parent = None
        node.left = None
        logger.info(f"Cut node {node.value} from parent")
        return True

    def _query_subtree(self, node: LinkCutNode) -> float:
        """Query subtree in splay tree.

        Args:
            node: Root of subtree.

        Returns:
            Sum of data in subtree.
        """
        if node is None:
            return 0.0
        result = node.data
        if node.left:
            result += self._query_subtree(node.left)
        if node.right:
            result += self._query_subtree(node.right)
        return result

    def path_query(self, u: LinkCutNode, v: LinkCutNode) -> float:
        """Query path from u to v.

        Args:
            u: First node.
            v: Second node.

        Returns:
            Sum of data along path.
        """
        if u == v:
            return u.data

        if not self.are_connected(u, v):
            logger.warning(f"Nodes {u.value} and {v.value} not connected")
            return 0.0

        self._access(u)
        self._access(v)
        self._splay(v)

        result = self._query_subtree(v)
        logger.info(f"Path query from {u.value} to {v.value}: {result}")
        return result

    def _update_subtree(self, node: LinkCutNode, value: float) -> None:
        """Update subtree in splay tree.

        Args:
            node: Root of subtree.
            value: Value to add.
        """
        if node:
            node.data += value
            if node.left:
                self._update_subtree(node.left, value)
            if node.right:
                self._update_subtree(node.right, value)

    def path_update(self, u: LinkCutNode, v: LinkCutNode, value: float) -> None:
        """Update path from u to v by adding value.

        Args:
            u: First node.
            v: Second node.
            value: Value to add.
        """
        if u == v:
            u.data += value
            return

        if not self.are_connected(u, v):
            logger.warning(f"Nodes {u.value} and {v.value} not connected")
            return

        self._access(u)
        self._access(v)
        self._splay(v)

        self._update_subtree(v, value)
        logger.info(f"Path update from {u.value} to {v.value} with value {value}")

    def get_path_nodes(self, u: LinkCutNode, v: LinkCutNode) -> List[LinkCutNode]:
        """Get all nodes on path from u to v.

        Args:
            u: First node.
            v: Second node.

        Returns:
            List of nodes on path.
        """
        self._access(u)
        self._access(v)

        if u == v:
            return [u]

        path = []
        current = u
        visited = set()

        while current and current not in visited:
            visited.add(current)
            path.append(current)
            if current == v:
                break
            current = current.path_parent or current.parent

        if v not in path:
            path.append(v)

        logger.info(f"Path from {u.value} to {v.value}: {[n.value for n in path]}")
        return path

    def are_connected(self, u: LinkCutNode, v: LinkCutNode) -> bool:
        """Check if two nodes are in same tree.

        Args:
            u: First node.
            v: Second node.

        Returns:
            True if connected, False otherwise.
        """
        root_u = self.find_root(u)
        root_v = self.find_root(v)
        return root_u == root_v


def main() -> None:
    """Main function to demonstrate link-cut tree operations."""
    tree = LinkCutTree()

    print("Link-Cut Tree Operations Demo")
    print("=" * 50)

    nodes = [tree.create_node(i) for i in range(7)]

    print("\nLinking nodes:")
    tree.link(nodes[1], nodes[0])
    tree.link(nodes[2], nodes[0])
    tree.link(nodes[3], nodes[1])
    tree.link(nodes[4], nodes[1])
    tree.link(nodes[5], nodes[2])
    tree.link(nodes[6], nodes[2])

    print("\nFinding roots:")
    root1 = tree.find_root(nodes[3])
    root2 = tree.find_root(nodes[5])
    print(f"Root of node 3: {root1.value}")
    print(f"Root of node 5: {root2.value}")

    print("\nChecking connectivity:")
    connected = tree.are_connected(nodes[3], nodes[5])
    print(f"Nodes 3 and 5 connected: {connected}")

    print("\nPath query:")
    result = tree.path_query(nodes[3], nodes[5])
    print(f"Path sum: {result}")

    print("\nCutting edge:")
    tree.cut(nodes[1])

    print("\nChecking connectivity after cut:")
    connected = tree.are_connected(nodes[3], nodes[0])
    print(f"Nodes 3 and 0 connected: {connected}")


if __name__ == "__main__":
    main()
