"""Unit tests for heap data structure module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import MinHeap, MaxHeap, HeapSort


class TestMinHeap:
    """Test cases for MinHeap class."""

    def test_minheap_empty(self):
        """Test empty min-heap."""
        heap = MinHeap()
        assert heap.is_empty()
        assert heap.size() == 0
        assert heap.peek() is None
        assert heap.extract_min() is None

    def test_minheap_insert_single(self):
        """Test inserting single element."""
        heap = MinHeap()
        heap.insert(5)
        assert heap.size() == 1
        assert heap.peek() == 5
        assert not heap.is_empty()

    def test_minheap_insert_multiple(self):
        """Test inserting multiple elements."""
        heap = MinHeap()
        heap.insert(5)
        heap.insert(2)
        heap.insert(8)
        assert heap.size() == 3
        assert heap.peek() == 2

    def test_minheap_extract_min(self):
        """Test extracting minimum element."""
        heap = MinHeap()
        heap.insert(5)
        heap.insert(2)
        heap.insert(8)
        heap.insert(1)
        assert heap.extract_min() == 1
        assert heap.extract_min() == 2
        assert heap.extract_min() == 5
        assert heap.extract_min() == 8
        assert heap.is_empty()

    def test_minheap_build_heap(self):
        """Test building heap from array."""
        items = [5, 2, 8, 1, 9, 3]
        heap = MinHeap(items)
        assert heap.size() == 6
        assert heap.peek() == 1

    def test_minheap_extract_all(self):
        """Test extracting all elements in order."""
        items = [5, 2, 8, 1, 9, 3]
        heap = MinHeap(items)
        extracted = []
        while not heap.is_empty():
            extracted.append(heap.extract_min())
        assert extracted == [1, 2, 3, 5, 8, 9]

    def test_minheap_duplicates(self):
        """Test heap with duplicate values."""
        heap = MinHeap()
        heap.insert(5)
        heap.insert(2)
        heap.insert(5)
        heap.insert(2)
        assert heap.extract_min() == 2
        assert heap.extract_min() == 2
        assert heap.extract_min() == 5
        assert heap.extract_min() == 5

    def test_minheap_single_element(self):
        """Test heap with single element."""
        heap = MinHeap([5])
        assert heap.peek() == 5
        assert heap.extract_min() == 5
        assert heap.is_empty()

    def test_minheap_already_sorted(self):
        """Test building heap from already sorted array."""
        items = [1, 2, 3, 4, 5]
        heap = MinHeap(items)
        assert heap.peek() == 1
        extracted = []
        while not heap.is_empty():
            extracted.append(heap.extract_min())
        assert extracted == [1, 2, 3, 4, 5]

    def test_minheap_reverse_sorted(self):
        """Test building heap from reverse sorted array."""
        items = [5, 4, 3, 2, 1]
        heap = MinHeap(items)
        assert heap.peek() == 1
        extracted = []
        while not heap.is_empty():
            extracted.append(heap.extract_min())
        assert extracted == [1, 2, 3, 4, 5]

    def test_minheap_negative_numbers(self):
        """Test heap with negative numbers."""
        items = [-5, -2, -8, -1, -9]
        heap = MinHeap(items)
        assert heap.peek() == -9
        assert heap.extract_min() == -9

    def test_minheap_floats(self):
        """Test heap with floating point numbers."""
        items = [5.5, 2.2, 8.8, 1.1, 9.9]
        heap = MinHeap(items)
        assert heap.peek() == 1.1
        assert heap.extract_min() == 1.1


class TestMaxHeap:
    """Test cases for MaxHeap class."""

    def test_maxheap_empty(self):
        """Test empty max-heap."""
        heap = MaxHeap()
        assert heap.is_empty()
        assert heap.size() == 0
        assert heap.peek() is None
        assert heap.extract_max() is None

    def test_maxheap_insert_single(self):
        """Test inserting single element."""
        heap = MaxHeap()
        heap.insert(5)
        assert heap.size() == 1
        assert heap.peek() == 5
        assert not heap.is_empty()

    def test_maxheap_insert_multiple(self):
        """Test inserting multiple elements."""
        heap = MaxHeap()
        heap.insert(5)
        heap.insert(2)
        heap.insert(8)
        assert heap.size() == 3
        assert heap.peek() == 8

    def test_maxheap_extract_max(self):
        """Test extracting maximum element."""
        heap = MaxHeap()
        heap.insert(5)
        heap.insert(2)
        heap.insert(8)
        heap.insert(1)
        assert heap.extract_max() == 8
        assert heap.extract_max() == 5
        assert heap.extract_max() == 2
        assert heap.extract_max() == 1
        assert heap.is_empty()

    def test_maxheap_build_heap(self):
        """Test building heap from array."""
        items = [5, 2, 8, 1, 9, 3]
        heap = MaxHeap(items)
        assert heap.size() == 6
        assert heap.peek() == 9

    def test_maxheap_extract_all(self):
        """Test extracting all elements in order."""
        items = [5, 2, 8, 1, 9, 3]
        heap = MaxHeap(items)
        extracted = []
        while not heap.is_empty():
            extracted.append(heap.extract_max())
        assert extracted == [9, 8, 5, 3, 2, 1]

    def test_maxheap_duplicates(self):
        """Test heap with duplicate values."""
        heap = MaxHeap()
        heap.insert(5)
        heap.insert(2)
        heap.insert(5)
        heap.insert(2)
        assert heap.extract_max() == 5
        assert heap.extract_max() == 5
        assert heap.extract_max() == 2
        assert heap.extract_max() == 2

    def test_maxheap_single_element(self):
        """Test heap with single element."""
        heap = MaxHeap([5])
        assert heap.peek() == 5
        assert heap.extract_max() == 5
        assert heap.is_empty()

    def test_maxheap_already_sorted(self):
        """Test building heap from already sorted array."""
        items = [1, 2, 3, 4, 5]
        heap = MaxHeap(items)
        assert heap.peek() == 5
        extracted = []
        while not heap.is_empty():
            extracted.append(heap.extract_max())
        assert extracted == [5, 4, 3, 2, 1]

    def test_maxheap_reverse_sorted(self):
        """Test building heap from reverse sorted array."""
        items = [5, 4, 3, 2, 1]
        heap = MaxHeap(items)
        assert heap.peek() == 5
        extracted = []
        while not heap.is_empty():
            extracted.append(heap.extract_max())
        assert extracted == [5, 4, 3, 2, 1]

    def test_maxheap_negative_numbers(self):
        """Test heap with negative numbers."""
        items = [-5, -2, -8, -1, -9]
        heap = MaxHeap(items)
        assert heap.peek() == -1
        assert heap.extract_max() == -1

    def test_maxheap_floats(self):
        """Test heap with floating point numbers."""
        items = [5.5, 2.2, 8.8, 1.1, 9.9]
        heap = MaxHeap(items)
        assert heap.peek() == 9.9
        assert heap.extract_max() == 9.9


class TestHeapSort:
    """Test cases for HeapSort class."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for testing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.fixture
    def config_file(self, temp_dir):
        """Create temporary config file."""
        config = {
            "logging": {"level": "INFO", "file": str(temp_dir / "app.log")},
        }
        config_path = temp_dir / "config.yaml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)
        return str(config_path)

    @pytest.fixture
    def heap_sort(self, config_file):
        """Create HeapSort instance."""
        return HeapSort(config_path=config_file)

    def test_sort_ascending_empty(self, heap_sort):
        """Test sorting empty array."""
        result = heap_sort.sort_ascending([])
        assert result == []

    def test_sort_ascending_single(self, heap_sort):
        """Test sorting single element."""
        result = heap_sort.sort_ascending([5])
        assert result == [5]

    def test_sort_ascending_simple(self, heap_sort):
        """Test sorting simple array."""
        result = heap_sort.sort_ascending([5, 2, 8, 1, 9, 3])
        assert result == [1, 2, 3, 5, 8, 9]

    def test_sort_ascending_already_sorted(self, heap_sort):
        """Test sorting already sorted array."""
        result = heap_sort.sort_ascending([1, 2, 3, 4, 5])
        assert result == [1, 2, 3, 4, 5]

    def test_sort_ascending_reverse_sorted(self, heap_sort):
        """Test sorting reverse sorted array."""
        result = heap_sort.sort_ascending([5, 4, 3, 2, 1])
        assert result == [1, 2, 3, 4, 5]

    def test_sort_ascending_duplicates(self, heap_sort):
        """Test sorting array with duplicates."""
        result = heap_sort.sort_ascending([5, 2, 5, 2, 1])
        assert result == [1, 2, 2, 5, 5]

    def test_sort_descending_empty(self, heap_sort):
        """Test sorting empty array descending."""
        result = heap_sort.sort_descending([])
        assert result == []

    def test_sort_descending_single(self, heap_sort):
        """Test sorting single element descending."""
        result = heap_sort.sort_descending([5])
        assert result == [5]

    def test_sort_descending_simple(self, heap_sort):
        """Test sorting simple array descending."""
        result = heap_sort.sort_descending([5, 2, 8, 1, 9, 3])
        assert result == [9, 8, 5, 3, 2, 1]

    def test_sort_descending_already_sorted(self, heap_sort):
        """Test sorting already sorted array descending."""
        result = heap_sort.sort_descending([5, 4, 3, 2, 1])
        assert result == [5, 4, 3, 2, 1]

    def test_sort_descending_reverse_sorted(self, heap_sort):
        """Test sorting reverse sorted array descending."""
        result = heap_sort.sort_descending([1, 2, 3, 4, 5])
        assert result == [5, 4, 3, 2, 1]

    def test_sort_descending_duplicates(self, heap_sort):
        """Test sorting array with duplicates descending."""
        result = heap_sort.sort_descending([5, 2, 5, 2, 1])
        assert result == [5, 5, 2, 2, 1]

    def test_compare_with_builtin(self, heap_sort):
        """Test comparison with built-in sorted."""
        arr = [5, 2, 8, 1, 9, 3]
        comparison = heap_sort.compare_with_builtin(arr)
        assert comparison["array_length"] == 6
        assert comparison["heap_sort_asc"]["success"] is True
        assert comparison["heap_sort_desc"]["success"] is True
        assert comparison["builtin_sorted"]["success"] is True
        assert comparison["heap_sort_asc"]["result"] == [1, 2, 3, 5, 8, 9]
        assert comparison["builtin_sorted"]["result"] == [1, 2, 3, 5, 8, 9]

    def test_compare_with_builtin_with_iterations(self, heap_sort):
        """Test comparison with multiple iterations."""
        arr = [5, 2, 8, 1, 9, 3]
        comparison = heap_sort.compare_with_builtin(arr, iterations=10)
        assert comparison["iterations"] == 10
        assert comparison["heap_sort_asc"]["success"] is True

    def test_sort_ascending_negative(self, heap_sort):
        """Test sorting array with negative numbers."""
        result = heap_sort.sort_ascending([-5, -2, -8, -1, -9])
        assert result == [-9, -8, -5, -2, -1]

    def test_sort_descending_negative(self, heap_sort):
        """Test sorting array with negative numbers descending."""
        result = heap_sort.sort_descending([-5, -2, -8, -1, -9])
        assert result == [-1, -2, -5, -8, -9]

    def test_sort_ascending_floats(self, heap_sort):
        """Test sorting array with floating point numbers."""
        result = heap_sort.sort_ascending([5.5, 2.2, 8.8, 1.1, 9.9])
        assert result == [1.1, 2.2, 5.5, 8.8, 9.9]

    def test_sort_descending_floats(self, heap_sort):
        """Test sorting array with floating point numbers descending."""
        result = heap_sort.sort_descending([5.5, 2.2, 8.8, 1.1, 9.9])
        assert result == [9.9, 8.8, 5.5, 2.2, 1.1]

    def test_sort_ascending_large(self, heap_sort):
        """Test sorting large array."""
        arr = list(range(100, 0, -1))
        result = heap_sort.sort_ascending(arr)
        assert result == list(range(1, 101))

    def test_sort_descending_large(self, heap_sort):
        """Test sorting large array descending."""
        arr = list(range(1, 101))
        result = heap_sort.sort_descending(arr)
        assert result == list(range(100, 0, -1))
