# Contributing to Claude Code Setup

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing.

## Development Setup

1. Fork and clone the repository
2. Install UV: `curl -LsSf https://astral.sh/uv/install.sh | sh`
3. Install dependencies: `uv sync --dev`
4. Install pre-commit hooks: `uv run pre-commit install`

## Code Style

This project uses:
- **Ruff** for linting and formatting
- **mypy** for type checking
- **Conventional Commits** for commit messages

### Running Checks

```bash
# Format code
uv run ruff format .

# Lint code
uv run ruff check . --fix

# Type check
uv run mypy src
```

## Testing

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov

# Run specific test categories
uv run pytest -m unit
uv run pytest -m integration
```

## Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat: add new feature`
- `fix: resolve bug`
- `docs: update documentation`
- `test: add tests`
- `refactor: code improvements`
- `chore: maintenance tasks`

## Pull Request Process

1. Create a feature branch from `main`
2. Make your changes
3. Ensure all tests pass
4. Update documentation if needed
5. Submit a pull request

## Questions?

Open an issue for questions or discussions.
