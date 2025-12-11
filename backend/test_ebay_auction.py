"""
Quick test to see what the eBay scraper detects
"""
import asyncio
from app.scrapers.ebay_scraper import EbayScraper
from app.database import SessionLocal
from app.models import Product

async def test_auction():
    # Get the eBay product from database
    db = SessionLocal()
    products = db.query(Product).all()
    
    print("Products in database:")
    for p in products:
        print(f"{p.id}: {p.name} - {p.url[:50]}...")
    
    # Find eBay product - look for the auction (item 366042770374)
    ebay_product = None
    for p in products:
        if 'ebay.com' in p.url.lower() and '366042770374' in p.url:
            ebay_product = p
            break
    
    # If not found, just get any eBay product
    if not ebay_product:
        for p in products:
            if 'ebay.com' in p.url.lower():
                ebay_product = p
                break
    
    if not ebay_product:
        print("\nNo eBay product found!")
        db.close()
        return
    
    print(f"\n{'='*60}")
    print(f"Testing: {ebay_product.name}")
    print(f"URL: {ebay_product.url}")
    print(f"{'='*60}\n")
    
    # Scrape it
    scraper = EbayScraper(ebay_product.url)
    result = await scraper.scrape()
    
    print("Scraping results:")
    print(f"  Price: ${result.get('price')}")
    print(f"  In Stock: {result.get('in_stock')}")
    print(f"  Currency: {result.get('currency')}")
    print(f"  Is Auction: {result.get('is_auction')}")
    print(f"  Bid Count: {result.get('bid_count')}")
    print(f"  Auction End: {result.get('auction_end_time')}")
    print(f"  Buy It Now: ${result.get('buy_it_now_price')}")
    print(f"  Image URL: {result.get('image_url')[:60] if result.get('image_url') else None}...")
    
    db.close()

if __name__ == "__main__":
    asyncio.run(test_auction())

