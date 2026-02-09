"""Unit tests for character frequency analyzer module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import CharacterFrequencyAnalyzer


class TestCharacterFrequencyAnalyzer:
    """Test cases for CharacterFrequencyAnalyzer class."""

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
        """Create CharacterFrequencyAnalyzer instance."""
        return CharacterFrequencyAnalyzer(config_path=config_file)

    def test_load_config_success(self, temp_dir):
        """Test successful configuration loading."""
        config = {"logging": {"level": "INFO"}}
        config_path = temp_dir / "config.yaml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)

        analyzer = CharacterFrequencyAnalyzer(config_path=str(config_path))
        assert analyzer.config["logging"]["level"] == "INFO"

    def test_load_config_file_not_found(self):
        """Test FileNotFoundError when config file doesn't exist."""
        with pytest.raises(FileNotFoundError):
            CharacterFrequencyAnalyzer(config_path="nonexistent.yaml")

    def test_count_characters_dict(self, analyzer):
        """Test character counting using dictionary method."""
        frequency = analyzer.count_characters_dict("hello")
        assert frequency["h"] == 1
        assert frequency["e"] == 1
        assert frequency["l"] == 2
        assert frequency["o"] == 1

    def test_count_characters_dict_empty(self, analyzer):
        """Test counting with empty string."""
        frequency = analyzer.count_characters_dict("")
        assert frequency == {}

    def test_count_characters_dict_single_char(self, analyzer):
        """Test counting with single character."""
        frequency = analyzer.count_characters_dict("a")
        assert frequency["a"] == 1

    def test_count_characters_defaultdict(self, analyzer):
        """Test character counting using defaultdict method."""
        frequency = analyzer.count_characters_defaultdict("hello")
        assert frequency["l"] == 2
        assert frequency["h"] == 1

    def test_count_characters_counter(self, analyzer):
        """Test character counting using Counter method."""
        frequency = analyzer.count_characters_counter("hello")
        assert frequency["l"] == 2
        assert frequency["h"] == 1

    def test_all_methods_same_result(self, analyzer):
        """Test that all methods produce same result."""
        text = "hello"
        dict_result = analyzer.count_characters_dict(text)
        defaultdict_result = analyzer.count_characters_defaultdict(text)
        counter_result = analyzer.count_characters_counter(text)

        assert dict_result == defaultdict_result == counter_result

    def test_get_frequency_analysis(self, analyzer):
        """Test getting frequency analysis."""
        analyzer.count_characters_dict("hello")
        analysis = analyzer.get_frequency_analysis()

        assert "total_characters" in analysis
        assert "unique_characters" in analysis
        assert "most_common" in analysis
        assert "frequency_distribution" in analysis

    def test_get_top_characters(self, analyzer):
        """Test getting top N characters."""
        analyzer.count_characters_dict("hello world")
        top_chars = analyzer.get_top_characters(3)

        assert len(top_chars) == 3
        assert top_chars[0][1] >= top_chars[1][1]

    def test_get_character_info(self, analyzer):
        """Test getting character information."""
        analyzer.count_characters_dict("hello")
        info = analyzer.get_character_info("l")

        assert info is not None
        assert info["count"] == 2
        assert "percentage" in info
        assert "unicode_code" in info

    def test_get_character_info_not_found(self, analyzer):
        """Test getting info for non-existent character."""
        analyzer.count_characters_dict("hello")
        info = analyzer.get_character_info("z")

        assert info is None

    def test_generate_report(self, analyzer, temp_dir):
        """Test report generation."""
        analyzer.count_characters_dict("hello")
        report_path = temp_dir / "report.txt"
        report = analyzer.generate_report(output_path=str(report_path))

        assert report_path.exists()
        assert "CHARACTER FREQUENCY ANALYSIS REPORT" in report
        assert "Total characters" in report
        assert "Most common" in report

    def test_generate_report_no_data(self, analyzer):
        """Test report generation without frequency data."""
        report = analyzer.generate_report()
        assert "No frequency data available" in report

    def test_count_with_special_characters(self, analyzer):
        """Test counting with special characters."""
        frequency = analyzer.count_characters_dict("hello\nworld\t!")
        assert "\n" in frequency
        assert "\t" in frequency
        assert "!" in frequency

    def test_count_with_unicode(self, analyzer):
        """Test counting with Unicode characters."""
        frequency = analyzer.count_characters_dict("hello 世界")
        assert "世" in frequency
        assert "界" in frequency
