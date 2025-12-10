"""
Simple utility to clean bad price data from the database
"""
import sys
sys.path.insert(0, '.')

from app.database import SessionLocal
from app.models import PriceHistory, Product
from datetime import datetime

def list_products():
    """List all products with their IDs"""
    db = SessionLocal()
    try:
        products = db.query(Product).all()
        print("\n" + "="*60)
        print("Available Products:")
        print("="*60)
        for p in products:
            history_count = db.query(PriceHistory).filter(PriceHistory.product_id == p.id).count()
            print(f"ID: {p.id} | {p.name}")
            print(f"   URL: {p.url}")
            print(f"   Price History Records: {history_count}")
            print()
    finally:
        db.close()

def delete_price_history(product_id: int):
    """Delete all price history for a product"""
    db = SessionLocal()
    try:
        # Get product name for confirmation
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            print(f"❌ Product ID {product_id} not found!")
            return
        
        # Count records
        count = db.query(PriceHistory).filter(PriceHistory.product_id == product_id).count()
        
        if count == 0:
            print(f"ℹ️  No price history found for '{product.name}'")
            return
        
        print(f"\n⚠️  About to delete {count} price history records for:")
        print(f"   '{product.name}'")
        confirm = input("\nType 'yes' to confirm: ")
        
        if confirm.lower() == 'yes':
            db.query(PriceHistory).filter(PriceHistory.product_id == product_id).delete()
            
            # Reset last_scanned_at
            product.last_scanned_at = None
            
            db.commit()
            print(f"✅ Deleted {count} price history records")
            print("✅ Reset last scanned time")
        else:
            print("❌ Cancelled")
    finally:
        db.close()

def delete_bad_prices(product_id: int, bad_price: float):
    """Delete price history entries with a specific (bad) price"""
    db = SessionLocal()
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            print(f"❌ Product ID {product_id} not found!")
            return
        
        # Find bad records
        bad_records = db.query(PriceHistory).filter(
            PriceHistory.product_id == product_id,
            PriceHistory.price == bad_price
        ).all()
        
        if not bad_records:
            print(f"ℹ️  No records found with price ${bad_price}")
            return
        
        print(f"\n⚠️  Found {len(bad_records)} records with price ${bad_price} for:")
        print(f"   '{product.name}'")
        print("\nDates of bad records:")
        for record in bad_records[:10]:  # Show first 10
            print(f"   - {record.scraped_at}")
        if len(bad_records) > 10:
            print(f"   ... and {len(bad_records) - 10} more")
        
        confirm = input("\nType 'yes' to delete these records: ")
        
        if confirm.lower() == 'yes':
            for record in bad_records:
                db.delete(record)
            db.commit()
            print(f"✅ Deleted {len(bad_records)} bad price records")
        else:
            print("❌ Cancelled")
    finally:
        db.close()

if __name__ == "__main__":
    print("="*60)
    print("Price Tracker - Data Cleanup Utility")
    print("="*60)
    
    while True:
        print("\nOptions:")
        print("1. List all products")
        print("2. Delete ALL price history for a product")
        print("3. Delete records with specific bad price")
        print("4. Exit")
        
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == "1":
            list_products()
        
        elif choice == "2":
            list_products()
            try:
                product_id = int(input("\nEnter Product ID to clear: "))
                delete_price_history(product_id)
            except ValueError:
                print("❌ Invalid Product ID")
        
        elif choice == "3":
            list_products()
            try:
                product_id = int(input("\nEnter Product ID: "))
                bad_price = float(input("Enter the bad price to delete (e.g., 699.99): "))
                delete_bad_prices(product_id, bad_price)
            except ValueError:
                print("❌ Invalid input")
        
        elif choice == "4":
            print("\n👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice")
