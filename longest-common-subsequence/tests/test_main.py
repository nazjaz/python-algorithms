"""Unit tests for LCS calculator module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import LCSCalculator


class TestLCSCalculator:
    """Test cases for LCSCalculator class."""

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
    def calculator(self, config_file):
        """Create LCSCalculator instance."""
        return LCSCalculator(config_path=config_file)

    def test_load_config_success(self, temp_dir):
        """Test successful configuration loading."""
        config = {
            "logging": {"level": "DEBUG"},
        }
        config_path = temp_dir / "config.yaml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)

        calculator = LCSCalculator(config_path=str(config_path))
        assert calculator.config["logging"]["level"] == "DEBUG"

    def test_load_config_file_not_found(self):
        """Test FileNotFoundError when config file doesn't exist."""
        with pytest.raises(FileNotFoundError):
            LCSCalculator(config_path="nonexistent.yaml")

    def test_lcs_length_simple(self, calculator):
        """Test LCS length calculation with simple strings."""
        assert calculator.lcs_length("ABC", "AC") == 2
        assert calculator.lcs_length("ABCDGH", "AEDFHR") == 3

    def test_lcs_length_identical(self, calculator):
        """Test LCS length with identical strings."""
        assert calculator.lcs_length("ABC", "ABC") == 3
        assert calculator.lcs_length("", "") == 0

    def test_lcs_length_no_common(self, calculator):
        """Test LCS length with no common characters."""
        assert calculator.lcs_length("ABC", "XYZ") == 0

    def test_lcs_length_empty_strings(self, calculator):
        """Test LCS length with empty strings."""
        assert calculator.lcs_length("", "ABC") == 0
        assert calculator.lcs_length("ABC", "") == 0
        assert calculator.lcs_length("", "") == 0

    def test_lcs_simple(self, calculator):
        """Test LCS finding with simple strings."""
        assert calculator.lcs("ABC", "AC") == "AC"
        assert calculator.lcs("ABCDGH", "AEDFHR") == "ADH"

    def test_lcs_identical(self, calculator):
        """Test LCS with identical strings."""
        assert calculator.lcs("ABC", "ABC") == "ABC"

    def test_lcs_no_common(self, calculator):
        """Test LCS with no common characters."""
        assert calculator.lcs("ABC", "XYZ") == ""

    def test_lcs_empty_strings(self, calculator):
        """Test LCS with empty strings."""
        assert calculator.lcs("", "ABC") == ""
        assert calculator.lcs("ABC", "") == ""
        assert calculator.lcs("", "") == ""

    def test_lcs_known_cases(self, calculator):
        """Test LCS with known test cases."""
        assert calculator.lcs("AGGTAB", "GXTXAYB") == "GTAB"
        assert calculator.lcs("ABCDEF", "ACDF") == "ACDF"

    def test_lcs_all_simple(self, calculator):
        """Test finding all LCS with simple strings."""
        all_lcs = calculator.lcs_all("ABC", "AC")
        assert "AC" in all_lcs

    def test_lcs_all_multiple(self, calculator):
        """Test finding all LCS when multiple exist."""
        all_lcs = calculator.lcs_all("ABCD", "ACBD")
        # Both "ABD" and "ACD" are valid LCS
        assert len(all_lcs) >= 1

    def test_lcs_all_empty(self, calculator):
        """Test finding all LCS with empty strings."""
        all_lcs = calculator.lcs_all("", "ABC")
        assert all_lcs == [""]

    def test_visualize_dp_table(self, calculator):
        """Test DP table visualization."""
        calculator.lcs_length("ABC", "AC")
        visualization = calculator.visualize_dp_table("ABC", "AC")
        assert "DP Table" in visualization
        assert "ABC" in visualization or "AC" in visualization

    def test_calculate_with_details(self, calculator):
        """Test detailed calculation."""
        result = calculator.calculate_with_details("ABC", "AC")
        assert "string1" in result
        assert "string2" in result
        assert "length" in result
        assert "lcs" in result
        assert "dp_table" in result
        assert result["length"] == 2
        assert result["lcs"] == "AC"

    def test_calculate_with_details_dp_table(self, calculator):
        """Test that DP table is populated in details."""
        result = calculator.calculate_with_details("ABC", "AC")
        assert len(result["dp_table"]) > 0
        assert len(result["dp_table"][0]) > 0

    def test_generate_report(self, calculator, temp_dir):
        """Test report generation."""
        result = calculator.calculate_with_details("ABC", "AC")
        report_path = temp_dir / "report.txt"
        report = calculator.generate_report(result, output_path=str(report_path))

        assert report_path.exists()
        assert "LONGEST COMMON SUBSEQUENCE" in report
        assert "DYNAMIC PROGRAMMING TABLE" in report
        assert "ABC" in report
        assert "AC" in report

    def test_dp_table_structure(self, calculator):
        """Test that DP table has correct structure."""
        calculator.lcs_length("ABC", "AC")
        assert len(calculator.dp_table) == 4  # len("ABC") + 1
        assert len(calculator.dp_table[0]) == 3  # len("AC") + 1

    def test_backtrack_correctness(self, calculator):
        """Test that backtracking produces correct LCS."""
        str1, str2 = "ABCDGH", "AEDFHR"
        lcs = calculator.lcs(str1, str2)
        length = calculator.lcs_length(str1, str2)
        assert len(lcs) == length
        assert self._is_subsequence(lcs, str1)
        assert self._is_subsequence(lcs, str2)

    def test_lcs_is_subsequence(self, calculator):
        """Test that LCS is a valid subsequence of both strings."""
        test_cases = [
            ("ABCDGH", "AEDFHR"),
            ("AGGTAB", "GXTXAYB"),
            ("ABCDEF", "ACDF"),
        ]

        for str1, str2 in test_cases:
            lcs = calculator.lcs(str1, str2)
            assert self._is_subsequence(lcs, str1)
            assert self._is_subsequence(lcs, str2)

    def test_lcs_optimal_length(self, calculator):
        """Test that LCS has optimal length."""
        str1, str2 = "ABCDGH", "AEDFHR"
        lcs = calculator.lcs(str1, str2)
        length = calculator.lcs_length(str1, str2)
        assert len(lcs) == length

    def test_multiple_calls(self, calculator):
        """Test multiple LCS calculations."""
        result1 = calculator.lcs("ABC", "AC")
        result2 = calculator.lcs("XYZ", "XZ")
        assert result1 == "AC"
        assert result2 == "XZ"

    def test_large_strings(self, calculator):
        """Test with larger strings."""
        str1 = "ABCDEFGHIJKLMNOP"
        str2 = "ACEGIKMOQ"
        lcs = calculator.lcs(str1, str2)
        assert len(lcs) > 0
        assert self._is_subsequence(lcs, str1)
        assert self._is_subsequence(lcs, str2)

    def test_single_character_strings(self, calculator):
        """Test with single character strings."""
        assert calculator.lcs("A", "A") == "A"
        assert calculator.lcs("A", "B") == ""
        assert calculator.lcs("A", "") == ""

    def test_repeated_characters(self, calculator):
        """Test with repeated characters."""
        lcs = calculator.lcs("AAA", "AAA")
        assert lcs == "AAA"

        lcs = calculator.lcs("AAB", "AAC")
        assert "AA" in lcs

    def _is_subsequence(self, sub: str, string: str) -> bool:
        """Helper method to check if sub is subsequence of string."""
        if not sub:
            return True

        i = 0
        for char in string:
            if i < len(sub) and char == sub[i]:
                i += 1

        return i == len(sub)
