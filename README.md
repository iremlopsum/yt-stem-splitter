# Stems - Audio Processing Toolkit

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-55%20passing-brightgreen.svg)]()

**A complete Python toolkit for downloading YouTube audio, analyzing BPM/key, and separating audio stems using Demucs.** Features an elegant CLI with progress bars, automatic metadata detection, and organized output.

---

## 🚀 Quick Start (2 Minutes)

### Installation

```bash
# Clone the repository
git clone https://github.com/iremlopsum/stems.git
cd stems

# Create and activate virtual environment
python3 -m venv demucs-env
source demucs-env/bin/activate  # On Windows: demucs-env\Scripts\activate

# Install the package
pip install -e .
```

### Your First Command

```bash
# Download, analyze, and split a YouTube track (all-in-one)
./yt "https://youtube.com/watch?v=..."

# That's it! The tool will:
# ✓ Download high-quality audio
# ✓ Detect BPM and key automatically
# ✓ Split into vocals and instrumental
# ✓ Generate a markdown summary
# ✓ Open results in Finder/Explorer
```

---

## ✨ Features

- 🎵 **YouTube Audio Download** - High-quality audio extraction using yt-dlp
- 🎹 **BPM & Key Detection** - Automatic tempo and musical key analysis
- 🎧 **Stem Separation** - Split audio into vocals and instrumentals using Demucs
- 🌐 **TuneBat Integration** - Scrape accurate BPM/key from TuneBat database
- 📊 **Audio Analysis** - Powered by Essentia library
- 🧪 **Well-Tested** - 55+ unit and integration tests with high coverage
- 📦 **Modular Design** - Use as CLI or import as Python library
- ✨ **Polished UX** - Progress bars, auto-generated markdown, browser/Finder integration

---

## 📋 Installation & Setup

### Requirements

**Required:**
- Python 3.10+
- yt-dlp (for YouTube downloads)

**Optional (for full functionality):**
- FFmpeg (for audio conversion)
- essentia (for audio analysis)
- demucs (for stem separation)
- selenium (for TuneBat scraping)

### Complete Installation

```bash
# Clone repository
git clone https://github.com/iremlopsum/stems.git
cd stems

# Create virtual environment (recommended)
python3 -m venv demucs-env
source demucs-env/bin/activate

# Option 1: Install all features
pip install -e ".[audio,scraping]"

# Option 2: Install core only (YouTube download)
pip install -e .

# Option 3: For development
pip install -r requirements-dev.txt
```

### Verify Installation

```bash
# Check that commands are available
stems-yt --help
stems-split --help

# Run tests to verify everything works
./run_tests.sh
```

---

## 💻 Usage

### Command Line Interface

**Complete Workflow (YouTube → Analysis → Stems):**

```bash
# Download, analyze BPM/key, and split stems (all-in-one)
./yt "https://youtube.com/watch?v=..."

# With manual BPM/key override
./yt "https://youtube.com/watch?v=..." 128 "A Minor"

# Or use the installed command
stems-yt "https://youtube.com/watch?v=..."
```

**Output includes:**
- Original audio (WAV format)
- Vocals stem
- Instrumental stem
- Markdown file with metadata
- Auto-opens Google search for verification
- Auto-opens Finder/Explorer with results

**Split Existing Audio:**

```bash
# Split audio file into stems
stems-split path/to/audio.wav

# Or use the script
python split_stems.py path/to/audio.wav
```

### Python Library Usage

**Download YouTube Audio:**

```python
from src.downloader.youtube import download_youtube_audio, get_youtube_title

# Get track info
url = "https://youtube.com/watch?v=..."
title = get_youtube_title(url)

# Download audio
audio_path = download_youtube_audio(url, "/output/dir")
```

**Analyze Audio:**

```python
from src.audio.analysis import analyze_audio_bpm_key

# Detect BPM and key
bpm, key, sources = analyze_audio_bpm_key("/path/to/audio.wav")
print(f"BPM: {bpm}, Key: {key}")
print(f"Detected by: {', '.join(sources)}")
```

**Split Stems:**

```python
from src.audio.stem_splitter import split_audio_stems

# Split into vocals and instrumental
vocals_path, instrumental_path = split_audio_stems(
    "my_song.wav",
    output_dir="./output",
    two_stems=True,
    stem_type="vocals"
)
```

**Scrape Metadata:**

```python
from src.scrapers.tunebat import scrape_tunebat_info, is_tunebat_available

if is_tunebat_available():
    bpm, key, camelot = scrape_tunebat_info("Song Title")
    print(f"TuneBat data: {bpm} BPM, {key}, Camelot {camelot}")
```

**Sanitize Filenames:**

```python
from src.utils.sanitization import sanitize_filename

safe_name = sanitize_filename("Song (feat. Artist)")
```

---

## 🧪 Testing

The project has **55 tests** (39 unit, 16 integration) with high coverage.

### Run Tests

```bash
# Run all unit tests (fast, <1 second)
./run_tests.sh

# Or run manually
pytest tests/ --ignore=tests/test_integration.py

# Run all tests including integration
pytest

# Run with coverage report
pytest --cov=src --cov-report=html
open htmlcov/index.html

# Run integration tests (validates real YouTube URLs)
./run_integration_tests.sh
```

### Test Coverage

```
tests/
├── test_sanitization.py         (9 tests)  - String sanitization
├── test_subprocess_utils.py     (6 tests)  - Subprocess helpers
├── test_file_utils.py           (3 tests)  - File operations
├── test_audio_analysis.py       (5 tests)  - Audio analysis
├── test_stem_splitter.py        (4 tests)  - Stem separation
├── test_youtube_downloader.py   (6 tests)  - YouTube downloads
├── test_tunebat.py              (6 tests)  - TuneBat scraping
└── test_integration.py          (16 tests) - End-to-end workflow
```

**📖 Detailed testing documentation:** See [TESTING.md](TESTING.md)

---

## 🏗️ Architecture

The project follows a clean layered architecture:

```
┌─────────────────────────────────────────┐
│  CLI Layer (yt, split_stems.py)        │  ← User interface
├─────────────────────────────────────────┤
│  Business Logic                          │  ← Core functionality
│  ├─ downloader/ (YouTube)               │
│  ├─ audio/ (analysis, stem splitting)   │
│  └─ scrapers/ (TuneBat)                 │
├─────────────────────────────────────────┤
│  Utilities                               │  ← Shared helpers
│  ├─ subprocess_utils.py                 │
│  ├─ sanitization.py                     │
│  └─ file_utils.py                       │
├─────────────────────────────────────────┤
│  External Dependencies                   │  ← Third-party tools
│  (yt-dlp, demucs, essentia, selenium)   │
└─────────────────────────────────────────┘
```

### Key Design Principles

1. **Separation of Concerns** - Each module has a single responsibility
2. **Testability** - All external dependencies are mockable
3. **Type Safety** - Type hints throughout the codebase
4. **Dependency Flow** - Dependencies only flow downward (no circular imports)

### Project Structure

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
├── requirements.txt            # Production dependencies
├── requirements-dev.txt        # Development dependencies
└── pyproject.toml              # Package configuration
```

**📖 Detailed architecture documentation:** See [ARCHITECTURE.md](ARCHITECTURE.md)

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

### Quick Contribution Guide

1. **Fork and clone** the repository
2. **Set up development environment:**
   ```bash
   python3 -m venv demucs-env
   source demucs-env/bin/activate
   pip install -r requirements-dev.txt
   ```
3. **Create a branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Make your changes** and add tests
5. **Run tests and linting:**
   ```bash
   ./run_tests.sh           # Run tests
   black src/ tests/        # Format code
   flake8 src/ tests/       # Lint code
   ```
6. **Commit and push:**
   ```bash
   git commit -m "Add your feature"
   git push origin feature/your-feature-name
   ```
7. **Create a Pull Request** on GitHub

### Code Standards

- ✅ Use type hints for all function signatures
- ✅ Add docstrings to all public functions
- ✅ Write tests for all new code
- ✅ Follow PEP 8 style guidelines
- ✅ Keep functions focused and single-purpose

**📖 Detailed contributing guide:** See [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 🐛 Troubleshooting

<details>
<summary><b>yt-dlp not found</b></summary>

```bash
pip install yt-dlp
```
</details>

<details>
<summary><b>Essentia not available</b></summary>

```bash
pip install essentia
# Or install with audio extras:
pip install -e ".[audio]"
```
</details>

<details>
<summary><b>TuneBat scraping not working</b></summary>

```bash
pip install selenium
# Also ensure you have Chrome/Chromium installed
# Or install with scraping extras:
pip install -e ".[scraping]"
```
</details>

<details>
<summary><b>Tests failing</b></summary>

```bash
# Make sure dev dependencies are installed
pip install -r requirements-dev.txt

# Run unit tests only (no network required)
pytest tests/ --ignore=tests/test_integration.py
```
</details>

<details>
<summary><b>FFmpeg errors</b></summary>

Install FFmpeg for your system:

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH.
</details>

---

## 📚 Documentation

- **[README.md](README.md)** (this file) - Quick start and overview
- **[TESTING.md](TESTING.md)** - Complete testing guide with 55+ tests
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System design and module structure
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution guidelines
- **[CHANGELOG.md](CHANGELOG.md)** - Version history and release notes
- **[TODO.md](TODO.md)** - Roadmap for Homebrew installation support
- **[OPEN_SOURCE_CHECKLIST.md](OPEN_SOURCE_CHECKLIST.md)** - Pre-publication checklist

---

## 🗺️ Roadmap & Future Plans

### Current Features ✅
- [x] Progress bars for better UX
- [x] Auto-generated markdown summaries
- [x] Browser integration for verification
- [x] Finder/Explorer integration
- [x] Comprehensive test suite (55 tests)

### Planned Features 🚧

**v0.2.0 - Enhanced Audio Processing**
- [ ] Support for 4-stem separation (drums, bass, vocals, other)
- [ ] Playlist batch processing
- [ ] Custom output directory specification
- [ ] Configuration file support

**v0.3.0 - Distribution & UI**
- [ ] GUI interface
- [ ] Docker container
- [ ] **Homebrew installation** (see [TODO.md](TODO.md))
- [ ] Additional metadata sources

**v1.0.0 - Production Ready**
- [ ] Stable public API
- [ ] Full documentation
- [ ] CI/CD pipeline with GitHub Actions
- [ ] Performance optimizations

---

## 📊 Project Stats

- **Lines of Code:** ~2,000
- **Test Coverage:** High (55 tests)
- **Dependencies:** Minimal (yt-dlp required, others optional)
- **Python Version:** 3.10+
- **License:** MIT
- **Status:** Active development

---

## 🙏 Acknowledgments

This project is built on top of amazing open-source tools:

- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)** - YouTube download functionality
- **[Demucs](https://github.com/facebookresearch/demucs)** - State-of-the-art stem separation
- **[Essentia](https://essentia.upf.edu/)** - Comprehensive audio analysis library
- **[TuneBat](https://tunebat.com/)** - Music metadata database

---

## 📞 Support & Community

- 🐛 **[Report a Bug](https://github.com/iremlopsum/stems/issues/new?labels=bug)** - Found an issue? Let us know
- 💡 **[Request a Feature](https://github.com/iremlopsum/stems/issues/new?labels=enhancement)** - Have an idea? We'd love to hear it
- 💬 **[Discussions](https://github.com/iremlopsum/stems/discussions)** - Ask questions, share ideas
- 📖 **[Documentation](https://github.com/iremlopsum/stems/wiki)** - Comprehensive guides

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

You are free to:
- ✅ Use commercially
- ✅ Modify
- ✅ Distribute
- ✅ Private use

---

## 🎯 Use Cases

**For Music Producers:**
- Quickly extract vocals or instrumentals from reference tracks
- Analyze BPM and key for DJ mixing
- Study production techniques by isolating stems

**For DJs:**
- Create acapella versions for mashups
- Match BPM and key for harmonic mixing
- Prepare tracks for live performances

**For Audio Engineers:**
- Analyze audio characteristics
- Extract specific stems for remixing
- Study mixing and mastering techniques

**For Developers:**
- Use as a library in your own projects
- Extend with custom audio processing
- Integrate into larger audio workflows

---

## 🔧 Advanced Usage

### Custom Output Directory

```python
from src.audio.stem_splitter import split_audio_stems

split_audio_stems(
    "track.wav",
    output_dir="/custom/path",
    two_stems=True,
    stem_type="vocals"
)
```

### Batch Processing

```python
import os
from src.audio.stem_splitter import split_audio_stems

audio_files = [f for f in os.listdir("./input") if f.endswith(".wav")]

for audio_file in audio_files:
    print(f"Processing {audio_file}...")
    split_audio_stems(
        os.path.join("./input", audio_file),
        output_dir="./output"
    )
```

### Error Handling

```python
from src.downloader.youtube import download_youtube_audio, get_youtube_title

try:
    title = get_youtube_title(url)
    audio_path = download_youtube_audio(url, output_dir)
except Exception as e:
    print(f"Error downloading: {e}")
```

---

## 📈 Performance Considerations

**Typical Processing Times:**
- YouTube download (3-5 min track): 10-30 seconds
- BPM/Key detection: 5-15 seconds
- Stem separation: 30-90 seconds (depends on track length and hardware)

**System Requirements:**
- **Minimum:** 4GB RAM, 2-core CPU
- **Recommended:** 8GB RAM, 4-core CPU, GPU (for faster Demucs processing)

**Storage:**
- Original audio: ~30-50 MB per track (WAV)
- Stems: ~30-50 MB per stem
- Total: ~100-150 MB per processed track

---

## 🔒 Security & Privacy

- ✅ No telemetry or analytics
- ✅ All processing happens locally
- ✅ No data is sent to external servers (except YouTube/TuneBat queries)
- ✅ Input validation and sanitization
- ✅ Safe subprocess execution (no shell injection)

---

## 📝 Release History

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

**Latest:** v0.1.0 (2025-01-01)
- Initial release
- YouTube download, BPM/key detection, stem separation
- 55 tests with high coverage
- Complete documentation

---

## ❓ FAQ

<details>
<summary><b>Can I use this for commercial projects?</b></summary>

Yes! The MIT license allows commercial use. However, be aware of copyright laws when processing copyrighted music.
</details>

<details>
<summary><b>Which audio formats are supported?</b></summary>

The tool works with any format supported by FFmpeg (MP3, WAV, FLAC, OGG, M4A, etc.). YouTube downloads are converted to WAV for processing.
</details>

<details>
<summary><b>How accurate is the BPM/key detection?</b></summary>

Very accurate! We use TuneBat (human-verified database) as the primary source, with Essentia as a fallback. Most detections are within ±3 BPM and handle enharmonic equivalents for keys.
</details>

<details>
<summary><b>Can I process local audio files?</b></summary>

Yes! Use `stems-split` to process any local audio file. You don't need YouTube for stem separation.
</details>

<details>
<summary><b>Does this work offline?</b></summary>

Partially. Stem separation and local audio analysis work offline. YouTube downloads and TuneBat scraping require internet.
</details>

<details>
<summary><b>Is GPU acceleration supported?</b></summary>

Yes! Demucs automatically uses GPU if available (CUDA), which significantly speeds up stem separation.
</details>

---

## 🌟 Star History

If you find this project useful, please consider giving it a star on GitHub! ⭐

---

**Made with ❤️ for music producers and audio enthusiasts**

[⬆ Back to top](#stems---audio-processing-toolkit)
