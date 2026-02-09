"""Test suite for Miller-Rabin primality test implementation."""

import pytest

from src.main import MillerRabin


class TestMillerRabin:
    """Test cases for MillerRabin class."""

    def test_initialization(self) -> None:
        """Test MillerRabin initialization."""
        mr = MillerRabin()
        assert mr is not None

    def test_mod_power(self) -> None:
        """Test modular exponentiation."""
        mr = MillerRabin()
        assert mr._mod_power(2, 3, 7) == 1
        assert mr._mod_power(3, 4, 7) == 4
        assert mr._mod_power(5, 0, 7) == 1
        assert mr._mod_power(2, 10, 1000) == 24

    def test_decompose(self) -> None:
        """Test decomposition of n-1."""
        mr = MillerRabin()
        d, r = mr._decompose(7)
        assert d == 3
        assert r == 1
        assert d * (2 ** r) == 6

        d, r = mr._decompose(9)
        assert d == 1
        assert r == 3
        assert d * (2 ** r) == 8

    def test_is_prime_deterministic_small_primes(self) -> None:
        """Test deterministic test with small primes."""
        mr = MillerRabin()
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
        for p in primes:
            assert mr.is_prime_deterministic(p) is True, f"{p} should be prime"

    def test_is_prime_deterministic_small_composites(self) -> None:
        """Test deterministic test with small composites."""
        mr = MillerRabin()
        composites = [4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 22, 24, 25]
        for c in composites:
            assert mr.is_prime_deterministic(c) is False, f"{c} should be composite"

    def test_is_prime_deterministic_large_primes(self) -> None:
        """Test deterministic test with larger primes."""
        mr = MillerRabin()
        large_primes = [97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149]
        for p in large_primes:
            assert mr.is_prime_deterministic(p) is True, f"{p} should be prime"

    def test_is_prime_deterministic_large_composites(self) -> None:
        """Test deterministic test with larger composites."""
        mr = MillerRabin()
        large_composites = [100, 102, 104, 105, 106, 108, 110, 111, 112, 114]
        for c in large_composites:
            assert mr.is_prime_deterministic(c) is False, f"{c} should be composite"

    def test_is_prime_deterministic_edge_cases(self) -> None:
        """Test deterministic test with edge cases."""
        mr = MillerRabin()
        assert mr.is_prime_deterministic(2) is True
        assert mr.is_prime_deterministic(3) is True

    def test_is_prime_deterministic_invalid_input(self) -> None:
        """Test deterministic test with invalid input."""
        mr = MillerRabin()
        with pytest.raises(ValueError, match="n must be >= 2"):
            mr.is_prime_deterministic(1)
        with pytest.raises(ValueError, match="n must be >= 2"):
            mr.is_prime_deterministic(0)
        with pytest.raises(ValueError, match="n must be >= 2"):
            mr.is_prime_deterministic(-1)

    def test_is_prime_probabilistic_small_primes(self) -> None:
        """Test probabilistic test with small primes."""
        mr = MillerRabin()
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
        for p in primes:
            assert mr.is_prime_probabilistic(p, k=5) is True, f"{p} should be prime"

    def test_is_prime_probabilistic_small_composites(self) -> None:
        """Test probabilistic test with small composites."""
        mr = MillerRabin()
        composites = [4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 22, 24, 25]
        for c in composites:
            assert mr.is_prime_probabilistic(c, k=5) is False, f"{c} should be composite"

    def test_is_prime_probabilistic_invalid_input(self) -> None:
        """Test probabilistic test with invalid input."""
        mr = MillerRabin()
        with pytest.raises(ValueError, match="n must be >= 2"):
            mr.is_prime_probabilistic(1)
        with pytest.raises(ValueError, match="k must be >= 1"):
            mr.is_prime_probabilistic(5, k=0)

    def test_find_next_prime(self) -> None:
        """Test finding next prime."""
        mr = MillerRabin()
        assert mr.find_next_prime(2) == 3
        assert mr.find_next_prime(3) == 5
        assert mr.find_next_prime(4) == 5
        assert mr.find_next_prime(10) == 11
        assert mr.find_next_prime(97) == 101

    def test_find_next_prime_deterministic(self) -> None:
        """Test finding next prime with deterministic test."""
        mr = MillerRabin()
        assert mr.find_next_prime(2, deterministic=True) == 3
        assert mr.find_next_prime(10, deterministic=True) == 11

    def test_find_next_prime_invalid_input(self) -> None:
        """Test find_next_prime with invalid input."""
        mr = MillerRabin()
        with pytest.raises(ValueError, match="n must be >= 1"):
            mr.find_next_prime(0)

    def test_find_previous_prime(self) -> None:
        """Test finding previous prime."""
        mr = MillerRabin()
        assert mr.find_previous_prime(3) == 2
        assert mr.find_previous_prime(5) == 3
        assert mr.find_previous_prime(10) == 7
        assert mr.find_previous_prime(101) == 97

    def test_find_previous_prime_deterministic(self) -> None:
        """Test finding previous prime with deterministic test."""
        mr = MillerRabin()
        assert mr.find_previous_prime(5, deterministic=True) == 3
        assert mr.find_previous_prime(10, deterministic=True) == 7

    def test_find_previous_prime_invalid_input(self) -> None:
        """Test find_previous_prime with invalid input."""
        mr = MillerRabin()
        with pytest.raises(ValueError, match="n must be >= 3"):
            mr.find_previous_prime(2)

    def test_generate_prime(self) -> None:
        """Test generating random prime."""
        mr = MillerRabin()
        prime = mr.generate_prime(8)
        assert prime >= 128
        assert prime < 256
        assert mr.is_prime_probabilistic(prime, k=10) is True

    def test_generate_prime_deterministic(self) -> None:
        """Test generating random prime with deterministic test."""
        mr = MillerRabin()
        prime = mr.generate_prime(8, deterministic=True)
        assert prime >= 128
        assert prime < 256
        assert mr.is_prime_deterministic(prime) is True

    def test_generate_prime_invalid_input(self) -> None:
        """Test generate_prime with invalid input."""
        mr = MillerRabin()
        with pytest.raises(ValueError, match="bits must be >= 2"):
            mr.generate_prime(1)

    def test_count_primes_in_range(self) -> None:
        """Test counting primes in range."""
        mr = MillerRabin()
        count = mr.count_primes_in_range(2, 10)
        expected_primes = [2, 3, 5, 7]
        assert count == len(expected_primes)

        count = mr.count_primes_in_range(10, 20)
        expected_primes = [11, 13, 17, 19]
        assert count == len(expected_primes)

    def test_count_primes_in_range_deterministic(self) -> None:
        """Test counting primes in range with deterministic test."""
        mr = MillerRabin()
        count = mr.count_primes_in_range(2, 10, deterministic=True)
        expected_primes = [2, 3, 5, 7]
        assert count == len(expected_primes)

    def test_count_primes_in_range_invalid_input(self) -> None:
        """Test count_primes_in_range with invalid input."""
        mr = MillerRabin()
        with pytest.raises(ValueError, match="start must be <= end"):
            mr.count_primes_in_range(10, 5)
        with pytest.raises(ValueError, match="start must be >= 2"):
            mr.count_primes_in_range(1, 10)

    def test_deterministic_bases_coverage(self) -> None:
        """Test that deterministic bases cover expected ranges."""
        mr = MillerRabin()
        test_cases = [
            (2, True),
            (3, True),
            (4, False),
            (97, True),
            (100, False),
            (101, True),
            (1000, False),
            (1009, True),
        ]

        for n, expected in test_cases:
            result = mr.is_prime_deterministic(n)
            assert result == expected, f"n={n}, expected={expected}, got={result}"

    def test_large_prime_deterministic(self) -> None:
        """Test deterministic test with larger known primes."""
        mr = MillerRabin()
        large_primes = [
            1009,
            1013,
            1019,
            1021,
            1031,
            1033,
            1039,
            1049,
            1051,
            1061,
        ]
        for p in large_primes:
            assert mr.is_prime_deterministic(p) is True, f"{p} should be prime"

    def test_carmichael_numbers(self) -> None:
        """Test that Carmichael numbers are correctly identified as composite."""
        mr = MillerRabin()
        carmichael_numbers = [561, 1105, 1729, 2465, 2821]
        for c in carmichael_numbers:
            assert mr.is_prime_deterministic(c) is False, f"{c} should be composite"

    def test_witness_function(self) -> None:
        """Test witness function."""
        mr = MillerRabin()
        d, r = mr._decompose(9)
        assert mr._witness(2, d, r, 9) is True

    def test_get_deterministic_bases(self) -> None:
        """Test getting deterministic bases."""
        mr = MillerRabin()
        bases = mr._get_deterministic_bases(100)
        assert bases == [2]

        bases = mr._get_deterministic_bases(10000)
        assert bases == [2, 3, 5]

    def test_very_large_number_probabilistic(self) -> None:
        """Test probabilistic test with very large number."""
        mr = MillerRabin()
        large_prime = 982451653
        result = mr.is_prime_probabilistic(large_prime, k=20)
        assert result is True

    def test_range_consistency(self) -> None:
        """Test that deterministic and probabilistic give same results for small numbers."""
        mr = MillerRabin()
        for n in range(2, 100):
            det_result = mr.is_prime_deterministic(n)
            prob_result = mr.is_prime_probabilistic(n, k=10)
            assert det_result == prob_result, f"n={n}, det={det_result}, prob={prob_result}"
