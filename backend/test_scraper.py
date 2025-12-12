"""
Test script for custom scrapers
Usage: python test_scraper.py [URL]
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from app.scrapers.scraper_factory import ScraperFactory


async def test_scraper(url: str):
    """Test scraping a specific URL"""
    # Avoid Windows console encoding issues (e.g., cp1252) causing UnicodeEncodeError for emoji.
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # Python 3.7+
    except Exception:
        pass

    print(f"\n{'='*60}")
    print(f"Testing Price Scraper")
    print(f"{'='*60}")
    print(f"URL: {url}\n")
    
    try:
        # Determine which scraper will be used
        scraper = ScraperFactory.create_scraper(url)
        print(f"Using scraper: {scraper.__class__.__name__}\n")
        
        # Scrape the URL
        print("Scraping... (this may take a few seconds)")
        result = await ScraperFactory.scrape_url(url)
        
        # Display results
        print(f"\n{'='*60}")
        print("Results:")
        print(f"{'='*60}")
        
        if result['price']:
            print(f"Price: {result['currency']} ${result['price']:.2f}")
        else:
            print("Price: Not found")
        
        if result['in_stock']:
            print("Stock Status: In Stock")
        else:
            print("Stock Status: Out of Stock")
        
        print(f"{'='*60}\n")
        
    except Exception as e:
        print(f"\nError: {e}\n")
        import traceback
        traceback.print_exc()


async def test_multiple_urls():
    """Test multiple example URLs"""
    test_urls = [
        # Add your test URLs here
        "https://www.example.com/product",
    ]
    
    print("\n" + "="*60)
    print("Testing Multiple URLs")
    print("="*60)
    
    for url in test_urls:
        await test_scraper(url)
        await asyncio.sleep(2)  # Delay between requests


def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        # Test single URL from command line
        url = sys.argv[1]
        asyncio.run(test_scraper(url))
    else:
        # Show usage
        print("\nPrice Tracker - Scraper Test Utility")
        print("="*60)
        print("\nUsage:")
        print("  python test_scraper.py <PRODUCT_URL>")
        print("\nExample:")
        print("  python test_scraper.py https://www.amazon.com/dp/B08N5WRWNW")
        print("\nSupported Sites:")
        print("  • Amazon (amazon.com, amazon.co.uk, etc.)")
        print("  • eBay (ebay.com)")
        print("  • Newegg (newegg.com)")
        print("  • Generic scraper for other sites")
        print("\n")


if __name__ == "__main__":
    main()

