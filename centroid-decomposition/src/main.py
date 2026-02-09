"""Centroid Decomposition for Solving Tree Problems with Divide and Conquer.

This module provides functionality to implement centroid decomposition that
decomposes a tree into a centroid tree for efficient divide and conquer
solutions to tree problems. Centroid decomposition achieves O(n log n) time
complexity for many tree problems.
"""

import logging
import logging.handlers
from pathlib import Path
from typing import Callable, Dict, List, Optional, Set, Tuple

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
        self.neighbors: List["TreeNode"] = []
        self.parent: Optional["TreeNode"] = None

    def add_neighbor(self, neighbor: "TreeNode") -> None:
        """Add neighbor node (undirected edge).

        Args:
            neighbor: Neighbor node to add.
        """
        if neighbor not in self.neighbors:
            self.neighbors.append(neighbor)
        if self not in neighbor.neighbors:
            neighbor.neighbors.append(self)

    def __repr__(self) -> str:
        """String representation."""
        return f"TreeNode({self.value}, data={self.data})"


class CentroidDecomposition:
    """Centroid decomposition for divide and conquer tree problems."""

    def __init__(self, root: TreeNode, config_path: str = "config.yaml") -> None:
        """Initialize centroid decomposition.

        Args:
            root: Root of the tree.
            config_path: Path to configuration file.
        """
        self.root = root
        self.n = self._count_nodes(root)
        self.subtree_size: Dict[TreeNode, int] = {}
        self.centroid_tree_parent: Dict[TreeNode, Optional[TreeNode]] = {}
        self.centroid_tree_root: Optional[TreeNode] = None
        self.decomposed: bool = False
        self._setup_logging()
        self._load_config(config_path)

    def _setup_logging(self) -> None:
        """Configure logging for centroid decomposition operations."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        handler = logging.handlers.RotatingFileHandler(
            log_dir / "centroid_decomposition.log",
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
        """Count nodes in tree using DFS.

        Args:
            node: Current node.

        Returns:
            Number of nodes.
        """
        if node is None:
            return 0

        visited: Set[TreeNode] = set()

        def dfs(n: TreeNode) -> int:
            visited.add(n)
            count = 1
            for neighbor in n.neighbors:
                if neighbor not in visited:
                    count += dfs(neighbor)
            return count

        return dfs(node)

    def _compute_sizes(
        self, node: TreeNode, parent: Optional[TreeNode], visited: Set[TreeNode]
    ) -> int:
        """Compute subtree sizes.

        Args:
            node: Current node.
            parent: Parent node.
            visited: Set of visited nodes.

        Returns:
            Subtree size.
        """
        visited.add(node)
        size = 1

        for neighbor in node.neighbors:
            if neighbor != parent and neighbor not in visited:
                size += self._compute_sizes(neighbor, node, visited)

        self.subtree_size[node] = size
        return size

    def _find_centroid(
        self, node: TreeNode, parent: Optional[TreeNode], total_size: int, visited: Set[TreeNode]
    ) -> Optional[TreeNode]:
        """Find centroid of tree.

        Args:
            node: Current node.
            parent: Parent node.
            total_size: Total size of current component.
            visited: Set of visited nodes.

        Returns:
            Centroid node or None.
        """
        visited.add(node)

        for neighbor in node.neighbors:
            if neighbor != parent and neighbor not in visited:
                if self.subtree_size[neighbor] > total_size // 2:
                    return self._find_centroid(neighbor, node, total_size, visited)

        return node

    def _get_component_nodes(
        self, node: TreeNode, parent: Optional[TreeNode], visited: Set[TreeNode]
    ) -> List[TreeNode]:
        """Get all nodes in component.

        Args:
            node: Current node.
            parent: Parent node.
            visited: Set of visited nodes.

        Returns:
            List of nodes in component.
        """
        visited.add(node)
        nodes = [node]

        for neighbor in node.neighbors:
            if neighbor != parent and neighbor not in visited:
                nodes.extend(self._get_component_nodes(neighbor, node, visited))

        return nodes

    def _remove_centroid(self, centroid: TreeNode) -> List[List[TreeNode]]:
        """Remove centroid and get connected components.

        Args:
            centroid: Centroid node to remove.

        Returns:
            List of connected components.
        """
        visited: Set[TreeNode] = {centroid}
        components: List[List[TreeNode]] = []

        for neighbor in centroid.neighbors:
            if neighbor not in visited:
                component = self._get_component_nodes(neighbor, centroid, visited.copy())
                if component:
                    components.append(component)

        return components

    def _decompose(
        self, nodes: List[TreeNode], parent_centroid: Optional[TreeNode]
    ) -> Optional[TreeNode]:
        """Recursively decompose tree using centroids.

        Args:
            nodes: Nodes in current component.
            parent_centroid: Parent centroid in centroid tree.

        Returns:
            Centroid node.
        """
        if not nodes:
            return None

        if len(nodes) == 1:
            centroid = nodes[0]
            self.centroid_tree_parent[centroid] = parent_centroid
            return centroid

        root = nodes[0]
        visited: Set[TreeNode] = set()
        self._compute_sizes(root, None, visited)

        visited.clear()
        total_size = self.subtree_size[root]
        centroid = self._find_centroid(root, None, total_size, visited)

        if centroid is None:
            centroid = nodes[0]

        self.centroid_tree_parent[centroid] = parent_centroid

        components = self._remove_centroid(centroid)
        for component in components:
            child_centroid = self._decompose(component, centroid)
            if child_centroid:
                pass

        return centroid

    def decompose(self) -> None:
        """Perform centroid decomposition."""
        if self.decomposed:
            logger.warning("Tree already decomposed")
            return

        visited: Set[TreeNode] = set()
        all_nodes = self._get_component_nodes(self.root, None, visited)
        self.centroid_tree_root = self._decompose(all_nodes, None)
        self.decomposed = True
        if self.centroid_tree_root:
            logger.info(f"Centroid decomposition completed, root: {self.centroid_tree_root.value}")
        else:
            logger.info("Centroid decomposition completed")

    def _dfs_from_centroid(
        self,
        centroid: TreeNode,
        node: TreeNode,
        parent: Optional[TreeNode],
        visited: Set[TreeNode],
        distance: int,
        callback: Callable[[TreeNode, int], None],
    ) -> None:
        """DFS from centroid to process nodes.

        Args:
            centroid: Centroid node.
            node: Current node.
            parent: Parent node.
            visited: Set of visited nodes.
            distance: Distance from centroid.
            callback: Callback function(node, distance).
        """
        visited.add(node)
        callback(node, distance)

        for neighbor in node.neighbors:
            if neighbor != parent and neighbor not in visited:
                self._dfs_from_centroid(
                    centroid, neighbor, node, visited, distance + 1, callback
                )

    def solve_with_divide_conquer(
        self,
        problem_solver: Callable[[TreeNode, List[Tuple[TreeNode, int]]], float],
    ) -> float:
        """Solve tree problem using divide and conquer.

        Args:
            problem_solver: Function that solves problem for centroid and distances.

        Returns:
            Problem solution.

        Raises:
            ValueError: If tree not decomposed.
        """
        if not self.decomposed:
            raise ValueError("Tree must be decomposed first")

        def solve_recursive(centroid: TreeNode) -> float:
            if centroid is None:
                return 0.0

            visited: Set[TreeNode] = {centroid}
            distances: List[Tuple[TreeNode, int]] = [(centroid, 0)]

            for neighbor in centroid.neighbors:
                if neighbor not in visited:
                    self._dfs_from_centroid(
                        centroid,
                        neighbor,
                        centroid,
                        visited,
                        1,
                        lambda n, d: distances.append((n, d)),
                    )

            result = problem_solver(centroid, distances)

            parent = self.centroid_tree_parent.get(centroid)
            if parent:
                result += solve_recursive(parent)

            return result

        return solve_recursive(self.centroid_tree_root)

    def count_paths_with_condition(
        self, condition: Callable[[int], bool]
    ) -> int:
        """Count paths satisfying condition using divide and conquer.

        Args:
            condition: Function that checks if distance satisfies condition.

        Returns:
            Number of paths satisfying condition.

        Raises:
            ValueError: If tree not decomposed.
        """
        if not self.decomposed:
            raise ValueError("Tree must be decomposed first")

        total_paths = 0

        def solve_for_centroid(
            centroid: TreeNode, distances: List[Tuple[TreeNode, int]]
        ) -> float:
            nonlocal total_paths

            count = 0
            for node, dist in distances:
                if condition(dist):
                    count += 1

            total_paths += count
            return count

        self.solve_with_divide_conquer(solve_for_centroid)
        return total_paths

    def get_centroid_tree_root(self) -> Optional[TreeNode]:
        """Get root of centroid tree.

        Returns:
            Root of centroid tree or None if not decomposed.
        """
        return self.centroid_tree_root

    def get_centroid_parent(self, node: TreeNode) -> Optional[TreeNode]:
        """Get parent of node in centroid tree.

        Args:
            node: Node in centroid tree.

        Returns:
            Parent node or None.
        """
        return self.centroid_tree_parent.get(node)


def build_tree_from_edges(
    n: int, edges: List[Tuple[int, int]], root_value: int = 0
) -> TreeNode:
    """Build tree from list of edges.

    Args:
        n: Number of nodes.
        edges: List of (u, v) edges (undirected).
        root_value: Value of root node.

    Returns:
        Root node of tree.

    Raises:
        ValueError: If invalid tree structure.
    """
    nodes: Dict[int, TreeNode] = {}
    for i in range(n):
        nodes[i] = TreeNode(i, data=0.0)

    for u, v in edges:
        if u not in nodes or v not in nodes:
            raise ValueError(f"Invalid edge: ({u}, {v})")
        nodes[u].add_neighbor(nodes[v])

    if root_value not in nodes:
        raise ValueError(f"Root value {root_value} not in nodes")

    root = nodes[root_value]
    logger.info(f"Built tree with {n} nodes, root: {root_value}")
    return root


def main() -> None:
    """Main function to demonstrate centroid decomposition."""
    print("Centroid Decomposition Demo")
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

    cd = CentroidDecomposition(root)
    cd.decompose()

    centroid_root = cd.get_centroid_tree_root()
    if centroid_root:
        print(f"\nCentroid tree root: {centroid_root.value}")

    print("\nCounting paths with distance <= 2:")
    count = cd.count_paths_with_condition(lambda d: d <= 2)
    print(f"Number of paths: {count}")


if __name__ == "__main__":
    main()
