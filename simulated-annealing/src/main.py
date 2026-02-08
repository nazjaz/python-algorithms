"""Simulated Annealing Algorithm for Global Optimization.

This module provides functionality to solve global optimization problems
using simulated annealing algorithm with configurable temperature scheduling
and acceptance criteria.
"""

import logging
import logging.handlers
import math
import random
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

import numpy as np
import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class TemperatureScheduler:
    """Manages temperature scheduling for simulated annealing."""

    def __init__(
        self,
        initial_temperature: float,
        final_temperature: float,
        max_iterations: int,
        schedule_type: str = "exponential",
    ) -> None:
        """Initialize temperature scheduler.

        Args:
            initial_temperature: Starting temperature value.
            final_temperature: Ending temperature value.
            max_iterations: Maximum number of iterations.
            schedule_type: Type of cooling schedule ('exponential', 'linear',
                          'logarithmic', 'geometric').

        Raises:
            ValueError: If temperatures are invalid or schedule_type is unknown.
        """
        if initial_temperature <= 0:
            raise ValueError("Initial temperature must be positive")
        if final_temperature <= 0:
            raise ValueError("Final temperature must be positive")
        if initial_temperature <= final_temperature:
            raise ValueError(
                "Initial temperature must be greater than final temperature"
            )
        if max_iterations <= 0:
            raise ValueError("Max iterations must be positive")

        self.initial_temperature = initial_temperature
        self.final_temperature = final_temperature
        self.max_iterations = max_iterations
        self.schedule_type = schedule_type
        self._calculate_cooling_factor()

    def _calculate_cooling_factor(self) -> None:
        """Calculate cooling factor based on schedule type."""
        if self.schedule_type == "exponential":
            # T(k) = T0 * alpha^k where alpha = (Tf/T0)^(1/max_iter)
            self.alpha = (self.final_temperature / self.initial_temperature) ** (
                1.0 / self.max_iterations
            )
        elif self.schedule_type == "geometric":
            # Similar to exponential but with different interpretation
            self.alpha = (self.final_temperature / self.initial_temperature) ** (
                1.0 / self.max_iterations
            )
        elif self.schedule_type == "linear":
            # T(k) = T0 - k * (T0 - Tf) / max_iter
            self.cooling_rate = (
                self.initial_temperature - self.final_temperature
            ) / self.max_iterations
        elif self.schedule_type == "logarithmic":
            # T(k) = T0 / (1 + log(1 + k))
            self.log_base = (
                self.initial_temperature / self.final_temperature - 1
            ) ** (1.0 / self.max_iterations)
        else:
            raise ValueError(
                f"Unknown schedule type: {self.schedule_type}. "
                "Must be 'exponential', 'linear', 'logarithmic', or 'geometric'"
            )

    def get_temperature(self, iteration: int) -> float:
        """Get temperature for given iteration.

        Args:
            iteration: Current iteration number (0-indexed).

        Returns:
            Current temperature value.

        Raises:
            ValueError: If iteration is out of valid range.
        """
        if iteration < 0 or iteration > self.max_iterations:
            raise ValueError(
                f"Iteration {iteration} out of range [0, {self.max_iterations}]"
            )

        if self.schedule_type == "exponential":
            return self.initial_temperature * (self.alpha ** iteration)
        elif self.schedule_type == "geometric":
            return self.initial_temperature * (self.alpha ** iteration)
        elif self.schedule_type == "linear":
            temp = self.initial_temperature - iteration * self.cooling_rate
            return max(temp, self.final_temperature)
        elif self.schedule_type == "logarithmic":
            return self.initial_temperature / (1 + math.log(1 + iteration))
        else:
            return self.final_temperature


class AcceptanceCriterion:
    """Manages acceptance criteria for simulated annealing."""

    @staticmethod
    def metropolis(
        current_energy: float,
        candidate_energy: float,
        temperature: float,
    ) -> bool:
        """Metropolis acceptance criterion.

        Accepts candidate if it's better, or with probability
        exp(-(E_new - E_old) / T) if it's worse.

        Args:
            current_energy: Energy of current solution.
            candidate_energy: Energy of candidate solution.
            temperature: Current temperature.

        Returns:
            True if candidate should be accepted, False otherwise.

        Raises:
            ValueError: If temperature is non-positive.
        """
        if temperature <= 0:
            raise ValueError("Temperature must be positive for acceptance")

        if candidate_energy <= current_energy:
            return True

        delta_energy = candidate_energy - current_energy
        probability = math.exp(-delta_energy / temperature)
        return random.random() < probability

    @staticmethod
    def threshold(
        current_energy: float,
        candidate_energy: float,
        temperature: float,
        threshold: float = 0.5,
    ) -> bool:
        """Threshold-based acceptance criterion.

        Accepts candidate if improvement ratio exceeds threshold.

        Args:
            current_energy: Energy of current solution.
            candidate_energy: Energy of candidate solution.
            temperature: Current temperature (not used but kept for interface).
            threshold: Acceptance threshold (default: 0.5).

        Returns:
            True if candidate should be accepted, False otherwise.
        """
        if candidate_energy <= current_energy:
            return True

        improvement_ratio = (current_energy - candidate_energy) / abs(
            current_energy
        )
        return improvement_ratio >= threshold


class SimulatedAnnealing:
    """Implements simulated annealing for global optimization."""

    def __init__(self, config_path: str = "config.yaml") -> None:
        """Initialize SimulatedAnnealing with configuration.

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
        sa_config = self.config.get("simulated_annealing", {})
        self.initial_temperature = sa_config.get("initial_temperature", 100.0)
        self.final_temperature = sa_config.get("final_temperature", 0.01)
        self.max_iterations = sa_config.get("max_iterations", 1000)
        self.schedule_type = sa_config.get("schedule_type", "exponential")
        self.acceptance_criterion = sa_config.get(
            "acceptance_criterion", "metropolis"
        )
        self.random_seed = sa_config.get("random_seed", None)

        if self.random_seed is not None:
            random.seed(self.random_seed)
            np.random.seed(self.random_seed)

        self.temperature_scheduler = TemperatureScheduler(
            self.initial_temperature,
            self.final_temperature,
            self.max_iterations,
            self.schedule_type,
        )

    def _generate_neighbor(
        self,
        current_solution: np.ndarray,
        bounds: Optional[List[Tuple[float, float]]],
        step_size: float,
    ) -> np.ndarray:
        """Generate a neighboring solution.

        Args:
            current_solution: Current solution vector.
            bounds: Optional list of (min, max) bounds for each dimension.
            step_size: Maximum step size for perturbation.

        Returns:
            New candidate solution vector.
        """
        dimension = len(current_solution)
        perturbation = np.random.normal(0, step_size, dimension)
        candidate = current_solution + perturbation

        if bounds is not None:
            for i in range(dimension):
                min_val, max_val = bounds[i]
                candidate[i] = np.clip(candidate[i], min_val, max_val)

        return candidate

    def optimize(
        self,
        objective_function: Callable[[np.ndarray], float],
        initial_solution: Optional[np.ndarray] = None,
        bounds: Optional[List[Tuple[float, float]]] = None,
        dimension: int = 2,
        step_size: float = 1.0,
    ) -> Dict[str, any]:
        """Run simulated annealing optimization.

        Args:
            objective_function: Function to minimize (takes array, returns float).
            initial_solution: Optional starting solution. If None, random.
            bounds: Optional list of (min, max) bounds for each dimension.
            dimension: Problem dimension (used if initial_solution is None).
            step_size: Maximum step size for neighbor generation.

        Returns:
            Dictionary containing:
                - best_solution: Best solution found
                - best_energy: Best energy value
                - iterations: Total iterations performed
                - history: List of (iteration, energy, temperature) tuples
                - converged: Whether algorithm converged

        Raises:
            ValueError: If parameters are invalid.
        """
        if initial_solution is None:
            if bounds is not None:
                initial_solution = np.array(
                    [
                        random.uniform(bounds[i][0], bounds[i][1])
                        for i in range(dimension)
                    ]
                )
            else:
                initial_solution = np.random.uniform(-10, 10, dimension)
        else:
            dimension = len(initial_solution)

        if bounds is not None and len(bounds) != dimension:
            raise ValueError(
                f"Bounds length {len(bounds)} doesn't match "
                f"dimension {dimension}"
            )

        current_solution = initial_solution.copy()
        current_energy = objective_function(current_solution)
        best_solution = current_solution.copy()
        best_energy = current_energy

        history = []
        converged = False

        logger.info(
            f"Starting simulated annealing: initial_energy={current_energy:.6f}"
        )

        for iteration in range(self.max_iterations):
            temperature = self.temperature_scheduler.get_temperature(iteration)

            candidate_solution = self._generate_neighbor(
                current_solution, bounds, step_size
            )
            candidate_energy = objective_function(candidate_solution)

            if self.acceptance_criterion == "metropolis":
                accepted = AcceptanceCriterion.metropolis(
                    current_energy, candidate_energy, temperature
                )
            elif self.acceptance_criterion == "threshold":
                threshold_val = self.config.get("simulated_annealing", {}).get(
                    "threshold", 0.5
                )
                accepted = AcceptanceCriterion.threshold(
                    current_energy, candidate_energy, temperature, threshold_val
                )
            else:
                accepted = AcceptanceCriterion.metropolis(
                    current_energy, candidate_energy, temperature
                )

            if accepted:
                current_solution = candidate_solution
                current_energy = candidate_energy

                if candidate_energy < best_energy:
                    best_solution = candidate_solution.copy()
                    best_energy = candidate_energy
                    logger.debug(
                        f"Iteration {iteration}: new best energy "
                        f"{best_energy:.6f}"
                    )

            history.append((iteration, current_energy, temperature))

            if iteration % (self.max_iterations // 10) == 0:
                logger.info(
                    f"Iteration {iteration}: energy={current_energy:.6f}, "
                    f"temperature={temperature:.6f}"
                )

            if temperature <= self.final_temperature:
                converged = True
                logger.info(f"Converged at iteration {iteration}")
                break

        logger.info(
            f"Optimization complete: best_energy={best_energy:.6f}, "
            f"iterations={iteration+1}"
        )

        return {
            "best_solution": best_solution,
            "best_energy": best_energy,
            "iterations": iteration + 1,
            "history": history,
            "converged": converged,
        }


def main() -> None:
    """Main entry point for command-line usage."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Simulated Annealing for Global Optimization"
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
        help="Run test optimization problem",
    )

    args = parser.parse_args()

    sa = SimulatedAnnealing(config_path=args.config)

    if args.test:
        # Test with Rastrigin function (common optimization benchmark)
        def rastrigin(x: np.ndarray) -> float:
            """Rastrigin function: global minimum at origin."""
            n = len(x)
            A = 10
            return A * n + np.sum(x ** 2 - A * np.cos(2 * np.pi * x))

        logger.info("Running test optimization on Rastrigin function")
        result = sa.optimize(
            rastrigin,
            dimension=2,
            bounds=[(-5.12, 5.12), (-5.12, 5.12)],
            step_size=0.5,
        )

        print(f"\nOptimization Results:")
        print(f"Best solution: {result['best_solution']}")
        print(f"Best energy: {result['best_energy']:.6f}")
        print(f"Iterations: {result['iterations']}")
        print(f"Converged: {result['converged']}")


if __name__ == "__main__":
    main()
