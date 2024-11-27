"""Main entrypoint of the tool
- Fetch the last version of ATM 10
- Download the server files in the same directory as the script
"""

import logging
import sys
from automation.webdriver import setup_webdriver
from automation.version_management import (
    get_latest_version_url,
    build_download_url,
    download_new_server_files,
    get_current_version,
    FORGE_URL
)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def main() -> bool:
    try:
        logger.info("Identifying current ATM modpack version...")
        current_version = get_current_version()
        
        if current_version:
            logger.info(f"Current version: {current_version}")
        else:
            logger.info("No existing version found")

        logger.info("Setting up WebDriver...")
        driver = setup_webdriver()
        
        logger.info("Navigating to Forge website...")
        driver.get(FORGE_URL)
        
        version_url = get_latest_version_url(driver)
        download_url = build_download_url(version_url)
        download_new_server_files(driver, download_url)
        
        return True

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return False

    finally:
        if driver:
            driver.quit()


if __name__ == "__main__":
    try:
        result = main()
        sys.exit(0 if result else 1)
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)
