#!/usr/bin/env python3
"""Main entry point for PhoneInfoga application."""

import logging

from phoneinfoga.logs import init_logging
from phoneinfoga.build import get_version_string, is_release
from phoneinfoga.cli import main

# Initialize logging
init_logging()

logger = logging.getLogger(__name__)
logger.debug(f"Build info - isRelease: {is_release()}, version: {get_version_string()}")

if __name__ == "__main__":
    main()
