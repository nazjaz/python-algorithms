"""Extended Euclidean Algorithm and Chinese Remainder Theorem implementation.

This module implements the extended Euclidean algorithm for computing modular
inverses and the Chinese Remainder Theorem for solving systems of congruences.
"""

import logging
import sys
from typing import List, Optional, Tuple

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class ExtendedEuclidean:
    """Extended Euclidean Algorithm and Chinese Remainder Theorem implementation.

    Provides methods for computing GCD, modular inverses, and solving systems
    of congruences using the Chinese Remainder Theorem.
    """

    def __init__(self) -> None:
        """Initialize Extended Euclidean calculator."""
        pass

    def extended_gcd(self, a: int, b: int) -> Tuple[int, int, int]:
        """Compute extended GCD and Bézout coefficients.

        Finds integers x and y such that: ax + by = gcd(a, b)

        Args:
            a: First integer.
            b: Second integer.

        Returns:
            Tuple (gcd, x, y) where:
            - gcd is the greatest common divisor of a and b
            - x and y are Bézout coefficients satisfying ax + by = gcd(a, b)

        Example:
            >>> ee = ExtendedEuclidean()
            >>> gcd, x, y = ee.extended_gcd(48, 18)
            >>> gcd == 6 and 48*x + 18*y == 6
            True
        """
        if a == 0:
            return (abs(b), 0, 1 if b > 0 else -1)

        gcd, x1, y1 = self.extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1

        return (gcd, x, y)

    def gcd(self, a: int, b: int) -> int:
        """Compute greatest common divisor.

        Args:
            a: First integer.
            b: Second integer.

        Returns:
            GCD of a and b.
        """
        gcd_result, _, _ = self.extended_gcd(a, b)
        return gcd_result

    def modular_inverse(self, a: int, m: int) -> Optional[int]:
        """Compute modular inverse of a modulo m.

        Finds x such that: ax ≡ 1 (mod m)

        Args:
            a: Number to find inverse for.
            m: Modulus.

        Returns:
            Modular inverse of a modulo m, or None if it doesn't exist.

        Raises:
            ValueError: If m <= 0.

        Example:
            >>> ee = ExtendedEuclidean()
            >>> inv = ee.modular_inverse(3, 7)
            >>> (3 * inv) % 7 == 1
            True
        """
        if m <= 0:
            raise ValueError("Modulus must be positive")

        a = a % m
        if a < 0:
            a += m

        gcd, x, _ = self.extended_gcd(a, m)

        if gcd != 1:
            return None

        return (x % m + m) % m

    def solve_congruence(
        self, a: int, b: int, m: int
    ) -> Optional[List[int]]:
        """Solve linear congruence ax ≡ b (mod m).

        Args:
            a: Coefficient.
            b: Constant term.
            m: Modulus.

        Returns:
            List of solutions modulo m, or None if no solution exists.

        Raises:
            ValueError: If m <= 0.

        Example:
            >>> ee = ExtendedEuclidean()
            >>> solutions = ee.solve_congruence(3, 1, 7)
            >>> all((3 * x) % 7 == 1 for x in solutions)
            True
        """
        if m <= 0:
            raise ValueError("Modulus must be positive")

        a = a % m
        b = b % m

        if a == 0:
            if b == 0:
                return list(range(m))
            return None

        gcd, x, _ = self.extended_gcd(a, m)

        if b % gcd != 0:
            return None

        a_dash = a // gcd
        b_dash = b // gcd
        m_dash = m // gcd

        x0 = (x * b_dash) % m_dash
        if x0 < 0:
            x0 += m_dash

        solutions = []
        for k in range(gcd):
            solutions.append(x0 + k * m_dash)

        return solutions

    def chinese_remainder_theorem(
        self, remainders: List[int], moduli: List[int]
    ) -> Optional[Tuple[int, int]]:
        """Solve system of congruences using Chinese Remainder Theorem.

        Solves the system:
        x ≡ r₁ (mod m₁)
        x ≡ r₂ (mod m₂)
        ...
        x ≡ rₙ (mod mₙ)

        Args:
            remainders: List of remainders [r₁, r₂, ..., rₙ].
            moduli: List of moduli [m₁, m₂, ..., mₙ].

        Returns:
            Tuple (solution, M) where:
            - solution is the unique solution modulo M
            - M is the product of all moduli
            Returns None if no solution exists.

        Raises:
            ValueError: If lists have different lengths or moduli are invalid.

        Example:
            >>> ee = ExtendedEuclidean()
            >>> x, M = ee.chinese_remainder_theorem([2, 3, 2], [3, 5, 7])
            >>> x % 3 == 2 and x % 5 == 3 and x % 7 == 2
            True
        """
        if len(remainders) != len(moduli):
            raise ValueError("Remainders and moduli must have same length")

        if not moduli:
            raise ValueError("Moduli list cannot be empty")

        for m in moduli:
            if m <= 0:
                raise ValueError("All moduli must be positive")

        n = len(moduli)

        if n == 1:
            return (remainders[0] % moduli[0], moduli[0])

        M = 1
        for m in moduli:
            M *= m

        for i in range(n):
            for j in range(i + 1, n):
                if self.gcd(moduli[i], moduli[j]) != 1:
                    logger.warning(
                        f"Moduli {moduli[i]} and {moduli[j]} are not coprime. "
                        "Solution may not be unique or may not exist."
                    )

        solution = 0

        for i in range(n):
            M_i = M // moduli[i]
            inv_M_i = self.modular_inverse(M_i, moduli[i])

            if inv_M_i is None:
                return None

            solution = (solution + remainders[i] * M_i * inv_M_i) % M

        return (solution, M)

    def chinese_remainder_theorem_general(
        self, remainders: List[int], moduli: List[int]
    ) -> Optional[Tuple[int, int]]:
        """Solve system of congruences (general case, moduli need not be coprime).

        Uses iterative method to handle non-coprime moduli.

        Args:
            remainders: List of remainders [r₁, r₂, ..., rₙ].
            moduli: List of moduli [m₁, m₂, ..., mₙ].

        Returns:
            Tuple (solution, M) where:
            - solution is a solution modulo M
            - M is the least common multiple of moduli
            Returns None if no solution exists.

        Raises:
            ValueError: If lists have different lengths or moduli are invalid.
        """
        if len(remainders) != len(moduli):
            raise ValueError("Remainders and moduli must have same length")

        if not moduli:
            raise ValueError("Moduli list cannot be empty")

        for m in moduli:
            if m <= 0:
                raise ValueError("All moduli must be positive")

        n = len(moduli)

        if n == 1:
            return (remainders[0] % moduli[0], moduli[0])

        x = remainders[0]
        m = moduli[0]

        for i in range(1, n):
            r = remainders[i]
            n_i = moduli[i]

            gcd = self.gcd(m, n_i)

            if (x - r) % gcd != 0:
                return None

            x1, m1 = self._solve_two_congruences(x, m, r, n_i)
            if x1 is None:
                return None

            x = x1
            m = m1

        return (x, m)

    def _solve_two_congruences(
        self, r1: int, m1: int, r2: int, m2: int
    ) -> Optional[Tuple[int, int]]:
        """Solve system of two congruences.

        Solves:
        x ≡ r₁ (mod m₁)
        x ≡ r₂ (mod m₂)

        Args:
            r1: Remainder for first congruence.
            m1: Modulus for first congruence.
            r2: Remainder for second congruence.
            m2: Modulus for second congruence.

        Returns:
            Tuple (solution, lcm) or None if no solution.
        """
        gcd = self.gcd(m1, m2)

        if (r1 - r2) % gcd != 0:
            return None

        lcm = (m1 * m2) // gcd

        gcd, x, y = self.extended_gcd(m1, m2)

        k = (r2 - r1) // gcd
        solution = (r1 + k * x * m1) % lcm

        if solution < 0:
            solution += lcm

        return (solution, lcm)

    def lcm(self, a: int, b: int) -> int:
        """Compute least common multiple.

        Args:
            a: First integer.
            b: Second integer.

        Returns:
            LCM of a and b.
        """
        if a == 0 or b == 0:
            return 0
        return abs(a * b) // self.gcd(a, b)

    def lcm_list(self, numbers: List[int]) -> int:
        """Compute LCM of a list of numbers.

        Args:
            numbers: List of integers.

        Returns:
            LCM of all numbers.

        Raises:
            ValueError: If list is empty.
        """
        if not numbers:
            raise ValueError("List cannot be empty")

        result = numbers[0]
        for num in numbers[1:]:
            result = self.lcm(result, num)

        return result


def main() -> None:
    """Main function to run the Extended Euclidean and CRT CLI interface."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Extended Euclidean Algorithm and Chinese Remainder Theorem"
    )
    parser.add_argument(
        "--gcd",
        type=str,
        help="Compute GCD (format: a,b)",
    )
    parser.add_argument(
        "--extended-gcd",
        type=str,
        help="Compute extended GCD (format: a,b)",
    )
    parser.add_argument(
        "--modular-inverse",
        type=str,
        help="Compute modular inverse (format: a,m)",
    )
    parser.add_argument(
        "--solve-congruence",
        type=str,
        help="Solve congruence ax ≡ b (mod m) (format: a,b,m)",
    )
    parser.add_argument(
        "--crt",
        type=str,
        help="Solve CRT system (format: r1,r2,...;m1,m2,...)",
    )
    parser.add_argument(
        "--crt-general",
        type=str,
        help="Solve CRT system (general case) (format: r1,r2,...;m1,m2,...)",
    )
    parser.add_argument(
        "--lcm",
        type=str,
        help="Compute LCM (format: a,b or a,b,c,...)",
    )

    args = parser.parse_args()

    try:
        ee = ExtendedEuclidean()

        if args.gcd:
            try:
                parts = args.gcd.split(",")
                if len(parts) != 2:
                    raise ValueError("Format: a,b")
                a, b = int(parts[0].strip()), int(parts[1].strip())
            except (ValueError, IndexError) as e:
                logger.error(f"Invalid format: {e}")
                sys.exit(1)

            gcd = ee.gcd(a, b)
            print(f"GCD({a}, {b}) = {gcd}")

        elif args.extended_gcd:
            try:
                parts = args.extended_gcd.split(",")
                if len(parts) != 2:
                    raise ValueError("Format: a,b")
                a, b = int(parts[0].strip()), int(parts[1].strip())
            except (ValueError, IndexError) as e:
                logger.error(f"Invalid format: {e}")
                sys.exit(1)

            gcd, x, y = ee.extended_gcd(a, b)
            print(f"Extended GCD({a}, {b}):")
            print(f"  GCD = {gcd}")
            print(f"  Coefficients: x = {x}, y = {y}")
            print(f"  Verification: {a}*{x} + {b}*{y} = {a*x + b*y}")

        elif args.modular_inverse:
            try:
                parts = args.modular_inverse.split(",")
                if len(parts) != 2:
                    raise ValueError("Format: a,m")
                a, m = int(parts[0].strip()), int(parts[1].strip())
            except (ValueError, IndexError) as e:
                logger.error(f"Invalid format: {e}")
                sys.exit(1)

            inv = ee.modular_inverse(a, m)
            if inv is not None:
                print(f"Modular inverse of {a} modulo {m}: {inv}")
                print(f"Verification: ({a} * {inv}) mod {m} = {(a * inv) % m}")
            else:
                print(f"No modular inverse exists for {a} modulo {m}")

        elif args.solve_congruence:
            try:
                parts = args.solve_congruence.split(",")
                if len(parts) != 3:
                    raise ValueError("Format: a,b,m")
                a, b, m = (
                    int(parts[0].strip()),
                    int(parts[1].strip()),
                    int(parts[2].strip()),
                )
            except (ValueError, IndexError) as e:
                logger.error(f"Invalid format: {e}")
                sys.exit(1)

            solutions = ee.solve_congruence(a, b, m)
            if solutions is not None:
                print(f"Solutions to {a}x ≡ {b} (mod {m}): {solutions}")
                for x in solutions:
                    print(f"  Verification: {a}*{x} mod {m} = {(a*x) % m}")
            else:
                print(f"No solution exists for {a}x ≡ {b} (mod {m})")

        elif args.crt:
            try:
                parts = args.crt.split(";")
                if len(parts) != 2:
                    raise ValueError("Format: r1,r2,...;m1,m2,...")
                remainders = [int(x.strip()) for x in parts[0].split(",")]
                moduli = [int(x.strip()) for x in parts[1].split(",")]
            except (ValueError, IndexError) as e:
                logger.error(f"Invalid format: {e}")
                sys.exit(1)

            result = ee.chinese_remainder_theorem(remainders, moduli)
            if result:
                x, M = result
                print(f"Chinese Remainder Theorem solution:")
                print(f"  Remainders: {remainders}")
                print(f"  Moduli: {moduli}")
                print(f"  Solution: x ≡ {x} (mod {M})")
                for i, (r, m) in enumerate(zip(remainders, moduli)):
                    print(f"  Verification {i+1}: {x} mod {m} = {x % m} (expected {r})")
            else:
                print("No solution exists for the given system")

        elif args.crt_general:
            try:
                parts = args.crt_general.split(";")
                if len(parts) != 2:
                    raise ValueError("Format: r1,r2,...;m1,m2,...")
                remainders = [int(x.strip()) for x in parts[0].split(",")]
                moduli = [int(x.strip()) for x in parts[1].split(",")]
            except (ValueError, IndexError) as e:
                logger.error(f"Invalid format: {e}")
                sys.exit(1)

            result = ee.chinese_remainder_theorem_general(remainders, moduli)
            if result:
                x, M = result
                print(f"Chinese Remainder Theorem solution (general case):")
                print(f"  Remainders: {remainders}")
                print(f"  Moduli: {moduli}")
                print(f"  Solution: x ≡ {x} (mod {M})")
                for i, (r, m) in enumerate(zip(remainders, moduli)):
                    print(f"  Verification {i+1}: {x} mod {m} = {x % m} (expected {r})")
            else:
                print("No solution exists for the given system")

        elif args.lcm:
            try:
                parts = [int(x.strip()) for x in args.lcm.split(",")]
                if len(parts) < 2:
                    raise ValueError("Need at least 2 numbers")
            except (ValueError, IndexError) as e:
                logger.error(f"Invalid format: {e}")
                sys.exit(1)

            if len(parts) == 2:
                lcm = ee.lcm(parts[0], parts[1])
                print(f"LCM({parts[0]}, {parts[1]}) = {lcm}")
            else:
                lcm = ee.lcm_list(parts)
                print(f"LCM({parts}) = {lcm}")

        else:
            print("Extended Euclidean Algorithm and Chinese Remainder Theorem")
            print("Use --help to see available options")
            print("\nExamples:")
            print("  python src/main.py --gcd 48,18")
            print("  python src/main.py --extended-gcd 48,18")
            print("  python src/main.py --modular-inverse 3,7")
            print("  python src/main.py --crt '2,3,2;3,5,7'")

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
