"""Application entry point."""
import uvicorn
import sys
import logging

from src.utils import setup_logging
from src.core.config import settings

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


def main():
    """Run the application."""
    try:
        logger.info(f"Starting {settings.api_title}")
        uvicorn.run(
            "src.api.main:app",
            host="0.0.0.0",
            port=8000,
            reload=settings.debug,
            log_level=settings.log_level.lower(),
        )
    except Exception as e:
        logger.error(f"Failed to start application: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
