"""Unit tests for genetic algorithm implementation."""

import tempfile
from pathlib import Path

import numpy as np
import pytest
import yaml

from src.main import (
    CrossoverOperator,
    GeneticAlgorithm,
    MutationOperator,
    SelectionOperator,
)


class TestSelectionOperator:
    """Test selection operator functionality."""

    def test_tournament_selection(self):
        """Test tournament selection."""
        population = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
        fitness = np.array([10.0, 5.0, 2.0, 8.0])

        selected, indices = SelectionOperator.tournament_selection(
            population, fitness, tournament_size=2
        )

        assert len(selected) == len(population)
        assert len(indices) == len(population)
        assert all(idx in range(len(population)) for idx in indices)

    def test_roulette_wheel_selection(self):
        """Test roulette wheel selection."""
        population = np.array([[1, 2], [3, 4], [5, 6]])
        fitness = np.array([10.0, 5.0, 2.0])

        selected, indices = SelectionOperator.roulette_wheel_selection(
            population, fitness
        )

        assert len(selected) == len(population)
        assert len(indices) == len(population)

    def test_rank_based_selection(self):
        """Test rank-based selection."""
        population = np.array([[1, 2], [3, 4], [5, 6]])
        fitness = np.array([10.0, 5.0, 2.0])

        selected, indices = SelectionOperator.rank_based_selection(
            population, fitness, selection_pressure=1.5
        )

        assert len(selected) == len(population)
        assert len(indices) == len(population)

    def test_elitism_selection(self):
        """Test elitism selection."""
        population = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
        fitness = np.array([10.0, 5.0, 2.0, 8.0])

        selected, indices = SelectionOperator.elitism_selection(
            population, fitness, elite_size=2
        )

        assert len(selected) == 2
        assert len(indices) == 2
        assert np.argmin(fitness) in indices


class TestCrossoverOperator:
    """Test crossover operator functionality."""

    def test_single_point_crossover(self):
        """Test single-point crossover."""
        parent1 = np.array([1, 2, 3, 4, 5])
        parent2 = np.array([6, 7, 8, 9, 10])

        offspring1, offspring2 = CrossoverOperator.single_point_crossover(
            parent1, parent2, crossover_rate=1.0
        )

        assert len(offspring1) == len(parent1)
        assert len(offspring2) == len(parent2)
        assert np.allclose(offspring1 + offspring2, parent1 + parent2)

    def test_single_point_crossover_no_crossover(self):
        """Test single-point crossover with zero rate."""
        parent1 = np.array([1, 2, 3])
        parent2 = np.array([4, 5, 6])

        offspring1, offspring2 = CrossoverOperator.single_point_crossover(
            parent1, parent2, crossover_rate=0.0
        )

        np.testing.assert_array_equal(offspring1, parent1)
        np.testing.assert_array_equal(offspring2, parent2)

    def test_multi_point_crossover(self):
        """Test multi-point crossover."""
        parent1 = np.array([1, 2, 3, 4, 5])
        parent2 = np.array([6, 7, 8, 9, 10])

        offspring1, offspring2 = CrossoverOperator.multi_point_crossover(
            parent1, parent2, num_points=2, crossover_rate=1.0
        )

        assert len(offspring1) == len(parent1)
        assert len(offspring2) == len(parent2)

    def test_uniform_crossover(self):
        """Test uniform crossover."""
        parent1 = np.array([1, 2, 3, 4, 5])
        parent2 = np.array([6, 7, 8, 9, 10])

        offspring1, offspring2 = CrossoverOperator.uniform_crossover(
            parent1, parent2, crossover_rate=1.0, mixing_ratio=0.5
        )

        assert len(offspring1) == len(parent1)
        assert len(offspring2) == len(parent2)

    def test_arithmetic_crossover(self):
        """Test arithmetic crossover."""
        parent1 = np.array([1.0, 2.0, 3.0])
        parent2 = np.array([4.0, 5.0, 6.0])

        offspring1, offspring2 = CrossoverOperator.arithmetic_crossover(
            parent1, parent2, crossover_rate=1.0, alpha=0.5
        )

        assert len(offspring1) == len(parent1)
        assert len(offspring2) == len(parent2)
        np.testing.assert_allclose(
            offspring1 + offspring2, parent1 + parent2, rtol=1e-10
        )


class TestMutationOperator:
    """Test mutation operator functionality."""

    def test_gaussian_mutation(self):
        """Test Gaussian mutation."""
        individual = np.array([1.0, 2.0, 3.0])
        mutated = MutationOperator.gaussian_mutation(
            individual, mutation_rate=1.0, mutation_strength=0.1
        )

        assert len(mutated) == len(individual)
        assert not np.array_equal(mutated, individual)

    def test_gaussian_mutation_with_bounds(self):
        """Test Gaussian mutation with bounds."""
        individual = np.array([1.0, 2.0, 3.0])
        bounds = [(0.0, 5.0), (0.0, 5.0), (0.0, 5.0)]

        mutated = MutationOperator.gaussian_mutation(
            individual,
            mutation_rate=1.0,
            mutation_strength=1.0,
            bounds=bounds,
        )

        assert len(mutated) == len(individual)
        for i in range(len(mutated)):
            assert bounds[i][0] <= mutated[i] <= bounds[i][1]

    def test_uniform_mutation(self):
        """Test uniform mutation."""
        individual = np.array([1.0, 2.0, 3.0])
        mutated = MutationOperator.uniform_mutation(
            individual, mutation_rate=1.0, mutation_range=0.5
        )

        assert len(mutated) == len(individual)

    def test_uniform_mutation_with_bounds(self):
        """Test uniform mutation with bounds."""
        individual = np.array([1.0, 2.0, 3.0])
        bounds = [(0.0, 5.0), (0.0, 5.0), (0.0, 5.0)]

        mutated = MutationOperator.uniform_mutation(
            individual,
            mutation_rate=1.0,
            mutation_range=1.0,
            bounds=bounds,
        )

        for i in range(len(mutated)):
            assert bounds[i][0] <= mutated[i] <= bounds[i][1]

    def test_swap_mutation(self):
        """Test swap mutation."""
        individual = np.array([1, 2, 3, 4, 5])
        mutated = MutationOperator.swap_mutation(
            individual, mutation_rate=1.0
        )

        assert len(mutated) == len(individual)
        assert set(mutated) == set(individual)

    def test_polynomial_mutation(self):
        """Test polynomial mutation."""
        individual = np.array([1.0, 2.0, 3.0])
        bounds = [(0.0, 5.0), (0.0, 5.0), (0.0, 5.0)]

        mutated = MutationOperator.polynomial_mutation(
            individual, mutation_rate=1.0, eta=20.0, bounds=bounds
        )

        assert len(mutated) == len(individual)
        for i in range(len(mutated)):
            assert bounds[i][0] <= mutated[i] <= bounds[i][1]

    def test_polynomial_mutation_requires_bounds(self):
        """Test that polynomial mutation requires bounds."""
        individual = np.array([1.0, 2.0, 3.0])

        with pytest.raises(ValueError, match="requires bounds"):
            MutationOperator.polynomial_mutation(
                individual, mutation_rate=1.0, eta=20.0, bounds=None
            )


class TestGeneticAlgorithm:
    """Test genetic algorithm optimization."""

    def create_temp_config(self, config_dict: dict) -> str:
        """Create temporary config file for testing."""
        temp_file = tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False
        )
        yaml.dump(config_dict, temp_file)
        temp_file.close()
        return temp_file.name

    def test_initialization_with_default_config(self):
        """Test initialization with default config file."""
        ga = GeneticAlgorithm()
        assert ga.population_size > 0
        assert ga.max_generations > 0
        assert 0 <= ga.crossover_rate <= 1
        assert 0 <= ga.mutation_rate <= 1

    def test_initialization_with_custom_config(self):
        """Test initialization with custom config file."""
        config = {
            "genetic_algorithm": {
                "population_size": 30,
                "max_generations": 50,
                "crossover_rate": 0.9,
                "mutation_rate": 0.2,
                "elite_size": 2,
                "selection_type": "roulette",
                "crossover_type": "uniform",
                "mutation_type": "uniform",
            },
            "logging": {"level": "INFO", "file": "logs/test.log"},
        }

        config_path = self.create_temp_config(config)
        try:
            ga = GeneticAlgorithm(config_path=config_path)
            assert ga.population_size == 30
            assert ga.max_generations == 50
            assert ga.crossover_rate == 0.9
            assert ga.mutation_rate == 0.2
            assert ga.elite_size == 2
        finally:
            Path(config_path).unlink()

    def test_optimize_quadratic_function(self):
        """Test optimization on simple quadratic function."""
        ga = GeneticAlgorithm()

        def quadratic(x):
            return np.sum(x ** 2)

        result = ga.optimize(
            quadratic,
            dimension=2,
            bounds=[(-10, 10), (-10, 10)],
        )

        assert "best_solution" in result
        assert "best_fitness" in result
        assert "generations" in result
        assert "history" in result
        assert "final_population" in result
        assert "final_fitness" in result
        assert result["best_fitness"] >= 0
        assert len(result["best_solution"]) == 2

    def test_optimize_with_initial_population(self):
        """Test optimization with provided initial population."""
        config = {
            "genetic_algorithm": {
                "population_size": 4,
                "max_generations": 10,
                "crossover_rate": 0.8,
                "mutation_rate": 0.1,
            },
            "logging": {"level": "WARNING", "file": "logs/test.log"},
        }

        config_path = self.create_temp_config(config)
        try:
            ga = GeneticAlgorithm(config_path=config_path)

            def objective(x):
                return np.sum(x ** 2)

            initial_pop = np.array(
                [[1, 1], [2, 2], [3, 3], [4, 4]]
            )

            result = ga.optimize(
                objective,
                dimension=2,
                initial_population=initial_pop,
                bounds=[(-10, 10), (-10, 10)],
            )

            assert len(result["best_solution"]) == 2
        finally:
            Path(config_path).unlink()

    def test_optimize_rastrigin_function(self):
        """Test optimization on Rastrigin function."""
        ga = GeneticAlgorithm()

        def rastrigin(x):
            n = len(x)
            A = 10
            return A * n + np.sum(x ** 2 - A * np.cos(2 * np.pi * x))

        result = ga.optimize(
            rastrigin,
            dimension=2,
            bounds=[(-5.12, 5.12), (-5.12, 5.12)],
        )

        assert result["best_fitness"] >= 0
        assert len(result["history"]) == result["generations"]

    def test_optimize_without_bounds(self):
        """Test optimization without bounds."""
        ga = GeneticAlgorithm()

        def objective(x):
            return np.sum(x ** 2)

        result = ga.optimize(
            objective,
            dimension=3,
        )

        assert len(result["best_solution"]) == 3

    def test_optimize_improves_solution(self):
        """Test that optimization improves solution over generations."""
        ga = GeneticAlgorithm()

        def objective(x):
            return np.sum(x ** 2)

        result = ga.optimize(
            objective,
            dimension=2,
            bounds=[(-10, 10), (-10, 10)],
        )

        initial_fitness = result["history"][0][1]
        final_fitness = result["best_fitness"]

        assert final_fitness <= initial_fitness

    def test_invalid_bounds_length(self):
        """Test that mismatched bounds length raises error."""
        ga = GeneticAlgorithm()

        def objective(x):
            return np.sum(x ** 2)

        with pytest.raises(ValueError, match="Bounds length"):
            ga.optimize(
                objective,
                dimension=2,
                bounds=[(-10, 10)],
            )

    def test_invalid_initial_population_size(self):
        """Test that mismatched initial population size raises error."""
        ga = GeneticAlgorithm()

        def objective(x):
            return np.sum(x ** 2)

        initial_pop = np.array([[1, 1], [2, 2]])

        with pytest.raises(ValueError, match="population size"):
            ga.optimize(
                objective,
                dimension=2,
                initial_population=initial_pop,
            )

    def test_config_file_not_found(self):
        """Test that missing config file raises error."""
        with pytest.raises(FileNotFoundError):
            GeneticAlgorithm(config_path="nonexistent.yaml")

    def test_history_tracking(self):
        """Test that generation history is properly tracked."""
        ga = GeneticAlgorithm()

        def objective(x):
            return np.sum(x ** 2)

        result = ga.optimize(
            objective,
            dimension=2,
            bounds=[(-10, 10), (-10, 10)],
        )

        assert len(result["history"]) == result["generations"]
        for generation, best_fitness, avg_fitness in result["history"]:
            assert isinstance(generation, int)
            assert isinstance(best_fitness, (int, float))
            assert isinstance(avg_fitness, (int, float))
            assert best_fitness >= 0

    def test_different_selection_types(self):
        """Test optimization with different selection types."""
        selection_types = ["tournament", "roulette", "rank"]

        for selection_type in selection_types:
            config = {
                "genetic_algorithm": {
                    "population_size": 20,
                    "max_generations": 10,
                    "crossover_rate": 0.8,
                    "mutation_rate": 0.1,
                    "selection_type": selection_type,
                    "crossover_type": "single_point",
                    "mutation_type": "gaussian",
                },
                "logging": {"level": "WARNING", "file": "logs/test.log"},
            }

            config_path = self.create_temp_config(config)
            try:
                ga = GeneticAlgorithm(config_path=config_path)

                def objective(x):
                    return np.sum(x ** 2)

                result = ga.optimize(
                    objective,
                    dimension=2,
                    bounds=[(-10, 10), (-10, 10)],
                )

                assert result["best_fitness"] >= 0
            finally:
                Path(config_path).unlink()

    def test_different_crossover_types(self):
        """Test optimization with different crossover types."""
        crossover_types = ["single_point", "multi_point", "uniform", "arithmetic"]

        for crossover_type in crossover_types:
            config = {
                "genetic_algorithm": {
                    "population_size": 20,
                    "max_generations": 10,
                    "crossover_rate": 0.8,
                    "mutation_rate": 0.1,
                    "selection_type": "tournament",
                    "crossover_type": crossover_type,
                    "mutation_type": "gaussian",
                },
                "logging": {"level": "WARNING", "file": "logs/test.log"},
            }

            config_path = self.create_temp_config(config)
            try:
                ga = GeneticAlgorithm(config_path=config_path)

                def objective(x):
                    return np.sum(x ** 2)

                result = ga.optimize(
                    objective,
                    dimension=2,
                    bounds=[(-10, 10), (-10, 10)],
                )

                assert result["best_fitness"] >= 0
            finally:
                Path(config_path).unlink()

    def test_different_mutation_types(self):
        """Test optimization with different mutation types."""
        mutation_types = ["gaussian", "uniform", "swap"]

        for mutation_type in mutation_types:
            config = {
                "genetic_algorithm": {
                    "population_size": 20,
                    "max_generations": 10,
                    "crossover_rate": 0.8,
                    "mutation_rate": 0.1,
                    "selection_type": "tournament",
                    "crossover_type": "single_point",
                    "mutation_type": mutation_type,
                },
                "logging": {"level": "WARNING", "file": "logs/test.log"},
            }

            config_path = self.create_temp_config(config)
            try:
                ga = GeneticAlgorithm(config_path=config_path)

                def objective(x):
                    return np.sum(x ** 2)

                result = ga.optimize(
                    objective,
                    dimension=2,
                    bounds=[(-10, 10), (-10, 10)],
                )

                assert result["best_fitness"] >= 0
            finally:
                Path(config_path).unlink()

    def test_random_seed_reproducibility(self):
        """Test that random seed produces reproducible results."""
        config = {
            "genetic_algorithm": {
                "population_size": 20,
                "max_generations": 10,
                "crossover_rate": 0.8,
                "mutation_rate": 0.1,
                "random_seed": 42,
            },
            "logging": {"level": "WARNING", "file": "logs/test.log"},
        }

        config_path = self.create_temp_config(config)
        try:
            ga1 = GeneticAlgorithm(config_path=config_path)

            def objective(x):
                return np.sum(x ** 2)

            result1 = ga1.optimize(
                objective,
                dimension=2,
                bounds=[(-10, 10), (-10, 10)],
            )

            ga2 = GeneticAlgorithm(config_path=config_path)
            result2 = ga2.optimize(
                objective,
                dimension=2,
                bounds=[(-10, 10), (-10, 10)],
            )

            np.testing.assert_array_almost_equal(
                result1["best_solution"],
                result2["best_solution"],
                decimal=5,
            )
        finally:
            Path(config_path).unlink()

    def test_elitism_preserves_best(self):
        """Test that elitism preserves best solutions."""
        config = {
            "genetic_algorithm": {
                "population_size": 20,
                "max_generations": 10,
                "crossover_rate": 0.8,
                "mutation_rate": 0.1,
                "elite_size": 2,
            },
            "logging": {"level": "WARNING", "file": "logs/test.log"},
        }

        config_path = self.create_temp_config(config)
        try:
            ga = GeneticAlgorithm(config_path=config_path)

            def objective(x):
                return np.sum(x ** 2)

            result = ga.optimize(
                objective,
                dimension=2,
                bounds=[(-10, 10), (-10, 10)],
            )

            assert result["best_fitness"] >= 0
        finally:
            Path(config_path).unlink()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
