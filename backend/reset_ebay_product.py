"""
Utility script to reset an eBay product for testing
Deletes the product and all its price history, then recreates it fresh
"""
from app.database import SessionLocal
from app.models import Product, PriceHistory, Vendor
import sys

# ===== CONFIGURATION =====
# Edit these values to reset different eBay products
EBAY_URL = "https://www.ebay.com/itm/366042770374"
PRODUCT_NAME = "NVIDIA RTX 4000 SFF Ada 20GB"
# =========================

def reset_ebay_product():
    """Delete and recreate an eBay product"""
    db = SessionLocal()
    
    try:
        # Find the product
        product = db.query(Product).filter(Product.url == EBAY_URL).first()
        
        if product:
            print(f"\n🗑️  Found existing product: {product.name}")
            print(f"   Price history entries: {len(product.price_history)}")
            
            # Delete it (cascade will delete price history too)
            db.delete(product)
            db.commit()
            print("✅ Deleted successfully")
        else:
            print("\n⚠️  Product not found (maybe already deleted)")
        
        # Find or create eBay vendor
        ebay_vendor = db.query(Vendor).filter(Vendor.name == "eBay").first()
        if not ebay_vendor:
            ebay_vendor = Vendor(
                name="eBay",
                website="https://www.ebay.com",
                is_active=True
            )
            db.add(ebay_vendor)
            db.commit()
            print("✅ Created eBay vendor")
        
        # Create fresh product
        new_product = Product(
            name=PRODUCT_NAME,
            url=EBAY_URL,
            vendor_id=ebay_vendor.id,
            is_active=True,
            scan_frequency_minutes=15,  # Frequent for auction tracking
            # Auction fields will be auto-populated on first scan
            is_auction=False,
            auction_end_time=None,
            current_bid_count=None,
            buy_it_now_price=None,
        )
        db.add(new_product)
        db.commit()
        
        print(f"\n✅ Created fresh product: {new_product.name}")
        print(f"   ID: {new_product.id}")
        print(f"   URL: {new_product.url}")
        print(f"   Scan frequency: {new_product.scan_frequency_minutes} minutes")
        print(f"\n💰 Next scan will use Bright Data to get complete auction data")
        print(f"   Expected cost: ~$0.0015 (one-time)")
        print(f"   All future scans: FREE\n")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Error: {e}")
        return False
    finally:
        db.close()
    
    return True

if __name__ == "__main__":
    print("=" * 70)
    print("Reset eBay Product for Testing")
    print("=" * 70)
    print(f"\nThis will DELETE and RECREATE:")
    print(f"  Product: {PRODUCT_NAME}")
    print(f"  URL: {EBAY_URL}")
    print(f"\n⚠️  All price history will be LOST!")
    print("=" * 70)
    
    response = input("\nContinue? (yes/no): ")
    if response.lower() == 'yes':
        if reset_ebay_product():
            print("\n🎉 Done! You can now scan the product to test Bright Data integration.")
    else:
        print("\n❌ Cancelled.")

