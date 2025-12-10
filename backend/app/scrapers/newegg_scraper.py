"""
Newegg-specific scraper
NOTE: Newegg has strong anti-scraping measures. Consider using API or different vendor.
"""
from .base_scraper import BaseScraper
from typing import Dict, Any
from bs4 import BeautifulSoup
import logging
import asyncio
import json
import re

logger = logging.getLogger(__name__)


class NeweggScraper(BaseScraper):
    """Custom scraper for Newegg product pages"""
    
    def __init__(self, url: str):
        super().__init__(url)
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
            
            # Try JSON-LD data first (most reliable)
            price = self._extract_price_from_json(soup, html)
            
            # Fallback to HTML extraction if JSON fails
            if not price:
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
    
    def _extract_price_from_json(self, soup, html: str) -> float:
        """Extract price from JSON-LD structured data (most reliable)"""
        try:
            # Look for JSON-LD script tags
            json_scripts = soup.find_all('script', type='application/ld+json')
            for script in json_scripts:
                try:
                    data = json.loads(script.string)
                    
                    # Handle single object or array
                    if isinstance(data, list):
                        data = data[0] if data else {}
                    
                    # Look for Product schema
                    if data.get('@type') == 'Product':
                        offers = data.get('offers', {})
                        if isinstance(offers, dict):
                            price_str = offers.get('price')
                            if price_str:
                                price = self.parse_price(str(price_str))
                                if price:
                                    logger.info(f"Found price in JSON-LD: ${price}")
                                    return price
                except (json.JSONDecodeError, AttributeError, KeyError) as e:
                    continue
            
            # Try to find price in JavaScript variables
            price_patterns = [
                r'"price":\s*"?([0-9,]+\.?[0-9]*)"?',
                r'product_price[\'"]?\s*:\s*[\'"]?([0-9,]+\.?[0-9]*)',
                r'"selling_price":\s*([0-9,]+\.?[0-9]*)',
            ]
            
            for pattern in price_patterns:
                matches = re.findall(pattern, html)
                if matches:
                    # Get the highest price (likely the main product, not addon)
                    prices = []
                    for match in matches:
                        price = self.parse_price(match)
                        if price and price > 100:  # Filter out likely addon prices
                            prices.append(price)
                    
                    if prices:
                        # Sort and get highest (main product usually most expensive)
                        prices.sort(reverse=True)
                        logger.info(f"Found price in JavaScript: ${prices[0]} (from {len(prices)} candidates)")
                        return prices[0]
        
        except Exception as e:
            logger.warning(f"Error extracting price from JSON: {e}")
        
        return None
    
    def _extract_price(self, soup) -> float:
        """Extract price from Newegg page - prioritize main product price over ads"""
        
        # Strategy 1: Look for price in the main product info section (avoid sponsored ads)
        # Newegg typically has product-buy-box or product-wrap for the actual product
        product_section = soup.find('div', {'class': ['product-buy-box', 'product-wrap', 'product-pane']})
        
        if product_section:
            # Look for price-current within the product section
            price_element = product_section.find('li', {'class': 'price-current'})
            if price_element:
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
                        logger.info(f"Found price in product section: ${price}")
                        return price
        
        # Strategy 2: Find ALL price-current elements, skip the first one (likely ad)
        all_prices = soup.find_all('li', {'class': 'price-current'})
        logger.info(f"Found {len(all_prices)} price elements total")
        
        # If we have multiple prices, the first is often a sponsored ad, try the second
        if len(all_prices) > 1:
            for idx, price_element in enumerate(all_prices[1:], 1):  # Skip first one
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
                        logger.info(f"Found price at index {idx}: ${price}")
                        return price
        
        # Strategy 3: Last resort - first price element (original behavior)
        if len(all_prices) > 0:
            price_element = all_prices[0]
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
                    logger.warning(f"Using first price (may be ad): ${price}")
                    return price
        
        # Fallback to general price class
        price_element = soup.find('span', {'class': 'price'})
        if price_element:
            return self.parse_price(price_element.get_text(strip=True))
        
        logger.warning("No price found on Newegg page")
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

