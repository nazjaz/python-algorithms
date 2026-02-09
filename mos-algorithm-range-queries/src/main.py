"""Mo's algorithm for offline range queries with square root decomposition.

This module implements Mo's algorithm for efficiently processing multiple
range queries offline using square root decomposition optimization.
"""

import logging
import math
import sys
from typing import Callable, Dict, List, Optional, Tuple

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class Query:
    """Represents a range query."""

    def __init__(self, left: int, right: int, index: int = 0) -> None:
        """Initialize a query.

        Args:
            left: Left endpoint (inclusive, 0-indexed).
            right: Right endpoint (inclusive, 0-indexed).
            index: Query index for preserving order.
        """
        self.left = left
        self.right = right
        self.index = index

    def __repr__(self) -> str:
        """String representation of query."""
        return f"Query({self.left}, {self.right}, index={self.index})"


class MosAlgorithm:
    """Mo's algorithm for offline range queries.

    Processes multiple range queries efficiently by reordering them
    using square root decomposition.
    """

    def __init__(self, array: List[int]) -> None:
        """Initialize Mo's algorithm with an array.

        Args:
            array: Input array for queries.
        """
        self.array = array
        self.n = len(array)
        self.block_size = int(math.sqrt(self.n)) if self.n > 0 else 1

    def _get_block(self, index: int) -> int:
        """Get block number for an index.

        Args:
            index: Array index.

        Returns:
            Block number.
        """
        return index // self.block_size

    def _compare_queries(self, q1: Query, q2: Query) -> int:
        """Compare two queries for sorting.

        Args:
            q1: First query.
            q2: Second query.

        Returns:
            Comparison result (-1, 0, or 1).
        """
        block1 = self._get_block(q1.left)
        block2 = self._get_block(q2.left)

        if block1 != block2:
            return block1 - block2

        if block1 % 2 == 0:
            return q1.right - q2.right
        else:
            return q2.right - q1.right

    def process_queries(
        self,
        queries: List[Query],
        add_func: Callable[[int], None],
        remove_func: Callable[[int], None],
        get_result_func: Callable[[], any],
    ) -> List[any]:
        """Process queries using Mo's algorithm.

        Args:
            queries: List of queries to process.
            add_func: Function to call when adding an element at index.
            remove_func: Function to call when removing an element at index.
            get_result_func: Function to get current result.

        Returns:
            List of results in original query order.
        """
        if not queries:
            return []

        sorted_queries = sorted(queries, key=lambda q: (
            self._get_block(q.left),
            q.right if self._get_block(q.left) % 2 == 0 else -q.right
        ))

        results = [None] * len(queries)
        current_left = 0
        current_right = -1

        for query in sorted_queries:
            while current_left > query.left:
                current_left -= 1
                add_func(current_left)

            while current_right < query.right:
                current_right += 1
                add_func(current_right)

            while current_left < query.left:
                remove_func(current_left)
                current_left += 1

            while current_right > query.right:
                remove_func(current_right)
                current_right -= 1

            results[query.index] = get_result_func()

        return results

    def range_sum_queries(self, queries: List[Query]) -> List[int]:
        """Answer range sum queries.

        Args:
            queries: List of range sum queries.

        Returns:
            List of sum results.
        """
        current_sum = 0

        def add(index: int) -> None:
            nonlocal current_sum
            current_sum += self.array[index]

        def remove(index: int) -> None:
            nonlocal current_sum
            current_sum -= self.array[index]

        def get_result() -> int:
            return current_sum

        return self.process_queries(queries, add, remove, get_result)

    def range_distinct_count_queries(
        self, queries: List[Query]
    ) -> List[int]:
        """Answer range distinct count queries.

        Args:
            queries: List of range distinct count queries.

        Returns:
            List of distinct count results.
        """
        frequency: Dict[int, int] = {}
        distinct_count = 0

        def add(index: int) -> None:
            nonlocal distinct_count
            value = self.array[index]
            frequency[value] = frequency.get(value, 0) + 1
            if frequency[value] == 1:
                distinct_count += 1

        def remove(index: int) -> None:
            nonlocal distinct_count
            value = self.array[index]
            frequency[value] = frequency.get(value, 0) - 1
            if frequency[value] == 0:
                distinct_count -= 1

        def get_result() -> int:
            return distinct_count

        return self.process_queries(queries, add, remove, get_result)

    def range_max_queries(self, queries: List[Query]) -> List[Optional[int]]:
        """Answer range maximum queries.

        Args:
            queries: List of range maximum queries.

        Returns:
            List of maximum values.
        """
        frequency: Dict[int, int] = {}
        max_value: Optional[int] = None

        def add(index: int) -> None:
            nonlocal max_value
            value = self.array[index]
            frequency[value] = frequency.get(value, 0) + 1
            if max_value is None or value > max_value:
                max_value = value

        def remove(index: int) -> None:
            nonlocal max_value
            value = self.array[index]
            frequency[value] = frequency.get(value, 0) - 1
            if frequency[value] == 0:
                frequency.pop(value)
                if value == max_value:
                    if frequency:
                        max_value = max(frequency.keys())
                    else:
                        max_value = None

        def get_result() -> Optional[int]:
            return max_value

        return self.process_queries(queries, add, remove, get_result)

    def range_min_queries(self, queries: List[Query]) -> List[Optional[int]]:
        """Answer range minimum queries.

        Args:
            queries: List of range minimum queries.

        Returns:
            List of minimum values.
        """
        frequency: Dict[int, int] = {}
        min_value: Optional[int] = None

        def add(index: int) -> None:
            nonlocal min_value
            value = self.array[index]
            frequency[value] = frequency.get(value, 0) + 1
            if min_value is None or value < min_value:
                min_value = value

        def remove(index: int) -> None:
            nonlocal min_value
            value = self.array[index]
            frequency[value] = frequency.get(value, 0) - 1
            if frequency[value] == 0:
                frequency.pop(value)
                if value == min_value:
                    if frequency:
                        min_value = min(frequency.keys())
                    else:
                        min_value = None

        def get_result() -> Optional[int]:
            return min_value

        return self.process_queries(queries, add, remove, get_result)

    def range_frequency_queries(
        self, queries: List[Query], target_value: int
    ) -> List[int]:
        """Answer range frequency queries for a specific value.

        Args:
            queries: List of range frequency queries.
            target_value: Value to count frequency of.

        Returns:
            List of frequency results.
        """
        frequency = 0

        def add(index: int) -> None:
            nonlocal frequency
            if self.array[index] == target_value:
                frequency += 1

        def remove(index: int) -> None:
            nonlocal frequency
            if self.array[index] == target_value:
                frequency -= 1

        def get_result() -> int:
            return frequency

        return self.process_queries(queries, add, remove, get_result)

    def range_mode_queries(self, queries: List[Query]) -> List[Optional[int]]:
        """Answer range mode (most frequent element) queries.

        Args:
            queries: List of range mode queries.

        Returns:
            List of mode values.
        """
        frequency: Dict[int, int] = {}
        max_frequency = 0
        mode_value: Optional[int] = None

        def add(index: int) -> None:
            nonlocal max_frequency, mode_value
            value = self.array[index]
            frequency[value] = frequency.get(value, 0) + 1
            if frequency[value] > max_frequency:
                max_frequency = frequency[value]
                mode_value = value
            elif frequency[value] == max_frequency and value < mode_value:
                mode_value = value

        def remove(index: int) -> None:
            nonlocal max_frequency, mode_value
            value = self.array[index]
            frequency[value] = frequency.get(value, 0) - 1
            if frequency[value] == 0:
                frequency.pop(value)

            if value == mode_value and frequency.get(value, 0) < max_frequency:
                if frequency:
                    max_frequency = max(frequency.values())
                    mode_value = min(
                        k for k, v in frequency.items() if v == max_frequency
                    )
                else:
                    max_frequency = 0
                    mode_value = None

        def get_result() -> Optional[int]:
            return mode_value

        return self.process_queries(queries, add, remove, get_result)


def main() -> None:
    """Main function to run the Mo's algorithm CLI interface."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Mo's algorithm for offline range queries"
    )
    parser.add_argument(
        "--array",
        type=str,
        required=True,
        help="Comma-separated array values",
    )
    parser.add_argument(
        "--queries",
        type=str,
        required=True,
        help="Queries in format 'l1,r1;l2,r2;...' (0-indexed)",
    )
    parser.add_argument(
        "--type",
        type=str,
        choices=["sum", "distinct", "max", "min", "frequency", "mode"],
        default="sum",
        help="Query type (default: sum)",
    )
    parser.add_argument(
        "--target",
        type=int,
        help="Target value for frequency queries",
    )

    args = parser.parse_args()

    try:
        array = [int(x.strip()) for x in args.array.split(",")]

        query_parts = args.queries.split(";")
        queries = []
        for i, part in enumerate(query_parts):
            left, right = map(int, part.split(","))
            queries.append(Query(left, right, index=i))

        mos = MosAlgorithm(array)

        print(f"Array: {array}")
        print(f"Number of queries: {len(queries)}")
        print(f"Block size: {mos.block_size}")
        print()

        if args.type == "sum":
            results = mos.range_sum_queries(queries)
            print("Range Sum Queries:")
            for i, (query, result) in enumerate(zip(queries, results)):
                print(f"  Query {i+1}: Sum[{query.left}..{query.right}] = {result}")

        elif args.type == "distinct":
            results = mos.range_distinct_count_queries(queries)
            print("Range Distinct Count Queries:")
            for i, (query, result) in enumerate(zip(queries, results)):
                print(
                    f"  Query {i+1}: Distinct[{query.left}..{query.right}] = {result}"
                )

        elif args.type == "max":
            results = mos.range_max_queries(queries)
            print("Range Maximum Queries:")
            for i, (query, result) in enumerate(zip(queries, results)):
                print(f"  Query {i+1}: Max[{query.left}..{query.right}] = {result}")

        elif args.type == "min":
            results = mos.range_min_queries(queries)
            print("Range Minimum Queries:")
            for i, (query, result) in enumerate(zip(queries, results)):
                print(f"  Query {i+1}: Min[{query.left}..{query.right}] = {result}")

        elif args.type == "frequency":
            if args.target is None:
                logger.error("--target is required for frequency queries")
                sys.exit(1)
            results = mos.range_frequency_queries(queries, args.target)
            print(f"Range Frequency Queries (target={args.target}):")
            for i, (query, result) in enumerate(zip(queries, results)):
                print(
                    f"  Query {i+1}: Freq[{query.left}..{query.right}] = {result}"
                )

        elif args.type == "mode":
            results = mos.range_mode_queries(queries)
            print("Range Mode Queries:")
            for i, (query, result) in enumerate(zip(queries, results)):
                print(f"  Query {i+1}: Mode[{query.left}..{query.right}] = {result}")

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
