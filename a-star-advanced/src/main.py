"""A* Pathfinding Algorithm with Multiple Heuristics and Bidirectional Search.

This module provides functionality to find optimal paths using A* algorithm
with configurable heuristics and bidirectional search optimization.
"""

import heapq
import logging
import logging.handlers
import math
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

import numpy as np
import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class Heuristic:
    """Implements various heuristic functions for A* algorithm."""

    @staticmethod
    def manhattan_distance(
        node1: Tuple[int, int], node2: Tuple[int, int]
    ) -> float:
        """Calculate Manhattan distance (L1 norm).

        Args:
            node1: First node coordinates (x, y).
            node2: Second node coordinates (x, y).

        Returns:
            Manhattan distance between nodes.
        """
        return abs(node1[0] - node2[0]) + abs(node1[1] - node2[1])

    @staticmethod
    def euclidean_distance(
        node1: Tuple[int, int], node2: Tuple[int, int]
    ) -> float:
        """Calculate Euclidean distance (L2 norm).

        Args:
            node1: First node coordinates (x, y).
            node2: Second node coordinates (x, y).

        Returns:
            Euclidean distance between nodes.
        """
        dx = node1[0] - node2[0]
        dy = node1[1] - node2[1]
        return math.sqrt(dx * dx + dy * dy)

    @staticmethod
    def chebyshev_distance(
        node1: Tuple[int, int], node2: Tuple[int, int]
    ) -> float:
        """Calculate Chebyshev distance (L∞ norm).

        Args:
            node1: First node coordinates (x, y).
            node2: Second node coordinates (x, y).

        Returns:
            Chebyshev distance between nodes.
        """
        return max(abs(node1[0] - node2[0]), abs(node1[1] - node2[1]))

    @staticmethod
    def diagonal_distance(
        node1: Tuple[int, int], node2: Tuple[int, int]
    ) -> float:
        """Calculate diagonal distance (octile distance).

        Args:
            node1: First node coordinates (x, y).
            node2: Second node coordinates (x, y).

        Returns:
            Diagonal distance between nodes.
        """
        dx = abs(node1[0] - node2[0])
        dy = abs(node1[1] - node2[1])
        return (dx + dy) + (math.sqrt(2) - 2) * min(dx, dy)

    @staticmethod
    def octile_distance(
        node1: Tuple[int, int], node2: Tuple[int, int]
    ) -> float:
        """Calculate octile distance (8-directional movement).

        Args:
            node1: First node coordinates (x, y).
            node2: Second node coordinates (x, y).

        Returns:
            Octile distance between nodes.
        """
        dx = abs(node1[0] - node2[0])
        dy = abs(node1[1] - node2[1])
        return max(dx, dy) + (math.sqrt(2) - 1) * min(dx, dy)

    @staticmethod
    def zero_heuristic(
        node1: Tuple[int, int], node2: Tuple[int, int]
    ) -> float:
        """Zero heuristic (equivalent to Dijkstra's algorithm).

        Args:
            node1: First node coordinates (x, y).
            node2: Second node coordinates (x, y).

        Returns:
            Always returns 0.
        """
        return 0.0

    @classmethod
    def get_heuristic(cls, heuristic_name: str) -> Callable:
        """Get heuristic function by name.

        Args:
            heuristic_name: Name of heuristic ('manhattan', 'euclidean',
                          'chebyshev', 'diagonal', 'octile', 'zero').

        Returns:
            Heuristic function.

        Raises:
            ValueError: If heuristic name is unknown.
        """
        heuristics = {
            "manhattan": cls.manhattan_distance,
            "euclidean": cls.euclidean_distance,
            "chebyshev": cls.chebyshev_distance,
            "diagonal": cls.diagonal_distance,
            "octile": cls.octile_distance,
            "zero": cls.zero_heuristic,
        }

        if heuristic_name.lower() not in heuristics:
            raise ValueError(
                f"Unknown heuristic: {heuristic_name}. "
                f"Must be one of {list(heuristics.keys())}"
            )

        return heuristics[heuristic_name.lower()]


class GridGraph:
    """Represents a grid-based graph for pathfinding."""

    def __init__(
        self,
        grid: np.ndarray,
        allow_diagonal: bool = True,
        movement_cost: Dict[str, float] = None,
    ) -> None:
        """Initialize grid graph.

        Args:
            grid: 2D numpy array where 0 = walkable, 1 = obstacle.
            allow_diagonal: Whether diagonal movement is allowed.
            movement_cost: Dictionary with 'straight' and 'diagonal' costs.
        """
        self.grid = grid
        self.height, self.width = grid.shape
        self.allow_diagonal = allow_diagonal

        if movement_cost is None:
            movement_cost = {"straight": 1.0, "diagonal": math.sqrt(2)}

        self.straight_cost = movement_cost.get("straight", 1.0)
        self.diagonal_cost = movement_cost.get("diagonal", math.sqrt(2))

    def is_valid(self, node: Tuple[int, int]) -> bool:
        """Check if node is valid and walkable.

        Args:
            node: Node coordinates (x, y).

        Returns:
            True if node is valid and walkable.
        """
        x, y = node
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        return self.grid[y, x] == 0

    def get_neighbors(self, node: Tuple[int, int]) -> List[Tuple[Tuple[int, int], float]]:
        """Get neighboring nodes with movement costs.

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
            if self.is_valid(neighbor):
                neighbors.append((neighbor, cost))

        return neighbors


class AStar:
    """Implements A* pathfinding algorithm."""

    def __init__(self, config_path: str = "config.yaml") -> None:
        """Initialize A* algorithm with configuration.

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
        astar_config = self.config.get("a_star", {})
        self.heuristic_name = astar_config.get("heuristic", "manhattan")
        self.allow_diagonal = astar_config.get("allow_diagonal", True)
        self.bidirectional = astar_config.get("bidirectional", False)
        self.movement_cost = astar_config.get("movement_cost", {})

        self.heuristic = Heuristic.get_heuristic(self.heuristic_name)

    def _reconstruct_path(
        self,
        came_from: Dict[Tuple[int, int], Tuple[int, int]],
        current: Tuple[int, int],
    ) -> List[Tuple[int, int]]:
        """Reconstruct path from start to current node.

        Args:
            came_from: Dictionary mapping nodes to their predecessors.
            current: Current node.

        Returns:
            List of nodes from start to current.
        """
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path

    def search(
        self,
        graph: GridGraph,
        start: Tuple[int, int],
        goal: Tuple[int, int],
    ) -> Dict[str, any]:
        """Run A* search algorithm.

        Args:
            graph: GridGraph instance.
            start: Start node coordinates (x, y).
            goal: Goal node coordinates (x, y).

        Returns:
            Dictionary containing:
                - path: List of nodes from start to goal
                - cost: Total path cost
                - nodes_explored: Number of nodes explored
                - path_length: Number of nodes in path
                - found: Whether path was found

        Raises:
            ValueError: If start or goal nodes are invalid.
        """
        if not graph.is_valid(start):
            raise ValueError(f"Start node {start} is not valid")
        if not graph.is_valid(goal):
            raise ValueError(f"Goal node {goal} is not valid")

        if self.bidirectional:
            return self._bidirectional_search(graph, start, goal)
        else:
            return self._unidirectional_search(graph, start, goal)

    def _unidirectional_search(
        self,
        graph: GridGraph,
        start: Tuple[int, int],
        goal: Tuple[int, int],
    ) -> Dict[str, any]:
        """Run unidirectional A* search.

        Args:
            graph: GridGraph instance.
            start: Start node coordinates (x, y).
            goal: Goal node coordinates (x, y).

        Returns:
            Dictionary with path information.
        """
        open_set = []
        heapq.heappush(open_set, (0, start))

        came_from: Dict[Tuple[int, int], Tuple[int, int]] = {}
        g_score: Dict[Tuple[int, int], float] = {start: 0.0}
        f_score: Dict[Tuple[int, int], float] = {
            start: self.heuristic(start, goal)
        }

        nodes_explored = 0

        logger.info(f"Starting A* search from {start} to {goal}")

        while open_set:
            current_f, current = heapq.heappop(open_set)

            if current == goal:
                path = self._reconstruct_path(came_from, current)
                logger.info(
                    f"Path found: length={len(path)}, "
                    f"cost={g_score[current]:.2f}, "
                    f"nodes_explored={nodes_explored}"
                )
                return {
                    "path": path,
                    "cost": g_score[current],
                    "nodes_explored": nodes_explored,
                    "path_length": len(path),
                    "found": True,
                }

            nodes_explored += 1

            for neighbor, move_cost in graph.get_neighbors(current):
                tentative_g = g_score[current] + move_cost

                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + self.heuristic(
                        neighbor, goal
                    )
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        logger.warning(f"No path found from {start} to {goal}")
        return {
            "path": [],
            "cost": float("inf"),
            "nodes_explored": nodes_explored,
            "path_length": 0,
            "found": False,
        }

    def _bidirectional_search(
        self,
        graph: GridGraph,
        start: Tuple[int, int],
        goal: Tuple[int, int],
    ) -> Dict[str, any]:
        """Run bidirectional A* search.

        Args:
            graph: GridGraph instance.
            start: Start node coordinates (x, y).
            goal: Goal node coordinates (x, y).

        Returns:
            Dictionary with path information.
        """
        open_set_forward = []
        open_set_backward = []
        heapq.heappush(open_set_forward, (0, start))
        heapq.heappush(open_set_backward, (0, goal))

        came_from_forward: Dict[Tuple[int, int], Tuple[int, int]] = {}
        came_from_backward: Dict[Tuple[int, int], Tuple[int, int]] = {}

        g_score_forward: Dict[Tuple[int, int], float] = {start: 0.0}
        g_score_backward: Dict[Tuple[int, int], float] = {goal: 0.0}

        f_score_forward: Dict[Tuple[int, int], float] = {
            start: self.heuristic(start, goal)
        }
        f_score_backward: Dict[Tuple[int, int], float] = {
            goal: self.heuristic(goal, start)
        }

        visited_forward: Dict[Tuple[int, int], bool] = {}
        visited_backward: Dict[Tuple[int, int], bool] = {}

        best_meeting_node = None
        best_cost = float("inf")

        nodes_explored = 0

        logger.info(
            f"Starting bidirectional A* search from {start} to {goal}"
        )

        while open_set_forward or open_set_backward:
            if open_set_forward:
                current_f, current = heapq.heappop(open_set_forward)

                if current in visited_backward:
                    meeting_cost = (
                        g_score_forward[current] + g_score_backward[current]
                    )
                    if meeting_cost < best_cost:
                        best_cost = meeting_cost
                        best_meeting_node = current

                visited_forward[current] = True
                nodes_explored += 1

                for neighbor, move_cost in graph.get_neighbors(current):
                    tentative_g = g_score_forward[current] + move_cost

                    if (
                        neighbor not in g_score_forward
                        or tentative_g < g_score_forward[neighbor]
                    ):
                        came_from_forward[neighbor] = current
                        g_score_forward[neighbor] = tentative_g
                        f_score_forward[neighbor] = tentative_g + self.heuristic(
                            neighbor, goal
                        )
                        heapq.heappush(
                            open_set_forward, (f_score_forward[neighbor], neighbor)
                        )

            if open_set_backward:
                current_f, current = heapq.heappop(open_set_backward)

                if current in visited_forward:
                    meeting_cost = (
                        g_score_forward[current] + g_score_backward[current]
                    )
                    if meeting_cost < best_cost:
                        best_cost = meeting_cost
                        best_meeting_node = current

                visited_backward[current] = True
                nodes_explored += 1

                for neighbor, move_cost in graph.get_neighbors(current):
                    tentative_g = g_score_backward[current] + move_cost

                    if (
                        neighbor not in g_score_backward
                        or tentative_g < g_score_backward[neighbor]
                    ):
                        came_from_backward[neighbor] = current
                        g_score_backward[neighbor] = tentative_g
                        f_score_backward[neighbor] = tentative_g + self.heuristic(
                            neighbor, start
                        )
                        heapq.heappush(
                            open_set_backward,
                            (f_score_backward[neighbor], neighbor),
                        )

            if best_meeting_node is not None:
                path_forward = self._reconstruct_path(
                    came_from_forward, best_meeting_node
                )
                path_backward = self._reconstruct_path(
                    came_from_backward, best_meeting_node
                )
                path_backward.reverse()
                path = path_forward + path_backward[1:]

                logger.info(
                    f"Bidirectional path found: length={len(path)}, "
                    f"cost={best_cost:.2f}, "
                    f"nodes_explored={nodes_explored}"
                )

                return {
                    "path": path,
                    "cost": best_cost,
                    "nodes_explored": nodes_explored,
                    "path_length": len(path),
                    "found": True,
                }

        logger.warning(f"No path found from {start} to {goal}")
        return {
            "path": [],
            "cost": float("inf"),
            "nodes_explored": nodes_explored,
            "path_length": 0,
            "found": False,
        }


def main() -> None:
    """Main entry point for command-line usage."""
    import argparse

    parser = argparse.ArgumentParser(
        description="A* Pathfinding with Multiple Heuristics"
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

    astar = AStar(config_path=args.config)

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

        graph = GridGraph(grid, allow_diagonal=astar.allow_diagonal)

        start = (0, 0)
        goal = (7, 7)

        result = astar.search(graph, start, goal)

        print(f"\nPathfinding Results:")
        print(f"Path found: {result['found']}")
        if result["found"]:
            print(f"Path length: {result['path_length']}")
            print(f"Path cost: {result['cost']:.2f}")
            print(f"Nodes explored: {result['nodes_explored']}")
            print(f"Path: {result['path'][:5]}...{result['path'][-5:]}")


if __name__ == "__main__":
    main()
