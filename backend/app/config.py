"""
Application configuration from environment variables
Loads from .env file at project root
"""
import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load .env from project root (two directories up from this file)
project_root = Path(__file__).parent.parent.parent
env_path = project_root / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    """Application settings loaded from environment variables"""
    
    # Server Configuration
    SERVER_HOST: str = os.getenv("SERVER_HOST", "0.0.0.0")
    SERVER_PORT: int = int(os.getenv("SERVER_PORT", "8081"))
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./price_tracker.db")
    
    # Scheduler
    SCAN_INTERVAL_MINUTES: int = int(os.getenv("SCAN_INTERVAL_MINUTES", "15"))
    
    # Scraping Settings
    SCRAPING_DELAY: float = float(os.getenv("SCRAPING_DELAY", "1"))
    SCRAPING_TIMEOUT: int = int(os.getenv("SCRAPING_TIMEOUT", "10"))
    
    # Scraping Service Configuration
    SCRAPING_SERVICE: str = os.getenv("SCRAPING_SERVICE", "direct").lower()
    
    # Bright Data - Unlocker API (recommended)
    BRIGHTDATA_API_KEY: Optional[str] = os.getenv("BRIGHTDATA_API_KEY")
    BRIGHTDATA_PROXY_NAME: Optional[str] = os.getenv("BRIGHTDATA_PROXY_NAME")
    
    # Bright Data - Traditional Proxy (alternative)
    BRIGHTDATA_USERNAME: Optional[str] = os.getenv("BRIGHTDATA_USERNAME")
    BRIGHTDATA_PASSWORD: Optional[str] = os.getenv("BRIGHTDATA_PASSWORD")
    BRIGHTDATA_HOST: Optional[str] = os.getenv("BRIGHTDATA_HOST")
    BRIGHTDATA_PORT: Optional[int] = int(os.getenv("BRIGHTDATA_PORT")) if os.getenv("BRIGHTDATA_PORT") else None

    # ScraperAPI (optional)
    # NOTE: This is only used if SCRAPING_SERVICE=scraperapi
    SCRAPERAPI_KEY: Optional[str] = os.getenv("SCRAPERAPI_KEY")
    
    @property
    def is_brightdata_configured(self) -> bool:
        """Check if Bright Data is properly configured"""
        if self.SCRAPING_SERVICE != "brightdata":
            return False
        
        # Method 1: Unlocker API (simpler - just API key + proxy name)
        if self.BRIGHTDATA_API_KEY and self.BRIGHTDATA_PROXY_NAME:
            return True
        
        # Method 2: Traditional proxy (username/password/host/port)
        if (self.BRIGHTDATA_USERNAME and self.BRIGHTDATA_PASSWORD 
            and self.BRIGHTDATA_HOST and self.BRIGHTDATA_PORT):
            return True
        
        return False

    @property
    def is_scraperapi_configured(self) -> bool:
        """Check if ScraperAPI is properly configured"""
        return self.SCRAPING_SERVICE == "scraperapi" and bool(self.SCRAPERAPI_KEY)


settings = Settings()

