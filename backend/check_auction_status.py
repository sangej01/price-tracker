"""Quick script to check auction product status in database"""
from app.database import SessionLocal
from app.models import Product, PriceHistory

db = SessionLocal()

# Find eBay product
product = db.query(Product).filter(Product.url.like('%ebay%')).first()

if product:
    # Get latest price
    latest_price = db.query(PriceHistory).filter(
        PriceHistory.product_id == product.id
    ).order_by(PriceHistory.scraped_at.desc()).first()
    
    print(f"\n{'='*60}")
    print(f"Product: {product.name}")
    print(f"{'='*60}")
    print(f"URL: {product.url}")
    print(f"Is Auction: {product.is_auction}")
    print(f"Auction End Time: {product.auction_end_time}")
    print(f"Current Bid Count: {product.current_bid_count}")
    print(f"Buy It Now Price: ${product.buy_it_now_price if product.buy_it_now_price else 'N/A'}")
    if latest_price:
        print(f"Latest Price: ${latest_price.price}")
        print(f"Price Bid Count: {latest_price.bid_count}")
        print(f"Is Auction Active: {latest_price.is_auction_active}")
    print(f"Last Scanned: {product.last_scanned_at}")
    print(f"{'='*60}\n")
    
    print("🔍 DIAGNOSIS:")
    if not product.is_auction:
        print("❌ Product not marked as auction - eBay scraper didn't detect auction!")
        print("   Reason: Direct scraping returns incomplete HTML")
        print("   Solution: Force Bright Data for first eBay scan")
else:
    print("No eBay product found!")

db.close()

