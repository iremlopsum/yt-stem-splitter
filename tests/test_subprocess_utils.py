"""Unit tests for subprocess utilities."""

import unittest
import subprocess
from unittest.mock import patch, MagicMock
from src.utils.subprocess_utils import run_command, run_command_capture


class TestSubprocessUtils(unittest.TestCase):
    """Test cases for subprocess utility functions."""
    
    @patch('subprocess.run')
    def test_run_command_success(self, mock_run):
        """Test successful command execution."""
        mock_run.return_value = MagicMock(returncode=0)
        
        result = run_command(["echo", "hello"])
        
        mock_run.assert_called_once_with(["echo", "hello"], cwd=None, check=True)
        self.assertIsNotNone(result)
    
    @patch('subprocess.run')
    def test_run_command_with_cwd(self, mock_run):
        """Test command execution with working directory."""
        mock_run.return_value = MagicMock(returncode=0)
        
        run_command(["ls"], cwd="/tmp")
        
        mock_run.assert_called_once_with(["ls"], cwd="/tmp", check=True)
    
    @patch('subprocess.run')
    def test_run_command_failure(self, mock_run):
        """Test that failed command raises exception."""
        mock_run.side_effect = subprocess.CalledProcessError(1, ["false"])
        
        with self.assertRaises(subprocess.CalledProcessError):
            run_command(["false"])
    
    @patch('subprocess.run')
    def test_run_command_capture_success(self, mock_run):
        """Test capturing command output."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="output text",
            stderr=""
        )
        
        result = run_command_capture(["echo", "test"])
        
        mock_run.assert_called_once_with(
            ["echo", "test"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        self.assertEqual(result.stdout, "output text")
    
    @patch('subprocess.run')
    def test_run_command_capture_with_stderr(self, mock_run):
        """Test capturing command with stderr."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="",
            stderr="error message"
        )
        
        result = run_command_capture(["some_command"])
        
        self.assertEqual(result.stderr, "error message")
    
    @patch('subprocess.run')
    def test_run_command_capture_failure(self, mock_run):
        """Test that failed capture command raises exception."""
        mock_run.side_effect = subprocess.CalledProcessError(1, ["false"])
        
        with self.assertRaises(subprocess.CalledProcessError):
            run_command_capture(["false"])


if __name__ == "__main__":
    unittest.main()

