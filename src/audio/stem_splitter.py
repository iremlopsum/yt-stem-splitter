"""Audio stem separation using Demucs."""

import os
import shutil
from typing import Tuple
from ..utils.subprocess_utils import run_command


def split_audio_stems(
    input_path: str,
    output_dir: str = None,
    two_stems: bool = True,
    stem_type: str = "vocals"
) -> Tuple[str, str]:
    """
    Split audio file into stems using Demucs.
    
    Args:
        input_path: Path to input audio file
        output_dir: Directory for output files (defaults to current directory)
        two_stems: If True, split into two stems (target + rest)
        stem_type: Type of stem to isolate when two_stems=True (default: "vocals")
        
    Returns:
        Tuple of (vocals_output_path, instrumental_output_path)
        
    Raises:
        subprocess.CalledProcessError: If Demucs command fails
        FileNotFoundError: If expected output files are not created
    """
    basename = os.path.splitext(os.path.basename(input_path))[0]
    
    if output_dir is None:
        output_dir = os.path.join(os.getcwd(), "demucs_output")
    
    # Clean up old output directory
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    
    # Build Demucs command
    cmd = ["demucs"]
    if two_stems:
        cmd.extend(["--two-stems", stem_type])
    cmd.extend(["-o", output_dir, input_path])
    
    # Run Demucs
    run_command(cmd)
    
    # Locate output files
    stem_folder = os.path.join(output_dir, "htdemucs", basename)
    vocals_path = os.path.join(stem_folder, "vocals.wav")
    instrumental_path = os.path.join(stem_folder, "no_vocals.wav")
    
    if not os.path.exists(vocals_path):
        raise FileNotFoundError(f"Expected vocals file not found: {vocals_path}")
    if not os.path.exists(instrumental_path):
        raise FileNotFoundError(f"Expected instrumental file not found: {instrumental_path}")
    
    # Copy results to current directory with descriptive names
    out_vocals = f"{basename}_vocals.wav"
    out_instrumental = f"{basename}_instrumental.wav"
    
    shutil.copyfile(vocals_path, out_vocals)
    shutil.copyfile(instrumental_path, out_instrumental)
    
    print(f"Vocals saved to {out_vocals}")
    print(f"Instrumental saved to {out_instrumental}")
    
    return out_vocals, out_instrumental

