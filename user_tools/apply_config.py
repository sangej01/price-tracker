"""
Quick script to apply config.py settings to the single root .env file
Run this after modifying config.py
"""
import os
import sys
from pathlib import Path

# Ensure this works no matter where it's launched from (double-click, etc.)
project_root = Path(__file__).resolve().parent.parent
os.chdir(project_root)
sys.path.insert(0, str(project_root))

from config import generate_env_files  # noqa: E402

if __name__ == "__main__":
    # Avoid Windows console encoding issues (e.g., cp1252) causing UnicodeEncodeError.
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # Python 3.7+
    except Exception:
        pass

    print("Applying configuration from config.py...\n")
    generate_env_files()


