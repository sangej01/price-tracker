"""
Backend server startup script that reads configuration from .env
"""
import sys
import uvicorn
from app.config import settings

if __name__ == "__main__":
    # Avoid Windows console encoding issues (e.g., cp1252) causing UnicodeEncodeError.
    # Prefer forcing UTF-8 if supported; fall back to ASCII-only output.
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # Python 3.7+
    except Exception:
        pass

    print(f"Starting Price Tracker Backend on {settings.SERVER_HOST}:{settings.SERVER_PORT}")
    
    uvicorn.run(
        "app.main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=True,
        log_level="info"
    )


