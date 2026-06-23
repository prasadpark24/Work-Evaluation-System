#!/usr/bin/env python3
"""
Production App Launcher
=======================
Easy one-command startup with built-in health checks.

Usage:
    python launch.py          # Run with health check
    python launch.py --skip   # Skip health check (faster)
"""

import sys
import subprocess
from pathlib import Path

def main():
    skip_check = "--skip" in sys.argv
    
    if not skip_check:
        print("🔍 Running health check...")
        result = subprocess.run([sys.executable, "health_check.py"])
        if result.returncode != 0:
            print("\n❌ Health check failed. Fix issues and try again.")
            return 1
        print("\n✅ Health check passed!\n")
    
    print("🚀 Launching Streamlit application...")
    print("📱 App will open at: http://localhost:8501")
    print("📝 Press Ctrl+C to stop\n")
    
    result = subprocess.run([sys.executable, "-m", "streamlit", "run", "main.py"])
    return result.returncode

if __name__ == "__main__":
    sys.exit(main())
