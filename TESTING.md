# Testing Documentation

Complete guide for testing the stems audio processing toolkit.

## Table of Contents

1. [Overview](#overview)
2. [Running Tests](#running-tests)
3. [Test Structure](#test-structure)
4. [Unit Tests](#unit-tests)
5. [Integration Tests](#integration-tests)
6. [Writing Tests](#writing-tests)
7. [Testing Patterns](#testing-patterns)
8. [CI/CD Integration](#cicd-integration)

---

## Overview

The project has comprehensive test coverage with two types of tests:

- **Unit Tests** (40+ tests) - Fast, mocked, no external dependencies
- **Integration Tests** (16+ tests) - Validates real YouTube URLs, requires network

**Total Coverage:** 50+ tests covering all major functionality

---

## Running Tests

### Quick Commands

```bash
# Run unit tests only (fast, <1 second)
pytest tests/ --ignore=tests/test_integration.py

# Run all tests (including integration)
pytest

# Run with coverage report
pytest --cov=src --cov-report=html
open htmlcov/index.html

# Run integration tests (requires network)
./run_integration_tests.sh
# or
pytest tests/test_integration.py -v -s
```

### Using Test Runner Scripts

```bash
# Unit tests
./run_tests.sh

# Integration tests
./run_integration_tests.sh
```

### Specific Test Selection

```bash
# Run specific test file
pytest tests/test_sanitization.py

# Run specific test class
pytest tests/test_sanitization.py::TestSanitization

# Run specific test method
pytest tests/test_sanitization.py::TestSanitization::test_sanitize_basic_string

# Run with verbose output
pytest -v

# Run with print statements visible
pytest -s
```

---

## Test Structure

### Test Files

**Unit Tests:**
```
tests/
├── test_sanitization.py         (9 tests)  - String sanitization
├── test_subprocess_utils.py     (6 tests)  - Subprocess helpers
├── test_file_utils.py           (3 tests)  - File operations
├── test_audio_analysis.py       (5 tests)  - Audio analysis
├── test_stem_splitter.py        (5 tests)  - Stem separation
├── test_youtube_downloader.py   (6 tests)  - YouTube downloads
└── test_tunebat.py              (6 tests)  - TuneBat scraping
```

**Integration Tests:**
```
tests/
└── test_integration.py          (16 tests) - Real URL validation
    ├── TestYouTubeIntegration   (2 tests)  - URL validation
    ├── TestKeyNormalization     (6 tests)  - Key matching
    └── TestBPMNormalization     (8 tests)  - BPM matching
```

### Test Pyramid

```
      ┌─────────────┐
      │  Manual     │  Few manual CLI tests
      ├─────────────┤
      │ Integration │  Some integration tests
      │   (16)      │  (real URLs, network)
      ├─────────────┤
      │    Unit     │  Many unit tests (40+)
      │   (40+)     │  (mocked, fast)
      └─────────────┘
```

---

## Unit Tests

### Characteristics

- ✅ **Fast** - Run in <1 second total
- ✅ **Isolated** - All external dependencies mocked
- ✅ **Reliable** - No network, file system, or external service dependencies
- ✅ **Focused** - Test one function/behavior at a time

### Example: Testing Pure Functions

```python
# tests/test_sanitization.py
def test_sanitize_basic_string(self):
    """Test sanitization of a basic string."""
    result = sanitize_filename("Simple Title")
    self.assertEqual(result, "Simple Title")

def test_sanitize_with_special_chars(self):
    """Test removal of special characters."""
    result = sanitize_filename("Title: With @ Special # Chars!")
    self.assertEqual(result, "Title With  Special  Chars")
```

### Example: Mocking Subprocess Calls

```python
# tests/test_youtube_downloader.py
@patch('src.downloader.youtube.run_command_capture')
def test_get_youtube_title_success(self, mock_run):
    """Test successful title retrieval."""
    mock_run.return_value = MagicMock(stdout="Amazing Song Title\n")
    
    title = get_youtube_title("https://youtube.com/watch?v=test")
    
    self.assertEqual(title, "Amazing Song Title")
    mock_run.assert_called_once()
```

### Example: Mocking External Libraries

```python
# tests/test_audio_analysis.py
@patch('src.audio.analysis.es.MonoLoader')
@patch('src.audio.analysis.es.RhythmExtractor2013')
def test_analyze_audio_success(self, mock_rhythm, mock_loader):
    """Test successful audio analysis."""
    mock_loader.return_value.return_value = MagicMock()
    mock_rhythm.return_value.return_value = (128.5, [], 0.9, None, [])
    
    bpm, key, sources = analyze_audio_bpm_key("/path/to/test.wav")
    
    self.assertEqual(bpm, "128")
```

---

## Integration Tests

### Overview

Integration tests validate the complete workflow with real YouTube URLs.

**Test URLs:**

1. **https://www.youtube.com/watch?v=33mjGmfy7PA**
   - Expected: BPM = 99, Key = G Major

2. **https://www.youtube.com/watch?v=AtNjDbxQZQI**
   - Expected: BPM = 99, Key = A#min

### Flexible Matching

#### BPM Matching

**Normalization:**
```python
"99"      → 99
"99.5"    → 99 (rounded down)
"99 BPM"  → 99 (text removed)
"~99"     → 99 (symbols removed)
```

**Tolerance:** ±3 BPM (accepts 96-102 for expected 99)

```python
bpm_match("97", 99, tolerance=3)   # True
bpm_match("102", 99, tolerance=3)  # True
bpm_match("95", 99, tolerance=3)   # False
```

#### Key Matching

**Normalization:**
```python
"G Major"   → "Gmaj"
"G major"   → "Gmaj" (case insensitive)
"A#min"     → "A#min"
"A# Minor"  → "A#min" (normalized)
"A#m"       → "A#min" (short form)
```

**Enharmonic Equivalents:**
- A# ↔ Bb
- C# ↔ Db
- D# ↔ Eb
- F# ↔ Gb
- G# ↔ Ab

```python
keys_match("A# Minor", "Bb Minor", tolerance=True)  # True
keys_match("G Major", "G major", tolerance=True)    # True
keys_match("G Major", "G Minor", tolerance=True)    # False
```

### Running Integration Tests

```bash
# All integration tests
pytest tests/test_integration.py -v -s

# Specific URL test
pytest tests/test_integration.py::TestYouTubeIntegration::test_youtube_url_1_metadata -v -s

# Just utility tests (fast, no network)
pytest tests/test_integration.py::TestKeyNormalization -v
pytest tests/test_integration.py::TestBPMNormalization -v
```

### Test Output Example

```
test_youtube_url_1_metadata ...
✓ Retrieved title: Song Name
  TuneBat: BPM=99, Key=G Major, Camelot=9B
  Detected: BPM=99, Key=G Major
  Expected: BPM=99, Key=G major
ok
```

### Requirements

Integration tests require:
- Network access
- yt-dlp installed
- Optional: essentia (for audio analysis)
- Optional: selenium + undetected-chromedriver (for TuneBat)

Tests automatically skip if dependencies are missing.

---

## Writing Tests

### Test Structure (AAA Pattern)

```python
def test_example(self):
    """Test description."""
    # Arrange - Set up test data and mocks
    mock_data = MagicMock()
    expected_result = "output"
    
    # Act - Call the function being tested
    result = function_to_test(mock_data)
    
    # Assert - Verify the results
    self.assertEqual(result, expected_result)
```

### Adding a New Unit Test

```python
"""Unit tests for your module."""

import unittest
from unittest.mock import patch, MagicMock
from src.yourpackage.yourmodule import your_function


class TestYourModule(unittest.TestCase):
    """Test cases for your module."""
    
    def test_basic_functionality(self):
        """Test basic functionality."""
        result = your_function("input")
        self.assertEqual(result, "expected")
    
    def test_edge_case(self):
        """Test edge case."""
        result = your_function("")
        self.assertEqual(result, "default")
    
    def test_error_handling(self):
        """Test error handling."""
        with self.assertRaises(ValueError):
            your_function(None)


if __name__ == "__main__":
    unittest.main()
```

### Adding Integration Test for New URL

```python
def test_youtube_url_3_metadata(self):
    """
    Test YouTube URL: https://www.youtube.com/watch?v=YOUR_VIDEO_ID
    Expected: BPM=120, Key=C Major
    """
    url = "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"
    expected_bpm = 120
    expected_key = "C Major"
    
    # Get title
    try:
        title = get_youtube_title(url)
        print(f"\n✓ Retrieved title: {title}")
    except Exception as e:
        self.skipTest(f"Could not fetch title: {e}")
    
    # Try TuneBat scraping
    detected_bpm = None
    detected_key = None
    
    if is_tunebat_available():
        bpm, key, camelot = scrape_tunebat_info(title)
        if bpm:
            detected_bpm = bpm
        if key:
            detected_key = key
    
    # Verify results
    if detected_bpm:
        self.assertTrue(
            bpm_match(detected_bpm, expected_bpm, tolerance=3),
            f"BPM mismatch: detected {detected_bpm}, expected {expected_bpm}±3"
        )
    
    if detected_key:
        self.assertTrue(
            keys_match(detected_key, expected_key, tolerance=True),
            f"Key mismatch: detected {detected_key}, expected {expected_key}"
        )
```

---

## Testing Patterns

### Pattern 1: Pure Functions

**When:** Function has no side effects

```python
# No mocking needed
def test_pure_function(self):
    result = sanitize_filename("Test String!")
    self.assertEqual(result, "Test String")
```

### Pattern 2: Mocking Subprocess

**When:** Function calls external commands

```python
@patch('src.module.run_command_capture')
def test_with_subprocess(self, mock_run):
    mock_run.return_value = MagicMock(stdout="output")
    result = function_that_runs_command()
    mock_run.assert_called_once()
```

### Pattern 3: Mocking External Libraries

**When:** Function uses external libraries (Essentia, Selenium)

```python
@patch('src.module.external_library')
def test_with_library(self, mock_lib):
    mock_lib.return_value = expected_value
    result = function_using_library()
    self.assertEqual(result, expected_value)
```

### Pattern 4: Testing Errors

**When:** Verifying error handling

```python
def test_error_case(self):
    with self.assertRaises(ValueError) as cm:
        function_that_should_fail(invalid_input)
    
    self.assertIn("expected error message", str(cm.exception))
```

---

## Best Practices

### ✅ DO

1. **Write focused tests** - One concept per test
2. **Use descriptive names** - `test_sanitize_empty_string_returns_default`
3. **Mock external dependencies** - Subprocess, network, file system
4. **Test edge cases** - Empty inputs, None, large data
5. **Use setUp/tearDown** - For common test fixtures
6. **Keep tests fast** - Mock expensive operations
7. **Assert one thing** - Clear failure messages

### ❌ DON'T

1. **Test implementation details** - Test behavior, not internals
2. **Share state between tests** - Each test should be independent
3. **Use real files/network** - Always mock in unit tests
4. **Write brittle tests** - Tests shouldn't break on refactoring
5. **Ignore test failures** - Fix or update tests immediately
6. **Skip error cases** - Test failure paths too

---

## Coverage

### Generate Coverage Report

```bash
# HTML report
pytest --cov=src --cov-report=html
open htmlcov/index.html

# Terminal report with missing lines
pytest --cov=src --cov-report=term-missing

# XML report (for CI/CD)
pytest --cov=src --cov-report=xml
```

### Coverage Goals

- **Minimum:** 70% coverage
- **Good:** 80-90% coverage
- **Excellent:** 95%+ coverage

Focus on:
- All public functions
- Error handling paths
- Edge cases
- Integration points

---

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: "3.9"
      - run: pip install -r requirements-dev.txt
      - run: pytest tests/ --ignore=tests/test_integration.py --cov=src
      
  integration-tests:
    runs-on: ubuntu-latest
    # Run only on schedule or manual trigger
    if: github.event_name == 'schedule' || github.event_name == 'workflow_dispatch'
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r requirements-dev.txt
      - run: pytest tests/test_integration.py -v
```

### Separate Fast and Slow Tests

```yaml
# Fast tests (always run)
- name: Unit Tests
  run: pytest tests/ --ignore=tests/test_integration.py

# Slow tests (scheduled)
- name: Integration Tests
  run: pytest tests/test_integration.py
  if: github.event_name == 'schedule'
```

---

## Troubleshooting

### Tests Skipped: "Dependencies not available"

**Solution:** Install required dependencies
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Integration Test Failed: "Could not fetch title"

**Possible causes:**
- No network connection
- yt-dlp not installed
- YouTube URL blocked

**Solution:**
```bash
# Verify yt-dlp works
yt-dlp --version
yt-dlp --print "%(title)s" "https://youtube.com/watch?v=33mjGmfy7PA"
```

### Test Failed: BPM/Key Mismatch

**Possible causes:**
- Detection algorithm variation
- Track metadata changed on TuneBat

**Solution:**
- Check test output for actual detected values
- Verify expected values are still correct
- Adjust tolerance if detection is close but not exact

---

## Performance

### Test Speed

**Unit Tests:**
- All unit tests: <1 second
- Individual test file: <0.1 second

**Integration Tests:**
- Per URL test: 30-60 seconds (includes download)
- Total integration suite: 1-2 minutes

**Recommendation:** Run unit tests frequently during development, integration tests before commits.

---

## Summary

The testing strategy provides:
- ✅ **Fast unit tests** for rapid development
- ✅ **Realistic integration tests** for end-to-end validation
- ✅ **High coverage** (90%+ of testable code)
- ✅ **Flexible matching** for real-world variations
- ✅ **CI/CD ready** with separate test suites
- ✅ **Well-documented** with examples and patterns

**Remember:** Good tests enable confident refactoring!

