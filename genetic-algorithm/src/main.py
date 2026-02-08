"""Genetic Algorithm for Optimization.

This module provides functionality to solve optimization problems using
genetic algorithm with configurable selection, crossover, and mutation
operators.
"""

import logging
import logging.handlers
import random
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

import numpy as np
import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class SelectionOperator:
    """Implements various selection operators for genetic algorithm."""

    @staticmethod
    def tournament_selection(
        population: np.ndarray,
        fitness: np.ndarray,
        tournament_size: int = 3,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Select parents using tournament selection.

        Args:
            population: Array of individuals (population_size, dimension).
            fitness: Array of fitness values (population_size,).
            tournament_size: Number of individuals competing in tournament.

        Returns:
            Tuple of (selected_parents, selected_indices).
        """
        population_size = len(population)
        selected_indices = []

        for _ in range(population_size):
            tournament_indices = np.random.choice(
                population_size, size=tournament_size, replace=False
            )
            tournament_fitness = fitness[tournament_indices]
            winner_idx = tournament_indices[np.argmin(tournament_fitness)]
            selected_indices.append(winner_idx)

        return population[selected_indices], np.array(selected_indices)

    @staticmethod
    def roulette_wheel_selection(
        population: np.ndarray,
        fitness: np.ndarray,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Select parents using roulette wheel selection.

        Converts minimization to maximization by inverting fitness.

        Args:
            population: Array of individuals (population_size, dimension).
            fitness: Array of fitness values (population_size,).

        Returns:
            Tuple of (selected_parents, selected_indices).
        """
        max_fitness = np.max(fitness)
        adjusted_fitness = max_fitness - fitness + 1e-10
        probabilities = adjusted_fitness / np.sum(adjusted_fitness)

        population_size = len(population)
        selected_indices = np.random.choice(
            population_size, size=population_size, p=probabilities
        )

        return population[selected_indices], selected_indices

    @staticmethod
    def rank_based_selection(
        population: np.ndarray,
        fitness: np.ndarray,
        selection_pressure: float = 2.0,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Select parents using rank-based selection.

        Args:
            population: Array of individuals (population_size, dimension).
            fitness: Array of fitness values (population_size,).
            selection_pressure: Selection pressure parameter (1.0-2.0).

        Returns:
            Tuple of (selected_parents, selected_indices).
        """
        population_size = len(population)
        ranks = np.argsort(np.argsort(fitness))
        probabilities = (
            selection_pressure
            - (2 * selection_pressure - 2) * ranks / (population_size - 1)
        )
        probabilities = probabilities / np.sum(probabilities)

        selected_indices = np.random.choice(
            population_size, size=population_size, p=probabilities
        )

        return population[selected_indices], selected_indices

    @staticmethod
    def elitism_selection(
        population: np.ndarray,
        fitness: np.ndarray,
        elite_size: int = 1,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Select best individuals using elitism.

        Args:
            population: Array of individuals (population_size, dimension).
            fitness: Array of fitness values (population_size,).
            elite_size: Number of elite individuals to select.

        Returns:
            Tuple of (selected_parents, selected_indices).
        """
        elite_indices = np.argsort(fitness)[:elite_size]
        return population[elite_indices], elite_indices


class CrossoverOperator:
    """Implements various crossover operators for genetic algorithm."""

    @staticmethod
    def single_point_crossover(
        parent1: np.ndarray,
        parent2: np.ndarray,
        crossover_rate: float = 0.8,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Perform single-point crossover.

        Args:
            parent1: First parent individual.
            parent2: Second parent individual.
            crossover_rate: Probability of crossover occurring.

        Returns:
            Tuple of (offspring1, offspring2).
        """
        if random.random() > crossover_rate:
            return parent1.copy(), parent2.copy()

        dimension = len(parent1)
        crossover_point = random.randint(1, dimension - 1)

        offspring1 = np.concatenate(
            [parent1[:crossover_point], parent2[crossover_point:]]
        )
        offspring2 = np.concatenate(
            [parent2[:crossover_point], parent1[crossover_point:]]
        )

        return offspring1, offspring2

    @staticmethod
    def multi_point_crossover(
        parent1: np.ndarray,
        parent2: np.ndarray,
        num_points: int = 2,
        crossover_rate: float = 0.8,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Perform multi-point crossover.

        Args:
            parent1: First parent individual.
            parent2: Second parent individual.
            num_points: Number of crossover points.
            crossover_rate: Probability of crossover occurring.

        Returns:
            Tuple of (offspring1, offspring2).
        """
        if random.random() > crossover_rate:
            return parent1.copy(), parent2.copy()

        dimension = len(parent1)
        crossover_points = sorted(
            random.sample(range(1, dimension), min(num_points, dimension - 1))
        )
        crossover_points = [0] + crossover_points + [dimension]

        offspring1 = np.zeros_like(parent1)
        offspring2 = np.zeros_like(parent2)

        for i in range(len(crossover_points) - 1):
            start = crossover_points[i]
            end = crossover_points[i + 1]
            if i % 2 == 0:
                offspring1[start:end] = parent1[start:end]
                offspring2[start:end] = parent2[start:end]
            else:
                offspring1[start:end] = parent2[start:end]
                offspring2[start:end] = parent1[start:end]

        return offspring1, offspring2

    @staticmethod
    def uniform_crossover(
        parent1: np.ndarray,
        parent2: np.ndarray,
        crossover_rate: float = 0.8,
        mixing_ratio: float = 0.5,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Perform uniform crossover.

        Args:
            parent1: First parent individual.
            parent2: Second parent individual.
            crossover_rate: Probability of crossover occurring.
            mixing_ratio: Probability of taking gene from parent1.

        Returns:
            Tuple of (offspring1, offspring2).
        """
        if random.random() > crossover_rate:
            return parent1.copy(), parent2.copy()

        mask = np.random.random(len(parent1)) < mixing_ratio
        offspring1 = np.where(mask, parent1, parent2)
        offspring2 = np.where(mask, parent2, parent1)

        return offspring1, offspring2

    @staticmethod
    def arithmetic_crossover(
        parent1: np.ndarray,
        parent2: np.ndarray,
        crossover_rate: float = 0.8,
        alpha: float = 0.5,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Perform arithmetic crossover (blend crossover).

        Args:
            parent1: First parent individual.
            parent2: Second parent individual.
            crossover_rate: Probability of crossover occurring.
            alpha: Blend parameter (0.0-1.0).

        Returns:
            Tuple of (offspring1, offspring2).
        """
        if random.random() > crossover_rate:
            return parent1.copy(), parent2.copy()

        offspring1 = alpha * parent1 + (1 - alpha) * parent2
        offspring2 = (1 - alpha) * parent1 + alpha * parent2

        return offspring1, offspring2


class MutationOperator:
    """Implements various mutation operators for genetic algorithm."""

    @staticmethod
    def gaussian_mutation(
        individual: np.ndarray,
        mutation_rate: float = 0.1,
        mutation_strength: float = 0.1,
        bounds: Optional[List[Tuple[float, float]]] = None,
    ) -> np.ndarray:
        """Apply Gaussian mutation to individual.

        Args:
            individual: Individual to mutate.
            mutation_rate: Probability of mutating each gene.
            mutation_strength: Standard deviation of Gaussian noise.
            bounds: Optional bounds for each dimension.

        Returns:
            Mutated individual.
        """
        mutated = individual.copy()
        mask = np.random.random(len(individual)) < mutation_rate
        noise = np.random.normal(0, mutation_strength, len(individual))
        mutated[mask] += noise[mask]

        if bounds is not None:
            for i in range(len(mutated)):
                min_val, max_val = bounds[i]
                mutated[i] = np.clip(mutated[i], min_val, max_val)

        return mutated

    @staticmethod
    def uniform_mutation(
        individual: np.ndarray,
        mutation_rate: float = 0.1,
        mutation_range: float = 1.0,
        bounds: Optional[List[Tuple[float, float]]] = None,
    ) -> np.ndarray:
        """Apply uniform mutation to individual.

        Args:
            individual: Individual to mutate.
            mutation_rate: Probability of mutating each gene.
            mutation_range: Range of uniform mutation.
            bounds: Optional bounds for each dimension.

        Returns:
            Mutated individual.
        """
        mutated = individual.copy()
        mask = np.random.random(len(individual)) < mutation_rate
        noise = np.random.uniform(
            -mutation_range, mutation_range, len(individual)
        )
        mutated[mask] += noise[mask]

        if bounds is not None:
            for i in range(len(mutated)):
                min_val, max_val = bounds[i]
                mutated[i] = np.clip(mutated[i], min_val, max_val)

        return mutated

    @staticmethod
    def swap_mutation(
        individual: np.ndarray,
        mutation_rate: float = 0.1,
    ) -> np.ndarray:
        """Apply swap mutation to individual (swaps two genes).

        Args:
            individual: Individual to mutate.
            mutation_rate: Probability of mutation occurring.

        Returns:
            Mutated individual.
        """
        if random.random() > mutation_rate:
            return individual.copy()

        mutated = individual.copy()
        indices = np.random.choice(len(individual), size=2, replace=False)
        mutated[indices[0]], mutated[indices[1]] = (
            mutated[indices[1]],
            mutated[indices[0]],
        )

        return mutated

    @staticmethod
    def polynomial_mutation(
        individual: np.ndarray,
        mutation_rate: float = 0.1,
        eta: float = 20.0,
        bounds: Optional[List[Tuple[float, float]]] = None,
    ) -> np.ndarray:
        """Apply polynomial mutation (common in NSGA-II).

        Args:
            individual: Individual to mutate.
            mutation_rate: Probability of mutating each gene.
            eta: Distribution index (higher = less disruptive).
            bounds: Optional bounds for each dimension.

        Returns:
            Mutated individual.
        """
        mutated = individual.copy()

        if bounds is None:
            raise ValueError("Polynomial mutation requires bounds")

        for i in range(len(individual)):
            if random.random() < mutation_rate:
                min_val, max_val = bounds[i]
                delta = (mutated[i] - min_val) / (max_val - min_val)
                u = random.random()

                if u < 0.5:
                    delta_q = (2 * u + (1 - 2 * u) * (1 - delta) ** (eta + 1)) ** (
                        1 / (eta + 1)
                    ) - 1
                else:
                    delta_q = 1 - (
                        2 * (1 - u)
                        + 2 * (u - 0.5) * delta ** (eta + 1)
                    ) ** (1 / (eta + 1))

                mutated[i] = mutated[i] + delta_q * (max_val - min_val)
                mutated[i] = np.clip(mutated[i], min_val, max_val)

        return mutated


class GeneticAlgorithm:
    """Implements genetic algorithm for optimization."""

    def __init__(self, config_path: str = "config.yaml") -> None:
        """Initialize GeneticAlgorithm with configuration.

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
        ga_config = self.config.get("genetic_algorithm", {})
        self.population_size = ga_config.get("population_size", 50)
        self.max_generations = ga_config.get("max_generations", 100)
        self.crossover_rate = ga_config.get("crossover_rate", 0.8)
        self.mutation_rate = ga_config.get("mutation_rate", 0.1)
        self.elite_size = ga_config.get("elite_size", 1)

        self.selection_type = ga_config.get("selection_type", "tournament")
        self.selection_params = ga_config.get("selection_params", {})
        self.crossover_type = ga_config.get("crossover_type", "single_point")
        self.crossover_params = ga_config.get("crossover_params", {})
        self.mutation_type = ga_config.get("mutation_type", "gaussian")
        self.mutation_params = ga_config.get("mutation_params", {})

        self.random_seed = ga_config.get("random_seed", None)

        if self.random_seed is not None:
            random.seed(self.random_seed)
            np.random.seed(self.random_seed)

    def _initialize_population(
        self,
        dimension: int,
        bounds: Optional[List[Tuple[float, float]]],
    ) -> np.ndarray:
        """Initialize random population.

        Args:
            dimension: Problem dimension.
            bounds: Optional bounds for each dimension.

        Returns:
            Initial population array.
        """
        if bounds is not None:
            population = np.array(
                [
                    [
                        random.uniform(bounds[j][0], bounds[j][1])
                        for j in range(dimension)
                    ]
                    for _ in range(self.population_size)
                ]
            )
        else:
            population = np.random.uniform(
                -10, 10, size=(self.population_size, dimension)
            )

        return population

    def _evaluate_population(
        self,
        population: np.ndarray,
        objective_function: Callable[[np.ndarray], float],
    ) -> np.ndarray:
        """Evaluate fitness of entire population.

        Args:
            population: Population array.
            objective_function: Function to minimize.

        Returns:
            Array of fitness values.
        """
        return np.array(
            [objective_function(individual) for individual in population]
        )

    def optimize(
        self,
        objective_function: Callable[[np.ndarray], float],
        dimension: int,
        bounds: Optional[List[Tuple[float, float]]] = None,
        initial_population: Optional[np.ndarray] = None,
    ) -> Dict[str, any]:
        """Run genetic algorithm optimization.

        Args:
            objective_function: Function to minimize.
            dimension: Problem dimension.
            bounds: Optional bounds for each dimension.
            initial_population: Optional initial population.

        Returns:
            Dictionary containing:
                - best_solution: Best solution found
                - best_fitness: Best fitness value
                - generations: Total generations evolved
                - history: List of (generation, best_fitness, avg_fitness)
                - final_population: Final population
                - final_fitness: Final fitness values

        Raises:
            ValueError: If parameters are invalid.
        """
        if bounds is not None and len(bounds) != dimension:
            raise ValueError(
                f"Bounds length {len(bounds)} doesn't match "
                f"dimension {dimension}"
            )

        if initial_population is None:
            population = self._initialize_population(dimension, bounds)
        else:
            if len(initial_population) != self.population_size:
                raise ValueError(
                    f"Initial population size {len(initial_population)} "
                    f"doesn't match configured size {self.population_size}"
                )
            population = initial_population.copy()

        fitness = self._evaluate_population(population, objective_function)
        best_idx = np.argmin(fitness)
        best_solution = population[best_idx].copy()
        best_fitness = fitness[best_idx]

        history = []
        logger.info(
            f"Starting genetic algorithm: initial_best_fitness={best_fitness:.6f}"
        )

        for generation in range(self.max_generations):
            # Selection
            if self.selection_type == "tournament":
                tournament_size = self.selection_params.get(
                    "tournament_size", 3
                )
                selected, _ = SelectionOperator.tournament_selection(
                    population, fitness, tournament_size
                )
            elif self.selection_type == "roulette":
                selected, _ = SelectionOperator.roulette_wheel_selection(
                    population, fitness
                )
            elif self.selection_type == "rank":
                selection_pressure = self.selection_params.get(
                    "selection_pressure", 2.0
                )
                selected, _ = SelectionOperator.rank_based_selection(
                    population, fitness, selection_pressure
                )
            else:
                selected, _ = SelectionOperator.tournament_selection(
                    population, fitness
                )

            # Elitism
            elite_indices = np.argsort(fitness)[: self.elite_size]
            elite = population[elite_indices].copy()

            # Crossover and mutation
            new_population = []
            for i in range(0, len(selected) - 1, 2):
                parent1 = selected[i]
                parent2 = selected[i + 1]

                if self.crossover_type == "single_point":
                    offspring1, offspring2 = (
                        CrossoverOperator.single_point_crossover(
                            parent1, parent2, self.crossover_rate
                        )
                    )
                elif self.crossover_type == "multi_point":
                    num_points = self.crossover_params.get("num_points", 2)
                    offspring1, offspring2 = (
                        CrossoverOperator.multi_point_crossover(
                            parent1, parent2, num_points, self.crossover_rate
                        )
                    )
                elif self.crossover_type == "uniform":
                    mixing_ratio = self.crossover_params.get(
                        "mixing_ratio", 0.5
                    )
                    offspring1, offspring2 = (
                        CrossoverOperator.uniform_crossover(
                            parent1,
                            parent2,
                            self.crossover_rate,
                            mixing_ratio,
                        )
                    )
                elif self.crossover_type == "arithmetic":
                    alpha = self.crossover_params.get("alpha", 0.5)
                    offspring1, offspring2 = (
                        CrossoverOperator.arithmetic_crossover(
                            parent1, parent2, self.crossover_rate, alpha
                        )
                    )
                else:
                    offspring1, offspring2 = (
                        CrossoverOperator.single_point_crossover(
                            parent1, parent2, self.crossover_rate
                        )
                    )

                # Mutation
                if self.mutation_type == "gaussian":
                    mutation_strength = self.mutation_params.get(
                        "mutation_strength", 0.1
                    )
                    offspring1 = MutationOperator.gaussian_mutation(
                        offspring1,
                        self.mutation_rate,
                        mutation_strength,
                        bounds,
                    )
                    offspring2 = MutationOperator.gaussian_mutation(
                        offspring2,
                        self.mutation_rate,
                        mutation_strength,
                        bounds,
                    )
                elif self.mutation_type == "uniform":
                    mutation_range = self.mutation_params.get(
                        "mutation_range", 1.0
                    )
                    offspring1 = MutationOperator.uniform_mutation(
                        offspring1,
                        self.mutation_rate,
                        mutation_range,
                        bounds,
                    )
                    offspring2 = MutationOperator.uniform_mutation(
                        offspring2,
                        self.mutation_rate,
                        mutation_range,
                        bounds,
                    )
                elif self.mutation_type == "swap":
                    offspring1 = MutationOperator.swap_mutation(
                        offspring1, self.mutation_rate
                    )
                    offspring2 = MutationOperator.swap_mutation(
                        offspring2, self.mutation_rate
                    )
                elif self.mutation_type == "polynomial":
                    eta = self.mutation_params.get("eta", 20.0)
                    offspring1 = MutationOperator.polynomial_mutation(
                        offspring1, self.mutation_rate, eta, bounds
                    )
                    offspring2 = MutationOperator.polynomial_mutation(
                        offspring2, self.mutation_rate, eta, bounds
                    )
                else:
                    mutation_strength = self.mutation_params.get(
                        "mutation_strength", 0.1
                    )
                    offspring1 = MutationOperator.gaussian_mutation(
                        offspring1,
                        self.mutation_rate,
                        mutation_strength,
                        bounds,
                    )
                    offspring2 = MutationOperator.gaussian_mutation(
                        offspring2,
                        self.mutation_rate,
                        mutation_strength,
                        bounds,
                    )

                new_population.append(offspring1)
                new_population.append(offspring2)

            # Replace population (keep elite)
            population = np.array(new_population)
            if self.elite_size > 0:
                population[: self.elite_size] = elite

            # Evaluate new population
            fitness = self._evaluate_population(population, objective_function)
            best_idx = np.argmin(fitness)
            current_best = fitness[best_idx]

            if current_best < best_fitness:
                best_solution = population[best_idx].copy()
                best_fitness = current_best
                logger.debug(
                    f"Generation {generation}: new best fitness "
                    f"{best_fitness:.6f}"
                )

            avg_fitness = np.mean(fitness)
            history.append((generation, best_fitness, avg_fitness))

            if generation % (self.max_generations // 10) == 0:
                logger.info(
                    f"Generation {generation}: best_fitness={best_fitness:.6f}, "
                    f"avg_fitness={avg_fitness:.6f}"
                )

        logger.info(
            f"Optimization complete: best_fitness={best_fitness:.6f}, "
            f"generations={self.max_generations}"
        )

        return {
            "best_solution": best_solution,
            "best_fitness": best_fitness,
            "generations": self.max_generations,
            "history": history,
            "final_population": population,
            "final_fitness": fitness,
        }


def main() -> None:
    """Main entry point for command-line usage."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Genetic Algorithm for Optimization"
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

    ga = GeneticAlgorithm(config_path=args.config)

    if args.test:
        # Test with Rastrigin function
        def rastrigin(x: np.ndarray) -> float:
            """Rastrigin function: global minimum at origin."""
            n = len(x)
            A = 10
            return A * n + np.sum(x ** 2 - A * np.cos(2 * np.pi * x))

        logger.info("Running test optimization on Rastrigin function")
        result = ga.optimize(
            rastrigin,
            dimension=2,
            bounds=[(-5.12, 5.12), (-5.12, 5.12)],
        )

        print(f"\nOptimization Results:")
        print(f"Best solution: {result['best_solution']}")
        print(f"Best fitness: {result['best_fitness']:.6f}")
        print(f"Generations: {result['generations']}")


if __name__ == "__main__":
    main()
