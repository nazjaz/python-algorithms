"""Miller-Rabin primality test implementation with deterministic variant.

This module implements the Miller-Rabin probabilistic and deterministic
primality tests for efficient large number testing.
"""

import logging
import random
import sys
from typing import List, Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class MillerRabin:
    """Miller-Rabin primality test implementation.

    Provides both probabilistic and deterministic variants for testing
    whether a number is prime.
    """

    DETERMINISTIC_BASES = {
        2047: [2],
        1373653: [2, 3],
        9080191: [31, 73],
        25326001: [2, 3, 5],
        3215031751: [2, 3, 5, 7],
        4759123141: [2, 7, 61],
        1122004669633: [2, 13, 23, 1662803],
        2152302898747: [2, 3, 5, 7, 11],
        3474749660383: [2, 3, 5, 7, 11, 13],
        341550071728321: [2, 3, 5, 7, 11, 13, 17],
    }

    def __init__(self) -> None:
        """Initialize Miller-Rabin tester."""
        pass

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

    def _decompose(self, n: int) -> tuple[int, int]:
        """Decompose n-1 as d * 2^r where d is odd.

        Args:
            n: Number to decompose (n-1 will be decomposed).

        Returns:
            Tuple (d, r) where d is odd and n-1 = d * 2^r.
        """
        if n <= 1:
            return (0, 0)

        n_minus_one = n - 1
        r = 0
        d = n_minus_one

        while d % 2 == 0:
            r += 1
            d //= 2

        return (d, r)

    def _witness(self, a: int, d: int, r: int, n: int) -> bool:
        """Check if a is a witness for compositeness of n.

        Args:
            a: Base to test.
            d: Odd part of n-1.
            r: Power of 2 in n-1.
            n: Number being tested.

        Returns:
            True if a is a witness (n is composite), False otherwise.
        """
        x = self._mod_power(a, d, n)

        if x == 1 or x == n - 1:
            return False

        for _ in range(r - 1):
            x = (x * x) % n
            if x == n - 1:
                return False

        return True

    def is_prime_probabilistic(
        self, n: int, k: int = 10
    ) -> bool:
        """Test if n is prime using probabilistic Miller-Rabin test.

        Args:
            n: Number to test.
            k: Number of random bases to test (default: 10).

        Returns:
            True if n is probably prime, False if n is definitely composite.

        Raises:
            ValueError: If n < 2 or k < 1.
        """
        if n < 2:
            raise ValueError("n must be >= 2")
        if k < 1:
            raise ValueError("k must be >= 1")

        if n == 2:
            return True
        if n % 2 == 0:
            return False
        if n == 3:
            return True

        d, r = self._decompose(n)

        for _ in range(k):
            if n <= 3:
                break
            a = random.randint(2, n - 2)
            if self._witness(a, d, r, n):
                return False

        return True

    def is_prime_deterministic(self, n: int) -> bool:
        """Test if n is prime using deterministic Miller-Rabin test.

        Uses known sets of bases for different ranges to provide
        deterministic results up to 341,550,071,728,321.

        Args:
            n: Number to test.

        Returns:
            True if n is prime, False if n is composite.

        Raises:
            ValueError: If n < 2.
        """
        if n < 2:
            raise ValueError("n must be >= 2")

        if n == 2:
            return True
        if n % 2 == 0:
            return False

        if n in self.DETERMINISTIC_BASES:
            bases = self.DETERMINISTIC_BASES[n]
        else:
            bases = self._get_deterministic_bases(n)

        if bases is None:
            logger.warning(
                f"n = {n} is too large for deterministic test. "
                "Falling back to probabilistic test."
            )
            return self.is_prime_probabilistic(n, k=20)

        d, r = self._decompose(n)

        for a in bases:
            if a >= n:
                continue
            if self._witness(a, d, r, n):
                return False

        return True

    def _get_deterministic_bases(self, n: int) -> Optional[List[int]]:
        """Get deterministic bases for given n.

        Args:
            n: Number to test.

        Returns:
            List of bases to use, or None if n is too large.
        """
        for threshold, bases in sorted(self.DETERMINISTIC_BASES.items()):
            if n < threshold:
                return bases

        return None

    def find_next_prime(self, n: int, deterministic: bool = False) -> int:
        """Find the next prime number after n.

        Args:
            n: Starting number.
            deterministic: Use deterministic test if True.

        Returns:
            Next prime number after n.

        Raises:
            ValueError: If n < 1.
        """
        if n < 1:
            raise ValueError("n must be >= 1")

        candidate = n + 1
        if candidate == 2:
            return 2

        if candidate % 2 == 0:
            candidate += 1

        test_func = (
            self.is_prime_deterministic
            if deterministic
            else self.is_prime_probabilistic
        )

        while True:
            if test_func(candidate):
                return candidate
            candidate += 2

    def find_previous_prime(self, n: int, deterministic: bool = False) -> int:
        """Find the previous prime number before n.

        Args:
            n: Starting number.
            deterministic: Use deterministic test if True.

        Returns:
            Previous prime number before n, or 2 if no prime exists.

        Raises:
            ValueError: If n < 3.
        """
        if n < 3:
            raise ValueError("n must be >= 3")

        candidate = n - 1
        if candidate == 2:
            return 2

        if candidate % 2 == 0:
            candidate -= 1

        test_func = (
            self.is_prime_deterministic
            if deterministic
            else self.is_prime_probabilistic
        )

        while candidate >= 2:
            if test_func(candidate):
                return candidate
            candidate -= 2

        return 2

    def generate_prime(
        self, bits: int, deterministic: bool = False
    ) -> int:
        """Generate a random prime number with specified number of bits.

        Args:
            bits: Number of bits for the prime.
            deterministic: Use deterministic test if True.

        Returns:
            Random prime number with approximately 'bits' bits.

        Raises:
            ValueError: If bits < 2.
        """
        if bits < 2:
            raise ValueError("bits must be >= 2")

        min_val = 2 ** (bits - 1)
        max_val = (2 ** bits) - 1

        test_func = (
            self.is_prime_deterministic
            if deterministic
            else self.is_prime_probabilistic
        )

        max_attempts = 1000
        for _ in range(max_attempts):
            candidate = random.randint(min_val, max_val)
            if candidate % 2 == 0:
                candidate += 1
            if candidate > max_val:
                candidate = min_val + (candidate - max_val - 1)
                if candidate % 2 == 0:
                    candidate += 1

            if test_func(candidate):
                return candidate

        raise RuntimeError(
            f"Failed to generate prime with {bits} bits after "
            f"{max_attempts} attempts"
        )

    def count_primes_in_range(
        self, start: int, end: int, deterministic: bool = False
    ) -> int:
        """Count prime numbers in a range.

        Args:
            start: Start of range (inclusive).
            end: End of range (inclusive).
            deterministic: Use deterministic test if True.

        Returns:
            Number of primes in the range.

        Raises:
            ValueError: If start > end or start < 2.
        """
        if start > end:
            raise ValueError("start must be <= end")
        if start < 2:
            raise ValueError("start must be >= 2")

        test_func = (
            self.is_prime_deterministic
            if deterministic
            else self.is_prime_probabilistic
        )

        count = 0
        if start == 2:
            count += 1
            start = 3

        if start % 2 == 0:
            start += 1

        for n in range(start, end + 1, 2):
            if test_func(n):
                count += 1

        return count


def main() -> None:
    """Main function to run the Miller-Rabin CLI interface."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Miller-Rabin primality test with deterministic variant"
    )
    parser.add_argument(
        "number",
        type=int,
        nargs="?",
        help="Number to test for primality",
    )
    parser.add_argument(
        "--test",
        type=int,
        help="Number to test for primality",
    )
    parser.add_argument(
        "--deterministic",
        action="store_true",
        help="Use deterministic variant",
    )
    parser.add_argument(
        "--probabilistic",
        action="store_true",
        help="Use probabilistic variant (default)",
    )
    parser.add_argument(
        "--rounds",
        type=int,
        default=10,
        help="Number of rounds for probabilistic test (default: 10)",
    )
    parser.add_argument(
        "--next-prime",
        type=int,
        help="Find next prime after given number",
    )
    parser.add_argument(
        "--prev-prime",
        type=int,
        help="Find previous prime before given number",
    )
    parser.add_argument(
        "--generate",
        type=int,
        help="Generate random prime with specified number of bits",
    )
    parser.add_argument(
        "--count",
        type=str,
        help="Count primes in range (format: start,end)",
    )

    args = parser.parse_args()

    try:
        mr = MillerRabin()

        if args.test is not None:
            n = args.test
            if args.deterministic:
                is_prime = mr.is_prime_deterministic(n)
                method = "deterministic"
            else:
                is_prime = mr.is_prime_probabilistic(n, k=args.rounds)
                method = f"probabilistic (k={args.rounds})"

            print(f"Testing {n} using {method} Miller-Rabin test")
            if is_prime:
                print(f"{n} is prime")
            else:
                print(f"{n} is composite")

        elif args.next_prime is not None:
            n = args.next_prime
            next_p = mr.find_next_prime(n, deterministic=args.deterministic)
            method = "deterministic" if args.deterministic else "probabilistic"
            print(f"Next prime after {n} (using {method} test): {next_p}")

        elif args.prev_prime is not None:
            n = args.prev_prime
            prev_p = mr.find_previous_prime(n, deterministic=args.deterministic)
            method = "deterministic" if args.deterministic else "probabilistic"
            print(f"Previous prime before {n} (using {method} test): {prev_p}")

        elif args.generate is not None:
            bits = args.generate
            prime = mr.generate_prime(bits, deterministic=args.deterministic)
            method = "deterministic" if args.deterministic else "probabilistic"
            print(f"Generated {bits}-bit prime (using {method} test): {prime}")

        elif args.count is not None:
            try:
                parts = args.count.split(",")
                if len(parts) != 2:
                    raise ValueError("Format: start,end")
                start = int(parts[0].strip())
                end = int(parts[1].strip())
            except (ValueError, IndexError) as e:
                logger.error(f"Invalid range format: {e}")
                sys.exit(1)

            count = mr.count_primes_in_range(
                start, end, deterministic=args.deterministic
            )
            method = "deterministic" if args.deterministic else "probabilistic"
            print(
                f"Number of primes in [{start}, {end}] "
                f"(using {method} test): {count}"
            )

        elif args.number is not None:
            n = args.number
            if args.deterministic:
                is_prime = mr.is_prime_deterministic(n)
                method = "deterministic"
            else:
                is_prime = mr.is_prime_probabilistic(n, k=args.rounds)
                method = f"probabilistic (k={args.rounds})"

            print(f"Testing {n} using {method} Miller-Rabin test")
            if is_prime:
                print(f"{n} is prime")
            else:
                print(f"{n} is composite")

        else:
            print("Miller-Rabin Primality Test")
            print("Use --help to see available options")
            print("\nExamples:")
            print("  python src/main.py 97")
            print("  python src/main.py --test 97 --deterministic")
            print("  python src/main.py --next-prime 100")
            print("  python src/main.py --generate 32")

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
