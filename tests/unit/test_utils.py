"""Unit tests for utility functions."""

from __future__ import annotations

import pytest

from claude_code_setup.utils.helpers import sanitize_string, validate_input


class TestSanitizeString:
    """Tests for sanitize_string function."""

    @pytest.mark.unit
    def test_removes_special_characters(self) -> None:
        """Test that special characters are removed."""
        assert sanitize_string("Hello!@#World") == "HelloWorld"

    @pytest.mark.unit
    def test_preserves_alphanumeric(self) -> None:
        """Test that alphanumeric characters are preserved."""
        assert sanitize_string("Test123") == "Test123"

    @pytest.mark.unit
    def test_preserves_spaces(self) -> None:
        """Test that spaces are preserved."""
        assert sanitize_string("Hello World") == "Hello World"


class TestValidateInput:
    """Tests for validate_input function."""

    @pytest.mark.unit
    def test_returns_value_when_not_none(self) -> None:
        """Test that value is returned when not None."""
        assert validate_input("value", "default") == "value"

    @pytest.mark.unit
    def test_returns_default_when_none(self) -> None:
        """Test that default is returned when value is None."""
        assert validate_input(None, "default") == "default"

    @pytest.mark.unit
    def test_works_with_different_types(self) -> None:
        """Test with various types."""
        assert validate_input(42, 0) == 42
        assert validate_input(None, 0) == 0
        assert validate_input([1, 2], []) == [1, 2]
