"""File and dependency management utilities."""

import sys
from .subprocess_utils import run_command_capture


def ensure_dependency(dep: str) -> None:
    """
    Check if a system dependency is available in PATH.
    
    Args:
        dep: Name of the dependency (e.g., 'yt-dlp', 'ffmpeg')
        
    Raises:
        SystemExit: If dependency is not found
    """
    try:
        run_command_capture([dep, "--version"])
    except Exception:
        print(f"Error: required dependency '{dep}' not found in PATH.")
        sys.exit(1)

