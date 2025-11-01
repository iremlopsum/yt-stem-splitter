"""TuneBat web scraping for BPM and key information."""

import os
import time
import tempfile
import shutil
from typing import Optional, Tuple
from urllib.parse import quote

# Suppress Selenium/ChromeDriver logging
os.environ['WDM_LOG_LEVEL'] = '0'

# Check if Selenium is available
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    TUNEBAT_AVAILABLE = True
except ImportError:
    TUNEBAT_AVAILABLE = False


def is_tunebat_available() -> bool:
    """Check if TuneBat scraping dependencies are available."""
    return TUNEBAT_AVAILABLE


def _extract_track_info(driver) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Extract BPM, key, and Camelot from TuneBat page.
    
    Args:
        driver: Selenium WebDriver instance
        
    Returns:
        Tuple of (bpm, key, camelot)
    """
    bpm = None
    key = None
    camelot = None
    
    try:
        # Find all info containers
        info_containers = driver.find_elements(By.CSS_SELECTOR, 'div.yIPfN')
        
        for container in info_containers:
            try:
                # Get the label (in span with ant-typography-secondary class)
                label_element = container.find_element(By.CSS_SELECTOR, 'span.ant-typography-secondary')
                label = label_element.text.strip().lower()
                
                # Get the value (in h3 with ant-typography class)
                value_element = container.find_element(By.CSS_SELECTOR, 'h3.ant-typography')
                value = value_element.text.strip()
                
                if 'bpm' in label:
                    bpm = value
                elif 'key' in label:
                    key = value
                elif 'camelot' in label:
                    camelot = value
            except:
                continue
    except:
        pass
    
    return bpm, key, camelot


def scrape_tunebat_info(
    track_title: str,
    chrome_version: int = 141,
    silent: bool = False
) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Scrape TuneBat for BPM and key information.
    
    Args:
        track_title: Title of the track to search for
        chrome_version: Chrome driver version to use (kept for API compatibility, not used)
        silent: If True, suppress print statements
        
    Returns:
        Tuple of (bpm, key, camelot) where each can be None if not found
        
    Raises:
        ImportError: If required dependencies are not installed
    """
    if not TUNEBAT_AVAILABLE:
        return None, None, None
    
    driver = None
    temp_dir = None
    try:
        if not silent:
            print("Searching TuneBat for track information...")
        
        # Set up headless Chrome options
        options = Options()
        options.add_argument('--headless=new')  # Use new headless mode
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--log-level=3')  # Suppress Chrome logs
        options.add_argument('--window-size=1920,1080')
        
        # Add a realistic user agent to avoid bot detection
        options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        # Disable automation flags
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--disable-blink-features=AutomationControlled')
        
        # Use a unique temporary user data directory to avoid conflicts
        temp_dir = tempfile.mkdtemp()
        options.add_argument(f'--user-data-dir={temp_dir}')
        
        # Suppress logging
        import logging
        logging.getLogger('selenium').setLevel(logging.ERROR)
        logging.getLogger('urllib3').setLevel(logging.ERROR)
        
        # Initialize ChromeDriver
        service = Service()
        driver = webdriver.Chrome(service=service, options=options)
        
        # Search TuneBat
        search_query = quote(track_title)
        search_url = f"https://tunebat.com/Search?q={search_query}"
        driver.get(search_url)
        
        # Wait for Cloudflare and page to load
        time.sleep(10)  # Give Cloudflare time to pass
        wait = WebDriverWait(driver, 15)
        
        # Find first search result link
        try:
            first_result = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/Info/']"))
            )
            result_url = first_result.get_attribute('href')
            if not silent:
                print(f"Found TuneBat page: {result_url}")
            
            # Navigate to song page
            driver.get(result_url)
            time.sleep(10)  # Wait for page to load (including Cloudflare)
            
            # Extract song information
            bpm, key, camelot = _extract_track_info(driver)
            
            if bpm or key:
                if not silent:
                    print(f"✓ Retrieved from TuneBat: BPM={bpm}, Key={key}, Camelot={camelot}")
                return bpm, key, camelot
            else:
                if not silent:
                    print("Could not extract BPM/Key from TuneBat page")
                return None, None, None
                
        except Exception as e:
            if not silent:
                print(f"Could not find song on TuneBat: {e}")
            return None, None, None
    
    except Exception as e:
        if not silent:
            print(f"TuneBat scraping failed: {e}")
        return None, None, None
    
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass
        
        # Clean up temporary user data directory
        if temp_dir and os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir)
            except:
                pass

