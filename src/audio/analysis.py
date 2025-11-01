"""Audio analysis using Essentia library."""

from typing import Optional, Tuple, List

# Check if Essentia is available
try:
    import essentia.standard as es
    ESSENTIA_AVAILABLE = True
except ImportError:
    ESSENTIA_AVAILABLE = False


def is_essentia_available() -> bool:
    """Check if Essentia library is available."""
    return ESSENTIA_AVAILABLE


def analyze_audio_bpm_key(
    wav_path: str,
    sample_rate: int = 44100
) -> Tuple[Optional[str], Optional[str], List[str]]:
    """
    Analyze audio file to detect BPM and key using Essentia.
    
    Args:
        wav_path: Path to WAV file
        sample_rate: Sample rate for analysis (default: 44100)
        
    Returns:
        Tuple of (bpm, key, sources) where:
        - bpm: Detected BPM as string (e.g., "128") or None
        - key: Detected key (e.g., "A Major") or None
        - sources: List of detection methods used
        
    Raises:
        ImportError: If Essentia is not installed
    """
    if not ESSENTIA_AVAILABLE:
        return None, None, []
    
    try:
        print("Analyzing audio file for BPM and key...")
        
        # Load audio file
        loader = es.MonoLoader(filename=wav_path, sampleRate=sample_rate)
        audio = loader()
        
        # Detect BPM using RhythmExtractor2013
        rhythm_extractor = es.RhythmExtractor2013(method="multifeature")
        bpm, beats, beats_confidence, _, beats_intervals = rhythm_extractor(audio)
        bpm_str = str(int(round(bpm)))
        
        # Detect key using KeyExtractor
        key_extractor = es.KeyExtractor()
        key, scale, strength = key_extractor(audio)
        
        # Essentia returns key like "A" and scale like "major" or "minor"
        # Format as "A Major" or "A Minor"
        detected_key = f"{key} {scale.capitalize()}"
        
        return bpm_str, detected_key, ["Audio analysis (Essentia)"]
    
    except Exception as e:
        print(f"Audio analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return None, None, []

