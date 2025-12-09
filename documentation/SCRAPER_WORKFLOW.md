# Scraper System Workflow

## Visual Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER ADDS PRODUCT                        │
│                   (e.g., Amazon product URL)                    │
└────────────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                      PRODUCT SAVED TO DB                        │
│                   (with URL and scan frequency)                 │
└────────────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                     SCHEDULER RUNS (15 min)                     │
│               Checks which products need scanning               │
└────────────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PRICE SCANNER SERVICE                        │
│              Loops through products due for scan                │
└────────────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                      SCRAPER FACTORY                            │
│            Analyzes URL → Selects Scraper                       │
│                                                                 │
│  amazon.com     → AmazonScraper                                 │
│  ebay.com       → EbayScraper                                   │
│  newegg.com     → NeweggScraper                                 │
│  other sites    → GenericScraper                                │
└────────────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                     SELECTED SCRAPER                            │
│                                                                 │
│  1. fetch_page()  → Get HTML from website                       │
│  2. parse HTML    → Extract price & stock                       │
│  3. return data   → {price, in_stock, currency}                 │
└────────────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                   SAVE TO PRICE HISTORY                         │
│            (timestamp, price, stock status)                     │
└────────────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                    UPDATE DASHBOARD                             │
│        User sees latest price, trends, statistics              │
└─────────────────────────────────────────────────────────────────┘
```

## Code Flow

### 1. Scheduler Triggers Scan
```python
# backend/app/scheduler.py
def scan_prices_job():
    result = PriceScannerService.scan_all_due_products(db)
```

### 2. Scanner Service Gets Products
```python
# backend/app/services/price_scanner.py
async def scan_product(product, db):
    result = await ScraperFactory.scrape_url(product.url)
    # Save to database
```

### 3. Factory Selects Scraper
```python
# backend/app/scrapers/scraper_factory.py
def create_scraper(url):
    domain = urlparse(url).netloc
    
    if 'amazon.com' in domain:
        return AmazonScraper(url)
    elif 'ebay.com' in domain:
        return EbayScraper(url)
    # etc...
    
    return GenericScraper(url)
```

### 4. Scraper Extracts Data
```python
# backend/app/scrapers/amazon_scraper.py
async def scrape(self):
    html = await self.fetch_page()
    soup = BeautifulSoup(html, 'lxml')
    
    price = self._extract_price(soup)
    in_stock = self._check_stock(soup)
    
    return {
        "price": price,
        "in_stock": in_stock,
        "currency": "USD"
    }
```

### 5. Data Saved to Database
```python
# backend/app/services/price_scanner.py
price_history = PriceHistory(
    product_id=product.id,
    price=result['price'],
    currency=result['currency'],
    in_stock=result['in_stock'],
    scraped_at=datetime.utcnow()
)
db.add(price_history)
db.commit()
```

## Data Flow Diagram

```
┌──────────┐
│ Products │ (products table)
└────┬─────┘
     │
     │ has many
     │
     ▼
┌──────────────┐
│ PriceHistory │ (price_history table)
└──────────────┘
     │
     │ Each record contains:
     │ - product_id
     │ - price
     │ - currency
     │ - in_stock
     │ - scraped_at (timestamp)
     │
     ▼
┌──────────────┐
│  Dashboard   │ (API aggregates data)
└──────────────┘
     │
     │ Shows:
     │ - Current price
     │ - Price changes
     │ - Trend charts
     │ - Statistics
```

## Scraper Class Hierarchy

```
┌─────────────────┐
│  BaseScraper    │ (Abstract Base Class)
│                 │
│  + fetch_page() │ ← Fetches HTML
│  + parse_price()│ ← Extracts numbers from text
│  + scrape()     │ ← Abstract (must implement)
└────────┬────────┘
         │
         │ extends
         │
    ┌────┴────────────────────────────────┐
    │                                     │
    ▼                                     ▼
┌──────────────┐                 ┌─────────────────┐
│GenericScraper│                 │ Vendor-Specific │
│              │                 │    Scrapers     │
│ Uses common  │                 │                 │
│ CSS patterns │                 │ • AmazonScraper │
└──────────────┘                 │ • EbayScraper   │
                                 │ • NeweggScraper │
                                 └─────────────────┘
```

## Adding a New Scraper (Step by Step)

```
Step 1: Create File
└─> backend/app/scrapers/walmart_scraper.py

Step 2: Write Class
└─> class WalmartScraper(BaseScraper):
        async def scrape(self): ...

Step 3: Import in Factory
└─> backend/app/scrapers/scraper_factory.py
    from .walmart_scraper import WalmartScraper

Step 4: Register Domain
└─> elif 'walmart.com' in domain:
        return WalmartScraper(url)

Step 5: Test
└─> python test_scraper.py https://walmart.com/product

Step 6: Use Automatically
└─> System now auto-selects WalmartScraper
    for all walmart.com URLs!
```

## Request Flow (Detailed)

```
User clicks "Scan All Products"
        │
        ▼
POST /api/scanner/scan-all
        │
        ▼
PriceScannerService.scan_all_due_products()
        │
        ├─> Get all active products from DB
        │
        ├─> Filter products due for scan
        │   (based on last_scanned_at + scan_frequency)
        │
        └─> For each product:
                │
                ├─> ScraperFactory.scrape_url(product.url)
                │       │
                │       ├─> Parse domain from URL
                │       │
                │       ├─> Select scraper class
                │       │   - AmazonScraper if amazon.com
                │       │   - EbayScraper if ebay.com
                │       │   - GenericScraper otherwise
                │       │
                │       ├─> scraper.fetch_page()
                │       │   - HTTP GET request
                │       │   - Returns HTML
                │       │
                │       ├─> scraper.scrape()
                │       │   - Parse HTML with BeautifulSoup
                │       │   - Find price elements
                │       │   - Find stock status
                │       │   - Return dict
                │       │
                │       └─> Return {price, in_stock, currency}
                │
                ├─> Create PriceHistory record
                │   - product_id
                │   - price
                │   - currency
                │   - in_stock
                │   - scraped_at (now)
                │
                ├─> Update product.last_scanned_at
                │
                └─> Save to database
```

## Error Handling Flow

```
Try to scrape product
        │
        ├─ HTTP Error (403, 404, etc.)
        │   └─> Log warning
        │       └─> Return {price: None, in_stock: False}
        │
        ├─ Parsing Error (element not found)
        │   └─> Try fallback selectors
        │       ├─> Success? → Return data
        │       └─> Fail? → Return defaults
        │
        ├─ Timeout
        │   └─> Log error
        │       └─> Return defaults
        │
        └─ Any other exception
            └─> Log error with traceback
                └─> Return defaults
                    └─> Continue with next product
```

## Configuration Points

### Scan Frequency
```python
# Per-product setting (default: 60 minutes)
product.scan_frequency_minutes = 120  # Check every 2 hours
```

### Global Scheduler
```python
# backend/app/scheduler.py
# Check for due products every 15 minutes
scheduler.add_job(
    scan_prices_job,
    trigger=IntervalTrigger(minutes=15),
    ...
)
```

### Rate Limiting (BaseScraper)
```python
# Minimum delay between requests to same domain
_min_delay = 2  # seconds
```

## Performance Optimization

```
Sequential Scanning
├─ Product 1 → Scrape → Save
├─ Product 2 → Scrape → Save
├─ Product 3 → Scrape → Save
└─ Takes: N × (scrape_time + save_time)

Concurrent Scanning (Current Implementation)
├─ Product 1 ┐
├─ Product 2 ├─ All scrape concurrently
├─ Product 3 ┘
└─ Takes: max(scrape_time) + save_time

Benefits:
• Faster total scan time
• Better resource utilization
• Still respects rate limits per domain
```

## Maintenance Checklist

```
Weekly:
□ Check for scraper failures in logs
□ Test a few products manually

Monthly:
□ Review which scrapers are most used
□ Update selectors if sites changed
□ Add new vendor scrapers if needed

When Adding Products:
□ Test URL with test_scraper.py first
□ Verify price and stock detection
□ Adjust scan frequency as needed
```

---

This workflow ensures accurate, reliable price tracking across multiple vendors! 🚀

