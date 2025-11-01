"""Unit tests for audio analysis module."""

import unittest
from unittest.mock import patch, MagicMock
from src.audio.analysis import (
    is_essentia_available,
    analyze_audio_bpm_key,
    ESSENTIA_AVAILABLE
)


class TestAudioAnalysis(unittest.TestCase):
    """Test cases for audio analysis functions."""
    
    def test_is_essentia_available(self):
        """Test checking if Essentia is available."""
        result = is_essentia_available()
        self.assertIsInstance(result, bool)
        self.assertEqual(result, ESSENTIA_AVAILABLE)
    
    @unittest.skipIf(not ESSENTIA_AVAILABLE, "Essentia not installed")
    @patch('src.audio.analysis.es.MonoLoader')
    @patch('src.audio.analysis.es.RhythmExtractor2013')
    @patch('src.audio.analysis.es.KeyExtractor')
    def test_analyze_audio_success(self, mock_key_extractor, mock_rhythm, mock_loader):
        """Test successful audio analysis."""
        # Mock audio data
        mock_audio = MagicMock()
        mock_loader.return_value.return_value = mock_audio
        
        # Mock rhythm extraction
        mock_rhythm_instance = MagicMock()
        mock_rhythm_instance.return_value = (128.5, [], 0.9, None, [])
        mock_rhythm.return_value = mock_rhythm_instance
        
        # Mock key extraction
        mock_key_instance = MagicMock()
        mock_key_instance.return_value = ("A", "major", 0.8)
        mock_key_extractor.return_value = mock_key_instance
        
        bpm, key, sources = analyze_audio_bpm_key("/path/to/test.wav")
        
        self.assertEqual(bpm, "128")
        self.assertEqual(key, "A Major")
        self.assertIn("Audio analysis (Essentia)", sources)
    
    @unittest.skipIf(ESSENTIA_AVAILABLE, "Test for when Essentia is not available")
    def test_analyze_audio_no_essentia(self):
        """Test analysis when Essentia is not available."""
        bpm, key, sources = analyze_audio_bpm_key("/path/to/test.wav")
        
        self.assertIsNone(bpm)
        self.assertIsNone(key)
        self.assertEqual(sources, [])
    
    @unittest.skipIf(not ESSENTIA_AVAILABLE, "Essentia not installed")
    @patch('src.audio.analysis.es.MonoLoader')
    def test_analyze_audio_file_not_found(self, mock_loader):
        """Test analysis with non-existent file."""
        mock_loader.side_effect = Exception("File not found")
        
        bpm, key, sources = analyze_audio_bpm_key("/nonexistent/file.wav")
        
        self.assertIsNone(bpm)
        self.assertIsNone(key)
        self.assertEqual(sources, [])
    
    @unittest.skipIf(not ESSENTIA_AVAILABLE, "Essentia not installed")
    def test_analyze_audio_custom_sample_rate(self):
        """Test analysis with custom sample rate."""
        with patch('src.audio.analysis.es.MonoLoader') as mock_loader, \
             patch('src.audio.analysis.es.RhythmExtractor2013') as mock_rhythm, \
             patch('src.audio.analysis.es.KeyExtractor') as mock_key:
            
            mock_loader.return_value.return_value = MagicMock()
            mock_rhythm.return_value.return_value = (120.0, [], 0.8, None, [])
            mock_key.return_value.return_value = ("C", "minor", 0.7)
            
            analyze_audio_bpm_key("/path/to/test.wav", sample_rate=48000)
            
            mock_loader.assert_called_with(
                filename="/path/to/test.wav",
                sampleRate=48000
            )


if __name__ == "__main__":
    unittest.main()

