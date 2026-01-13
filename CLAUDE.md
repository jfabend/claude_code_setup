## Project Overview

 - Currently: Python project template for Claude Code projects
 - Uses src-layout pattern (src/claude_code_setup/)
 - Tests live in tests/unit/, tests/integration/, tests/e2e/
 - After cloning and adjusting this repo, please describe repo structure here

## Key Commands

 uv sync --dev          # Install dependencies
 uv run pytest          # Run tests
 uv run pytest --cov    # Run with coverage
 uv run ruff check .    # Lint
 uv run ruff format .   # Format
 uv run mypy src        # Type check
 uv run tox             # Run all checks

## General guidelines
 - Don’t refactor unrelated code unless asked.

## Coding guidelines

 - All added code must be portable (Linux, Windows, macOS)
 - Test-driven development: Add tests firsts, then add the actual code
 - Quality gate: tests pass and changes combile/build (when applicable)
 - All code should follow the SOLID guidelines
 - Double quotes, 88-char line length
 - Full type hints required (MyPy strict)
 - Docstrings for public functions
 - Use from __future__ import annotations
 - Test markers: @pytest.mark.unit, @pytest.mark.integration, @pytest.mark.e2e
 - 80% test coverage minimum enforced

## Commit Format (Conventional Commits)

 - feat: new features
 - fix: bug fixes
 - docs: documentation
 - test: tests
 - refactor: improvements
 - chore: maintenance