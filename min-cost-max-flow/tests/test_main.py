"""Unit tests for min-cost max-flow module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import Edge, FlowNetwork, MinCostMaxFlow


class TestEdge:
    """Test cases for Edge class."""

    def test_edge_creation(self):
        """Test Edge creation."""
        edge = Edge(to=1, capacity=10.0, cost=2.0)
        assert edge.to == 1
        assert edge.capacity == 10.0
        assert edge.cost == 2.0
        assert edge.flow == 0.0

    def test_edge_repr(self):
        """Test Edge string representation."""
        edge = Edge(to=1, capacity=10.0, cost=2.0)
        assert "Edge" in repr(edge)


class TestFlowNetwork:
    """Test cases for FlowNetwork class."""

    def test_network_creation(self):
        """Test FlowNetwork creation."""
        network = FlowNetwork(5)
        assert network.num_vertices == 5
        assert len(network.graph) == 5

    def test_add_edge(self):
        """Test adding edge to network."""
        network = FlowNetwork(3)
        network.add_edge(0, 1, 10.0, 2.0)

        assert len(network.graph[0]) > 0
        assert len(network.graph[1]) > 0

    def test_get_residual_capacity(self):
        """Test getting residual capacity."""
        network = FlowNetwork(3)
        network.add_edge(0, 1, 10.0, 2.0)

        edge = network.graph[0][0]
        capacity = network.get_residual_capacity(edge)
        assert capacity == 10.0

        edge.flow = 3.0
        capacity = network.get_residual_capacity(edge)
        assert capacity == 7.0

    def test_is_residual(self):
        """Test checking if edge is residual."""
        network = FlowNetwork(3)
        network.add_edge(0, 1, 10.0, 2.0)

        edge = network.graph[0][0]
        assert network.is_residual(edge) is True

        edge.flow = 10.0
        assert network.is_residual(edge) is False


class TestMinCostMaxFlow:
    """Test cases for MinCostMaxFlow class."""

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
        network.add_edge(0, 1, 10.0, 1.0)
        network.add_edge(0, 2, 5.0, 2.0)
        network.add_edge(1, 2, 15.0, 1.0)
        network.add_edge(1, 3, 10.0, 3.0)
        network.add_edge(2, 3, 10.0, 1.0)
        return network

    def test_successive_shortest_paths(self, simple_network, config_file):
        """Test successive shortest paths algorithm."""
        solver = MinCostMaxFlow(simple_network, config_path=config_file)
        flow, cost = solver.successive_shortest_paths(0, 3)

        assert flow >= 0.0
        assert cost >= 0.0

    def test_cycle_canceling(self, simple_network, config_file):
        """Test cycle canceling algorithm."""
        solver = MinCostMaxFlow(simple_network, config_path=config_file)
        flow, cost = solver.cycle_canceling(0, 3)

        assert flow >= 0.0
        assert cost >= 0.0

    def test_get_flow(self, simple_network, config_file):
        """Test getting flow on edges."""
        solver = MinCostMaxFlow(simple_network, config_path=config_file)
        solver.successive_shortest_paths(0, 3)

        flow_dict = solver.get_flow()
        assert isinstance(flow_dict, dict)

    def test_simple_network(self, config_file):
        """Test on simple network."""
        network = FlowNetwork(3)
        network.add_edge(0, 1, 10.0, 1.0)
        network.add_edge(1, 2, 10.0, 1.0)

        solver = MinCostMaxFlow(network, config_path=config_file)
        flow, cost = solver.successive_shortest_paths(0, 2)

        assert flow == 10.0
        assert cost == 20.0

    def test_cycle_canceling_simple(self, config_file):
        """Test cycle canceling on simple network."""
        network = FlowNetwork(3)
        network.add_edge(0, 1, 10.0, 1.0)
        network.add_edge(1, 2, 10.0, 1.0)

        solver = MinCostMaxFlow(network, config_path=config_file)
        flow, cost = solver.cycle_canceling(0, 2)

        assert flow == 10.0
        assert cost == 20.0

    def test_network_with_multiple_paths(self, config_file):
        """Test network with multiple paths."""
        network = FlowNetwork(4)
        network.add_edge(0, 1, 5.0, 1.0)
        network.add_edge(0, 2, 5.0, 2.0)
        network.add_edge(1, 3, 5.0, 1.0)
        network.add_edge(2, 3, 5.0, 1.0)

        solver = MinCostMaxFlow(network, config_path=config_file)
        flow, cost = solver.successive_shortest_paths(0, 3)

        assert flow == 10.0
        assert cost == 15.0

    def test_network_with_negative_cost(self, config_file):
        """Test network with negative cost edges."""
        network = FlowNetwork(4)
        network.add_edge(0, 1, 10.0, -1.0)
        network.add_edge(1, 2, 10.0, 2.0)
        network.add_edge(2, 3, 10.0, 1.0)

        solver = MinCostMaxFlow(network, config_path=config_file)
        flow, cost = solver.cycle_canceling(0, 3)

        assert flow >= 0.0

    def test_empty_network(self, config_file):
        """Test on empty network."""
        network = FlowNetwork(2)

        solver = MinCostMaxFlow(network, config_path=config_file)
        flow, cost = solver.successive_shortest_paths(0, 1)

        assert flow == 0.0
        assert cost == 0.0

    def test_single_edge_network(self, config_file):
        """Test on single edge network."""
        network = FlowNetwork(2)
        network.add_edge(0, 1, 5.0, 3.0)

        solver = MinCostMaxFlow(network, config_path=config_file)
        flow, cost = solver.successive_shortest_paths(0, 1)

        assert flow == 5.0
        assert cost == 15.0

    def test_algorithm_consistency(self, simple_network, config_file):
        """Test consistency between algorithms."""
        network1 = FlowNetwork(4)
        network1.add_edge(0, 1, 10.0, 1.0)
        network1.add_edge(0, 2, 5.0, 2.0)
        network1.add_edge(1, 2, 15.0, 1.0)
        network1.add_edge(1, 3, 10.0, 3.0)
        network1.add_edge(2, 3, 10.0, 1.0)

        network2 = FlowNetwork(4)
        network2.add_edge(0, 1, 10.0, 1.0)
        network2.add_edge(0, 2, 5.0, 2.0)
        network2.add_edge(1, 2, 15.0, 1.0)
        network2.add_edge(1, 3, 10.0, 3.0)
        network2.add_edge(2, 3, 10.0, 1.0)

        solver1 = MinCostMaxFlow(network1, config_path=config_file)
        flow1, cost1 = solver1.successive_shortest_paths(0, 3)

        solver2 = MinCostMaxFlow(network2, config_path=config_file)
        flow2, cost2 = solver2.cycle_canceling(0, 3)

        assert flow1 == flow2
