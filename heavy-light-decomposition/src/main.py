"""Heavy-Light Decomposition for Efficient Path Queries and Updates on Trees.

This module provides functionality to implement heavy-light decomposition
(HLD) that decomposes a tree into chains for efficient path queries and
updates. HLD achieves O(log^2 n) time complexity for path operations.
"""

import logging
import logging.handlers
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class TreeNode:
    """Node in a tree."""

    def __init__(self, value: int, data: float = 0.0) -> None:
        """Initialize tree node.

        Args:
            value: Node value/identifier.
            data: Data stored in node.
        """
        self.value = value
        self.data = data
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
        return f"TreeNode({self.value}, data={self.data})"


class SegmentTree:
    """Segment tree for range queries and updates."""

    def __init__(
        self,
        size: int,
        operation: Callable[[float, float], float] = lambda x, y: x + y,
        identity: float = 0.0,
    ) -> None:
        """Initialize segment tree.

        Args:
            size: Size of array.
            operation: Binary operation (default: addition).
            identity: Identity element for operation.
        """
        self.n = size
        self.operation = operation
        self.identity = identity
        self.size = 1
        while self.size < self.n:
            self.size *= 2
        self.tree = [identity] * (2 * self.size)
        self.lazy = [identity] * (2 * self.size)

    def _apply(self, idx: int, value: float) -> None:
        """Apply lazy update.

        Args:
            idx: Index in segment tree.
            value: Value to apply.
        """
        self.tree[idx] = self.operation(self.tree[idx], value)
        if idx < self.size:
            self.lazy[idx] = self.operation(self.lazy[idx], value)

    def _push(self, idx: int) -> None:
        """Push lazy update to children.

        Args:
            idx: Index in segment tree.
        """
        if self.lazy[idx] != self.identity:
            self._apply(2 * idx, self.lazy[idx])
            self._apply(2 * idx + 1, self.lazy[idx])
            self.lazy[idx] = self.identity

    def _build(self, arr: List[float]) -> None:
        """Build segment tree from array.

        Args:
            arr: Input array.
        """
        for i in range(self.n):
            self.tree[self.size + i] = arr[i]
        for i in range(self.size - 1, 0, -1):
            self.tree[i] = self.operation(
                self.tree[2 * i], self.tree[2 * i + 1]
            )

    def update_range(
        self, left: int, right: int, value: float
    ) -> None:
        """Update range [left, right] with value.

        Args:
            left: Left index (inclusive).
            right: Right index (inclusive).
            value: Value to apply.
        """
        left += self.size
        right += self.size
        l0, r0 = left, right

        while left <= right:
            if left % 2 == 1:
                self._apply(left, value)
                left += 1
            if right % 2 == 0:
                self._apply(right, value)
                right -= 1
            left //= 2
            right //= 2

        left, right = l0, r0
        while left > 1:
            left //= 2
            right //= 2
            self._push(left)
            self._push(right)
            if left < right:
                self.tree[left] = self.operation(
                    self.tree[2 * left], self.tree[2 * left + 1]
                )
                self.tree[right] = self.operation(
                    self.tree[2 * right], self.tree[2 * right + 1]
                )

    def query_range(self, left: int, right: int) -> float:
        """Query range [left, right].

        Args:
            left: Left index (inclusive).
            right: Right index (inclusive).

        Returns:
            Result of operation over range.
        """
        left += self.size
        right += self.size
        result = self.identity

        self._push(left)
        self._push(right)

        while left <= right:
            if left % 2 == 1:
                result = self.operation(result, self.tree[left])
                left += 1
            if right % 2 == 0:
                result = self.operation(result, self.tree[right])
                right -= 1
            left //= 2
            right //= 2

        return result


class HeavyLightDecomposition:
    """Heavy-light decomposition for path queries and updates."""

    def __init__(self, root: TreeNode, config_path: str = "config.yaml") -> None:
        """Initialize heavy-light decomposition.

        Args:
            root: Root of the tree.
            config_path: Path to configuration file.
        """
        self.root = root
        self.n = self._count_nodes(root)
        self.subtree_size: Dict[TreeNode, int] = {}
        self.parent: Dict[TreeNode, Optional[TreeNode]] = {}
        self.depth: Dict[TreeNode, int] = {}
        self.heavy_child: Dict[TreeNode, Optional[TreeNode]] = {}
        self.chain_head: Dict[TreeNode, TreeNode] = {}
        self.chain_pos: Dict[TreeNode, int] = {}
        self.chains: List[List[TreeNode]] = []
        self.chain_segment_trees: List[SegmentTree] = []
        self.node_to_chain: Dict[TreeNode, int] = {}
        self._setup_logging()
        self._load_config(config_path)
        self._decompose()

    def _setup_logging(self) -> None:
        """Configure logging for HLD operations."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        handler = logging.handlers.RotatingFileHandler(
            log_dir / "hld.log",
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

    def _dfs_size(self, node: TreeNode, parent: Optional[TreeNode], d: int) -> None:
        """DFS to compute subtree sizes and depths.

        Args:
            node: Current node.
            parent: Parent node.
            d: Current depth.
        """
        self.parent[node] = parent
        self.depth[node] = d
        self.subtree_size[node] = 1
        self.heavy_child[node] = None

        max_size = 0
        for child in node.children:
            self._dfs_size(child, node, d + 1)
            self.subtree_size[node] += self.subtree_size[child]
            if self.subtree_size[child] > max_size:
                max_size = self.subtree_size[child]
                self.heavy_child[node] = child

    def _dfs_chains(self, node: TreeNode, chain_id: int) -> None:
        """DFS to build chains.

        Args:
            node: Current node.
            chain_id: Current chain ID.
        """
        if chain_id >= len(self.chains):
            self.chains.append([])

        self.chains[chain_id].append(node)
        self.node_to_chain[node] = chain_id
        self.chain_pos[node] = len(self.chains[chain_id]) - 1
        self.chain_head[node] = self.chains[chain_id][0]

        if self.heavy_child[node]:
            self._dfs_chains(self.heavy_child[node], chain_id)

        for child in node.children:
            if child != self.heavy_child[node]:
                self._dfs_chains(child, len(self.chains))

    def _decompose(self) -> None:
        """Perform heavy-light decomposition."""
        self._dfs_size(self.root, None, 0)
        self._dfs_chains(self.root, 0)

        for chain in self.chains:
            chain_data = [node.data for node in chain]
            seg_tree = SegmentTree(len(chain))
            seg_tree._build(chain_data)
            self.chain_segment_trees.append(seg_tree)

        logger.info(
            f"Decomposed tree into {len(self.chains)} chains with {self.n} nodes"
        )

    def _lca(self, u: TreeNode, v: TreeNode) -> TreeNode:
        """Find lowest common ancestor.

        Args:
            u: First node.
            v: Second node.

        Returns:
            LCA node.
        """
        while self.node_to_chain[u] != self.node_to_chain[v]:
            if (
                self.depth[self.chain_head[u]]
                < self.depth[self.chain_head[v]]
            ):
                v = self.parent[self.chain_head[v]]
            else:
                u = self.parent[self.chain_head[u]]

        if self.depth[u] < self.depth[v]:
            return u
        return v

    def _query_chain(
        self, chain_id: int, left: int, right: int
    ) -> float:
        """Query range in a chain.

        Args:
            chain_id: Chain ID.
            left: Left position in chain.
            right: Right position in chain.

        Returns:
            Query result.
        """
        if left > right:
            left, right = right, left
        return self.chain_segment_trees[chain_id].query_range(left, right)

    def _update_chain(
        self, chain_id: int, left: int, right: int, value: float
    ) -> None:
        """Update range in a chain.

        Args:
            chain_id: Chain ID.
            left: Left position in chain.
            right: Right position in chain.
            value: Value to add.
        """
        if left > right:
            left, right = right, left
        self.chain_segment_trees[chain_id].update_range(left, right, value)

    def query_path(self, u: TreeNode, v: TreeNode) -> float:
        """Query path from u to v.

        Args:
            u: First node.
            v: Second node.

        Returns:
            Sum of data along path.
        """
        u_orig, v_orig = u, v
        lca = self._lca(u, v)
        result = 0.0

        while u != lca:
            chain_id = self.node_to_chain[u]
            head = self.chain_head[u]
            if self.node_to_chain[head] == self.node_to_chain[lca]:
                pos_u = self.chain_pos[u]
                pos_lca = self.chain_pos[lca]
                result += self._query_chain(chain_id, pos_lca, pos_u)
                u = lca
            else:
                pos_u = self.chain_pos[u]
                pos_head = self.chain_pos[head]
                result += self._query_chain(chain_id, pos_head, pos_u)
                u = self.parent[head]

        while v != lca:
            chain_id = self.node_to_chain[v]
            head = self.chain_head[v]
            if self.node_to_chain[head] == self.node_to_chain[lca]:
                pos_v = self.chain_pos[v]
                pos_lca = self.chain_pos[lca]
                result += self._query_chain(chain_id, pos_lca, pos_v)
                v = lca
            else:
                pos_v = self.chain_pos[v]
                pos_head = self.chain_pos[head]
                result += self._query_chain(chain_id, pos_head, pos_v)
                v = self.parent[head]

        lca_chain_id = self.node_to_chain[lca]
        lca_pos = self.chain_pos[lca]
        result += self._query_chain(lca_chain_id, lca_pos, lca_pos)

        logger.info(f"Path query from {u_orig.value} to {v_orig.value}: {result}")
        return result

    def update_path(self, u: TreeNode, v: TreeNode, value: float) -> None:
        """Update path from u to v by adding value.

        Args:
            u: First node.
            v: Second node.
            value: Value to add to each node.
        """
        u_orig, v_orig = u, v
        lca = self._lca(u, v)

        while u != lca:
            chain_id = self.node_to_chain[u]
            head = self.chain_head[u]
            if self.node_to_chain[head] == self.node_to_chain[lca]:
                pos_u = self.chain_pos[u]
                pos_lca = self.chain_pos[lca]
                self._update_chain(chain_id, pos_lca, pos_u, value)
                u = lca
            else:
                pos_u = self.chain_pos[u]
                pos_head = self.chain_pos[head]
                self._update_chain(chain_id, pos_head, pos_u, value)
                u = self.parent[head]

        while v != lca:
            chain_id = self.node_to_chain[v]
            head = self.chain_head[v]
            if self.node_to_chain[head] == self.node_to_chain[lca]:
                pos_v = self.chain_pos[v]
                pos_lca = self.chain_pos[lca]
                self._update_chain(chain_id, pos_lca, pos_v, value)
                v = lca
            else:
                pos_v = self.chain_pos[v]
                pos_head = self.chain_pos[head]
                self._update_chain(chain_id, pos_head, pos_v, value)
                v = self.parent[head]

        lca_chain_id = self.node_to_chain[lca]
        lca_pos = self.chain_pos[lca]
        self._update_chain(lca_chain_id, lca_pos, lca_pos, value)

        logger.info(f"Path update from {u_orig.value} to {v_orig.value} with value {value}")

    def query_subtree(self, node: TreeNode) -> float:
        """Query subtree rooted at node.

        Args:
            node: Root of subtree.

        Returns:
            Sum of data in subtree.
        """
        chain_id = self.node_to_chain[node]
        pos = self.chain_pos[node]
        chain = self.chains[chain_id]

        result = self._query_chain(chain_id, pos, len(chain) - 1)

        for child in node.children:
            if child != self.heavy_child[node]:
                result += self.query_subtree(child)

        logger.info(f"Subtree query for node {node.value}: {result}")
        return result

    def get_lca(self, u: TreeNode, v: TreeNode) -> TreeNode:
        """Get lowest common ancestor of two nodes.

        Args:
            u: First node.
            v: Second node.

        Returns:
            LCA node.
        """
        lca = self._lca(u, v)
        logger.info(f"LCA of {u.value} and {v.value}: {lca.value}")
        return lca

    def get_distance(self, u: TreeNode, v: TreeNode) -> int:
        """Get distance between two nodes.

        Args:
            u: First node.
            v: Second node.

        Returns:
            Distance (number of edges).
        """
        lca = self._lca(u, v)
        distance = (
            self.depth[u] + self.depth[v] - 2 * self.depth[lca]
        )
        logger.info(f"Distance between {u.value} and {v.value}: {distance}")
        return distance


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
        nodes[i] = TreeNode(i, data=0.0)

    for parent, child in edges:
        if parent not in nodes or child not in nodes:
            raise ValueError(f"Invalid edge: ({parent}, {child})")
        nodes[parent].add_child(nodes[child])

    if root_value not in nodes:
        raise ValueError(f"Root value {root_value} not in nodes")

    root = nodes[root_value]
    logger.info(f"Built tree with {n} nodes, root: {root_value}")
    return root


def main() -> None:
    """Main function to demonstrate heavy-light decomposition."""
    print("Heavy-Light Decomposition Demo")
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

    hld = HeavyLightDecomposition(root)

    node3 = root.children[0].children[0]
    node4 = root.children[0].children[1]
    node5 = root.children[1].children[0]
    node6 = root.children[1].children[1]

    print(f"\nNumber of chains: {len(hld.chains)}")

    print("\nPath query from node 3 to node 4:")
    result = hld.query_path(node3, node4)
    print(f"Result: {result}")

    print("\nPath update: add 5 to path from node 3 to node 5:")
    hld.update_path(node3, node5, 5.0)

    print("\nPath query from node 3 to node 5 after update:")
    result = hld.query_path(node3, node5)
    print(f"Result: {result}")

    print("\nLCA of node 3 and node 5:")
    lca = hld.get_lca(node3, node5)
    print(f"LCA: {lca.value}")

    print("\nDistance between node 3 and node 6:")
    distance = hld.get_distance(node3, node6)
    print(f"Distance: {distance}")


if __name__ == "__main__":
    main()
