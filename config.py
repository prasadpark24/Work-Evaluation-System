"""
Production Configuration
========================
Centralized configuration for the Employee Performance Evaluation System.
"""

import os
from pathlib import Path

# ─────────────────────────────────────────────────────────────────────────────
# Directories
# ─────────────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
CHROMA_DB_DIR = BASE_DIR / "chroma_db"
LOG_DIR = BASE_DIR / "logs"

# Create directories if they don't exist
CHROMA_DB_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

# ─────────────────────────────────────────────────────────────────────────────
# LLM & Embedding Models
# ─────────────────────────────────────────────────────────────────────────────
EMBED_MODEL = os.getenv("EMBED_MODEL", "nomic-embed-text")
LLM_MODEL = os.getenv("LLM_MODEL", "llama3.2:latest")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# ─────────────────────────────────────────────────────────────────────────────
# PDF & RAG Settings
# ─────────────────────────────────────────────────────────────────────────────
PDF_FILE = BASE_DIR / "employee_details.pdf"
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "5000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "1500"))
RAG_TOP_K = int(os.getenv("RAG_TOP_K", "3"))

# ─────────────────────────────────────────────────────────────────────────────
# Streamlit Configuration
# ─────────────────────────────────────────────────────────────────────────────
STREAMLIT_PAGE_TITLE = "Employee Performance Evaluation"
STREAMLIT_PAGE_ICON = "📊"
STREAMLIT_LAYOUT = "wide"

# ─────────────────────────────────────────────────────────────────────────────
# Logging
# ─────────────────────────────────────────────────────────────────────────────
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = LOG_DIR / "app.log"

# ─────────────────────────────────────────────────────────────────────────────
# GitHub Settings
# ─────────────────────────────────────────────────────────────────────────────
GITHUB_DEFAULT_DAYS = int(os.getenv("GITHUB_DEFAULT_DAYS", "90"))

# ─────────────────────────────────────────────────────────────────────────────
# Cache Settings
# ─────────────────────────────────────────────────────────────────────────────
CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", "3600"))  # 1 hour

# ─────────────────────────────────────────────────────────────────────────────
# Default Employee Data
# ─────────────────────────────────────────────────────────────────────────────
DEFAULT_EMPLOYEE_ID = "EMP001"
DEFAULT_MONTH = "2024-04"
DEFAULT_QUARTER = "Q1-2024"
DEFAULT_YEAR = "2024"
