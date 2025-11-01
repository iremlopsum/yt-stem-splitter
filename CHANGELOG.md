# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed
- TuneBat scraper now uses standard Selenium instead of undetected-chromedriver
- Updated CSS selectors to match current TuneBat page structure (div.yIPfN containers)
- Added Cloudflare bot detection bypass with custom user-agent and headless mode
- Improved page load wait times for reliable scraping

### Added
- Initial release of Stems audio processing toolkit
- YouTube audio download functionality using yt-dlp
- BPM and key detection using Essentia
- Audio stem separation using Demucs
- TuneBat web scraping for accurate metadata
- Comprehensive test suite (55 tests: 39 unit, 16 integration)
- Integration tests for real YouTube URLs
- Modular package structure following best practices
- Type hints throughout codebase
- CLI and library usage modes
- Flexible BPM/key matching with tolerance
- Enharmonic equivalent support for key detection
- Progress bars for download, metadata detection, and stem splitting
- Auto-generated markdown summary files
- Google search integration for manual verification
- Finder/Explorer integration for easy file access
- Organized output directory structure
- Entry point commands: `stems-yt` and `stems-split`

### Documentation
- Complete README with quick start guide and updated features
- Testing documentation (TESTING.md) with accurate test counts
- Architecture documentation (ARCHITECTURE.md)
- Contributing guidelines (CONTRIBUTING.md)
- Open source readiness checklist (OPEN_SOURCE_CHECKLIST.md)
- Comprehensive docstrings on all public functions
- Test runner scripts with clear output

## [0.1.0] - 2025-01-01

### Added
- Initial project structure
- YouTube download functionality with yt-dlp
- Stem splitting with Demucs (vocals + instrumental)
- Audio analysis capabilities with Essentia
- TuneBat scraping for metadata
- Command-line interfaces with progress tracking
- Comprehensive test suite
- Full documentation

---

## Future Versions

### Planned for 0.2.0
- [ ] Support for 4-stem separation (drums, bass, vocals, other)
- [ ] Playlist batch processing
- [ ] Improved error handling and logging
- [ ] Performance optimizations
- [ ] Configuration file support
- [ ] Custom output directory specification

### Planned for 0.3.0
- [ ] GUI interface
- [ ] Docker container
- [ ] Additional metadata sources
- [ ] Enhanced audio analysis features

### Planned for 1.0.0
- [ ] Stable public API
- [ ] Complete documentation
- [ ] Full test coverage
- [ ] Production-ready release

---

## Version History

### [0.1.0] - 2025-01-01
- Initial release

