"""Test suite for Mo's algorithm implementation."""

import pytest

from src.main import MosAlgorithm, Query


class TestQuery:
    """Test cases for Query class."""

    def test_query_initialization(self) -> None:
        """Test query initialization."""
        query = Query(0, 5, index=0)
        assert query.left == 0
        assert query.right == 5
        assert query.index == 0

    def test_query_repr(self) -> None:
        """Test query string representation."""
        query = Query(1, 3, index=2)
        repr_str = repr(query)
        assert "Query" in repr_str
        assert "1" in repr_str
        assert "3" in repr_str


class TestMosAlgorithm:
    """Test cases for MosAlgorithm class."""

    def test_initialization(self) -> None:
        """Test MosAlgorithm initialization."""
        array = [1, 2, 3, 4, 5]
        mos = MosAlgorithm(array)
        assert mos.array == array
        assert mos.n == 5
        assert mos.block_size > 0

    def test_initialization_empty(self) -> None:
        """Test initialization with empty array."""
        mos = MosAlgorithm([])
        assert mos.n == 0
        assert mos.block_size == 1

    def test_get_block(self) -> None:
        """Test block number calculation."""
        array = list(range(100))
        mos = MosAlgorithm(array)
        assert mos._get_block(0) == 0
        assert mos._get_block(mos.block_size - 1) == 0
        assert mos._get_block(mos.block_size) == 1

    def test_range_sum_queries_simple(self) -> None:
        """Test range sum queries with simple case."""
        array = [1, 2, 3, 4, 5]
        mos = MosAlgorithm(array)
        queries = [Query(0, 2, 0), Query(1, 3, 1)]
        results = mos.range_sum_queries(queries)
        assert results[0] == 6
        assert results[1] == 9

    def test_range_sum_queries_single(self) -> None:
        """Test range sum query with single element."""
        array = [1, 2, 3, 4, 5]
        mos = MosAlgorithm(array)
        queries = [Query(2, 2, 0)]
        results = mos.range_sum_queries(queries)
        assert results[0] == 3

    def test_range_sum_queries_full_range(self) -> None:
        """Test range sum query for full array."""
        array = [1, 2, 3, 4, 5]
        mos = MosAlgorithm(array)
        queries = [Query(0, 4, 0)]
        results = mos.range_sum_queries(queries)
        assert results[0] == 15

    def test_range_sum_queries_empty(self) -> None:
        """Test range sum queries with empty query list."""
        array = [1, 2, 3]
        mos = MosAlgorithm(array)
        results = mos.range_sum_queries([])
        assert results == []

    def test_range_distinct_count_queries(self) -> None:
        """Test range distinct count queries."""
        array = [1, 2, 2, 3, 3, 3]
        mos = MosAlgorithm(array)
        queries = [Query(0, 2, 0), Query(1, 5, 1)]
        results = mos.range_distinct_count_queries(queries)
        assert results[0] == 2
        assert results[1] == 3

    def test_range_distinct_count_all_same(self) -> None:
        """Test distinct count with all same elements."""
        array = [1, 1, 1, 1]
        mos = MosAlgorithm(array)
        queries = [Query(0, 3, 0)]
        results = mos.range_distinct_count_queries(queries)
        assert results[0] == 1

    def test_range_distinct_count_all_different(self) -> None:
        """Test distinct count with all different elements."""
        array = [1, 2, 3, 4, 5]
        mos = MosAlgorithm(array)
        queries = [Query(0, 4, 0)]
        results = mos.range_distinct_count_queries(queries)
        assert results[0] == 5

    def test_range_max_queries(self) -> None:
        """Test range maximum queries."""
        array = [1, 5, 3, 2, 4]
        mos = MosAlgorithm(array)
        queries = [Query(0, 2, 0), Query(1, 4, 1)]
        results = mos.range_max_queries(queries)
        assert results[0] == 5
        assert results[1] == 5

    def test_range_max_queries_single(self) -> None:
        """Test range max query with single element."""
        array = [1, 2, 3]
        mos = MosAlgorithm(array)
        queries = [Query(1, 1, 0)]
        results = mos.range_max_queries(queries)
        assert results[0] == 2

    def test_range_min_queries(self) -> None:
        """Test range minimum queries."""
        array = [5, 1, 3, 2, 4]
        mos = MosAlgorithm(array)
        queries = [Query(0, 2, 0), Query(1, 4, 1)]
        results = mos.range_min_queries(queries)
        assert results[0] == 1
        assert results[1] == 1

    def test_range_min_queries_single(self) -> None:
        """Test range min query with single element."""
        array = [1, 2, 3]
        mos = MosAlgorithm(array)
        queries = [Query(1, 1, 0)]
        results = mos.range_min_queries(queries)
        assert results[0] == 2

    def test_range_frequency_queries(self) -> None:
        """Test range frequency queries."""
        array = [1, 2, 2, 3, 2, 4]
        mos = MosAlgorithm(array)
        queries = [Query(0, 2, 0), Query(1, 4, 1)]
        results = mos.range_frequency_queries(queries, 2)
        assert results[0] == 2
        assert results[1] == 2

    def test_range_frequency_queries_not_found(self) -> None:
        """Test frequency query when value not found."""
        array = [1, 2, 3, 4, 5]
        mos = MosAlgorithm(array)
        queries = [Query(0, 4, 0)]
        results = mos.range_frequency_queries(queries, 10)
        assert results[0] == 0

    def test_range_mode_queries(self) -> None:
        """Test range mode queries."""
        array = [1, 2, 2, 3, 2, 4]
        mos = MosAlgorithm(array)
        queries = [Query(0, 2, 0), Query(1, 4, 1)]
        results = mos.range_mode_queries(queries)
        assert results[0] == 2
        assert results[1] == 2

    def test_range_mode_queries_tie(self) -> None:
        """Test mode query with tie (returns smaller value)."""
        array = [1, 2, 1, 2, 3]
        mos = MosAlgorithm(array)
        queries = [Query(0, 3, 0)]
        results = mos.range_mode_queries(queries)
        assert results[0] in [1, 2]

    def test_multiple_queries_order(self) -> None:
        """Test that results are returned in original query order."""
        array = [1, 2, 3, 4, 5]
        mos = MosAlgorithm(array)
        queries = [
            Query(0, 0, index=0),
            Query(1, 1, index=1),
            Query(2, 2, index=2),
        ]
        results = mos.range_sum_queries(queries)
        assert results[0] == 1
        assert results[1] == 2
        assert results[2] == 3

    def test_overlapping_queries(self) -> None:
        """Test overlapping range queries."""
        array = [1, 2, 3, 4, 5]
        mos = MosAlgorithm(array)
        queries = [Query(0, 2, 0), Query(1, 3, 1), Query(2, 4, 2)]
        results = mos.range_sum_queries(queries)
        assert results[0] == 6
        assert results[1] == 9
        assert results[2] == 12

    def test_nested_queries(self) -> None:
        """Test nested range queries."""
        array = [1, 2, 3, 4, 5]
        mos = MosAlgorithm(array)
        queries = [Query(0, 4, 0), Query(1, 3, 1), Query(2, 2, 2)]
        results = mos.range_sum_queries(queries)
        assert results[0] == 15
        assert results[1] == 9
        assert results[2] == 3

    def test_large_array(self) -> None:
        """Test with larger array."""
        array = list(range(1, 101))
        mos = MosAlgorithm(array)
        queries = [Query(0, 99, 0), Query(10, 20, 1)]
        results = mos.range_sum_queries(queries)
        assert results[0] == sum(array)
        assert results[1] == sum(array[10:21])

    def test_negative_numbers(self) -> None:
        """Test with negative numbers."""
        array = [-1, -2, -3, -4, -5]
        mos = MosAlgorithm(array)
        queries = [Query(0, 2, 0)]
        results = mos.range_sum_queries(queries)
        assert results[0] == -6

    def test_duplicate_values(self) -> None:
        """Test with duplicate values."""
        array = [1, 1, 1, 2, 2, 3]
        mos = MosAlgorithm(array)
        queries = [Query(0, 5, 0)]
        results = mos.range_distinct_count_queries(queries)
        assert results[0] == 3

    def test_process_queries_custom(self) -> None:
        """Test process_queries with custom functions."""
        array = [1, 2, 3, 4, 5]
        mos = MosAlgorithm(array)
        queries = [Query(0, 2, 0)]

        count = 0

        def add(index: int) -> None:
            nonlocal count
            count += 1

        def remove(index: int) -> None:
            nonlocal count
            count -= 1

        def get_result() -> int:
            return count

        results = mos.process_queries(queries, add, remove, get_result)
        assert results[0] == 3

    def test_sum_verification(self) -> None:
        """Test that sum queries match naive computation."""
        array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        mos = MosAlgorithm(array)
        queries = [
            Query(0, 2, 0),
            Query(1, 4, 1),
            Query(2, 6, 2),
            Query(0, 9, 3),
        ]

        results = mos.range_sum_queries(queries)

        for query, result in zip(queries, results):
            expected = sum(array[query.left : query.right + 1])
            assert result == expected, f"Query {query}: expected {expected}, got {result}"

    def test_distinct_verification(self) -> None:
        """Test that distinct count matches naive computation."""
        array = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
        mos = MosAlgorithm(array)
        queries = [Query(0, 2, 0), Query(1, 5, 1), Query(0, 9, 2)]

        results = mos.range_distinct_count_queries(queries)

        for query, result in zip(queries, results):
            expected = len(set(array[query.left : query.right + 1]))
            assert result == expected, f"Query {query}: expected {expected}, got {result}"
