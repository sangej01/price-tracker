"""
Sample data seeder for quick testing
Run this after starting the backend to populate with example data
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from app.database import SessionLocal, engine, Base
from app.models import Vendor, Product


def seed_database():
    """Seed database with sample vendors and products"""
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(Vendor).count() > 0:
            print("Database already has data. Skipping seed.")
            return
        
        print("Seeding database with sample data...")
        
        # Create sample vendors
        vendors = [
            Vendor(name="Amazon", domain="amazon.com"),
            Vendor(name="Best Buy", domain="bestbuy.com"),
            Vendor(name="Walmart", domain="walmart.com"),
        ]
        
        for vendor in vendors:
            db.add(vendor)
        
        db.commit()
        print(f"Created {len(vendors)} vendors")
        
        # Create sample products (you'll need to replace these with real URLs)
        products = [
            Product(
                name="Sample Product 1",
                url="https://www.example.com/product1",
                vendor_id=1,
                description="This is a sample product for testing",
                scan_frequency_minutes=60
            ),
            Product(
                name="Sample Product 2",
                url="https://www.example.com/product2",
                vendor_id=2,
                description="Another sample product",
                scan_frequency_minutes=120
            ),
        ]
        
        for product in products:
            db.add(product)
        
        db.commit()
        print(f"Created {len(products)} products")
        
        print("\n✅ Database seeded successfully!")
        print("\nNote: Sample products have example URLs.")
        print("Please update them with real product URLs in the Products page.")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()


