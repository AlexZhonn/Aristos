from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class ReceiptItem(BaseModel):
    name: str
    quantity: float = 1.0
    price: float
    calories: Optional[float] = None
    protein: Optional[float] = None
    unit: Optional[str] = None


class Receipt(BaseModel):
    receipt_id: str
    user_id: str
    image_url: Optional[str] = None
    store_name: Optional[str] = None
    purchase_date: datetime
    total_amount: float
    items: List[ReceiptItem]
    processed_at: datetime = datetime.now()


class ReceiptCreate(BaseModel):
    image_base64: str
    purchase_date: Optional[datetime] = None


class ReceiptUpdate(BaseModel):
    store_name: Optional[str] = None
    purchase_date: Optional[datetime] = None
    total_amount: Optional[float] = None
    items: Optional[List[ReceiptItem]] = None
