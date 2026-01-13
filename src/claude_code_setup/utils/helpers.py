"""Helper utility functions."""

from __future__ import annotations

import re
from typing import TypeVar

T = TypeVar("T")


def sanitize_string(value: str) -> str:
    """
    Sanitize a string by removing special characters.

    Args:
        value: The string to sanitize.

    Returns:
        A sanitized string with only alphanumeric characters and spaces.
    """
    return re.sub(r"[^a-zA-Z0-9\s]", "", value).strip()


def validate_input(value: T | None, default: T) -> T:
    """
    Validate input and return default if None.

    Args:
        value: The value to validate.
        default: The default value to return if value is None.

    Returns:
        The value if not None, otherwise the default.
    """
    return value if value is not None else default
