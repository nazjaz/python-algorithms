"""Rolling hash implementation with multiple moduli for robust string matching.

This module implements a polynomial rolling hash using multiple prime moduli
to reduce hash collisions and provide robust string matching and substring
hashing capabilities.
"""

import logging
import sys
from typing import List, Optional, Tuple

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class RollingHash:
    """Rolling hash with multiple moduli for robust string hashing.

    Uses polynomial rolling hash with multiple prime moduli to minimize
    hash collisions and provide reliable string matching.
    """

    DEFAULT_MODULI = [10**9 + 7, 10**9 + 9, 10**9 + 21]
    DEFAULT_BASE = 256

    def __init__(
        self,
        moduli: Optional[List[int]] = None,
        base: int = DEFAULT_BASE,
    ) -> None:
        """Initialize rolling hash with specified moduli and base.

        Args:
            moduli: List of prime moduli to use. Defaults to large primes.
            base: Base for polynomial hash. Should be larger than alphabet size.

        Raises:
            ValueError: If moduli list is empty or base is invalid.
        """
        if moduli is None:
            moduli = self.DEFAULT_MODULI.copy()

        if not moduli:
            raise ValueError("At least one modulus is required")

        if base < 2:
            raise ValueError("Base must be at least 2")

        self.moduli: List[int] = moduli
        self.base: int = base
        self.num_moduli: int = len(moduli)

        self.powers: List[List[int]] = []
        for _ in range(self.num_moduli):
            self.powers.append([1])

    def _compute_powers(self, length: int) -> None:
        """Precompute powers of base modulo each modulus.

        Args:
            length: Maximum length to precompute powers for.
        """
        for i in range(self.num_moduli):
            while len(self.powers[i]) <= length:
                last_power = self.powers[i][-1]
                next_power = (last_power * self.base) % self.moduli[i]
                self.powers[i].append(next_power)

    def hash_string(self, text: str) -> Tuple[int, ...]:
        """Compute hash of a string using all moduli.

        Args:
            text: String to hash.

        Returns:
            Tuple of hash values, one for each modulus.
        """
        if not text:
            return tuple(0 for _ in range(self.num_moduli))

        self._compute_powers(len(text) - 1)

        hashes = [0] * self.num_moduli

        for char in text:
            char_value = ord(char)
            for i in range(self.num_moduli):
                hashes[i] = (hashes[i] * self.base + char_value) % self.moduli[i]

        return tuple(hashes)

    def hash_substring(
        self, text: str, start: int, length: int
    ) -> Tuple[int, ...]:
        """Compute hash of a substring using all moduli.

        Args:
            text: Source string.
            start: Starting index of substring.
            length: Length of substring.

        Returns:
            Tuple of hash values for the substring.

        Raises:
            IndexError: If start or length is out of bounds.
        """
        if start < 0 or start + length > len(text):
            raise IndexError(
                f"Substring indices out of bounds: "
                f"start={start}, length={length}, text_length={len(text)}"
            )

        if length == 0:
            return tuple(0 for _ in range(self.num_moduli))

        self._compute_powers(length - 1)

        hashes = [0] * self.num_moduli

        for i in range(start, start + length):
            char_value = ord(text[i])
            for j in range(self.num_moduli):
                hashes[j] = (
                    hashes[j] * self.base + char_value
                ) % self.moduli[j]

        return tuple(hashes)

    def build_prefix_hashes(self, text: str) -> List[List[int]]:
        """Build prefix hash array for efficient substring queries.

        Args:
            text: String to build prefix hashes for.

        Returns:
            List of lists, where each inner list contains prefix hashes
            for one modulus.
        """
        if not text:
            return [[0] for _ in range(self.num_moduli)]

        self._compute_powers(len(text) - 1)

        prefix_hashes = [[0] for _ in range(self.num_moduli)]

        for char in text:
            char_value = ord(char)
            for i in range(self.num_moduli):
                new_hash = (
                    prefix_hashes[i][-1] * self.base + char_value
                ) % self.moduli[i]
                prefix_hashes[i].append(new_hash)

        return prefix_hashes

    def get_substring_hash_from_prefix(
        self,
        prefix_hashes: List[List[int]],
        start: int,
        length: int,
    ) -> Tuple[int, ...]:
        """Get substring hash from prefix hash array.

        Uses the formula: hash(s[l:r]) = (prefix[r] - prefix[l] * base^(r-l)) mod m

        Args:
            prefix_hashes: Prefix hash array from build_prefix_hashes.
            start: Starting index of substring.
            length: Length of substring.

        Returns:
            Tuple of hash values for the substring.

        Raises:
            IndexError: If indices are out of bounds.
            ValueError: If prefix_hashes structure is invalid.
        """
        if not prefix_hashes or len(prefix_hashes) != self.num_moduli:
            raise ValueError("Invalid prefix_hashes structure")

        text_length = len(prefix_hashes[0]) - 1

        if start < 0 or start + length > text_length:
            raise IndexError(
                f"Substring indices out of bounds: "
                f"start={start}, length={length}, text_length={text_length}"
            )

        if length == 0:
            return tuple(0 for _ in range(self.num_moduli))

        self._compute_powers(length)

        result_hashes = []

        for i in range(self.num_moduli):
            end = start + length
            prefix_start = prefix_hashes[i][start]
            prefix_end = prefix_hashes[i][end]
            power = self.powers[i][length]

            hash_value = (
                prefix_end - prefix_start * power
            ) % self.moduli[i]

            if hash_value < 0:
                hash_value += self.moduli[i]

            result_hashes.append(hash_value)

        return tuple(result_hashes)

    def find_pattern(
        self, text: str, pattern: str
    ) -> List[int]:
        """Find all occurrences of pattern in text using rolling hash.

        Args:
            text: Text to search in.
            pattern: Pattern to search for.

        Returns:
            List of starting indices where pattern occurs.
        """
        if not pattern:
            return list(range(len(text) + 1))

        if len(pattern) > len(text):
            return []

        pattern_hash = self.hash_string(pattern)
        occurrences = []

        text_hash = self.hash_substring(text, 0, len(pattern))

        if text_hash == pattern_hash and text[:len(pattern)] == pattern:
            occurrences.append(0)

        self._compute_powers(len(pattern) - 1)

        for i in range(1, len(text) - len(pattern) + 1):
            text_hash = self._roll_hash(
                text_hash, text[i - 1], text[i + len(pattern) - 1], len(pattern)
            )

            if text_hash == pattern_hash:
                if text[i : i + len(pattern)] == pattern:
                    occurrences.append(i)

        return occurrences

    def _roll_hash(
        self,
        current_hash: Tuple[int, ...],
        remove_char: str,
        add_char: str,
        pattern_length: int,
    ) -> Tuple[int, ...]:
        """Roll the hash by removing one character and adding another.

        Args:
            current_hash: Current hash tuple.
            remove_char: Character being removed from the left.
            add_char: Character being added to the right.
            pattern_length: Length of the pattern/window.

        Returns:
            New hash tuple after rolling.
        """
        new_hash = list(current_hash)
        remove_value = ord(remove_char)
        add_value = ord(add_char)

        for i in range(self.num_moduli):
            power = self.powers[i][pattern_length - 1]
            new_hash[i] = (
                (current_hash[i] - remove_value * power) * self.base + add_value
            ) % self.moduli[i]

            if new_hash[i] < 0:
                new_hash[i] += self.moduli[i]

        return tuple(new_hash)

    def compare_substrings(
        self,
        text1: str,
        start1: int,
        text2: str,
        start2: int,
        length: int,
    ) -> bool:
        """Compare two substrings using hashing.

        Args:
            text1: First text.
            start1: Starting index in first text.
            text2: Second text.
            start2: Starting index in second text.
            length: Length of substrings to compare.

        Returns:
            True if substrings are equal, False otherwise.

        Raises:
            IndexError: If indices are out of bounds.
        """
        hash1 = self.hash_substring(text1, start1, length)
        hash2 = self.hash_substring(text2, start2, length)

        if hash1 != hash2:
            return False

        return text1[start1 : start1 + length] == text2[start2 : start2 + length]

    def longest_common_prefix_hash(
        self, text1: str, start1: int, text2: str, start2: int
    ) -> int:
        """Find longest common prefix of two substrings using binary search.

        Args:
            text1: First text.
            start1: Starting index in first text.
            text2: Second text.
            start2: Starting index in second text.

        Returns:
            Length of longest common prefix.

        Raises:
            IndexError: If indices are out of bounds.
        """
        max_length = min(
            len(text1) - start1, len(text2) - start2
        )

        if max_length == 0:
            return 0

        left, right = 0, max_length
        result = 0

        while left <= right:
            mid = (left + right) // 2

            if self.compare_substrings(text1, start1, text2, start2, mid):
                result = mid
                left = mid + 1
            else:
                right = mid - 1

        return result


def main() -> None:
    """Main function to run the rolling hash CLI interface."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Rolling hash with multiple moduli for string matching"
    )
    parser.add_argument(
        "text",
        type=str,
        help="Input text string",
    )
    parser.add_argument(
        "--pattern",
        type=str,
        help="Pattern to search for in text",
    )
    parser.add_argument(
        "--hash",
        action="store_true",
        help="Compute and display hash of the text",
    )
    parser.add_argument(
        "--substring",
        type=str,
        help="Compute hash of substring in format 'start:length'",
    )
    parser.add_argument(
        "--compare",
        type=str,
        help="Compare substrings in format 'text2,start1,start2,length'",
    )
    parser.add_argument(
        "--moduli",
        type=str,
        help="Comma-separated list of moduli (default: large primes)",
    )
    parser.add_argument(
        "--base",
        type=int,
        default=256,
        help="Base for polynomial hash (default: 256)",
    )

    args = parser.parse_args()

    try:
        moduli = None
        if args.moduli:
            moduli = [int(m.strip()) for m in args.moduli.split(",")]

        rolling_hash = RollingHash(moduli=moduli, base=args.base)

        if args.hash:
            hashes = rolling_hash.hash_string(args.text)
            print(f"Hash values: {hashes}")
            print(f"Hash (combined): {hash(hashes)}")

        if args.pattern:
            occurrences = rolling_hash.find_pattern(args.text, args.pattern)
            if occurrences:
                print(
                    f"Pattern '{args.pattern}' found at positions: "
                    f"{occurrences}"
                )
                print(f"Total occurrences: {len(occurrences)}")
            else:
                print(f"Pattern '{args.pattern}' not found in text")

        if args.substring:
            try:
                start, length = map(int, args.substring.split(":"))
                substring = args.text[start : start + length]
                hashes = rolling_hash.hash_substring(args.text, start, length)
                print(
                    f"Substring '{substring}' (start={start}, length={length}): "
                    f"{hashes}"
                )
            except (ValueError, IndexError) as e:
                logger.error(f"Invalid substring format: {e}")
                sys.exit(1)

        if args.compare:
            try:
                parts = args.compare.split(",")
                if len(parts) != 4:
                    raise ValueError("Compare format: text2,start1,start2,length")
                text2, start1, start2, length = (
                    parts[0],
                    int(parts[1]),
                    int(parts[2]),
                    int(parts[3]),
                )
                are_equal = rolling_hash.compare_substrings(
                    args.text, start1, text2, start2, length
                )
                substr1 = args.text[start1 : start1 + length]
                substr2 = text2[start2 : start2 + length]
                print(
                    f"Substring 1: '{substr1}' (start={start1})"
                )
                print(
                    f"Substring 2: '{substr2}' (start={start2})"
                )
                print(f"Are equal: {are_equal}")
            except (ValueError, IndexError) as e:
                logger.error(f"Invalid compare format: {e}")
                sys.exit(1)

        if not any([args.hash, args.pattern, args.substring, args.compare]):
            hashes = rolling_hash.hash_string(args.text)
            print(f"Text: {args.text}")
            print(f"Hash values: {hashes}")
            print(f"Using moduli: {rolling_hash.moduli}")
            print(f"Using base: {rolling_hash.base}")

    except Exception as e:
        logger.error(f"Error processing: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
