"""Character Frequency Analyzer - Count character occurrences.

This module provides functionality to count occurrences of each character in
a string using dictionary data structure with frequency analysis.
"""

import logging
import logging.handlers
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Optional

import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class CharacterFrequencyAnalyzer:
    """Analyzes character frequency in strings using dictionary data structure."""

    def __init__(self, config_path: str = "config.yaml") -> None:
        """Initialize CharacterFrequencyAnalyzer with configuration.

        Args:
            config_path: Path to configuration YAML file.

        Raises:
            FileNotFoundError: If config file doesn't exist.
            yaml.YAMLError: If config file is invalid YAML.
        """
        self.config = self._load_config(config_path)
        self._setup_logging()
        self.frequency_data: Dict[str, int] = {}
        self.analysis_stats: Dict[str, any] = {}

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

    def count_characters_dict(self, text: str) -> Dict[str, int]:
        """Count character occurrences using dictionary.

        Args:
            text: String to analyze.

        Returns:
            Dictionary mapping characters to their counts.
        """
        logger.info(f"Counting characters in string of length {len(text)}")
        frequency = {}

        for char in text:
            if char in frequency:
                frequency[char] += 1
            else:
                frequency[char] = 1
            logger.debug(f"Character '{char}': count = {frequency[char]}")

        self.frequency_data = frequency
        self._update_analysis_stats(text, frequency)

        logger.info(
            f"Found {len(frequency)} unique characters, "
            f"total characters: {len(text)}"
        )

        return frequency

    def count_characters_defaultdict(self, text: str) -> Dict[str, int]:
        """Count character occurrences using defaultdict.

        Args:
            text: String to analyze.

        Returns:
            Dictionary mapping characters to their counts.
        """
        logger.info(
            f"Counting characters using defaultdict in string of length {len(text)}"
        )
        frequency = defaultdict(int)

        for char in text:
            frequency[char] += 1
            logger.debug(f"Character '{char}': count = {frequency[char]}")

        self.frequency_data = dict(frequency)
        self._update_analysis_stats(text, self.frequency_data)

        return self.frequency_data

    def count_characters_counter(self, text: str) -> Dict[str, int]:
        """Count character occurrences using Counter.

        Args:
            text: String to analyze.

        Returns:
            Dictionary mapping characters to their counts.
        """
        logger.info(
            f"Counting characters using Counter in string of length {len(text)}"
        )
        frequency = dict(Counter(text))

        self.frequency_data = frequency
        self._update_analysis_stats(text, frequency)

        logger.info(
            f"Found {len(frequency)} unique characters using Counter"
        )

        return frequency

    def _update_analysis_stats(
        self, text: str, frequency: Dict[str, int]
    ) -> None:
        """Update analysis statistics.

        Args:
            text: Original text string.
            frequency: Character frequency dictionary.
        """
        total_chars = len(text)
        unique_chars = len(frequency)

        most_common = max(frequency.items(), key=lambda x: x[1]) if frequency else None
        least_common = min(frequency.items(), key=lambda x: x[1]) if frequency else None

        self.analysis_stats = {
            "total_characters": total_chars,
            "unique_characters": unique_chars,
            "most_common": most_common,
            "least_common": least_common,
            "average_frequency": total_chars / unique_chars if unique_chars > 0 else 0,
        }

    def get_frequency_analysis(self) -> Dict[str, any]:
        """Get detailed frequency analysis.

        Returns:
            Dictionary containing analysis data.
        """
        if not self.frequency_data:
            return {}

        sorted_by_frequency = sorted(
            self.frequency_data.items(), key=lambda x: x[1], reverse=True
        )

        analysis = self.analysis_stats.copy()
        analysis["frequency_distribution"] = sorted_by_frequency
        analysis["character_percentages"] = {
            char: (count / analysis["total_characters"]) * 100
            for char, count in self.frequency_data.items()
        }

        return analysis

    def get_top_characters(self, n: int = 10) -> List[tuple]:
        """Get top N most frequent characters.

        Args:
            n: Number of top characters to return.

        Returns:
            List of tuples (character, count) sorted by frequency.
        """
        if not self.frequency_data:
            return []

        sorted_chars = sorted(
            self.frequency_data.items(), key=lambda x: x[1], reverse=True
        )
        return sorted_chars[:n]

    def get_character_info(self, char: str) -> Optional[Dict[str, any]]:
        """Get detailed information about a specific character.

        Args:
            char: Character to get information for.

        Returns:
            Dictionary with character information or None if not found.
        """
        if not self.frequency_data or char not in self.frequency_data:
            return None

        count = self.frequency_data[char]
        total = self.analysis_stats.get("total_characters", 0)
        percentage = (count / total * 100) if total > 0 else 0

        return {
            "character": char,
            "count": count,
            "percentage": percentage,
            "unicode_code": ord(char),
            "is_whitespace": char.isspace(),
            "is_alphanumeric": char.isalnum(),
            "is_alpha": char.isalpha(),
            "is_digit": char.isdigit(),
        }

    def generate_report(self, output_path: Optional[str] = None) -> str:
        """Generate frequency analysis report.

        Args:
            output_path: Optional path to save report file.

        Returns:
            Report content as string.
        """
        if not self.frequency_data:
            return "No frequency data available. Run count_characters() first."

        analysis = self.get_frequency_analysis()

        report_lines = [
            "=" * 80,
            "CHARACTER FREQUENCY ANALYSIS REPORT",
            "=" * 80,
            "",
            "SUMMARY",
            "-" * 80,
            f"Total characters: {analysis['total_characters']:,}",
            f"Unique characters: {analysis['unique_characters']:,}",
            f"Average frequency: {analysis['average_frequency']:.2f}",
            "",
        ]

        if analysis.get("most_common"):
            most_char, most_count = analysis["most_common"]
            report_lines.append(f"Most common: '{most_char}' ({most_count} occurrences)")

        if analysis.get("least_common"):
            least_char, least_count = analysis["least_common"]
            report_lines.append(f"Least common: '{least_char}' ({least_count} occurrences)")

        report_lines.extend([
            "",
            "TOP 10 MOST FREQUENT CHARACTERS",
            "-" * 80,
        ])

        top_chars = self.get_top_characters(10)
        for idx, (char, count) in enumerate(top_chars, 1):
            percentage = analysis["character_percentages"].get(char, 0)
            char_display = repr(char) if char in ['\n', '\t', ' '] else char
            report_lines.append(
                f"{idx:2d}. '{char_display}': {count:6,} occurrences ({percentage:5.2f}%)"
            )

        report_lines.extend([
            "",
            "COMPLETE FREQUENCY DISTRIBUTION",
            "-" * 80,
        ])

        for char, count in analysis["frequency_distribution"]:
            percentage = analysis["character_percentages"].get(char, 0)
            char_display = repr(char) if char in ['\n', '\t', ' '] else char
            report_lines.append(
                f"'{char_display}': {count:6,} ({percentage:5.2f}%)"
            )

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
    import argparse

    parser = argparse.ArgumentParser(
        description="Count character occurrences with frequency analysis"
    )
    parser.add_argument(
        "text",
        help="String to analyze",
    )
    parser.add_argument(
        "-c",
        "--config",
        default="config.yaml",
        help="Path to configuration file (default: config.yaml)",
    )
    parser.add_argument(
        "-m",
        "--method",
        choices=["dict", "defaultdict", "counter", "all"],
        default="dict",
        help="Counting method (default: dict)",
    )
    parser.add_argument(
        "-t",
        "--top",
        type=int,
        help="Show top N most frequent characters",
    )
    parser.add_argument(
        "-s",
        "--search",
        help="Get detailed info for specific character",
    )
    parser.add_argument(
        "-r",
        "--report",
        help="Output path for analysis report",
    )

    args = parser.parse_args()

    try:
        analyzer = CharacterFrequencyAnalyzer(config_path=args.config)

        if args.method == "all":
            print("\nComparing all methods:")
            print("-" * 60)
            dict_result = analyzer.count_characters_dict(args.text)
            print(f"Dictionary method: {len(dict_result)} unique characters")

            defaultdict_result = analyzer.count_characters_defaultdict(args.text)
            print(f"DefaultDict method: {len(defaultdict_result)} unique characters")

            counter_result = analyzer.count_characters_counter(args.text)
            print(f"Counter method: {len(counter_result)} unique characters")

        elif args.method == "dict":
            frequency = analyzer.count_characters_dict(args.text)
        elif args.method == "defaultdict":
            frequency = analyzer.count_characters_defaultdict(args.text)
        elif args.method == "counter":
            frequency = analyzer.count_characters_counter(args.text)

        if args.method != "all":
            print(f"\nCharacter Frequency Analysis:")
            print(f"Total characters: {len(args.text)}")
            print(f"Unique characters: {len(frequency)}")
            print("\nFrequency distribution:")

            sorted_freq = sorted(
                frequency.items(), key=lambda x: x[1], reverse=True
            )
            for char, count in sorted_freq[:20]:
                char_display = repr(char) if char in ['\n', '\t', ' '] else char
                print(f"  '{char_display}': {count}")

            if len(sorted_freq) > 20:
                print(f"  ... and {len(sorted_freq) - 20} more")

        if args.top:
            top_chars = analyzer.get_top_characters(args.top)
            print(f"\nTop {args.top} most frequent characters:")
            for idx, (char, count) in enumerate(top_chars, 1):
                char_display = repr(char) if char in ['\n', '\t', ' '] else char
                print(f"  {idx}. '{char_display}': {count}")

        if args.search:
            info = analyzer.get_character_info(args.search)
            if info:
                print(f"\nCharacter '{args.search}' information:")
                print(f"  Count: {info['count']}")
                print(f"  Percentage: {info['percentage']:.2f}%")
                print(f"  Unicode code: U+{info['unicode_code']:04X}")
            else:
                print(f"Character '{args.search}' not found in text")

        if args.report:
            report = analyzer.generate_report(output_path=args.report)
            print(f"\nReport saved to {args.report}")

    except Exception as e:
        logger.error(f"Error during execution: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
