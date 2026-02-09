"""Test suite for NTT (Number Theoretic Transform) implementation."""

import pytest

from src.main import NTT


class TestNTT:
    """Test cases for NTT class."""

    def test_initialization_default(self) -> None:
        """Test default initialization."""
        ntt = NTT()
        assert ntt.mod == 998244353
        assert ntt.root == 3

    def test_initialization_custom(self) -> None:
        """Test initialization with custom modulus."""
        mod = 7340033
        ntt = NTT(mod=mod)
        assert ntt.mod == mod

    def test_is_prime(self) -> None:
        """Test prime checking."""
        ntt = NTT()
        assert ntt._is_prime(2) is True
        assert ntt._is_prime(3) is True
        assert ntt._is_prime(4) is False
        assert ntt._is_prime(17) is True
        assert ntt._is_prime(998244353) is True

    def test_mod_power(self) -> None:
        """Test modular exponentiation."""
        ntt = NTT()
        assert ntt._mod_power(2, 3, 7) == 1
        assert ntt._mod_power(3, 4, 7) == 4
        assert ntt._mod_power(5, 0, 7) == 1

    def test_mod_inverse(self) -> None:
        """Test modular inverse."""
        ntt = NTT()
        inv = ntt._mod_inverse(3, 7)
        assert (inv * 3) % 7 == 1
        assert ntt._mod_inverse(2, 5) == 3

    def test_next_power_of_two(self) -> None:
        """Test next power of two calculation."""
        ntt = NTT()
        assert ntt._next_power_of_two(0) == 1
        assert ntt._next_power_of_two(1) == 1
        assert ntt._next_power_of_two(2) == 2
        assert ntt._next_power_of_two(3) == 4
        assert ntt._next_power_of_two(5) == 8
        assert ntt._next_power_of_two(16) == 16

    def test_ntt_single_element(self) -> None:
        """Test NTT with single element."""
        ntt = NTT()
        result = ntt.ntt([5])
        assert result == [5]

    def test_ntt_two_elements(self) -> None:
        """Test NTT with two elements."""
        ntt = NTT()
        coeffs = [1, 2]
        result = ntt.ntt(coeffs)
        assert len(result) == 2

    def test_ntt_four_elements(self) -> None:
        """Test NTT with four elements."""
        ntt = NTT()
        coeffs = [1, 2, 3, 4]
        result = ntt.ntt(coeffs)
        assert len(result) == 4

    def test_ntt_non_power_of_two(self) -> None:
        """Test NTT with non-power-of-two length."""
        ntt = NTT()
        coeffs = [1, 2, 3]
        result = ntt.ntt(coeffs)
        assert len(result) == 4

    def test_ntt_empty(self) -> None:
        """Test NTT with empty list raises error."""
        ntt = NTT()
        with pytest.raises(ValueError, match="cannot be empty"):
            ntt.ntt([])

    def test_intt_single_element(self) -> None:
        """Test inverse NTT with single element."""
        ntt = NTT()
        result = ntt.intt([5])
        assert result == [5]

    def test_intt_two_elements(self) -> None:
        """Test inverse NTT with two elements."""
        ntt = NTT()
        values = ntt.ntt([1, 2])
        result = ntt.intt(values)
        assert result == [1, 2]

    def test_ntt_intt_roundtrip(self) -> None:
        """Test that NTT followed by INTT returns original."""
        ntt = NTT()
        original = [1, 2, 3, 4]
        ntt_result = ntt.ntt(original)
        intt_result = ntt.intt(ntt_result)
        assert intt_result == original

    def test_ntt_intt_roundtrip_large(self) -> None:
        """Test NTT/INTT roundtrip with larger array."""
        ntt = NTT()
        original = list(range(1, 9))
        ntt_result = ntt.ntt(original)
        intt_result = ntt.intt(ntt_result)
        assert intt_result == original

    def test_multiply_polynomials_simple(self) -> None:
        """Test simple polynomial multiplication."""
        ntt = NTT()
        poly1 = [1, 2]
        poly2 = [3, 4]
        result = ntt.multiply_polynomials(poly1, poly2)
        expected = [3, 10, 8]
        assert result == expected

    def test_multiply_polynomials_quadratic(self) -> None:
        """Test polynomial multiplication with quadratic terms."""
        ntt = NTT()
        poly1 = [1, 2, 3]
        poly2 = [4, 5]
        result = ntt.multiply_polynomials(poly1, poly2)
        expected = [4, 13, 22, 15]
        assert result == expected

    def test_multiply_polynomials_identity(self) -> None:
        """Test polynomial multiplication with identity."""
        ntt = NTT()
        poly1 = [1, 0, 0]
        poly2 = [1]
        result = ntt.multiply_polynomials(poly1, poly2)
        assert result == [1, 0, 0]

    def test_multiply_polynomials_zero(self) -> None:
        """Test polynomial multiplication with zero polynomial."""
        ntt = NTT()
        poly1 = [1, 2]
        poly2 = [0]
        result = ntt.multiply_polynomials(poly1, poly2)
        assert result == [0]

    def test_multiply_polynomials_empty(self) -> None:
        """Test that empty polynomials raise error."""
        ntt = NTT()
        with pytest.raises(ValueError, match="cannot be empty"):
            ntt.multiply_polynomials([], [1, 2])
        with pytest.raises(ValueError, match="cannot be empty"):
            ntt.multiply_polynomials([1, 2], [])

    def test_convolve_simple(self) -> None:
        """Test simple convolution."""
        ntt = NTT()
        signal1 = [1, 2]
        signal2 = [3, 4]
        result = ntt.convolve(signal1, signal2)
        expected = [3, 10, 8]
        assert result == expected

    def test_convolve_empty(self) -> None:
        """Test that empty signals raise error."""
        ntt = NTT()
        with pytest.raises(ValueError, match="cannot be empty"):
            ntt.convolve([], [1, 2])

    def test_circular_convolution_simple(self) -> None:
        """Test simple circular convolution."""
        ntt = NTT()
        signal1 = [1, 2, 3]
        signal2 = [4, 5, 6]
        result = ntt.circular_convolution(signal1, signal2)
        assert len(result) == 3

    def test_circular_convolution_different_lengths(self) -> None:
        """Test that different length signals raise error."""
        ntt = NTT()
        signal1 = [1, 2]
        signal2 = [3, 4, 5]
        with pytest.raises(ValueError, match="same length"):
            ntt.circular_convolution(signal1, signal2)

    def test_circular_convolution_empty(self) -> None:
        """Test that empty signals raise error."""
        ntt = NTT()
        with pytest.raises(ValueError, match="cannot be empty"):
            ntt.circular_convolution([], [1, 2])

    def test_autocorrelation_simple(self) -> None:
        """Test simple autocorrelation."""
        ntt = NTT()
        signal = [1, 2, 3]
        result = ntt.autocorrelation(signal)
        assert len(result) == 5

    def test_autocorrelation_empty(self) -> None:
        """Test that empty signal raises error."""
        ntt = NTT()
        with pytest.raises(ValueError, match="cannot be empty"):
            ntt.autocorrelation([])

    def test_cross_correlation_simple(self) -> None:
        """Test simple cross-correlation."""
        ntt = NTT()
        signal1 = [1, 2, 3]
        signal2 = [4, 5]
        result = ntt.cross_correlation(signal1, signal2)
        assert len(result) == 4

    def test_cross_correlation_empty(self) -> None:
        """Test that empty signals raise error."""
        ntt = NTT()
        with pytest.raises(ValueError, match="cannot be empty"):
            ntt.cross_correlation([], [1, 2])

    def test_evaluate_polynomial_linear(self) -> None:
        """Test evaluating linear polynomial."""
        ntt = NTT()
        coefficients = [2, 3]
        value = ntt.evaluate_polynomial(coefficients, 5)
        expected = (2 * 5 + 3) % ntt.mod
        assert value == expected

    def test_evaluate_polynomial_quadratic(self) -> None:
        """Test evaluating quadratic polynomial."""
        ntt = NTT()
        coefficients = [1, 2, 3]
        value = ntt.evaluate_polynomial(coefficients, 2)
        expected = (1 * 4 + 2 * 2 + 3) % ntt.mod
        assert value == expected

    def test_evaluate_polynomial_empty(self) -> None:
        """Test evaluating empty polynomial returns zero."""
        ntt = NTT()
        value = ntt.evaluate_polynomial([], 5)
        assert value == 0

    def test_evaluate_polynomial_zero(self) -> None:
        """Test evaluating polynomial at zero."""
        ntt = NTT()
        coefficients = [1, 2, 3]
        value = ntt.evaluate_polynomial(coefficients, 0)
        assert value == 3

    def test_polynomial_to_string_linear(self) -> None:
        """Test polynomial string representation for linear."""
        ntt = NTT()
        coefficients = [1, 2]
        result = ntt.polynomial_to_string(coefficients)
        assert len(result) > 0

    def test_polynomial_to_string_empty(self) -> None:
        """Test polynomial string representation for empty."""
        ntt = NTT()
        result = ntt.polynomial_to_string([])
        assert result == "0"

    def test_polynomial_to_string_zero(self) -> None:
        """Test polynomial string representation for zero."""
        ntt = NTT()
        result = ntt.polynomial_to_string([0, 0, 0])
        assert result == "0"

    def test_large_polynomial_multiplication(self) -> None:
        """Test multiplication of larger polynomials."""
        ntt = NTT()
        poly1 = [1] * 10
        poly2 = [1] * 10
        result = ntt.multiply_polynomials(poly1, poly2)
        assert len(result) == 19
        assert result[0] == 1
        assert result[-1] == 1

    def test_ntt_intt_consistency(self) -> None:
        """Test NTT and INTT consistency for various sizes."""
        ntt = NTT()
        for size in [1, 2, 4, 8, 16]:
            original = list(range(1, size + 1))
            ntt_result = ntt.ntt(original)
            intt_result = ntt.intt(ntt_result)
            assert intt_result == original

    def test_multiply_polynomials_known_result(self) -> None:
        """Test polynomial multiplication with known result."""
        ntt = NTT()
        poly1 = [1, 1]
        poly2 = [1, 1]
        result = ntt.multiply_polynomials(poly1, poly2)
        expected = [1, 2, 1]
        assert result == expected

    def test_negative_coefficients(self) -> None:
        """Test polynomial multiplication with negative coefficients."""
        ntt = NTT()
        poly1 = [1, -2]
        poly2 = [3, 4]
        result = ntt.multiply_polynomials(poly1, poly2)
        coeff0 = (1 * 3) % ntt.mod
        coeff1 = (1 * 4 + (-2) * 3) % ntt.mod
        coeff2 = ((-2) * 4) % ntt.mod
        expected = [coeff0, coeff1, coeff2]
        assert result == expected

    def test_get_root_of_unity(self) -> None:
        """Test root of unity calculation."""
        ntt = NTT()
        root4 = ntt._get_root_of_unity(4)
        root4_pow4 = ntt._mod_power(root4, 4, ntt.mod)
        assert root4_pow4 == 1
