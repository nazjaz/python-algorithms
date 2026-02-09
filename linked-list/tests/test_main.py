"""Unit tests for linked list module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import Node, LinkedList, LinkedListVisualizer


class TestNode:
    """Test cases for Node class."""

    def test_node_initialization(self):
        """Test node initialization."""
        node = Node(10)
        assert node.data == 10
        assert node.next is None

    def test_node_repr(self):
        """Test node string representation."""
        node = Node(10)
        assert "Node(10)" in repr(node)


class TestLinkedList:
    """Test cases for LinkedList class."""

    def test_linked_list_initialization(self):
        """Test linked list initialization."""
        ll = LinkedList()
        assert ll.is_empty() is True
        assert ll.size() == 0
        assert ll.head is None

    def test_insert_at_beginning(self):
        """Test insertion at beginning."""
        ll = LinkedList()
        ll.insert_at_beginning(10)
        assert ll.size() == 1
        assert ll.head.data == 10

        ll.insert_at_beginning(20)
        assert ll.size() == 2
        assert ll.head.data == 20
        assert ll.head.next.data == 10

    def test_insert_at_end(self):
        """Test insertion at end."""
        ll = LinkedList()
        ll.insert_at_end(10)
        assert ll.size() == 1
        assert ll.head.data == 10

        ll.insert_at_end(20)
        assert ll.size() == 2
        assert ll.head.data == 10
        assert ll.head.next.data == 20

    def test_insert_at_end_empty_list(self):
        """Test insertion at end of empty list."""
        ll = LinkedList()
        ll.insert_at_end(10)
        assert ll.head.data == 10
        assert ll.head.next is None

    def test_insert_at_position_beginning(self):
        """Test insertion at position 0."""
        ll = LinkedList()
        result = ll.insert_at_position(10, 0)
        assert result is True
        assert ll.head.data == 10

    def test_insert_at_position_middle(self):
        """Test insertion at middle position."""
        ll = LinkedList()
        ll.insert_at_end(10)
        ll.insert_at_end(30)
        result = ll.insert_at_position(20, 1)
        assert result is True
        assert ll.head.next.data == 20

    def test_insert_at_position_end(self):
        """Test insertion at end position."""
        ll = LinkedList()
        ll.insert_at_end(10)
        ll.insert_at_end(20)
        result = ll.insert_at_position(30, 2)
        assert result is True
        assert ll.head.next.next.data == 30

    def test_insert_at_position_invalid_negative(self):
        """Test insertion at invalid negative position."""
        ll = LinkedList()
        result = ll.insert_at_position(10, -1)
        assert result is False

    def test_insert_at_position_invalid_too_large(self):
        """Test insertion at position beyond size."""
        ll = LinkedList()
        ll.insert_at_end(10)
        result = ll.insert_at_position(20, 5)
        assert result is False

    def test_delete_at_beginning(self):
        """Test deletion at beginning."""
        ll = LinkedList()
        ll.insert_at_end(10)
        ll.insert_at_end(20)
        data = ll.delete_at_beginning()
        assert data == 10
        assert ll.size() == 1
        assert ll.head.data == 20

    def test_delete_at_beginning_empty(self):
        """Test deletion at beginning of empty list."""
        ll = LinkedList()
        data = ll.delete_at_beginning()
        assert data is None

    def test_delete_at_beginning_single_node(self):
        """Test deletion at beginning with single node."""
        ll = LinkedList()
        ll.insert_at_end(10)
        data = ll.delete_at_beginning()
        assert data == 10
        assert ll.is_empty()

    def test_delete_at_end(self):
        """Test deletion at end."""
        ll = LinkedList()
        ll.insert_at_end(10)
        ll.insert_at_end(20)
        data = ll.delete_at_end()
        assert data == 20
        assert ll.size() == 1
        assert ll.head.data == 10

    def test_delete_at_end_empty(self):
        """Test deletion at end of empty list."""
        ll = LinkedList()
        data = ll.delete_at_end()
        assert data is None

    def test_delete_at_end_single_node(self):
        """Test deletion at end with single node."""
        ll = LinkedList()
        ll.insert_at_end(10)
        data = ll.delete_at_end()
        assert data == 10
        assert ll.is_empty()

    def test_delete_at_position(self):
        """Test deletion at specific position."""
        ll = LinkedList()
        ll.insert_at_end(10)
        ll.insert_at_end(20)
        ll.insert_at_end(30)
        data = ll.delete_at_position(1)
        assert data == 20
        assert ll.size() == 2
        assert ll.head.next.data == 30

    def test_delete_at_position_beginning(self):
        """Test deletion at position 0."""
        ll = LinkedList()
        ll.insert_at_end(10)
        ll.insert_at_end(20)
        data = ll.delete_at_position(0)
        assert data == 10
        assert ll.head.data == 20

    def test_delete_at_position_invalid(self):
        """Test deletion at invalid position."""
        ll = LinkedList()
        ll.insert_at_end(10)
        data = ll.delete_at_position(5)
        assert data is None

    def test_delete_by_value(self):
        """Test deletion by value."""
        ll = LinkedList()
        ll.insert_at_end(10)
        ll.insert_at_end(20)
        ll.insert_at_end(30)
        result = ll.delete_by_value(20)
        assert result is True
        assert ll.size() == 2
        assert ll.head.next.data == 30

    def test_delete_by_value_first(self):
        """Test deletion of first value."""
        ll = LinkedList()
        ll.insert_at_end(10)
        ll.insert_at_end(20)
        result = ll.delete_by_value(10)
        assert result is True
        assert ll.head.data == 20

    def test_delete_by_value_not_found(self):
        """Test deletion of non-existent value."""
        ll = LinkedList()
        ll.insert_at_end(10)
        result = ll.delete_by_value(99)
        assert result is False

    def test_delete_by_value_empty(self):
        """Test deletion by value in empty list."""
        ll = LinkedList()
        result = ll.delete_by_value(10)
        assert result is False

    def test_search(self):
        """Test search operation."""
        ll = LinkedList()
        ll.insert_at_end(10)
        ll.insert_at_end(20)
        ll.insert_at_end(30)
        position = ll.search(20)
        assert position == 1

    def test_search_not_found(self):
        """Test search for non-existent value."""
        ll = LinkedList()
        ll.insert_at_end(10)
        position = ll.search(99)
        assert position is None

    def test_search_empty(self):
        """Test search in empty list."""
        ll = LinkedList()
        position = ll.search(10)
        assert position is None

    def test_get(self):
        """Test get operation."""
        ll = LinkedList()
        ll.insert_at_end(10)
        ll.insert_at_end(20)
        value = ll.get(1)
        assert value == 20

    def test_get_invalid(self):
        """Test get with invalid position."""
        ll = LinkedList()
        ll.insert_at_end(10)
        value = ll.get(5)
        assert value is None

    def test_traverse(self):
        """Test traversal operation."""
        ll = LinkedList()
        ll.insert_at_end(10)
        ll.insert_at_end(20)
        ll.insert_at_end(30)
        values = ll.traverse()
        assert values == [10, 20, 30]

    def test_traverse_empty(self):
        """Test traversal of empty list."""
        ll = LinkedList()
        values = ll.traverse()
        assert values == []

    def test_visualize(self):
        """Test visualization."""
        ll = LinkedList()
        ll.insert_at_end(10)
        ll.insert_at_end(20)
        visualization = ll.visualize()
        assert "10" in visualization
        assert "20" in visualization
        assert "NULL" in visualization

    def test_visualize_empty(self):
        """Test visualization of empty list."""
        ll = LinkedList()
        visualization = ll.visualize()
        assert "Empty" in visualization or "NULL" in visualization

    def test_visualize_detailed(self):
        """Test detailed visualization."""
        ll = LinkedList()
        ll.insert_at_end(10)
        visualization = ll.visualize_detailed()
        assert "10" in visualization
        assert "Size" in visualization

    def test_to_list(self):
        """Test conversion to list."""
        ll = LinkedList()
        ll.insert_at_end(10)
        ll.insert_at_end(20)
        result = ll.to_list()
        assert result == [10, 20]

    def test_from_list(self):
        """Test creation from list."""
        ll = LinkedList()
        ll.from_list([10, 20, 30])
        assert ll.size() == 3
        assert ll.traverse() == [10, 20, 30]

    def test_reverse(self):
        """Test reverse operation."""
        ll = LinkedList()
        ll.insert_at_end(10)
        ll.insert_at_end(20)
        ll.insert_at_end(30)
        ll.reverse()
        assert ll.traverse() == [30, 20, 10]

    def test_reverse_empty(self):
        """Test reverse of empty list."""
        ll = LinkedList()
        ll.reverse()
        assert ll.is_empty()

    def test_reverse_single(self):
        """Test reverse of single node list."""
        ll = LinkedList()
        ll.insert_at_end(10)
        ll.reverse()
        assert ll.head.data == 10

    def test_repr(self):
        """Test string representation."""
        ll = LinkedList()
        ll.insert_at_end(10)
        ll.insert_at_end(20)
        repr_str = repr(ll)
        assert "10" in repr_str
        assert "20" in repr_str

    def test_len(self):
        """Test length operation."""
        ll = LinkedList()
        assert len(ll) == 0
        ll.insert_at_end(10)
        assert len(ll) == 1

    def test_multiple_operations(self):
        """Test multiple operations in sequence."""
        ll = LinkedList()
        ll.insert_at_beginning(10)
        ll.insert_at_end(20)
        ll.insert_at_position(15, 1)
        assert ll.traverse() == [10, 15, 20]
        ll.delete_at_position(1)
        assert ll.traverse() == [10, 20]
        ll.delete_by_value(10)
        assert ll.traverse() == [20]


class TestLinkedListVisualizer:
    """Test cases for LinkedListVisualizer class."""

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
    def visualizer(self, config_file):
        """Create LinkedListVisualizer instance."""
        return LinkedListVisualizer(config_path=config_file)

    def test_load_config_success(self, temp_dir):
        """Test successful configuration loading."""
        config = {
            "logging": {"level": "DEBUG"},
        }
        config_path = temp_dir / "config.yaml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)

        visualizer = LinkedListVisualizer(config_path=str(config_path))
        assert visualizer.config["logging"]["level"] == "DEBUG"

    def test_load_config_file_not_found(self):
        """Test FileNotFoundError when config file doesn't exist."""
        with pytest.raises(FileNotFoundError):
            LinkedListVisualizer(config_path="nonexistent.yaml")

    def test_insert_at_beginning(self, visualizer):
        """Test insertion at beginning with visualizer."""
        visualizer.insert_at_beginning(10)
        assert visualizer.linked_list.size() == 1
        assert len(visualizer.operation_history) == 1

    def test_insert_at_end(self, visualizer):
        """Test insertion at end with visualizer."""
        visualizer.insert_at_end(10)
        assert visualizer.linked_list.size() == 1

    def test_delete_at_beginning(self, visualizer):
        """Test deletion at beginning with visualizer."""
        visualizer.insert_at_end(10)
        data = visualizer.delete_at_beginning()
        assert data == 10
        assert visualizer.linked_list.is_empty()

    def test_operation_history(self, visualizer):
        """Test operation history recording."""
        visualizer.insert_at_beginning(10)
        visualizer.insert_at_end(20)
        assert len(visualizer.operation_history) == 2
        assert visualizer.operation_history[0]["operation"] == "insert_at_beginning"
        assert visualizer.operation_history[1]["operation"] == "insert_at_end"

    def test_print_visualization(self, visualizer, capsys):
        """Test printing visualization."""
        visualizer.insert_at_end(10)
        visualizer.print_visualization()
        captured = capsys.readouterr()
        assert "10" in captured.out

    def test_generate_report(self, visualizer, temp_dir):
        """Test report generation."""
        visualizer.insert_at_end(10)
        visualizer.insert_at_end(20)
        report_path = temp_dir / "report.txt"
        report = visualizer.generate_report(output_path=str(report_path))

        assert report_path.exists()
        assert "LINKED LIST OPERATIONS REPORT" in report
        assert "OPERATION HISTORY" in report
