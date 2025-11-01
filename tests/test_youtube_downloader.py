"""Unit tests for YouTube downloader module."""

import unittest
import os
import tempfile
from unittest.mock import patch, MagicMock
from src.downloader.youtube import get_youtube_title, download_youtube_audio


class TestYouTubeDownloader(unittest.TestCase):
    """Test cases for YouTube download functionality."""
    
    @patch('src.downloader.youtube.run_command_capture')
    def test_get_youtube_title_success(self, mock_run):
        """Test successful title retrieval."""
        mock_run.return_value = MagicMock(stdout="Amazing Song Title\n")
        
        title = get_youtube_title("https://youtube.com/watch?v=test")
        
        self.assertEqual(title, "Amazing Song Title")
        mock_run.assert_called_once_with([
            "yt-dlp",
            "--no-playlist",
            "--print",
            "%(title)s",
            "https://youtube.com/watch?v=test"
        ])
    
    @patch('src.downloader.youtube.run_command_capture')
    def test_get_youtube_title_with_special_chars(self, mock_run):
        """Test title with special characters."""
        mock_run.return_value = MagicMock(stdout="Song (feat. Artist) - Remix\n")
        
        title = get_youtube_title("https://youtube.com/watch?v=test")
        
        self.assertEqual(title, "Song (feat. Artist) - Remix")
    
    @patch('src.downloader.youtube.subprocess.run')
    @patch('src.downloader.youtube.os.makedirs')
    @patch('src.downloader.youtube.os.listdir')
    @patch('src.downloader.youtube.os.path.getmtime')
    def test_download_youtube_audio_success(
        self, mock_getmtime, mock_listdir, mock_makedirs, mock_run
    ):
        """Test successful audio download."""
        mock_listdir.return_value = ["song.wav"]
        mock_getmtime.return_value = 123456789
        
        result = download_youtube_audio(
            "https://youtube.com/watch?v=test",
            "/output/dir"
        )
        
        self.assertEqual(result, "/output/dir/song.wav")
        mock_makedirs.assert_called_once_with("/output/dir", exist_ok=True)
        mock_run.assert_called_once()
    
    @patch('src.downloader.youtube.subprocess.run')
    @patch('src.downloader.youtube.os.makedirs')
    @patch('src.downloader.youtube.os.listdir')
    def test_download_youtube_audio_no_file_found(
        self, mock_listdir, mock_makedirs, mock_run
    ):
        """Test error when no audio file is found after download."""
        mock_listdir.return_value = []  # No files
        
        with self.assertRaises(FileNotFoundError) as cm:
            download_youtube_audio(
                "https://youtube.com/watch?v=test",
                "/output/dir"
            )
        
        self.assertIn("No WAV file found", str(cm.exception))
    
    @patch('src.downloader.youtube.subprocess.run')
    @patch('src.downloader.youtube.os.makedirs')
    @patch('src.downloader.youtube.os.listdir')
    @patch('src.downloader.youtube.os.path.getmtime')
    def test_download_youtube_audio_custom_format(
        self, mock_getmtime, mock_listdir, mock_makedirs, mock_run
    ):
        """Test download with custom audio format."""
        mock_listdir.return_value = ["song.mp3"]
        mock_getmtime.return_value = 123456789
        
        result = download_youtube_audio(
            "https://youtube.com/watch?v=test",
            "/output/dir",
            audio_format="mp3"
        )
        
        self.assertEqual(result, "/output/dir/song.mp3")
        
        # Verify format was passed to yt-dlp
        actual_cmd = mock_run.call_args[0][0]
        self.assertIn("--audio-format", actual_cmd)
        format_idx = actual_cmd.index("--audio-format")
        self.assertEqual(actual_cmd[format_idx + 1], "mp3")
    
    @patch('src.downloader.youtube.subprocess.run')
    @patch('src.downloader.youtube.os.makedirs')
    @patch('src.downloader.youtube.os.listdir')
    @patch('src.downloader.youtube.os.path.getmtime')
    def test_download_youtube_audio_multiple_files(
        self, mock_getmtime, mock_listdir, mock_makedirs, mock_run
    ):
        """Test download when multiple files exist (returns most recent)."""
        mock_listdir.return_value = ["old_song.wav", "new_song.wav"]
        
        # Make new_song.wav more recent
        def getmtime_side_effect(path):
            if "new_song" in path:
                return 200
            return 100
        
        mock_getmtime.side_effect = getmtime_side_effect
        
        result = download_youtube_audio(
            "https://youtube.com/watch?v=test",
            "/output/dir"
        )
        
        self.assertEqual(result, "/output/dir/new_song.wav")


if __name__ == "__main__":
    unittest.main()

