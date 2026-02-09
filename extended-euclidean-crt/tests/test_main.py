"""Test suite for Extended Euclidean Algorithm and CRT implementation."""

import pytest

from src.main import ExtendedEuclidean


class TestExtendedEuclidean:
    """Test cases for ExtendedEuclidean class."""

    def test_initialization(self) -> None:
        """Test ExtendedEuclidean initialization."""
        ee = ExtendedEuclidean()
        assert ee is not None

    def test_extended_gcd_simple(self) -> None:
        """Test extended GCD with simple case."""
        ee = ExtendedEuclidean()
        gcd, x, y = ee.extended_gcd(48, 18)
        assert gcd == 6
        assert 48 * x + 18 * y == 6

    def test_extended_gcd_coprime(self) -> None:
        """Test extended GCD with coprime numbers."""
        ee = ExtendedEuclidean()
        gcd, x, y = ee.extended_gcd(17, 13)
        assert gcd == 1
        assert 17 * x + 13 * y == 1

    def test_extended_gcd_zero(self) -> None:
        """Test extended GCD with zero."""
        ee = ExtendedEuclidean()
        gcd, x, y = ee.extended_gcd(0, 5)
        assert gcd == 5
        assert x == 0
        assert y == 1

        gcd, x, y = ee.extended_gcd(5, 0)
        assert gcd == 5

    def test_extended_gcd_negative(self) -> None:
        """Test extended GCD with negative numbers."""
        ee = ExtendedEuclidean()
        gcd, x, y = ee.extended_gcd(-48, 18)
        assert gcd == 6
        assert abs(-48) * x + 18 * y == 6 or -48 * x + 18 * y == 6

    def test_gcd_simple(self) -> None:
        """Test GCD computation."""
        ee = ExtendedEuclidean()
        assert ee.gcd(48, 18) == 6
        assert ee.gcd(17, 13) == 1
        assert ee.gcd(100, 25) == 25

    def test_gcd_zero(self) -> None:
        """Test GCD with zero."""
        ee = ExtendedEuclidean()
        assert ee.gcd(0, 5) == 5
        assert ee.gcd(5, 0) == 5

    def test_modular_inverse_simple(self) -> None:
        """Test modular inverse computation."""
        ee = ExtendedEuclidean()
        inv = ee.modular_inverse(3, 7)
        assert inv == 5
        assert (3 * inv) % 7 == 1

    def test_modular_inverse_coprime(self) -> None:
        """Test modular inverse with coprime numbers."""
        ee = ExtendedEuclidean()
        inv = ee.modular_inverse(5, 11)
        assert (5 * inv) % 11 == 1

    def test_modular_inverse_nonexistent(self) -> None:
        """Test modular inverse when it doesn't exist."""
        ee = ExtendedEuclidean()
        inv = ee.modular_inverse(4, 8)
        assert inv is None

    def test_modular_inverse_invalid_modulus(self) -> None:
        """Test modular inverse with invalid modulus."""
        ee = ExtendedEuclidean()
        with pytest.raises(ValueError, match="Modulus must be positive"):
            ee.modular_inverse(3, 0)
        with pytest.raises(ValueError, match="Modulus must be positive"):
            ee.modular_inverse(3, -5)

    def test_modular_inverse_negative_a(self) -> None:
        """Test modular inverse with negative a."""
        ee = ExtendedEuclidean()
        inv = ee.modular_inverse(-3, 7)
        assert (-3 * inv) % 7 == 1 or (4 * inv) % 7 == 1

    def test_solve_congruence_simple(self) -> None:
        """Test solving simple congruence."""
        ee = ExtendedEuclidean()
        solutions = ee.solve_congruence(3, 1, 7)
        assert solutions is not None
        assert len(solutions) == 1
        assert (3 * solutions[0]) % 7 == 1

    def test_solve_congruence_multiple_solutions(self) -> None:
        """Test congruence with multiple solutions."""
        ee = ExtendedEuclidean()
        solutions = ee.solve_congruence(2, 0, 8)
        assert solutions is not None
        assert len(solutions) == 2
        for x in solutions:
            assert (2 * x) % 8 == 0

    def test_solve_congruence_no_solution(self) -> None:
        """Test congruence with no solution."""
        ee = ExtendedEuclidean()
        solutions = ee.solve_congruence(2, 1, 4)
        assert solutions is None

    def test_solve_congruence_invalid_modulus(self) -> None:
        """Test solve_congruence with invalid modulus."""
        ee = ExtendedEuclidean()
        with pytest.raises(ValueError, match="Modulus must be positive"):
            ee.solve_congruence(3, 1, 0)

    def test_chinese_remainder_theorem_simple(self) -> None:
        """Test Chinese Remainder Theorem with simple case."""
        ee = ExtendedEuclidean()
        result = ee.chinese_remainder_theorem([2, 3, 2], [3, 5, 7])
        assert result is not None
        x, M = result
        assert x % 3 == 2
        assert x % 5 == 3
        assert x % 7 == 2
        assert M == 105

    def test_chinese_remainder_theorem_two_equations(self) -> None:
        """Test CRT with two equations."""
        ee = ExtendedEuclidean()
        result = ee.chinese_remainder_theorem([2, 3], [3, 5])
        assert result is not None
        x, M = result
        assert x % 3 == 2
        assert x % 5 == 3
        assert M == 15

    def test_chinese_remainder_theorem_single_equation(self) -> None:
        """Test CRT with single equation."""
        ee = ExtendedEuclidean()
        result = ee.chinese_remainder_theorem([5], [7])
        assert result is not None
        x, M = result
        assert x % 7 == 5
        assert M == 7

    def test_chinese_remainder_theorem_different_lengths(self) -> None:
        """Test CRT with mismatched lengths."""
        ee = ExtendedEuclidean()
        with pytest.raises(ValueError, match="same length"):
            ee.chinese_remainder_theorem([2, 3], [3, 5, 7])

    def test_chinese_remainder_theorem_empty(self) -> None:
        """Test CRT with empty lists."""
        ee = ExtendedEuclidean()
        with pytest.raises(ValueError, match="cannot be empty"):
            ee.chinese_remainder_theorem([], [])

    def test_chinese_remainder_theorem_invalid_moduli(self) -> None:
        """Test CRT with invalid moduli."""
        ee = ExtendedEuclidean()
        with pytest.raises(ValueError, match="must be positive"):
            ee.chinese_remainder_theorem([2, 3], [3, 0])

    def test_chinese_remainder_theorem_general_simple(self) -> None:
        """Test general CRT with simple case."""
        ee = ExtendedEuclidean()
        result = ee.chinese_remainder_theorem_general([2, 3, 2], [3, 5, 7])
        assert result is not None
        x, M = result
        assert x % 3 == 2
        assert x % 5 == 3
        assert x % 7 == 2

    def test_chinese_remainder_theorem_general_non_coprime(self) -> None:
        """Test general CRT with non-coprime moduli."""
        ee = ExtendedEuclidean()
        result = ee.chinese_remainder_theorem_general([2, 0], [4, 6])
        assert result is not None
        x, M = result
        assert x % 4 == 2
        assert x % 6 == 0

    def test_chinese_remainder_theorem_general_no_solution(self) -> None:
        """Test general CRT with no solution."""
        ee = ExtendedEuclidean()
        result = ee.chinese_remainder_theorem_general([1, 0], [2, 4])
        assert result is None

    def test_lcm_simple(self) -> None:
        """Test LCM computation."""
        ee = ExtendedEuclidean()
        assert ee.lcm(4, 6) == 12
        assert ee.lcm(5, 7) == 35
        assert ee.lcm(12, 18) == 36

    def test_lcm_zero(self) -> None:
        """Test LCM with zero."""
        ee = ExtendedEuclidean()
        assert ee.lcm(0, 5) == 0
        assert ee.lcm(5, 0) == 0

    def test_lcm_list(self) -> None:
        """Test LCM of list."""
        ee = ExtendedEuclidean()
        assert ee.lcm_list([4, 6, 8]) == 24
        assert ee.lcm_list([3, 5, 7]) == 105

    def test_lcm_list_empty(self) -> None:
        """Test LCM of empty list."""
        ee = ExtendedEuclidean()
        with pytest.raises(ValueError, match="cannot be empty"):
            ee.lcm_list([])

    def test_extended_gcd_verification(self) -> None:
        """Test that extended GCD always satisfies Bézout's identity."""
        ee = ExtendedEuclidean()
        test_cases = [(48, 18), (17, 13), (100, 25), (21, 14), (35, 15)]

        for a, b in test_cases:
            gcd, x, y = ee.extended_gcd(a, b)
            assert a * x + b * y == gcd, f"Failed for ({a}, {b})"

    def test_modular_inverse_verification(self) -> None:
        """Test that modular inverse always satisfies the property."""
        ee = ExtendedEuclidean()
        test_cases = [(3, 7), (5, 11), (7, 13), (9, 17)]

        for a, m in test_cases:
            inv = ee.modular_inverse(a, m)
            if inv is not None:
                assert (a * inv) % m == 1, f"Failed for ({a}, {m})"

    def test_crt_verification(self) -> None:
        """Test that CRT solution satisfies all congruences."""
        ee = ExtendedEuclidean()
        remainders = [2, 3, 2]
        moduli = [3, 5, 7]

        result = ee.chinese_remainder_theorem(remainders, moduli)
        assert result is not None
        x, M = result

        for r, m in zip(remainders, moduli):
            assert x % m == r, f"Failed for x ≡ {r} (mod {m})"

    def test_crt_general_verification(self) -> None:
        """Test that general CRT solution satisfies all congruences."""
        ee = ExtendedEuclidean()
        remainders = [1, 2, 3]
        moduli = [2, 3, 4]

        result = ee.chinese_remainder_theorem_general(remainders, moduli)
        assert result is not None
        x, M = result

        for r, m in zip(remainders, moduli):
            assert x % m == r, f"Failed for x ≡ {r} (mod {m})"

    def test_solve_two_congruences(self) -> None:
        """Test solving two congruences."""
        ee = ExtendedEuclidean()
        result = ee._solve_two_congruences(2, 3, 3, 5)
        assert result is not None
        x, lcm = result
        assert x % 3 == 2
        assert x % 5 == 3

    def test_solve_two_congruences_no_solution(self) -> None:
        """Test solving two congruences with no solution."""
        ee = ExtendedEuclidean()
        result = ee._solve_two_congruences(1, 2, 0, 4)
        assert result is None
