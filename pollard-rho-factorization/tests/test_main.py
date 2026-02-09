"""Test suite for Pollard's rho factorization implementation."""

import pytest

from src.main import PollardRho


class TestPollardRho:
    """Test cases for PollardRho class."""

    def test_initialization(self) -> None:
        """Test PollardRho initialization."""
        pr = PollardRho()
        assert pr is not None

    def test_gcd(self) -> None:
        """Test GCD computation."""
        pr = PollardRho()
        assert pr._gcd(48, 18) == 6
        assert pr._gcd(17, 13) == 1
        assert pr._gcd(100, 25) == 25
        assert pr._gcd(0, 5) == 5
        assert pr._gcd(5, 0) == 5

    def test_polynomial(self) -> None:
        """Test polynomial function."""
        pr = PollardRho()
        assert pr._polynomial(2, 1, 7) == 5
        assert pr._polynomial(3, 1, 7) == 3
        assert pr._polynomial(0, 1, 7) == 1

    def test_find_factor_small_composite(self) -> None:
        """Test finding factor of small composite number."""
        pr = PollardRho()
        factor = pr.find_factor(100)
        assert factor is not None
        assert 100 % factor == 0
        assert factor > 1
        assert factor < 100

    def test_find_factor_prime(self) -> None:
        """Test finding factor of prime number."""
        pr = PollardRho()
        factor = pr.find_factor(97)
        assert factor is None

    def test_find_factor_invalid_input(self) -> None:
        """Test find_factor with invalid input."""
        pr = PollardRho()
        with pytest.raises(ValueError, match="n must be >= 2"):
            pr.find_factor(1)
        with pytest.raises(ValueError, match="n must be >= 2"):
            pr.find_factor(0)

    def test_factorize_small_number(self) -> None:
        """Test factorization of small number."""
        pr = PollardRho()
        factors = pr.factorize(12)
        assert factors == {2: 2, 3: 1}
        assert 2 ** 2 * 3 ** 1 == 12

    def test_factorize_square(self) -> None:
        """Test factorization of perfect square."""
        pr = PollardRho()
        factors = pr.factorize(100)
        assert factors == {2: 2, 5: 2}
        assert 2 ** 2 * 5 ** 2 == 100

    def test_factorize_prime(self) -> None:
        """Test factorization of prime number."""
        pr = PollardRho()
        factors = pr.factorize(97)
        assert factors == {97: 1}

    def test_factorize_power_of_prime(self) -> None:
        """Test factorization of power of prime."""
        pr = PollardRho()
        factors = pr.factorize(16)
        assert factors == {2: 4}
        assert 2 ** 4 == 16

    def test_factorize_invalid_input(self) -> None:
        """Test factorize with invalid input."""
        pr = PollardRho()
        with pytest.raises(ValueError, match="n must be >= 2"):
            pr.factorize(1)
        with pytest.raises(ValueError, match="n must be >= 2"):
            pr.factorize(0)

    def test_factorize_list(self) -> None:
        """Test factorization into list."""
        pr = PollardRho()
        factors_list = pr.factorize_list(12)
        assert sorted(factors_list) == [2, 2, 3]
        assert factors_list[0] * factors_list[1] * factors_list[2] == 12

    def test_factorize_list_prime(self) -> None:
        """Test factorization list for prime."""
        pr = PollardRho()
        factors_list = pr.factorize_list(97)
        assert factors_list == [97]

    def test_get_all_factors(self) -> None:
        """Test getting all divisors."""
        pr = PollardRho()
        divisors = pr.get_all_factors(12)
        expected = [1, 2, 3, 4, 6, 12]
        assert divisors == expected

    def test_get_all_factors_square(self) -> None:
        """Test getting all divisors of perfect square."""
        pr = PollardRho()
        divisors = pr.get_all_factors(100)
        expected = [1, 2, 4, 5, 10, 20, 25, 50, 100]
        assert divisors == expected

    def test_get_all_factors_prime(self) -> None:
        """Test getting all divisors of prime."""
        pr = PollardRho()
        divisors = pr.get_all_factors(97)
        assert divisors == [1, 97]

    def test_get_all_factors_one(self) -> None:
        """Test getting all divisors of 1."""
        pr = PollardRho()
        divisors = pr.get_all_factors(1)
        assert divisors == [1]

    def test_get_all_factors_invalid_input(self) -> None:
        """Test get_all_factors with invalid input."""
        pr = PollardRho()
        with pytest.raises(ValueError, match="n must be >= 1"):
            pr.get_all_factors(0)

    def test_is_prime_true(self) -> None:
        """Test is_prime for prime numbers."""
        pr = PollardRho()
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 97]
        for p in primes:
            assert pr.is_prime(p) is True, f"{p} should be prime"

    def test_is_prime_false(self) -> None:
        """Test is_prime for composite numbers."""
        pr = PollardRho()
        composites = [4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 22, 24, 25, 100]
        for c in composites:
            assert pr.is_prime(c) is False, f"{c} should be composite"

    def test_is_prime_invalid_input(self) -> None:
        """Test is_prime with invalid input."""
        pr = PollardRho()
        with pytest.raises(ValueError, match="n must be >= 2"):
            pr.is_prime(1)
        with pytest.raises(ValueError, match="n must be >= 2"):
            pr.is_prime(0)

    def test_prime_factors(self) -> None:
        """Test getting distinct prime factors."""
        pr = PollardRho()
        prime_factors = pr.prime_factors(12)
        assert sorted(prime_factors) == [2, 3]

    def test_prime_factors_square(self) -> None:
        """Test prime factors of perfect square."""
        pr = PollardRho()
        prime_factors = pr.prime_factors(100)
        assert sorted(prime_factors) == [2, 5]

    def test_prime_factors_prime(self) -> None:
        """Test prime factors of prime number."""
        pr = PollardRho()
        prime_factors = pr.prime_factors(97)
        assert prime_factors == [97]

    def test_factorization_string(self) -> None:
        """Test factorization string representation."""
        pr = PollardRho()
        fact_str = pr.factorization_string(12)
        assert "2" in fact_str
        assert "3" in fact_str

    def test_factorization_string_square(self) -> None:
        """Test factorization string for perfect square."""
        pr = PollardRho()
        fact_str = pr.factorization_string(100)
        assert "2^2" in fact_str
        assert "5^2" in fact_str

    def test_factorization_string_prime(self) -> None:
        """Test factorization string for prime."""
        pr = PollardRho()
        fact_str = pr.factorization_string(97)
        assert fact_str == "97"

    def test_factorization_consistency(self) -> None:
        """Test that factorization is consistent."""
        pr = PollardRho()
        test_numbers = [12, 18, 24, 36, 48, 60, 72, 84, 96, 100]

        for n in test_numbers:
            factors_dict = pr.factorize(n)
            product = 1
            for factor, multiplicity in factors_dict.items():
                product *= factor ** multiplicity
            assert product == n, f"Factorization of {n} is incorrect"

    def test_larger_composite(self) -> None:
        """Test factorization of larger composite number."""
        pr = PollardRho()
        n = 1001
        factors = pr.factorize(n)
        product = 1
        for factor, multiplicity in factors.items():
            product *= factor ** multiplicity
        assert product == n

    def test_pollard_rho_single(self) -> None:
        """Test single Pollard rho iteration."""
        pr = PollardRho()
        factor = pr._pollard_rho_single(100, c=1)
        assert factor is not None
        assert 100 % factor == 0

    def test_is_prime_simple(self) -> None:
        """Test simple primality test."""
        pr = PollardRho()
        assert pr._is_prime_simple(2) is True
        assert pr._is_prime_simple(3) is True
        assert pr._is_prime_simple(4) is False
        assert pr._is_prime_simple(97) is True
        assert pr._is_prime_simple(100) is False

    def test_factorize_product_verification(self) -> None:
        """Test that factorized product equals original number."""
        pr = PollardRho()
        test_cases = [50, 75, 90, 120, 150, 200, 250, 300]

        for n in test_cases:
            factors_dict = pr.factorize(n)
            product = 1
            for factor, multiplicity in factors_dict.items():
                product *= factor ** multiplicity
            assert product == n, f"Product mismatch for {n}"

    def test_all_factors_completeness(self) -> None:
        """Test that all factors are divisors."""
        pr = PollardRho()
        n = 100
        divisors = pr.get_all_factors(n)

        for d in divisors:
            assert n % d == 0, f"{d} should divide {n}"

        assert len(divisors) > 0
        assert 1 in divisors
        assert n in divisors
