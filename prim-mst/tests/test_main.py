"""Unit tests for Prim's algorithm module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import PrimMST, MinHeap


class TestMinHeap:
    """Test cases for MinHeap class."""

    def test_minheap_empty(self):
        """Test empty min-heap."""
        heap = MinHeap()
        assert heap.is_empty()
        assert heap.extract_min() is None

    def test_minheap_insert_extract(self):
        """Test insert and extract operations."""
        heap = MinHeap()
        heap.insert(5.0, 0)
        heap.insert(2.0, 1)
        heap.insert(8.0, 2)
        assert not heap.is_empty()
        weight, vertex = heap.extract_min()
        assert weight == 2.0
        assert vertex == 1

    def test_minheap_multiple_extracts(self):
        """Test multiple extract operations."""
        heap = MinHeap()
        heap.insert(5.0, 0)
        heap.insert(2.0, 1)
        heap.insert(8.0, 2)
        heap.insert(1.0, 3)
        extracted = []
        while not heap.is_empty():
            extracted.append(heap.extract_min())
        weights = [w for w, v in extracted]
        assert weights == [1.0, 2.0, 5.0, 8.0]


class TestPrimMST:
    """Test cases for PrimMST class."""

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
    def prim(self, config_file):
        """Create PrimMST instance."""
        return PrimMST(config_path=config_file)

    def test_find_mst_list_simple(self, prim):
        """Test finding MST using list-based approach."""
        edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3), (0, 3, 4)]
        mst_edges, total_weight = prim.find_mst_list(4, edges)
        assert len(mst_edges) == 3
        assert total_weight == 6.0

    def test_find_mst_heap_simple(self, prim):
        """Test finding MST using heap-based approach."""
        edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3), (0, 3, 4)]
        mst_edges, total_weight = prim.find_mst_heap(4, edges)
        assert len(mst_edges) == 3
        assert total_weight == 6.0

    def test_find_mst_list_empty_graph(self, prim):
        """Test finding MST for empty graph."""
        mst_edges, total_weight = prim.find_mst_list(0, [])
        assert mst_edges == []
        assert total_weight == 0.0

    def test_find_mst_heap_empty_graph(self, prim):
        """Test finding MST for empty graph."""
        mst_edges, total_weight = prim.find_mst_heap(0, [])
        assert mst_edges == []
        assert total_weight == 0.0

    def test_find_mst_list_single_vertex(self, prim):
        """Test finding MST for single vertex."""
        mst_edges, total_weight = prim.find_mst_list(1, [])
        assert mst_edges == []
        assert total_weight == 0.0

    def test_find_mst_heap_single_vertex(self, prim):
        """Test finding MST for single vertex."""
        mst_edges, total_weight = prim.find_mst_heap(1, [])
        assert mst_edges == []
        assert total_weight == 0.0

    def test_find_mst_list_disconnected(self, prim):
        """Test finding MST for disconnected graph."""
        edges = [(0, 1, 1), (2, 3, 2)]
        with pytest.raises(ValueError, match="disconnected"):
            prim.find_mst_list(4, edges)

    def test_find_mst_heap_disconnected(self, prim):
        """Test finding MST for disconnected graph."""
        edges = [(0, 1, 1), (2, 3, 2)]
        with pytest.raises(ValueError, match="disconnected"):
            prim.find_mst_heap(4, edges)

    def test_find_mst_list_complete_graph(self, prim):
        """Test finding MST for complete graph."""
        edges = [
            (0, 1, 1),
            (0, 2, 2),
            (0, 3, 3),
            (1, 2, 4),
            (1, 3, 5),
            (2, 3, 6),
        ]
        mst_edges, total_weight = prim.find_mst_list(4, edges)
        assert len(mst_edges) == 3
        assert total_weight == 6.0

    def test_find_mst_heap_complete_graph(self, prim):
        """Test finding MST for complete graph."""
        edges = [
            (0, 1, 1),
            (0, 2, 2),
            (0, 3, 3),
            (1, 2, 4),
            (1, 3, 5),
            (2, 3, 6),
        ]
        mst_edges, total_weight = prim.find_mst_heap(4, edges)
        assert len(mst_edges) == 3
        assert total_weight == 6.0

    def test_find_mst_list_negative_weights(self, prim):
        """Test finding MST with negative weights."""
        edges = [(0, 1, -1), (1, 2, -2), (2, 3, -3), (0, 3, -4)]
        mst_edges, total_weight = prim.find_mst_list(4, edges)
        assert len(mst_edges) == 3
        assert total_weight == -9.0

    def test_find_mst_heap_negative_weights(self, prim):
        """Test finding MST with negative weights."""
        edges = [(0, 1, -1), (1, 2, -2), (2, 3, -3), (0, 3, -4)]
        mst_edges, total_weight = prim.find_mst_heap(4, edges)
        assert len(mst_edges) == 3
        assert total_weight == -9.0

    def test_find_mst_list_invalid_vertex(self, prim):
        """Test finding MST with invalid vertex."""
        edges = [(0, 1, 1), (1, 10, 2)]
        with pytest.raises(ValueError, match="out of range"):
            prim.find_mst_list(4, edges)

    def test_find_mst_heap_invalid_vertex(self, prim):
        """Test finding MST with invalid vertex."""
        edges = [(0, 1, 1), (1, 10, 2)]
        with pytest.raises(ValueError, match="out of range"):
            prim.find_mst_heap(4, edges)

    def test_find_mst_list_self_loop(self, prim):
        """Test finding MST with self-loop."""
        edges = [(0, 0, 1), (0, 1, 2)]
        with pytest.raises(ValueError, match="Self-loops"):
            prim.find_mst_list(2, edges)

    def test_find_mst_heap_self_loop(self, prim):
        """Test finding MST with self-loop."""
        edges = [(0, 0, 1), (0, 1, 2)]
        with pytest.raises(ValueError, match="Self-loops"):
            prim.find_mst_heap(2, edges)

    def test_find_mst_list_invalid_start_vertex(self, prim):
        """Test finding MST with invalid start vertex."""
        edges = [(0, 1, 1), (1, 2, 2)]
        with pytest.raises(ValueError, match="out of range"):
            prim.find_mst_list(3, edges, start_vertex=5)

    def test_find_mst_heap_invalid_start_vertex(self, prim):
        """Test finding MST with invalid start vertex."""
        edges = [(0, 1, 1), (1, 2, 2)]
        with pytest.raises(ValueError, match="out of range"):
            prim.find_mst_heap(3, edges, start_vertex=5)

    def test_find_mst_list_different_start(self, prim):
        """Test finding MST with different start vertex."""
        edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3), (0, 3, 4)]
        mst_edges1, weight1 = prim.find_mst_list(4, edges, start_vertex=0)
        mst_edges2, weight2 = prim.find_mst_list(4, edges, start_vertex=2)
        assert weight1 == weight2
        assert len(mst_edges1) == len(mst_edges2)

    def test_find_mst_heap_different_start(self, prim):
        """Test finding MST with different start vertex."""
        edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3), (0, 3, 4)]
        mst_edges1, weight1 = prim.find_mst_heap(4, edges, start_vertex=0)
        mst_edges2, weight2 = prim.find_mst_heap(4, edges, start_vertex=2)
        assert weight1 == weight2
        assert len(mst_edges1) == len(mst_edges2)

    def test_get_mst_edges_list(self, prim):
        """Test getting MST edges using list-based approach."""
        edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3), (0, 3, 4)]
        mst_edges = prim.get_mst_edges_list(4, edges)
        assert len(mst_edges) == 3

    def test_get_mst_edges_heap(self, prim):
        """Test getting MST edges using heap-based approach."""
        edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3), (0, 3, 4)]
        mst_edges = prim.get_mst_edges_heap(4, edges)
        assert len(mst_edges) == 3

    def test_get_mst_weight_list(self, prim):
        """Test getting MST weight using list-based approach."""
        edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3), (0, 3, 4)]
        total_weight = prim.get_mst_weight_list(4, edges)
        assert total_weight == 6.0

    def test_get_mst_weight_heap(self, prim):
        """Test getting MST weight using heap-based approach."""
        edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3), (0, 3, 4)]
        total_weight = prim.get_mst_weight_heap(4, edges)
        assert total_weight == 6.0

    def test_compare_approaches(self, prim):
        """Test comparing list-based and heap-based approaches."""
        edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3), (0, 3, 4)]
        comparison = prim.compare_approaches(4, edges)
        assert comparison["num_vertices"] == 4
        assert comparison["num_edges"] == 4
        assert comparison["list_based"]["success"] is True
        assert comparison["heap_based"]["success"] is True
        assert abs(
            comparison["list_based"]["total_weight"]
            - comparison["heap_based"]["total_weight"]
        ) < 0.001

    def test_compare_approaches_with_iterations(self, prim):
        """Test comparison with multiple iterations."""
        edges = [(0, 1, 1), (1, 2, 2)]
        comparison = prim.compare_approaches(3, edges, iterations=10)
        assert comparison["iterations"] == 10
        assert comparison["list_based"]["success"] is True
        assert comparison["heap_based"]["success"] is True

    def test_compare_approaches_different_start(self, prim):
        """Test comparison with different start vertex."""
        edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3)]
        comparison = prim.compare_approaches(4, edges, start_vertex=2)
        assert comparison["start_vertex"] == 2
        assert comparison["list_based"]["success"] is True
        assert comparison["heap_based"]["success"] is True

    def test_generate_report_success(self, prim, temp_dir):
        """Test report generation."""
        edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3)]
        comparison = prim.compare_approaches(4, edges)
        report_path = temp_dir / "report.txt"

        report = prim.generate_report(comparison, output_path=str(report_path))

        assert "PRIM'S" in report
        assert "LIST-BASED" in report
        assert "HEAP-BASED" in report
        assert report_path.exists()

    def test_generate_report_no_output(self, prim):
        """Test report generation without saving to file."""
        edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3)]
        comparison = prim.compare_approaches(4, edges)
        report = prim.generate_report(comparison)

        assert "PRIM'S" in report
        assert "LIST-BASED" in report
        assert "HEAP-BASED" in report

    def test_find_mst_list_large_graph(self, prim):
        """Test finding MST for larger graph."""
        edges = [(i, i + 1, i + 1) for i in range(9)]
        mst_edges, total_weight = prim.find_mst_list(10, edges)
        assert len(mst_edges) == 9
        assert total_weight == sum(range(1, 10))

    def test_find_mst_heap_large_graph(self, prim):
        """Test finding MST for larger graph."""
        edges = [(i, i + 1, i + 1) for i in range(9)]
        mst_edges, total_weight = prim.find_mst_heap(10, edges)
        assert len(mst_edges) == 9
        assert total_weight == sum(range(1, 10))

    def test_find_mst_list_floating_point_weights(self, prim):
        """Test finding MST with floating point weights."""
        edges = [
            (0, 1, 1.5),
            (1, 2, 2.5),
            (2, 3, 3.5),
            (0, 3, 4.5),
        ]
        mst_edges, total_weight = prim.find_mst_list(4, edges)
        assert len(mst_edges) == 3
        assert abs(total_weight - 7.5) < 0.001

    def test_find_mst_heap_floating_point_weights(self, prim):
        """Test finding MST with floating point weights."""
        edges = [
            (0, 1, 1.5),
            (1, 2, 2.5),
            (2, 3, 3.5),
            (0, 3, 4.5),
        ]
        mst_edges, total_weight = prim.find_mst_heap(4, edges)
        assert len(mst_edges) == 3
        assert abs(total_weight - 7.5) < 0.001

    def test_find_mst_list_negative_num_vertices(self, prim):
        """Test finding MST with negative number of vertices."""
        with pytest.raises(ValueError, match="non-negative"):
            prim.find_mst_list(-1, [])

    def test_find_mst_heap_negative_num_vertices(self, prim):
        """Test finding MST with negative number of vertices."""
        with pytest.raises(ValueError, match="non-negative"):
            prim.find_mst_heap(-1, [])
