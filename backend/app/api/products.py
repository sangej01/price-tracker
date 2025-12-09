from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from urllib.parse import urlparse
from ..database import get_db
from ..models import Product
from ..schemas import ProductCreate, ProductUpdate, Product as ProductSchema
from ..services.price_scanner import PriceScannerService

router = APIRouter(prefix="/api/products", tags=["products"])


@router.get("/", response_model=List[ProductSchema])
def get_products(skip: int = 0, limit: int = 100, active_only: bool = False, db: Session = Depends(get_db)):
    """Get all products"""
    query = db.query(Product)
    if active_only:
        query = query.filter(Product.is_active == True)
    products = query.offset(skip).limit(limit).all()
    return products


@router.get("/{product_id}", response_model=ProductSchema)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get a specific product"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/", response_model=ProductSchema)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """Create a new product"""
    # Check if product URL already exists
    existing = db.query(Product).filter(Product.url == product.url).first()
    if existing:
        raise HTTPException(status_code=400, detail="Product with this URL already exists")
    
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.put("/{product_id}", response_model=ProductSchema)
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    """Update a product"""
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    update_data = product.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product


@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Delete a product"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}


@router.post("/{product_id}/scan")
async def scan_product(product_id: int, db: Session = Depends(get_db)):
    """Manually trigger a price scan for a specific product"""
    success = await PriceScannerService.force_scan_product(product_id, db)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found or scan failed")
    return {"message": "Product scanned successfully"}


@router.get("/{product_id}/scraper-info")
def get_scraper_info(product_id: int, db: Session = Depends(get_db)):
    """Get information about which scraper will be used for this product"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Determine scraper type based on URL
    from ..scrapers.scraper_factory import ScraperFactory
    scraper = ScraperFactory.create_scraper(product.url)
    scraper_name = scraper.__class__.__name__
    
    # Parse domain
    domain = urlparse(product.url).netloc
    
    # Determine if it's a vendor-specific or generic scraper
    is_optimized = scraper_name != "GenericScraper"
    
    return {
        "scraper_type": scraper_name,
        "domain": domain,
        "is_optimized": is_optimized,
        "description": _get_scraper_description(scraper_name)
    }


@router.post("/test-url")
async def test_url_scraping(url: str):
    """Test scraping a URL without adding it as a product"""
    try:
        from ..scrapers.scraper_factory import ScraperFactory
        
        # Get scraper info
        scraper = ScraperFactory.create_scraper(url)
        scraper_name = scraper.__class__.__name__
        
        # Attempt to scrape
        result = await ScraperFactory.scrape_url(url)
        
        return {
            "success": result['price'] is not None,
            "scraper_used": scraper_name,
            "price": result['price'],
            "currency": result['currency'],
            "in_stock": result['in_stock'],
            "is_optimized": scraper_name != "GenericScraper"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def _get_scraper_description(scraper_name: str) -> str:
    """Get human-readable description of scraper"""
    descriptions = {
        "AmazonScraper": "Optimized for Amazon with multi-currency support and comprehensive price detection",
        "EbayScraper": "Optimized for eBay listings with quantity tracking",
        "NeweggScraper": "Optimized for Newegg electronics with split price parsing",
        "GenericScraper": "Generic scraper using common e-commerce patterns (may be less accurate)"
    }
    return descriptions.get(scraper_name, "Unknown scraper")
