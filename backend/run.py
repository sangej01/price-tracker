"""
Backend server startup script that reads configuration from .env
"""
import uvicorn
from app.config import settings

if __name__ == "__main__":
    print(f"🚀 Starting Price Tracker Backend on {settings.SERVER_HOST}:{settings.SERVER_PORT}")
    
    uvicorn.run(
        "app.main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=True,
        log_level="info"
    )


