"""
Database migration script to add auction tracking fields
Run this script to add auction support to existing database
"""
import sys
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.database import engine

def migrate():
    """Add auction tracking fields to products and price_history tables"""
    with engine.connect() as conn:
        print("Adding auction fields to products table...")
        
        # Add columns to products table
        try:
            conn.execute(text("""
                ALTER TABLE products 
                ADD COLUMN is_auction BOOLEAN DEFAULT 0
            """))
            conn.commit()
            print("✓ Added is_auction column")
        except Exception as e:
            print(f"  is_auction column may already exist: {e}")
        
        try:
            conn.execute(text("""
                ALTER TABLE products 
                ADD COLUMN auction_end_time TIMESTAMP NULL
            """))
            conn.commit()
            print("✓ Added auction_end_time column")
        except Exception as e:
            print(f"  auction_end_time column may already exist: {e}")
        
        try:
            conn.execute(text("""
                ALTER TABLE products 
                ADD COLUMN current_bid_count INTEGER NULL
            """))
            conn.commit()
            print("✓ Added current_bid_count column")
        except Exception as e:
            print(f"  current_bid_count column may already exist: {e}")
        
        try:
            conn.execute(text("""
                ALTER TABLE products 
                ADD COLUMN buy_it_now_price REAL NULL
            """))
            conn.commit()
            print("✓ Added buy_it_now_price column")
        except Exception as e:
            print(f"  buy_it_now_price column may already exist: {e}")
        
        print("\nAdding auction fields to price_history table...")
        
        # Add columns to price_history table
        try:
            conn.execute(text("""
                ALTER TABLE price_history 
                ADD COLUMN bid_count INTEGER NULL
            """))
            conn.commit()
            print("✓ Added bid_count column")
        except Exception as e:
            print(f"  bid_count column may already exist: {e}")
        
        try:
            conn.execute(text("""
                ALTER TABLE price_history 
                ADD COLUMN is_auction_active BOOLEAN NULL
            """))
            conn.commit()
            print("✓ Added is_auction_active column")
        except Exception as e:
            print(f"  is_auction_active column may already exist: {e}")
        
        print("\n✅ Migration completed successfully!")
        print("Auction tracking fields have been added to the database.")

if __name__ == "__main__":
    print("=" * 60)
    print("Database Migration: Add Auction Tracking Fields")
    print("=" * 60)
    print()
    
    response = input("This will modify your database. Continue? (yes/no): ")
    if response.lower() == 'yes':
        migrate()
    else:
        print("Migration cancelled.")


