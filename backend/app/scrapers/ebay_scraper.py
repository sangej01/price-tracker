"""
eBay-specific scraper with auction support
"""
from .base_scraper import BaseScraper
from typing import Dict, Any, Optional
from bs4 import BeautifulSoup
import logging
import asyncio
import re
from datetime import datetime

logger = logging.getLogger(__name__)


class EbayScraper(BaseScraper):
    """Custom scraper for eBay product pages with auction support"""
    
    def __init__(self, url: str, use_paid_service: bool = False):
        super().__init__(url, use_paid_service)
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

            # eBay often serves bot-check / consent / blocked pages to direct HTTP clients.
            # In those cases, price/stock parsing will be unreliable. Prefer a conservative
            # "unknown but likely in stock" rather than a false out-of-stock.
            html_l = html.lower()
            if any(token in html_l for token in [
                "captcha",
                "pardon our interruption",
                "checking your browser before you access ebay",
                "reference id:",
                "verify you are a human",
                "robot check",
                "access denied",
                "service unavailable",
                "enable javascript",
            ]):
                logger.warning(f"eBay page looks blocked/bot-checked; cannot reliably parse: {self.url}")
                return {"price": None, "in_stock": True, "currency": "USD", "image_url": None}
            
            soup = BeautifulSoup(html, 'lxml')
            
            # Extract price
            price = self._extract_price(soup)
            
            # Extract auction data first (we need this for stock check)
            auction_data = self._extract_auction_data(soup)
            
            # Check availability (pass auction data so it knows if it's an active auction)
            in_stock = self._check_stock(soup, is_auction=auction_data.get('is_auction', False))
            
            # Extract image
            image_url = self._extract_image(soup)
            
            # Detect currency
            currency = self._detect_currency(soup)
            
            logger.info(f"eBay scrape successful: ${price}, in_stock={in_stock}, image={bool(image_url)}, auction={auction_data['is_auction']}")
            
            return {
                "price": price,
                "in_stock": in_stock,
                "currency": currency,
                "image_url": image_url,
                **auction_data  # Include auction fields
            }
            
        except Exception as e:
            logger.error(f"Error scraping eBay product {self.url}: {e}")
            return {"price": None, "in_stock": False, "currency": "USD", "image_url": None}
    
    def _extract_price(self, soup) -> Optional[float]:
        """Extract price from eBay page"""
        # First, try meta tags (often present even when DOM is complex)
        meta_price_selectors = [
            ('meta', {'itemprop': 'price'}),
            ('meta', {'property': 'og:price:amount'}),
            ('meta', {'property': 'product:price:amount'}),
        ]
        for tag, attrs in meta_price_selectors:
            element = soup.find(tag, attrs)
            if element:
                price_text = element.get('content', '') or ''
                price = self.parse_price(price_text)
                if price:
                    return price

        # Try multiple eBay price selectors (additive; keep existing ones first)
        price_selectors = [
            # Classic / older layouts
            ('span', {'class': 'x-price-primary'}),
            ('div', {'class': 'x-price-primary'}),
            ('span', {'id': 'prcIsum'}),
            ('div', {'class': 'mainPrice'}),
            # Structured data
            ('span', {'itemprop': 'price'}),
        ]
        
        for tag, attrs in price_selectors:
            element = soup.find(tag, attrs)
            if element:
                price_text = element.get_text(strip=True)
                price = self.parse_price(price_text)
                if price:
                    return price

        # Newer eBay layout: price is often inside nested ux-textspans under x-price-primary
        css_selectors = [
            'div.x-price-primary span.ux-textspans',
            'span.x-price-primary span.ux-textspans',
            '[data-testid="x-price-primary"] span.ux-textspans',
            '[data-testid="x-price-primary"] span',  # fallback
        ]
        for selector in css_selectors:
            el = soup.select_one(selector)
            if el:
                price_text = el.get_text(strip=True)
                price = self.parse_price(price_text)
                if price:
                    return price
        
        return None
    
    def _check_stock(self, soup, is_auction: bool = False) -> bool:
        """Check eBay availability"""
        # Be conservative: only mark out-of-stock when we see explicit "listing ended" messaging.
        ended_phrases = [
            r"\bthis listing was ended\b",
            r"\bthis listing has ended\b",
            r"\bthe seller ended this listing\b",
            r"\bauction ended\b",
            r"\blisting ended\b",
            r"\bthis item is out of stock\b",
        ]

        overlay = soup.find('div', {'class': 'vi-overlayTitleBar'})
        if overlay:
            overlay_text = overlay.get_text(" ", strip=True)
            if overlay_text and re.search("|".join(ended_phrases), overlay_text, re.I):
                return False

        page_text = soup.get_text(" ", strip=True)
        if page_text and re.search("|".join(ended_phrases), page_text, re.I):
            return False
        
        # If it's an auction, it's "in stock" by default (unless ended above)
        if is_auction:
            return True

        # Positive signals: if we can see purchase CTAs, treat as in stock.
        add_to_cart = soup.find('a', {'id': 'atcBtn'}) or soup.find('a', {'class': 'ux-call-to-action'})
        if add_to_cart:
            return True
        
        # Check if it's an active auction (has bids or "Place bid" button)
        auction_indicators = [
            soup.find('span', string=re.compile(r'\d+\s*bid', re.I)),
            soup.find('a', string=re.compile(r'Place bid', re.I)),
            soup.find('button', string=re.compile(r'Place bid', re.I)),
        ]
        if any(indicator for indicator in auction_indicators if indicator):
            return True  # Active auction is "in stock"
        
        # Check for quantity available
        quantity = soup.find('div', {'class': 'x-quantity__availability'})
        if quantity:
            qty_text = quantity.get_text().lower()
            if 'available' in qty_text or 'in stock' in qty_text:
                return True
            # Avoid treating generic "X sold" counters as out-of-stock.
            if any(phrase in qty_text for phrase in ['sold out', 'out of stock', 'unavailable', 'no longer available']):
                return False
        
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
    
    def _extract_auction_data(self, soup) -> Dict[str, Any]:
        """Extract auction-specific data if this is an auction listing"""
        auction_data = {
            "is_auction": False,
            "bid_count": None,
            "auction_end_time": None,
            "buy_it_now_price": None,
        }
        
        try:
            # Check if this is an auction (not just Buy It Now)
            # Look for bid count indicators
            bid_count_selectors = [
                soup.find('span', {'class': 'vi-qtyS-hot-red'}),  # Hot auction
                soup.find('a', {'class': 'vi-txt-underline'}),    # Bid link
                soup.find('span', string=re.compile(r'\d+\s*bid', re.I)),
            ]
            
            for element in bid_count_selectors:
                if element:
                    text = element.get_text()
                    # Extract number of bids
                    bid_match = re.search(r'(\d+)\s*bid', text, re.I)
                    if bid_match:
                        auction_data["is_auction"] = True
                        auction_data["bid_count"] = int(bid_match.group(1))
                        break
            
            # If it's an auction, try to get end time
            if auction_data["is_auction"]:
                # Look for timer or end time text
                time_selectors = [
                    soup.find('span', {'class': 'timeMs'}),
                    soup.find('span', {'id': 'bb_tlft'}),
                    soup.find('span', {'class': 'vi-tm-left'}),
                ]
                
                logger.debug("Looking for auction end time...")
                for element in time_selectors:
                    if element:
                        time_text = element.get_text()
                        logger.debug(f"Found time element: '{time_text}'")
                        # Try to parse relative time and calculate end datetime
                        end_datetime = self._parse_time_remaining(time_text)
                        if end_datetime:
                            auction_data["auction_end_time"] = end_datetime
                            logger.debug(f"Parsed end time: {end_datetime}")
                            break
                        else:
                            logger.debug(f"Could not parse time text: '{time_text}'")
                
                if not auction_data["auction_end_time"]:
                    logger.debug("No time remaining element found on page")
            
            # Check for Buy It Now price (some auctions have both bid and BIN)
            bin_selectors = [
                soup.find('div', {'class': 'vi-buybox-binPrice'}),
                soup.find('span', string=re.compile(r'Buy It Now', re.I)),
            ]
            
            for element in bin_selectors:
                if element:
                    # Look for price near "Buy It Now"
                    parent = element.parent
                    if parent:
                        price_elem = parent.find('span', {'class': 'notranslate'})
                        if price_elem:
                            bin_price = self.parse_price(price_elem.get_text())
                            if bin_price:
                                auction_data["buy_it_now_price"] = bin_price
                                break
        
        except Exception as e:
            logger.warning(f"Error extracting auction data: {e}")
        
        return auction_data
    
    def _parse_time_remaining(self, time_text: str) -> Optional[datetime]:
        """Parse time remaining text (e.g., '2d 5h' or '3h 45m') into end datetime"""
        try:
            from datetime import datetime, timedelta
            
            # Extract days, hours, minutes, seconds
            days = hours = minutes = seconds = 0
            
            day_match = re.search(r'(\d+)d', time_text, re.I)
            if day_match:
                days = int(day_match.group(1))
            
            hour_match = re.search(r'(\d+)h', time_text, re.I)
            if hour_match:
                hours = int(hour_match.group(1))
            
            minute_match = re.search(r'(\d+)m', time_text, re.I)
            if minute_match:
                minutes = int(minute_match.group(1))
            
            second_match = re.search(r'(\d+)s', time_text, re.I)
            if second_match:
                seconds = int(second_match.group(1))
            
            # Calculate end time from now
            if days or hours or minutes or seconds:
                time_remaining = timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
                end_time = datetime.utcnow() + time_remaining
                return end_time
            
            return None
            
        except Exception as e:
            logger.warning(f"Error parsing time remaining '{time_text}': {e}")
            return None
    
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
