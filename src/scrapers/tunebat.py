"""TuneBat web scraping for BPM and key information."""

import time
import platform
import subprocess
from typing import Optional, Tuple
from urllib.parse import quote

# Check if Selenium and undetected_chromedriver are available
try:
    import undetected_chromedriver as uc
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    TUNEBAT_AVAILABLE = True
except ImportError:
    TUNEBAT_AVAILABLE = False


def is_tunebat_available() -> bool:
    """Check if TuneBat scraping dependencies are available."""
    return TUNEBAT_AVAILABLE


def _hide_chrome_window(driver) -> None:
    """Attempt to hide or minimize the Chrome window."""
    try:
        driver.minimize_window()
    except:
        # If minimize doesn't work, try to move it off-screen
        try:
            driver.set_window_position(-2000, -2000)
            driver.set_window_size(1, 1)
        except:
            pass
    
    # On macOS, try to hide Chrome completely using AppleScript
    if platform.system() == 'Darwin':
        try:
            subprocess.run(
                ['osascript', '-e', 
                 'tell application "System Events" to set visible of process "Google Chrome" to false'],
                capture_output=True,
                timeout=1
            )
        except:
            pass


def _extract_track_info(driver, wait: WebDriverWait) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Extract BPM, key, and Camelot from TuneBat page.
    
    Args:
        driver: Selenium WebDriver instance
        wait: WebDriverWait instance
        
    Returns:
        Tuple of (bpm, key, camelot)
    """
    bpm = None
    key = None
    camelot = None
    
    try:
        # Get BPM
        bpm_label = driver.find_element(
            By.XPATH,
            "//span[contains(@class, 'ant-typography-secondary') and text()='BPM']"
        )
        bpm_parent = bpm_label.find_element(By.XPATH, "..")
        bpm_element = bpm_parent.find_element(By.TAG_NAME, "h3")
        bpm = bpm_element.text.strip()
    except:
        pass
    
    try:
        # Get Key
        key_label = driver.find_element(
            By.XPATH,
            "//span[contains(@class, 'ant-typography-secondary') and text()='key']"
        )
        key_parent = key_label.find_element(By.XPATH, "..")
        key_element = key_parent.find_element(By.TAG_NAME, "h3")
        key = key_element.text.strip()
    except:
        pass
    
    try:
        # Get Camelot
        camelot_label = driver.find_element(
            By.XPATH,
            "//span[contains(@class, 'ant-typography-secondary') and text()='camelot']"
        )
        camelot_parent = camelot_label.find_element(By.XPATH, "..")
        camelot_element = camelot_parent.find_element(By.TAG_NAME, "h3")
        camelot = camelot_element.text.strip()
    except:
        pass
    
    return bpm, key, camelot


def scrape_tunebat_info(
    track_title: str,
    chrome_version: int = 141
) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Scrape TuneBat for BPM and key information.
    
    Args:
        track_title: Title of the track to search for
        chrome_version: Chrome driver version to use
        
    Returns:
        Tuple of (bpm, key, camelot) where each can be None if not found
        
    Raises:
        ImportError: If required dependencies are not installed
    """
    if not TUNEBAT_AVAILABLE:
        return None, None, None
    
    driver = None
    try:
        print("Searching TuneBat for track information...")
        
        # Set up undetected Chrome
        options = uc.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        
        # Initialize driver
        driver = uc.Chrome(
            options=options,
            version_main=chrome_version,
            use_subprocess=True
        )
        
        # Hide the window
        _hide_chrome_window(driver)
        
        # Search TuneBat
        search_query = quote(track_title)
        search_url = f"https://tunebat.com/Search?q={search_query}"
        driver.get(search_url)
        
        # Wait for search results
        time.sleep(3)
        wait = WebDriverWait(driver, 10)
        
        # Find first search result link
        try:
            first_result = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/Info/']"))
            )
            result_url = first_result.get_attribute('href')
            print(f"Found TuneBat page: {result_url}")
            
            # Navigate to song page
            driver.get(result_url)
            time.sleep(3)
            
            # Scroll to trigger lazy loading
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)
            
            # Extract song information
            bpm, key, camelot = _extract_track_info(driver, wait)
            
            if bpm or key:
                print(f"✓ Retrieved from TuneBat: BPM={bpm}, Key={key}, Camelot={camelot}")
                return bpm, key, camelot
            else:
                print("Could not extract BPM/Key from TuneBat page")
                # Debug info
                try:
                    all_secondary_spans = driver.find_elements(
                        By.CLASS_NAME,
                        "ant-typography-secondary"
                    )
                    print(f"  Found {len(all_secondary_spans)} label elements")
                    if all_secondary_spans:
                        labels = [span.text for span in all_secondary_spans[:5]]
                        print(f"  Labels: {labels}")
                except:
                    pass
                return None, None, None
                
        except Exception as e:
            print(f"Could not find song on TuneBat: {e}")
            return None, None, None
    
    except Exception as e:
        print(f"TuneBat scraping failed: {e}")
        return None, None, None
    
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass

