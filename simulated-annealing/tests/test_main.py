"""Unit tests for simulated annealing implementation."""

import math
import tempfile
from pathlib import Path

import numpy as np
import pytest
import yaml

from src.main import (
    AcceptanceCriterion,
    SimulatedAnnealing,
    TemperatureScheduler,
)


class TestTemperatureScheduler:
    """Test temperature scheduling functionality."""

    def test_exponential_schedule(self):
        """Test exponential cooling schedule."""
        scheduler = TemperatureScheduler(
            initial_temperature=100.0,
            final_temperature=0.01,
            max_iterations=1000,
            schedule_type="exponential",
        )

        temp_0 = scheduler.get_temperature(0)
        temp_final = scheduler.get_temperature(1000)

        assert math.isclose(temp_0, 100.0, rel_tol=1e-6)
        assert math.isclose(temp_final, 0.01, rel_tol=1e-3)

    def test_linear_schedule(self):
        """Test linear cooling schedule."""
        scheduler = TemperatureScheduler(
            initial_temperature=100.0,
            final_temperature=0.01,
            max_iterations=1000,
            schedule_type="linear",
        )

        temp_0 = scheduler.get_temperature(0)
        temp_500 = scheduler.get_temperature(500)
        temp_final = scheduler.get_temperature(1000)

        assert math.isclose(temp_0, 100.0, rel_tol=1e-6)
        assert 50.0 < temp_500 < 100.0
        assert math.isclose(temp_final, 0.01, rel_tol=1e-3)

    def test_logarithmic_schedule(self):
        """Test logarithmic cooling schedule."""
        scheduler = TemperatureScheduler(
            initial_temperature=100.0,
            final_temperature=0.01,
            max_iterations=1000,
            schedule_type="logarithmic",
        )

        temp_0 = scheduler.get_temperature(0)
        temp_100 = scheduler.get_temperature(100)

        assert math.isclose(temp_0, 100.0, rel_tol=1e-6)
        assert temp_100 < temp_0

    def test_geometric_schedule(self):
        """Test geometric cooling schedule."""
        scheduler = TemperatureScheduler(
            initial_temperature=100.0,
            final_temperature=0.01,
            max_iterations=1000,
            schedule_type="geometric",
        )

        temp_0 = scheduler.get_temperature(0)
        temp_final = scheduler.get_temperature(1000)

        assert math.isclose(temp_0, 100.0, rel_tol=1e-6)
        assert math.isclose(temp_final, 0.01, rel_tol=1e-3)

    def test_temperature_decreases_monotonically(self):
        """Test that temperature decreases monotonically."""
        scheduler = TemperatureScheduler(
            initial_temperature=100.0,
            final_temperature=0.01,
            max_iterations=1000,
            schedule_type="exponential",
        )

        prev_temp = scheduler.get_temperature(0)
        for i in range(1, 1000, 100):
            curr_temp = scheduler.get_temperature(i)
            assert curr_temp <= prev_temp
            prev_temp = curr_temp

    def test_invalid_initial_temperature(self):
        """Test that negative initial temperature raises error."""
        with pytest.raises(ValueError, match="Initial temperature must be positive"):
            TemperatureScheduler(
                initial_temperature=-10.0,
                final_temperature=0.01,
                max_iterations=1000,
            )

    def test_invalid_final_temperature(self):
        """Test that negative final temperature raises error."""
        with pytest.raises(ValueError, match="Final temperature must be positive"):
            TemperatureScheduler(
                initial_temperature=100.0,
                final_temperature=-0.01,
                max_iterations=1000,
            )

    def test_invalid_temperature_order(self):
        """Test that initial < final temperature raises error."""
        with pytest.raises(
            ValueError, match="Initial temperature must be greater"
        ):
            TemperatureScheduler(
                initial_temperature=0.01,
                final_temperature=100.0,
                max_iterations=1000,
            )

    def test_invalid_schedule_type(self):
        """Test that unknown schedule type raises error."""
        with pytest.raises(ValueError, match="Unknown schedule type"):
            TemperatureScheduler(
                initial_temperature=100.0,
                final_temperature=0.01,
                max_iterations=1000,
                schedule_type="invalid",
            )

    def test_out_of_range_iteration(self):
        """Test that out-of-range iteration raises error."""
        scheduler = TemperatureScheduler(
            initial_temperature=100.0,
            final_temperature=0.01,
            max_iterations=1000,
        )

        with pytest.raises(ValueError, match="out of range"):
            scheduler.get_temperature(1001)


class TestAcceptanceCriterion:
    """Test acceptance criteria functionality."""

    def test_metropolis_accepts_better_solution(self):
        """Test that Metropolis always accepts better solutions."""
        current_energy = 10.0
        candidate_energy = 5.0
        temperature = 1.0

        assert AcceptanceCriterion.metropolis(
            current_energy, candidate_energy, temperature
        )

    def test_metropolis_rejects_much_worse_solution_at_low_temp(self):
        """Test that Metropolis rejects much worse solutions at low temp."""
        current_energy = 5.0
        candidate_energy = 100.0
        temperature = 0.01

        accepted = AcceptanceCriterion.metropolis(
            current_energy, candidate_energy, temperature
        )
        assert not accepted

    def test_metropolis_may_accept_worse_at_high_temp(self):
        """Test that Metropolis may accept worse solutions at high temp."""
        current_energy = 5.0
        candidate_energy = 6.0
        temperature = 100.0

        results = [
            AcceptanceCriterion.metropolis(
                current_energy, candidate_energy, temperature
            )
            for _ in range(100)
        ]

        assert any(results)

    def test_metropolis_invalid_temperature(self):
        """Test that zero temperature raises error."""
        with pytest.raises(ValueError, match="Temperature must be positive"):
            AcceptanceCriterion.metropolis(10.0, 5.0, 0.0)

    def test_threshold_accepts_better_solution(self):
        """Test that threshold always accepts better solutions."""
        current_energy = 10.0
        candidate_energy = 5.0
        temperature = 1.0

        assert AcceptanceCriterion.threshold(
            current_energy, candidate_energy, temperature
        )

    def test_threshold_rejects_worse_solution(self):
        """Test that threshold rejects worse solutions below threshold."""
        current_energy = 10.0
        candidate_energy = 15.0
        temperature = 1.0
        threshold = 0.5

        accepted = AcceptanceCriterion.threshold(
            current_energy, candidate_energy, temperature, threshold
        )
        assert not accepted


class TestSimulatedAnnealing:
    """Test simulated annealing optimization."""

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
        sa = SimulatedAnnealing()
        assert sa.initial_temperature > 0
        assert sa.final_temperature > 0
        assert sa.max_iterations > 0

    def test_initialization_with_custom_config(self):
        """Test initialization with custom config file."""
        config = {
            "simulated_annealing": {
                "initial_temperature": 200.0,
                "final_temperature": 0.1,
                "max_iterations": 500,
                "schedule_type": "linear",
                "acceptance_criterion": "metropolis",
            },
            "logging": {"level": "INFO", "file": "logs/test.log"},
        }

        config_path = self.create_temp_config(config)
        try:
            sa = SimulatedAnnealing(config_path=config_path)
            assert sa.initial_temperature == 200.0
            assert sa.final_temperature == 0.1
            assert sa.max_iterations == 500
            assert sa.schedule_type == "linear"
        finally:
            Path(config_path).unlink()

    def test_optimize_quadratic_function(self):
        """Test optimization on simple quadratic function."""
        sa = SimulatedAnnealing()

        def quadratic(x):
            return np.sum(x ** 2)

        result = sa.optimize(
            quadratic,
            dimension=2,
            bounds=[(-10, 10), (-10, 10)],
            step_size=1.0,
        )

        assert "best_solution" in result
        assert "best_energy" in result
        assert "iterations" in result
        assert "history" in result
        assert "converged" in result
        assert result["best_energy"] >= 0
        assert len(result["best_solution"]) == 2

    def test_optimize_with_initial_solution(self):
        """Test optimization with provided initial solution."""
        sa = SimulatedAnnealing()

        def objective(x):
            return np.sum(x ** 2)

        initial = np.array([5.0, 5.0])
        result = sa.optimize(
            objective,
            initial_solution=initial,
            bounds=[(-10, 10), (-10, 10)],
            step_size=1.0,
        )

        assert len(result["best_solution"]) == 2

    def test_optimize_rastrigin_function(self):
        """Test optimization on Rastrigin function."""
        sa = SimulatedAnnealing()

        def rastrigin(x):
            n = len(x)
            A = 10
            return A * n + np.sum(x ** 2 - A * np.cos(2 * np.pi * x))

        result = sa.optimize(
            rastrigin,
            dimension=2,
            bounds=[(-5.12, 5.12), (-5.12, 5.12)],
            step_size=0.5,
        )

        assert result["best_energy"] >= 0
        assert len(result["history"]) == result["iterations"]

    def test_optimize_without_bounds(self):
        """Test optimization without bounds."""
        sa = SimulatedAnnealing()

        def objective(x):
            return np.sum(x ** 2)

        result = sa.optimize(
            objective,
            dimension=3,
            step_size=1.0,
        )

        assert len(result["best_solution"]) == 3

    def test_optimize_improves_solution(self):
        """Test that optimization improves solution over iterations."""
        sa = SimulatedAnnealing()

        def objective(x):
            return np.sum(x ** 2)

        initial = np.array([10.0, 10.0])
        initial_energy = objective(initial)

        result = sa.optimize(
            objective,
            initial_solution=initial,
            bounds=[(-10, 10), (-10, 10)],
            step_size=1.0,
        )

        assert result["best_energy"] <= initial_energy

    def test_invalid_bounds_length(self):
        """Test that mismatched bounds length raises error."""
        sa = SimulatedAnnealing()

        def objective(x):
            return np.sum(x ** 2)

        with pytest.raises(ValueError, match="Bounds length"):
            sa.optimize(
                objective,
                dimension=2,
                bounds=[(-10, 10)],
                step_size=1.0,
            )

    def test_config_file_not_found(self):
        """Test that missing config file raises error."""
        with pytest.raises(FileNotFoundError):
            SimulatedAnnealing(config_path="nonexistent.yaml")

    def test_history_tracking(self):
        """Test that iteration history is properly tracked."""
        sa = SimulatedAnnealing()

        def objective(x):
            return np.sum(x ** 2)

        result = sa.optimize(
            objective,
            dimension=2,
            bounds=[(-10, 10), (-10, 10)],
            step_size=1.0,
        )

        assert len(result["history"]) == result["iterations"]
        for iteration, energy, temperature in result["history"]:
            assert isinstance(iteration, int)
            assert isinstance(energy, (int, float))
            assert isinstance(temperature, (int, float))
            assert temperature > 0

    def test_different_schedule_types(self):
        """Test optimization with different schedule types."""
        schedule_types = ["exponential", "linear", "logarithmic", "geometric"]

        for schedule_type in schedule_types:
            config = {
                "simulated_annealing": {
                    "initial_temperature": 100.0,
                    "final_temperature": 0.01,
                    "max_iterations": 100,
                    "schedule_type": schedule_type,
                    "acceptance_criterion": "metropolis",
                },
                "logging": {"level": "WARNING", "file": "logs/test.log"},
            }

            config_path = self.create_temp_config(config)
            try:
                sa = SimulatedAnnealing(config_path=config_path)

                def objective(x):
                    return np.sum(x ** 2)

                result = sa.optimize(
                    objective,
                    dimension=2,
                    bounds=[(-10, 10), (-10, 10)],
                    step_size=1.0,
                )

                assert result["best_energy"] >= 0
            finally:
                Path(config_path).unlink()

    def test_random_seed_reproducibility(self):
        """Test that random seed produces reproducible results."""
        config = {
            "simulated_annealing": {
                "initial_temperature": 100.0,
                "final_temperature": 0.01,
                "max_iterations": 50,
                "schedule_type": "exponential",
                "acceptance_criterion": "metropolis",
                "random_seed": 42,
            },
            "logging": {"level": "WARNING", "file": "logs/test.log"},
        }

        config_path = self.create_temp_config(config)
        try:
            sa1 = SimulatedAnnealing(config_path=config_path)

            def objective(x):
                return np.sum(x ** 2)

            result1 = sa1.optimize(
                objective,
                dimension=2,
                bounds=[(-10, 10), (-10, 10)],
                step_size=1.0,
            )

            sa2 = SimulatedAnnealing(config_path=config_path)
            result2 = sa2.optimize(
                objective,
                dimension=2,
                bounds=[(-10, 10), (-10, 10)],
                step_size=1.0,
            )

            np.testing.assert_array_almost_equal(
                result1["best_solution"], result2["best_solution"], decimal=5
            )
        finally:
            Path(config_path).unlink()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
