"""Logging configuration."""
import logging
import logging.config
import os

from src.core.config import settings


def setup_logging() -> None:
    """Configure logging for the application."""
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            },
        },
        "handlers": {
            "default": {
                "level": settings.log_level,
                "class": "logging.StreamHandler",
                "formatter": "default",
            },
            "file": {
                "level": "DEBUG",
                "class": "logging.FileHandler",
                "filename": "logs/app.log",
                "formatter": "default",
            },
        },
        "root": {
            "level": settings.log_level,
            "handlers": ["default", "file"],
        },
    }

    logging.config.dictConfig(logging_config)
