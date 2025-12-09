"""
Application configuration from environment variables
"""
import os
from typing import Optional
from dotenv import load_dotenv

# Load .env file if it exists
load_dotenv()


class Settings:
    """Application settings"""
    
    # Scraping Service Configuration
    SCRAPING_SERVICE: str = os.getenv("SCRAPING_SERVICE", "direct").lower()
    
    # Bright Data - Unlocker API (simpler, recommended)
    BRIGHTDATA_API_KEY: Optional[str] = os.getenv("BRIGHTDATA_API_KEY")
    BRIGHTDATA_ZONE: Optional[str] = os.getenv("BRIGHTDATA_ZONE")  # Proxy/zone name
    
    # Bright Data - Traditional Proxy (alternative method)
    BRIGHTDATA_USERNAME: Optional[str] = os.getenv("BRIGHTDATA_USERNAME")
    BRIGHTDATA_PASSWORD: Optional[str] = os.getenv("BRIGHTDATA_PASSWORD")
    BRIGHTDATA_HOST: Optional[str] = os.getenv("BRIGHTDATA_HOST")
    BRIGHTDATA_PORT: Optional[int] = int(os.getenv("BRIGHTDATA_PORT")) if os.getenv("BRIGHTDATA_PORT") else None
    
    # Direct Scraping
    SCRAPING_DELAY: float = float(os.getenv("SCRAPING_DELAY", "1"))
    SCRAPING_TIMEOUT: int = int(os.getenv("SCRAPING_TIMEOUT", "10"))
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./price_tracker.db")
    
    # Application
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    @property
    def is_brightdata_configured(self) -> bool:
        """Check if Bright Data is properly configured"""
        if self.SCRAPING_SERVICE != "brightdata":
            return False
        
        # Method 1: Unlocker API (simpler - just API key + zone)
        if self.BRIGHTDATA_API_KEY and self.BRIGHTDATA_ZONE:
            return True
        
        # Method 2: Traditional proxy (username/password/host/port)
        if (self.BRIGHTDATA_USERNAME and self.BRIGHTDATA_PASSWORD 
            and self.BRIGHTDATA_HOST and self.BRIGHTDATA_PORT):
            return True
        
        return False


settings = Settings()

