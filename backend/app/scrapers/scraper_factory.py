from typing import Dict, Any
from urllib.parse import urlparse
from .base_scraper import GenericScraper
from .amazon_scraper import AmazonScraper
from .ebay_scraper import EbayScraper
from .newegg_scraper import NeweggScraper


class ScraperFactory:
    """Factory to create appropriate scraper based on domain"""

    @staticmethod
    def create_scraper(url: str, use_paid_service: bool = False):
        """
        Create a scraper instance based on the URL domain
        Returns domain-specific scraper if available, otherwise GenericScraper
        
        Args:
            url: URL to scrape
            use_paid_service: If True, force use of paid scraping service (for initial auction scans)
        """
        domain = urlparse(url).netloc.lower()
        
        # Domain-specific scrapers for better accuracy
        if 'amazon.com' in domain or 'amazon.co' in domain:
            return AmazonScraper(url, use_paid_service)
        elif 'ebay.com' in domain or 'ebay.co' in domain:
            return EbayScraper(url, use_paid_service)
        elif 'newegg.com' in domain:
            return NeweggScraper(url, use_paid_service)
        # Add more scrapers here as needed
        
        # Default to generic scraper
        return GenericScraper(url, use_paid_service)

    @staticmethod
    async def scrape_url(url: str, use_paid_service: bool = False) -> Dict[str, Any]:
        """Convenience method to scrape a URL"""
        scraper = ScraperFactory.create_scraper(url, use_paid_service)
        return await scraper.scrape()


