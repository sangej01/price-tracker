"""
Quick script to apply config.py settings to .env files
Run this after modifying config.py
"""
import sys
import os

# Add parent directory to path to import config
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from config import generate_env_files

if __name__ == "__main__":
    print("🔧 Applying configuration from config.py...\n")
    generate_env_files()


