"""
Newegg-specific scraper
NOTE: Newegg has strong anti-scraping measures. Consider using API or different vendor.
"""
from .base_scraper import BaseScraper
from typing import Dict, Any
from bs4 import BeautifulSoup
import logging
import asyncio

logger = logging.getLogger(__name__)


class NeweggScraper(BaseScraper):
    """Custom scraper for Newegg product pages"""
    
    def __init__(self, url: str, use_paid_service: bool = False):
        super().__init__(url, use_paid_service)
        # More realistic headers for Newegg
        self.headers.update({
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
    
    async def scrape(self) -> Dict[str, Any]:
        """
        Scrape Newegg product page
        Returns: dict with price, in_stock, currency, image_url
        """
        try:
            # Add delay to avoid rate limiting
            await asyncio.sleep(1)
            
            html = await self.fetch_page()
            if not html:
                logger.warning(f"Failed to fetch Newegg page: {self.url}")
                return {"price": None, "in_stock": False, "currency": "USD", "image_url": None}
            
            soup = BeautifulSoup(html, 'lxml')
            
            # Extract price
            price = self._extract_price(soup)
            
            # Check stock
            in_stock = self._check_stock(soup)
            
            # Extract image
            image_url = self._extract_image(soup)
            
            logger.info(f"Newegg scrape successful: ${price}, in_stock={in_stock}, image={bool(image_url)}")
            
            return {
                "price": price,
                "in_stock": in_stock,
                "currency": "USD",
                "image_url": image_url
            }
            
        except Exception as e:
            logger.error(f"Error scraping Newegg product {self.url}: {e}")
            return {"price": None, "in_stock": False, "currency": "USD", "image_url": None}
    
    def _extract_price(self, soup) -> float:
        """Extract price from Newegg page"""
        # Newegg often uses price-current class
        price_element = soup.find('li', {'class': 'price-current'})
        
        if price_element:
            # Newegg splits dollars and cents
            price_text = ""
            
            strong = price_element.find('strong')
            if strong:
                price_text = strong.get_text(strip=True)
            
            sup = price_element.find('sup')
            if sup:
                price_text += sup.get_text(strip=True)
            
            if price_text:
                price = self.parse_price(price_text)
                if price:
                    return price
        
        # Fallback to general price class
        price_element = soup.find('span', {'class': 'price'})
        if price_element:
            return self.parse_price(price_element.get_text(strip=True))
        
        return None
    
    def _check_stock(self, soup) -> bool:
        """Check Newegg stock availability"""
        # Check product inventory
        inventory = soup.find('div', {'class': 'product-inventory'})
        if inventory:
            inv_text = inventory.get_text().lower()
            if any(phrase in inv_text for phrase in ['out of stock', 'sold out', 'discontinued']):
                return False
        
        # Check for Add to Cart button
        add_button = soup.find('button', {'class': 'btn-primary', 'title': 'Add to cart'})
        if add_button:
            return True
        
        return True
    
    def _extract_image(self, soup) -> str:
        """Extract product image URL from Newegg page"""
        # Try multiple image selectors
        image_selectors = [
            # Main product image
            ('img', {'class': 'product-view-img-original'}),
            # Alternative selectors
            ('div', {'class': 'product-view-img-original'}),
            ('img', {'class': 'product-image'}),
        ]
        
        for tag, attrs in image_selectors:
            element = soup.find(tag, attrs)
            if element:
                # Try src attribute
                img_url = element.get('src')
                if img_url:
                    # If it's a relative URL, make it absolute
                    if img_url.startswith('//'):
                        img_url = 'https:' + img_url
                    elif img_url.startswith('/'):
                        img_url = 'https://www.newegg.com' + img_url
                    return img_url
        
        return None

