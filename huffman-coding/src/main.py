"""Huffman Coding with Adaptive and Canonical Variants.

This module provides functionality to compress data using Huffman coding
with standard, adaptive, and canonical variants.
"""

import heapq
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


class HuffmanNode:
    """Represents a node in Huffman tree."""

    def __init__(
        self,
        symbol: Optional[int] = None,
        frequency: int = 0,
        left: Optional["HuffmanNode"] = None,
        right: Optional["HuffmanNode"] = None,
    ) -> None:
        """Initialize Huffman node.

        Args:
            symbol: Symbol value (None for internal nodes).
            frequency: Frequency of symbol or subtree.
            left: Left child node.
            right: Right child node.
        """
        self.symbol = symbol
        self.frequency = frequency
        self.left = left
        self.right = right

    def __lt__(self, other: "HuffmanNode") -> bool:
        """Compare nodes for priority queue."""
        if self.frequency != other.frequency:
            return self.frequency < other.frequency
        if self.symbol is not None and other.symbol is not None:
            return self.symbol < other.symbol
        return id(self) < id(other)

    def is_leaf(self) -> bool:
        """Check if node is a leaf."""
        return self.left is None and self.right is None


class StandardHuffman:
    """Implements standard Huffman coding."""

    def __init__(self) -> None:
        """Initialize standard Huffman coder."""
        self.root: Optional[HuffmanNode] = None
        self.codes: Dict[int, str] = {}
        self.reverse_codes: Dict[str, int] = {}

    def build_tree(self, frequencies: Dict[int, int]) -> None:
        """Build Huffman tree from symbol frequencies.

        Args:
            frequencies: Dictionary mapping symbols to frequencies.
        """
        if not frequencies:
            self.root = None
            return

        if len(frequencies) == 1:
            symbol = list(frequencies.keys())[0]
            self.root = HuffmanNode(symbol=symbol, frequency=frequencies[symbol])
            self.codes = {symbol: "0"}
            self.reverse_codes = {"0": symbol}
            return

        heap = []
        for symbol, freq in frequencies.items():
            node = HuffmanNode(symbol=symbol, frequency=freq)
            heapq.heappush(heap, node)

        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)

            merged = HuffmanNode(
                frequency=left.frequency + right.frequency, left=left, right=right
            )
            heapq.heappush(heap, merged)

        self.root = heapq.heappop(heap)
        self._generate_codes(self.root, "")

    def _generate_codes(self, node: Optional[HuffmanNode], code: str) -> None:
        """Generate Huffman codes by traversing tree.

        Args:
            node: Current node.
            code: Current code string.
        """
        if node is None:
            return

        if node.is_leaf():
            if code:
                self.codes[node.symbol] = code
                self.reverse_codes[code] = node.symbol
            else:
                self.codes[node.symbol] = "0"
                self.reverse_codes["0"] = node.symbol
        else:
            self._generate_codes(node.left, code + "0")
            self._generate_codes(node.right, code + "1")

    def encode(self, data: bytes) -> Tuple[str, Dict[int, str]]:
        """Encode data using Huffman codes.

        Args:
            data: Input data to encode.

        Returns:
            Tuple of (encoded_bits, codes_dict).
        """
        if not self.codes:
            raise ValueError("Huffman tree not built. Call build_tree() first.")

        encoded = []
        for byte in data:
            if byte not in self.codes:
                raise ValueError(f"Symbol {byte} not in Huffman tree")
            encoded.append(self.codes[byte])

        return "".join(encoded), self.codes.copy()

    def decode(self, encoded_bits: str) -> bytes:
        """Decode data using Huffman codes.

        Args:
            encoded_bits: Encoded bit string.

        Returns:
            Decoded data as bytes.
        """
        if not self.reverse_codes:
            raise ValueError("Huffman tree not built. Call build_tree() first.")

        decoded = []
        current_code = ""

        for bit in encoded_bits:
            current_code += bit
            if current_code in self.reverse_codes:
                decoded.append(self.reverse_codes[current_code])
                current_code = ""

        if current_code:
            raise ValueError(f"Invalid code at end: {current_code}")

        return bytes(decoded)


class CanonicalHuffman:
    """Implements canonical Huffman coding."""

    def __init__(self) -> None:
        """Initialize canonical Huffman coder."""
        self.codes: Dict[int, str] = {}
        self.reverse_codes: Dict[str, int] = {}
        self.code_lengths: Dict[int, int] = {}

    def build_from_lengths(self, code_lengths: Dict[int, int]) -> None:
        """Build canonical codes from code lengths.

        Args:
            code_lengths: Dictionary mapping symbols to code lengths.
        """
        if not code_lengths:
            return

        self.code_lengths = code_lengths.copy()

        symbols_by_length = defaultdict(list)
        for symbol, length in code_lengths.items():
            symbols_by_length[length].append(symbol)

        for length in symbols_by_length:
            symbols_by_length[length].sort()

        code = 0
        prev_length = 0

        for length in sorted(symbols_by_length.keys()):
            code <<= length - prev_length

            for symbol in symbols_by_length[length]:
                code_str = format(code, f"0{length}b")
                self.codes[symbol] = code_str
                self.reverse_codes[code_str] = symbol
                code += 1

            prev_length = length

    def build_from_standard(self, standard_huffman: StandardHuffman) -> None:
        """Build canonical codes from standard Huffman tree.

        Args:
            standard_huffman: StandardHuffman instance with built tree.
        """
        if not standard_huffman.codes:
            return

        code_lengths = {
            symbol: len(code) for symbol, code in standard_huffman.codes.items()
        }
        self.build_from_lengths(code_lengths)

    def encode(self, data: bytes) -> Tuple[str, Dict[int, int]]:
        """Encode data using canonical Huffman codes.

        Args:
            data: Input data to encode.

        Returns:
            Tuple of (encoded_bits, code_lengths_dict).
        """
        if not self.codes:
            raise ValueError("Canonical codes not built. Call build_from_lengths() first.")

        encoded = []
        for byte in data:
            if byte not in self.codes:
                raise ValueError(f"Symbol {byte} not in canonical codes")
            encoded.append(self.codes[byte])

        return "".join(encoded), self.code_lengths.copy()

    def decode(self, encoded_bits: str) -> bytes:
        """Decode data using canonical Huffman codes.

        Args:
            encoded_bits: Encoded bit string.

        Returns:
            Decoded data as bytes.
        """
        if not self.reverse_codes:
            raise ValueError("Canonical codes not built. Call build_from_lengths() first.")

        decoded = []
        current_code = ""

        for bit in encoded_bits:
            current_code += bit
            if current_code in self.reverse_codes:
                decoded.append(self.reverse_codes[current_code])
                current_code = ""

        if current_code:
            raise ValueError(f"Invalid code at end: {current_code}")

        return bytes(decoded)


class AdaptiveHuffman:
    """Implements adaptive Huffman coding (FGK algorithm)."""

    def __init__(self) -> None:
        """Initialize adaptive Huffman coder."""
        self.root: Optional[HuffmanNode] = None
        self.nyt_node: Optional[HuffmanNode] = None
        self.symbol_nodes: Dict[int, HuffmanNode] = {}
        self.node_list: List[HuffmanNode] = []
        self.codes: Dict[int, str] = {}
        self.reverse_codes: Dict[str, int] = {}

    def _initialize_tree(self) -> None:
        """Initialize tree with NYT (Not Yet Transmitted) node."""
        self.root = HuffmanNode(symbol=None, frequency=0)
        self.nyt_node = self.root
        self.symbol_nodes = {}
        self.node_list = [self.root]

    def _get_code(self, node: HuffmanNode) -> str:
        """Get code for node by traversing to root.

        Args:
            node: Node to get code for.

        Returns:
            Code string.
        """
        code = ""
        current = node
        parent_map = self._build_parent_map()

        while current != self.root:
            parent = parent_map.get(current)
            if parent and parent.left == current:
                code = "0" + code
            elif parent and parent.right == current:
                code = "1" + code
            current = parent

        return code

    def _build_parent_map(self) -> Dict[HuffmanNode, HuffmanNode]:
        """Build parent map for tree traversal.

        Returns:
            Dictionary mapping nodes to their parents.
        """
        parent_map = {}
        if self.root:
            self._build_parent_map_recursive(self.root, None, parent_map)
        return parent_map

    def _build_parent_map_recursive(
        self,
        node: HuffmanNode,
        parent: Optional[HuffmanNode],
        parent_map: Dict[HuffmanNode, HuffmanNode],
    ) -> None:
        """Recursively build parent map.

        Args:
            node: Current node.
            parent: Parent node.
            parent_map: Dictionary to populate.
        """
        if parent:
            parent_map[node] = parent
        if node.left:
            self._build_parent_map_recursive(node.left, node, parent_map)
        if node.right:
            self._build_parent_map_recursive(node.right, node, parent_map)

    def _find_node_to_increment(self, node: HuffmanNode) -> Optional[HuffmanNode]:
        """Find node to swap with (for tree balancing).

        Args:
            node: Node that was incremented.

        Returns:
            Node to swap with, or None.
        """
        parent_map = self._build_parent_map()
        current = node

        while current != self.root:
            parent = parent_map.get(current)
            if parent and parent.right == current:
                sibling = parent.left
                if sibling and sibling.frequency < current.frequency:
                    return sibling
            current = parent

        return None

    def _increment_frequency(self, node: HuffmanNode) -> None:
        """Increment frequency and update tree.

        Args:
            node: Node to increment.
        """
        node.frequency += 1

        swap_node = self._find_node_to_increment(node)
        if swap_node and swap_node != node:
            self._swap_nodes(node, swap_node)

        parent_map = self._build_parent_map()
        parent = parent_map.get(node)
        if parent:
            self._increment_frequency(parent)

    def _swap_nodes(self, node1: HuffmanNode, node2: HuffmanNode) -> None:
        """Swap two nodes in tree.

        Args:
            node1: First node.
            node2: Second node.
        """
        parent_map = self._build_parent_map()
        parent1 = parent_map.get(node1)
        parent2 = parent_map.get(node2)

        if parent1:
            if parent1.left == node1:
                parent1.left = node2
            else:
                parent1.right = node2

        if parent2:
            if parent2.left == node2:
                parent2.left = node1
            else:
                parent2.right = node1

        if node1 == self.root:
            self.root = node2
        elif node2 == self.root:
            self.root = node1

    def encode(self, data: bytes) -> str:
        """Encode data using adaptive Huffman coding.

        Args:
            data: Input data to encode.

        Returns:
            Encoded bit string.
        """
        self._initialize_tree()
        encoded = []

        for symbol in data:
            if symbol in self.symbol_nodes:
                node = self.symbol_nodes[symbol]
                code = self._get_code(node)
                encoded.append(code)
                self._increment_frequency(node)
            else:
                nyt_code = self._get_code(self.nyt_node)
                symbol_bits = format(symbol, "08b")
                encoded.append(nyt_code + symbol_bits)

                new_node = HuffmanNode(symbol=symbol, frequency=1)
                self.symbol_nodes[symbol] = new_node

                if self.nyt_node == self.root:
                    self.root = HuffmanNode(
                        frequency=1, left=self.nyt_node, right=new_node
                    )
                    self.nyt_node = self.root.left
                else:
                    parent = self._build_parent_map().get(self.nyt_node)
                    if parent:
                        internal = HuffmanNode(
                            frequency=1, left=self.nyt_node, right=new_node
                        )
                        if parent.left == self.nyt_node:
                            parent.left = internal
                        else:
                            parent.right = internal
                        self.nyt_node = internal.left

                self._update_node_list()

        return "".join(encoded)

    def _update_node_list(self) -> None:
        """Update node list for tree traversal."""
        self.node_list = []
        if self.root:
            self._collect_nodes(self.root)

    def _collect_nodes(self, node: HuffmanNode) -> None:
        """Collect all nodes in tree.

        Args:
            node: Current node.
        """
        if node:
            self.node_list.append(node)
            if node.left:
                self._collect_nodes(node.left)
            if node.right:
                self._collect_nodes(node.right)

    def decode(self, encoded_bits: str) -> bytes:
        """Decode data using adaptive Huffman coding.

        Args:
            encoded_bits: Encoded bit string.

        Returns:
            Decoded data as bytes.
        """
        self._initialize_tree()
        decoded = []
        i = 0

        while i < len(encoded_bits):
            current = self.root

            while current and not current.is_leaf():
                if i >= len(encoded_bits):
                    break
                bit = encoded_bits[i]
                i += 1
                if bit == "0":
                    current = current.left
                else:
                    current = current.right

            if current and current.symbol is not None:
                decoded.append(current.symbol)
                self._increment_frequency(current)
            elif current == self.nyt_node:
                if i + 8 > len(encoded_bits):
                    break
                symbol_bits = encoded_bits[i : i + 8]
                symbol = int(symbol_bits, 2)
                i += 8
                decoded.append(symbol)

                new_node = HuffmanNode(symbol=symbol, frequency=1)
                self.symbol_nodes[symbol] = new_node

                if self.nyt_node == self.root:
                    self.root = HuffmanNode(
                        frequency=1, left=self.nyt_node, right=new_node
                    )
                    self.nyt_node = self.root.left
                else:
                    parent_map = self._build_parent_map()
                    parent = parent_map.get(self.nyt_node)
                    if parent:
                        internal = HuffmanNode(
                            frequency=1, left=self.nyt_node, right=new_node
                        )
                        if parent.left == self.nyt_node:
                            parent.left = internal
                        else:
                            parent.right = internal
                        self.nyt_node = internal.left

                self._update_node_list()

        return bytes(decoded)


class HuffmanCodingManager:
    """Manages Huffman coding operations with configuration."""

    def __init__(self, config_path: str = "config.yaml") -> None:
        """Initialize HuffmanCodingManager with configuration.

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
            "%(asctime)s - %(name)s - %(levelname)s - " "%(message)s"
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

    def compress_standard(self, data: bytes) -> Tuple[str, Dict[int, str]]:
        """Compress data using standard Huffman coding.

        Args:
            data: Input data to compress.

        Returns:
            Tuple of (encoded_bits, codes_dict).
        """
        frequencies = Counter(data)
        huffman = StandardHuffman()
        huffman.build_tree(frequencies)
        return huffman.encode(data)

    def decompress_standard(
        self, encoded_bits: str, codes: Dict[int, str]
    ) -> bytes:
        """Decompress data using standard Huffman coding.

        Args:
            encoded_bits: Encoded bit string.
            codes: Huffman codes dictionary.

        Returns:
            Decoded data.
        """
        huffman = StandardHuffman()
        frequencies = Counter()
        for symbol, code in codes.items():
            frequencies[symbol] = len(code)
        huffman.build_tree(frequencies)
        huffman.codes = codes
        huffman.reverse_codes = {v: k for k, v in codes.items()}
        return huffman.decode(encoded_bits)

    def compress_canonical(self, data: bytes) -> Tuple[str, Dict[int, int]]:
        """Compress data using canonical Huffman coding.

        Args:
            data: Input data to compress.

        Returns:
            Tuple of (encoded_bits, code_lengths_dict).
        """
        frequencies = Counter(data)
        standard = StandardHuffman()
        standard.build_tree(frequencies)

        canonical = CanonicalHuffman()
        canonical.build_from_standard(standard)
        return canonical.encode(data)

    def decompress_canonical(
        self, encoded_bits: str, code_lengths: Dict[int, int]
    ) -> bytes:
        """Decompress data using canonical Huffman coding.

        Args:
            encoded_bits: Encoded bit string.
            code_lengths: Code lengths dictionary.

        Returns:
            Decoded data.
        """
        canonical = CanonicalHuffman()
        canonical.build_from_lengths(code_lengths)
        return canonical.decode(encoded_bits)

    def compress_adaptive(self, data: bytes) -> str:
        """Compress data using adaptive Huffman coding.

        Args:
            data: Input data to compress.

        Returns:
            Encoded bit string.
        """
        adaptive = AdaptiveHuffman()
        return adaptive.encode(data)

    def decompress_adaptive(self, encoded_bits: str) -> bytes:
        """Decompress data using adaptive Huffman coding.

        Args:
            encoded_bits: Encoded bit string.

        Returns:
            Decoded data.
        """
        adaptive = AdaptiveHuffman()
        return adaptive.decode(encoded_bits)

    def get_compression_ratio(
        self, original_size: int, compressed_bits: int
    ) -> float:
        """Calculate compression ratio.

        Args:
            original_size: Size of original data in bytes.
            compressed_bits: Size of compressed data in bits.

        Returns:
            Compression ratio (original / compressed).
        """
        compressed_bytes = (compressed_bits + 7) // 8
        if compressed_bytes == 0:
            return float("inf")
        return original_size / compressed_bytes


def main() -> None:
    """Main entry point for command-line usage."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Huffman Coding with Adaptive and Canonical Variants"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="config.yaml",
        help="Path to configuration file",
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Run test compression",
    )

    args = parser.parse_args()

    manager = HuffmanCodingManager(config_path=args.config)

    if args.test:
        logger.info("Running test compression")

        test_data = b"abracadabra"
        print(f"\nOriginal data: {test_data}")
        print(f"Original size: {len(test_data)} bytes")

        print("\n=== Standard Huffman ===")
        encoded, codes = manager.compress_standard(test_data)
        print(f"Encoded bits: {len(encoded)} bits ({len(encoded)/8:.2f} bytes)")
        print(f"Compression ratio: {manager.get_compression_ratio(len(test_data), len(encoded)):.2f}")
        decoded = manager.decompress_standard(encoded, codes)
        print(f"Decoded: {decoded}")
        print(f"Match: {test_data == decoded}")

        print("\n=== Canonical Huffman ===")
        encoded, lengths = manager.compress_canonical(test_data)
        print(f"Encoded bits: {len(encoded)} bits ({len(encoded)/8:.2f} bytes)")
        print(f"Compression ratio: {manager.get_compression_ratio(len(test_data), len(encoded)):.2f}")
        decoded = manager.decompress_canonical(encoded, lengths)
        print(f"Decoded: {decoded}")
        print(f"Match: {test_data == decoded}")

        print("\n=== Adaptive Huffman ===")
        encoded = manager.compress_adaptive(test_data)
        print(f"Encoded bits: {len(encoded)} bits ({len(encoded)/8:.2f} bytes)")
        print(f"Compression ratio: {manager.get_compression_ratio(len(test_data), len(encoded)):.2f}")
        decoded = manager.decompress_adaptive(encoded)
        print(f"Decoded: {decoded}")
        print(f"Match: {test_data == decoded}")


if __name__ == "__main__":
    main()
