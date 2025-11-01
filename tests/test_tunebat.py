"""Unit tests for TuneBat scraper module."""

import unittest
from unittest.mock import patch, MagicMock
from src.scrapers.tunebat import (
    is_tunebat_available,
    scrape_tunebat_info,
    TUNEBAT_AVAILABLE
)


class TestTuneBatScraper(unittest.TestCase):
    """Test cases for TuneBat scraping functionality."""
    
    def test_is_tunebat_available(self):
        """Test checking if TuneBat dependencies are available."""
        result = is_tunebat_available()
        self.assertIsInstance(result, bool)
        self.assertEqual(result, TUNEBAT_AVAILABLE)
    
    @unittest.skipIf(not TUNEBAT_AVAILABLE, "TuneBat dependencies not installed")
    @patch('src.scrapers.tunebat.Service')
    @patch('src.scrapers.tunebat.webdriver.Chrome')
    @patch('src.scrapers.tunebat._extract_track_info')
    def test_scrape_tunebat_success(
        self, mock_extract, mock_chrome, mock_service
    ):
        """Test successful TuneBat scraping."""
        # Mock WebDriver
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver
        
        # Mock search result
        mock_element = MagicMock()
        mock_element.get_attribute.return_value = "https://tunebat.com/Info/TestSong"
        mock_driver.find_element.return_value = mock_element
        
        # Mock extraction results
        mock_extract.return_value = ("128", "A Minor", "8A")
        
        bpm, key, camelot = scrape_tunebat_info("Test Song", silent=True)
        
        self.assertEqual(bpm, "128")
        self.assertEqual(key, "A Minor")
        self.assertEqual(camelot, "8A")
        
        # Verify driver was quit
        mock_driver.quit.assert_called_once()
    
    @unittest.skipIf(TUNEBAT_AVAILABLE, "Test for when dependencies are not available")
    def test_scrape_tunebat_no_dependencies(self):
        """Test scraping when dependencies are not available."""
        bpm, key, camelot = scrape_tunebat_info("Test Song")
        
        self.assertIsNone(bpm)
        self.assertIsNone(key)
        self.assertIsNone(camelot)
    
    @unittest.skipIf(not TUNEBAT_AVAILABLE, "TuneBat dependencies not installed")
    @patch('src.scrapers.tunebat.Service')
    @patch('src.scrapers.tunebat.webdriver.Chrome')
    def test_scrape_tunebat_no_results(self, mock_chrome, mock_service):
        """Test scraping when no results are found."""
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver
        
        # Simulate no search results
        from selenium.common.exceptions import TimeoutException
        mock_driver.find_element.side_effect = TimeoutException()
        
        bpm, key, camelot = scrape_tunebat_info("Nonexistent Song", silent=True)
        
        self.assertIsNone(bpm)
        self.assertIsNone(key)
        self.assertIsNone(camelot)
        
        mock_driver.quit.assert_called_once()
    
    @unittest.skipIf(not TUNEBAT_AVAILABLE, "TuneBat dependencies not installed")
    @patch('src.scrapers.tunebat.Service')
    @patch('src.scrapers.tunebat.webdriver.Chrome')
    def test_scrape_tunebat_driver_cleanup_on_error(self, mock_chrome, mock_service):
        """Test that driver is cleaned up even on error."""
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver
        
        # Simulate error during scraping
        mock_driver.get.side_effect = Exception("Network error")
        
        bpm, key, camelot = scrape_tunebat_info("Test Song", silent=True)
        
        # Should still try to quit driver
        mock_driver.quit.assert_called_once()
        
        # Should return None values
        self.assertIsNone(bpm)
        self.assertIsNone(key)
        self.assertIsNone(camelot)
    
    @unittest.skipIf(not TUNEBAT_AVAILABLE, "TuneBat dependencies not installed")
    @patch('src.scrapers.tunebat.Service')
    @patch('src.scrapers.tunebat.webdriver.Chrome')
    @patch('src.scrapers.tunebat._extract_track_info')
    def test_scrape_tunebat_custom_chrome_version(
        self, mock_extract, mock_chrome, mock_service
    ):
        """Test scraping with custom Chrome version parameter (kept for API compatibility)."""
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver
        
        mock_element = MagicMock()
        mock_element.get_attribute.return_value = "https://tunebat.com/Info/Test"
        mock_driver.find_element.return_value = mock_element
        
        mock_extract.return_value = ("120", "C Major", "8B")
        
        scrape_tunebat_info("Test Song", chrome_version=142, silent=True)
        
        # Verify Chrome was initialized (chrome_version parameter is ignored in new implementation)
        mock_chrome.assert_called_once()


if __name__ == "__main__":
    unittest.main()

