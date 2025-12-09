"""
eBay-specific scraper
"""
from .base_scraper import BaseScraper
from typing import Dict, Any
from bs4 import BeautifulSoup
import logging
import asyncio

logger = logging.getLogger(__name__)


class EbayScraper(BaseScraper):
    """Custom scraper for eBay product pages"""
    
    def __init__(self, url: str):
        super().__init__(url)
        # eBay-specific headers
        self.headers.update({
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        })
    
    async def scrape(self) -> Dict[str, Any]:
        """
        Scrape eBay product page
        Returns: dict with price, in_stock, currency, image_url
        """
        try:
            # Add delay to avoid rate limiting
            await asyncio.sleep(1)
            
            html = await self.fetch_page()
            if not html:
                logger.warning(f"Failed to fetch eBay page: {self.url}")
                return {"price": None, "in_stock": False, "currency": "USD", "image_url": None}
            
            soup = BeautifulSoup(html, 'lxml')
            
            # Extract price
            price = self._extract_price(soup)
            
            # Check availability
            in_stock = self._check_stock(soup)
            
            # Extract image
            image_url = self._extract_image(soup)
            
            # Detect currency
            currency = self._detect_currency(soup)
            
            logger.info(f"eBay scrape successful: ${price}, in_stock={in_stock}, image={bool(image_url)}")
            
            return {
                "price": price,
                "in_stock": in_stock,
                "currency": currency,
                "image_url": image_url
            }
            
        except Exception as e:
            logger.error(f"Error scraping eBay product {self.url}: {e}")
            return {"price": None, "in_stock": False, "currency": "USD", "image_url": None}
    
    def _extract_price(self, soup) -> float:
        """Extract price from eBay page"""
        # Try multiple eBay price selectors
        price_selectors = [
            # Buy It Now price
            ('span', {'class': 'x-price-primary'}),
            ('div', {'class': 'x-price-primary'}),
            # Auction current bid
            ('span', {'id': 'prcIsum'}),
            # Alternative price locations
            ('span', {'itemprop': 'price'}),
            ('div', {'class': 'mainPrice'}),
        ]
        
        for tag, attrs in price_selectors:
            element = soup.find(tag, attrs)
            if element:
                price_text = element.get_text(strip=True)
                price = self.parse_price(price_text)
                if price:
                    return price
        
        return None
    
    def _check_stock(self, soup) -> bool:
        """Check eBay availability"""
        # Check for out of stock indicators
        availability_indicators = [
            soup.find('div', {'class': 'vi-overlayTitleBar'}),
            soup.find('span', string=lambda s: s and 'ended' in s.lower()),
            soup.find('span', string=lambda s: s and 'sold' in s.lower()),
        ]
        
        # If any "ended" or "sold out" indicator exists
        if any(indicator for indicator in availability_indicators if indicator):
            return False
        
        # Check for quantity available
        quantity = soup.find('div', {'class': 'x-quantity__availability'})
        if quantity:
            qty_text = quantity.get_text().lower()
            if 'available' in qty_text or 'in stock' in qty_text:
                return True
            if 'sold' in qty_text or 'unavailable' in qty_text:
                return False
        
        # Check for "Add to cart" button (usually means in stock)
        add_to_cart = soup.find('a', {'id': 'atcBtn'}) or soup.find('a', {'class': 'ux-call-to-action'})
        if add_to_cart:
            return True
        
        # Default to True if we can't determine
        return True
    
    def _detect_currency(self, soup) -> str:
        """Detect currency from eBay page"""
        # Look for currency symbol or code
        price_element = soup.find('span', {'class': 'x-price-primary'})
        if price_element:
            price_text = price_element.get_text()
            if '$' in price_text or 'USD' in price_text:
                return 'USD'
            elif '£' in price_text or 'GBP' in price_text:
                return 'GBP'
            elif '€' in price_text or 'EUR' in price_text:
                return 'EUR'
        
        # Default to USD
        return 'USD'
    
    def _extract_image(self, soup) -> str:
        """Extract product image URL from eBay page"""
        # Try multiple image selectors
        image_selectors = [
            # Main product image
            ('img', {'id': 'icImg'}),
            # Alternative main image
            ('img', {'class': 'vi-image-gallery__image'}),
            # Responsive image
            ('img', {'class': 'img img500'}),
        ]
        
        for tag, attrs in image_selectors:
            element = soup.find(tag, attrs)
            if element:
                # Try src attribute
                img_url = element.get('src')
                if img_url and 'ebayimg.com' in img_url:
                    # eBay sometimes uses small thumbnails in src, look for high-res in data attributes
                    data_zoom = element.get('data-zoom-src')
                    if data_zoom:
                        return data_zoom
                    return img_url
        
        return None
