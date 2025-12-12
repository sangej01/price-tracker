from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional, List


# Vendor Schemas
class VendorBase(BaseModel):
    name: str
    domain: str


class VendorCreate(VendorBase):
    pass


class VendorUpdate(BaseModel):
    name: Optional[str] = None
    domain: Optional[str] = None
    is_active: Optional[bool] = None


class Vendor(VendorBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Product Schemas
class ProductBase(BaseModel):
    name: str
    url: str
    vendor_id: int
    image_url: Optional[str] = None
    description: Optional[str] = None
    scan_frequency_minutes: int = 60


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    url: Optional[str] = None
    vendor_id: Optional[int] = None
    image_url: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    scan_frequency_minutes: Optional[int] = None


class Product(ProductBase):
    id: int
    is_active: bool
    created_at: datetime
    last_scanned_at: Optional[datetime] = None
    # Auction fields
    is_auction: bool = False
    auction_end_time: Optional[datetime] = None
    current_bid_count: Optional[int] = None
    buy_it_now_price: Optional[float] = None

    class Config:
        from_attributes = True


# Price History Schemas
class PriceHistoryBase(BaseModel):
    price: float
    currency: str = "USD"
    in_stock: bool = True


class PriceHistoryCreate(PriceHistoryBase):
    product_id: int


class PriceHistory(PriceHistoryBase):
    id: int
    product_id: int
    scraped_at: datetime
    # Auction fields
    bid_count: Optional[int] = None
    is_auction_active: Optional[bool] = None

    class Config:
        from_attributes = True


# Dashboard Schemas
class ProductWithLatestPrice(BaseModel):
    id: int
    name: str
    url: str
    vendor_name: str
    image_url: Optional[str] = None
    current_price: Optional[float] = None
    previous_price: Optional[float] = None
    price_change: Optional[float] = None
    price_change_percent: Optional[float] = None
    in_stock: bool = True
    last_scanned_at: Optional[datetime] = None
    currency: str = "USD"
    scan_frequency_minutes: int = 60
    # Auction fields
    is_auction: bool = False
    auction_end_time: Optional[datetime] = None
    current_bid_count: Optional[int] = None
    buy_it_now_price: Optional[float] = None

    class Config:
        from_attributes = True


class ProductPriceStats(BaseModel):
    product_id: int
    product_name: str
    current_price: Optional[float] = None
    lowest_price: Optional[float] = None
    highest_price: Optional[float] = None
    average_price: Optional[float] = None
    price_history: List[PriceHistory] = []

    class Config:
        from_attributes = True


# Settings Schemas
class SettingBase(BaseModel):
    key: str
    value: str


class SettingCreate(SettingBase):
    pass


class SettingUpdate(BaseModel):
    value: str


class Setting(SettingBase):
    class Config:
        from_attributes = True


