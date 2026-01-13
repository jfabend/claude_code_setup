# Claude Code Setup

[![CI](https://github.com/jfabend/claude_code_setup/actions/workflows/ci.yml/badge.svg)](https://github.com/jfabend/claude_code_setup/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/jfabend/claude_code_setup/branch/main/graph/badge.svg)](https://codecov.io/gh/jfabend/claude_code_setup)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

A starting point for Claude Code projects with modern Python tooling.

## Features

- Modern Python project structure (src layout)
- Fast dependency management with UV
- Comprehensive testing with pytest
- Code quality with Ruff (linting & formatting)
- Type checking with mypy
- Pre-commit hooks for automated checks
- GitHub Actions CI/CD pipeline
- Multi-Python version testing with tox

## Requirements

- Python 3.12+
- [UV](https://docs.astral.sh/uv/) (recommended) or pip

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/jfabend/claude_code_setup.git
cd claude_code_setup

# Install UV (if not already installed)
# On macOS/Linux:
curl -LsSf https://astral.sh/uv/install.sh | sh
# On Windows:
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Create virtual environment and install dependencies
uv sync --dev

# Install pre-commit hooks
uv run pre-commit install
```

### Development

```bash
# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov

# Run linting
uv run ruff check .

# Run formatting
uv run ruff format .

# Run type checking
uv run mypy src

# Run all checks (like CI)
uv run tox
```

### Running Tests by Category

```bash
# Run only unit tests
uv run pytest -m unit

# Run only integration tests
uv run pytest -m integration

# Run only e2e tests
uv run pytest -m e2e

# Skip slow tests
uv run pytest -m "not slow"
```

## Project Structure

```
claude_code_setup/
├── src/claude_code_setup/    # Source code
│   ├── core/                 # Core functionality
│   └── utils/                # Utility functions
├── tests/                    # Test suite
│   ├── unit/                 # Unit tests
│   ├── integration/          # Integration tests
│   └── e2e/                  # End-to-end tests
└── docs/                     # Documentation
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
