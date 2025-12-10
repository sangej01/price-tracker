from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List
from datetime import datetime, timedelta
from ..database import get_db
from ..models import Product, PriceHistory, Vendor
from ..schemas import ProductWithLatestPrice, ProductPriceStats, PriceHistory as PriceHistorySchema

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/products", response_model=List[ProductWithLatestPrice])
def get_dashboard_products(db: Session = Depends(get_db)):
    """Get all products with their latest price information for dashboard"""
    products = db.query(Product).filter(Product.is_active == True).all()
    
    result = []
    for product in products:
        # Get latest price
        latest_price = db.query(PriceHistory).filter(
            PriceHistory.product_id == product.id
        ).order_by(desc(PriceHistory.scraped_at)).first()
        
        # Get previous price for comparison
        previous_price_record = db.query(PriceHistory).filter(
            PriceHistory.product_id == product.id
        ).order_by(desc(PriceHistory.scraped_at)).offset(1).first()
        
        vendor = db.query(Vendor).filter(Vendor.id == product.vendor_id).first()
        
        current_price = latest_price.price if latest_price else None
        previous_price = previous_price_record.price if previous_price_record else None
        price_change = None
        price_change_percent = None
        
        if current_price and previous_price:
            price_change = current_price - previous_price
            price_change_percent = ((current_price - previous_price) / previous_price) * 100
        
        result.append(ProductWithLatestPrice(
            id=product.id,
            name=product.name,
            url=product.url,
            vendor_name=vendor.name if vendor else "Unknown",
            image_url=product.image_url,
            current_price=current_price,
            previous_price=previous_price,
            price_change=price_change,
            price_change_percent=price_change_percent,
            in_stock=latest_price.in_stock if latest_price else False,
            last_scanned_at=product.last_scanned_at,
            currency=latest_price.currency if latest_price else "USD",
            scan_frequency_minutes=product.scan_frequency_minutes,
            # Auction fields
            is_auction=product.is_auction if hasattr(product, 'is_auction') else False,
            auction_end_time=product.auction_end_time if hasattr(product, 'auction_end_time') else None,
            current_bid_count=product.current_bid_count if hasattr(product, 'current_bid_count') else None,
            buy_it_now_price=product.buy_it_now_price if hasattr(product, 'buy_it_now_price') else None,
        ))
    
    return result


@router.get("/products/{product_id}/stats", response_model=ProductPriceStats)
def get_product_stats(product_id: int, days: int = 30, db: Session = Depends(get_db)):
    """Get price statistics and history for a specific product"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Get price history for the specified period
    since_date = datetime.utcnow() - timedelta(days=days)
    price_history = db.query(PriceHistory).filter(
        PriceHistory.product_id == product_id,
        PriceHistory.scraped_at >= since_date
    ).order_by(PriceHistory.scraped_at).all()
    
    # Calculate statistics
    prices = [ph.price for ph in price_history if ph.price is not None]
    
    current_price = prices[-1] if prices else None
    lowest_price = min(prices) if prices else None
    highest_price = max(prices) if prices else None
    average_price = sum(prices) / len(prices) if prices else None
    
    return ProductPriceStats(
        product_id=product.id,
        product_name=product.name,
        current_price=current_price,
        lowest_price=lowest_price,
        highest_price=highest_price,
        average_price=average_price,
        price_history=[PriceHistorySchema.from_orm(ph) for ph in price_history]
    )


@router.get("/summary")
def get_dashboard_summary(db: Session = Depends(get_db)):
    """Get overall dashboard summary statistics"""
    total_products = db.query(Product).filter(Product.is_active == True).count()
    total_vendors = db.query(Vendor).filter(Vendor.is_active == True).count()
    
    # Count products with recent scans (within last 24 hours)
    since_date = datetime.utcnow() - timedelta(hours=24)
    recently_scanned = db.query(Product).filter(
        Product.is_active == True,
        Product.last_scanned_at >= since_date
    ).count()
    
    # Count total price records
    total_price_records = db.query(PriceHistory).count()
    
    return {
        "total_products": total_products,
        "total_vendors": total_vendors,
        "recently_scanned": recently_scanned,
        "total_price_records": total_price_records
    }


