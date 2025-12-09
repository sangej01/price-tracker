"""
Third-party scraping service integrations
"""
import aiohttp
import logging
from typing import Optional
from ..config import settings

logger = logging.getLogger(__name__)


class ScrapingServiceClient:
    """Client for third-party scraping services"""
    
    @staticmethod
    async def fetch_with_brightdata(url: str) -> Optional[str]:
        """
        Fetch URL using Bright Data proxy service
        Docs: https://docs.brightdata.com/
        """
        if not settings.is_brightdata_configured:
            logger.warning("Bright Data not configured, falling back to direct scraping")
            return None
        
        try:
            # Method 1: Unlocker API (recommended - API endpoint method!)
            if settings.BRIGHTDATA_API_KEY and settings.BRIGHTDATA_ZONE:
                logger.info(f"🔓 Using Bright Data Unlocker API for {url}")
                
                # Bright Data Unlocker API endpoint
                api_url = "https://api.brightdata.com/request"
                
                headers = {
                    'Authorization': f'Bearer {settings.BRIGHTDATA_API_KEY}',
                    'Content-Type': 'application/json'
                }
                
                payload = {
                    'zone': settings.BRIGHTDATA_ZONE,
                    'url': url,
                    'format': 'raw'  # Get raw HTML
                }
                
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        api_url,
                        headers=headers,
                        json=payload,
                        timeout=aiohttp.ClientTimeout(total=30)
                    ) as response:
                        if response.status == 200:
                            html = await response.text()
                            logger.info(f"✅ Bright Data Unlocker API: Successfully fetched {url}")
                            return html
                        else:
                            error_text = await response.text()
                            logger.error(f"❌ Bright Data Unlocker API: HTTP {response.status} for {url}: {error_text}")
                            return None
            
            # Method 2: Traditional proxy credentials
            elif settings.BRIGHTDATA_USERNAME and settings.BRIGHTDATA_PASSWORD:
                logger.info(f"🌐 Using Bright Data Proxy for {url}")
                
                proxy_url = f"http://{settings.BRIGHTDATA_USERNAME}:{settings.BRIGHTDATA_PASSWORD}@{settings.BRIGHTDATA_HOST}:{settings.BRIGHTDATA_PORT}"
                
                proxy_auth = aiohttp.BasicAuth(
                    settings.BRIGHTDATA_USERNAME,
                    settings.BRIGHTDATA_PASSWORD
                )
                
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        url,
                        proxy=proxy_url,
                        proxy_auth=proxy_auth,
                        timeout=aiohttp.ClientTimeout(total=settings.SCRAPING_TIMEOUT),
                        headers={
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        }
                    ) as response:
                        if response.status == 200:
                            html = await response.text()
                            logger.info(f"✅ Bright Data Proxy: Successfully fetched {url}")
                            return html
                        else:
                            logger.error(f"❌ Bright Data Proxy: HTTP {response.status} for {url}")
                            return None
                        
        except Exception as e:
            logger.error(f"❌ Bright Data error for {url}: {e}")
            return None
    
    @staticmethod
    async def fetch_url(url: str) -> Optional[str]:
        """
        Fetch URL using configured scraping service
        Falls back to direct scraping if no service configured
        """
        # Try Bright Data if configured
        if settings.is_brightdata_configured:
            logger.info(f"🌐 Using Bright Data for {url}")
            return await ScrapingServiceClient.fetch_with_brightdata(url)
        else:
            # No service configured, return None to trigger direct scraping fallback
            logger.debug(f"📡 No scraping service configured, using direct scraping for {url}")
            return None

