"""Unit tests for queue data structure module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import ArrayQueue, LinkedListQueue, QueuePerformanceAnalyzer


class TestArrayQueue:
    """Test cases for ArrayQueue class."""

    def test_queue_initialization(self):
        """Test queue initialization."""
        queue = ArrayQueue()
        assert queue.is_empty() is True
        assert queue.size() == 0

    def test_enqueue(self):
        """Test enqueue operation."""
        queue = ArrayQueue()
        queue.enqueue(1)
        assert queue.is_empty() is False
        assert queue.size() == 1

    def test_dequeue(self):
        """Test dequeue operation."""
        queue = ArrayQueue()
        queue.enqueue(10)
        queue.enqueue(20)
        assert queue.dequeue() == 10
        assert queue.dequeue() == 20
        assert queue.is_empty() is True

    def test_dequeue_empty_queue(self):
        """Test dequeue from empty queue raises error."""
        queue = ArrayQueue()
        with pytest.raises(IndexError, match="Queue is empty"):
            queue.dequeue()

    def test_front(self):
        """Test front operation."""
        queue = ArrayQueue()
        queue.enqueue(10)
        queue.enqueue(20)
        assert queue.front() == 10
        assert queue.size() == 2  # Size unchanged

    def test_front_empty_queue(self):
        """Test front on empty queue raises error."""
        queue = ArrayQueue()
        with pytest.raises(IndexError, match="Queue is empty"):
            queue.front()

    def test_rear(self):
        """Test rear operation."""
        queue = ArrayQueue()
        queue.enqueue(10)
        queue.enqueue(20)
        assert queue.rear() == 20
        assert queue.size() == 2  # Size unchanged

    def test_rear_empty_queue(self):
        """Test rear on empty queue raises error."""
        queue = ArrayQueue()
        with pytest.raises(IndexError, match="Queue is empty"):
            queue.rear()

    def test_is_empty(self):
        """Test is_empty method."""
        queue = ArrayQueue()
        assert queue.is_empty() is True
        queue.enqueue(1)
        assert queue.is_empty() is False

    def test_size(self):
        """Test size method."""
        queue = ArrayQueue()
        assert queue.size() == 0
        queue.enqueue(1)
        assert queue.size() == 1
        queue.enqueue(2)
        assert queue.size() == 2
        queue.dequeue()
        assert queue.size() == 1

    def test_fifo_behavior(self):
        """Test First In First Out behavior."""
        queue = ArrayQueue()
        items = [1, 2, 3, 4, 5]
        for item in items:
            queue.enqueue(item)

        dequeued = []
        while not queue.is_empty():
            dequeued.append(queue.dequeue())

        assert dequeued == items


class TestLinkedListQueue:
    """Test cases for LinkedListQueue class."""

    def test_queue_initialization(self):
        """Test queue initialization."""
        queue = LinkedListQueue()
        assert queue.is_empty() is True
        assert queue.size() == 0

    def test_enqueue(self):
        """Test enqueue operation."""
        queue = LinkedListQueue()
        queue.enqueue(1)
        assert queue.is_empty() is False
        assert queue.size() == 1

    def test_dequeue(self):
        """Test dequeue operation."""
        queue = LinkedListQueue()
        queue.enqueue(10)
        queue.enqueue(20)
        assert queue.dequeue() == 10
        assert queue.dequeue() == 20
        assert queue.is_empty() is True

    def test_dequeue_empty_queue(self):
        """Test dequeue from empty queue raises error."""
        queue = LinkedListQueue()
        with pytest.raises(IndexError, match="Queue is empty"):
            queue.dequeue()

    def test_front(self):
        """Test front operation."""
        queue = LinkedListQueue()
        queue.enqueue(10)
        queue.enqueue(20)
        assert queue.front() == 10
        assert queue.size() == 2  # Size unchanged

    def test_front_empty_queue(self):
        """Test front on empty queue raises error."""
        queue = LinkedListQueue()
        with pytest.raises(IndexError, match="Queue is empty"):
            queue.front()

    def test_rear(self):
        """Test rear operation."""
        queue = LinkedListQueue()
        queue.enqueue(10)
        queue.enqueue(20)
        assert queue.rear() == 20
        assert queue.size() == 2  # Size unchanged

    def test_rear_empty_queue(self):
        """Test rear on empty queue raises error."""
        queue = LinkedListQueue()
        with pytest.raises(IndexError, match="Queue is empty"):
            queue.rear()

    def test_is_empty(self):
        """Test is_empty method."""
        queue = LinkedListQueue()
        assert queue.is_empty() is True
        queue.enqueue(1)
        assert queue.is_empty() is False

    def test_size(self):
        """Test size method."""
        queue = LinkedListQueue()
        assert queue.size() == 0
        queue.enqueue(1)
        assert queue.size() == 1
        queue.enqueue(2)
        assert queue.size() == 2
        queue.dequeue()
        assert queue.size() == 1

    def test_fifo_behavior(self):
        """Test First In First Out behavior."""
        queue = LinkedListQueue()
        items = [1, 2, 3, 4, 5]
        for item in items:
            queue.enqueue(item)

        dequeued = []
        while not queue.is_empty():
            dequeued.append(queue.dequeue())

        assert dequeued == items

    def test_single_element(self):
        """Test queue with single element."""
        queue = LinkedListQueue()
        queue.enqueue(42)
        assert queue.front() == 42
        assert queue.rear() == 42
        assert queue.size() == 1
        assert queue.dequeue() == 42
        assert queue.is_empty() is True


class TestQueuePerformanceAnalyzer:
    """Test cases for QueuePerformanceAnalyzer class."""

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
    def analyzer(self, config_file):
        """Create QueuePerformanceAnalyzer instance."""
        return QueuePerformanceAnalyzer(config_path=config_file)

    def test_load_config_success(self, temp_dir):
        """Test successful configuration loading."""
        config = {
            "logging": {"level": "DEBUG"},
        }
        config_path = temp_dir / "config.yaml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)

        analyzer = QueuePerformanceAnalyzer(config_path=str(config_path))
        assert analyzer.config["logging"]["level"] == "DEBUG"

    def test_load_config_file_not_found(self):
        """Test FileNotFoundError when config file doesn't exist."""
        with pytest.raises(FileNotFoundError):
            QueuePerformanceAnalyzer(config_path="nonexistent.yaml")

    def test_compare_implementations(self, analyzer):
        """Test performance comparison."""
        operations = ["enqueue 1", "enqueue 2", "dequeue", "enqueue 3"]
        comparison = analyzer.compare_implementations(operations)

        assert "operations_count" in comparison
        assert "array_queue" in comparison
        assert "linked_list_queue" in comparison

        assert comparison["array_queue"]["success"] is True
        assert comparison["linked_list_queue"]["success"] is True

    def test_compare_implementations_multiple_iterations(self, analyzer):
        """Test performance comparison with multiple iterations."""
        operations = ["enqueue 1", "enqueue 2", "dequeue"]
        comparison = analyzer.compare_implementations(operations, iterations=10)

        assert comparison["iterations"] == 10
        assert all(
            impl.get("success", False)
            for impl in [
                comparison["array_queue"],
                comparison["linked_list_queue"],
            ]
        )

    def test_generate_report(self, analyzer, temp_dir):
        """Test report generation."""
        operations = ["enqueue 1", "enqueue 2", "dequeue"]
        comparison = analyzer.compare_implementations(operations)
        report_path = temp_dir / "report.txt"
        report = analyzer.generate_report(comparison, output_path=str(report_path))

        assert report_path.exists()
        assert "QUEUE IMPLEMENTATION PERFORMANCE COMPARISON REPORT" in report
        assert "Array Queue" in report
        assert "Linked List Queue" in report

    def test_both_implementations_same_behavior(self):
        """Test that both implementations have same behavior."""
        array_queue = ArrayQueue()
        linked_queue = LinkedListQueue()

        items = [1, 2, 3, 4, 5]

        for item in items:
            array_queue.enqueue(item)
            linked_queue.enqueue(item)

        assert array_queue.size() == linked_queue.size()
        assert array_queue.front() == linked_queue.front()
        assert array_queue.rear() == linked_queue.rear()

        array_results = []
        linked_results = []

        while not array_queue.is_empty():
            array_results.append(array_queue.dequeue())

        while not linked_queue.is_empty():
            linked_results.append(linked_queue.dequeue())

        assert array_results == linked_results
