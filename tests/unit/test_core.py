"""Unit tests for core module."""

from __future__ import annotations

import pytest

from claude_code_setup.core.main import example_function


class TestExampleFunction:
    """Tests for example_function."""

    @pytest.mark.unit
    def test_basic_greeting(self) -> None:
        """Test basic greeting generation."""
        result = example_function("World")
        assert result == "Hello, World!"

    @pytest.mark.unit
    def test_greeting_with_count(self) -> None:
        """Test greeting with repetition count."""
        result = example_function("Claude", count=3)
        assert result == "Hello, Claude! Hello, Claude! Hello, Claude!"

    @pytest.mark.unit
    def test_empty_name(self) -> None:
        """Test greeting with empty name."""
        result = example_function("")
        assert result == "Hello, !"

    @pytest.mark.unit
    @pytest.mark.parametrize(
        ("name", "count", "expected"),
        [
            ("Alice", 1, "Hello, Alice!"),
            ("Bob", 2, "Hello, Bob! Hello, Bob!"),
            ("", 1, "Hello, !"),
        ],
    )
    def test_parametrized_greetings(self, name: str, count: int, expected: str) -> None:
        """Test various greeting combinations."""
        assert example_function(name, count=count) == expected
