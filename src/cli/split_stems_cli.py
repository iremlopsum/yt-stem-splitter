#!/usr/bin/env python3
"""CLI for splitting audio stems using Demucs."""

import sys
import os
from ..audio.stem_splitter import split_audio_stems


def main():
    """Main entry point for split_stems CLI."""
    if len(sys.argv) != 2:
        print("Usage: python split_stems.py path/to/audiofile.wav")
        sys.exit(1)

    audio_path = sys.argv[1]

    if not os.path.isfile(audio_path):
        print(f"File not found: {audio_path}")
        sys.exit(1)

    try:
        split_audio_stems(audio_path)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

