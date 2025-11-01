"""Logging configuration and initialization."""

import logging
import os
from typing import Optional

from phoneinfoga.build import is_release


class LogConfig:
    """Configuration for logging."""
    
    def __init__(self) -> None:
        """Initialize logging configuration."""
        self.level: int = logging.WARNING
        self.report_caller: bool = False
        
        # Set debug level if not a release build
        if not is_release():
            self.level = logging.DEBUG
        
        # Override with environment variable if set
        log_level_str = os.getenv("LOG_LEVEL", "").upper()
        if log_level_str:
            level_map = {
                "DEBUG": logging.DEBUG,
                "INFO": logging.INFO,
                "WARNING": logging.WARNING,
                "WARN": logging.WARNING,
                "ERROR": logging.ERROR,
                "CRITICAL": logging.CRITICAL,
            }
            self.level = level_map.get(log_level_str, self.level)


def init_logging() -> None:
    """Initialize logging with appropriate configuration."""
    config = LogConfig()
    
    # Configure root logger
    logging.basicConfig(
        level=config.level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    
    # Set report caller if needed
    if config.report_caller:
        logging.basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
        )


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Get a logger instance.
    
    Args:
        name: Name for the logger. If None, returns root logger.
        
    Returns:
        logging.Logger: Configured logger instance
    """
    return logging.getLogger(name)
