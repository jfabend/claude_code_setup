"""Integration tests."""

from __future__ import annotations

import pytest

from claude_code_setup.core.main import example_function
from claude_code_setup.utils.helpers import sanitize_string


class TestIntegration:
    """Integration tests combining multiple modules."""

    @pytest.mark.integration
    def test_sanitized_greeting(self) -> None:
        """Test greeting with sanitized input."""
        dirty_name = "Claude!@#$%"
        clean_name = sanitize_string(dirty_name)
        result = example_function(clean_name)
        assert result == "Hello, Claude!"
