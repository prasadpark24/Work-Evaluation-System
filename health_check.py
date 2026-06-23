"""
Health Check & Startup Verification
====================================
Verifies system dependencies and connectivity before running the app.
"""

import sys
import subprocess
from pathlib import Path
from logger_setup import get_logger

logger = get_logger()


def check_dependencies():
    """Check if all required packages are installed."""
    required_packages = [
        'streamlit', 'langchain', 'ollama', 'mcp', 'chromadb', 'PyGithub'
    ]
    missing = []
    
    for package in required_packages:
        try:
            __import__(package)
            logger.info(f"✓ {package} installed")
        except ImportError:
            missing.append(package)
            logger.error(f"✗ {package} NOT installed")
    
    return len(missing) == 0, missing


def check_ollama():
    """Check if Ollama service is running."""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        logger.info("✓ Ollama service is running")
        return True
    except Exception as e:
        logger.warning(f"✗ Ollama service not accessible: {e}")
        return False


def check_pdf():
    """Check if employee_details.pdf exists."""
    pdf_path = Path("employee_details.pdf")
    if pdf_path.exists():
        logger.info(f"✓ PDF file found: {pdf_path}")
        return True
    else:
        logger.warning(f"✗ PDF file not found: {pdf_path}")
        return False


def main():
    """Run all health checks."""
    logger.info("=" * 60)
    logger.info("Starting Health Check & Startup Verification")
    logger.info("=" * 60)
    
    deps_ok, missing = check_dependencies()
    ollama_ok = check_ollama()
    pdf_ok = check_pdf()
    
    logger.info("=" * 60)
    logger.info("Health Check Summary:")
    logger.info(f"  Dependencies: {'✓ PASS' if deps_ok else '✗ FAIL'}")
    logger.info(f"  Ollama Service: {'✓ PASS' if ollama_ok else '✗ WARNING'}")
    logger.info(f"  PDF File: {'✓ PASS' if pdf_ok else '✗ WARNING'}")
    logger.info("=" * 60)
    
    if not deps_ok:
        logger.error(f"Missing packages: {', '.join(missing)}")
        logger.error("Run: pip install -r requirements.txt")
        return False
    
    if not ollama_ok:
        logger.warning("Ollama service is not running. Start it before using RAG features.")
    
    if not pdf_ok:
        logger.warning("PDF file not found. RAG features will not work. Place employee_details.pdf in the project root.")
    
    logger.info("✓ Health check complete! Ready to start the app.")
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
