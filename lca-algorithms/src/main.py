"""LCA (Lowest Common Ancestor) Algorithms using Binary Lifting and Euler Tour.

This module provides functionality to implement LCA algorithms using two
different techniques: binary lifting and Euler tour. Both algorithms achieve
O(log n) query time complexity with different preprocessing approaches.
"""

import logging
import logging.handlers
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class TreeNode:
    """Node in a tree."""

    def __init__(self, value: int) -> None:
        """Initialize tree node.

        Args:
            value: Node value.
        """
        self.value = value
        self.children: List["TreeNode"] = []
        self.parent: Optional["TreeNode"] = None

    def add_child(self, child: "TreeNode") -> None:
        """Add child node.

        Args:
            child: Child node to add.
        """
        child.parent = self
        self.children.append(child)

    def __repr__(self) -> str:
        """String representation."""
        return f"TreeNode({self.value})"


class LCABinaryLifting:
    """LCA using binary lifting technique."""

    def __init__(self, root: TreeNode, config_path: str = "config.yaml") -> None:
        """Initialize LCA with binary lifting.

        Args:
            root: Root of the tree.
            config_path: Path to configuration file.
        """
        self.root = root
        self.n = self._count_nodes(root)
        self.max_log = (self.n).bit_length()
        self.parent: List[List[int]] = []
        self.depth: List[int] = []
        self.node_to_index: Dict[TreeNode, int] = {}
        self.index_to_node: Dict[int, TreeNode] = {}
        self._setup_logging()
        self._load_config(config_path)
        self._preprocess()

    def _setup_logging(self) -> None:
        """Configure logging for LCA operations."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        handler = logging.handlers.RotatingFileHandler(
            log_dir / "lca.log",
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

    def _count_nodes(self, node: Optional[TreeNode]) -> int:
        """Count nodes in tree.

        Args:
            node: Current node.

        Returns:
            Number of nodes.
        """
        if node is None:
            return 0
        count = 1
        for child in node.children:
            count += self._count_nodes(child)
        return count

    def _index_nodes(self, node: Optional[TreeNode], index: int) -> int:
        """Assign indices to nodes.

        Args:
            node: Current node.
            index: Current index.

        Returns:
            Next available index.
        """
        if node is None:
            return index

        self.node_to_index[node] = index
        self.index_to_node[index] = node
        current_index = index
        index += 1

        for child in node.children:
            index = self._index_nodes(child, index)

        return index

    def _dfs(self, node: Optional[TreeNode], parent_idx: int, d: int) -> None:
        """Perform DFS to compute depth and parent table.

        Args:
            node: Current node.
            parent_idx: Parent index.
            d: Current depth.
        """
        if node is None:
            return

        node_idx = self.node_to_index[node]
        self.depth[node_idx] = d
        self.parent[node_idx][0] = parent_idx

        for child in node.children:
            child_idx = self.node_to_index[child]
            self._dfs(child, node_idx, d + 1)

    def _preprocess(self) -> None:
        """Preprocess tree for binary lifting."""
        self._index_nodes(self.root, 0)

        self.parent = [[-1] * self.max_log for _ in range(self.n)]
        self.depth = [0] * self.n

        root_idx = self.node_to_index[self.root]
        self._dfs(self.root, -1, 0)

        for j in range(1, self.max_log):
            for i in range(self.n):
                if self.parent[i][j - 1] != -1:
                    self.parent[i][j] = self.parent[self.parent[i][j - 1]][j - 1]

        logger.info(f"Preprocessed tree with {self.n} nodes using binary lifting")

    def _lift(self, node_idx: int, k: int) -> int:
        """Lift node up by k levels.

        Args:
            node_idx: Node index.
            k: Number of levels to lift.

        Returns:
            Index of node after lifting.
        """
        for i in range(self.max_log):
            if k & (1 << i):
                if node_idx == -1:
                    return -1
                node_idx = self.parent[node_idx][i]
        return node_idx

    def lca(self, u: TreeNode, v: TreeNode) -> Optional[TreeNode]:
        """Find lowest common ancestor of two nodes.

        Args:
            u: First node.
            v: Second node.

        Returns:
            LCA node or None if nodes not in tree.
        """
        if u not in self.node_to_index or v not in self.node_to_index:
            logger.warning("One or both nodes not in tree")
            return None

        u_idx = self.node_to_index[u]
        v_idx = self.node_to_index[v]

        if self.depth[u_idx] < self.depth[v_idx]:
            u_idx, v_idx = v_idx, u_idx

        u_idx = self._lift(u_idx, self.depth[u_idx] - self.depth[v_idx])

        if u_idx == v_idx:
            result = self.index_to_node[u_idx]
            logger.info(f"LCA of {u.value} and {v.value}: {result.value}")
            return result

        for i in range(self.max_log - 1, -1, -1):
            if self.parent[u_idx][i] != self.parent[v_idx][i]:
                u_idx = self.parent[u_idx][i]
                v_idx = self.parent[v_idx][i]

        lca_idx = self.parent[u_idx][0]
        result = self.index_to_node[lca_idx]
        logger.info(f"LCA of {u.value} and {v.value}: {result.value}")
        return result


class LCAEulerTour:
    """LCA using Euler tour technique."""

    def __init__(self, root: TreeNode, config_path: str = "config.yaml") -> None:
        """Initialize LCA with Euler tour.

        Args:
            root: Root of the tree.
            config_path: Path to configuration file.
        """
        self.root = root
        self.euler_tour: List[int] = []
        self.depth: List[int] = []
        self.first_occurrence: Dict[int, int] = {}
        self.node_to_value: Dict[TreeNode, int] = {}
        self.value_to_node: Dict[int, TreeNode] = {}
        self._setup_logging()
        self._load_config(config_path)
        self._preprocess()

    def _setup_logging(self) -> None:
        """Configure logging for LCA operations."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        handler = logging.handlers.RotatingFileHandler(
            log_dir / "lca.log",
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

    def _euler_tour_dfs(
        self, node: Optional[TreeNode], d: int
    ) -> None:
        """Perform Euler tour DFS.

        Args:
            node: Current node.
            d: Current depth.
        """
        if node is None:
            return

        value = node.value
        self.node_to_value[node] = value
        self.value_to_node[value] = node

        if value not in self.first_occurrence:
            self.first_occurrence[value] = len(self.euler_tour)

        self.euler_tour.append(value)
        self.depth.append(d)

        for child in node.children:
            self._euler_tour_dfs(child, d + 1)
            self.euler_tour.append(value)
            self.depth.append(d)

    def _preprocess(self) -> None:
        """Preprocess tree for Euler tour."""
        self._euler_tour_dfs(self.root, 0)

        n = len(self.euler_tour)
        self.log_n = (n).bit_length()
        self.sparse_table: List[List[int]] = [[0] * n for _ in range(self.log_n)]

        for i in range(n):
            self.sparse_table[0][i] = i

        for j in range(1, self.log_n):
            for i in range(n - (1 << j) + 1):
                left = self.sparse_table[j - 1][i]
                right = self.sparse_table[j - 1][i + (1 << (j - 1))]
                if self.depth[left] < self.depth[right]:
                    self.sparse_table[j][i] = left
                else:
                    self.sparse_table[j][i] = right

        logger.info(f"Preprocessed tree with Euler tour of length {n}")

    def _rmq(self, left: int, right: int) -> int:
        """Range minimum query on depth array.

        Args:
            left: Left index.
            right: Right index.

        Returns:
            Index of minimum depth in range.
        """
        length = right - left + 1
        k = (length).bit_length() - 1
        idx1 = self.sparse_table[k][left]
        idx2 = self.sparse_table[k][right - (1 << k) + 1]

        if self.depth[idx1] < self.depth[idx2]:
            return idx1
        return idx2

    def lca(self, u: TreeNode, v: TreeNode) -> Optional[TreeNode]:
        """Find lowest common ancestor of two nodes.

        Args:
            u: First node.
            v: Second node.

        Returns:
            LCA node or None if nodes not in tree.
        """
        if u not in self.node_to_value or v not in self.node_to_value:
            logger.warning("One or both nodes not in tree")
            return None

        u_value = self.node_to_value[u]
        v_value = self.node_to_value[v]

        if u_value not in self.first_occurrence or v_value not in self.first_occurrence:
            logger.warning("Nodes not found in Euler tour")
            return None

        first_u = self.first_occurrence[u_value]
        first_v = self.first_occurrence[v_value]

        if first_u > first_v:
            first_u, first_v = first_v, first_u

        min_idx = self._rmq(first_u, first_v)
        lca_value = self.euler_tour[min_idx]
        result = self.value_to_node[lca_value]
        logger.info(f"LCA of {u.value} and {v.value}: {result.value}")
        return result


def build_tree_from_edges(
    n: int, edges: List[Tuple[int, int]], root_value: int = 0
) -> TreeNode:
    """Build tree from list of edges.

    Args:
        n: Number of nodes.
        edges: List of (parent, child) edges.
        root_value: Value of root node.

    Returns:
        Root node of tree.

    Raises:
        ValueError: If invalid tree structure.
    """
    nodes: Dict[int, TreeNode] = {}
    for i in range(n):
        nodes[i] = TreeNode(i)

    children_count: Dict[int, int] = {}
    for parent, child in edges:
        if parent not in nodes or child not in nodes:
            raise ValueError(f"Invalid edge: ({parent}, {child})")
        nodes[parent].add_child(nodes[child])
        children_count[child] = children_count.get(child, 0) + 1

    if root_value not in nodes:
        raise ValueError(f"Root value {root_value} not in nodes")

    root = nodes[root_value]
    logger.info(f"Built tree with {n} nodes, root: {root_value}")
    return root


def main() -> None:
    """Main function to demonstrate LCA algorithms."""
    print("LCA Algorithms Demo")
    print("=" * 50)

    n = 7
    edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)]
    root = build_tree_from_edges(n, edges, 0)

    print("\nTree structure:")
    print("      0")
    print("    /   \\")
    print("   1     2")
    print("  / \\   / \\")
    print(" 3   4 5   6")

    print("\n=== Binary Lifting LCA ===")
    lca_bl = LCABinaryLifting(root)
    node3 = root.children[0].children[0]
    node4 = root.children[0].children[1]
    node5 = root.children[1].children[0]
    node6 = root.children[1].children[1]

    lca_result = lca_bl.lca(node3, node4)
    print(f"LCA(3, 4) = {lca_result.value if lca_result else None}")

    lca_result = lca_bl.lca(node3, node5)
    print(f"LCA(3, 5) = {lca_result.value if lca_result else None}")

    lca_result = lca_bl.lca(node5, node6)
    print(f"LCA(5, 6) = {lca_result.value if lca_result else None}")

    print("\n=== Euler Tour LCA ===")
    lca_et = LCAEulerTour(root)

    lca_result = lca_et.lca(node3, node4)
    print(f"LCA(3, 4) = {lca_result.value if lca_result else None}")

    lca_result = lca_et.lca(node3, node5)
    print(f"LCA(3, 5) = {lca_result.value if lca_result else None}")

    lca_result = lca_et.lca(node5, node6)
    print(f"LCA(5, 6) = {lca_result.value if lca_result else None}")


if __name__ == "__main__":
    main()
