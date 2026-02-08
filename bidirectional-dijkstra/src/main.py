"""Bidirectional Dijkstra Algorithm for Shortest Path Finding.

This module provides functionality to find shortest paths using bidirectional
Dijkstra algorithm with forward and backward searches meeting in the middle.
"""

import heapq
import logging
import logging.handlers
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

import numpy as np
import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class Graph:
    """Represents a weighted graph for pathfinding."""

    def __init__(
        self,
        adjacency_list: Optional[Dict[int, List[Tuple[int, float]]]] = None,
        grid: Optional[np.ndarray] = None,
        allow_diagonal: bool = True,
        movement_cost: Dict[str, float] = None,
    ) -> None:
        """Initialize graph from adjacency list or grid.

        Args:
            adjacency_list: Dictionary mapping nodes to list of (neighbor, weight).
            grid: 2D numpy array where 0 = walkable, 1 = obstacle.
            allow_diagonal: Whether diagonal movement is allowed (for grid).
            movement_cost: Dictionary with 'straight' and 'diagonal' costs (for grid).
        """
        if adjacency_list is not None:
            self.adjacency_list = adjacency_list
            self.nodes = set(adjacency_list.keys())
            for neighbors in adjacency_list.values():
                self.nodes.update(neighbor for neighbor, _ in neighbors)
            self.is_grid = False
        elif grid is not None:
            self.grid = grid
            self.height, self.width = grid.shape
            self.allow_diagonal = allow_diagonal
            if movement_cost is None:
                import math

                movement_cost = {"straight": 1.0, "diagonal": math.sqrt(2)}
            self.straight_cost = movement_cost.get("straight", 1.0)
            self.diagonal_cost = movement_cost.get("diagonal", math.sqrt(2))
            self.is_grid = True
            self.nodes = set()
            for y in range(self.height):
                for x in range(self.width):
                    if grid[y, x] == 0:
                        self.nodes.add((x, y))
        else:
            raise ValueError("Must provide either adjacency_list or grid")

    def get_neighbors(self, node) -> List[Tuple]:
        """Get neighboring nodes with edge weights.

        Args:
            node: Current node.

        Returns:
            List of tuples (neighbor, weight).
        """
        if self.is_grid:
            return self._get_grid_neighbors(node)
        else:
            return self.adjacency_list.get(node, [])

    def _get_grid_neighbors(self, node: Tuple[int, int]) -> List[Tuple[Tuple[int, int], float]]:
        """Get neighbors for grid-based graph.

        Args:
            node: Current node coordinates (x, y).

        Returns:
            List of tuples (neighbor, cost).
        """
        x, y = node
        neighbors = []

        directions = [
            (0, 1, self.straight_cost),
            (1, 0, self.straight_cost),
            (0, -1, self.straight_cost),
            (-1, 0, self.straight_cost),
        ]

        if self.allow_diagonal:
            import math

            directions.extend(
                [
                    (1, 1, self.diagonal_cost),
                    (1, -1, self.diagonal_cost),
                    (-1, 1, self.diagonal_cost),
                    (-1, -1, self.diagonal_cost),
                ]
            )

        for dx, dy, cost in directions:
            neighbor = (x + dx, y + dy)
            if self._is_valid_grid_node(neighbor):
                neighbors.append((neighbor, cost))

        return neighbors

    def _is_valid_grid_node(self, node: Tuple[int, int]) -> bool:
        """Check if grid node is valid and walkable.

        Args:
            node: Node coordinates (x, y).

        Returns:
            True if node is valid and walkable.
        """
        x, y = node
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        return self.grid[y, x] == 0


class BidirectionalDijkstra:
    """Implements bidirectional Dijkstra algorithm for shortest path finding."""

    def __init__(self, config_path: str = "config.yaml") -> None:
        """Initialize BidirectionalDijkstra with configuration.

        Args:
            config_path: Path to configuration YAML file.

        Raises:
            FileNotFoundError: If config file doesn't exist.
            yaml.YAMLError: If config file is invalid YAML.
        """
        self.config = self._load_config(config_path)
        self._setup_logging()
        self._initialize_parameters()

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
        dijkstra_config = self.config.get("bidirectional_dijkstra", {})
        self.max_iterations = dijkstra_config.get("max_iterations", 10000)

    def _reconstruct_path(
        self,
        came_from_forward: Dict,
        came_from_backward: Dict,
        meeting_node,
        start,
        goal,
    ) -> List:
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

    def search(
        self,
        graph: Graph,
        start,
        goal,
    ) -> Dict[str, any]:
        """Run bidirectional Dijkstra search algorithm.

        Args:
            graph: Graph instance.
            start: Start node.
            goal: Goal node.

        Returns:
            Dictionary containing:
                - path: List of nodes from start to goal
                - cost: Total path cost
                - nodes_explored_forward: Nodes explored in forward search
                - nodes_explored_backward: Nodes explored in backward search
                - nodes_explored: Total nodes explored
                - path_length: Number of nodes in path
                - found: Whether path was found
                - meeting_node: Node where searches met

        Raises:
            ValueError: If start or goal nodes are invalid.
        """
        if start not in graph.nodes:
            raise ValueError(f"Start node {start} is not in graph")
        if goal not in graph.nodes:
            raise ValueError(f"Goal node {goal} is not in graph")

        if start == goal:
            return {
                "path": [start],
                "cost": 0.0,
                "nodes_explored_forward": 0,
                "nodes_explored_backward": 0,
                "nodes_explored": 0,
                "path_length": 1,
                "found": True,
                "meeting_node": start,
            }

        open_set_forward = []
        open_set_backward = []
        heapq.heappush(open_set_forward, (0.0, start))
        heapq.heappush(open_set_backward, (0.0, goal))

        dist_forward: Dict = {start: 0.0}
        dist_backward: Dict = {goal: 0.0}

        came_from_forward: Dict = {start: None}
        came_from_backward: Dict = {goal: None}

        visited_forward: Set = set()
        visited_backward: Set = set()

        best_meeting_node = None
        best_cost = float("inf")

        nodes_explored_forward = 0
        nodes_explored_backward = 0

        logger.info(
            f"Starting bidirectional Dijkstra from {start} to {goal}"
        )

        iteration = 0
        while (
            (open_set_forward or open_set_backward)
            and iteration < self.max_iterations
        ):
            iteration += 1

            if open_set_forward:
                current_dist, current = heapq.heappop(open_set_forward)

                if current in visited_forward:
                    continue

                visited_forward.add(current)
                nodes_explored_forward += 1

                if current in visited_backward:
                    meeting_cost = dist_forward[current] + dist_backward[current]
                    if meeting_cost < best_cost:
                        best_cost = meeting_cost
                        best_meeting_node = current
                        logger.debug(
                            f"Found meeting node {current} with cost {meeting_cost:.2f}"
                        )

                for neighbor, weight in graph.get_neighbors(current):
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
                nodes_explored_backward += 1

                if current in visited_forward:
                    meeting_cost = dist_forward[current] + dist_backward[current]
                    if meeting_cost < best_cost:
                        best_cost = meeting_cost
                        best_meeting_node = current
                        logger.debug(
                            f"Found meeting node {current} with cost {meeting_cost:.2f}"
                        )

                for neighbor, weight in graph.get_neighbors(current):
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

                    logger.info(
                        f"Path found: length={len(path)}, cost={best_cost:.2f}, "
                        f"nodes_explored={nodes_explored_forward + nodes_explored_backward}"
                    )

                    return {
                        "path": path,
                        "cost": best_cost,
                        "nodes_explored_forward": nodes_explored_forward,
                        "nodes_explored_backward": nodes_explored_backward,
                        "nodes_explored": nodes_explored_forward
                        + nodes_explored_backward,
                        "path_length": len(path),
                        "found": True,
                        "meeting_node": best_meeting_node,
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
                "nodes_explored_forward": nodes_explored_forward,
                "nodes_explored_backward": nodes_explored_backward,
                "nodes_explored": nodes_explored_forward + nodes_explored_backward,
                "path_length": len(path),
                "found": True,
                "meeting_node": best_meeting_node,
            }

        logger.warning(f"No path found from {start} to {goal}")
        return {
            "path": [],
            "cost": float("inf"),
            "nodes_explored_forward": nodes_explored_forward,
            "nodes_explored_backward": nodes_explored_backward,
            "nodes_explored": nodes_explored_forward + nodes_explored_backward,
            "path_length": 0,
            "found": False,
            "meeting_node": None,
        }


def main() -> None:
    """Main entry point for command-line usage."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Bidirectional Dijkstra Shortest Path Finding"
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

    dijkstra = BidirectionalDijkstra(config_path=args.config)

    if args.test:
        logger.info("Running test pathfinding on sample grid")

        grid = np.array(
            [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 1, 1, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
            ]
        )

        graph = Graph(grid=grid, allow_diagonal=True)

        start = (0, 0)
        goal = (7, 7)

        result = dijkstra.search(graph, start, goal)

        print(f"\nPathfinding Results:")
        print(f"Path found: {result['found']}")
        if result["found"]:
            print(f"Path length: {result['path_length']}")
            print(f"Path cost: {result['cost']:.2f}")
            print(f"Nodes explored (forward): {result['nodes_explored_forward']}")
            print(f"Nodes explored (backward): {result['nodes_explored_backward']}")
            print(f"Total nodes explored: {result['nodes_explored']}")
            print(f"Meeting node: {result['meeting_node']}")
            print(f"Path: {result['path'][:5]}...{result['path'][-5:]}")


if __name__ == "__main__":
    main()
