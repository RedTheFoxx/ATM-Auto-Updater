"""Main entrypoint for the ATM server updater tool."""

import logging
import sys
from server_updater import ServerUpdater

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def main() -> int:
    """Main entry point of the application."""
    try:
        with ServerUpdater() as updater:
            success = updater.run()
            return 0 if success else 1
            
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
