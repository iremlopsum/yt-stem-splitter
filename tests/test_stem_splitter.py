"""Unit tests for stem splitter module."""

import unittest
import os
import tempfile
from unittest.mock import patch, MagicMock, call
from src.audio.stem_splitter import split_audio_stems


class TestStemSplitter(unittest.TestCase):
    """Test cases for audio stem splitting."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
    
    @patch('src.audio.stem_splitter.run_command')
    @patch('src.audio.stem_splitter.shutil.rmtree')
    @patch('src.audio.stem_splitter.os.makedirs')
    @patch('src.audio.stem_splitter.os.path.exists')
    @patch('src.audio.stem_splitter.shutil.copyfile')
    def test_split_audio_stems_success(
        self, mock_copy, mock_exists, mock_makedirs, mock_rmtree, mock_run
    ):
        """Test successful stem splitting."""
        input_path = "/path/to/song.wav"
        
        # Mock file existence checks
        def exists_side_effect(path):
            # Output dir exists initially, then stem files exist
            if "demucs_output" in path and "htdemucs" not in path:
                return True
            if "vocals.wav" in path or "no_vocals.wav" in path:
                return True
            return False
        
        mock_exists.side_effect = exists_side_effect
        
        vocals, instrumental = split_audio_stems(input_path)
        
        # Verify Demucs command was called
        expected_cmd = [
            "demucs",
            "--two-stems", "vocals",
            "-o", unittest.mock.ANY,
            input_path
        ]
        mock_run.assert_called_once()
        actual_cmd = mock_run.call_args[0][0]
        self.assertEqual(actual_cmd[0], "demucs")
        self.assertIn("--two-stems", actual_cmd)
        self.assertIn("vocals", actual_cmd)
        
        # Verify output files
        self.assertEqual(vocals, "song_vocals.wav")
        self.assertEqual(instrumental, "song_instrumental.wav")
        
        # Verify files were copied
        self.assertEqual(mock_copy.call_count, 2)
    
    @patch('src.audio.stem_splitter.run_command')
    @patch('src.audio.stem_splitter.os.path.exists')
    def test_split_audio_missing_output_files(self, mock_exists, mock_run):
        """Test error when expected output files are missing."""
        input_path = "/path/to/song.wav"
        
        # Mock that output files don't exist
        mock_exists.return_value = False
        
        with patch('src.audio.stem_splitter.os.makedirs'):
            with self.assertRaises(FileNotFoundError):
                split_audio_stems(input_path)
    
    @patch('src.audio.stem_splitter.run_command')
    @patch('src.audio.stem_splitter.os.path.exists')
    @patch('src.audio.stem_splitter.os.makedirs')
    @patch('src.audio.stem_splitter.shutil.rmtree')
    @patch('src.audio.stem_splitter.shutil.copyfile')
    def test_split_audio_custom_output_dir(
        self, mock_copy, mock_rmtree, mock_makedirs, mock_exists, mock_run
    ):
        """Test stem splitting with custom output directory."""
        input_path = "/path/to/song.wav"
        custom_output = "/custom/output"
        
        mock_exists.side_effect = lambda p: "vocals.wav" in p or "no_vocals.wav" in p
        
        split_audio_stems(input_path, output_dir=custom_output)
        
        # Verify custom output directory was used
        actual_cmd = mock_run.call_args[0][0]
        self.assertIn("-o", actual_cmd)
        idx = actual_cmd.index("-o")
        self.assertEqual(actual_cmd[idx + 1], custom_output)
    
    @patch('src.audio.stem_splitter.run_command')
    @patch('src.audio.stem_splitter.os.path.exists')
    @patch('src.audio.stem_splitter.os.makedirs')
    @patch('src.audio.stem_splitter.shutil.rmtree')
    @patch('src.audio.stem_splitter.shutil.copyfile')
    def test_split_audio_different_stem_type(
        self, mock_copy, mock_rmtree, mock_makedirs, mock_exists, mock_run
    ):
        """Test stem splitting with different stem type."""
        input_path = "/path/to/song.wav"
        
        mock_exists.side_effect = lambda p: "vocals.wav" in p or "no_vocals.wav" in p
        
        split_audio_stems(input_path, stem_type="drums")
        
        # Verify stem type was used
        actual_cmd = mock_run.call_args[0][0]
        self.assertIn("--two-stems", actual_cmd)
        idx = actual_cmd.index("--two-stems")
        self.assertEqual(actual_cmd[idx + 1], "drums")


if __name__ == "__main__":
    unittest.main()

