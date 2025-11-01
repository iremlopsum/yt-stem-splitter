# Architecture Overview

## Module Dependency Graph

```
┌─────────────────────────────────────────────────────────────────┐
│                       CLI Layer (Entry Points)                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  yt (script)                    split_stems.py (script)         │
│      │                                  │                       │
│      └──────┐                          ┌┘                       │
│             ▼                          ▼                        │
│    src/cli/yt_cli.py          src/cli/split_stems_cli.py       │
│             │                          │                        │
└─────────────┼──────────────────────────┼─────────────────────────┘
              │                          │
              │                          │
┌─────────────┴──────────────────────────┴─────────────────────────┐
│                     Business Logic Layer                         │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────┐  ┌────────────────┐  ┌─────────────────┐   │
│  │ src/downloader │  │   src/audio    │  │  src/scrapers   │   │
│  ├────────────────┤  ├────────────────┤  ├─────────────────┤   │
│  │  youtube.py    │  │  analysis.py   │  │   tunebat.py    │   │
│  │                │  │stem_splitter.py│  │                 │   │
│  └────────┬───────┘  └────────┬───────┘  └────────┬────────┘   │
│           │                   │                    │            │
│           └───────────────────┴────────────────────┘            │
│                               │                                 │
└───────────────────────────────┼─────────────────────────────────┘
                                │
                                │
┌───────────────────────────────┴─────────────────────────────────┐
│                      Utility Layer                               │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  src/utils/                                                      │
│  ├── subprocess_utils.py   (subprocess wrappers)                 │
│  ├── sanitization.py       (string cleaning)                     │
│  └── file_utils.py         (dependency checking)                 │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
                                │
                                │
┌───────────────────────────────┴─────────────────────────────────┐
│                    External Dependencies                         │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  • yt-dlp (YouTube downloads)                                    │
│  • demucs (stem separation)                                      │
│  • essentia (audio analysis)                                     │
│  • selenium + undetected-chromedriver (web scraping)             │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## Layer Descriptions

### 1. CLI Layer (Top)

**Purpose:** User interface and orchestration

**Components:**

- `yt` - Executable script for YouTube downloads
- `split_stems.py` - Executable script for stem splitting
- `src/cli/yt_cli.py` - YouTube CLI implementation
- `src/cli/split_stems_cli.py` - Stem splitting CLI implementation

**Characteristics:**

- Thin wrappers that orchestrate other modules
- Handle command-line argument parsing
- Coordinate workflow between modules
- Print user-friendly messages

**Testing:** Integration tests or manual testing (CLI is tested through underlying modules)

---

### 2. Business Logic Layer (Middle)

**Purpose:** Core functionality and domain logic

**Components:**

#### `src/downloader/`

- `youtube.py` - YouTube video/audio downloading
  - `get_youtube_title()` - Fetch video title
  - `download_youtube_audio()` - Download audio file

#### `src/audio/`

- `analysis.py` - Audio analysis with Essentia
  - `analyze_audio_bpm_key()` - Detect BPM and key
  - `is_essentia_available()` - Check library availability
- `stem_splitter.py` - Stem separation with Demucs
  - `split_audio_stems()` - Split audio into stems

#### `src/scrapers/`

- `tunebat.py` - Web scraping for music metadata
  - `scrape_tunebat_info()` - Scrape BPM/key from TuneBat
  - `is_tunebat_available()` - Check dependencies

**Characteristics:**

- Pure business logic
- Minimal external dependencies within layer
- Uses utility layer for common operations
- Extensively unit tested

**Testing:** Comprehensive unit tests with mocking

---

### 3. Utility Layer (Bottom)

**Purpose:** Shared helper functions used across business logic

**Components:**

#### `src/utils/subprocess_utils.py`

- `run_command()` - Execute subprocess with error checking
- `run_command_capture()` - Execute and capture output

#### `src/utils/sanitization.py`

- `sanitize_filename()` - Clean strings for safe filenames

#### `src/utils/file_utils.py`

- `ensure_dependency()` - Verify system dependencies exist

**Characteristics:**

- Pure functions when possible
- No business logic
- Reusable across modules
- Minimal dependencies

**Testing:** Direct unit tests, easiest to test

---

## Module Interaction Patterns

### Pattern 1: Download Workflow

```python
# yt CLI orchestrates multiple modules
def main():
    # 1. Dependency check (utils)
    ensure_dependency("yt-dlp")

    # 2. Get title (downloader)
    title = get_youtube_title(url)

    # 3. Sanitize (utils)
    safe_title = sanitize_filename(title)

    # 4. Download (downloader)
    wav_path = download_youtube_audio(url, safe_title)

    # 5. Analyze (audio)
    bpm, key, _ = analyze_audio_bpm_key(wav_path)

    # 6. Scrape (scrapers)
    tunebat_bpm, tunebat_key, _ = scrape_tunebat_info(title)
```

### Pattern 2: Stem Splitting Workflow

```python
# split_stems CLI uses audio module
def main():
    # 1. Validate input (cli)
    if not os.path.isfile(audio_path):
        sys.exit(1)

    # 2. Split stems (audio)
    vocals, instrumental = split_audio_stems(audio_path)
```

---

## Dependency Flow

### Imports Flow (Top to Bottom)

```
CLI modules
    ↓ import
Business Logic modules
    ↓ import
Utility modules
    ↓ import
Standard library / External packages
```

**Rule:** Lower layers never import from higher layers

### Example: Correct Dependency Direction

```python
# ✅ GOOD - Higher layer imports lower layer
# src/cli/yt_cli.py
from src.downloader.youtube import download_youtube_audio
from src.utils.sanitization import sanitize_filename

# ✅ GOOD - Same layer imports (no circular dependency)
# src/audio/analysis.py
from ..utils.subprocess_utils import run_command

# ❌ BAD - Lower layer importing higher layer
# src/utils/sanitization.py
from src.cli.yt_cli import main  # NEVER DO THIS!
```

---

## Testing Architecture

### Test Organization

```
tests/
├── test_sanitization.py         → src/utils/sanitization.py
├── test_subprocess_utils.py     → src/utils/subprocess_utils.py
├── test_file_utils.py           → src/utils/file_utils.py
├── test_audio_analysis.py       → src/audio/analysis.py
├── test_stem_splitter.py        → src/audio/stem_splitter.py
├── test_youtube_downloader.py   → src/downloader/youtube.py
└── test_tunebat.py              → src/scrapers/tunebat.py
```

### Test Pyramid

```
      ┌─────────────┐
      │  Manual     │  Few manual CLI tests
      │  Tests      │
      ├─────────────┤
      │ Integration │  Some integration tests
      │   Tests     │  (multiple modules)
      ├─────────────┤
      │    Unit     │  Many unit tests
      │   Tests     │  (individual functions)
      └─────────────┘
```

**Distribution:**

- 70% Unit tests (fast, isolated)
- 25% Integration tests (module interactions)
- 5% Manual tests (full CLI workflow)

---

## Data Flow Example

### YouTube Download Flow

```
User Input
   │
   ├─ URL: "https://youtube.com/..."
   │
   ▼
┌─────────────────┐
│  yt_cli.main()  │
└────────┬────────┘
         │
         ├─ ensure_dependency("yt-dlp")
         │     └─► file_utils.ensure_dependency()
         │
         ├─ get_youtube_title(url)
         │     └─► youtube.get_youtube_title()
         │         └─► subprocess_utils.run_command_capture()
         │             └─► yt-dlp --print "%(title)s"
         │
         ├─ sanitize_filename(title)
         │     └─► sanitization.sanitize_filename()
         │
         ├─ download_youtube_audio(url, dir)
         │     └─► youtube.download_youtube_audio()
         │         └─► subprocess_utils.run_command()
         │             └─► yt-dlp --extract-audio
         │
         ├─ split_audio_stems(wav_path)
         │     └─► stem_splitter.split_audio_stems()
         │         └─► subprocess_utils.run_command()
         │             └─► demucs --two-stems vocals
         │
         ├─ scrape_tunebat_info(title)
         │     └─► tunebat.scrape_tunebat_info()
         │         └─► Selenium WebDriver
         │
         └─ analyze_audio_bpm_key(wav_path)
               └─► analysis.analyze_audio_bpm_key()
                   └─► Essentia library
```

---

## Extension Points

### Adding New Features

#### 1. New Audio Analysis Method

```python
# Add to src/audio/
# Create: src/audio/new_analyzer.py

def analyze_with_new_method(audio_path: str) -> dict:
    """New analysis method."""
    # Implementation
    pass

# Create: tests/test_new_analyzer.py
class TestNewAnalyzer(unittest.TestCase):
    """Tests for new analyzer."""
    pass
```

#### 2. New Scraper

```python
# Add to src/scrapers/
# Create: src/scrapers/new_site.py

def scrape_new_site(query: str) -> tuple:
    """Scrape from new website."""
    # Implementation
    pass

# Create: tests/test_new_site.py
```

#### 3. New Utility Function

```python
# Add to src/utils/
# Create: src/utils/new_util.py

def new_helper_function(input: str) -> str:
    """New utility function."""
    # Implementation
    pass

# Create: tests/test_new_util.py
```

---

## Design Patterns Used

### 1. **Facade Pattern**

CLI modules provide simple interface to complex subsystems:

```python
# Complex subsystem calls hidden behind simple CLI
def main():
    wav_path = download_youtube_audio(url, dir)  # Hides yt-dlp complexity
    bpm, key = analyze_audio_bpm_key(wav_path)   # Hides Essentia complexity
```

### 2. **Adapter Pattern**

Utility functions adapt external tools to consistent interface:

```python
def run_command(cmd: List[str], cwd: Optional[str] = None):
    """Adapts subprocess.run to project's needs."""
    return subprocess.run(cmd, cwd=cwd, check=True)
```

### 3. **Strategy Pattern**

Multiple detection strategies for BPM/key:

```python
# Try multiple strategies
if is_tunebat_available():
    bpm, key = scrape_tunebat_info(title)

if not bpm and is_essentia_available():
    bpm, key = analyze_audio_bpm_key(audio_path)
```

### 4. **Factory Pattern** (implicit)

Functions create and return configured objects:

```python
def download_youtube_audio(url, output_dir, audio_format="wav"):
    """Factory for downloaded audio files."""
    # Configure and execute download
    # Return path to created file
    return audio_path
```

---

## Performance Considerations

### Fast Operations (No Mocking Needed in Tests)

- String sanitization
- Path manipulation
- Data structure operations

### Slow Operations (Always Mock in Tests)

- Network requests (YouTube, TuneBat)
- Subprocess calls (yt-dlp, demucs)
- File I/O (large audio files)
- Audio analysis (Essentia)

### Caching Opportunities

```python
# Future enhancement: cache API responses
@lru_cache(maxsize=128)
def get_youtube_title(url: str) -> str:
    """Cached title fetching."""
    pass
```

---

## Security Considerations

### Input Validation

```python
# Always sanitize user inputs
def sanitize_filename(name: str) -> str:
    """Remove dangerous characters from filenames."""
    name = re.sub(r"[^\w\- ()]", "", name)
    return name or "yt_download"
```

### Subprocess Safety

```python
# Use list form, not shell=True
subprocess.run(["yt-dlp", url], check=True)  # ✅ Safe
subprocess.run(f"yt-dlp {url}", shell=True)  # ❌ Dangerous
```

### Dependency Checking

```python
# Verify dependencies before use
def ensure_dependency(dep: str):
    """Check required tools exist."""
    try:
        run_command_capture([dep, "--version"])
    except Exception:
        sys.exit(1)
```

---

## Conclusion

This architecture provides:

- ✅ Clear separation of concerns
- ✅ Testable components
- ✅ Reusable modules
- ✅ Easy to extend
- ✅ Maintainable codebase
- ✅ Type-safe interfaces
- ✅ Well-documented structure

The layered architecture ensures that:

1. Each layer has a specific responsibility
2. Dependencies flow in one direction (top to bottom)
3. Lower layers are reusable
4. Testing is straightforward with appropriate mocking
5. New features can be added without affecting existing code
