"""
Quick script to apply config.py settings to .env files
Run this after modifying config.py
"""
import sys
sys.path.insert(0, '.')
from config import generate_env_files

if __name__ == "__main__":
    print("🔧 Applying configuration from config.py...\n")
    generate_env_files()

