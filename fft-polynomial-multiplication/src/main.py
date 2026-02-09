"""Fast Fourier Transform (FFT) implementation for polynomial multiplication.

This module implements the FFT algorithm for efficient polynomial multiplication
and convolution operations using the Cooley-Tukey algorithm.
"""

import cmath
import logging
import sys
from typing import List, Tuple

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class FFT:
    """Fast Fourier Transform implementation for polynomial operations.

    Implements FFT and inverse FFT for efficient polynomial multiplication
    and convolution operations.
    """

    def __init__(self) -> None:
        """Initialize FFT instance."""
        pass

    def _next_power_of_two(self, n: int) -> int:
        """Find the smallest power of two greater than or equal to n.

        Args:
            n: Input number.

        Returns:
            Smallest power of two >= n.
        """
        if n == 0:
            return 1
        power = 1
        while power < n:
            power <<= 1
        return power

    def fft(self, coefficients: List[complex]) -> List[complex]:
        """Compute Fast Fourier Transform of polynomial coefficients.

        Converts polynomial from coefficient representation to point-value
        representation using divide-and-conquer approach.

        Args:
            coefficients: List of polynomial coefficients (complex numbers).

        Returns:
            List of FFT values (point-value representation).

        Raises:
            ValueError: If coefficients list is empty.
        """
        if not coefficients:
            raise ValueError("Coefficients list cannot be empty")

        n = len(coefficients)

        if n == 1:
            return coefficients

        if n & (n - 1) != 0:
            next_power = self._next_power_of_two(n)
            coefficients = coefficients + [0] * (next_power - n)
            n = next_power

        even_coeffs = [coefficients[i] for i in range(0, n, 2)]
        odd_coeffs = [coefficients[i] for i in range(1, n, 2)]

        even_fft = self.fft(even_coeffs)
        odd_fft = self.fft(odd_coeffs)

        result = [0] * n
        angle = -2 * cmath.pi / n

        for k in range(n // 2):
            twiddle = cmath.exp(angle * k * 1j) * odd_fft[k]
            result[k] = even_fft[k] + twiddle
            result[k + n // 2] = even_fft[k] - twiddle

        return result

    def ifft(self, values: List[complex]) -> List[complex]:
        """Compute Inverse Fast Fourier Transform.

        Converts polynomial from point-value representation back to
        coefficient representation.

        Args:
            values: List of FFT values (point-value representation).

        Returns:
            List of polynomial coefficients.

        Raises:
            ValueError: If values list is empty.
        """
        if not values:
            raise ValueError("Values list cannot be empty")

        n = len(values)

        if n == 1:
            return values

        if n & (n - 1) != 0:
            next_power = self._next_power_of_two(n)
            values = values + [0] * (next_power - n)
            n = next_power

        even_vals = [values[i] for i in range(0, n, 2)]
        odd_vals = [values[i] for i in range(1, n, 2)]

        even_ifft = self.ifft(even_vals)
        odd_ifft = self.ifft(odd_vals)

        result = [0] * n
        angle = 2 * cmath.pi / n

        for k in range(n // 2):
            twiddle = cmath.exp(angle * k * 1j) * odd_ifft[k]
            result[k] = even_ifft[k] + twiddle
            result[k + n // 2] = even_ifft[k] - twiddle

        return result

    def multiply_polynomials(
        self, poly1: List[float], poly2: List[float]
    ) -> List[float]:
        """Multiply two polynomials using FFT.

        Args:
            poly1: Coefficients of first polynomial.
            poly2: Coefficients of second polynomial.

        Returns:
            Coefficients of product polynomial.

        Raises:
            ValueError: If either polynomial is empty.
        """
        if not poly1 or not poly2:
            raise ValueError("Polynomials cannot be empty")

        max_degree = len(poly1) + len(poly2) - 1
        size = self._next_power_of_two(max_degree)

        coeffs1 = [complex(x, 0) for x in poly1] + [0] * (size - len(poly1))
        coeffs2 = [complex(x, 0) for x in poly2] + [0] * (size - len(poly2))

        fft1 = self.fft(coeffs1)
        fft2 = self.fft(coeffs2)

        pointwise_product = [fft1[i] * fft2[i] for i in range(size)]

        result_complex = self.ifft(pointwise_product)

        result = [round((x / size).real) for x in result_complex[:max_degree]]

        return result

    def convolve(
        self, signal1: List[float], signal2: List[float]
    ) -> List[float]:
        """Compute convolution of two signals using FFT.

        Convolution is equivalent to polynomial multiplication where
        one polynomial is reversed.

        Args:
            signal1: First signal.
            signal2: Second signal.

        Returns:
            Convolution result.

        Raises:
            ValueError: If either signal is empty.
        """
        if not signal1 or not signal2:
            raise ValueError("Signals cannot be empty")

        return self.multiply_polynomials(signal1, signal2)

    def circular_convolution(
        self, signal1: List[float], signal2: List[float]
    ) -> List[float]:
        """Compute circular (cyclic) convolution of two signals.

        Args:
            signal1: First signal.
            signal2: Second signal.

        Returns:
            Circular convolution result.

        Raises:
            ValueError: If signals have different lengths or are empty.
        """
        if not signal1 or not signal2:
            raise ValueError("Signals cannot be empty")

        if len(signal1) != len(signal2):
            raise ValueError("Signals must have the same length for circular convolution")

        n = len(signal1)

        coeffs1 = [complex(x, 0) for x in signal1]
        coeffs2 = [complex(x, 0) for x in signal2]

        fft1 = self.fft(coeffs1)
        fft2 = self.fft(coeffs2)

        pointwise_product = [fft1[i] * fft2[i] for i in range(n)]

        result_complex = self.ifft(pointwise_product)

        result = [round((x / n).real) for x in result_complex]

        return result

    def autocorrelation(self, signal: List[float]) -> List[float]:
        """Compute autocorrelation of a signal.

        Args:
            signal: Input signal.

        Returns:
            Autocorrelation result.

        Raises:
            ValueError: If signal is empty.
        """
        if not signal:
            raise ValueError("Signal cannot be empty")

        reversed_signal = signal[::-1]
        return self.convolve(signal, reversed_signal)

    def cross_correlation(
        self, signal1: List[float], signal2: List[float]
    ) -> List[float]:
        """Compute cross-correlation of two signals.

        Args:
            signal1: First signal.
            signal2: Second signal.

        Returns:
            Cross-correlation result.

        Raises:
            ValueError: If either signal is empty.
        """
        if not signal1 or not signal2:
            raise ValueError("Signals cannot be empty")

        reversed_signal2 = signal2[::-1]
        return self.convolve(signal1, reversed_signal2)

    def evaluate_polynomial(
        self, coefficients: List[float], x: float
    ) -> float:
        """Evaluate polynomial at a point using Horner's method.

        Args:
            coefficients: Polynomial coefficients.
            x: Point to evaluate at.

        Returns:
            Polynomial value at x.
        """
        if not coefficients:
            return 0.0

        result = coefficients[0]
        for coeff in coefficients[1:]:
            result = result * x + coeff

        return result

    def polynomial_to_string(self, coefficients: List[float]) -> str:
        """Convert polynomial coefficients to string representation.

        Args:
            coefficients: Polynomial coefficients.

        Returns:
            String representation of polynomial.
        """
        if not coefficients:
            return "0"

        terms = []
        for i, coeff in enumerate(coefficients):
            if abs(coeff) < 1e-10:
                continue

            if i == 0:
                terms.append(f"{coeff:.2f}")
            elif i == 1:
                if abs(coeff - 1) < 1e-10:
                    terms.append("x")
                elif abs(coeff + 1) < 1e-10:
                    terms.append("-x")
                else:
                    terms.append(f"{coeff:.2f}x")
            else:
                if abs(coeff - 1) < 1e-10:
                    terms.append(f"x^{i}")
                elif abs(coeff + 1) < 1e-10:
                    terms.append(f"-x^{i}")
                else:
                    terms.append(f"{coeff:.2f}x^{i}")

        if not terms:
            return "0"

        result = terms[0]
        for term in terms[1:]:
            if term.startswith("-"):
                result += f" - {term[1:]}"
            else:
                result += f" + {term}"

        return result


def main() -> None:
    """Main function to run the FFT CLI interface."""
    import argparse

    parser = argparse.ArgumentParser(
        description="FFT for polynomial multiplication and convolution"
    )
    parser.add_argument(
        "--poly1",
        type=str,
        help="First polynomial coefficients (comma-separated)",
    )
    parser.add_argument(
        "--poly2",
        type=str,
        help="Second polynomial coefficients (comma-separated)",
    )
    parser.add_argument(
        "--multiply",
        action="store_true",
        help="Multiply two polynomials",
    )
    parser.add_argument(
        "--convolve",
        action="store_true",
        help="Compute convolution of two signals",
    )
    parser.add_argument(
        "--circular",
        action="store_true",
        help="Compute circular convolution",
    )
    parser.add_argument(
        "--autocorr",
        type=str,
        help="Compute autocorrelation (comma-separated signal)",
    )
    parser.add_argument(
        "--crosscorr",
        type=str,
        help="Compute cross-correlation (format: signal1,signal2)",
    )
    parser.add_argument(
        "--evaluate",
        type=str,
        help="Evaluate polynomial at point (format: coefficients,x)",
    )

    args = parser.parse_args()

    try:
        fft = FFT()

        if args.multiply:
            if not args.poly1 or not args.poly2:
                logger.error("Both --poly1 and --poly2 required for multiplication")
                sys.exit(1)

            try:
                poly1 = [float(x.strip()) for x in args.poly1.split(",")]
                poly2 = [float(x.strip()) for x in args.poly2.split(",")]
            except ValueError as e:
                logger.error(f"Invalid polynomial format: {e}")
                sys.exit(1)

            result = fft.multiply_polynomials(poly1, poly2)
            poly1_str = fft.polynomial_to_string(poly1)
            poly2_str = fft.polynomial_to_string(poly2)
            result_str = fft.polynomial_to_string(result)

            print(f"Polynomial 1: {poly1_str}")
            print(f"Polynomial 2: {poly2_str}")
            print(f"Product: {result_str}")
            print(f"Coefficients: {result}")

        elif args.convolve:
            if not args.poly1 or not args.poly2:
                logger.error("Both --poly1 and --poly2 required for convolution")
                sys.exit(1)

            try:
                signal1 = [float(x.strip()) for x in args.poly1.split(",")]
                signal2 = [float(x.strip()) for x in args.poly2.split(",")]
            except ValueError as e:
                logger.error(f"Invalid signal format: {e}")
                sys.exit(1)

            result = fft.convolve(signal1, signal2)
            print(f"Signal 1: {signal1}")
            print(f"Signal 2: {signal2}")
            print(f"Convolution: {result}")

        elif args.circular:
            if not args.poly1 or not args.poly2:
                logger.error("Both --poly1 and --poly2 required for circular convolution")
                sys.exit(1)

            try:
                signal1 = [float(x.strip()) for x in args.poly1.split(",")]
                signal2 = [float(x.strip()) for x in args.poly2.split(",")]
            except ValueError as e:
                logger.error(f"Invalid signal format: {e}")
                sys.exit(1)

            result = fft.circular_convolution(signal1, signal2)
            print(f"Signal 1: {signal1}")
            print(f"Signal 2: {signal2}")
            print(f"Circular Convolution: {result}")

        elif args.autocorr:
            try:
                signal = [float(x.strip()) for x in args.autocorr.split(",")]
            except ValueError as e:
                logger.error(f"Invalid signal format: {e}")
                sys.exit(1)

            result = fft.autocorrelation(signal)
            print(f"Signal: {signal}")
            print(f"Autocorrelation: {result}")

        elif args.crosscorr:
            try:
                parts = args.crosscorr.split(";")
                if len(parts) != 2:
                    raise ValueError("Format: signal1;signal2 (use semicolon to separate signals)")
                signal1 = [float(x.strip()) for x in parts[0].split(",")]
                signal2 = [float(x.strip()) for x in parts[1].split(",")]
            except (ValueError, IndexError) as e:
                logger.error(f"Invalid format: {e}")
                sys.exit(1)

            result = fft.cross_correlation(signal1, signal2)
            print(f"Signal 1: {signal1}")
            print(f"Signal 2: {signal2}")
            print(f"Cross-correlation: {result}")

        elif args.evaluate:
            try:
                parts = args.evaluate.split(";")
                if len(parts) != 2:
                    raise ValueError("Format: coefficients;x (use semicolon to separate)")
                coefficients = [float(x.strip()) for x in parts[0].split(",")]
                x = float(parts[1].strip())
            except (ValueError, IndexError) as e:
                logger.error(f"Invalid format: {e}")
                sys.exit(1)

            value = fft.evaluate_polynomial(coefficients, x)
            poly_str = fft.polynomial_to_string(coefficients)
            print(f"Polynomial: {poly_str}")
            print(f"P({x}) = {value}")

        else:
            print("FFT Polynomial Multiplication and Convolution")
            print("Use --help to see available options")
            print("\nExample:")
            print("  python src/main.py --multiply --poly1 '1,2,3' --poly2 '4,5'")

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
