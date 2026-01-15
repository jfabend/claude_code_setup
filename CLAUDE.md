## Project Overview

 - Claude Code orchestration framework with specialized agents, commands, and skills
 - Uses src-layout pattern (src/claude_code_setup/)
 - Tests live in tests/unit/, tests/integration/, tests/e2e/

## Available Agents

 - `implementer` - Writes production code following SOLID principles
 - `architect` - Designs system architecture and ADRs
 - `test-writer` - Creates tests using TDD approach
 - `code-reviewer` - Reviews PRs and code quality
 - `debugger` - Debugs issues and fixes bugs
 - `api-designer` - Designs API interfaces
 - `docs-writer` - Writes documentation
 - `refactorer` - Improves code structure
 - `code-simplifier` - Simplifies complex code
 - `project-librarian` - Manages project knowledge
 - `cloud-platform-architect` - Designs cloud architecture
 - `database-specialist` - Designs databases

## Available Commands

 Commands are located in `.claude/commands/`:
 - `create-pr` - Creates GitHub PRs with auto-generated title/body
 - `solve-issue` - Fetches and solves GitHub issues with TDD
 - `plan-to-issues` - Converts plan files to GitHub issues (epic + sub-issues)
 - `review-pr` - Reviews GitHub pull requests

## Skills

 Skills are located in `.claude/skills/`:
 - `maintaining-project-context` - Updates CLAUDE.md/AGENTS.md when code contracts change

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