"""Unit tests for GCD calculator module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import GCDCalculator


class TestGCDCalculator:
    """Test cases for GCDCalculator class."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for testing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.fixture
    def config_file(self, temp_dir):
        """Create temporary config file."""
        config = {
            "logging": {"level": "INFO", "file": str(temp_dir / "app.log")},
        }
        config_path = temp_dir / "config.yaml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)
        return str(config_path)

    @pytest.fixture
    def calculator(self, config_file):
        """Create GCDCalculator instance."""
        return GCDCalculator(config_path=config_file)

    def test_load_config_success(self, temp_dir):
        """Test successful configuration loading."""
        config = {
            "logging": {"level": "DEBUG"},
        }
        config_path = temp_dir / "config.yaml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)

        calculator = GCDCalculator(config_path=str(config_path))
        assert calculator.config["logging"]["level"] == "DEBUG"

    def test_load_config_file_not_found(self):
        """Test FileNotFoundError when config file doesn't exist."""
        with pytest.raises(FileNotFoundError):
            GCDCalculator(config_path="nonexistent.yaml")

    def test_gcd_simple(self, calculator):
        """Test GCD calculation with simple numbers."""
        assert calculator.gcd(48, 18) == 6
        assert calculator.gcd(18, 48) == 6

    def test_gcd_coprime(self, calculator):
        """Test GCD of coprime numbers."""
        assert calculator.gcd(17, 13) == 1
        assert calculator.gcd(7, 5) == 1

    def test_gcd_one_is_zero(self, calculator):
        """Test GCD when one number is zero."""
        assert calculator.gcd(0, 5) == 5
        assert calculator.gcd(5, 0) == 5

    def test_gcd_both_zero(self, calculator):
        """Test GCD when both numbers are zero."""
        with pytest.raises(ValueError, match="undefined"):
            calculator.gcd(0, 0)

    def test_gcd_negative_numbers(self, calculator):
        """Test GCD with negative numbers."""
        assert calculator.gcd(-48, 18) == 6
        assert calculator.gcd(48, -18) == 6
        assert calculator.gcd(-48, -18) == 6

    def test_gcd_same_number(self, calculator):
        """Test GCD when both numbers are the same."""
        assert calculator.gcd(10, 10) == 10
        assert calculator.gcd(1, 1) == 1

    def test_gcd_large_numbers(self, calculator):
        """Test GCD with large numbers."""
        assert calculator.gcd(1000000, 1000001) == 1
        assert calculator.gcd(100, 25) == 25

    def test_extended_gcd_simple(self, calculator):
        """Test Extended Euclidean algorithm with simple numbers."""
        gcd, x, y = calculator.extended_gcd(48, 18)
        assert gcd == 6
        assert 48 * x + 18 * y == 6

    def test_extended_gcd_coprime(self, calculator):
        """Test Extended Euclidean algorithm with coprime numbers."""
        gcd, x, y = calculator.extended_gcd(17, 13)
        assert gcd == 1
        assert 17 * x + 13 * y == 1

    def test_extended_gcd_verification(self, calculator):
        """Test that extended GCD satisfies linear combination."""
        test_cases = [
            (48, 18),
            (17, 13),
            (100, 25),
            (56, 42),
            (17, 5),
        ]

        for a, b in test_cases:
            gcd, x, y = calculator.extended_gcd(a, b)
            assert a * x + b * y == gcd

    def test_extended_gcd_negative_numbers(self, calculator):
        """Test Extended Euclidean algorithm with negative numbers."""
        gcd, x, y = calculator.extended_gcd(-48, 18)
        assert gcd == 6
        assert -48 * x + 18 * y == 6

    def test_extended_gcd_both_zero(self, calculator):
        """Test Extended Euclidean algorithm when both numbers are zero."""
        with pytest.raises(ValueError, match="undefined"):
            calculator.extended_gcd(0, 0)

    def test_extended_gcd_one_zero(self, calculator):
        """Test Extended Euclidean algorithm when one number is zero."""
        gcd, x, y = calculator.extended_gcd(5, 0)
        assert gcd == 5
        assert 5 * x + 0 * y == 5

    def test_gcd_multiple_two_numbers(self, calculator):
        """Test GCD of multiple numbers with two numbers."""
        assert calculator.gcd_multiple([48, 18]) == 6

    def test_gcd_multiple_three_numbers(self, calculator):
        """Test GCD of multiple numbers with three numbers."""
        assert calculator.gcd_multiple([48, 18, 12]) == 6
        assert calculator.gcd_multiple([12, 18, 24]) == 6

    def test_gcd_multiple_many_numbers(self, calculator):
        """Test GCD of multiple numbers with many numbers."""
        assert calculator.gcd_multiple([12, 18, 24, 30, 36]) == 6

    def test_gcd_multiple_empty_list(self, calculator):
        """Test GCD of multiple numbers with empty list."""
        with pytest.raises(ValueError, match="empty"):
            calculator.gcd_multiple([])

    def test_gcd_multiple_all_zero(self, calculator):
        """Test GCD of multiple numbers when all are zero."""
        with pytest.raises(ValueError, match="all numbers are zero"):
            calculator.gcd_multiple([0, 0, 0])

    def test_gcd_multiple_with_zeros(self, calculator):
        """Test GCD of multiple numbers with some zeros."""
        assert calculator.gcd_multiple([48, 18, 0]) == 6

    def test_lcm_simple(self, calculator):
        """Test LCM calculation with simple numbers."""
        assert calculator.lcm(4, 6) == 12
        assert calculator.lcm(5, 7) == 35

    def test_lcm_verification(self, calculator):
        """Test that LCM * GCD = a * b."""
        test_cases = [
            (48, 18),
            (17, 13),
            (100, 25),
            (56, 42),
        ]

        for a, b in test_cases:
            lcm_result = calculator.lcm(a, b)
            gcd_result = calculator.gcd(a, b)
            assert lcm_result * gcd_result == abs(a * b)

    def test_lcm_same_number(self, calculator):
        """Test LCM when both numbers are the same."""
        assert calculator.lcm(10, 10) == 10

    def test_lcm_both_zero(self, calculator):
        """Test LCM when both numbers are zero."""
        with pytest.raises(ValueError, match="undefined"):
            calculator.lcm(0, 0)

    def test_modular_inverse_exists(self, calculator):
        """Test modular inverse when it exists."""
        inverse = calculator.modular_inverse(3, 11)
        assert inverse == 4
        assert (3 * inverse) % 11 == 1

    def test_modular_inverse_does_not_exist(self, calculator):
        """Test modular inverse when it doesn't exist."""
        inverse = calculator.modular_inverse(2, 4)
        assert inverse is None

    def test_modular_inverse_coprime(self, calculator):
        """Test modular inverse with coprime numbers."""
        inverse = calculator.modular_inverse(17, 13)
        assert inverse is not None
        assert (17 * inverse) % 13 == 1

    def test_modular_inverse_negative_modulus(self, calculator):
        """Test modular inverse with negative modulus."""
        with pytest.raises(ValueError, match="positive"):
            calculator.modular_inverse(3, -11)

    def test_modular_inverse_zero_modulus(self, calculator):
        """Test modular inverse with zero modulus."""
        with pytest.raises(ValueError, match="positive"):
            calculator.modular_inverse(3, 0)

    def test_verify_linear_combination_correct(self, calculator):
        """Test verification of correct linear combination."""
        assert calculator.verify_linear_combination(48, 18, 6, 1, -2) is True

    def test_verify_linear_combination_incorrect(self, calculator):
        """Test verification of incorrect linear combination."""
        assert calculator.verify_linear_combination(48, 18, 6, 1, 1) is False

    def test_calculate_with_details_basic(self, calculator):
        """Test detailed calculation without extended algorithm."""
        result = calculator.calculate_with_details(48, 18, use_extended=False)
        assert result["a"] == 48
        assert result["b"] == 18
        assert result["gcd"] == 6
        assert result["lcm"] == 144
        assert "extended_gcd" not in result

    def test_calculate_with_details_extended(self, calculator):
        """Test detailed calculation with extended algorithm."""
        result = calculator.calculate_with_details(48, 18, use_extended=True)
        assert result["gcd"] == 6
        assert "extended_gcd" in result
        assert result["extended_gcd"]["gcd"] == 6
        assert result["extended_gcd"]["verified"] is True

    def test_generate_report(self, calculator, temp_dir):
        """Test report generation."""
        result = calculator.calculate_with_details(48, 18, use_extended=True)
        report_path = temp_dir / "report.txt"
        report = calculator.generate_report(
            48, 18, result, output_path=str(report_path)
        )

        assert report_path.exists()
        assert "GCD CALCULATION REPORT" in report
        assert "EUCLIDEAN ALGORITHM" in report
        assert "48" in report
        assert "18" in report

    def test_generate_report_extended(self, calculator):
        """Test report generation with extended algorithm."""
        result = calculator.calculate_with_details(48, 18, use_extended=True)
        report = calculator.generate_report(48, 18, result)

        assert "EXTENDED EUCLIDEAN ALGORITHM" in report
        assert "Linear combination" in report

    def test_euclidean_algorithm_property(self, calculator):
        """Test that Euclidean algorithm satisfies gcd(a, b) = gcd(b, a mod b)."""
        test_cases = [
            (48, 18),
            (17, 13),
            (100, 25),
            (56, 42),
        ]

        for a, b in test_cases:
            gcd_ab = calculator.gcd(a, b)
            gcd_ba = calculator.gcd(b, a % b)
            assert gcd_ab == gcd_ba

    def test_extended_gcd_symmetry(self, calculator):
        """Test that extended GCD handles order correctly."""
        gcd1, x1, y1 = calculator.extended_gcd(48, 18)
        gcd2, x2, y2 = calculator.extended_gcd(18, 48)

        assert gcd1 == gcd2
        # Note: coefficients may differ due to different order
        assert 48 * x1 + 18 * y1 == gcd1
        assert 18 * x2 + 48 * y2 == gcd2

    def test_gcd_edge_cases(self, calculator):
        """Test GCD with edge cases."""
        assert calculator.gcd(1, 1) == 1
        assert calculator.gcd(1, 100) == 1
        assert calculator.gcd(100, 1) == 1
        assert calculator.gcd(0, 1) == 1
        assert calculator.gcd(1, 0) == 1

    def test_extended_gcd_edge_cases(self, calculator):
        """Test Extended GCD with edge cases."""
        gcd, x, y = calculator.extended_gcd(1, 1)
        assert gcd == 1
        assert 1 * x + 1 * y == 1

        gcd, x, y = calculator.extended_gcd(1, 0)
        assert gcd == 1
        assert 1 * x + 0 * y == 1
