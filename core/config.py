"""Configuration settings for the ATM server updater."""

from pathlib import Path

# Web related settings
FORGE_URL = "https://www.curseforge.com/minecraft/modpacks/all-the-mods-10/files/all?page=1&pageSize=10"
TIMEOUT_SECONDS = 60

# Backup configuration
BACKUP_ITEMS = {
    "server.properties": {"type": "file"},
    "ops.json": {"type": "file"},
    "whitelist.json": {"type": "file"},
    "journeymap": {"type": "folder"},
    "fluffyworld": {"type": "folder"},
    "eula.txt": {"type": "file"},
    "user_jvm_args.txt": {"type": "file"},
    "banned-ips.json": {"type": "file"},
    "banned-players.json": {"type": "file"},
    "servericon.png": {"type": "file"},
}

# Paths
BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR

# Chrome options
CHROME_OPTIONS = [
    "--headless",
    "--no-sandbox",
    "--disable-dev-shm-usage",
    "--disable-gpu",
    "--disable-blink-features=AutomationControlled",
    "--enable-unsafe-swiftshader",
    "--disable-software-rasterizer",
    "--disable-webgl",
    "--disable-webgl2",
    "--log-level=3",
]

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
