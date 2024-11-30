"""Main entrypoint of the tool
- Fetch the last version of ATM 10
- Download the server files in the same directory as the script
"""

import logging
import sys
from automation.webdriver import setup_webdriver
from automation.web_ops import (
    get_latest_version_url,
    build_download_url,
    download_new_server_files,
    get_current_version,
    FORGE_URL
)
from automation.filesystem_ops import backup_items, unzip_new_server_files

BACKUP_DICT = {
    "server.properties": {"type": "file"},
    "ops.json": {"type": "file"},
    "whitelist.json": {"type": "file"},
    "journeymap": {"type": "folder"},
    "fluffyworld": {"type": "folder"},
}


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def main() -> bool:
    try:
        # Step 1. Check the current pack version
        logger.info("Identifying current ATM modpack version...")
        current_version = get_current_version()
        
        if current_version:
            logger.info(f"Current version: {current_version}")
        else:
            logger.info("No existing version found")

        # Step 2. Setup WebDriver
        logger.info("Setting up WebDriver...")
        driver = setup_webdriver()
        
        # Step 3. Navigate to Forge website
        logger.info("Navigating to Forge website...")
        driver.get(FORGE_URL)
        
        # Step 4. Get the latest version url
        version_url = get_latest_version_url(driver)
        
        # Step 5. Build the download url
        download_url = build_download_url(version_url)
        
        # Step 6. Download the new server files by sending to the driver the download url
        zip_name = download_new_server_files(driver, download_url)

        # Step 7. Unzip the new server files
        unzip_new_server_files(zip_name)

        # Step 8. Backup things from the old folder to the new one
        backup_items(current_version, zip_name, BACKUP_DICT)

        
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
