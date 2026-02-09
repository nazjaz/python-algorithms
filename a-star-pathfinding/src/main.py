"""A* Pathfinding Algorithm with Customizable Heuristics and Visualization.

This module provides functionality to find optimal paths using A* algorithm
with support for multiple heuristics (Manhattan, Euclidean, Chebyshev) and
visualization capabilities.
"""

import logging
import logging.handlers
import math
import time
from pathlib import Path
from typing import Callable, Dict, List, Optional, Set, Tuple

import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class Node:
    """Node in the pathfinding grid."""

    def __init__(
        self, x: int, y: int, g: float = float("inf"), h: float = 0.0
    ) -> None:
        """Initialize Node.

        Args:
            x: X coordinate.
            y: Y coordinate.
            g: Cost from start to this node.
            h: Heuristic estimate from this node to goal.
        """
        self.x = x
        self.y = y
        self.g = g
        self.h = h
        self.f = g + h
        self.parent: Optional["Node"] = None

    def __eq__(self, other: object) -> bool:
        """Check equality based on coordinates."""
        if not isinstance(other, Node):
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        """Hash based on coordinates."""
        return hash((self.x, self.y))

    def __lt__(self, other: "Node") -> bool:
        """Compare nodes for priority queue (lower f-value has higher priority)."""
        if self.f != other.f:
            return self.f < other.f
        return self.h < other.h

    def __repr__(self) -> str:
        """String representation."""
        return f"Node({self.x}, {self.y}, f={self.f:.2f})"


class AStarPathfinder:
    """A* pathfinding algorithm with customizable heuristics."""

    def __init__(self, config_path: str = "config.yaml") -> None:
        """Initialize AStarPathfinder with configuration.

        Args:
            config_path: Path to configuration YAML file.

        Raises:
            FileNotFoundError: If config file doesn't exist.
            yaml.YAMLError: If config file is invalid YAML.
        """
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

    def manhattan_distance(
        self, x1: int, y1: int, x2: int, y2: int
    ) -> float:
        """Calculate Manhattan distance heuristic.

        Sum of absolute differences in x and y coordinates.
        Suitable for grid-based movement (4-directional).

        Args:
            x1: X coordinate of first point.
            y1: Y coordinate of first point.
            x2: X coordinate of second point.
            y2: Y coordinate of second point.

        Returns:
            Manhattan distance.
        """
        return abs(x1 - x2) + abs(y1 - y2)

    def euclidean_distance(
        self, x1: int, y1: int, x2: int, y2: int
    ) -> float:
        """Calculate Euclidean distance heuristic.

        Straight-line distance between two points.
        Suitable for continuous movement.

        Args:
            x1: X coordinate of first point.
            y1: Y coordinate of first point.
            x2: X coordinate of second point.
            y2: Y coordinate of second point.

        Returns:
            Euclidean distance.
        """
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def chebyshev_distance(
        self, x1: int, y1: int, x2: int, y2: int
    ) -> float:
        """Calculate Chebyshev distance heuristic.

        Maximum of absolute differences in x and y coordinates.
        Suitable for 8-directional movement (including diagonals).

        Args:
            x1: X coordinate of first point.
            y1: Y coordinate of first point.
            x2: X coordinate of second point.
            y2: Y coordinate of second point.

        Returns:
            Chebyshev distance.
        """
        return max(abs(x1 - x2), abs(y1 - y2))

    def diagonal_distance(
        self, x1: int, y1: int, x2: int, y2: int
    ) -> float:
        """Calculate diagonal distance heuristic.

        Combines Manhattan and diagonal movement costs.
        Suitable for 8-directional movement with different costs.

        Args:
            x1: X coordinate of first point.
            y1: Y coordinate of first point.
            x2: X coordinate of second point.
            y2: Y coordinate of second point.

        Returns:
            Diagonal distance.
        """
        dx = abs(x1 - x2)
        dy = abs(y1 - y2)
        return (dx + dy) + (math.sqrt(2) - 2) * min(dx, dy)

    def _get_neighbors(
        self,
        node: Node,
        grid: List[List[int]],
        allow_diagonal: bool = False,
    ) -> List[Tuple[int, int]]:
        """Get valid neighbors of a node.

        Args:
            node: Current node.
            grid: Grid representation (0=free, 1=obstacle).
            allow_diagonal: Whether to allow diagonal movement.

        Returns:
            List of (x, y) tuples for valid neighbors.
        """
        neighbors: List[Tuple[int, int]] = []
        rows = len(grid)
        cols = len(grid[0]) if grid else 0

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        if allow_diagonal:
            directions.extend([(1, 1), (1, -1), (-1, 1), (-1, -1)])

        for dx, dy in directions:
            nx, ny = node.x + dx, node.y + dy
            if (
                0 <= nx < rows
                and 0 <= ny < cols
                and grid[nx][ny] == 0
            ):
                neighbors.append((nx, ny))

        return neighbors

    def _reconstruct_path(self, node: Node) -> List[Tuple[int, int]]:
        """Reconstruct path from goal to start.

        Args:
            node: Goal node.

        Returns:
            List of (x, y) tuples representing the path.
        """
        path: List[Tuple[int, int]] = []
        current: Optional[Node] = node

        while current is not None:
            path.append((current.x, current.y))
            current = current.parent

        path.reverse()
        return path

    def find_path(
        self,
        grid: List[List[int]],
        start: Tuple[int, int],
        goal: Tuple[int, int],
        heuristic: str = "manhattan",
        allow_diagonal: bool = False,
    ) -> Tuple[Optional[List[Tuple[int, int]]], Dict[str, any]]:
        """Find path using A* algorithm.

        Args:
            grid: Grid representation (0=free, 1=obstacle).
            start: Start position as (x, y) tuple.
            goal: Goal position as (x, y) tuple.
            heuristic: Heuristic function name (manhattan, euclidean,
                       chebyshev, diagonal).
            allow_diagonal: Whether to allow diagonal movement.

        Returns:
            Tuple containing:
                - Path as list of (x, y) tuples, or None if no path
                - Dictionary with statistics (nodes_explored, path_length, etc.)

        Raises:
            ValueError: If inputs are invalid.
        """
        if not grid or not grid[0]:
            raise ValueError("Grid cannot be empty")

        rows = len(grid)
        cols = len(grid[0])

        if not (0 <= start[0] < rows and 0 <= start[1] < cols):
            raise ValueError(f"Start position {start} out of grid bounds")
        if not (0 <= goal[0] < rows and 0 <= goal[1] < cols):
            raise ValueError(f"Goal position {goal} out of grid bounds")

        if grid[start[0]][start[1]] == 1:
            raise ValueError("Start position is an obstacle")
        if grid[goal[0]][goal[1]] == 1:
            raise ValueError("Goal position is an obstacle")

        # Select heuristic function
        heuristic_funcs: Dict[str, Callable[[int, int, int, int], float]] = {
            "manhattan": self.manhattan_distance,
            "euclidean": self.euclidean_distance,
            "chebyshev": self.chebyshev_distance,
            "diagonal": self.diagonal_distance,
        }

        if heuristic not in heuristic_funcs:
            raise ValueError(
                f"Unknown heuristic: {heuristic}. "
                f"Choose from {list(heuristic_funcs.keys())}"
            )

        h_func = heuristic_funcs[heuristic]

        logger.info(
            f"A* pathfinding: grid {rows}x{cols}, start={start}, "
            f"goal={goal}, heuristic={heuristic}, "
            f"diagonal={allow_diagonal}"
        )

        # Initialize
        start_node = Node(start[0], start[1], g=0.0, h=h_func(*start, *goal))
        goal_node = Node(goal[0], goal[1])

        open_set: List[Node] = [start_node]
        closed_set: Set[Node] = set()
        nodes_explored = 0

        # A* algorithm
        while open_set:
            # Get node with minimum f-value
            open_set.sort()
            current = open_set.pop(0)
            nodes_explored += 1

            logger.debug(
                f"  Exploring {current}, f={current.f:.2f}, "
                f"g={current.g:.2f}, h={current.h:.2f}"
            )

            # Check if goal reached
            if current == goal_node:
                path = self._reconstruct_path(current)
                logger.info(
                    f"Path found: length={len(path)}, "
                    f"nodes_explored={nodes_explored}"
                )
                return path, {
                    "nodes_explored": nodes_explored,
                    "path_length": len(path),
                    "path_cost": current.g,
                    "success": True,
                }

            closed_set.add(current)

            # Explore neighbors
            neighbors = self._get_neighbors(current, grid, allow_diagonal)
            for nx, ny in neighbors:
                neighbor = Node(nx, ny)

                if neighbor in closed_set:
                    continue

                # Calculate movement cost
                if allow_diagonal and abs(nx - current.x) == 1 and abs(ny - current.y) == 1:
                    move_cost = math.sqrt(2)
                else:
                    move_cost = 1.0

                tentative_g = current.g + move_cost

                # Check if this path to neighbor is better
                neighbor_in_open = False
                for node in open_set:
                    if node == neighbor:
                        neighbor_in_open = True
                        if tentative_g < node.g:
                            node.g = tentative_g
                            node.f = node.g + node.h
                            node.parent = current
                        break

                if not neighbor_in_open:
                    neighbor.g = tentative_g
                    neighbor.h = h_func(nx, ny, goal[0], goal[1])
                    neighbor.f = neighbor.g + neighbor.h
                    neighbor.parent = current
                    open_set.append(neighbor)
                    logger.debug(
                        f"    Added neighbor ({nx}, {ny}), "
                        f"f={neighbor.f:.2f}"
                    )

        logger.warning("No path found")
        return None, {
            "nodes_explored": nodes_explored,
            "path_length": 0,
            "path_cost": float("inf"),
            "success": False,
        }

    def visualize_path(
        self,
        grid: List[List[int]],
        path: Optional[List[Tuple[int, int]]],
        start: Tuple[int, int],
        goal: Tuple[int, int],
    ) -> str:
        """Visualize grid with path.

        Args:
            grid: Grid representation (0=free, 1=obstacle).
            path: Path as list of (x, y) tuples.
            start: Start position.
            goal: Goal position.

        Returns:
            String representation of visualized grid.
        """
        rows = len(grid)
        cols = len(grid[0]) if grid else 0

        # Create visualization grid
        vis_grid = [["." for _ in range(cols)] for _ in range(rows)]

        # Mark obstacles
        for i in range(rows):
            for j in range(cols):
                if grid[i][j] == 1:
                    vis_grid[i][j] = "#"

        # Mark path
        if path:
            for x, y in path[1:-1]:  # Exclude start and goal
                vis_grid[x][y] = "*"

        # Mark start and goal
        vis_grid[start[0]][start[1]] = "S"
        vis_grid[goal[0]][goal[1]] = "G"

        # Build visualization string
        lines = []
        lines.append("Grid Visualization:")
        lines.append("  S = Start, G = Goal, # = Obstacle, * = Path, . = Free")
        lines.append("")

        for i, row in enumerate(vis_grid):
            lines.append(f"  {''.join(row)}")

        return "\n".join(lines)

    def compare_heuristics(
        self,
        grid: List[List[int]],
        start: Tuple[int, int],
        goal: Tuple[int, int],
        allow_diagonal: bool = False,
        iterations: int = 1,
    ) -> Dict[str, any]:
        """Compare different heuristics.

        Args:
            grid: Grid representation (0=free, 1=obstacle).
            start: Start position.
            goal: Goal position.
            allow_diagonal: Whether to allow diagonal movement.
            iterations: Number of iterations for timing (default: 1).

        Returns:
            Dictionary containing comparison data.
        """
        logger.info(
            f"Comparing heuristics: start={start}, goal={goal}, "
            f"iterations={iterations}"
        )

        heuristics = ["manhattan", "euclidean", "chebyshev", "diagonal"]
        results = {
            "grid_size": (len(grid), len(grid[0]) if grid else 0),
            "start": start,
            "goal": goal,
            "allow_diagonal": allow_diagonal,
            "iterations": iterations,
        }

        for heuristic in heuristics:
            try:
                start_time = time.perf_counter()
                for _ in range(iterations):
                    path, stats = self.find_path(
                        grid, start, goal, heuristic, allow_diagonal
                    )
                heuristic_time = time.perf_counter() - start_time

                results[heuristic] = {
                    "path_found": path is not None,
                    "path_length": len(path) if path else 0,
                    "nodes_explored": stats["nodes_explored"],
                    "path_cost": stats["path_cost"],
                    "time_seconds": heuristic_time / iterations,
                    "time_milliseconds": (heuristic_time / iterations) * 1000,
                    "success": True,
                }
            except Exception as e:
                logger.error(f"Heuristic {heuristic} failed: {e}")
                results[heuristic] = {"success": False, "error": str(e)}

        return results

    def generate_report(
        self,
        comparison_data: Dict[str, any],
        output_path: Optional[str] = None,
    ) -> str:
        """Generate comparison report for heuristics.

        Args:
            comparison_data: Comparison data from compare_heuristics().
            output_path: Optional path to save report file.

        Returns:
            Report content as string.
        """
        report_lines = [
            "=" * 80,
            "A* PATHFINDING HEURISTIC COMPARISON REPORT",
            "=" * 80,
            "",
            f"Grid size: {comparison_data['grid_size'][0]}x{comparison_data['grid_size'][1]}",
            f"Start: {comparison_data['start']}",
            f"Goal: {comparison_data['goal']}",
            f"Allow diagonal: {comparison_data['allow_diagonal']}",
            f"Iterations: {comparison_data['iterations']}",
            "",
            "RESULTS",
            "-" * 80,
        ]

        heuristics = ["manhattan", "euclidean", "chebyshev", "diagonal"]
        for heuristic in heuristics:
            report_lines.append(f"\n{heuristic.upper()} HEURISTIC:")
            h_data = comparison_data[heuristic]
            if h_data.get("success", False):
                report_lines.append(f"  Path found: {h_data['path_found']}")
                if h_data["path_found"]:
                    report_lines.append(f"  Path length: {h_data['path_length']}")
                    report_lines.append(
                        f"  Path cost: {h_data['path_cost']:.2f}"
                    )
                report_lines.append(
                    f"  Nodes explored: {h_data['nodes_explored']}"
                )
                report_lines.append(
                    f"  Time: {h_data['time_milliseconds']:.4f} ms "
                    f"({h_data['time_seconds']:.6f} seconds)"
                )
            else:
                report_lines.append(f"  Status: Failed")
                report_lines.append(f"  Error: {h_data.get('error', 'Unknown')}")

        report_lines.extend([
            "",
            "ALGORITHM COMPLEXITY",
            "-" * 80,
            "A* Algorithm:",
            "  Time Complexity: O(b^d) where b=branching factor, d=depth",
            "  Space Complexity: O(b^d) for open and closed sets",
            "  Optimal: Yes (with admissible heuristic)",
            "",
            "Heuristics:",
            "  Manhattan: |x1-x2| + |y1-y2| (4-directional movement)",
            "  Euclidean: sqrt((x1-x2)² + (y1-y2)²) (continuous movement)",
            "  Chebyshev: max(|x1-x2|, |y1-y2|) (8-directional movement)",
            "  Diagonal: Combines Manhattan and diagonal costs",
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
        description="A* pathfinding algorithm with customizable heuristics "
        "and visualization"
    )
    parser.add_argument(
        "-g",
        "--grid",
        type=str,
        help="Grid as string (e.g., '5x5' for 5x5 grid)",
    )
    parser.add_argument(
        "-s",
        "--start",
        type=str,
        help="Start position as 'x-y' (e.g., '0-0')",
    )
    parser.add_argument(
        "-e",
        "--end",
        type=str,
        help="End position as 'x-y' (e.g., '4-4')",
    )
    parser.add_argument(
        "-o",
        "--obstacles",
        nargs="+",
        type=str,
        help="Obstacles as 'x-y' pairs (e.g., '1-1 2-2')",
    )
    parser.add_argument(
        "-h",
        "--heuristic",
        choices=["manhattan", "euclidean", "chebyshev", "diagonal"],
        default="manhattan",
        help="Heuristic function (default: manhattan)",
    )
    parser.add_argument(
        "-d",
        "--diagonal",
        action="store_true",
        help="Allow diagonal movement",
    )
    parser.add_argument(
        "-c",
        "--config",
        default="config.yaml",
        help="Path to configuration file (default: config.yaml)",
    )
    parser.add_argument(
        "-m",
        "--mode",
        choices=["find", "compare", "visualize"],
        default="find",
        help="Operation mode (default: find)",
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
        pathfinder = AStarPathfinder(config_path=args.config)

        # Parse grid size
        if args.grid:
            rows, cols = map(int, args.grid.split("x"))
        else:
            rows, cols = 10, 10

        # Create grid
        grid = [[0 for _ in range(cols)] for _ in range(rows)]

        # Add obstacles
        if args.obstacles:
            for obs_str in args.obstacles:
                x, y = map(int, obs_str.split("-"))
                if 0 <= x < rows and 0 <= y < cols:
                    grid[x][y] = 1

        # Parse start and end
        if args.start:
            start = tuple(map(int, args.start.split("-")))
        else:
            start = (0, 0)

        if args.end:
            goal = tuple(map(int, args.end.split("-")))
        else:
            goal = (rows - 1, cols - 1)

        logger.info(
            f"Input: grid {rows}x{cols}, start={start}, goal={goal}, "
            f"heuristic={args.heuristic}"
        )

        if args.mode == "find":
            path, stats = pathfinder.find_path(
                grid, start, goal, args.heuristic, args.diagonal
            )

            if path:
                print(f"\nPath found (length: {len(path)}):")
                print(f"  {path}")
                print(f"\nStatistics:")
                print(f"  Nodes explored: {stats['nodes_explored']}")
                print(f"  Path cost: {stats['path_cost']:.2f}")
                print(f"\n{pathfinder.visualize_path(grid, path, start, goal)}")
            else:
                print("No path found")

        elif args.mode == "compare":
            comparison = pathfinder.compare_heuristics(
                grid, start, goal, args.diagonal, args.iterations
            )

            print(f"\nA* Heuristic Comparison:")
            print(f"Grid: {comparison['grid_size'][0]}x{comparison['grid_size'][1]}")
            print(f"Start: {comparison['start']}, Goal: {comparison['goal']}")
            print("-" * 60)

            heuristics = ["manhattan", "euclidean", "chebyshev", "diagonal"]
            for heuristic in heuristics:
                h_data = comparison[heuristic]
                if h_data.get("success", False):
                    status = (
                        f"found, length={h_data['path_length']}"
                        if h_data["path_found"]
                        else "not found"
                    )
                    print(
                        f"{heuristic:12s}: {status:20s} "
                        f"explored={h_data['nodes_explored']:4d}  "
                        f"({h_data['time_milliseconds']:8.4f} ms)"
                    )
                else:
                    print(
                        f"{heuristic:12s}: Failed - "
                        f"{h_data.get('error', 'Unknown')}"
                    )

            if args.report:
                report = pathfinder.generate_report(
                    comparison, output_path=args.report
                )
                print(f"\nReport saved to {args.report}")

        elif args.mode == "visualize":
            path, stats = pathfinder.find_path(
                grid, start, goal, args.heuristic, args.diagonal
            )
            visualization = pathfinder.visualize_path(grid, path, start, goal)
            print(f"\n{visualization}")
            if path:
                print(f"\nPath length: {len(path)}")
                print(f"Nodes explored: {stats['nodes_explored']}")

    except Exception as e:
        logger.error(f"Error during execution: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
