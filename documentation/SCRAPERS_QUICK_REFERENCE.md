# Custom Scrapers Quick Reference

## Quick Start Checklist

1. ✅ Create scraper file in `backend/app/scrapers/`
2. ✅ Import `BaseScraper` and inherit from it
3. ✅ Implement `async def scrape()` method
4. ✅ Register in `scraper_factory.py`
5. ✅ Test with `test_scraper.py`

## Minimal Scraper Template

```python
# backend/app/scrapers/mysite_scraper.py
from .base_scraper import BaseScraper
from bs4 import BeautifulSoup

class MySiteScraper(BaseScraper):
    async def scrape(self):
        html = await self.fetch_page()
        if not html:
            return {"price": None, "in_stock": False, "currency": "USD"}
        
        soup = BeautifulSoup(html, 'lxml')
        
        # Find price
        price_elem = soup.find('span', {'class': 'price'})
        price = self.parse_price(price_elem.get_text()) if price_elem else None
        
        # Check stock
        in_stock = 'out of stock' not in soup.get_text().lower()
        
        return {"price": price, "in_stock": in_stock, "currency": "USD"}
```

## Register in Factory

```python
# backend/app/scrapers/scraper_factory.py
from .mysite_scraper import MySiteScraper

# In create_scraper method:
if 'mysite.com' in domain:
    return MySiteScraper(url)
```

## Common CSS Selectors

```python
# Find by class
soup.find('span', {'class': 'price'})

# Find by ID
soup.find('div', {'id': 'product-price'})

# Find by attribute
soup.find('span', {'itemprop': 'price'})
soup.find('meta', {'property': 'product:price'})

# Multiple classes
soup.find('span', {'class': 'price current'})

# Get attribute value
element.get('content')  # For meta tags

# Get text
element.get_text(strip=True)
```

## Common Patterns

### Multi-Currency Support

```python
def _detect_currency(self) -> str:
    if '.co.uk' in self.url:
        return 'GBP'
    elif '.de' in self.url:
        return 'EUR'
    return 'USD'
```

### Multiple Price Selectors

```python
selectors = [
    ('span', {'class': 'sale-price'}),
    ('span', {'class': 'regular-price'}),
    ('div', {'class': 'price'}),
]

for tag, attrs in selectors:
    elem = soup.find(tag, attrs)
    if elem:
        price = self.parse_price(elem.get_text())
        if price:
            return price
```

### Stock Status Checks

```python
# Method 1: Check text
text = soup.get_text().lower()
in_stock = 'in stock' in text and 'out of stock' not in text

# Method 2: Check specific element
avail = soup.find('div', {'class': 'availability'})
in_stock = 'available' in avail.get_text().lower() if avail else True

# Method 3: Check for button
button = soup.find('button', {'id': 'add-to-cart'})
in_stock = button is not None and not button.get('disabled')
```

## Testing Your Scraper

```python
# backend/test_scraper.py
import asyncio
from app.scrapers.scraper_factory import ScraperFactory

async def test():
    url = "YOUR_PRODUCT_URL_HERE"
    result = await ScraperFactory.scrape_url(url)
    print(f"Price: ${result['price']}")
    print(f"In Stock: {result['in_stock']}")

asyncio.run(test())
```

Run: `cd backend && python test_scraper.py`

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Price not found | Check selectors with browser DevTools |
| Getting 403/blocked | Add delays, rotate user agents, or use Bright Data |
| JavaScript content | Use Bright Data commercial scraping service |
| Wrong currency | Implement `_detect_currency()` method |
| Inconsistent results | Add multiple fallback selectors |

## Example Sites

### Already Implemented ✅
- Amazon (`amazon_scraper.py`)
- eBay (`ebay_scraper.py`)
- Newegg (`newegg_scraper.py`)

### To Add:
- Best Buy
- Walmart
- Target
- B&H Photo
- Micro Center

## Pro Tips

1. **Always use fallback selectors** - websites change HTML frequently
2. **Test with multiple products** - different categories may have different layouts
3. **Add logging** - helps debug issues in production
4. **Handle exceptions** - return default values on errors
5. **Respect robots.txt** - add delays between requests
6. **Check for regional variations** - Amazon US vs UK have different layouts

## More Info

See `CUSTOM_SCRAPERS_GUIDE.md` for comprehensive documentation.

