"""Unit tests for maximum flow module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import FlowNetwork, MaxFlowSolver


class TestFlowNetwork:
    """Test cases for FlowNetwork class."""

    def test_flow_network_creation(self):
        """Test FlowNetwork creation."""
        network = FlowNetwork(5)
        assert network.num_vertices == 5
        assert len(network.graph) == 5
        assert len(network.residual) == 5

    def test_flow_network_invalid_vertices(self):
        """Test FlowNetwork creation with invalid vertices."""
        with pytest.raises(ValueError):
            FlowNetwork(0)
        with pytest.raises(ValueError):
            FlowNetwork(1)

    def test_add_edge(self):
        """Test adding edge to network."""
        network = FlowNetwork(5)
        network.add_edge(0, 1, 10)
        assert network.get_capacity(0, 1) == 10
        assert network.get_residual_capacity(0, 1) == 10

    def test_add_edge_invalid_vertices(self):
        """Test adding edge with invalid vertices."""
        network = FlowNetwork(5)
        with pytest.raises(ValueError):
            network.add_edge(-1, 1, 10)
        with pytest.raises(ValueError):
            network.add_edge(0, 10, 10)

    def test_add_edge_negative_capacity(self):
        """Test adding edge with negative capacity."""
        network = FlowNetwork(5)
        with pytest.raises(ValueError):
            network.add_edge(0, 1, -5)

    def test_get_capacity_nonexistent(self):
        """Test getting capacity of nonexistent edge."""
        network = FlowNetwork(5)
        assert network.get_capacity(0, 1) == 0

    def test_update_residual(self):
        """Test updating residual capacities."""
        network = FlowNetwork(5)
        network.add_edge(0, 1, 10)
        network.update_residual(0, 1, 5)
        assert network.get_residual_capacity(0, 1) == 5
        assert network.get_residual_capacity(1, 0) == 5


class TestMaxFlowSolver:
    """Test cases for MaxFlowSolver class."""

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
    def simple_network(self):
        """Create simple flow network."""
        network = FlowNetwork(4)
        network.add_edge(0, 1, 10)
        network.add_edge(0, 2, 10)
        network.add_edge(1, 3, 10)
        network.add_edge(2, 3, 10)
        return network

    @pytest.fixture
    def complex_network(self):
        """Create complex flow network."""
        network = FlowNetwork(6)
        network.add_edge(0, 1, 16)
        network.add_edge(0, 2, 13)
        network.add_edge(1, 2, 10)
        network.add_edge(1, 3, 12)
        network.add_edge(2, 1, 4)
        network.add_edge(2, 4, 14)
        network.add_edge(3, 2, 9)
        network.add_edge(3, 5, 20)
        network.add_edge(4, 3, 7)
        network.add_edge(4, 5, 4)
        return network

    def test_ford_fulkerson_simple(self, simple_network):
        """Test Ford-Fulkerson on simple network."""
        solver = MaxFlowSolver(simple_network)
        max_flow, flow_dict = solver.ford_fulkerson(0, 3)
        assert max_flow == 20
        assert isinstance(flow_dict, dict)

    def test_edmonds_karp_simple(self, simple_network):
        """Test Edmonds-Karp on simple network."""
        solver = MaxFlowSolver(simple_network)
        max_flow, flow_dict = solver.edmonds_karp(0, 3)
        assert max_flow == 20
        assert isinstance(flow_dict, dict)

    def test_dinic_simple(self, simple_network):
        """Test Dinic's on simple network."""
        solver = MaxFlowSolver(simple_network)
        max_flow, flow_dict = solver.dinic(0, 3)
        assert max_flow == 20
        assert isinstance(flow_dict, dict)

    def test_all_algorithms_same_result(self, simple_network):
        """Test all algorithms produce same result."""
        solver = MaxFlowSolver(simple_network)
        flow_ff, _ = solver.ford_fulkerson(0, 3)
        flow_ek, _ = solver.edmonds_karp(0, 3)
        flow_dinic, _ = solver.dinic(0, 3)
        assert flow_ff == flow_ek == flow_dinic

    def test_ford_fulkerson_complex(self, complex_network):
        """Test Ford-Fulkerson on complex network."""
        solver = MaxFlowSolver(complex_network)
        max_flow, flow_dict = solver.ford_fulkerson(0, 5)
        assert max_flow == 23
        assert isinstance(flow_dict, dict)

    def test_edmonds_karp_complex(self, complex_network):
        """Test Edmonds-Karp on complex network."""
        solver = MaxFlowSolver(complex_network)
        max_flow, flow_dict = solver.edmonds_karp(0, 5)
        assert max_flow == 23
        assert isinstance(flow_dict, dict)

    def test_dinic_complex(self, complex_network):
        """Test Dinic's on complex network."""
        solver = MaxFlowSolver(complex_network)
        max_flow, flow_dict = solver.dinic(0, 5)
        assert max_flow == 23
        assert isinstance(flow_dict, dict)

    def test_invalid_source(self, simple_network):
        """Test with invalid source vertex."""
        solver = MaxFlowSolver(simple_network)
        with pytest.raises(ValueError):
            solver.ford_fulkerson(-1, 3)
        with pytest.raises(ValueError):
            solver.edmonds_karp(10, 3)
        with pytest.raises(ValueError):
            solver.dinic(-1, 3)

    def test_invalid_sink(self, simple_network):
        """Test with invalid sink vertex."""
        solver = MaxFlowSolver(simple_network)
        with pytest.raises(ValueError):
            solver.ford_fulkerson(0, -1)
        with pytest.raises(ValueError):
            solver.edmonds_karp(0, 10)
        with pytest.raises(ValueError):
            solver.dinic(0, -1)

    def test_source_equals_sink(self, simple_network):
        """Test with source equal to sink."""
        solver = MaxFlowSolver(simple_network)
        with pytest.raises(ValueError):
            solver.ford_fulkerson(0, 0)
        with pytest.raises(ValueError):
            solver.edmonds_karp(0, 0)
        with pytest.raises(ValueError):
            solver.dinic(0, 0)

    def test_no_path(self):
        """Test network with no path from source to sink."""
        network = FlowNetwork(4)
        network.add_edge(0, 1, 10)
        network.add_edge(2, 3, 10)

        solver = MaxFlowSolver(network)
        max_flow, _ = solver.ford_fulkerson(0, 3)
        assert max_flow == 0

        max_flow, _ = solver.edmonds_karp(0, 3)
        assert max_flow == 0

        max_flow, _ = solver.dinic(0, 3)
        assert max_flow == 0

    def test_single_edge(self):
        """Test network with single edge."""
        network = FlowNetwork(2)
        network.add_edge(0, 1, 10)

        solver = MaxFlowSolver(network)
        max_flow, _ = solver.ford_fulkerson(0, 1)
        assert max_flow == 10

        max_flow, _ = solver.edmonds_karp(0, 1)
        assert max_flow == 10

        max_flow, _ = solver.dinic(0, 1)
        assert max_flow == 10

    def test_flow_dict_structure(self, simple_network):
        """Test flow dictionary structure."""
        solver = MaxFlowSolver(simple_network)
        _, flow_dict = solver.ford_fulkerson(0, 3)
        assert isinstance(flow_dict, dict)
        for (u, v), flow in flow_dict.items():
            assert isinstance(u, int)
            assert isinstance(v, int)
            assert isinstance(flow, int)
            assert flow > 0

    def test_min_cut(self, complex_network):
        """Test minimum cut computation."""
        solver = MaxFlowSolver(complex_network)
        source_side, sink_side = solver.get_min_cut(0, 5)
        assert len(source_side) > 0
        assert len(sink_side) > 0
        assert 0 in source_side
        assert 5 in sink_side
        assert len(source_side) + len(sink_side) == 6

    def test_min_cut_different_algorithms(self, complex_network):
        """Test min cut with different algorithms."""
        solver = MaxFlowSolver(complex_network)
        source_side_ff, sink_side_ff = solver.get_min_cut(
            0, 5, algorithm="ford_fulkerson"
        )
        source_side_ek, sink_side_ek = solver.get_min_cut(
            0, 5, algorithm="edmonds_karp"
        )
        source_side_dinic, sink_side_dinic = solver.get_min_cut(
            0, 5, algorithm="dinic"
        )

        assert len(source_side_ff) == len(source_side_ek))
        assert len(source_side_ek) == len(source_side_dinic))

    def test_min_cut_invalid_algorithm(self, simple_network):
        """Test min cut with invalid algorithm."""
        solver = MaxFlowSolver(simple_network)
        with pytest.raises(ValueError):
            solver.get_min_cut(0, 3, algorithm="invalid")

    def test_parallel_edges(self):
        """Test network with parallel edges."""
        network = FlowNetwork(3)
        network.add_edge(0, 1, 10)
        network.add_edge(0, 1, 5)
        network.add_edge(1, 2, 15)

        solver = MaxFlowSolver(network)
        max_flow, _ = solver.ford_fulkerson(0, 2)
        assert max_flow == 15

    def test_reverse_edges(self):
        """Test network with reverse edges."""
        network = FlowNetwork(3)
        network.add_edge(0, 1, 10)
        network.add_edge(1, 0, 5)
        network.add_edge(1, 2, 10)

        solver = MaxFlowSolver(network)
        max_flow, _ = solver.ford_fulkerson(0, 2)
        assert max_flow >= 0

    def test_large_network(self):
        """Test with larger network."""
        network = FlowNetwork(10)
        for i in range(9):
            network.add_edge(i, i + 1, 10)
        for i in range(0, 8, 2):
            network.add_edge(i, i + 2, 5)

        solver = MaxFlowSolver(network)
        max_flow, _ = solver.ford_fulkerson(0, 9)
        assert max_flow > 0

        max_flow, _ = solver.edmonds_karp(0, 9)
        assert max_flow > 0

        max_flow, _ = solver.dinic(0, 9)
        assert max_flow > 0
