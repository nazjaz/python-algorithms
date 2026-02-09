"""Unit tests for prime checker module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import PrimeChecker


class TestPrimeChecker:
    """Test cases for PrimeChecker class."""

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
    def checker(self, config_file):
        """Create PrimeChecker instance."""
        return PrimeChecker(config_path=config_file)

    def test_load_config_success(self, temp_dir):
        """Test successful configuration loading."""
        config = {"logging": {"level": "INFO"}}
        config_path = temp_dir / "config.yaml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)

        checker = PrimeChecker(config_path=str(config_path))
        assert checker.config["logging"]["level"] == "INFO"

    def test_load_config_file_not_found(self):
        """Test FileNotFoundError when config file doesn't exist."""
        with pytest.raises(FileNotFoundError):
            PrimeChecker(config_path="nonexistent.yaml")

    def test_is_prime_zero(self, checker):
        """Test that 0 is not prime."""
        assert checker.is_prime(0) is False

    def test_is_prime_one(self, checker):
        """Test that 1 is not prime."""
        assert checker.is_prime(1) is False

    def test_is_prime_two(self, checker):
        """Test that 2 is prime."""
        assert checker.is_prime(2) is True

    def test_is_prime_small_prime(self, checker):
        """Test small prime numbers."""
        assert checker.is_prime(3) is True
        assert checker.is_prime(5) is True
        assert checker.is_prime(7) is True
        assert checker.is_prime(11) is True

    def test_is_prime_small_composite(self, checker):
        """Test small composite numbers."""
        assert checker.is_prime(4) is False
        assert checker.is_prime(6) is False
        assert checker.is_prime(8) is False
        assert checker.is_prime(9) is False
        assert checker.is_prime(10) is False

    def test_is_prime_even_number(self, checker):
        """Test that even numbers (except 2) are not prime."""
        assert checker.is_prime(4) is False
        assert checker.is_prime(6) is False
        assert checker.is_prime(100) is False

    def test_is_prime_larger_prime(self, checker):
        """Test larger prime numbers."""
        assert checker.is_prime(17) is True
        assert checker.is_prime(29) is True
        assert checker.is_prime(97) is True

    def test_is_prime_larger_composite(self, checker):
        """Test larger composite numbers."""
        assert checker.is_prime(100) is False
        assert checker.is_prime(121) is False
        assert checker.is_prime(169) is False

    def test_is_prime_negative(self, checker):
        """Test that negative numbers are not prime."""
        assert checker.is_prime(-1) is False
        assert checker.is_prime(-5) is False

    def test_division_counting(self, checker):
        """Test that divisions are counted correctly."""
        checker.is_prime(17)
        assert checker.divisions > 0

    def test_find_primes_in_range(self, checker):
        """Test finding primes in a range."""
        primes = checker.find_primes_in_range(1, 20)
        expected = [2, 3, 5, 7, 11, 13, 17, 19]
        assert primes == expected

    def test_find_primes_in_range_small(self, checker):
        """Test finding primes in small range."""
        primes = checker.find_primes_in_range(1, 10)
        expected = [2, 3, 5, 7]
        assert primes == expected

    def test_find_primes_in_range_single(self, checker):
        """Test finding primes in range with single prime."""
        primes = checker.find_primes_in_range(13, 13)
        assert primes == [13]

    def test_find_primes_in_range_no_primes(self, checker):
        """Test finding primes in range with no primes."""
        primes = checker.find_primes_in_range(14, 16)
        assert primes == []

    def test_get_analysis(self, checker):
        """Test getting analysis data."""
        checker.is_prime(17)
        analysis = checker.get_analysis()

        assert "number" in analysis
        assert "is_prime" in analysis
        assert "divisions_performed" in analysis
        assert "square_root" in analysis

    def test_generate_report(self, checker, temp_dir):
        """Test report generation."""
        checker.is_prime(17)
        report_path = temp_dir / "report.txt"
        report = checker.generate_report(output_path=str(report_path))

        assert report_path.exists()
        assert "PRIME CHECKER ALGORITHM ANALYSIS REPORT" in report
        assert "Is Prime" in report
        assert "Total divisions" in report

    def test_generate_report_no_data(self, checker):
        """Test report generation without analysis data."""
        report = checker.generate_report()
        assert "No analysis data available" in report
