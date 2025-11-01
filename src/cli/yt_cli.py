#!/usr/bin/env python3
"""CLI for downloading YouTube audio and extracting track information."""

import os
import sys
from datetime import datetime
from urllib.parse import quote_plus

from ..utils.file_utils import ensure_dependency
from ..utils.sanitization import sanitize_filename
from ..utils.subprocess_utils import run_command
from ..downloader.youtube import download_youtube_audio, get_youtube_title
from ..audio.analysis import analyze_audio_bpm_key, is_essentia_available
from ..scrapers.tunebat import scrape_tunebat_info, is_tunebat_available


def write_track_info_markdown(
    md_path: str,
    title: str,
    url: str,
    wav_basename: str,
    bpm: str,
    key: str,
    camelot: str,
    sources: list
) -> None:
    """Write track information to a markdown file."""
    now = datetime.now().isoformat(timespec="seconds")
    
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write(f"- URL: {url}\n")
        f.write(f"- Downloaded WAV: {wav_basename}\n")
        f.write(f"- Detected BPM: {bpm if bpm else 'Unknown'}\n")
        f.write(f"- Detected Key: {key if key else 'Unknown'}\n")
        if camelot:
            f.write(f"- Camelot: {camelot}\n")
        if sources:
            f.write("- Detection Method:\n")
            for s in sources:
                f.write(f"  - {s}\n")
        # Helpful search link
        search_q = quote_plus(f'{title} bpm key')
        f.write(f"\n- Verify at: https://www.google.com/search?q={search_q}\n")
        f.write(f"\n_Generated: {now}_\n")


def print_track_summary(title: str, bpm: str, key: str, camelot: str, sources: list, target_dir: str) -> None:
    """Print a formatted summary of track information."""
    print("\n" + "="*60)
    print("🎵  TRACK INFORMATION")
    print("="*60)
    print(f"Song:     {title}")
    print(f"BPM:      {bpm if bpm else 'Unknown'}")
    print(f"Key:      {key if key else 'Unknown'}")
    if camelot:
        print(f"Camelot:  {camelot}")
    if sources:
        print(f"Source:   {', '.join(sources)}")
    print("="*60)
    print(f"\n✓ Done! Files saved to:\n  {target_dir}\n")


def detect_track_metadata(title: str, wav_path: str) -> tuple:
    """
    Detect BPM, key, and Camelot information for a track.
    
    Returns:
        Tuple of (bpm, key, camelot, sources)
    """
    bpm, key, sources = None, None, []
    camelot = None
    
    # Try TuneBat first (most accurate)
    if is_tunebat_available():
        print("\n🎹 Searching TuneBat database...")
        tunebat_bpm, tunebat_key, tunebat_camelot = scrape_tunebat_info(title)
        if tunebat_bpm:
            bpm = tunebat_bpm
            sources.append("TuneBat")
        if tunebat_key:
            key = tunebat_key
            if "TuneBat" not in sources:
                sources.append("TuneBat")
        if tunebat_camelot:
            camelot = tunebat_camelot
    else:
        print("\n⚠️  TuneBat scraping not available")
        print("   Install with: pip install undetected-chromedriver selenium")
    
    # Try Essentia audio analysis as fallback or validation
    if is_essentia_available() and (not bpm or not key):
        print("\n🎵 Analyzing audio file for BPM/Key...")
        essentia_bpm, essentia_key, essentia_sources = analyze_audio_bpm_key(wav_path)
        if essentia_bpm and not bpm:
            bpm = essentia_bpm
        if essentia_key and not key:
            key = essentia_key
        if essentia_sources:
            sources.extend(essentia_sources)
    elif not is_essentia_available() and (not bpm or not key):
        print("\n⚠️  Essentia not available for audio analysis")
        print("   Install with: pip install essentia")
    
    # Open web browser with Google search for manual verification
    search_query = f"{title} bpm key"
    google_search_url = f"https://www.google.com/search?q={quote_plus(search_query)}"
    print(f"\n🔍 Opening browser to verify BPM/Key...")
    print(f"   Search: {search_query}")
    try:
        run_command(["open", google_search_url])
    except Exception as e:
        print(f"   Could not open browser: {e}")
    
    return bpm, key, camelot, sources


def main():
    """Main entry point for yt CLI."""
    if len(sys.argv) < 2 or len(sys.argv) > 4:
        print("Usage: yt <youtube_url> [bpm] [key]")
        print("Example: yt 'https://youtube.com/...' 99 'G Major'")
        sys.exit(1)

    url = sys.argv[1]
    manual_bpm = sys.argv[2] if len(sys.argv) >= 3 else None
    manual_key = sys.argv[3] if len(sys.argv) >= 4 else None

    # Ensure dependencies
    ensure_dependency("yt-dlp")

    script_dir = os.path.dirname(os.path.realpath(__file__))

    # Get title
    try:
        title = get_youtube_title(url)
    except Exception as e:
        print(f"Failed to fetch video title: {e}")
        sys.exit(1)

    safe_title = sanitize_filename(title)
    target_dir = os.path.join(script_dir, safe_title)

    # Download WAV into target_dir
    print(f"Downloading audio to '{target_dir}'...")
    try:
        wav_path = download_youtube_audio(url, target_dir, audio_format="wav")
    except Exception as e:
        print(f"Failed to download audio: {e}")
        sys.exit(1)

    # Split stems (run split_stems.py with CWD=target_dir so outputs land next to wav)
    # Look for split_stems.py in project root (two levels up from src/cli/)
    project_root = os.path.dirname(os.path.dirname(script_dir))
    split_script = os.path.join(project_root, "split_stems.py")
    if not os.path.isfile(split_script):
        print(f"Warning: '{split_script}' not found. Skipping stem split.")
    else:
        print("Splitting stems...")
        try:
            run_command(
                [sys.executable, split_script, os.path.basename(wav_path)],
                cwd=target_dir
            )
        except Exception as e:
            print(f"split_stems.py failed: {e}")

    # Find BPM/Key via audio analysis and/or manual input
    if manual_bpm or manual_key:
        print(f"Using manually provided BPM/Key: {manual_bpm or 'Unknown'} BPM, {manual_key or 'Unknown'}")
        bpm, key, sources = manual_bpm, manual_key, ["Manually specified"]
        camelot = None
    else:
        bpm, key, camelot, sources = detect_track_metadata(title, wav_path)

    # Write markdown summary
    md_path = os.path.join(target_dir, f"{safe_title}.md")
    write_track_info_markdown(
        md_path, title, url, os.path.basename(wav_path),
        bpm, key, camelot, sources
    )

    # Pretty print summary
    print_track_summary(title, bpm, key, camelot, sources, target_dir)
    
    # Open Finder at location
    try:
        run_command(["open", target_dir])
    except Exception:
        pass


if __name__ == "__main__":
    main()

