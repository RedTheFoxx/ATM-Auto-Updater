"""Main class for handling ATM server updates."""

import logging
from pathlib import Path
from typing import Optional
from selenium import webdriver

from automation.webdriver import setup_webdriver
from automation.web_ops import (
    get_latest_version_url,
    build_download_url,
    download_new_server_files,
    get_current_version,
)
from automation.filesystem_ops import backup_items, unzip_new_server_files
from config import FORGE_URL, BACKUP_ITEMS

logger = logging.getLogger(__name__)

class ServerUpdater:
    """Handles the ATM server update process."""
    
    def __init__(self):
        self.driver: Optional[webdriver.Chrome] = None
        self.current_version: Optional[str] = None
        self.new_version_zip: Optional[str] = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.driver:
            self.driver.quit()

    def initialize(self):
        """Initialize the updater by checking current version and setting up WebDriver."""
        logger.info("Identifying current ATM modpack version...")
        self.current_version = get_current_version()
        
        if self.current_version:
            logger.info(f"Current version: {self.current_version}")
        else:
            logger.info("No existing version found")
            return False

        logger.info("Setting up WebDriver...")
        self.driver = setup_webdriver()

    def fetch_new_version(self) -> bool:
        """Fetch and download the new server version."""
        try:
            logger.info("Navigating to Forge website...")
            self.driver.get(FORGE_URL)
            
            version_url = get_latest_version_url(self.driver)
            download_url = build_download_url(version_url)
            self.new_version_zip = download_new_server_files(self.driver, download_url)
            
            return True
        except Exception as e:
            logger.error(f"Update can't continue. Please check your current server files can be found.")
            return False

    def update_server(self) -> bool:
        """Perform the server update process."""
        try:
            if not self.new_version_zip:
                raise ValueError("No new version downloaded")

            unzip_new_server_files(self.new_version_zip)
            
            if self.current_version:
                backup_items(self.current_version, self.new_version_zip, BACKUP_ITEMS)
            
            return True
        except Exception as e:
            logger.error(f"Error updating server: {e}")
            return False

    def run(self) -> bool:
        """Run the complete update process."""
        try:
            self.initialize()
            if not self.fetch_new_version():
                return False
            return self.update_server()
        except Exception as e:
            logger.error(f"Update process failed: {e}")
            return False
