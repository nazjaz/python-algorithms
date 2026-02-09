"""Number Theoretic Transform (NTT) implementation for modular arithmetic.

This module implements NTT as an alternative to FFT for exact integer arithmetic
using modular arithmetic instead of complex numbers.
"""

import logging
import sys
from typing import List, Optional, Tuple

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class NTT:
    """Number Theoretic Transform implementation for modular arithmetic.

    NTT is similar to FFT but works in modular arithmetic, providing exact
    integer results without floating-point errors.
    """

    DEFAULT_MOD = 998244353
    DEFAULT_ROOT = 3

    def __init__(self, mod: int = DEFAULT_MOD, root: Optional[int] = None) -> None:
        """Initialize NTT with modulus and primitive root.

        Args:
            mod: Prime modulus. Should be of form k*2^n + 1 for large n.
            root: Primitive root modulo mod. If None, will be computed.

        Raises:
            ValueError: If mod is not prime or root is invalid.
        """
        self.mod = mod
        if root is None:
            root = self._find_primitive_root(mod)
        self.root = root
        self.inv_root = self._mod_inverse(root, mod)

    def _is_prime(self, n: int) -> bool:
        """Check if a number is prime.

        Args:
            n: Number to check.

        Returns:
            True if n is prime, False otherwise.
        """
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False

        i = 3
        while i * i <= n:
            if n % i == 0:
                return False
            i += 2
        return True

    def _mod_power(self, base: int, exp: int, mod: int) -> int:
        """Compute base^exp mod mod efficiently.

        Args:
            base: Base number.
            exp: Exponent.
            mod: Modulus.

        Returns:
            base^exp mod mod.
        """
        result = 1
        base = base % mod
        while exp > 0:
            if exp % 2 == 1:
                result = (result * base) % mod
            exp = exp >> 1
            base = (base * base) % mod
        return result

    def _mod_inverse(self, a: int, mod: int) -> int:
        """Compute modular inverse using extended Euclidean algorithm.

        Args:
            a: Number to find inverse for.
            mod: Modulus.

        Returns:
            Modular inverse of a modulo mod.

        Raises:
            ValueError: If a and mod are not coprime.
        """
        def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
            if a == 0:
                return b, 0, 1
            gcd, x1, y1 = extended_gcd(b % a, a)
            x = y1 - (b // a) * x1
            y = x1
            return gcd, x, y

        gcd, x, _ = extended_gcd(a % mod, mod)
        if gcd != 1:
            raise ValueError(f"{a} and {mod} are not coprime")

        return (x % mod + mod) % mod

    def _find_primitive_root(self, mod: int) -> int:
        """Find a primitive root modulo mod.

        Args:
            mod: Prime modulus.

        Returns:
            Primitive root modulo mod.

        Raises:
            ValueError: If mod is not prime.
        """
        if not self._is_prime(mod):
            raise ValueError(f"{mod} is not prime")

        phi = mod - 1
        factors = self._prime_factors(phi)

        for g in range(2, mod):
            is_primitive = True
            for factor in factors:
                if self._mod_power(g, phi // factor, mod) == 1:
                    is_primitive = False
                    break
            if is_primitive:
                return g

        raise ValueError(f"No primitive root found for {mod}")

    def _prime_factors(self, n: int) -> List[int]:
        """Find prime factors of a number.

        Args:
            n: Number to factor.

        Returns:
            List of distinct prime factors.
        """
        factors = []
        d = 2
        while d * d <= n:
            if n % d == 0:
                factors.append(d)
                while n % d == 0:
                    n //= d
            d += 1
        if n > 1:
            factors.append(n)
        return factors

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

    def ntt(self, coefficients: List[int]) -> List[int]:
        """Compute Number Theoretic Transform.

        Converts polynomial from coefficient representation to point-value
        representation using modular arithmetic.

        Args:
            coefficients: List of polynomial coefficients (integers).

        Returns:
            List of NTT values (point-value representation modulo mod).

        Raises:
            ValueError: If coefficients list is empty.
        """
        if not coefficients:
            raise ValueError("Coefficients list cannot be empty")

        n = len(coefficients)
        coeffs = [x % self.mod for x in coefficients]

        if n == 1:
            return coeffs

        if n & (n - 1) != 0:
            next_power = self._next_power_of_two(n)
            coeffs = coeffs + [0] * (next_power - n)
            n = next_power

        root_unity = self._get_root_of_unity(n)
        return self._ntt_recursive(coeffs, n, root_unity)

    def _get_root_of_unity(self, n: int) -> int:
        """Get primitive root of unity for size n.

        Args:
            n: Size (must be power of 2 dividing mod-1).

        Returns:
            Primitive root of unity for size n.
        """
        if (self.mod - 1) % n != 0:
            raise ValueError(f"Size {n} does not divide mod-1 = {self.mod - 1}")

        exp = (self.mod - 1) // n
        return self._mod_power(self.root, exp, self.mod)

    def _ntt_recursive(
        self, coefficients: List[int], n: int, root: int
    ) -> List[int]:
        """Recursive helper for NTT computation.

        Args:
            coefficients: Polynomial coefficients.
            n: Size (must be power of 2).
            root: Primitive root of unity for size n.

        Returns:
            NTT values.
        """
        if n == 1:
            return coefficients

        even_coeffs = [coefficients[i] for i in range(0, n, 2)]
        odd_coeffs = [coefficients[i] for i in range(1, n, 2)]

        root_squared = (root * root) % self.mod
        even_ntt = self._ntt_recursive(even_coeffs, n // 2, root_squared)
        odd_ntt = self._ntt_recursive(odd_coeffs, n // 2, root_squared)

        result = [0] * n
        w = 1

        for k in range(n // 2):
            twiddle = (w * odd_ntt[k]) % self.mod
            result[k] = (even_ntt[k] + twiddle) % self.mod
            result[k + n // 2] = (even_ntt[k] - twiddle) % self.mod
            w = (w * root) % self.mod

        return result

    def intt(self, values: List[int]) -> List[int]:
        """Compute Inverse Number Theoretic Transform.

        Converts polynomial from point-value representation back to
        coefficient representation.

        Args:
            values: List of NTT values (point-value representation).

        Returns:
            List of polynomial coefficients modulo mod.

        Raises:
            ValueError: If values list is empty.
        """
        if not values:
            raise ValueError("Values list cannot be empty")

        n = len(values)
        vals = [x % self.mod for x in values]

        if n == 1:
            return vals

        if n & (n - 1) != 0:
            next_power = self._next_power_of_two(n)
            vals = vals + [0] * (next_power - n)
            n = next_power

        root_unity = self._get_root_of_unity(n)
        inv_root_unity = self._mod_inverse(root_unity, self.mod)
        result = self._ntt_recursive(vals, n, inv_root_unity)
        n_inv = self._mod_inverse(n, self.mod)

        return [(x * n_inv) % self.mod for x in result]

    def multiply_polynomials(
        self, poly1: List[int], poly2: List[int]
    ) -> List[int]:
        """Multiply two polynomials using NTT.

        Args:
            poly1: Coefficients of first polynomial.
            poly2: Coefficients of second polynomial.

        Returns:
            Coefficients of product polynomial modulo mod.

        Raises:
            ValueError: If either polynomial is empty.
        """
        if not poly1 or not poly2:
            raise ValueError("Polynomials cannot be empty")

        max_degree = len(poly1) + len(poly2) - 1
        size = self._next_power_of_two(max_degree)

        coeffs1 = [x % self.mod for x in poly1] + [0] * (size - len(poly1))
        coeffs2 = [x % self.mod for x in poly2] + [0] * (size - len(poly2))

        ntt1 = self.ntt(coeffs1)
        ntt2 = self.ntt(coeffs2)

        pointwise_product = [(ntt1[i] * ntt2[i]) % self.mod for i in range(size)]

        result = self.intt(pointwise_product)

        return result[:max_degree]

    def convolve(self, signal1: List[int], signal2: List[int]) -> List[int]:
        """Compute convolution of two signals using NTT.

        Args:
            signal1: First signal.
            signal2: Second signal.

        Returns:
            Convolution result modulo mod.

        Raises:
            ValueError: If either signal is empty.
        """
        if not signal1 or not signal2:
            raise ValueError("Signals cannot be empty")

        return self.multiply_polynomials(signal1, signal2)

    def circular_convolution(
        self, signal1: List[int], signal2: List[int]
    ) -> List[int]:
        """Compute circular (cyclic) convolution of two signals.

        Args:
            signal1: First signal.
            signal2: Second signal.

        Returns:
            Circular convolution result modulo mod.

        Raises:
            ValueError: If signals have different lengths or are empty.
        """
        if not signal1 or not signal2:
            raise ValueError("Signals cannot be empty")

        if len(signal1) != len(signal2):
            raise ValueError("Signals must have the same length for circular convolution")

        n = len(signal1)

        coeffs1 = [x % self.mod for x in signal1]
        coeffs2 = [x % self.mod for x in signal2]

        ntt1 = self.ntt(coeffs1)
        ntt2 = self.ntt(coeffs2)

        pointwise_product = [(ntt1[i] * ntt2[i]) % self.mod for i in range(n)]

        result = self.intt(pointwise_product)

        return result

    def autocorrelation(self, signal: List[int]) -> List[int]:
        """Compute autocorrelation of a signal.

        Args:
            signal: Input signal.

        Returns:
            Autocorrelation result modulo mod.

        Raises:
            ValueError: If signal is empty.
        """
        if not signal:
            raise ValueError("Signal cannot be empty")

        reversed_signal = signal[::-1]
        return self.convolve(signal, reversed_signal)

    def cross_correlation(
        self, signal1: List[int], signal2: List[int]
    ) -> List[int]:
        """Compute cross-correlation of two signals.

        Args:
            signal1: First signal.
            signal2: Second signal.

        Returns:
            Cross-correlation result modulo mod.

        Raises:
            ValueError: If either signal is empty.
        """
        if not signal1 or not signal2:
            raise ValueError("Signals cannot be empty")

        reversed_signal2 = signal2[::-1]
        return self.convolve(signal1, reversed_signal2)

    def evaluate_polynomial(
        self, coefficients: List[int], x: int
    ) -> int:
        """Evaluate polynomial at a point using Horner's method.

        Args:
            coefficients: Polynomial coefficients.
            x: Point to evaluate at.

        Returns:
            Polynomial value at x modulo mod.
        """
        if not coefficients:
            return 0

        result = coefficients[0] % self.mod
        x_mod = x % self.mod

        for coeff in coefficients[1:]:
            result = (result * x_mod + coeff) % self.mod

        return result

    def polynomial_to_string(self, coefficients: List[int]) -> str:
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
            coeff_mod = coeff % self.mod
            if coeff_mod == 0:
                continue

            if i == 0:
                terms.append(f"{coeff_mod}")
            elif i == 1:
                if coeff_mod == 1:
                    terms.append("x")
                elif coeff_mod == self.mod - 1:
                    terms.append("-x")
                else:
                    terms.append(f"{coeff_mod}x")
            else:
                if coeff_mod == 1:
                    terms.append(f"x^{i}")
                elif coeff_mod == self.mod - 1:
                    terms.append(f"-x^{i}")
                else:
                    terms.append(f"{coeff_mod}x^{i}")

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
    """Main function to run the NTT CLI interface."""
    import argparse

    parser = argparse.ArgumentParser(
        description="NTT for polynomial multiplication and convolution"
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
        help="Compute cross-correlation (format: signal1;signal2)",
    )
    parser.add_argument(
        "--evaluate",
        type=str,
        help="Evaluate polynomial at point (format: coefficients;x)",
    )
    parser.add_argument(
        "--mod",
        type=int,
        default=NTT.DEFAULT_MOD,
        help=f"Prime modulus (default: {NTT.DEFAULT_MOD})",
    )
    parser.add_argument(
        "--root",
        type=int,
        default=None,
        help="Primitive root (default: auto-detect)",
    )

    args = parser.parse_args()

    try:
        ntt = NTT(mod=args.mod, root=args.root)

        if args.multiply:
            if not args.poly1 or not args.poly2:
                logger.error("Both --poly1 and --poly2 required for multiplication")
                sys.exit(1)

            try:
                poly1 = [int(x.strip()) for x in args.poly1.split(",")]
                poly2 = [int(x.strip()) for x in args.poly2.split(",")]
            except ValueError as e:
                logger.error(f"Invalid polynomial format: {e}")
                sys.exit(1)

            result = ntt.multiply_polynomials(poly1, poly2)
            poly1_str = ntt.polynomial_to_string(poly1)
            poly2_str = ntt.polynomial_to_string(poly2)
            result_str = ntt.polynomial_to_string(result)

            print(f"Modulus: {ntt.mod}")
            print(f"Primitive root: {ntt.root}")
            print(f"Polynomial 1: {poly1_str}")
            print(f"Polynomial 2: {poly2_str}")
            print(f"Product: {result_str}")
            print(f"Coefficients: {result}")

        elif args.convolve:
            if not args.poly1 or not args.poly2:
                logger.error("Both --poly1 and --poly2 required for convolution")
                sys.exit(1)

            try:
                signal1 = [int(x.strip()) for x in args.poly1.split(",")]
                signal2 = [int(x.strip()) for x in args.poly2.split(",")]
            except ValueError as e:
                logger.error(f"Invalid signal format: {e}")
                sys.exit(1)

            result = ntt.convolve(signal1, signal2)
            print(f"Signal 1: {signal1}")
            print(f"Signal 2: {signal2}")
            print(f"Convolution: {result}")

        elif args.circular:
            if not args.poly1 or not args.poly2:
                logger.error("Both --poly1 and --poly2 required for circular convolution")
                sys.exit(1)

            try:
                signal1 = [int(x.strip()) for x in args.poly1.split(",")]
                signal2 = [int(x.strip()) for x in args.poly2.split(",")]
            except ValueError as e:
                logger.error(f"Invalid signal format: {e}")
                sys.exit(1)

            result = ntt.circular_convolution(signal1, signal2)
            print(f"Signal 1: {signal1}")
            print(f"Signal 2: {signal2}")
            print(f"Circular Convolution: {result}")

        elif args.autocorr:
            try:
                signal = [int(x.strip()) for x in args.autocorr.split(",")]
            except ValueError as e:
                logger.error(f"Invalid signal format: {e}")
                sys.exit(1)

            result = ntt.autocorrelation(signal)
            print(f"Signal: {signal}")
            print(f"Autocorrelation: {result}")

        elif args.crosscorr:
            try:
                parts = args.crosscorr.split(";")
                if len(parts) != 2:
                    raise ValueError("Format: signal1;signal2")
                signal1 = [int(x.strip()) for x in parts[0].split(",")]
                signal2 = [int(x.strip()) for x in parts[1].split(",")]
            except (ValueError, IndexError) as e:
                logger.error(f"Invalid format: {e}")
                sys.exit(1)

            result = ntt.cross_correlation(signal1, signal2)
            print(f"Signal 1: {signal1}")
            print(f"Signal 2: {signal2}")
            print(f"Cross-correlation: {result}")

        elif args.evaluate:
            try:
                parts = args.evaluate.split(";")
                if len(parts) != 2:
                    raise ValueError("Format: coefficients;x")
                coefficients = [int(x.strip()) for x in parts[0].split(",")]
                x = int(parts[1].strip())
            except (ValueError, IndexError) as e:
                logger.error(f"Invalid format: {e}")
                sys.exit(1)

            value = ntt.evaluate_polynomial(coefficients, x)
            poly_str = ntt.polynomial_to_string(coefficients)
            print(f"Polynomial: {poly_str}")
            print(f"P({x}) mod {ntt.mod} = {value}")

        else:
            print("NTT Polynomial Multiplication and Convolution")
            print("Use --help to see available options")
            print(f"\nDefault modulus: {NTT.DEFAULT_MOD}")
            print("\nExample:")
            print("  python src/main.py --multiply --poly1 '1,2,3' --poly2 '4,5'")

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
