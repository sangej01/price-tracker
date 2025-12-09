from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.price_scanner import PriceScannerService

router = APIRouter(prefix="/api/scanner", tags=["scanner"])


@router.post("/scan-all")
async def trigger_scan_all(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """Manually trigger a scan of all due products"""
    result = await PriceScannerService.scan_all_due_products(db)
    return {
        "message": "Scan completed",
        "results": result
    }


@router.get("/status")
def get_scanner_status(db: Session = Depends(get_db)):
    """Get the status of the price scanner"""
    # This could be expanded to show scheduler status, queue info, etc.
    return {
        "status": "active",
        "message": "Scanner is running"
    }

