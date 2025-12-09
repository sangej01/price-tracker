"""
Central Configuration File
===========================
All user-configurable settings for the Price Tracker application.
Modify this file to customize backend and frontend behavior.
"""

# =============================================================================
# BACKEND CONFIGURATION
# =============================================================================

class BackendConfig:
    """Backend server and API configuration"""
    
    # Server Settings
    HOST = "0.0.0.0"          # Server host (0.0.0.0 = all interfaces)
    PORT = 8081               # Server port
    DEBUG = False             # Debug mode
    
    # Database
    DATABASE_URL = "sqlite:///./backend/price_tracker.db"
    
    # Scheduler
    SCAN_INTERVAL_MINUTES = 480    # How often scheduler checks for due products
    
    # Scraping Settings
    # -----------------------------------------------------------------------------
    # 💰 COST CALCULATOR (with Bright Data - $0.005 avg per request)
    # -----------------------------------------------------------------------------
    # | Scan Interval | Products | Scans/Day | Requests/Day | Daily Cost | Monthly Cost |
    # |---------------|----------|-----------|--------------|------------|--------------|
    # | Hourly        | 4        | 24        | 96           | $0.10-$0.96| $3-$29       |
    # | Every 2 hours | 4        | 12        | 48           | $0.05-$0.48| $1.50-$14    |
    # | Every 4 hours | 4        | 6         | 24           | $0.02-$0.24| $0.60-$7     |
    # | Every 15 min  | 4        | 96        | 384          | $0.38-$3.84| $11-$115     |
    # -----------------------------------------------------------------------------
    # 💡 TIP: Use direct scraping (free) when possible, Bright Data only for blocked sites
    # Example: Only eBay needs Bright Data = 1 product × 96/day = ~$14/month vs $60/month
    # -----------------------------------------------------------------------------
    
    SCRAPING_DELAY = 1.0          # Delay between requests (seconds)
    SCRAPING_TIMEOUT = 10         # Request timeout (seconds)
    
    # Commercial Scraping Service (Optional)
    # Options: "direct", "brightdata"
    SCRAPING_SERVICE = "direct"   # Default to direct scraping
    
    # Bright Data Configuration (leave empty if not using)
    BRIGHTDATA_API_KEY = ""       # Your Bright Data API key
    BRIGHTDATA_ZONE = ""          # Your zone name (e.g., "residential_proxy1")


# =============================================================================
# FRONTEND CONFIGURATION
# =============================================================================

class FrontendConfig:
    """Frontend/React application configuration"""
    
    # API Connection
    API_BASE_URL = f"http://localhost:{BackendConfig.PORT}"
    
    # Development Server
    DEV_PORT = 3000               # Frontend dev server port
    
    # UI Settings
    PRODUCTS_PER_PAGE = 20        # Pagination
    CHART_DAYS = 30              # Days of price history to show
    AUTO_REFRESH_SECONDS = 300    # Auto-refresh interval (5 minutes)


# =============================================================================
# EXPORT CONFIGURATION
# =============================================================================

# Export for easy importing
backend = BackendConfig()
frontend = FrontendConfig()

# Generate .env files
def generate_env_files():
    """Generate .env files for backend and frontend"""
    
    # Backend .env
    backend_env = f"""# Backend Configuration (Auto-generated from config.py)
SERVER_HOST={BackendConfig.HOST}
SERVER_PORT={BackendConfig.PORT}
DEBUG={str(BackendConfig.DEBUG).lower()}

DATABASE_URL={BackendConfig.DATABASE_URL}

SCAN_INTERVAL_MINUTES={BackendConfig.SCAN_INTERVAL_MINUTES}
SCRAPING_DELAY={BackendConfig.SCRAPING_DELAY}
SCRAPING_TIMEOUT={BackendConfig.SCRAPING_TIMEOUT}

SCRAPING_SERVICE={BackendConfig.SCRAPING_SERVICE}
BRIGHTDATA_API_KEY={BackendConfig.BRIGHTDATA_API_KEY}
BRIGHTDATA_ZONE={BackendConfig.BRIGHTDATA_ZONE}
"""
    
    # Frontend .env
    frontend_env = f"""# Frontend Configuration (Auto-generated from config.py)
VITE_API_BASE_URL={FrontendConfig.API_BASE_URL}
"""
    
    # Write files
    with open("backend/.env", "w") as f:
        f.write(backend_env)
    print("✅ Generated backend/.env")
    
    with open("frontend/.env", "w") as f:
        f.write(frontend_env)
    print("✅ Generated frontend/.env")
    
    print("\n📝 Configuration applied! Restart servers to use new settings.")


if __name__ == "__main__":
    print("🔧 Price Tracker Configuration")
    print("=" * 50)
    print(f"\n📡 BACKEND")
    print(f"   Host: {BackendConfig.HOST}")
    print(f"   Port: {BackendConfig.PORT}")
    print(f"   API URL: http://localhost:{BackendConfig.PORT}")
    print(f"   Scraping Service: {BackendConfig.SCRAPING_SERVICE}")
    
    print(f"\n💻 FRONTEND")
    print(f"   Dev Port: {FrontendConfig.DEV_PORT}")
    print(f"   API Connection: {FrontendConfig.API_BASE_URL}")
    
    print("\n" + "=" * 50)
    
    # Ask to generate .env files
    response = input("\nGenerate .env files from this config? (y/n): ")
    if response.lower() == 'y':
        generate_env_files()
    else:
        print("Skipped .env generation.")

