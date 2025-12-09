# Custom Scrapers Guide

## Overview

The Price Tracker uses a **generic scraper** by default that works with many standard e-commerce sites. However, for better accuracy and reliability, you can create **vendor-specific scrapers** for individual websites.

## Architecture

### Current Structure

```
backend/app/scrapers/
├── base_scraper.py        # Abstract base class with common functionality
├── scraper_factory.py     # Factory pattern to select appropriate scraper
└── [your_scrapers_here]   # Add your custom scrapers here
```

### How It Works

1. **User adds product URL** → System extracts domain from URL
2. **Factory checks domain** → Selects appropriate scraper
3. **Scraper runs** → Extracts price, stock status, currency
4. **Data saved** → Stored in database with timestamp

## Creating a Custom Scraper

### Step 1: Create Your Scraper Class

Create a new file in `backend/app/scrapers/` (e.g., `amazon_scraper.py`):

```python
from .base_scraper import BaseScraper
from typing import Dict, Any


class AmazonScraper(BaseScraper):
    """Custom scraper for Amazon.com products"""
    
    async def scrape(self) -> Dict[str, Any]:
        """
        Scrape Amazon product page
        Returns: dict with price, in_stock, currency, product_name (optional)
        """
        html = await self.fetch_page()
        if not html:
            return {"price": None, "in_stock": False, "currency": "USD"}
        
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'lxml')
        
        # Extract price - Amazon has specific price elements
        price = None
        
        # Try multiple Amazon price selectors
        price_selectors = [
            # Whole price + fraction
            {'class': 'a-price-whole'},
            # Sale price
            {'id': 'priceblock_saleprice'},
            # Deal price
            {'id': 'priceblock_dealprice'},
            # Our price
            {'id': 'priceblock_ourprice'},
            # Buy box price
            {'class': 'a-price'},
        ]
        
        for selector in price_selectors:
            element = soup.find('span', selector)
            if element:
                price_text = element.get_text(strip=True)
                price = self.parse_price(price_text)
                if price:
                    break
        
        # Check stock status
        in_stock = True
        
        # Amazon availability element
        availability = soup.find('div', {'id': 'availability'})
        if availability:
            avail_text = availability.get_text().lower()
            if any(phrase in avail_text for phrase in ['out of stock', 'unavailable', 'currently unavailable']):
                in_stock = False
        
        # Extract product name (optional but useful)
        product_name = None
        title_elem = soup.find('span', {'id': 'productTitle'})
        if title_elem:
            product_name = title_elem.get_text(strip=True)
        
        return {
            "price": price,
            "in_stock": in_stock,
            "currency": "USD",
            "product_name": product_name  # Optional
        }
```

### Step 2: Register Your Scraper in Factory

Edit `backend/app/scrapers/scraper_factory.py`:

```python
from typing import Dict, Any
from urllib.parse import urlparse
from .base_scraper import GenericScraper
from .amazon_scraper import AmazonScraper  # Import your scraper


class ScraperFactory:
    """Factory to create appropriate scraper based on domain"""

    @staticmethod
    def create_scraper(url: str):
        """
        Create a scraper instance based on the URL domain
        """
        domain = urlparse(url).netloc.lower()
        
        # Add domain-specific scrapers here
        if 'amazon.com' in domain or 'amazon.co.uk' in domain:
            return AmazonScraper(url)
        elif 'ebay.com' in domain:
            return EbayScraper(url)
        elif 'newegg.com' in domain:
            return NeweggScraper(url)
        # Add more scrapers as needed
        
        # Default to generic scraper
        return GenericScraper(url)

    @staticmethod
    async def scrape_url(url: str) -> Dict[str, Any]:
        """Convenience method to scrape a URL"""
        scraper = ScraperFactory.create_scraper(url)
        return await scraper.scrape()
```

## Example Scrapers

### Example 1: eBay Scraper

```python
# backend/app/scrapers/ebay_scraper.py
from .base_scraper import BaseScraper
from typing import Dict, Any
from bs4 import BeautifulSoup


class EbayScraper(BaseScraper):
    """Custom scraper for eBay"""
    
    async def scrape(self) -> Dict[str, Any]:
        html = await self.fetch_page()
        if not html:
            return {"price": None, "in_stock": False, "currency": "USD"}
        
        soup = BeautifulSoup(html, 'lxml')
        
        # eBay price selectors
        price = None
        price_element = soup.find('span', {'itemprop': 'price'}) or \
                       soup.find('span', {'class': 'x-price-primary'})
        
        if price_element:
            price = self.parse_price(price_element.get_text(strip=True))
        
        # eBay stock check
        in_stock = True
        quantity = soup.find('span', {'class': 'qtyTxt'})
        if quantity and 'sold' in quantity.get_text().lower():
            in_stock = False
        
        return {
            "price": price,
            "in_stock": in_stock,
            "currency": "USD"
        }
```

### Example 2: Newegg Scraper

```python
# backend/app/scrapers/newegg_scraper.py
from .base_scraper import BaseScraper
from typing import Dict, Any
from bs4 import BeautifulSoup


class NeweggScraper(BaseScraper):
    """Custom scraper for Newegg"""
    
    async def scrape(self) -> Dict[str, Any]:
        html = await self.fetch_page()
        if not html:
            return {"price": None, "in_stock": False, "currency": "USD"}
        
        soup = BeautifulSoup(html, 'lxml')
        
        # Newegg price
        price = None
        price_element = soup.find('li', {'class': 'price-current'})
        if price_element:
            # Newegg often splits dollars and cents
            dollars = price_element.find('strong')
            cents = price_element.find('sup')
            if dollars:
                price_text = dollars.get_text(strip=True)
                if cents:
                    price_text += '.' + cents.get_text(strip=True)
                price = self.parse_price(price_text)
        
        # Stock status
        in_stock = True
        stock_element = soup.find('div', {'class': 'product-inventory'})
        if stock_element:
            stock_text = stock_element.get_text().lower()
            if 'out of stock' in stock_text or 'sold out' in stock_text:
                in_stock = False
        
        return {
            "price": price,
            "in_stock": in_stock,
            "currency": "USD"
        }
```

## Finding the Right Selectors

### Method 1: Browser Developer Tools (Recommended)

1. **Open the product page** in your browser
2. **Right-click on the price** → "Inspect" or "Inspect Element"
3. **Look at the HTML structure**:
   ```html
   <span class="price-current">$299.99</span>
   ```
4. **Note the element type and attributes**: `span` with class `price-current`

### Method 2: View Page Source

1. Right-click page → "View Page Source"
2. Search (Ctrl+F) for the price value
3. Find the surrounding HTML structure

### Common Price Selectors by Platform

```python
# Amazon
{'class': 'a-price-whole'}
{'id': 'priceblock_ourprice'}
{'class': 'a-price'}

# eBay
{'itemprop': 'price'}
{'class': 'x-price-primary'}

# Newegg
{'class': 'price-current'}

# Best Buy
{'class': 'priceView-customer-price'}

# Walmart
{'class': 'price-characteristic'}
{'itemprop': 'price'}

# Target
{'data-test': 'product-price'}
```

### Common Stock Status Patterns

```python
# Text patterns to check for out of stock
out_of_stock_patterns = [
    'out of stock',
    'currently unavailable',
    'sold out',
    'not available',
    'temporarily out of stock',
    'coming soon',
    'pre-order'
]

# Check availability
availability_div = soup.find('div', {'id': 'availability'})
if availability_div:
    text = availability_div.get_text().lower()
    in_stock = not any(pattern in text for pattern in out_of_stock_patterns)
```

## Advanced Techniques

### Handling JavaScript-Rendered Pages

Some sites render prices with JavaScript. For these sites, use commercial scraping services that handle JavaScript automatically:

**Recommended Approach:**
```env
# backend/.env
SCRAPING_SERVICE=brightdata
BRIGHTDATA_API_KEY=your_api_key
BRIGHTDATA_ZONE=your_zone_name
```

The `BaseScraper.fetch_page()` method automatically uses the configured service. No code changes needed in your scraper!

**How it works:**
- Bright Data/ScraperAPI render JavaScript automatically
- Returns fully-rendered HTML to your scraper
- Handles CAPTCHAs and anti-bot protection
- See [SCRAPING_SERVICES_GUIDE.md](SCRAPING_SERVICES_GUIDE.md) for setup

### Handling Multiple Currencies

```python
def detect_currency(self, soup) -> str:
    """Detect currency from page"""
    # Check meta tags
    currency_meta = soup.find('meta', {'property': 'product:price:currency'})
    if currency_meta:
        return currency_meta.get('content', 'USD')
    
    # Check common currency symbols
    price_text = soup.get_text()
    if '£' in price_text:
        return 'GBP'
    elif '€' in price_text:
        return 'EUR'
    elif '$' in price_text:
        return 'USD'
    
    return 'USD'
```

### Handling Price Ranges

```python
def parse_price_range(self, price_text: str) -> float:
    """Handle price ranges like '$10 - $20' - return lowest"""
    import re
    prices = re.findall(r'\d+\.?\d*', price_text)
    if prices:
        # Return the lowest price in range
        return min(float(p) for p in prices)
    return None
```

## Testing Your Scraper

### Manual Test Script

Create `backend/test_scraper.py`:

```python
import asyncio
from app.scrapers.scraper_factory import ScraperFactory


async def test_scraper():
    # Test URL
    url = "https://www.amazon.com/dp/B08N5WRWNW"
    
    print(f"Testing scraper for: {url}\n")
    
    result = await ScraperFactory.scrape_url(url)
    
    print("Results:")
    print(f"  Price: ${result['price']}" if result['price'] else "  Price: Not found")
    print(f"  In Stock: {result['in_stock']}")
    print(f"  Currency: {result['currency']}")
    if 'product_name' in result:
        print(f"  Product: {result['product_name']}")


if __name__ == "__main__":
    asyncio.run(test_scraper())
```

Run it:
```bash
cd backend
python test_scraper.py
```

## Troubleshooting

### Issue: Price Not Found

**Solutions:**
1. Verify selectors are correct (inspect page source)
2. Check if page requires JavaScript (use commercial scraping service)
3. Add more fallback selectors
4. Check for geographic restrictions

### Issue: Getting Blocked

**Solutions:**
1. Add delays between requests:
   ```python
   await asyncio.sleep(2)  # Wait 2 seconds
   ```

2. Rotate user agents:
   ```python
   import random
   
   user_agents = [
       'Mozilla/5.0 (Windows NT 10.0; Win64; x64)...',
       'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...',
   ]
   
   self.headers['User-Agent'] = random.choice(user_agents)
   ```

3. Use proxies (advanced):
   ```python
   proxy = 'http://proxy-server:port'
   async with session.get(self.url, headers=self.headers, proxy=proxy) as response:
       ...
   ```

### Issue: Incorrect Price Parsing

**Debug the parse function:**
```python
price_text = element.get_text(strip=True)
print(f"Raw price text: '{price_text}'")

price = self.parse_price(price_text)
print(f"Parsed price: {price}")
```

## Best Practices

### ✅ DO:
- Always handle exceptions gracefully
- Return default values if scraping fails
- Add logging for debugging
- Test with multiple product URLs
- Respect robots.txt
- Add reasonable delays between requests

### ❌ DON'T:
- Scrape too frequently (causes blocking)
- Ignore terms of service
- Store sensitive data
- Make synchronous blocking calls
- Leave debug prints in production

## Rate Limiting

Add rate limiting to avoid getting blocked:

```python
# backend/app/scrapers/base_scraper.py
import asyncio
from datetime import datetime

class BaseScraper:
    _last_request_time = {}
    _min_delay = 2  # Minimum seconds between requests to same domain
    
    async def fetch_page(self) -> str:
        domain = urlparse(self.url).netloc
        
        # Rate limiting
        if domain in self._last_request_time:
            elapsed = (datetime.now() - self._last_request_time[domain]).total_seconds()
            if elapsed < self._min_delay:
                await asyncio.sleep(self._min_delay - elapsed)
        
        # Make request
        html = await self._fetch()
        self._last_request_time[domain] = datetime.now()
        return html
```

## Example: Complete Production-Ready Scraper

```python
# backend/app/scrapers/amazon_scraper.py
from .base_scraper import BaseScraper
from typing import Dict, Any
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)


class AmazonScraper(BaseScraper):
    """Production-ready Amazon scraper"""
    
    def __init__(self, url: str):
        super().__init__(url)
        # Amazon-specific headers
        self.headers.update({
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml',
        })
    
    async def scrape(self) -> Dict[str, Any]:
        """Scrape Amazon product page with comprehensive error handling"""
        try:
            html = await self.fetch_page()
            if not html:
                logger.warning(f"Failed to fetch page: {self.url}")
                return self._default_result()
            
            soup = BeautifulSoup(html, 'lxml')
            
            # Extract data
            price = self._extract_price(soup)
            in_stock = self._check_stock(soup)
            currency = self._detect_currency(soup)
            
            logger.info(f"Successfully scraped {self.url}: ${price}")
            
            return {
                "price": price,
                "in_stock": in_stock,
                "currency": currency
            }
            
        except Exception as e:
            logger.error(f"Error scraping {self.url}: {e}")
            return self._default_result()
    
    def _extract_price(self, soup) -> float:
        """Extract price with multiple fallbacks"""
        selectors = [
            ('span', {'class': 'a-price-whole'}),
            ('span', {'id': 'priceblock_ourprice'}),
            ('span', {'id': 'priceblock_dealprice'}),
            ('span', {'class': 'a-price'}),
        ]
        
        for tag, attrs in selectors:
            element = soup.find(tag, attrs)
            if element:
                price = self.parse_price(element.get_text(strip=True))
                if price:
                    return price
        
        return None
    
    def _check_stock(self, soup) -> bool:
        """Check stock availability"""
        availability = soup.find('div', {'id': 'availability'})
        if availability:
            text = availability.get_text().lower()
            return 'in stock' in text or 'available' in text
        return True  # Default to in stock if can't determine
    
    def _detect_currency(self, soup) -> str:
        """Detect currency from page"""
        # Check if it's a different Amazon domain
        if '.co.uk' in self.url:
            return 'GBP'
        elif '.de' in self.url or '.fr' in self.url:
            return 'EUR'
        return 'USD'
    
    def _default_result(self) -> Dict[str, Any]:
        """Return default result on failure"""
        return {
            "price": None,
            "in_stock": False,
            "currency": "USD"
        }
```

## Deployment Checklist

Before deploying custom scrapers:

- [ ] Test with at least 5 different product URLs
- [ ] Handle all edge cases (sold out, price not found, etc.)
- [ ] Add proper logging
- [ ] Implement rate limiting
- [ ] Add error handling
- [ ] Test in production-like environment
- [ ] Document any special requirements
- [ ] Add monitoring for scraper failures

## Resources

- **BeautifulSoup Documentation**: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
- **Bright Data**: https://brightdata.com/ (commercial scraping service)
- **ScraperAPI**: https://www.scraperapi.com/ (commercial scraping service)
- **CSS Selectors Reference**: https://www.w3schools.com/cssref/css_selectors.asp
- **Chrome DevTools**: https://developer.chrome.com/docs/devtools/

## Getting Help

If you encounter issues:

1. Check the console logs for error messages
2. Test the scraper manually with `test_scraper.py`
3. Verify selectors haven't changed (websites update frequently)
4. Check if the website has anti-scraping measures
5. Consider using commercial scraping services for complex/protected sites
   - See [SCRAPING_SERVICES_GUIDE.md](SCRAPING_SERVICES_GUIDE.md)

---

**Happy Scraping! 🚀**

