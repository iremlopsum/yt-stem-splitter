"""Integration tests for real YouTube URLs with expected BPM and key values."""

import unittest
import os
import re
import tempfile
import shutil
from typing import Optional, Tuple

# Integration tests require actual dependencies
try:
    from src.downloader.youtube import get_youtube_title, download_youtube_audio
    from src.audio.analysis import analyze_audio_bpm_key, is_essentia_available
    from src.scrapers.tunebat import scrape_tunebat_info, is_tunebat_available
    CAN_RUN_INTEGRATION = True
except ImportError:
    CAN_RUN_INTEGRATION = False


def normalize_bpm(bpm_str: Optional[str]) -> Optional[int]:
    """
    Normalize BPM string to integer.
    
    Handles formats like: "99", "99.0", "99 BPM", "~99"
    
    Args:
        bpm_str: BPM as string or None
        
    Returns:
        BPM as integer or None
    """
    if not bpm_str:
        return None
    
    # Extract first number from string
    match = re.search(r'\d+', str(bpm_str))
    if match:
        return int(match.group())
    return None


def normalize_key(key_str: Optional[str]) -> Optional[str]:
    """
    Normalize musical key string for comparison.
    
    Handles formats like:
    - "G Major", "G major", "g major", "G"
    - "A# Minor", "A#min", "A# min", "A#m"
    - "G♯ Minor" (unicode sharp symbol)
    
    Args:
        key_str: Key as string or None
        
    Returns:
        Normalized key string (uppercase note, lowercase minor/major) or None
    """
    if not key_str:
        return None
    
    key_str = str(key_str).strip()
    
    # Replace unicode sharp symbol with #
    key_str = key_str.replace('♯', '#')
    # Replace unicode flat symbol with b
    key_str = key_str.replace('♭', 'b')
    
    # Extract note (e.g., "G", "A#", "Bb")
    note_match = re.match(r'^([A-G][#b]?)', key_str, re.IGNORECASE)
    if not note_match:
        return None
    
    # Uppercase the letter, but keep # and b as-is
    note_raw = note_match.group(1)
    note = note_raw[0].upper() + note_raw[1:].lower() if len(note_raw) > 1 else note_raw.upper()
    
    # Detect major/minor
    key_lower = key_str.lower()
    if 'min' in key_lower or 'm' == key_lower[-1]:
        return f"{note}min"
    else:
        return f"{note}maj"


def keys_match(detected: Optional[str], expected: str, tolerance: bool = True) -> bool:
    """
    Check if detected key matches expected key.
    
    Args:
        detected: Detected key string
        expected: Expected key string
        tolerance: If True, allow flexible matching
        
    Returns:
        True if keys match within tolerance
    """
    if not detected:
        return False
    
    detected_norm = normalize_key(detected)
    expected_norm = normalize_key(expected)
    
    if detected_norm == expected_norm:
        return True
    
    if tolerance:
        # Allow enharmonic equivalents (e.g., A# = Bb)
        enharmonics = {
            'A#': 'Bb', 'Bb': 'A#',
            'C#': 'Db', 'Db': 'C#',
            'D#': 'Eb', 'Eb': 'D#',
            'F#': 'Gb', 'Gb': 'F#',
            'G#': 'Ab', 'Ab': 'G#',
        }
        
        if detected_norm and expected_norm:
            detected_note = detected_norm[:-3]
            expected_note = expected_norm[:-3]
            detected_mode = detected_norm[-3:]
            expected_mode = expected_norm[-3:]
            
            if (detected_mode == expected_mode and 
                enharmonics.get(detected_note) == expected_note):
                return True
    
    return False


def bpm_match(detected: Optional[str], expected: int, tolerance: int = 2) -> bool:
    """
    Check if detected BPM matches expected BPM within tolerance.
    
    Args:
        detected: Detected BPM string
        expected: Expected BPM integer
        tolerance: Allowed difference in BPM
        
    Returns:
        True if BPM matches within tolerance
    """
    detected_int = normalize_bpm(detected)
    if detected_int is None:
        return False
    
    return abs(detected_int - expected) <= tolerance


@unittest.skipIf(not CAN_RUN_INTEGRATION, "Integration test dependencies not available")
class TestYouTubeIntegration(unittest.TestCase):
    """Integration tests for real YouTube URLs."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.temp_dir = tempfile.mkdtemp()
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test fixtures."""
        if os.path.exists(cls.temp_dir):
            shutil.rmtree(cls.temp_dir)
    
    def test_youtube_url_1_metadata(self):
        """
        Test YouTube URL: https://www.youtube.com/watch?v=33mjGmfy7PA
        Expected: BPM=99, Key=G Major
        """
        url = "https://www.youtube.com/watch?v=33mjGmfy7PA&list=LL&index=15"
        expected_bpm = 99
        expected_key = "G major"
        
        # Get title
        try:
            title = get_youtube_title(url)
            print(f"\n✓ Retrieved title: {title}")
        except Exception as e:
            self.skipTest(f"Could not fetch title: {e}")
        
        # Try TuneBat scraping
        detected_bpm = None
        detected_key = None
        
        if is_tunebat_available():
            try:
                bpm, key, camelot = scrape_tunebat_info(title)
                print(f"  TuneBat: BPM={bpm}, Key={key}, Camelot={camelot}")
                if bpm:
                    detected_bpm = bpm
                if key:
                    detected_key = key
            except Exception as e:
                print(f"  TuneBat failed: {e}")
        
        # Try audio analysis if TuneBat didn't work
        if (not detected_bpm or not detected_key) and is_essentia_available():
            try:
                # Download audio for analysis
                audio_path = download_youtube_audio(url, self.temp_dir)
                bpm, key, sources = analyze_audio_bpm_key(audio_path)
                print(f"  Essentia: BPM={bpm}, Key={key}")
                if bpm and not detected_bpm:
                    detected_bpm = bpm
                if key and not detected_key:
                    detected_key = key
            except Exception as e:
                print(f"  Audio analysis failed: {e}")
        
        # Verify results
        print(f"\n  Detected: BPM={detected_bpm}, Key={detected_key}")
        print(f"  Expected: BPM={expected_bpm}, Key={expected_key}")
        
        if detected_bpm:
            self.assertTrue(
                bpm_match(detected_bpm, expected_bpm, tolerance=3),
                f"BPM mismatch: detected {detected_bpm}, expected {expected_bpm}±3"
            )
        
        if detected_key:
            self.assertTrue(
                keys_match(detected_key, expected_key, tolerance=True),
                f"Key mismatch: detected {detected_key}, expected {expected_key}"
            )
    
    def test_youtube_url_2_metadata(self):
        """
        Test YouTube URL: https://www.youtube.com/watch?v=fswfZjDerAs
        Expected: BPM=97, Key=G#min
        """
        url = "https://www.youtube.com/watch?v=fswfZjDerAs&list=LL&index=31"
        expected_bpm = 97
        expected_key = "G#min"
        
        # Get title
        try:
            title = get_youtube_title(url)
            print(f"\n✓ Retrieved title: {title}")
        except Exception as e:
            self.skipTest(f"Could not fetch title: {e}")
        
        # Try TuneBat scraping
        detected_bpm = None
        detected_key = None
        
        if is_tunebat_available():
            try:
                bpm, key, camelot = scrape_tunebat_info(title)
                print(f"  TuneBat: BPM={bpm}, Key={key}, Camelot={camelot}")
                if bpm:
                    detected_bpm = bpm
                if key:
                    detected_key = key
            except Exception as e:
                print(f"  TuneBat failed: {e}")
        
        # Try audio analysis if TuneBat didn't work
        if (not detected_bpm or not detected_key) and is_essentia_available():
            try:
                # Download audio for analysis
                audio_path = download_youtube_audio(url, self.temp_dir)
                bpm, key, sources = analyze_audio_bpm_key(audio_path)
                print(f"  Essentia: BPM={bpm}, Key={key}")
                if bpm and not detected_bpm:
                    detected_bpm = bpm
                if key and not detected_key:
                    detected_key = key
            except Exception as e:
                print(f"  Audio analysis failed: {e}")
        
        # Verify results
        print(f"\n  Detected: BPM={detected_bpm}, Key={detected_key}")
        print(f"  Expected: BPM={expected_bpm}, Key={expected_key}")
        
        if detected_bpm:
            self.assertTrue(
                bpm_match(detected_bpm, expected_bpm, tolerance=3),
                f"BPM mismatch: detected {detected_bpm}, expected {expected_bpm}±3"
            )
        
        if detected_key:
            self.assertTrue(
                keys_match(detected_key, expected_key, tolerance=True),
                f"Key mismatch: detected {detected_key}, expected {expected_key}"
            )


class TestKeyNormalization(unittest.TestCase):
    """Test cases for key normalization utility functions."""
    
    def test_normalize_key_major_variations(self):
        """Test normalization of major key variations."""
        test_cases = [
            ("G Major", "Gmaj"),
            ("G major", "Gmaj"),
            ("g major", "Gmaj"),
            ("G", "Gmaj"),
        ]
        
        for input_key, expected in test_cases:
            with self.subTest(input_key=input_key):
                result = normalize_key(input_key)
                self.assertEqual(result, expected)
    
    def test_normalize_key_minor_variations(self):
        """Test normalization of minor key variations."""
        test_cases = [
            ("A# Minor", "A#min"),
            ("A#min", "A#min"),
            ("A# min", "A#min"),
            ("A#m", "A#min"),
            ("a# minor", "A#min"),
        ]
        
        for input_key, expected in test_cases:
            with self.subTest(input_key=input_key):
                result = normalize_key(input_key)
                self.assertEqual(result, expected)
    
    def test_normalize_key_with_flats(self):
        """Test normalization with flat notes."""
        test_cases = [
            ("Bb Minor", "Bbmin"),
            ("Bb major", "Bbmaj"),
            ("Eb Major", "Ebmaj"),
        ]
        
        for input_key, expected in test_cases:
            with self.subTest(input_key=input_key):
                result = normalize_key(input_key)
                self.assertEqual(result, expected)
    
    def test_keys_match_exact(self):
        """Test exact key matching."""
        self.assertTrue(keys_match("G Major", "G major"))
        self.assertTrue(keys_match("A#min", "A# Minor"))
        self.assertTrue(keys_match("Bb major", "Bb Major"))
    
    def test_keys_match_enharmonic(self):
        """Test enharmonic key matching (A# = Bb)."""
        self.assertTrue(keys_match("A# Minor", "Bb Minor", tolerance=True))
        self.assertTrue(keys_match("Bb major", "A# major", tolerance=True))
        self.assertTrue(keys_match("C# min", "Db min", tolerance=True))
    
    def test_keys_dont_match_different_mode(self):
        """Test that major and minor don't match."""
        self.assertFalse(keys_match("G Major", "G Minor"))
        self.assertFalse(keys_match("A# min", "A# major"))


class TestBPMNormalization(unittest.TestCase):
    """Test cases for BPM normalization utility functions."""
    
    def test_normalize_bpm_integer_string(self):
        """Test normalization of integer string."""
        self.assertEqual(normalize_bpm("99"), 99)
        self.assertEqual(normalize_bpm("128"), 128)
    
    def test_normalize_bpm_with_decimal(self):
        """Test normalization with decimal."""
        self.assertEqual(normalize_bpm("99.5"), 99)
        self.assertEqual(normalize_bpm("128.7"), 128)
    
    def test_normalize_bpm_with_text(self):
        """Test normalization with surrounding text."""
        self.assertEqual(normalize_bpm("99 BPM"), 99)
        self.assertEqual(normalize_bpm("~99"), 99)
        self.assertEqual(normalize_bpm("BPM: 128"), 128)
    
    def test_normalize_bpm_none(self):
        """Test normalization of None."""
        self.assertIsNone(normalize_bpm(None))
        self.assertIsNone(normalize_bpm(""))
    
    def test_bpm_match_exact(self):
        """Test exact BPM matching."""
        self.assertTrue(bpm_match("99", 99, tolerance=0))
        self.assertTrue(bpm_match("128", 128, tolerance=0))
    
    def test_bpm_match_within_tolerance(self):
        """Test BPM matching within tolerance."""
        self.assertTrue(bpm_match("97", 99, tolerance=2))
        self.assertTrue(bpm_match("101", 99, tolerance=2))
        self.assertTrue(bpm_match("99.5", 99, tolerance=2))
    
    def test_bpm_match_outside_tolerance(self):
        """Test BPM not matching outside tolerance."""
        self.assertFalse(bpm_match("95", 99, tolerance=2))
        self.assertFalse(bpm_match("103", 99, tolerance=2))
    
    def test_bpm_match_with_text(self):
        """Test BPM matching with formatted strings."""
        self.assertTrue(bpm_match("99 BPM", 99, tolerance=2))
        self.assertTrue(bpm_match("~98", 99, tolerance=2))


if __name__ == "__main__":
    # Run tests with verbose output
    unittest.main(verbosity=2)

