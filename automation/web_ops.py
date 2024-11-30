"""Version management, downloading and checking for updates."""

import logging
import os
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

logger = logging.getLogger(__name__)

TIMEOUT_SECONDS = 60
FORGE_URL = "https://www.curseforge.com/minecraft/modpacks/all-the-mods-10/files/all?page=1&pageSize=10"

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

def build_download_url(version_url: str) -> str:
    file_id = version_url.split("/")[-1]
    return f"https://www.curseforge.com/minecraft/modpacks/all-the-mods-10/download/{file_id}"

def download_new_server_files(driver: webdriver.Chrome, download_url: str) -> str:
    try:
        logger.info(f"Downloading from: {download_url}")
        driver.get(download_url)

        _ = WebDriverWait(driver, TIMEOUT_SECONDS).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(10)  # Wait for download to complete

        # Get the file ID from the URL and construct the expected filename
        file_id = download_url.split("/")[-1]
        zip_name = f"Server-Files-{file_id}.zip"

        logger.info("Download completed successfully")
        return zip_name

    except Exception as e:
        logger.error(f"Error downloading server files: {e}")
        raise

def get_current_version() -> str | None:
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    directories = [
        d
        for d in os.listdir(current_dir)
        if os.path.isdir(os.path.join(current_dir, d))
    ]

    pattern = r"^Server-Files-1\.\d+$"
    matching_dirs = [
        d for d in directories if re.match(pattern, d) and not d.endswith(".zip")
    ]

    if len(matching_dirs) > 1:
        raise RuntimeError(
            f"Multiple Server-Files directories found: {', '.join(matching_dirs)}"
        )

    return matching_dirs[0] if matching_dirs else None
