"""WebDriver setup and management functions. Scrapes CurseForges with respect."""

import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
import pathlib

logger = logging.getLogger(__name__)

TIMEOUT_SECONDS = 60
output_directory = pathlib.Path(__file__).parent.parent

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
