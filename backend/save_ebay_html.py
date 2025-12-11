"""
Save the raw HTML from eBay auction page to inspect it
"""
import asyncio
from app.scrapers.ebay_scraper import EbayScraper

async def save_html():
    url = "https://www.ebay.com/itm/366042770374"
    scraper = EbayScraper(url)
    
    # Get the HTML
    html = await scraper.fetch_page()
    
    if html:
        # Save to file
        with open('ebay_auction_page.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"✅ Saved HTML to ebay_auction_page.html ({len(html)} characters)")
        print(f"   You can open this file to search for time/countdown/timer elements")
    else:
        print("❌ Failed to fetch HTML")

if __name__ == "__main__":
    asyncio.run(save_html())

