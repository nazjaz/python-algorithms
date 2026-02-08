"""Iterative Deepening A* (IDA*) Pathfinding Algorithm.

This module provides functionality to find optimal paths using IDA* algorithm
with memory-efficient depth-first search and configurable heuristics.
"""

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
    """Implements various heuristic functions for IDA* algorithm."""

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
        """Zero heuristic (equivalent to iterative deepening DFS).

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


class IDAStar:
    """Implements Iterative Deepening A* pathfinding algorithm."""

    def __init__(self, config_path: str = "config.yaml") -> None:
        """Initialize IDA* algorithm with configuration.

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
        ida_config = self.config.get("ida_star", {})
        self.heuristic_name = ida_config.get("heuristic", "manhattan")
        self.allow_diagonal = ida_config.get("allow_diagonal", True)
        self.max_iterations = ida_config.get("max_iterations", 1000)
        self.movement_cost = ida_config.get("movement_cost", {})

        self.heuristic = Heuristic.get_heuristic(self.heuristic_name)

    def _depth_limited_search(
        self,
        graph: GridGraph,
        node: Tuple[int, int],
        goal: Tuple[int, int],
        g_cost: float,
        f_limit: float,
        path: List[Tuple[int, int]],
        visited: set,
    ) -> Tuple[Optional[List[Tuple[int, int]]], float]:
        """Perform depth-limited search with f-cost pruning.

        Args:
            graph: GridGraph instance.
            node: Current node.
            goal: Goal node.
            g_cost: Cost from start to current node.
            f_limit: Maximum f-cost to explore.
            path: Current path from start.
            visited: Set of visited nodes in current iteration.

        Returns:
            Tuple of (path if found, next_f_limit).
        """
        f_cost = g_cost + self.heuristic(node, goal)

        if f_cost > f_limit:
            return None, f_cost

        if node == goal:
            return path + [node], f_cost

        next_f_limit = float("inf")
        visited.add(node)

        for neighbor, move_cost in graph.get_neighbors(node):
            if neighbor in visited:
                continue

            new_g = g_cost + move_cost
            new_path = path + [node]

            result, candidate_f = self._depth_limited_search(
                graph, neighbor, goal, new_g, f_limit, new_path, visited
            )

            if result is not None:
                return result, candidate_f

            if candidate_f < next_f_limit:
                next_f_limit = candidate_f

        visited.remove(node)
        return None, next_f_limit

    def search(
        self,
        graph: GridGraph,
        start: Tuple[int, int],
        goal: Tuple[int, int],
    ) -> Dict[str, any]:
        """Run IDA* search algorithm.

        Args:
            graph: GridGraph instance.
            start: Start node coordinates (x, y).
            goal: Goal node coordinates (x, y).

        Returns:
            Dictionary containing:
                - path: List of nodes from start to goal
                - cost: Total path cost
                - iterations: Number of iterations performed
                - nodes_explored: Total nodes explored across iterations
                - path_length: Number of nodes in path
                - found: Whether path was found

        Raises:
            ValueError: If start or goal nodes are invalid.
        """
        if not graph.is_valid(start):
            raise ValueError(f"Start node {start} is not valid")
        if not graph.is_valid(goal):
            raise ValueError(f"Goal node {goal} is not valid")

        f_limit = self.heuristic(start, goal)
        iterations = 0
        total_nodes_explored = 0

        logger.info(
            f"Starting IDA* search from {start} to {goal} "
            f"with initial f-limit {f_limit:.2f}"
        )

        while iterations < self.max_iterations:
            visited = set()
            path, next_f_limit = self._depth_limited_search(
                graph, start, goal, 0.0, f_limit, [], visited
            )

            iterations += 1
            total_nodes_explored += len(visited)

            if path is not None:
                cost = self._calculate_path_cost(graph, path)

                logger.info(
                    f"Path found after {iterations} iterations: "
                    f"length={len(path)}, cost={cost:.2f}, "
                    f"nodes_explored={total_nodes_explored}"
                )

                return {
                    "path": path,
                    "cost": cost,
                    "iterations": iterations,
                    "nodes_explored": total_nodes_explored,
                    "path_length": len(path),
                    "found": True,
                }

            if next_f_limit == float("inf"):
                logger.warning(
                    f"No path found from {start} to {goal} "
                    f"after {iterations} iterations"
                )
                return {
                    "path": [],
                    "cost": float("inf"),
                    "iterations": iterations,
                    "nodes_explored": total_nodes_explored,
                    "path_length": 0,
                    "found": False,
                }

            f_limit = next_f_limit
            logger.debug(
                f"Iteration {iterations}: f-limit increased to {f_limit:.2f}"
            )

        logger.warning(
            f"Maximum iterations ({self.max_iterations}) reached "
            f"without finding path"
        )
        return {
            "path": [],
            "cost": float("inf"),
            "iterations": iterations,
            "nodes_explored": total_nodes_explored,
            "path_length": 0,
            "found": False,
        }

    def _calculate_path_cost(
        self,
        graph: GridGraph,
        path: List[Tuple[int, int]],
    ) -> float:
        """Calculate total cost of path.

        Args:
            graph: GridGraph instance.
            path: List of nodes in path.

        Returns:
            Total path cost.
        """
        if len(path) < 2:
            return 0.0

        total_cost = 0.0
        for i in range(len(path) - 1):
            current = path[i]
            neighbors = graph.get_neighbors(current)
            for neighbor, cost in neighbors:
                if neighbor == path[i + 1]:
                    total_cost += cost
                    break

        return total_cost


def main() -> None:
    """Main entry point for command-line usage."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Iterative Deepening A* Pathfinding"
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

    ida = IDAStar(config_path=args.config)

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

        graph = GridGraph(grid, allow_diagonal=ida.allow_diagonal)

        start = (0, 0)
        goal = (7, 7)

        result = ida.search(graph, start, goal)

        print(f"\nPathfinding Results:")
        print(f"Path found: {result['found']}")
        if result["found"]:
            print(f"Path length: {result['path_length']}")
            print(f"Path cost: {result['cost']:.2f}")
            print(f"Iterations: {result['iterations']}")
            print(f"Nodes explored: {result['nodes_explored']}")
            print(f"Path: {result['path'][:5]}...{result['path'][-5:]}")


if __name__ == "__main__":
    main()
