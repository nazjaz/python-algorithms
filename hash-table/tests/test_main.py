"""Unit tests for hash table module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import (
    HashTableChaining,
    HashTableOpenAddressing,
    HashTableVisualizer,
)


class TestHashTableChaining:
    """Test cases for HashTableChaining class."""

    def test_initialization(self):
        """Test hash table initialization."""
        table = HashTableChaining()
        assert table.capacity == 11
        assert table.size == 0
        assert len(table.buckets) == 11

    def test_initialization_custom_capacity(self):
        """Test initialization with custom capacity."""
        table = HashTableChaining(initial_capacity=20)
        assert table.capacity == 20
        assert len(table.buckets) == 20

    def test_insert(self):
        """Test inserting key-value pairs."""
        table = HashTableChaining()
        table.insert("key1", "value1")
        assert table.size == 1
        assert table.get("key1") == "value1"

    def test_insert_multiple(self):
        """Test inserting multiple key-value pairs."""
        table = HashTableChaining()
        table.insert("key1", "value1")
        table.insert("key2", "value2")
        table.insert("key3", "value3")
        assert table.size == 3

    def test_insert_update(self):
        """Test updating existing key."""
        table = HashTableChaining()
        table.insert("key1", "value1")
        table.insert("key1", "value2")
        assert table.size == 1
        assert table.get("key1") == "value2"

    def test_get_existing(self):
        """Test getting existing key."""
        table = HashTableChaining()
        table.insert("key1", "value1")
        assert table.get("key1") == "value1"

    def test_get_nonexistent(self):
        """Test getting non-existent key."""
        table = HashTableChaining()
        assert table.get("nonexistent") is None

    def test_delete_existing(self):
        """Test deleting existing key."""
        table = HashTableChaining()
        table.insert("key1", "value1")
        result = table.delete("key1")
        assert result is True
        assert table.size == 0
        assert table.get("key1") is None

    def test_delete_nonexistent(self):
        """Test deleting non-existent key."""
        table = HashTableChaining()
        result = table.delete("nonexistent")
        assert result is False

    def test_contains(self):
        """Test contains method."""
        table = HashTableChaining()
        table.insert("key1", "value1")
        assert table.contains("key1") is True
        assert table.contains("nonexistent") is False

    def test_load_factor(self):
        """Test load factor calculation."""
        table = HashTableChaining(initial_capacity=10)
        table.insert("key1", "value1")
        assert table.get_load_factor() == 0.1

    def test_resize(self):
        """Test automatic resizing."""
        table = HashTableChaining(initial_capacity=4)
        # Insert enough elements to trigger resize
        for i in range(4):
            table.insert(f"key{i}", f"value{i}")

        # Should have resized
        assert table.capacity > 4
        # All elements should still be accessible
        for i in range(4):
            assert table.get(f"key{i}") == f"value{i}"

    def test_collision_handling(self):
        """Test collision handling with chaining."""
        table = HashTableChaining(initial_capacity=2)
        # Force collisions by using small capacity
        table.insert("key1", "value1")
        table.insert("key2", "value2")
        table.insert("key3", "value3")

        # All should be accessible
        assert table.get("key1") == "value1"
        assert table.get("key2") == "value2"
        assert table.get("key3") == "value3"

    def test_visualize(self):
        """Test visualization."""
        table = HashTableChaining()
        table.insert("key1", "value1")
        visualization = table.visualize()
        assert "Hash Table" in visualization
        assert "key1" in visualization


class TestHashTableOpenAddressing:
    """Test cases for HashTableOpenAddressing class."""

    def test_initialization(self):
        """Test hash table initialization."""
        table = HashTableOpenAddressing()
        assert table.capacity == 11
        assert table.size == 0
        assert len(table.buckets) == 11

    def test_initialization_custom_capacity(self):
        """Test initialization with custom capacity."""
        table = HashTableOpenAddressing(initial_capacity=20)
        assert table.capacity == 20
        assert len(table.buckets) == 20

    def test_insert(self):
        """Test inserting key-value pairs."""
        table = HashTableOpenAddressing()
        table.insert("key1", "value1")
        assert table.size == 1
        assert table.get("key1") == "value1"

    def test_insert_multiple(self):
        """Test inserting multiple key-value pairs."""
        table = HashTableOpenAddressing()
        table.insert("key1", "value1")
        table.insert("key2", "value2")
        table.insert("key3", "value3")
        assert table.size == 3

    def test_insert_update(self):
        """Test updating existing key."""
        table = HashTableOpenAddressing()
        table.insert("key1", "value1")
        table.insert("key1", "value2")
        assert table.size == 1
        assert table.get("key1") == "value2"

    def test_get_existing(self):
        """Test getting existing key."""
        table = HashTableOpenAddressing()
        table.insert("key1", "value1")
        assert table.get("key1") == "value1"

    def test_get_nonexistent(self):
        """Test getting non-existent key."""
        table = HashTableOpenAddressing()
        assert table.get("nonexistent") is None

    def test_delete_existing(self):
        """Test deleting existing key."""
        table = HashTableOpenAddressing()
        table.insert("key1", "value1")
        result = table.delete("key1")
        assert result is True
        assert table.size == 0
        assert table.get("key1") is None

    def test_delete_nonexistent(self):
        """Test deleting non-existent key."""
        table = HashTableOpenAddressing()
        result = table.delete("nonexistent")
        assert result is False

    def test_contains(self):
        """Test contains method."""
        table = HashTableOpenAddressing()
        table.insert("key1", "value1")
        assert table.contains("key1") is True
        assert table.contains("nonexistent") is False

    def test_load_factor(self):
        """Test load factor calculation."""
        table = HashTableOpenAddressing(initial_capacity=10)
        table.insert("key1", "value1")
        assert table.get_load_factor() == 0.1

    def test_resize(self):
        """Test automatic resizing."""
        table = HashTableOpenAddressing(initial_capacity=4)
        # Insert enough elements to trigger resize
        for i in range(4):
            table.insert(f"key{i}", f"value{i}")

        # Should have resized
        assert table.capacity > 4
        # All elements should still be accessible
        for i in range(4):
            assert table.get(f"key{i}") == f"value{i}"

    def test_collision_handling_linear_probing(self):
        """Test collision handling with linear probing."""
        table = HashTableOpenAddressing(initial_capacity=5)
        # Force collisions
        table.insert("key1", "value1")
        table.insert("key2", "value2")
        table.insert("key3", "value3")

        # All should be accessible
        assert table.get("key1") == "value1"
        assert table.get("key2") == "value2"
        assert table.get("key3") == "value3"

    def test_deleted_marker(self):
        """Test that deleted entries are marked correctly."""
        table = HashTableOpenAddressing()
        table.insert("key1", "value1")
        table.delete("key1")
        # Should be able to insert at same position
        table.insert("key2", "value2")
        assert table.get("key2") == "value2"

    def test_visualize(self):
        """Test visualization."""
        table = HashTableOpenAddressing()
        table.insert("key1", "value1")
        visualization = table.visualize()
        assert "Hash Table" in visualization
        assert "key1" in visualization


class TestHashTableVisualizer:
    """Test cases for HashTableVisualizer class."""

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
        """Create HashTableVisualizer instance."""
        return HashTableVisualizer(config_path=config_file)

    def test_load_config_success(self, temp_dir):
        """Test successful configuration loading."""
        config = {
            "logging": {"level": "DEBUG"},
        }
        config_path = temp_dir / "config.yaml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)

        visualizer = HashTableVisualizer(config_path=str(config_path))
        assert visualizer.config["logging"]["level"] == "DEBUG"

    def test_load_config_file_not_found(self):
        """Test FileNotFoundError when config file doesn't exist."""
        with pytest.raises(FileNotFoundError):
            HashTableVisualizer(config_path="nonexistent.yaml")

    def test_compare_methods(self, visualizer):
        """Test method comparison."""
        operations = [
            ("insert", "key1", "value1"),
            ("insert", "key2", "value2"),
            ("insert", "key3", "value3"),
        ]
        results = visualizer.compare_methods(operations)

        assert "chaining" in results
        assert "open_addressing" in results
        assert results["chaining"]["size"] == 3
        assert results["open_addressing"]["size"] == 3

    def test_generate_report(self, visualizer, temp_dir):
        """Test report generation."""
        operations = [
            ("insert", "key1", "value1"),
            ("insert", "key2", "value2"),
        ]
        results = visualizer.compare_methods(operations)
        report_path = temp_dir / "report.txt"
        report = visualizer.generate_report(
            results, output_path=str(report_path)
        )

        assert report_path.exists()
        assert "HASH TABLE COLLISION HANDLING" in report
        assert "CHAINING" in report
        assert "OPEN ADDRESSING" in report

    def test_both_methods_same_results(self, visualizer):
        """Test that both methods produce same results."""
        operations = [
            ("insert", "key1", "value1"),
            ("insert", "key2", "value2"),
            ("insert", "key3", "value3"),
        ]
        results = visualizer.compare_methods(operations)

        chaining_table = results["chaining"]["table"]
        open_table = results["open_addressing"]["table"]

        # Both should have same keys
        assert chaining_table.get("key1") == open_table.get("key1")
        assert chaining_table.get("key2") == open_table.get("key2")
        assert chaining_table.get("key3") == open_table.get("key3")


class TestHashTableIntegration:
    """Integration tests for hash table operations."""

    def test_chaining_complex_operations(self):
        """Test complex operations with chaining."""
        table = HashTableChaining()
        table.insert("a", 1)
        table.insert("b", 2)
        table.insert("c", 3)
        table.delete("b")
        table.insert("d", 4)

        assert table.get("a") == 1
        assert table.get("b") is None
        assert table.get("c") == 3
        assert table.get("d") == 4
        assert table.size == 3

    def test_open_addressing_complex_operations(self):
        """Test complex operations with open addressing."""
        table = HashTableOpenAddressing()
        table.insert("a", 1)
        table.insert("b", 2)
        table.insert("c", 3)
        table.delete("b")
        table.insert("d", 4)

        assert table.get("a") == 1
        assert table.get("b") is None
        assert table.get("c") == 3
        assert table.get("d") == 4
        assert table.size == 3

    def test_large_dataset_chaining(self):
        """Test chaining with large dataset."""
        table = HashTableChaining()
        for i in range(100):
            table.insert(f"key{i}", f"value{i}")

        assert table.size == 100
        for i in range(100):
            assert table.get(f"key{i}") == f"value{i}"

    def test_large_dataset_open_addressing(self):
        """Test open addressing with large dataset."""
        table = HashTableOpenAddressing()
        for i in range(100):
            table.insert(f"key{i}", f"value{i}")

        assert table.size == 100
        for i in range(100):
            assert table.get(f"key{i}") == f"value{i}"
