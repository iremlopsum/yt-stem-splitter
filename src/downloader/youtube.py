"""YouTube download functionality using yt-dlp."""

import os
import subprocess
from typing import Optional
from ..utils.subprocess_utils import run_command, run_command_capture


def get_youtube_title(url: str) -> str:
    """
    Get the title of a YouTube video.
    
    Args:
        url: YouTube video URL
        
    Returns:
        Video title as string
        
    Raises:
        subprocess.CalledProcessError: If yt-dlp command fails
    """
    result = run_command_capture([
        "yt-dlp",
        "--no-playlist",
        "--print",
        "%(title)s",
        url
    ])
    return result.stdout.strip()


def download_youtube_audio(
    url: str,
    output_dir: str,
    audio_format: str = "wav",
    progress_bar = None
) -> str:
    """
    Download audio from YouTube video.
    
    Args:
        url: YouTube video URL
        output_dir: Directory to save the audio file
        audio_format: Audio format (default: "wav")
        progress_bar: Optional tqdm progress bar to update
        
    Returns:
        Path to the downloaded audio file
        
    Raises:
        subprocess.CalledProcessError: If download fails
        FileNotFoundError: If downloaded file cannot be located
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    if progress_bar:
        progress_bar.set_description("📥 Extracting URL...")
        progress_bar.update(10)
    
    # Download audio
    # Use Android client to work around YouTube 403 errors
    output_template = os.path.join(output_dir, "%(title)s.%(ext)s")
    
    if progress_bar:
        progress_bar.set_description("📥 Downloading audio...")
        progress_bar.update(10)
    
    # Suppress yt-dlp output
    subprocess.run([
        "yt-dlp",
        "--no-playlist",
        "--extract-audio",
        "--audio-format", audio_format,
        "--extractor-args", "youtube:player_client=android",
        "-o", output_template,
        "--quiet",
        "--no-warnings",
        url
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    if progress_bar:
        progress_bar.update(60)
        progress_bar.set_description("📥 Converting to WAV...")
    
    # Locate the downloaded file
    audio_files = [
        f for f in os.listdir(output_dir)
        if f.lower().endswith(f".{audio_format}")
    ]
    
    if not audio_files:
        raise FileNotFoundError(
            f"No {audio_format.upper()} file found after download in {output_dir}"
        )
    
    # Return the most recently modified file (in case multiple exist)
    audio_files.sort(
        key=lambda f: os.path.getmtime(os.path.join(output_dir, f)),
        reverse=True
    )
    
    if progress_bar:
        progress_bar.update(20)
    
    return os.path.join(output_dir, audio_files[0])

