# Stems - Audio Processing Toolkit

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)]()

A Python toolkit for downloading YouTube audio, analyzing BPM/key, and separating audio stems using Demucs. Features an elegant CLI with progress bars, automatic metadata detection, and organized output.

## ✨ Features

- 🎵 **YouTube Audio Download** - Download high-quality audio from YouTube videos
- 🎹 **BPM & Key Detection** - Automatically detect tempo and musical key
- 🎧 **Stem Separation** - Split audio into vocals and instrumentals using Demucs
- 🌐 **TuneBat Integration** - Scrape accurate BPM/key from TuneBat database
- 📊 **Audio Analysis** - Analyze tracks using Essentia library
- 🧪 **Well-Tested** - 55+ unit and integration tests with high coverage
- 📦 **Modular Design** - Use as CLI or import as Python library
- ✨ **Polished UX** - Progress bars, auto-generated markdown, browser/Finder integration

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/stems.git
cd stems

# Create and activate virtual environment (recommended)
python3 -m venv demucs-env
source demucs-env/bin/activate  # On Windows: demucs-env\Scripts\activate

# Install the package
pip install -e .

# Install with optional features
pip install -e ".[audio,scraping]"

# Install development dependencies
pip install -r requirements-dev.txt
```

### Basic Usage

**As Command Line Tool:**

```bash
# Download YouTube audio, detect BPM/key, and split stems (all-in-one)
./yt "https://youtube.com/watch?v=..."

# With manual BPM/key override
./yt "https://youtube.com/watch?v=..." 128 "A Minor"

# Or use the installed command
stems-yt "https://youtube.com/watch?v=..."

# Split audio into stems only
stems-split path/to/audio.wav
# or
python split_stems.py path/to/audio.wav
```

The `yt` command will:
- 📥 Download high-quality audio from YouTube
- 🎹 Detect BPM and key (via TuneBat and/or Essentia)
- ✂️ Split into vocals and instrumental stems
- 📝 Generate a markdown summary file
- 🌐 Open Google search for manual verification
- 📂 Open Finder/Explorer with the output files

**As Python Library:**

```python
# Download YouTube audio
from src.downloader.youtube import download_youtube_audio, get_youtube_title

title = get_youtube_title("https://youtube.com/...")
audio_path = download_youtube_audio(url, "/output/dir")

# Analyze audio
from src.audio.analysis import analyze_audio_bpm_key

bpm, key, sources = analyze_audio_bpm_key("/path/to/audio.wav")
print(f"BPM: {bpm}, Key: {key}")

# Split stems
from src.audio.stem_splitter import split_audio_stems

vocals, instrumental = split_audio_stems("/path/to/audio.wav")

# Sanitize filenames
from src.utils.sanitization import sanitize_filename

safe_name = sanitize_filename("Song (feat. Artist)")
```

## 📋 Requirements

### Required

- Python 3.10+
- yt-dlp
- tqdm (for progress bars)

### Optional

- **essentia** - For audio analysis (BPM/key detection)
- **demucs** - For stem separation
- **selenium + undetected-chromedriver** - For TuneBat scraping

Install all dependencies:

```bash
pip install -r requirements.txt

# For development
pip install -r requirements-dev.txt
```

## 📁 Project Structure

```
stems/
├── src/                        # Source code
│   ├── audio/                  # Audio processing (analysis, stem splitting)
│   ├── cli/                    # Command-line interfaces
│   │   ├── yt_cli.py          # YouTube download + analysis CLI
│   │   └── split_stems_cli.py # Stem splitting CLI
│   ├── downloader/             # YouTube downloads
│   ├── scrapers/               # Web scraping (TuneBat)
│   └── utils/                  # Shared utilities
├── tests/                      # Unit & integration tests (55+ tests)
├── yt                          # YouTube download wrapper script
├── split_stems.py              # Stem splitting wrapper script
├── run_tests.sh                # Test runner
├── run_integration_tests.sh    # Integration test runner
├── requirements.txt            # Production dependencies
├── requirements-dev.txt        # Development dependencies
└── pyproject.toml              # Package configuration
```

## 🧪 Testing

The project has 55+ tests with comprehensive coverage.

```bash
# Run all tests using the test script
./run_tests.sh

# Or run unit tests directly (fast, no network)
pytest tests/ --ignore=tests/test_integration.py

# Run all tests including integration tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run integration tests only (validates real YouTube URLs)
./run_integration_tests.sh
# or
pytest tests/test_integration.py -v -s
```

For detailed testing documentation, see [TESTING.md](TESTING.md).

## 🏗️ Architecture

The project follows a layered architecture with clear separation of concerns:

```
CLI Layer (yt, split_stems.py)
    ↓
Business Logic (audio, downloader, scrapers)
    ↓
Utilities (subprocess, sanitization, file ops)
    ↓
External Dependencies (yt-dlp, demucs, essentia)
```

Each module is:

- ✅ Independently testable
- ✅ Focused on single responsibility
- ✅ Loosely coupled
- ✅ Well-documented with type hints

For detailed architecture documentation, see [ARCHITECTURE.md](ARCHITECTURE.md).

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on:

- How to set up your development environment
- Our coding standards and best practices
- How to submit pull requests
- How to report bugs

## 📊 Design Principles

### 1. Separation of Concerns

Each module has a single, well-defined responsibility:

- `sanitization.py` → String cleaning
- `youtube.py` → YouTube downloads
- `analysis.py` → Audio analysis

### 2. Testability

- All external dependencies are mocked in tests
- Functions accept parameters (dependency injection)
- Pure functions wherever possible

### 3. Type Safety

- Type hints throughout the codebase
- Better IDE support and early error detection

### 4. Comprehensive Documentation

- Docstrings on all public functions
- Detailed guides for users and developers
- Examples for common use cases

## 📝 Examples

### Complete Workflow (Download + Analyze + Split)

The easiest way is to use the CLI:

```bash
./yt "https://youtube.com/watch?v=dQw4w9WgXcQ"
```

This creates an organized output directory with:
- Original audio (WAV)
- Vocals stem
- Instrumental stem
- Markdown file with metadata

### Download and Analyze Programmatically

```python
from src.downloader.youtube import download_youtube_audio, get_youtube_title
from src.audio.analysis import analyze_audio_bpm_key
from src.utils.sanitization import sanitize_filename

# Get track info
url = "https://youtube.com/watch?v=..."
title = get_youtube_title(url)
safe_title = sanitize_filename(title)

# Download audio
audio_path = download_youtube_audio(url, f"./downloads/{safe_title}")

# Analyze
bpm, key, sources = analyze_audio_bpm_key(audio_path)
print(f"Track: {title}")
print(f"BPM: {bpm}")
print(f"Key: {key}")
print(f"Detected by: {', '.join(sources)}")
```

### Split Audio Stems

```python
from src.audio.stem_splitter import split_audio_stems

# Split into vocals and instrumental
vocals_path, instrumental_path = split_audio_stems(
    "my_song.wav",
    output_dir="./output",
    two_stems=True,
    stem_type="vocals"
)

print(f"Vocals: {vocals_path}")
print(f"Instrumental: {instrumental_path}")
```

### Scrape TuneBat Metadata

```python
from src.scrapers.tunebat import scrape_tunebat_info, is_tunebat_available

if is_tunebat_available():
    bpm, key, camelot = scrape_tunebat_info("Song Title")
    print(f"TuneBat data: {bpm} BPM, {key}, Camelot {camelot}")
else:
    print("TuneBat dependencies not installed")
    print("Install with: pip install undetected-chromedriver selenium")
```

## 🐛 Troubleshooting

### "yt-dlp not found"

```bash
pip install yt-dlp
```

### "Essentia not available"

```bash
pip install essentia
```

### "TuneBat scraping not working"

```bash
pip install undetected-chromedriver selenium
```

### Tests failing

```bash
# Make sure dev dependencies are installed
pip install -r requirements-dev.txt

# Run unit tests only (no network required)
pytest tests/ --ignore=tests/test_integration.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube download
- [Demucs](https://github.com/facebookresearch/demucs) - Stem separation
- [Essentia](https://essentia.upf.edu/) - Audio analysis
- [TuneBat](https://tunebat.com/) - Music metadata database

## 📞 Support

- 🐛 [Report a Bug](https://github.com/yourusername/stems/issues/new?template=bug_report.md)
- 💡 [Request a Feature](https://github.com/yourusername/stems/issues/new?template=feature_request.md)
- 📖 [Documentation](https://github.com/yourusername/stems/wiki)

## 🗺️ Roadmap

- [x] Progress bars for better UX
- [x] Auto-generated markdown summaries
- [x] Browser integration for verification
- [x] Finder/Explorer integration
- [ ] Add support for more stem separation types (drums, bass, other)
- [ ] Implement playlist batch processing
- [ ] Add GUI interface
- [ ] Support for more music metadata sources
- [ ] Docker container for easy deployment
- [ ] CI/CD pipeline with GitHub Actions

---

Made with ❤️ for music producers and audio enthusiasts
