"""Test suite for FFT polynomial multiplication implementation."""

import pytest

from src.main import FFT


class TestFFT:
    """Test cases for FFT class."""

    def test_initialization(self) -> None:
        """Test FFT initialization."""
        fft = FFT()
        assert fft is not None

    def test_next_power_of_two(self) -> None:
        """Test next power of two calculation."""
        fft = FFT()
        assert fft._next_power_of_two(0) == 1
        assert fft._next_power_of_two(1) == 1
        assert fft._next_power_of_two(2) == 2
        assert fft._next_power_of_two(3) == 4
        assert fft._next_power_of_two(5) == 8
        assert fft._next_power_of_two(16) == 16

    def test_fft_single_element(self) -> None:
        """Test FFT with single element."""
        fft = FFT()
        result = fft.fft([complex(5, 0)])
        assert len(result) == 1
        assert abs(result[0] - complex(5, 0)) < 1e-10

    def test_fft_two_elements(self) -> None:
        """Test FFT with two elements."""
        fft = FFT()
        coeffs = [complex(1, 0), complex(2, 0)]
        result = fft.fft(coeffs)
        assert len(result) == 2
        assert abs(result[0] - complex(3, 0)) < 1e-10
        assert abs(result[1] - complex(-1, 0)) < 1e-10

    def test_fft_four_elements(self) -> None:
        """Test FFT with four elements."""
        fft = FFT()
        coeffs = [complex(1, 0), complex(2, 0), complex(3, 0), complex(4, 0)]
        result = fft.fft(coeffs)
        assert len(result) == 4
        expected_sum = sum(coeffs)
        assert abs(sum(result) - expected_sum) < 1e-10

    def test_fft_non_power_of_two(self) -> None:
        """Test FFT with non-power-of-two length."""
        fft = FFT()
        coeffs = [complex(1, 0), complex(2, 0), complex(3, 0)]
        result = fft.fft(coeffs)
        assert len(result) == 4

    def test_fft_empty(self) -> None:
        """Test FFT with empty list raises error."""
        fft = FFT()
        with pytest.raises(ValueError, match="cannot be empty"):
            fft.fft([])

    def test_ifft_single_element(self) -> None:
        """Test inverse FFT with single element."""
        fft = FFT()
        result = fft.ifft([complex(5, 0)])
        assert len(result) == 1
        assert abs(result[0] - complex(5, 0)) < 1e-10

    def test_ifft_two_elements(self) -> None:
        """Test inverse FFT with two elements."""
        fft = FFT()
        values = [complex(3, 0), complex(-1, 0)]
        result = fft.ifft(values)
        assert len(result) == 2
        assert abs(result[0] - complex(1, 0)) < 1e-10
        assert abs(result[1] - complex(2, 0)) < 1e-10

    def test_fft_ifft_roundtrip(self) -> None:
        """Test that FFT followed by IFFT returns original."""
        fft = FFT()
        original = [complex(1, 0), complex(2, 0), complex(3, 0), complex(4, 0)]
        fft_result = fft.fft(original)
        ifft_result = fft.ifft(fft_result)
        for i in range(len(original)):
            assert abs(ifft_result[i] - original[i]) < 1e-10

    def test_multiply_polynomials_simple(self) -> None:
        """Test simple polynomial multiplication."""
        fft = FFT()
        poly1 = [1, 2]
        poly2 = [3, 4]
        result = fft.multiply_polynomials(poly1, poly2)
        expected = [3, 10, 8]
        assert result == expected

    def test_multiply_polynomials_quadratic(self) -> None:
        """Test polynomial multiplication with quadratic terms."""
        fft = FFT()
        poly1 = [1, 2, 3]
        poly2 = [4, 5]
        result = fft.multiply_polynomials(poly1, poly2)
        expected = [4, 13, 22, 15]
        assert result == expected

    def test_multiply_polynomials_identity(self) -> None:
        """Test polynomial multiplication with identity."""
        fft = FFT()
        poly1 = [1, 0, 0]
        poly2 = [1]
        result = fft.multiply_polynomials(poly1, poly2)
        assert result == [1, 0, 0]

    def test_multiply_polynomials_zero(self) -> None:
        """Test polynomial multiplication with zero polynomial."""
        fft = FFT()
        poly1 = [1, 2]
        poly2 = [0]
        result = fft.multiply_polynomials(poly1, poly2)
        assert result == [0]

    def test_multiply_polynomials_empty(self) -> None:
        """Test that empty polynomials raise error."""
        fft = FFT()
        with pytest.raises(ValueError, match="cannot be empty"):
            fft.multiply_polynomials([], [1, 2])
        with pytest.raises(ValueError, match="cannot be empty"):
            fft.multiply_polynomials([1, 2], [])

    def test_convolve_simple(self) -> None:
        """Test simple convolution."""
        fft = FFT()
        signal1 = [1, 2]
        signal2 = [3, 4]
        result = fft.convolve(signal1, signal2)
        expected = [3, 10, 8]
        assert result == expected

    def test_convolve_empty(self) -> None:
        """Test that empty signals raise error."""
        fft = FFT()
        with pytest.raises(ValueError, match="cannot be empty"):
            fft.convolve([], [1, 2])

    def test_circular_convolution_simple(self) -> None:
        """Test simple circular convolution."""
        fft = FFT()
        signal1 = [1, 2, 3]
        signal2 = [4, 5, 6]
        result = fft.circular_convolution(signal1, signal2)
        assert len(result) == 3

    def test_circular_convolution_different_lengths(self) -> None:
        """Test that different length signals raise error."""
        fft = FFT()
        signal1 = [1, 2]
        signal2 = [3, 4, 5]
        with pytest.raises(ValueError, match="same length"):
            fft.circular_convolution(signal1, signal2)

    def test_circular_convolution_empty(self) -> None:
        """Test that empty signals raise error."""
        fft = FFT()
        with pytest.raises(ValueError, match="cannot be empty"):
            fft.circular_convolution([], [1, 2])

    def test_autocorrelation_simple(self) -> None:
        """Test simple autocorrelation."""
        fft = FFT()
        signal = [1, 2, 3]
        result = fft.autocorrelation(signal)
        assert len(result) == 5

    def test_autocorrelation_empty(self) -> None:
        """Test that empty signal raises error."""
        fft = FFT()
        with pytest.raises(ValueError, match="cannot be empty"):
            fft.autocorrelation([])

    def test_cross_correlation_simple(self) -> None:
        """Test simple cross-correlation."""
        fft = FFT()
        signal1 = [1, 2, 3]
        signal2 = [4, 5]
        result = fft.cross_correlation(signal1, signal2)
        assert len(result) == 4

    def test_cross_correlation_empty(self) -> None:
        """Test that empty signals raise error."""
        fft = FFT()
        with pytest.raises(ValueError, match="cannot be empty"):
            fft.cross_correlation([], [1, 2])

    def test_evaluate_polynomial_linear(self) -> None:
        """Test evaluating linear polynomial."""
        fft = FFT()
        coefficients = [2, 3]
        value = fft.evaluate_polynomial(coefficients, 5)
        assert value == 2 * 5 + 3

    def test_evaluate_polynomial_quadratic(self) -> None:
        """Test evaluating quadratic polynomial."""
        fft = FFT()
        coefficients = [1, 2, 3]
        value = fft.evaluate_polynomial(coefficients, 2)
        assert value == 1 * 4 + 2 * 2 + 3

    def test_evaluate_polynomial_empty(self) -> None:
        """Test evaluating empty polynomial returns zero."""
        fft = FFT()
        value = fft.evaluate_polynomial([], 5)
        assert value == 0.0

    def test_evaluate_polynomial_zero(self) -> None:
        """Test evaluating polynomial at zero."""
        fft = FFT()
        coefficients = [1, 2, 3]
        value = fft.evaluate_polynomial(coefficients, 0)
        assert value == 3

    def test_polynomial_to_string_linear(self) -> None:
        """Test polynomial string representation for linear."""
        fft = FFT()
        coefficients = [1, 2]
        result = fft.polynomial_to_string(coefficients)
        assert "x" in result or "2.00" in result

    def test_polynomial_to_string_quadratic(self) -> None:
        """Test polynomial string representation for quadratic."""
        fft = FFT()
        coefficients = [1, 2, 3]
        result = fft.polynomial_to_string(coefficients)
        assert len(result) > 0

    def test_polynomial_to_string_empty(self) -> None:
        """Test polynomial string representation for empty."""
        fft = FFT()
        result = fft.polynomial_to_string([])
        assert result == "0"

    def test_polynomial_to_string_zero(self) -> None:
        """Test polynomial string representation for zero."""
        fft = FFT()
        result = fft.polynomial_to_string([0, 0, 0])
        assert result == "0"

    def test_large_polynomial_multiplication(self) -> None:
        """Test multiplication of larger polynomials."""
        fft = FFT()
        poly1 = [1] * 10
        poly2 = [1] * 10
        result = fft.multiply_polynomials(poly1, poly2)
        assert len(result) == 19
        assert result[0] == 1
        assert result[-1] == 1

    def test_fft_ifft_consistency(self) -> None:
        """Test FFT and IFFT consistency for various sizes."""
        fft = FFT()
        for size in [1, 2, 4, 8, 16]:
            original = [complex(i, 0) for i in range(size)]
            fft_result = fft.fft(original)
            ifft_result = fft.ifft(fft_result)
            for i in range(size):
                assert abs(ifft_result[i] - original[i]) < 1e-10

    def test_multiply_polynomials_known_result(self) -> None:
        """Test polynomial multiplication with known result."""
        fft = FFT()
        poly1 = [1, 1]
        poly2 = [1, 1]
        result = fft.multiply_polynomials(poly1, poly2)
        expected = [1, 2, 1]
        assert result == expected

    def test_negative_coefficients(self) -> None:
        """Test polynomial multiplication with negative coefficients."""
        fft = FFT()
        poly1 = [1, -2]
        poly2 = [3, 4]
        result = fft.multiply_polynomials(poly1, poly2)
        expected = [3, -2, -8]
        assert result == expected
