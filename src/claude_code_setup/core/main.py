"""Main module with core functionality."""

from __future__ import annotations


def example_function(name: str, count: int = 1) -> str:
    """
    Generate a greeting message.

    Args:
        name: The name to greet.
        count: Number of times to repeat the greeting.

    Returns:
        A greeting string repeated count times.
    """
    greeting = f"Hello, {name}!"
    return " ".join([greeting] * count)


def main() -> None:
    """Entry point for the application."""
    print(example_function("World"))


if __name__ == "__main__":
    main()
