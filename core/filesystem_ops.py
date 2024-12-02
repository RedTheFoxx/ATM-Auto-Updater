"""Filesystem related operations, like backuping, transfering old maps and custom mods + server.properties. Also handles zipping operations."""

import os
import shutil
import logging
import zipfile

logger = logging.getLogger(__name__)

def backup_items(current_version: str, target_path: str, backup_dict: dict) -> None:
    """
    Backup files and folders from the current version to a target path based on a backup dictionary.
    Skip items that are not found instead of raising an error.
    
    Args:
        current_version (str): Path to the current version directory
        target_path (str): Path to the target directory where items will be backed up
        backup_dict (dict): Dictionary containing items to backup with their types
    """
    logger.info("Backing up custom files and folders...")
    for item, item_type in backup_dict.items():
        current_path = os.path.join(current_version, item)
        logger.debug(f"Processing backup of {item} ({item_type['type']})")
        
        if item_type["type"] == "file":
            if os.path.isfile(current_path):
                new_path = os.path.join(target_path, item)
                shutil.copy2(current_path, new_path)
                logger.info(f"Successfully backed up file: {item}")
            else:
                logger.warning(f"File not found, skipping: {item}")
        
        elif item_type["type"] == "folder":
            if os.path.isdir(current_path):
                new_path = os.path.join(target_path, item)
                shutil.copytree(current_path, new_path, dirs_exist_ok=True)
                logger.info(f"Successfully backed up folder: {item}")
            else:
                logger.warning(f"Folder not found, skipping: {item}")

def unzip_new_server_files(zip_name: str) -> None:
    """
    Extract the contents of a zip file containing server files.
    
    Args:
        zip_name (str): Path to the zip file to extract
    """
    logger.info(f"Extracting {zip_name}...")
    with zipfile.ZipFile(zip_name, 'r') as zip_ref:
        # Extract all contents to the current directory
        zip_ref.extractall('.')
    logger.info("Server files extracted successfully")

def zip_directory(directory_path: str) -> None:
    """
    Create a zip archive of a directory.
    The zip file will have the same name as the directory.
    
    Args:
        directory_path (str): Path to the directory to zip
    """
    if not os.path.exists(directory_path):
        raise ValueError(f"Directory not found: {directory_path}")
    
    zip_name = f"{directory_path}.zip"
    logger.info(f"Creating zip archive: {zip_name}")
    
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, directory_path)
                zipf.write(file_path, arcname)
    
    logger.info(f"Successfully created zip archive: {zip_name}")

if __name__ == "__main__":
    print("DEBUG MODE : Testing filesystem operations...")