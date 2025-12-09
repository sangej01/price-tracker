"""
Amazon-specific scraper with comprehensive price and stock detection
"""
from .base_scraper import BaseScraper
from typing import Dict, Any
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)


class AmazonScraper(BaseScraper):
    """Custom scraper optimized for Amazon product pages"""
    
    def __init__(self, url: str):
        super().__init__(url)
        # Amazon-specific headers
        self.headers.update({
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        })
    
    async def scrape(self) -> Dict[str, Any]:
        """
        Scrape Amazon product page
        Returns: dict with price, in_stock, currency, image_url
        """
        try:
            html = await self.fetch_page()
            if not html:
                logger.warning(f"Failed to fetch Amazon page: {self.url}")
                return {"price": None, "in_stock": False, "currency": "USD", "image_url": None}
            
            soup = BeautifulSoup(html, 'lxml')
            
            # Extract price
            price = self._extract_price(soup)
            
            # Check stock status
            in_stock = self._check_stock(soup)
            
            # Detect currency
            currency = self._detect_currency()
            
            # Extract image URL
            image_url = self._extract_image(soup)
            
            logger.info(f"Amazon scrape successful: ${price}, in_stock={in_stock}, image={bool(image_url)}")
            
            return {
                "price": price,
                "in_stock": in_stock,
                "currency": currency,
                "image_url": image_url
            }
            
        except Exception as e:
            logger.error(f"Error scraping Amazon product {self.url}: {e}")
            return {"price": None, "in_stock": False, "currency": "USD", "image_url": None}
    
    def _extract_price(self, soup) -> float:
        """Extract price using multiple Amazon-specific selectors"""
        # Try multiple Amazon price formats
        price_selectors = [
            # Standard price
            ('span', {'class': 'a-price-whole'}),
            # Our price
            ('span', {'id': 'priceblock_ourprice'}),
            # Deal price
            ('span', {'id': 'priceblock_dealprice'}),
            # Sale price
            ('span', {'id': 'priceblock_saleprice'}),
            # Buy box price
            ('span', {'class': 'a-price', 'data-a-size': 'xl'}),
            # Price inside buy box
            ('span', {'class': 'a-offscreen'}),
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
        """Check Amazon stock availability"""
        # Check availability div
        availability = soup.find('div', {'id': 'availability'})
        if availability:
            avail_text = availability.get_text().lower()
            
            # Out of stock indicators
            if any(phrase in avail_text for phrase in [
                'out of stock',
                'currently unavailable',
                'temporarily out of stock',
                'unavailable'
            ]):
                return False
            
            # In stock indicators
            if any(phrase in avail_text for phrase in ['in stock', 'available']):
                return True
        
        # Check for add to cart button (usually means in stock)
        add_to_cart = soup.find('input', {'id': 'add-to-cart-button'})
        if add_to_cart and not add_to_cart.get('disabled'):
            return True
        
        # Default to True if we can't determine
        return True
    
    def _detect_currency(self) -> str:
        """Detect currency based on Amazon domain"""
        if '.co.uk' in self.url:
            return 'GBP'
        elif '.ca' in self.url:
            return 'CAD'
        elif '.de' in self.url or '.fr' in self.url or '.es' in self.url or '.it' in self.url:
            return 'EUR'
        elif '.jp' in self.url:
            return 'JPY'
        elif '.au' in self.url:
            return 'AUD'
        return 'USD'
    
    def _extract_image(self, soup) -> str:
        """Extract product image URL from Amazon page"""
        # Try multiple image selectors
        image_selectors = [
            # Main product image
            ('img', {'id': 'landingImage'}),
            # Alternative main image
            ('img', {'class': 'a-dynamic-image'}),
            # Image block
            ('div', {'id': 'imgTagWrapperId'}),
        ]
        
        for tag, attrs in image_selectors:
            element = soup.find(tag, attrs)
            if element:
                # Try data-old-hires (high-res image)
                img_url = element.get('data-old-hires')
                if img_url:
                    return img_url
                
                # Try data-a-dynamic-image (JSON with multiple sizes)
                dynamic_img = element.get('data-a-dynamic-image')
                if dynamic_img:
                    try:
                        import json
                        img_dict = json.loads(dynamic_img)
                        if img_dict:
                            # Get the largest image (first one is usually biggest)
                            return list(img_dict.keys())[0]
                    except:
                        pass
                
                # Try src attribute
                img_url = element.get('src')
                if img_url and 'amazon.com' in img_url:
                    return img_url
        
        return None

