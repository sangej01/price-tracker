from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Optional
from ..database import get_db
from ..models import Settings, Vendor, Product
from pydantic import BaseModel
from datetime import datetime
import json

router = APIRouter(prefix="/api/settings", tags=["settings"])


class ScanFrequencySettings(BaseModel):
    default_frequency: int = 60  # Default minutes
    vendor_overrides: Dict[int, int] = {}  # vendor_id -> minutes


@router.get("/scan-frequency")
def get_scan_frequency_settings(db: Session = Depends(get_db)):
    """Get scan frequency settings"""
    # Get default frequency
    default_setting = db.query(Settings).filter(Settings.key == "default_scan_frequency").first()
    default_frequency = int(default_setting.value) if default_setting else 60
    
    # Get vendor overrides
    vendor_overrides_setting = db.query(Settings).filter(Settings.key == "vendor_scan_overrides").first()
    vendor_overrides = {}
    if vendor_overrides_setting:
        try:
            vendor_overrides = json.loads(vendor_overrides_setting.value)
            # Convert string keys back to integers
            vendor_overrides = {int(k): v for k, v in vendor_overrides.items()}
        except:
            vendor_overrides = {}
    
    return {
        "default_frequency": default_frequency,
        "vendor_overrides": vendor_overrides
    }


@router.put("/scan-frequency")
def update_scan_frequency_settings(
    settings: ScanFrequencySettings,
    db: Session = Depends(get_db)
):
    """Update scan frequency settings"""
    # Update default frequency
    default_setting = db.query(Settings).filter(Settings.key == "default_scan_frequency").first()
    if default_setting:
        default_setting.value = str(settings.default_frequency)
        default_setting.updated_at = datetime.utcnow()
    else:
        default_setting = Settings(
            key="default_scan_frequency",
            value=str(settings.default_frequency)
        )
        db.add(default_setting)
    
    # Update vendor overrides
    vendor_overrides_setting = db.query(Settings).filter(Settings.key == "vendor_scan_overrides").first()
    overrides_json = json.dumps(settings.vendor_overrides)
    if vendor_overrides_setting:
        vendor_overrides_setting.value = overrides_json
        vendor_overrides_setting.updated_at = datetime.utcnow()
    else:
        vendor_overrides_setting = Settings(
            key="vendor_scan_overrides",
            value=overrides_json
        )
        db.add(vendor_overrides_setting)
    
    db.commit()
    
    return {
        "message": "Settings updated successfully",
        "default_frequency": settings.default_frequency,
        "vendor_overrides": settings.vendor_overrides
    }


@router.post("/scan-frequency/apply-to-products")
def apply_frequency_to_products(
    vendor_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Apply frequency settings to existing products
    If vendor_id specified, only apply to that vendor's products
    Otherwise apply to all products
    """
    # Get settings
    settings = get_scan_frequency_settings(db)
    
    # Get products to update
    query = db.query(Product).filter(Product.is_active == True)
    if vendor_id:
        query = query.filter(Product.vendor_id == vendor_id)
    
    products = query.all()
    updated_count = 0
    
    for product in products:
        # Check if vendor has override
        if product.vendor_id in settings["vendor_overrides"]:
            new_frequency = settings["vendor_overrides"][product.vendor_id]
        else:
            new_frequency = settings["default_frequency"]
        
        if product.scan_frequency_minutes != new_frequency:
            product.scan_frequency_minutes = new_frequency
            updated_count += 1
    
    db.commit()
    
    return {
        "message": f"Updated {updated_count} products",
        "updated_count": updated_count
    }


