# Changelog

All notable changes to RinseKit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-01-10

### Added
- Initial public release of RinseKit (vibe-sweeper)
- AI phrase detection in code files
- Long comment block detection
- Support for multiple languages:
  - Python (`.py`)
  - JavaScript (`.js`, `.jsx`)
  - TypeScript (`.ts`, `.tsx`)
  - HTML (`.html`)
  - CSS (`.css`)
  - JSON (`.json`)
- Three CLI commands:
  - `scan` - Scan and generate report
  - `run` - Scan with optional formatter execution
  - `check` - CI mode that exits non-zero on issues
- Optional formatter integration:
  - `ruff` for Python
  - `biome` for JavaScript/TypeScript
- Markdown report generation
- YAML-based configuration system
- Comprehensive test suite with 95% code coverage
- CI/CD workflow with GitHub Actions
- Full documentation (README, CONTRIBUTING)
- MIT License

### Features
- Configurable AI phrase detection
- Configurable comment block length threshold
- Ignore patterns for common directories (node_modules, __pycache__, etc.)
- UTF-8 and latin-1 encoding support
- Clean, readable Markdown output

[0.1.0]: https://github.com/beerberidie/RinseKit/releases/tag/v0.1.0

