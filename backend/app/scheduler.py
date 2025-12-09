from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from .database import SessionLocal
from .services.price_scanner import PriceScannerService
import asyncio


def scan_prices_job():
    """Job to scan all due products"""
    print("Running scheduled price scan...")
    db = SessionLocal()
    try:
        # Run the async function in the event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(PriceScannerService.scan_all_due_products(db))
        print(f"Scan completed: {result}")
    finally:
        db.close()


def start_scheduler():
    """Start the background scheduler"""
    scheduler = BackgroundScheduler()
    
    # Schedule price scanning every 15 minutes
    scheduler.add_job(
        scan_prices_job,
        trigger=IntervalTrigger(minutes=15),
        id='price_scan_job',
        name='Scan product prices',
        replace_existing=True
    )
    
    scheduler.start()
    print("Scheduler started - scanning every 15 minutes")
    return scheduler


