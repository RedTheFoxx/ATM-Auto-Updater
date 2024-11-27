"""Main entrypoint of the tool
- Fetch the last version of ATM 10
- Download the server files in the same directory as the script
"""

import pathlib
import sys
import logging
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Constants
TIMEOUT_SECONDS = 60
pack_version = None
FORGE_URL = "https://www.curseforge.com/minecraft/modpacks/all-the-mods-10/files/all?page=1&pageSize=10"
output_directory = pathlib.Path(__file__).parent


def setup_webdriver() -> webdriver.Chrome | None:
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    chrome_options.add_argument("--enable-unsafe-swiftshader")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--disable-webgl")
    chrome_options.add_argument("--disable-webgl2")
    chrome_options.add_argument("--log-level=3")

    # Add download preferences
    chrome_options.add_experimental_option(
        "prefs",
        {
            "download.default_directory": str(output_directory),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
        },
    )

    try:
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=chrome_options
        )
        driver.set_page_load_timeout(TIMEOUT_SECONDS)
        return driver
    except WebDriverException as e:
        logger.error(f"Failed to initialize WebDriver: {e}")
        raise


def get_latest_version_url(driver: webdriver.Chrome | None) -> str:
    if driver is None:
        raise ValueError("WebDriver cannot be None")

    try:
        driver.implicitly_wait(10)

        logger.info("Loading page...")
        _ = WebDriverWait(driver, TIMEOUT_SECONDS).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.file-card"))
        )

        file_cards = driver.find_elements(By.CSS_SELECTOR, "a.file-card")

        logger.info("Searching for server file...")
        for card in file_cards:
            name = card.find_element(By.CSS_SELECTOR, "div.name").text
            if name.startswith("Server-Files"):
                download_url = card.get_attribute("href")
                logger.info(f"Found latest server file: {name}")
                return download_url

        raise ValueError("No server files found")

    except TimeoutException:
        logger.error("Timeout waiting for page to load")
        raise
    except Exception as e:
        logger.error(f"Error finding latest version: {e}")
        raise


def get_download_url(version_url: str) -> str:
    file_id = version_url.split("/")[-1]
    return f"https://www.curseforge.com/minecraft/modpacks/all-the-mods-10/download/{file_id}"


def download_server_files(driver: webdriver.Chrome, download_url: str) -> None:
    try:
        logger.info(f"Downloading from: {download_url}")
        driver.get(download_url)

        _ = WebDriverWait(driver, TIMEOUT_SECONDS).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(10)  # Wait for download to complete

        logger.info("Download completed successfully")

    except Exception as e:
        logger.error(f"Error downloading server files: {e}")
        raise


def main() -> bool:
    driver: webdriver.Chrome | None = None
    try:
        logger.info("Initializing WebDriver...")
        driver = setup_webdriver()

        logger.info(f"Navigating to {FORGE_URL}")
        driver.get(FORGE_URL)

        logger.info("Fetching latest version URL...")
        latest_version_url = get_latest_version_url(driver)

        logger.info(f"Latest version URL: {latest_version_url}")

        download_url = get_download_url(latest_version_url)
        logger.info(f"Download URL: {download_url}")

        download_server_files(driver, download_url)

        return True

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return False

    finally:
        if driver:
            logger.info("Closing WebDriver...")
            driver.quit()


if __name__ == "__main__":
    try:
        result = main()
        if not result:
            sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
        sys.exit(1)
