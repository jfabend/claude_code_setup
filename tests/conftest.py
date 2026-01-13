"""Pytest configuration and shared fixtures."""

from __future__ import annotations

import pytest


@pytest.fixture
def sample_name() -> str:
    """Provide a sample name for testing."""
    return "TestUser"


@pytest.fixture
def sample_names() -> list[str]:
    """Provide a list of sample names for testing."""
    return ["Alice", "Bob", "Charlie"]


@pytest.fixture(scope="session")
def session_data() -> dict[str, str]:
    """Provide session-scoped test data."""
    return {"key": "value", "environment": "test"}
