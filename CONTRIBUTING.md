# Contributing to RinseKit

Thank you for your interest in contributing to RinseKit! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue on GitHub with:

- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior vs. actual behavior
- Your environment (OS, Python version, etc.)
- Any relevant code samples or error messages

### Suggesting Enhancements

Enhancement suggestions are welcome! Please create an issue with:

- A clear description of the enhancement
- Use cases and benefits
- Any implementation ideas you might have

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** following the coding standards below
3. **Add tests** for any new functionality
4. **Ensure all tests pass** by running `pytest`
5. **Update documentation** if needed
6. **Submit a pull request** with a clear description of your changes

## Development Setup

### Prerequisites

- Python 3.9 or higher
- Git

### Setting Up Your Development Environment

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/RinseKit.git
cd RinseKit

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package in editable mode with dev dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=vibe_sweeper --cov-report=term-missing

# Run specific test file
pytest tests/test_scanner.py

# Run tests in verbose mode
pytest -v
```

### Code Style

We follow Python best practices:

- **PEP 8** style guide
- **Type hints** where appropriate
- **Docstrings** for all public functions and classes
- **Clear variable names** that describe their purpose

### Project Structure

```
RinseKit/
├── src/vibe_sweeper/       # Main package
│   ├── analysis/           # Metrics and analysis
│   ├── config/             # Configuration handling
│   ├── detectors/          # AI phrase and comment detectors
│   ├── refactors/          # Formatter integration
│   ├── report/             # Report generation
│   ├── cli.py              # CLI commands
│   └── scanner.py          # File scanning logic
├── tests/                  # Test suite
├── examples/               # Example projects
└── docs/                   # Documentation (if any)
```

## Adding New Features

### Adding a New Detector

1. Create a new file in `src/vibe_sweeper/detectors/`
2. Implement your detector function
3. Export it in `src/vibe_sweeper/detectors/__init__.py`
4. Add tests in `tests/test_detectors.py`
5. Update documentation

Example detector structure:

```python
from pathlib import Path
from typing import List, Dict

def detect_something(path: Path, text: str, config: Dict) -> List[Dict]:
    """
    Detect something in the given text.
    
    Args:
        path: Path to the file being analyzed
        text: Content of the file
        config: Configuration dictionary
        
    Returns:
        List of findings, each as a dictionary with:
        - file: str (file path)
        - line: int (line number)
        - kind: str (finding type)
        - other relevant fields
    """
    results = []
    # Your detection logic here
    return results
```

### Adding a New CLI Command

1. Add a new command function in `src/vibe_sweeper/cli.py`
2. Use the `@app.command()` decorator
3. Add tests in `tests/test_cli.py`
4. Update README with usage examples

### Adding Support for New Languages

1. Update `EXT_LANG_MAP` in `src/vibe_sweeper/scanner.py`
2. Update comment detection in `src/vibe_sweeper/detectors/comments.py` if needed
3. Add tests for the new language
4. Update README documentation

## Testing Guidelines

- **Write tests for all new code**
- **Aim for high code coverage** (we target 90%+)
- **Use descriptive test names** that explain what is being tested
- **Test edge cases** and error conditions
- **Use pytest fixtures** for common test setup

Example test structure:

```python
def test_feature_does_something():
    """Test that feature behaves correctly in normal case."""
    # Arrange
    input_data = "test input"
    
    # Act
    result = my_function(input_data)
    
    # Assert
    assert result == expected_output
```

## Documentation

- Update README.md for user-facing changes
- Add docstrings to all public functions
- Include type hints in function signatures
- Add inline comments for complex logic

## Commit Messages

Write clear, concise commit messages:

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit first line to 72 characters
- Reference issues and pull requests when relevant

Examples:
```
Add support for Ruby file detection

Fix AI phrase detection case sensitivity issue (#123)

Update README with new configuration options
```

## Release Process

(For maintainers)

1. Update version in `src/vibe_sweeper/__init__.py` and `pyproject.toml`
2. Update CHANGELOG.md
3. Create a git tag: `git tag -a v0.2.0 -m "Release v0.2.0"`
4. Push tag: `git push origin v0.2.0`
5. Create GitHub release with release notes

## Questions?

If you have questions about contributing, feel free to:

- Open an issue for discussion
- Reach out to the maintainers

## License

By contributing to RinseKit, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to RinseKit! 🎉

