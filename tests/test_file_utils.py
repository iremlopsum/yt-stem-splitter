"""Unit tests for file utilities."""

import unittest
import sys
from unittest.mock import patch, MagicMock
from src.utils.file_utils import ensure_dependency


class TestFileUtils(unittest.TestCase):
    """Test cases for file utility functions."""
    
    @patch('src.utils.file_utils.run_command_capture')
    def test_ensure_dependency_exists(self, mock_run):
        """Test checking for existing dependency."""
        mock_run.return_value = MagicMock(stdout="version 1.0")
        
        # Should not raise exception
        ensure_dependency("yt-dlp")
        
        mock_run.assert_called_once_with(["yt-dlp", "--version"])
    
    @patch('src.utils.file_utils.run_command_capture')
    @patch('builtins.print')
    def test_ensure_dependency_missing(self, mock_print, mock_run):
        """Test checking for missing dependency exits."""
        mock_run.side_effect = Exception("Command not found")
        
        with self.assertRaises(SystemExit) as cm:
            ensure_dependency("missing-tool")
        
        self.assertEqual(cm.exception.code, 1)
        mock_print.assert_called_with(
            "Error: required dependency 'missing-tool' not found in PATH."
        )
    
    @patch('src.utils.file_utils.run_command_capture')
    def test_ensure_dependency_multiple_checks(self, mock_run):
        """Test checking multiple dependencies."""
        mock_run.return_value = MagicMock(stdout="version")
        
        ensure_dependency("dep1")
        ensure_dependency("dep2")
        
        self.assertEqual(mock_run.call_count, 2)


if __name__ == "__main__":
    unittest.main()

