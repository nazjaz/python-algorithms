"""Trie (Prefix Tree) Data Structure.

This module provides functionality to implement trie (prefix tree) data
structure for efficient string prefix matching and autocomplete operations.
A trie is a tree-like data structure that stores strings in a way that
allows efficient prefix searches.
"""

import logging
import logging.handlers
import time
from pathlib import Path
from typing import Dict, List, Optional

import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class TrieNode:
    """Node in the trie data structure."""

    def __init__(self) -> None:
        """Initialize TrieNode."""
        self.children: Dict[str, "TrieNode"] = {}
        self.is_end_of_word = False
        self.word_count = 0

    def __repr__(self) -> str:
        """String representation."""
        return f"TrieNode(children={len(self.children)}, is_end={self.is_end_of_word})"


class Trie:
    """Trie (Prefix Tree) data structure for efficient string operations."""

    def __init__(self, config_path: str = "config.yaml") -> None:
        """Initialize Trie with configuration.

        Args:
            config_path: Path to configuration YAML file.

        Raises:
            FileNotFoundError: If config file doesn't exist.
            yaml.YAMLError: If config file is invalid YAML.
        """
        self.root = TrieNode()
        self.total_words = 0
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

    def insert(self, word: str) -> None:
        """Insert word into trie.

        Args:
            word: Word to insert.
        """
        if not word:
            logger.warning("Attempted to insert empty word")
            return

        current = self.root
        logger.debug(f"Inserting word: {word}")

        for char in word:
            if char not in current.children:
                current.children[char] = TrieNode()
                logger.debug(f"  Created node for character '{char}'")
            current = current.children[char]
            current.word_count += 1

        if not current.is_end_of_word:
            current.is_end_of_word = True
            self.total_words += 1
            logger.debug(f"  Marked end of word, total words: {self.total_words}")

    def search(self, word: str) -> bool:
        """Search for exact word in trie.

        Args:
            word: Word to search for.

        Returns:
            True if word exists, False otherwise.
        """
        if not word:
            return False

        current = self.root
        logger.debug(f"Searching for word: {word}")

        for char in word:
            if char not in current.children:
                logger.debug(f"  Character '{char}' not found")
                return False
            current = current.children[char]

        result = current.is_end_of_word
        logger.debug(f"  Word found: {result}")
        return result

    def starts_with(self, prefix: str) -> bool:
        """Check if any word in trie starts with given prefix.

        Args:
            prefix: Prefix to check.

        Returns:
            True if prefix exists, False otherwise.
        """
        if not prefix:
            return True

        current = self.root
        logger.debug(f"Checking prefix: {prefix}")

        for char in prefix:
            if char not in current.children:
                logger.debug(f"  Prefix not found at character '{char}'")
                return False
            current = current.children[char]

        logger.debug(f"  Prefix found")
        return True

    def _collect_words(
        self, node: TrieNode, prefix: str, words: List[str], limit: Optional[int] = None
    ) -> None:
        """Collect all words starting from given node.

        Args:
            node: Current node to explore.
            prefix: Current prefix string.
            words: List to collect words.
            limit: Maximum number of words to collect (None for all).
        """
        if limit is not None and len(words) >= limit:
            return

        if node.is_end_of_word:
            words.append(prefix)
            logger.debug(f"    Collected word: {prefix}")

        for char, child_node in sorted(node.children.items()):
            if limit is not None and len(words) >= limit:
                break
            self._collect_words(child_node, prefix + char, words, limit)

    def autocomplete(
        self, prefix: str, limit: Optional[int] = None
    ) -> List[str]:
        """Get autocomplete suggestions for given prefix.

        Args:
            prefix: Prefix to autocomplete.
            limit: Maximum number of suggestions (None for all).

        Returns:
            List of words that start with the prefix.
        """
        if not prefix:
            words: List[str] = []
            self._collect_words(self.root, "", words, limit)
            logger.info(f"Autocomplete (empty prefix): {len(words)} words")
            return words

        current = self.root
        logger.info(f"Autocomplete for prefix: '{prefix}'")

        # Navigate to prefix node
        for char in prefix:
            if char not in current.children:
                logger.debug(f"  Prefix '{prefix}' not found")
                return []
            current = current.children[char]

        # Collect all words from this node
        words: List[str] = []
        self._collect_words(current, prefix, words, limit)

        logger.info(f"  Found {len(words)} suggestions")
        return words

    def delete(self, word: str) -> bool:
        """Delete word from trie.

        Args:
            word: Word to delete.

        Returns:
            True if word was deleted, False if word doesn't exist.
        """
        if not word:
            return False

        def _delete_helper(node: TrieNode, word: str, index: int) -> bool:
            """Recursive helper to delete word."""
            if index == len(word):
                if not node.is_end_of_word:
                    return False
                node.is_end_of_word = False
                self.total_words -= 1
                return len(node.children) == 0

            char = word[index]
            if char not in node.children:
                return False

            child_node = node.children[char]
            should_delete_child = _delete_helper(child_node, word, index + 1)

            if should_delete_child:
                del node.children[char]
                return len(node.children) == 0 and not node.is_end_of_word

            return False

        result = _delete_helper(self.root, word, 0)
        if result:
            logger.info(f"Deleted word: {word}, total words: {self.total_words}")
        else:
            logger.debug(f"Word not found for deletion: {word}")
        return result

    def count_words(self) -> int:
        """Get total number of words in trie.

        Returns:
            Total number of words.
        """
        return self.total_words

    def count_words_with_prefix(self, prefix: str) -> int:
        """Count number of words with given prefix.

        Args:
            prefix: Prefix to count words for.

        Returns:
            Number of words starting with prefix.
        """
        if not prefix:
            return self.total_words

        current = self.root
        for char in prefix:
            if char not in current.children:
                return 0
            current = current.children[char]

        return current.word_count

    def get_all_words(self) -> List[str]:
        """Get all words in trie.

        Returns:
            List of all words.
        """
        words: List[str] = []
        self._collect_words(self.root, "", words)
        return words

    def longest_common_prefix(self) -> str:
        """Find longest common prefix of all words in trie.

        Returns:
            Longest common prefix string.
        """
        if not self.root.children:
            return ""

        prefix = ""
        current = self.root

        while len(current.children) == 1 and not current.is_end_of_word:
            char = next(iter(current.children))
            prefix += char
            current = current.children[char]

        logger.debug(f"Longest common prefix: '{prefix}'")
        return prefix

    def build_from_list(self, words: List[str]) -> None:
        """Build trie from list of words.

        Args:
            words: List of words to insert.
        """
        logger.info(f"Building trie from {len(words)} words")
        for word in words:
            self.insert(word)
        logger.info(f"Trie built with {self.total_words} words")

    def compare_performance(
        self, words: List[str], prefix: str, iterations: int = 1
    ) -> Dict[str, any]:
        """Compare performance of trie operations.

        Args:
            words: List of words to insert.
            prefix: Prefix for autocomplete testing.
            iterations: Number of iterations for timing (default: 1).

        Returns:
            Dictionary containing performance data.
        """
        logger.info(
            f"Performance comparison: {len(words)} words, "
            f"prefix='{prefix}', iterations={iterations}"
        )

        results = {
            "num_words": len(words),
            "prefix": prefix,
            "iterations": iterations,
            "insert": {},
            "search": {},
            "autocomplete": {},
            "starts_with": {},
        }

        # Insert operations
        try:
            start_time = time.perf_counter()
            for _ in range(iterations):
                trie = Trie(config_path=self.config.get("config_path", "config.yaml"))
                for word in words:
                    trie.insert(word)
            insert_time = time.perf_counter() - start_time

            results["insert"] = {
                "time_seconds": insert_time / iterations,
                "time_milliseconds": (insert_time / iterations) * 1000,
                "time_per_word_microseconds": (
                    (insert_time / iterations) / len(words) * 1000000
                ),
                "success": True,
            }
        except Exception as e:
            logger.error(f"Insert operations failed: {e}")
            results["insert"] = {"success": False, "error": str(e)}

        # Build trie for other operations
        trie = Trie(config_path=self.config.get("config_path", "config.yaml"))
        for word in words:
            trie.insert(word)

        # Search operations
        try:
            start_time = time.perf_counter()
            for _ in range(iterations):
                for word in words[:10]:  # Test with first 10 words
                    trie.search(word)
            search_time = time.perf_counter() - start_time

            results["search"] = {
                "operations": len(words[:10]) * iterations,
                "time_seconds": search_time / iterations,
                "time_milliseconds": (search_time / iterations) * 1000,
                "time_per_search_microseconds": (
                    (search_time / iterations) / len(words[:10]) * 1000000
                ),
                "success": True,
            }
        except Exception as e:
            logger.error(f"Search operations failed: {e}")
            results["search"] = {"success": False, "error": str(e)}

        # Autocomplete operations
        try:
            start_time = time.perf_counter()
            for _ in range(iterations):
                suggestions = trie.autocomplete(prefix)
            autocomplete_time = time.perf_counter() - start_time

            results["autocomplete"] = {
                "suggestions": len(suggestions),
                "time_seconds": autocomplete_time / iterations,
                "time_milliseconds": (autocomplete_time / iterations) * 1000,
                "success": True,
            }
        except Exception as e:
            logger.error(f"Autocomplete operations failed: {e}")
            results["autocomplete"] = {"success": False, "error": str(e)}

        # Starts with operations
        try:
            start_time = time.perf_counter()
            for _ in range(iterations):
                trie.starts_with(prefix)
            starts_time = time.perf_counter() - start_time

            results["starts_with"] = {
                "time_seconds": starts_time / iterations,
                "time_milliseconds": (starts_time / iterations) * 1000,
                "success": True,
            }
        except Exception as e:
            logger.error(f"Starts with operations failed: {e}")
            results["starts_with"] = {"success": False, "error": str(e)}

        return results

    def generate_report(
        self,
        performance_data: Dict[str, any],
        output_path: Optional[str] = None,
    ) -> str:
        """Generate performance report for trie operations.

        Args:
            performance_data: Performance data from compare_performance().
            output_path: Optional path to save report file.

        Returns:
            Report content as string.
        """
        report_lines = [
            "=" * 80,
            "TRIE DATA STRUCTURE PERFORMANCE REPORT",
            "=" * 80,
            "",
            f"Number of words: {performance_data['num_words']}",
            f"Prefix: '{performance_data['prefix']}'",
            f"Iterations: {performance_data['iterations']}",
            "",
            "RESULTS",
            "-" * 80,
        ]

        # Insert
        report_lines.append("\ninsert():")
        insert_data = performance_data["insert"]
        if insert_data.get("success", False):
            report_lines.append(
                f"  Time: {insert_data['time_milliseconds']:.4f} ms "
                f"({insert_data['time_seconds']:.6f} seconds)"
            )
            report_lines.append(
                f"  Time per word: "
                f"{insert_data['time_per_word_microseconds']:.2f} μs"
            )
        else:
            report_lines.append(f"  Status: Failed")
            report_lines.append(f"  Error: {insert_data.get('error', 'Unknown')}")

        # Search
        report_lines.append("\nsearch():")
        search_data = performance_data["search"]
        if search_data.get("success", False):
            report_lines.append(f"  Operations: {search_data['operations']}")
            report_lines.append(
                f"  Time: {search_data['time_milliseconds']:.4f} ms "
                f"({search_data['time_seconds']:.6f} seconds)"
            )
            report_lines.append(
                f"  Time per search: "
                f"{search_data['time_per_search_microseconds']:.2f} μs"
            )
        else:
            report_lines.append(f"  Status: Failed")
            report_lines.append(f"  Error: {search_data.get('error', 'Unknown')}")

        # Autocomplete
        report_lines.append("\nautocomplete():")
        autocomplete_data = performance_data["autocomplete"]
        if autocomplete_data.get("success", False):
            report_lines.append(
                f"  Suggestions: {autocomplete_data['suggestions']}"
            )
            report_lines.append(
                f"  Time: {autocomplete_data['time_milliseconds']:.4f} ms "
                f"({autocomplete_data['time_seconds']:.6f} seconds)"
            )
        else:
            report_lines.append(f"  Status: Failed")
            report_lines.append(
                f"  Error: {autocomplete_data.get('error', 'Unknown')}"
            )

        # Starts with
        report_lines.append("\nstarts_with():")
        starts_data = performance_data["starts_with"]
        if starts_data.get("success", False):
            report_lines.append(
                f"  Time: {starts_data['time_milliseconds']:.4f} ms "
                f"({starts_data['time_seconds']:.6f} seconds)"
            )
        else:
            report_lines.append(f"  Status: Failed")
            report_lines.append(
                f"  Error: {starts_data.get('error', 'Unknown')}"
            )

        report_lines.extend([
            "",
            "ALGORITHM COMPLEXITY",
            "-" * 80,
            "Trie Operations:",
            "  Insert: O(m) where m=word length",
            "  Search: O(m) where m=word length",
            "  Starts With: O(m) where m=prefix length",
            "  Autocomplete: O(m + k) where m=prefix length, k=number of suggestions",
            "  Delete: O(m) where m=word length",
            "  Space Complexity: O(ALPHABET_SIZE * N * M) where N=words, M=avg length",
            "",
            "Advantages:",
            "  - Fast prefix matching",
            "  - Efficient autocomplete",
            "  - Space efficient for common prefixes",
            "  - O(m) search time independent of dictionary size",
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
    import argparse

    parser = argparse.ArgumentParser(
        description="Trie (prefix tree) data structure for efficient string "
        "prefix matching and autocomplete"
    )
    parser.add_argument(
        "words",
        nargs="+",
        type=str,
        help="Words to insert into trie",
    )
    parser.add_argument(
        "-c",
        "--config",
        default="config.yaml",
        help="Path to configuration file (default: config.yaml)",
    )
    parser.add_argument(
        "-o",
        "--operation",
        choices=["insert", "search", "autocomplete", "prefix", "compare", "all"],
        default="all",
        help="Operation to perform (default: all)",
    )
    parser.add_argument(
        "-p",
        "--prefix",
        type=str,
        help="Prefix for autocomplete or prefix check",
    )
    parser.add_argument(
        "-w",
        "--word",
        type=str,
        help="Word for search operation",
    )
    parser.add_argument(
        "-l",
        "--limit",
        type=int,
        help="Limit number of autocomplete suggestions",
    )
    parser.add_argument(
        "-i",
        "--iterations",
        type=int,
        default=1,
        help="Number of iterations for timing (default: 1)",
    )
    parser.add_argument(
        "-r",
        "--report",
        help="Output path for performance report",
    )

    args = parser.parse_args()

    try:
        trie = Trie(config_path=args.config)

        words = args.words

        logger.info(f"Input: {len(words)} words")

        # Insert all words
        trie.build_from_list(words)

        if args.operation == "insert":
            print(f"Inserted {trie.count_words()} words into trie")

        elif args.operation == "search":
            if args.word:
                result = trie.search(args.word)
                print(f"Search for '{args.word}': {result}")
            else:
                print("No word specified for search. Use --word option")

        elif args.operation == "autocomplete":
            if args.prefix is not None:
                suggestions = trie.autocomplete(args.prefix, args.limit)
                print(f"Autocomplete for '{args.prefix}': {suggestions}")
            else:
                suggestions = trie.autocomplete("", args.limit)
                print(f"All words: {suggestions}")

        elif args.operation == "prefix":
            if args.prefix is not None:
                result = trie.starts_with(args.prefix)
                count = trie.count_words_with_prefix(args.prefix)
                print(f"Prefix '{args.prefix}': exists={result}, count={count}")
            else:
                print("No prefix specified. Use --prefix option")

        elif args.operation == "compare":
            prefix = args.prefix if args.prefix is not None else ""
            performance = trie.compare_performance(words, prefix, args.iterations)

            print(f"\nTrie Performance Comparison:")
            print(f"Words: {performance['num_words']}")
            print(f"Prefix: '{performance['prefix']}'")
            print("-" * 60)

            methods = [
                ("insert", "insert()"),
                ("search", "search()"),
                ("autocomplete", "autocomplete()"),
                ("starts_with", "starts_with()"),
            ]

            for method_key, method_name in methods:
                data = performance[method_key]
                if data.get("success", False):
                    if method_key == "insert":
                        print(
                            f"{method_name:20s}: "
                            f"{data['time_milliseconds']:8.4f} ms "
                            f"({data['time_per_word_microseconds']:.2f} μs/word)"
                        )
                    elif method_key == "search":
                        print(
                            f"{method_name:20s}: "
                            f"{data['time_milliseconds']:8.4f} ms "
                            f"({data['time_per_search_microseconds']:.2f} μs/search)"
                        )
                    elif method_key == "autocomplete":
                        print(
                            f"{method_name:20s}: "
                            f"suggestions={data['suggestions']}  "
                            f"({data['time_milliseconds']:8.4f} ms)"
                        )
                    else:
                        print(
                            f"{method_name:20s}: "
                            f"{data['time_milliseconds']:8.4f} ms"
                        )
                else:
                    print(
                        f"{method_name:20s}: Failed - "
                        f"{data.get('error', 'Unknown')}"
                    )

            if args.report:
                report = trie.generate_report(
                    performance, output_path=args.report
                )
                print(f"\nReport saved to {args.report}")

        elif args.operation == "all":
            print(f"Trie Statistics:")
            print(f"  Total words: {trie.count_words()}")
            print(f"  Longest common prefix: '{trie.longest_common_prefix()}'")

            if args.prefix is not None:
                suggestions = trie.autocomplete(args.prefix, args.limit)
                print(f"\nAutocomplete for '{args.prefix}':")
                for suggestion in suggestions:
                    print(f"  - {suggestion}")

            if args.word:
                result = trie.search(args.word)
                print(f"\nSearch for '{args.word}': {result}")

    except Exception as e:
        logger.error(f"Error during execution: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
