"""Contraction Hierarchies for Fast Shortest Path Queries in Road Networks.

This module provides functionality to preprocess road networks using contraction
hierarchies and perform fast shortest path queries.
"""

import heapq
import logging
import logging.handlers
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

import numpy as np
import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class RoadGraph:
    """Represents a road network graph."""

    def __init__(
        self,
        edges: Optional[List[Tuple[int, int, float]]] = None,
        num_nodes: Optional[int] = None,
    ) -> None:
        """Initialize road graph.

        Args:
            edges: List of (source, target, weight) tuples.
            num_nodes: Number of nodes (if None, inferred from edges).
        """
        if edges is None:
            edges = []

        self.edges = edges
        self.num_nodes = num_nodes or (
            max(max(e[0], e[1]) for e in edges) + 1 if edges else 0
        )

        self.forward_adj: Dict[int, List[Tuple[int, float]]] = defaultdict(list)
        self.backward_adj: Dict[int, List[Tuple[int, float]]] = defaultdict(list)

        for source, target, weight in edges:
            self.forward_adj[source].append((target, weight))
            self.backward_adj[target].append((source, weight))

    def get_outgoing(self, node: int) -> List[Tuple[int, float]]:
        """Get outgoing edges from node.

        Args:
            node: Node ID.

        Returns:
            List of (target, weight) tuples.
        """
        return self.forward_adj.get(node, [])

    def get_incoming(self, node: int) -> List[Tuple[int, float]]:
        """Get incoming edges to node.

        Args:
            node: Node ID.

        Returns:
            List of (source, weight) tuples.
        """
        return self.backward_adj.get(node, [])

    def add_edge(self, source: int, target: int, weight: float) -> None:
        """Add edge to graph.

        Args:
            source: Source node.
            target: Target node.
            weight: Edge weight.
        """
        self.forward_adj[source].append((target, weight))
        self.backward_adj[target].append((source, weight))
        self.edges.append((source, target, weight))


class ContractionHierarchies:
    """Implements Contraction Hierarchies for fast shortest path queries."""

    def __init__(self, config_path: str = "config.yaml") -> None:
        """Initialize ContractionHierarchies with configuration.

        Args:
            config_path: Path to configuration YAML file.

        Raises:
            FileNotFoundError: If config file doesn't exist.
            yaml.YAMLError: If config file is invalid YAML.
        """
        self.config = self._load_config(config_path)
        self._setup_logging()
        self._initialize_parameters()

        self.node_level: Dict[int, int] = {}
        self.upward_forward: Dict[int, List[Tuple[int, float]]] = defaultdict(list)
        self.upward_backward: Dict[int, List[Tuple[int, float]]] = defaultdict(list)
        self.preprocessed = False

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
            "%(asctime)s - %(name)s - %(levelname)s - " "%(message)s"
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

    def _initialize_parameters(self) -> None:
        """Initialize algorithm parameters from configuration."""
        ch_config = self.config.get("contraction_hierarchies", {})
        self.edge_difference_weight = ch_config.get("edge_difference_weight", 1.0)
        self.deleted_neighbors_weight = ch_config.get("deleted_neighbors_weight", 1.0)
        self.hop_limit = ch_config.get("hop_limit", 2)

    def _calculate_importance(
        self, graph: RoadGraph, node: int, deleted_neighbors: Set[int]
    ) -> float:
        """Calculate node importance for contraction ordering.

        Args:
            graph: Road graph.
            node: Node to evaluate.
            deleted_neighbors: Set of already contracted neighbors.

        Returns:
            Importance value (lower = more important, contract first).
        """
        incoming = graph.get_incoming(node)
        outgoing = graph.get_outgoing(node)

        incoming_count = len([n for n, _ in incoming if n not in deleted_neighbors])
        outgoing_count = len([n for n, _ in outgoing if n not in deleted_neighbors])

        edge_difference = incoming_count * outgoing_count - incoming_count - outgoing_count

        deleted_neighbors_count = len(deleted_neighbors.intersection(
            {n for n, _ in incoming} | {n for n, _ in outgoing}
        ))

        importance = (
            self.edge_difference_weight * edge_difference
            + self.deleted_neighbors_weight * deleted_neighbors_count
        )

        return importance

    def _find_shortcuts(
        self,
        graph: RoadGraph,
        node: int,
        deleted_neighbors: Set[int],
    ) -> List[Tuple[int, int, float]]:
        """Find shortcuts needed when contracting a node.

        Args:
            graph: Road graph.
            node: Node being contracted.
            deleted_neighbors: Set of already contracted neighbors.

        Returns:
            List of (source, target, weight) shortcut edges.
        """
        shortcuts = []
        incoming = graph.get_incoming(node)
        outgoing = graph.get_outgoing(node)

        for source, in_weight in incoming:
            if source in deleted_neighbors:
                continue

            for target, out_weight in outgoing:
                if target in deleted_neighbors:
                    continue

                if source == target:
                    continue

                shortcut_weight = in_weight + out_weight

                existing_weight = None
                for t, w in graph.get_outgoing(source):
                    if t == target:
                        existing_weight = w
                        break

                if existing_weight is None or shortcut_weight < existing_weight:
                    shortcuts.append((source, target, shortcut_weight))

        return shortcuts

    def _contract_node(
        self,
        graph: RoadGraph,
        node: int,
        level: int,
        deleted_neighbors: Set[int],
    ) -> List[Tuple[int, int, float]]:
        """Contract a node and add necessary shortcuts.

        Args:
            graph: Road graph.
            node: Node to contract.
            level: Contraction level.
            deleted_neighbors: Set of already contracted neighbors.

        Returns:
            List of shortcuts added.
        """
        shortcuts = self._find_shortcuts(graph, node, deleted_neighbors)

        for source, target, weight in shortcuts:
            graph.add_edge(source, target, weight)
            if self.node_level.get(source, 0) < level:
                self.upward_forward[source].append((target, weight))
            if self.node_level.get(target, 0) < level:
                self.upward_backward[target].append((source, weight))

        self.node_level[node] = level
        deleted_neighbors.add(node)

        return shortcuts

    def preprocess(self, graph: RoadGraph) -> Dict[str, any]:
        """Preprocess graph using contraction hierarchies.

        Args:
            graph: Road graph to preprocess.

        Returns:
            Dictionary with preprocessing statistics.
        """
        logger.info(f"Starting preprocessing for {graph.num_nodes} nodes")

        deleted_neighbors: Set[int] = set()
        shortcuts_added = 0
        nodes_contracted = 0

        remaining_nodes = set(range(graph.num_nodes))

        while remaining_nodes:
            if nodes_contracted % max(1, graph.num_nodes // 10) == 0:
                logger.info(
                    f"Progress: {nodes_contracted}/{graph.num_nodes} nodes contracted"
                )

            best_node = None
            best_importance = float("inf")

            for node in remaining_nodes:
                importance = self._calculate_importance(graph, node, deleted_neighbors)
                if importance < best_importance:
                    best_importance = importance
                    best_node = node

            if best_node is None:
                break

            level = nodes_contracted
            shortcuts = self._contract_node(
                graph, best_node, level, deleted_neighbors
            )
            shortcuts_added += len(shortcuts)
            nodes_contracted += 1
            remaining_nodes.remove(best_node)

        self.preprocessed = True

        logger.info(
            f"Preprocessing complete: {nodes_contracted} nodes contracted, "
            f"{shortcuts_added} shortcuts added"
        )

        return {
            "nodes_contracted": nodes_contracted,
            "shortcuts_added": shortcuts_added,
            "total_edges": len(graph.edges),
        }

    def _bidirectional_dijkstra_ch(
        self,
        graph: RoadGraph,
        start: int,
        goal: int,
    ) -> Dict[str, any]:
        """Run bidirectional Dijkstra on contracted hierarchy.

        Args:
            graph: Preprocessed road graph.
            start: Start node.
            goal: Goal node.

        Returns:
            Dictionary with path information.
        """
        if start == goal:
            return {
                "path": [start],
                "cost": 0.0,
                "nodes_explored": 0,
                "found": True,
            }

        open_set_forward = []
        open_set_backward = []
        heapq.heappush(open_set_forward, (0.0, start))
        heapq.heappush(open_set_backward, (0.0, goal))

        dist_forward: Dict[int, float] = {start: 0.0}
        dist_backward: Dict[int, float] = {goal: 0.0}

        came_from_forward: Dict[int, int] = {start: None}
        came_from_backward: Dict[int, int] = {goal: None}

        visited_forward: Set[int] = set()
        visited_backward: Set[int] = set()

        best_meeting_node = None
        best_cost = float("inf")

        nodes_explored = 0

        while open_set_forward or open_set_backward:
            if open_set_forward:
                current_dist, current = heapq.heappop(open_set_forward)

                if current in visited_forward:
                    continue

                visited_forward.add(current)
                nodes_explored += 1

                if current in visited_backward:
                    meeting_cost = dist_forward[current] + dist_backward[current]
                    if meeting_cost < best_cost:
                        best_cost = meeting_cost
                        best_meeting_node = current

                current_level = self.node_level.get(current, 0)

                for neighbor, weight in graph.get_outgoing(current):
                    neighbor_level = self.node_level.get(neighbor, 0)
                    if neighbor_level <= current_level and neighbor != current:
                        continue

                    new_dist = dist_forward[current] + weight

                    if neighbor not in dist_forward or new_dist < dist_forward[neighbor]:
                        dist_forward[neighbor] = new_dist
                        came_from_forward[neighbor] = current
                        heapq.heappush(open_set_forward, (new_dist, neighbor))

            if open_set_backward:
                current_dist, current = heapq.heappop(open_set_backward)

                if current in visited_backward:
                    continue

                visited_backward.add(current)
                nodes_explored += 1

                if current in visited_forward:
                    meeting_cost = dist_forward[current] + dist_backward[current]
                    if meeting_cost < best_cost:
                        best_cost = meeting_cost
                        best_meeting_node = current

                current_level = self.node_level.get(current, 0)

                for neighbor, weight in graph.get_incoming(current):
                    neighbor_level = self.node_level.get(neighbor, 0)
                    if neighbor_level <= current_level and neighbor != current:
                        continue

                    new_dist = dist_backward[current] + weight

                    if neighbor not in dist_backward or new_dist < dist_backward[neighbor]:
                        dist_backward[neighbor] = new_dist
                        came_from_backward[neighbor] = current
                        heapq.heappush(open_set_backward, (new_dist, neighbor))

            if best_meeting_node is not None:
                if (
                    not open_set_forward
                    or dist_forward[open_set_forward[0][1]] >= best_cost / 2
                ) and (
                    not open_set_backward
                    or dist_backward[open_set_backward[0][1]] >= best_cost / 2
                ):
                    path = self._reconstruct_path(
                        came_from_forward,
                        came_from_backward,
                        best_meeting_node,
                        start,
                        goal,
                    )

                    return {
                        "path": path,
                        "cost": best_cost,
                        "nodes_explored": nodes_explored,
                        "path_length": len(path),
                        "found": True,
                    }

        if best_meeting_node is not None:
            path = self._reconstruct_path(
                came_from_forward,
                came_from_backward,
                best_meeting_node,
                start,
                goal,
            )

            return {
                "path": path,
                "cost": best_cost,
                "nodes_explored": nodes_explored,
                "path_length": len(path),
                "found": True,
            }

        return {
            "path": [],
            "cost": float("inf"),
            "nodes_explored": nodes_explored,
            "path_length": 0,
            "found": False,
        }

    def _reconstruct_path(
        self,
        came_from_forward: Dict[int, int],
        came_from_backward: Dict[int, int],
        meeting_node: int,
        start: int,
        goal: int,
    ) -> List[int]:
        """Reconstruct path from start to goal through meeting node.

        Args:
            came_from_forward: Predecessor map for forward search.
            came_from_backward: Predecessor map for backward search.
            meeting_node: Node where searches met.
            start: Start node.
            goal: Goal node.

        Returns:
            Complete path from start to goal.
        """
        path_forward = []
        current = meeting_node
        while current is not None:
            path_forward.append(current)
            current = came_from_forward.get(current)

        path_forward.reverse()

        path_backward = []
        current = came_from_backward.get(meeting_node)
        while current is not None:
            path_backward.append(current)
            current = came_from_backward.get(current)

        return path_forward + path_backward

    def query(self, graph: RoadGraph, start: int, goal: int) -> Dict[str, any]:
        """Query shortest path using preprocessed contraction hierarchies.

        Args:
            graph: Preprocessed road graph.
            start: Start node.
            goal: Goal node.

        Returns:
            Dictionary with path information.

        Raises:
            ValueError: If graph not preprocessed or nodes invalid.
        """
        if not self.preprocessed:
            raise ValueError("Graph must be preprocessed before querying")

        if start < 0 or start >= graph.num_nodes:
            raise ValueError(f"Start node {start} is invalid")
        if goal < 0 or goal >= graph.num_nodes:
            raise ValueError(f"Goal node {goal} is invalid")

        return self._bidirectional_dijkstra_ch(graph, start, goal)


def main() -> None:
    """Main entry point for command-line usage."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Contraction Hierarchies for Road Networks"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="config.yaml",
        help="Path to configuration file",
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Run test pathfinding problem",
    )

    args = parser.parse_args()

    ch = ContractionHierarchies(config_path=args.config)

    if args.test:
        logger.info("Running test on sample road network")

        edges = [
            (0, 1, 1.0),
            (1, 2, 2.0),
            (2, 3, 1.0),
            (0, 2, 4.0),
            (1, 3, 5.0),
            (3, 4, 1.0),
            (2, 4, 2.0),
        ]

        graph = RoadGraph(edges=edges, num_nodes=5)

        logger.info("Preprocessing graph...")
        stats = ch.preprocess(graph)
        print(f"\nPreprocessing Statistics:")
        print(f"Nodes contracted: {stats['nodes_contracted']}")
        print(f"Shortcuts added: {stats['shortcuts_added']}")
        print(f"Total edges: {stats['total_edges']}")

        logger.info("Querying shortest path...")
        result = ch.query(graph, 0, 4)

        print(f"\nQuery Results:")
        print(f"Path found: {result['found']}")
        if result["found"]:
            print(f"Path: {result['path']}")
            print(f"Cost: {result['cost']:.2f}")
            print(f"Nodes explored: {result['nodes_explored']}")


if __name__ == "__main__":
    main()
