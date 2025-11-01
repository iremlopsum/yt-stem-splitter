# Contributing to Stems

Thank you for your interest in contributing to Stems! This document provides guidelines and instructions for contributing.

## 🎯 Ways to Contribute

- 🐛 Report bugs
- 💡 Suggest new features
- 📝 Improve documentation
- 🧪 Add tests
- 🔧 Fix issues
- ⚡ Optimize performance

## 🚀 Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/iremlopsum/stems.git
cd stems
```

### 2. Set Up Development Environment

```bash
# Create virtual environment (Python 3.10+)
python3 -m venv demucs-env
source demucs-env/bin/activate  # On Windows: demucs-env\Scripts\activate

# Install in development mode with all dependencies
pip install -e ".[audio,scraping,dev]"

# Or install requirements separately
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Verify installation
./run_tests.sh
# or
pytest tests/ --ignore=tests/test_integration.py
```

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-number-description
```

## 📝 Development Guidelines

### Code Style

We follow PEP 8 and use automated tools:

```bash
# Format code
black src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/
```

### Code Standards

1. **Type Hints** - Use type hints for all function signatures
2. **Docstrings** - Add docstrings to all public functions
3. **Error Handling** - Handle errors gracefully with informative messages
4. **Testing** - All new code must include tests

### Example Code

```python
from typing import Optional, List


def process_audio(
    audio_path: str,
    sample_rate: int = 44100
) -> Optional[dict]:
    """
    Process audio file and extract features.
    
    Args:
        audio_path: Path to audio file
        sample_rate: Sample rate for processing (default: 44100)
        
    Returns:
        Dictionary with extracted features or None if processing fails
        
    Raises:
        FileNotFoundError: If audio file doesn't exist
        ValueError: If sample rate is invalid
        
    Example:
        >>> features = process_audio("/path/to/audio.wav")
        >>> print(features['bpm'])
        128
    """
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    
    if sample_rate <= 0:
        raise ValueError(f"Invalid sample rate: {sample_rate}")
    
    try:
        # Processing logic here
        return {"bpm": 128, "key": "A Minor"}
    except Exception as e:
        print(f"Error processing audio: {e}")
        return None
```

## 🧪 Testing

### Writing Tests

All new features must include tests:

```python
# tests/test_your_feature.py
import unittest
from unittest.mock import patch, MagicMock
from src.your_module import your_function


class TestYourFeature(unittest.TestCase):
    """Test cases for your feature."""
    
    def test_basic_functionality(self):
        """Test basic functionality works."""
        result = your_function("input")
        self.assertEqual(result, "expected")
    
    @patch('src.your_module.external_dependency')
    def test_with_mocking(self, mock_dep):
        """Test with mocked dependencies."""
        mock_dep.return_value = "mocked_value"
        result = your_function("input")
        self.assertEqual(result, "expected")
    
    def test_error_handling(self):
        """Test error handling."""
        with self.assertRaises(ValueError):
            your_function(None)
```

### Running Tests

The project has 55 tests (39 unit, 16 integration).

```bash
# Run all unit tests with coverage
./run_tests.sh

# Run unit tests manually
pytest tests/ --ignore=tests/test_integration.py

# Run with coverage
pytest --cov=src --cov-report=html

# Run integration tests (requires network)
./run_integration_tests.sh
# or
pytest tests/test_integration.py -v -s
```

### Test Coverage

- Aim for at least 80% test coverage
- All new functions must be tested
- Include edge cases and error conditions
- The project currently maintains high test coverage across all modules

## 📋 Pull Request Process

### 1. Ensure Quality

Before submitting, make sure:

```bash
# Run all tests with coverage
./run_tests.sh

# Or run manually:
# Format code
black src/ tests/

# Check linting
flake8 src/ tests/

# Run all tests
pytest

# Check coverage
pytest --cov=src --cov-report=term-missing
```

### 2. Commit Messages

Use clear, descriptive commit messages:

```bash
# Good examples:
git commit -m "Add BPM detection with Essentia"
git commit -m "Fix bug in key normalization for flat notes"
git commit -m "Update documentation for stem splitting"

# Bad examples:
git commit -m "fix stuff"
git commit -m "update"
git commit -m "wip"
```

### 3. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:
- Clear description of changes
- Reference any related issues
- Screenshots if UI changes
- Test results

### 4. PR Checklist

- [ ] Code follows project style guidelines
- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] No linting errors
- [ ] Branch is up to date with main

## 🐛 Reporting Bugs

### Before Reporting

1. Check if issue already exists
2. Test with latest version
3. Gather relevant information

### Bug Report Template

```markdown
**Describe the bug**
A clear and concise description.

**To Reproduce**
Steps to reproduce:
1. Run command '...'
2. With input '...'
3. See error

**Expected behavior**
What you expected to happen.

**Actual behavior**
What actually happened.

**Environment:**
- OS: [e.g. macOS 14.0, Ubuntu 22.04, Windows 11]
- Python version: [e.g. 3.10.0, 3.11.0, 3.12.0]
- Package version: [e.g. 0.1.0]

**Additional context**
Error messages, logs, screenshots, etc.
```

## 💡 Suggesting Features

### Feature Request Template

```markdown
**Feature Description**
Clear and concise description of the feature.

**Use Case**
Describe the problem this feature would solve.

**Proposed Solution**
How you envision this feature working.

**Alternatives Considered**
Other solutions you've thought about.

**Additional Context**
Mockups, examples, references, etc.
```

## 📚 Documentation

### When to Update Documentation

- Adding new features
- Changing APIs
- Fixing bugs that affect usage
- Improving clarity

### Documentation Files

- `README.md` - Overview and quick start
- `TESTING.md` - Testing guide
- `ARCHITECTURE.md` - System design
- `CONTRIBUTING.md` - This file

### Docstring Format

```python
def function_name(param1: str, param2: int = 0) -> bool:
    """
    One-line summary.
    
    More detailed description if needed.
    Can span multiple lines.
    
    Args:
        param1: Description of param1
        param2: Description of param2 (default: 0)
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When this happens
        TypeError: When that happens
        
    Example:
        >>> result = function_name("test", 5)
        >>> print(result)
        True
    """
```

## 🏗️ Project Structure

When adding new features, follow the project structure:

```
src/
├── audio/          # Audio processing (analysis, stem splitting)
├── cli/            # Command-line interfaces
├── downloader/     # Download logic (YouTube, etc.)
├── scrapers/       # Web scraping (TuneBat, etc.)
└── utils/          # Shared utilities

tests/
├── test_*.py       # Unit tests (one file per module)
└── test_integration.py  # Integration tests
```

### Adding a New Module

1. Create module file in appropriate `src/` subdirectory
2. Add `__init__.py` exports
3. Create corresponding test file
4. Update documentation

Example:
```bash
# New audio analyzer
touch src/audio/new_analyzer.py
touch tests/test_new_analyzer.py

# Update exports
# Add to src/audio/__init__.py:
from .new_analyzer import analyze_function
__all__ = [..., "analyze_function"]
```

## 🔄 Development Workflow

### Typical Workflow

1. **Pick an issue** or create one
2. **Discuss** approach in issue comments
3. **Fork & clone** repository
4. **Create branch** from main
5. **Implement** feature/fix
6. **Add tests** for new code
7. **Update docs** if needed
8. **Run tests** and linting
9. **Commit** with clear messages
10. **Push** and create PR
11. **Address** review comments
12. **Merge** when approved

### Code Review Process

- At least one maintainer approval required
- All tests must pass
- No merge conflicts
- Documentation updated
- Code follows style guidelines

## ❓ Getting Help

- 💬 [GitHub Discussions](https://github.com/iremlopsum/stems/discussions)
- 🐛 [Issue Tracker](https://github.com/iremlopsum/stems/issues)
- 📧 Email: your.email@example.com

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

Contributors will be:
- Listed in README.md
- Mentioned in release notes
- Given credit in commit history

Thank you for contributing to Stems! 🎵

