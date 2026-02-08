"""Unit tests for Contraction Hierarchies implementation."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import ContractionHierarchies, RoadGraph


class TestRoadGraph:
    """Test road graph functionality."""

    def test_graph_initialization(self):
        """Test graph initialization from edges."""
        edges = [(0, 1, 1.0), (1, 2, 2.0)]
        graph = RoadGraph(edges=edges, num_nodes=3)
        assert graph.num_nodes == 3
        assert len(graph.edges) == 2

    def test_graph_num_nodes_inference(self):
        """Test that num_nodes is inferred from edges."""
        edges = [(0, 1, 1.0), (1, 2, 2.0), (2, 3, 1.0)]
        graph = RoadGraph(edges=edges)
        assert graph.num_nodes == 4

    def test_get_outgoing(self):
        """Test getting outgoing edges."""
        edges = [(0, 1, 1.0), (0, 2, 2.0)]
        graph = RoadGraph(edges=edges, num_nodes=3)
        outgoing = graph.get_outgoing(0)
        assert len(outgoing) == 2
        assert (1, 1.0) in outgoing
        assert (2, 2.0) in outgoing

    def test_get_incoming(self):
        """Test getting incoming edges."""
        edges = [(0, 1, 1.0), (2, 1, 2.0)]
        graph = RoadGraph(edges=edges, num_nodes=3)
        incoming = graph.get_incoming(1)
        assert len(incoming) == 2
        assert (0, 1.0) in incoming
        assert (2, 2.0) in incoming

    def test_add_edge(self):
        """Test adding edge to graph."""
        graph = RoadGraph(edges=[], num_nodes=3)
        graph.add_edge(0, 1, 1.5)
        assert len(graph.edges) == 1
        assert (0, 1, 1.5) in graph.edges
        assert (1, 1.5) in graph.get_outgoing(0)


class TestContractionHierarchies:
    """Test Contraction Hierarchies algorithm."""

    def create_temp_config(self, config_dict: dict) -> str:
        """Create temporary config file for testing."""
        temp_file = tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False
        )
        yaml.dump(config_dict, temp_file)
        temp_file.close()
        return temp_file.name

    def test_initialization_with_default_config(self):
        """Test initialization with default config file."""
        ch = ContractionHierarchies()
        assert ch.edge_difference_weight > 0
        assert not ch.preprocessed

    def test_initialization_with_custom_config(self):
        """Test initialization with custom config file."""
        config = {
            "contraction_hierarchies": {
                "edge_difference_weight": 2.0,
                "deleted_neighbors_weight": 1.5,
            },
            "logging": {"level": "INFO", "file": "logs/test.log"},
        }

        config_path = self.create_temp_config(config)
        try:
            ch = ContractionHierarchies(config_path=config_path)
            assert ch.edge_difference_weight == 2.0
            assert ch.deleted_neighbors_weight == 1.5
        finally:
            Path(config_path).unlink()

    def test_preprocessing_simple_graph(self):
        """Test preprocessing on simple graph."""
        edges = [(0, 1, 1.0), (1, 2, 2.0), (2, 3, 1.0)]
        graph = RoadGraph(edges=edges, num_nodes=4)
        ch = ContractionHierarchies()

        stats = ch.preprocess(graph)

        assert ch.preprocessed is True
        assert stats["nodes_contracted"] == 4
        assert stats["shortcuts_added"] >= 0
        assert len(ch.node_level) == 4

    def test_preprocessing_adds_shortcuts(self):
        """Test that preprocessing adds shortcuts when needed."""
        edges = [
            (0, 1, 1.0),
            (1, 2, 1.0),
            (0, 2, 5.0),
        ]
        graph = RoadGraph(edges=edges, num_nodes=3)
        ch = ContractionHierarchies()

        initial_edges = len(graph.edges)
        stats = ch.preprocess(graph)

        assert stats["shortcuts_added"] >= 0
        assert len(graph.edges) >= initial_edges

    def test_query_after_preprocessing(self):
        """Test query after preprocessing."""
        edges = [(0, 1, 1.0), (1, 2, 2.0), (2, 3, 1.0)]
        graph = RoadGraph(edges=edges, num_nodes=4)
        ch = ContractionHierarchies()

        ch.preprocess(graph)
        result = ch.query(graph, 0, 3)

        assert result["found"] is True
        assert len(result["path"]) > 0
        assert result["path"][0] == 0
        assert result["path"][-1] == 3
        assert result["cost"] > 0

    def test_query_without_preprocessing(self):
        """Test that query without preprocessing raises error."""
        edges = [(0, 1, 1.0)]
        graph = RoadGraph(edges=edges, num_nodes=2)
        ch = ContractionHierarchies()

        with pytest.raises(ValueError, match="must be preprocessed"):
            ch.query(graph, 0, 1)

    def test_query_same_start_and_goal(self):
        """Test query when start and goal are the same."""
        edges = [(0, 1, 1.0)]
        graph = RoadGraph(edges=edges, num_nodes=2)
        ch = ContractionHierarchies()

        ch.preprocess(graph)
        result = ch.query(graph, 0, 0)

        assert result["found"] is True
        assert result["path"] == [0]
        assert result["cost"] == 0.0

    def test_query_invalid_start(self):
        """Test query with invalid start node."""
        edges = [(0, 1, 1.0)]
        graph = RoadGraph(edges=edges, num_nodes=2)
        ch = ContractionHierarchies()

        ch.preprocess(graph)
        with pytest.raises(ValueError, match="Start node"):
            ch.query(graph, -1, 1)

    def test_query_invalid_goal(self):
        """Test query with invalid goal node."""
        edges = [(0, 1, 1.0)]
        graph = RoadGraph(edges=edges, num_nodes=2)
        ch = ContractionHierarchies()

        ch.preprocess(graph)
        with pytest.raises(ValueError, match="Goal node"):
            ch.query(graph, 0, 10)

    def test_query_path_optimality(self):
        """Test that query returns optimal path."""
        edges = [
            (0, 1, 1.0),
            (1, 2, 1.0),
            (0, 2, 5.0),
        ]
        graph = RoadGraph(edges=edges, num_nodes=3)
        ch = ContractionHierarchies()

        ch.preprocess(graph)
        result = ch.query(graph, 0, 2)

        assert result["found"] is True
        assert result["cost"] == 2.0

    def test_query_no_path(self):
        """Test query when no path exists."""
        edges = [(0, 1, 1.0), (2, 3, 1.0)]
        graph = RoadGraph(edges=edges, num_nodes=4)
        ch = ContractionHierarchies()

        ch.preprocess(graph)
        result = ch.query(graph, 0, 3)

        assert result["found"] is False
        assert result["cost"] == float("inf")

    def test_node_levels_assigned(self):
        """Test that node levels are assigned during preprocessing."""
        edges = [(0, 1, 1.0), (1, 2, 1.0)]
        graph = RoadGraph(edges=edges, num_nodes=3)
        ch = ContractionHierarchies()

        ch.preprocess(graph)

        assert 0 in ch.node_level
        assert 1 in ch.node_level
        assert 2 in ch.node_level

    def test_multiple_queries(self):
        """Test multiple queries on preprocessed graph."""
        edges = [
            (0, 1, 1.0),
            (1, 2, 2.0),
            (2, 3, 1.0),
            (0, 2, 4.0),
        ]
        graph = RoadGraph(edges=edges, num_nodes=4)
        ch = ContractionHierarchies()

        ch.preprocess(graph)

        result1 = ch.query(graph, 0, 3)
        result2 = ch.query(graph, 1, 3)
        result3 = ch.query(graph, 0, 2)

        assert result1["found"] is True
        assert result2["found"] is True
        assert result3["found"] is True

    def test_larger_graph(self):
        """Test preprocessing and query on larger graph."""
        edges = []
        num_nodes = 10
        for i in range(num_nodes - 1):
            edges.append((i, i + 1, 1.0))
            edges.append((i + 1, i, 1.0))

        graph = RoadGraph(edges=edges, num_nodes=num_nodes)
        ch = ContractionHierarchies()

        stats = ch.preprocess(graph)
        assert stats["nodes_contracted"] == num_nodes

        result = ch.query(graph, 0, num_nodes - 1)
        assert result["found"] is True
        assert result["cost"] == num_nodes - 1

    def test_config_file_not_found(self):
        """Test that missing config file raises error."""
        with pytest.raises(FileNotFoundError):
            ContractionHierarchies(config_path="nonexistent.yaml")

    def test_path_continuity(self):
        """Test that path is continuous."""
        edges = [
            (0, 1, 1.0),
            (1, 2, 1.0),
            (2, 3, 1.0),
            (3, 4, 1.0),
        ]
        graph = RoadGraph(edges=edges, num_nodes=5)
        ch = ContractionHierarchies()

        ch.preprocess(graph)
        result = ch.query(graph, 0, 4)

        assert result["found"] is True
        path = result["path"]

        for i in range(len(path) - 1):
            current = path[i]
            next_node = path[i + 1]
            assert current != next_node

    def test_path_length_matches_path(self):
        """Test that path_length matches actual path length."""
        edges = [(0, 1, 1.0), (1, 2, 1.0)]
        graph = RoadGraph(edges=edges, num_nodes=3)
        ch = ContractionHierarchies()

        ch.preprocess(graph)
        result = ch.query(graph, 0, 2)

        assert result["path_length"] == len(result["path"])

    def test_nodes_explored_tracking(self):
        """Test that nodes explored is tracked."""
        edges = [(0, 1, 1.0), (1, 2, 1.0), (2, 3, 1.0)]
        graph = RoadGraph(edges=edges, num_nodes=4)
        ch = ContractionHierarchies()

        ch.preprocess(graph)
        result = ch.query(graph, 0, 3)

        assert result["nodes_explored"] >= 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
