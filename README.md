# Claude Code Setup

[![CI](https://github.com/jfabend/claude_code_setup/actions/workflows/ci.yml/badge.svg)](https://github.com/jfabend/claude_code_setup/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/jfabend/claude_code_setup/branch/main/graph/badge.svg)](https://codecov.io/gh/jfabend/claude_code_setup)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

A Claude Code orchestration framework with specialized AI agents, GitHub integration, and modern Python tooling for building robust software projects.

## Features

- Modern Python project structure (src layout)
- Fast dependency management with UV
- Comprehensive testing with pytest
- Code quality with Ruff (linting & formatting)
- Type checking with mypy
- Pre-commit hooks for automated checks
- GitHub Actions CI/CD pipeline
- Multi-Python version testing with tox
- 12 specialized AI agents for different development roles
- GitHub integration commands (PR creation, issue solving)
- Project context maintenance skill for agents

## Before you start, please read these general instructions:
- Global guidelines for Claude Code
    - You can provide Claude Code with **global project-agnostic guidelines**
    - In this example, this global CLAUDE.md contains guidelines how it should organize and orchestrate itself
    - To provide your local Claude Code with those guidelines, all the files from the folder HOME_DIR_FILES must be copied to your home directory
    - On macOS, that would be ~/.claude
    - On Windows, it's C:\Users\<your-username>\.claude
- **Project-specific guidelines** for Claude Code live inside the CLAUDE.md in this repository.
- In **.claude/agents** you can see how you can set up individual agents, which Claude Code can spawn if necessary.
- In **.claude/skills** you can see how to set up skills which the agents can use.
- In **.claude/commands** you set up your own slash commands which YOU as user can use via the Claude Code CLI to run repetitive workflows.
    - Before starting slash commands, evaluate whether you want to run them in plan mode or act mode.
- Important configurations in *settings.json*
    - You can set up global project-agnostic settings.json in your home directory (like described above)
    - And you can set up project-specific settings.json in this project repo (.claude/settings.json)
    - **Permissions**: Configure what kind of bash commands Claude Code is allowed to run
    - **Default Mode**: Define the default mode (plan or act) which will be selected when starting the Claude Code CLI
    - **Hooks**:
        - Hooks are extremely important for Claude Code
        - With hooks, you can provide Claude Code with automated feedback right after its actions / tool use (e.g., linting or testing right after writing code).
        - Hooks can also be used to enforce a certain behavior while starting Claude Code or when Claude Code thinks it has completed the task.

## AI Agents

This framework includes 12 specialized agents in `.claude/agents/` for different development tasks:

| Agent | Purpose |
|-------|---------|
| **architect** | Designs system and component architecture, creates ADRs |
| **implementer** | Writes production code that satisfies tests and requirements |
| **test-writer** | Creates comprehensive tests following TDD principles |
| **code-reviewer** | Performs systematic code reviews for quality and security |
| **refactorer** | Improves code structure while preserving behavior |
| **code-simplifier** | Reduces complexity and improves readability |
| **debugger** | Investigates bugs and proposes minimal targeted fixes |
| **api-designer** | Designs robust REST and GraphQL APIs |
| **docs-writer** | Creates and maintains project documentation |
| **database-specialist** | Handles database architecture, design, and optimization |
| **cloud-platform-architect** | Designs cloud infrastructure solutions (AWS, Azure, GCP) |
| **project-librarian** | Maintains accurate project context documentation |

## Commands

The framework provides GitHub integration commands in `.claude/commands/`:

| Command | Description |
|---------|-------------|
| `/create-pr` | Creates GitHub Pull Requests with auto-generated title and body |
| `/solve-issue` | Fetches and solves GitHub issues using TDD workflow |
| `/plan-to-issues` | Converts plan files to GitHub issues (epic + sub-issues) |
| `/review-pr` | Reviews GitHub Pull Requests with detailed feedback |

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
├── .claude/
│   ├── agents/               # 12 specialized AI agents
│   ├── commands/             # GitHub integration commands
│   └── skills/               # Project context maintenance
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
