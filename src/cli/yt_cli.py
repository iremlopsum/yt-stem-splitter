#!/usr/bin/env python3
"""CLI for downloading YouTube audio and extracting track information."""

import os
import sys
import warnings
from datetime import datetime
from urllib.parse import quote_plus
from tqdm import tqdm

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

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


def detect_track_metadata(title: str, wav_path: str, progress_bar: tqdm = None) -> tuple:
    """
    Detect BPM, key, and Camelot information for a track.
    
    Returns:
        Tuple of (bpm, key, camelot, sources)
    """
    bpm, key, sources = None, None, []
    camelot = None
    
    # Try TuneBat first (most accurate)
    if is_tunebat_available():
        if progress_bar:
            progress_bar.set_description("🎹 Searching TuneBat...")
            progress_bar.update(10)
        tunebat_bpm, tunebat_key, tunebat_camelot = scrape_tunebat_info(title, silent=True)
        if tunebat_bpm:
            bpm = tunebat_bpm
            sources.append("TuneBat")
        if tunebat_key:
            key = tunebat_key
            if "TuneBat" not in sources:
                sources.append("TuneBat")
        if tunebat_camelot:
            camelot = tunebat_camelot
        if progress_bar:
            progress_bar.update(40)
    else:
        if progress_bar:
            progress_bar.update(50)
    
    # Try Essentia audio analysis as fallback or validation
    if is_essentia_available() and (not bpm or not key):
        if progress_bar:
            progress_bar.set_description("🎵 Analyzing audio...")
            progress_bar.update(10)
        essentia_bpm, essentia_key, essentia_sources = analyze_audio_bpm_key(wav_path)
        if essentia_bpm and not bpm:
            bpm = essentia_bpm
        if essentia_key and not key:
            key = essentia_key
        if essentia_sources:
            sources.extend(essentia_sources)
        if progress_bar:
            progress_bar.update(30)
    else:
        if progress_bar:
            progress_bar.update(40)
    
    # Open web browser with Google search for manual verification
    if progress_bar:
        progress_bar.set_description("🔍 Opening browser...")
    search_query = f"{title} bpm key"
    google_search_url = f"https://www.google.com/search?q={quote_plus(search_query)}"
    try:
        run_command(["open", google_search_url])
    except Exception:
        pass
    
    if progress_bar:
        progress_bar.update(10)
    
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

    # Get project root (two levels up from src/cli/)
    script_dir = os.path.dirname(os.path.realpath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    
    # Get title (silent operation)
    try:
        title = get_youtube_title(url)
    except Exception as e:
        print(f"Failed to fetch video title: {e}")
        sys.exit(1)

    safe_title = sanitize_filename(title)
    output_base = os.path.join(project_root, "output")
    target_dir = os.path.join(output_base, safe_title)
    
    # Create output directory if it doesn't exist
    os.makedirs(output_base, exist_ok=True)
    
    print(f"\n🎵 Processing: {title}\n")

    # Create three progress bars
    with tqdm(total=100, desc="📥 Downloading", position=0, leave=True, 
              bar_format='{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt}') as download_bar, \
         tqdm(total=100, desc="🎹 Getting key/BPM", position=1, leave=True,
              bar_format='{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt}') as metadata_bar, \
         tqdm(total=100, desc="✂️  Splitting stems", position=2, leave=True,
              bar_format='{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt}') as stems_bar:
        
        # Download WAV into target_dir
        try:
            wav_path = download_youtube_audio(url, target_dir, audio_format="wav", progress_bar=download_bar)
            download_bar.update(100 - download_bar.n)
            download_bar.set_description("📥 Download complete")
        except Exception as e:
            download_bar.set_description(f"📥 Download failed")
            download_bar.close()
            metadata_bar.close()
            stems_bar.close()
            print(f"\nFailed to download audio: {e}")
            sys.exit(1)

        # Find BPM/Key via audio analysis and/or manual input
        if manual_bpm or manual_key:
            bpm, key, sources = manual_bpm, manual_key, ["Manually specified"]
            camelot = None
            metadata_bar.update(100)
            metadata_bar.set_description("🎹 Using manual BPM/Key")
        else:
            bpm, key, camelot, sources = detect_track_metadata(title, wav_path, metadata_bar)
            metadata_bar.update(100 - metadata_bar.n)
            metadata_bar.set_description("🎹 Metadata complete")

        # Split stems (run split_stems.py with CWD=target_dir so outputs land next to wav)
        split_script = os.path.join(project_root, "split_stems.py")
        if not os.path.isfile(split_script):
            stems_bar.update(100)
            stems_bar.set_description("✂️  Stem split skipped")
        else:
            try:
                from ..audio.stem_splitter import split_audio_stems
                stems_bar.set_description("✂️  Running Demucs...")
                stems_bar.update(10)
                
                # Call stem splitter directly with progress bar
                input_file = os.path.join(target_dir, os.path.basename(wav_path))
                output_dir = os.path.join(target_dir, "demucs_output")
                
                import shutil
                basename = os.path.splitext(os.path.basename(input_file))[0]
                
                # Clean up old output directory
                if os.path.exists(output_dir):
                    shutil.rmtree(output_dir)
                os.makedirs(output_dir)
                
                stems_bar.update(10)
                
                # Run Demucs with quiet flag
                from ..utils.subprocess_utils import run_command
                cmd = ["demucs", "--two-stems", "vocals", "-o", output_dir, input_file]
                
                # Suppress output by redirecting to devnull
                import subprocess
                stems_bar.update(10)
                stems_bar.set_description("✂️  Separating audio...")
                subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
                stems_bar.update(50)
                
                # Locate and copy output files
                stem_folder = os.path.join(output_dir, "htdemucs", basename)
                vocals_path = os.path.join(stem_folder, "vocals.wav")
                instrumental_path = os.path.join(stem_folder, "no_vocals.wav")
                
                out_vocals = os.path.join(target_dir, f"{basename}_vocals.wav")
                out_instrumental = os.path.join(target_dir, f"{basename}_instrumental.wav")
                
                shutil.copyfile(vocals_path, out_vocals)
                shutil.copyfile(instrumental_path, out_instrumental)
                stems_bar.update(20)
                stems_bar.set_description("✂️  Stems complete")
                
            except Exception as e:
                stems_bar.set_description(f"✂️  Stem split failed")

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

