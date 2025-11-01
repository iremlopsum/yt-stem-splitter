"""Subprocess execution utilities."""

import subprocess
from typing import Optional, List


def run_command(cmd: List[str], cwd: Optional[str] = None) -> subprocess.CompletedProcess:
    """
    Run a command and check for errors.
    
    Args:
        cmd: Command and arguments as a list
        cwd: Working directory (optional)
        
    Returns:
        CompletedProcess instance
        
    Raises:
        subprocess.CalledProcessError: If command fails
    """
    return subprocess.run(cmd, cwd=cwd, check=True)


def run_command_capture(cmd: List[str]) -> subprocess.CompletedProcess:
    """
    Run a command and capture output.
    
    Args:
        cmd: Command and arguments as a list
        
    Returns:
        CompletedProcess instance with stdout and stderr captured
        
    Raises:
        subprocess.CalledProcessError: If command fails
    """
    return subprocess.run(
        cmd,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

