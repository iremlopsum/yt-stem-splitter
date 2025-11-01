"""Unit tests for sanitization utilities."""

import unittest
from src.utils.sanitization import sanitize_filename


class TestSanitization(unittest.TestCase):
    """Test cases for filename sanitization."""
    
    def test_sanitize_basic_string(self):
        """Test sanitization of a basic string."""
        result = sanitize_filename("Simple Title")
        self.assertEqual(result, "Simple Title")
    
    def test_sanitize_with_special_chars(self):
        """Test removal of special characters."""
        result = sanitize_filename("Title: With @ Special # Chars!")
        self.assertEqual(result, "Title With  Special  Chars")
    
    def test_sanitize_with_parentheses(self):
        """Test that parentheses are preserved."""
        result = sanitize_filename("Song (feat. Artist)")
        self.assertEqual(result, "Song (feat Artist)")
    
    def test_sanitize_with_multiple_spaces(self):
        """Test collapsing of multiple spaces."""
        result = sanitize_filename("Too    Many     Spaces")
        self.assertEqual(result, "Too Many Spaces")
    
    def test_sanitize_with_dash_underscore(self):
        """Test that dashes and underscores are preserved."""
        result = sanitize_filename("Track-Name_With-Dash_And_Underscore")
        self.assertEqual(result, "Track-Name_With-Dash_And_Underscore")
    
    def test_sanitize_empty_string(self):
        """Test sanitization of empty string returns default."""
        result = sanitize_filename("")
        self.assertEqual(result, "yt_download")
    
    def test_sanitize_only_special_chars(self):
        """Test sanitization of string with only special chars."""
        result = sanitize_filename("@#$%^&*")
        self.assertEqual(result, "yt_download")
    
    def test_sanitize_with_leading_trailing_spaces(self):
        """Test trimming of leading and trailing spaces."""
        result = sanitize_filename("   Spaces Around   ")
        self.assertEqual(result, "Spaces Around")
    
    def test_sanitize_unicode_characters(self):
        """Test handling of unicode characters."""
        result = sanitize_filename("Song™ with © symbols®")
        # Unicode symbols should be removed
        self.assertIn("Song", result)
        self.assertIn("with", result)
        self.assertIn("symbols", result)


if __name__ == "__main__":
    unittest.main()

