from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import aiohttp
from bs4 import BeautifulSoup
import re
from .scraping_service import ScrapingServiceClient


class BaseScraper(ABC):
    """Base scraper class for extracting product information from websites"""

    def __init__(self, url: str):
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    async def fetch_page(self) -> Optional[str]:
        """
        Fetch the HTML content of the page
        Uses third-party service if configured, otherwise direct scraping
        """
        try:
            # Try third-party scraping service first (if configured)
            html = await ScrapingServiceClient.fetch_url(self.url)
            if html:
                return html
            
            # Fallback to direct scraping
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url, headers=self.headers, timeout=30) as response:
                    if response.status == 200:
                        return await response.text()
                    return None
        except Exception as e:
            print(f"Error fetching page {self.url}: {e}")
            return None

    def parse_price(self, price_text: str) -> Optional[float]:
        """Extract numeric price from text"""
        if not price_text:
            return None
        
        # Remove currency symbols and extract numbers
        price_text = price_text.replace(',', '').replace('$', '').replace('€', '').replace('£', '')
        match = re.search(r'(\d+\.?\d*)', price_text)
        
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                return None
        return None

    @abstractmethod
    async def scrape(self) -> Dict[str, Any]:
        """
        Scrape product information from the URL
        Returns dict with keys: price, in_stock, currency, product_name (optional)
        """
        pass


class GenericScraper(BaseScraper):
    """Generic scraper that attempts to find price information using common patterns"""

    async def scrape(self) -> Dict[str, Any]:
        html = await self.fetch_page()
        if not html:
            return {"price": None, "in_stock": False, "currency": "USD"}

        soup = BeautifulSoup(html, 'lxml')
        
        # Common price selectors
        price_selectors = [
            {'name': 'span', 'class': 'price'},
            {'name': 'span', 'class': 'a-price-whole'},  # Amazon
            {'name': 'span', 'itemprop': 'price'},
            {'name': 'div', 'class': 'price'},
            {'name': 'span', 'class': 'product-price'},
            {'name': 'span', 'class': 'sale-price'},
            {'name': 'meta', 'property': 'product:price:amount'},
        ]

        price = None
        for selector in price_selectors:
            element = soup.find(**selector)
            if element:
                if element.name == 'meta':
                    price_text = element.get('content', '')
                else:
                    price_text = element.get_text(strip=True)
                
                price = self.parse_price(price_text)
                if price:
                    break

        # Check stock status
        in_stock = True
        out_of_stock_patterns = ['out of stock', 'unavailable', 'sold out', 'not available']
        page_text = soup.get_text().lower()
        
        for pattern in out_of_stock_patterns:
            if pattern in page_text:
                in_stock = False
                break

        return {
            "price": price,
            "in_stock": in_stock,
            "currency": "USD"
        }


