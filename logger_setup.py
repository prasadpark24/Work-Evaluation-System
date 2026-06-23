"""
Logging Setup
=============
Centralized logging configuration for production.
"""

import logging
import sys
from pathlib import Path
from config import LOG_LEVEL, LOG_FILE

# ─────────────────────────────────────────────────────────────────────────────
# Create logger
# ─────────────────────────────────────────────────────────────────────────────
logger = logging.getLogger("EmployeeEvaluation")
logger.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))

# ─────────────────────────────────────────────────────────────────────────────
# Console handler
# ─────────────────────────────────────────────────────────────────────────────
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))

# ─────────────────────────────────────────────────────────────────────────────
# File handler
# ─────────────────────────────────────────────────────────────────────────────
file_handler = logging.FileHandler(LOG_FILE, mode='a', encoding='utf-8')
file_handler.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))

# ─────────────────────────────────────────────────────────────────────────────
# Formatter
# ─────────────────────────────────────────────────────────────────────────────
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# ─────────────────────────────────────────────────────────────────────────────
# Add handlers to logger
# ─────────────────────────────────────────────────────────────────────────────
logger.addHandler(console_handler)
logger.addHandler(file_handler)


def get_logger():
    """Return the configured logger."""
    return logger