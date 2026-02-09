"""Anagram Finder - Character Frequency and Hash-Based Grouping.

This module provides an anagram finder that uses character frequency
comparison and hash-based grouping to efficiently find all anagrams in a
list of strings. It groups strings that are anagrams of each other.
"""

import argparse
import logging
import logging.handlers
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class AnagramFinder:
    """Anagram finder using character frequency and hash-based grouping."""

    def __init__(self, config_path: str = "config.yaml") -> None:
        """Initialize finder with configuration.

        Args:
            config_path: Path to configuration YAML file.

        Raises:
            FileNotFoundError: If config file doesn't exist.
            yaml.YAMLError: If config file is invalid YAML.
        """
        self.config = self._load_config(config_path)
        self._setup_logging()

    def _load_config(self, config_path: str) -> dict:
        """Load configuration from YAML file.

        Args:
            config_path: Path to configuration file.

        Returns:
            Dictionary containing configuration settings.

        Raises:
            FileNotFoundError: If config file doesn't exist.
            yaml.YAMLError: If config file is invalid YAML.
        """
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
            if not config:
                raise ValueError("Configuration file is empty")
            return config
        except FileNotFoundError:
            logger.error(f"Configuration file not found: {config_path}")
            raise
        except yaml.YAMLError as e:
            logger.error(f"Invalid YAML in configuration file: {e}")
            raise

    def _setup_logging(self) -> None:
        """Configure logging based on configuration settings."""
        log_level = self.config.get("logging", {}).get("level", "INFO")
        log_file = self.config.get("logging", {}).get("file", "logs/app.log")
        log_format = (
            "%(asctime)s - %(name)s - %(levelname)s - "
            "%(message)s"
        )

        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        logging.basicConfig(
            level=getattr(logging, log_level.upper()),
            format=log_format,
            handlers=[
                logging.handlers.RotatingFileHandler(
                    log_file, maxBytes=10485760, backupCount=5
                ),
                logging.StreamHandler(),
            ],
        )

    def _get_character_frequency(self, word: str) -> Counter:
        """Get character frequency of a word.

        Args:
            word: Input string.

        Returns:
            Counter object with character frequencies.
        """
        return Counter(word.lower())

    def _get_frequency_hash(self, word: str) -> str:
        """Generate hash key from character frequency.

        Creates a hash key by sorting characters and their frequencies.
        This ensures anagrams produce the same hash.

        Args:
            word: Input string.

        Returns:
            Hash string representing character frequency pattern.
        """
        freq = self._get_character_frequency(word)
        # Sort characters and create hash string
        sorted_chars = sorted(freq.items())
        hash_str = "".join(f"{char}{count}" for char, count in sorted_chars)
        return hash_str

    def _are_anagrams(self, word1: str, word2: str) -> bool:
        """Check if two words are anagrams using character frequency.

        Args:
            word1: First string.
            word2: Second string.

        Returns:
            True if words are anagrams, False otherwise.
        """
        if len(word1) != len(word2):
            return False

        freq1 = self._get_character_frequency(word1)
        freq2 = self._get_character_frequency(word2)

        return freq1 == freq2

    def find_anagrams(
        self, words: List[str], case_sensitive: bool = False
    ) -> Dict[str, List[str]]:
        """Find all anagrams in a list using hash-based grouping.

        Groups words that are anagrams of each other using hash-based
        grouping. Words with the same character frequency hash are grouped
        together.

        Args:
            words: List of strings to analyze.
            case_sensitive: If True, consider case when comparing.

        Returns:
            Dictionary mapping hash keys to lists of anagram groups.
            Each group contains words that are anagrams of each other.

        Example:
            >>> finder = AnagramFinder()
            >>> result = finder.find_anagrams(["listen", "silent", "enlist"])
            >>> # Returns grouped anagrams
        """
        logger.info(f"Finding anagrams in {len(words)} words")

        if not words:
            logger.warning("Empty word list provided")
            return {}

        # Hash-based grouping: group words by their frequency hash
        hash_groups: Dict[str, List[str]] = defaultdict(list)

        for word in words:
            if not word:
                continue

            # Normalize word based on case sensitivity
            normalized_word = word if case_sensitive else word.lower()
            original_word = word

            # Generate hash from character frequency
            hash_key = self._get_frequency_hash(normalized_word)

            # Group words with same hash together
            hash_groups[hash_key].append(original_word)

            logger.debug(
                f"Word '{original_word}' -> hash '{hash_key}' -> "
                f"group size: {len(hash_groups[hash_key])}"
            )

        # Filter out groups with only one word (no anagrams)
        anagram_groups = {
            hash_key: group
            for hash_key, group in hash_groups.items()
            if len(group) > 1
        }

        logger.info(
            f"Found {len(anagram_groups)} anagram groups with "
            f"{sum(len(group) for group in anagram_groups.values())} words"
        )

        return anagram_groups

    def find_anagrams_detailed(
        self, words: List[str], case_sensitive: bool = False
    ) -> Dict[str, Dict[str, any]]:
        """Find anagrams with detailed analysis.

        Args:
            words: List of strings to analyze.
            case_sensitive: If True, consider case when comparing.

        Returns:
            Dictionary with detailed anagram information including:
                - groups: Anagram groups
                - statistics: Analysis statistics
                - character_frequencies: Character frequency data
        """
        logger.info(f"Finding anagrams with detailed analysis")

        anagram_groups = self.find_anagrams(words, case_sensitive)

        # Calculate statistics
        total_groups = len(anagram_groups)
        total_words_in_groups = sum(len(group) for group in anagram_groups.values())
        largest_group_size = max(
            (len(group) for group in anagram_groups.values()), default=0
        )
        largest_group = [
            group
            for group in anagram_groups.values()
            if len(group) == largest_group_size
        ][0] if anagram_groups else []

        # Character frequency analysis
        character_frequencies = {}
        for word in words:
            if word:
                freq = self._get_character_frequency(word)
                character_frequencies[word] = dict(freq)

        result = {
            "groups": anagram_groups,
            "statistics": {
                "total_words": len(words),
                "total_anagram_groups": total_groups,
                "total_words_in_groups": total_words_in_groups,
                "words_without_anagrams": len(words) - total_words_in_groups,
                "largest_group_size": largest_group_size,
                "largest_group": largest_group,
            },
            "character_frequencies": character_frequencies,
        }

        logger.info(f"Detailed analysis complete: {result['statistics']}")
        return result

    def find_anagrams_for_word(
        self, target_word: str, word_list: List[str]
    ) -> List[str]:
        """Find all anagrams of a specific word in a list.

        Args:
            target_word: Word to find anagrams for.
            word_list: List of words to search in.

        Returns:
            List of words that are anagrams of target_word.
        """
        logger.info(f"Finding anagrams for '{target_word}'")

        anagrams = [
            word
            for word in word_list
            if word != target_word and self._are_anagrams(target_word, word)
        ]

        logger.info(f"Found {len(anagrams)} anagrams for '{target_word}'")
        return anagrams

    def get_character_frequency_analysis(
        self, word: str
    ) -> Dict[str, any]:
        """Get detailed character frequency analysis for a word.

        Args:
            word: Input string.

        Returns:
            Dictionary with frequency analysis including:
                - frequencies: Character frequency dictionary
                - sorted_frequencies: Sorted frequency list
                - unique_characters: Number of unique characters
                - total_characters: Total character count
        """
        freq = self._get_character_frequency(word)
        sorted_freq = sorted(freq.items(), key=lambda x: (-x[1], x[0]))

        return {
            "word": word,
            "frequencies": dict(freq),
            "sorted_frequencies": sorted_freq,
            "unique_characters": len(freq),
            "total_characters": len(word),
            "hash_key": self._get_frequency_hash(word),
        }

    def generate_report(
        self, result: Dict[str, Dict[str, any]], output_path: Optional[str] = None
    ) -> str:
        """Generate detailed anagram analysis report.

        Args:
            result: Result dictionary from find_anagrams_detailed.
            output_path: Optional path to save report file.

        Returns:
            Report content as string.
        """
        groups = result["groups"]
        stats = result["statistics"]

        report_lines = [
            "=" * 80,
            "ANAGRAM FINDER REPORT",
            "=" * 80,
            "",
            "STATISTICS",
            "-" * 80,
            f"Total words analyzed: {stats['total_words']}",
            f"Total anagram groups: {stats['total_anagram_groups']}",
            f"Words in anagram groups: {stats['total_words_in_groups']}",
            f"Words without anagrams: {stats['words_without_anagrams']}",
            f"Largest group size: {stats['largest_group_size']}",
            f"Largest group: {stats['largest_group']}",
            "",
            "ANAGRAM GROUPS",
            "-" * 80,
            "",
        ]

        if groups:
            for idx, (hash_key, group) in enumerate(groups.items(), 1):
                report_lines.append(f"Group {idx} (hash: {hash_key[:20]}...):")
                report_lines.append(f"  Words: {', '.join(group)}")
                report_lines.append(f"  Count: {len(group)}")
                report_lines.append("")
        else:
            report_lines.append("No anagram groups found.")
            report_lines.append("")

        report_lines.extend([
            "ALGORITHM DETAILS",
            "-" * 80,
            "Method: Character Frequency Comparison + Hash-Based Grouping",
            "",
            "Character Frequency Comparison:",
            "  - Count frequency of each character in each word",
            "  - Normalize to lowercase for case-insensitive comparison",
            "  - Two words are anagrams if they have same character frequencies",
            "",
            "Hash-Based Grouping:",
            "  - Generate hash key from sorted character frequencies",
            "  - Group words with same hash key together",
            "  - Hash key format: sorted characters with their counts",
            "",
            "ALGORITHM COMPLEXITY",
            "-" * 80,
            "Time Complexity: O(n * m) where:",
            "  - n = number of words",
            "  - m = average word length",
            "Space Complexity: O(n * m) for storing groups and frequencies",
            "",
            "PROPERTIES",
            "-" * 80,
            "- Case-insensitive by default (configurable)",
            "- Handles empty strings gracefully",
            "- Groups words efficiently using hash-based approach",
            "- Provides detailed frequency analysis",
        ])

        report_content = "\n".join(report_lines)

        if output_path:
            try:
                output_file = Path(output_path)
                output_file.parent.mkdir(parents=True, exist_ok=True)
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(report_content)
                logger.info(f"Report saved to {output_path}")
            except (IOError, PermissionError) as e:
                logger.error(f"Failed to save report: {e}")
                raise

        return report_content


def main() -> None:
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Find anagrams using character frequency and hash-based grouping"
    )
    parser.add_argument(
        "words",
        type=str,
        nargs="*",
        help="Words to analyze (space-separated)",
    )
    parser.add_argument(
        "-c",
        "--config",
        default="config.yaml",
        help="Path to configuration file (default: config.yaml)",
    )
    parser.add_argument(
        "-f",
        "--file",
        help="Path to file containing words (one per line)",
    )
    parser.add_argument(
        "-d",
        "--detailed",
        action="store_true",
        help="Show detailed analysis with statistics",
    )
    parser.add_argument(
        "-s",
        "--case-sensitive",
        action="store_true",
        help="Consider case when comparing words",
    )
    parser.add_argument(
        "-t",
        "--target",
        help="Find anagrams for a specific target word",
    )
    parser.add_argument(
        "-r",
        "--report",
        help="Output path for analysis report",
    )
    parser.add_argument(
        "--frequency",
        help="Show character frequency for a specific word",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run demonstration with example words",
    )

    args = parser.parse_args()

    try:
        finder = AnagramFinder(config_path=args.config)

        # Load words from file or arguments
        words = []
        if args.file:
            try:
                with open(args.file, "r", encoding="utf-8") as f:
                    words = [line.strip() for line in f if line.strip()]
                logger.info(f"Loaded {len(words)} words from file: {args.file}")
            except FileNotFoundError:
                logger.error(f"File not found: {args.file}")
                print(f"Error: File not found: {args.file}")
                return
        elif args.words:
            words = args.words
        elif args.demo or not args.target:
            # Run demonstration
            print("\n=== Anagram Finder Demonstration ===\n")

            examples = [
                ["listen", "silent", "enlist", "inlets", "tinsel"],
                ["evil", "vile", "live", "veil", "levi"],
                ["cat", "act", "tac", "dog", "god", "odg"],
                ["race", "care", "acre", "acer", "bare", "bear"],
            ]

            for example in examples:
                print(f"Words: {example}")
                if args.detailed:
                    result = finder.find_anagrams_detailed(
                        example, case_sensitive=args.case_sensitive
                    )
                    print(f"\nAnagram Groups: {len(result['groups'])}")
                    for hash_key, group in result["groups"].items():
                        print(f"  {group}")
                    print(f"\nStatistics:")
                    stats = result["statistics"]
                    print(f"  Total words: {stats['total_words']}")
                    print(f"  Anagram groups: {stats['total_anagram_groups']}")
                    print(f"  Largest group: {stats['largest_group']}")
                else:
                    groups = finder.find_anagrams(
                        example, case_sensitive=args.case_sensitive
                    )
                    print(f"Anagram Groups: {len(groups)}")
                    for group in groups.values():
                        print(f"  {group}")
                print()

        # Handle specific word frequency analysis
        if args.frequency:
            analysis = finder.get_character_frequency_analysis(args.frequency)
            print(f"\nCharacter Frequency Analysis for '{args.frequency}':")
            print(f"  Total characters: {analysis['total_characters']}")
            print(f"  Unique characters: {analysis['unique_characters']}")
            print(f"  Hash key: {analysis['hash_key']}")
            print(f"  Frequencies: {analysis['frequencies']}")
            print(f"  Sorted frequencies: {analysis['sorted_frequencies']}")

        # Handle target word anagram search
        if args.target:
            if not words:
                print("Error: Word list required for target search")
                return
            anagrams = finder.find_anagrams_for_word(args.target, words)
            print(f"\nAnagrams of '{args.target}':")
            if anagrams:
                print(f"  {anagrams}")
            else:
                print("  No anagrams found")

        # Handle standard anagram finding
        if words and not args.target and not args.frequency:
            if args.detailed:
                result = finder.find_anagrams_detailed(
                    words, case_sensitive=args.case_sensitive
                )
                print(f"\nAnagram Analysis:")
                print(f"  Total words: {result['statistics']['total_words']}")
                print(f"  Anagram groups: {result['statistics']['total_anagram_groups']}")
                print(f"  Words in groups: {result['statistics']['total_words_in_groups']}")
                print(f"\nAnagram Groups:")
                for hash_key, group in result["groups"].items():
                    print(f"  {group}")

                if args.report:
                    report = finder.generate_report(result, output_path=args.report)
                    print(f"\nReport saved to {args.report}")
            else:
                groups = finder.find_anagrams(
                    words, case_sensitive=args.case_sensitive
                )
                print(f"\nFound {len(groups)} anagram groups:")
                for group in groups.values():
                    print(f"  {group}")

                if args.report:
                    result = finder.find_anagrams_detailed(
                        words, case_sensitive=args.case_sensitive
                    )
                    report = finder.generate_report(result, output_path=args.report)
                    print(f"\nReport saved to {args.report}")

    except Exception as e:
        logger.error(f"Error during execution: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
