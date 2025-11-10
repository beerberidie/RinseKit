# RinseKit (vibe-sweeper)

[![CI](https://github.com/beerberidie/RinseKit/actions/workflows/ci.yml/badge.svg)](https://github.com/beerberidie/RinseKit/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://github.com/beerberidie/RinseKit/releases)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**RinseKit** is a CLI tool that scans a repository for "vibe-coded" / AI-ish mess
and produces a simple report. It can optionally run formatters like `ruff` (Python)
and `biome` (JS/TS/etc) if they are installed on your PATH.

This is a **v1 MVP** – focused on:
- Scanning files
- Detecting AI-style phrases & long comment blocks
- Producing a Markdown report
- Optional formatting pass via external tools

## Installation

From the project root:

```bash
pip install .
```

Or, in editable mode:

```bash
pip install -e .
```

## Usage

Scan the current directory (no changes applied):

```bash
vibe-sweeper scan .
```

Generate a report and run safe formatters where possible:

```bash
vibe-sweeper run . --apply
```

Check mode for CI (exits with non-zero code if issues are found):

```bash
vibe-sweeper check .
```

## Configuration

You can create a `vibe.yaml` at the project root to override defaults.

See `src/vibe_sweeper/config/default_rules.yaml` for the base configuration.

Example `vibe.yaml`:

```yaml
ai_phrases:
  - "as an ai language model"
  - "in this code snippet"
  - "this function is responsible for"
  - "custom phrase to detect"
max_comment_block_lines: 15
```

## Features

- 🔍 **AI Phrase Detection** - Identifies common AI-generated code patterns
- 📝 **Long Comment Block Detection** - Flags overly verbose comment blocks
- 🎨 **Formatter Integration** - Optional integration with `ruff` and `biome`
- 📊 **Markdown Reports** - Clean, readable reports in Markdown format
- ⚙️ **Configurable** - Customize detection rules via YAML config
- 🚀 **CI/CD Ready** - Check mode for continuous integration pipelines

## Supported Languages

- Python (`.py`)
- JavaScript (`.js`, `.jsx`)
- TypeScript (`.ts`, `.tsx`)
- HTML (`.html`)
- CSS (`.css`)
- JSON (`.json`)

## Development

### Running Tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=vibe_sweeper --cov-report=term-missing
```

### Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Built to help clean up AI-generated code and maintain code quality standards.
