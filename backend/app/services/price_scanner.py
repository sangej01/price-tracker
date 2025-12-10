from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List
import asyncio
from ..models import Product, PriceHistory
from ..scrapers.scraper_factory import ScraperFactory


class PriceScannerService:
    """Service for scanning product prices"""

    @staticmethod
    async def scan_product(product: Product, db: Session) -> bool:
        """
        Scan a single product and save price history
        Returns True if successful, False otherwise
        """
        try:
            # Scrape the product page
            result = await ScraperFactory.scrape_url(product.url)
            
            if result['price'] is not None:
                # Create price history entry
                price_history = PriceHistory(
                    product_id=product.id,
                    price=result['price'],
                    currency=result.get('currency', 'USD'),
                    in_stock=result.get('in_stock', True),
                    scraped_at=datetime.utcnow(),
                    # Auction data (if present)
                    bid_count=result.get('bid_count'),
                    is_auction_active=result.get('is_auction', False),
                )
                db.add(price_history)
                
                # Update product's last scanned timestamp and image URL
                product.last_scanned_at = datetime.utcnow()
                
                # Update image URL if we got one
                if result.get('image_url'):
                    product.image_url = result['image_url']
                
                # Update auction fields (if it's an auction)
                if result.get('is_auction'):
                    product.is_auction = True
                    product.current_bid_count = result.get('bid_count')
                    product.buy_it_now_price = result.get('buy_it_now_price')
                    if result.get('auction_end_time'):
                        product.auction_end_time = result.get('auction_end_time')
                
                db.commit()
                
                print(f"Successfully scanned {product.name}: ${result['price']}")
                return True
            else:
                print(f"Could not extract price for {product.name}")
                return False
                
        except Exception as e:
            print(f"Error scanning product {product.name}: {e}")
            db.rollback()
            return False

    @staticmethod
    async def scan_all_due_products(db: Session, force: bool = False) -> dict:
        """
        Scan all products that are due for scanning (or all if force=True)
        Returns dict with success/failure counts
        """
        now = datetime.utcnow()
        
        # Get all active products
        products = db.query(Product).filter(
            Product.is_active == True
        ).all()

        if force:
            # Force scan all products regardless of schedule
            due_products = products
        else:
            # Only scan products that are due
            due_products = []
            for product in products:
                if product.last_scanned_at is None:
                    due_products.append(product)
                else:
                    time_since_scan = now - product.last_scanned_at
                    scan_interval = timedelta(minutes=product.scan_frequency_minutes)
                    if time_since_scan >= scan_interval:
                        due_products.append(product)

        if not due_products:
            return {"total": 0, "success": 0, "failed": 0}

        # Scan products concurrently
        results = await asyncio.gather(
            *[PriceScannerService.scan_product(product, db) for product in due_products],
            return_exceptions=True
        )

        success_count = sum(1 for r in results if r is True)
        failed_count = len(results) - success_count

        return {
            "total": len(due_products),
            "success": success_count,
            "failed": failed_count
        }

    @staticmethod
    async def force_scan_product(product_id: int, db: Session) -> bool:
        """Force scan a specific product regardless of schedule"""
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            return False
        
        return await PriceScannerService.scan_product(product, db)


