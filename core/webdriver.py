"""WebDriver setup and management functions. Scrapes CurseForges with respect."""

import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
import pathlib

logger = logging.getLogger(__name__)

from core.config import TIMEOUT_SECONDS, OUTPUT_DIR, CHROME_OPTIONS, USER_AGENT

def setup_webdriver() -> webdriver.Chrome | None:
    chrome_options = Options()
    for option in CHROME_OPTIONS:
        chrome_options.add_argument(option)
    chrome_options.add_argument(f"--user-agent={USER_AGENT}")

    chrome_options.add_experimental_option(
        "prefs",
        {
            "download.default_directory": str(OUTPUT_DIR),
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
