from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class FoodCategory(str, Enum):
    PRODUCE = "produce"
    DAIRY = "dairy"
    MEAT = "meat"
    PANTRY = "pantry"
    FROZEN = "frozen"
    BEVERAGES = "beverages"
    SNACKS = "snacks"
    OTHER = "other"


class Ingredient(BaseModel):
    item_id: str
    user_id: str
    name: str
    category: FoodCategory
    quantity: float
    unit: str
    purchase_date: datetime
    expiration_date: datetime
    calories: Optional[float] = None
    protein: Optional[float] = None
    receipt_id: Optional[str] = None
    consumed: bool = False
    consumed_date: Optional[datetime] = None


class IngredientCreate(BaseModel):
    name: str
    category: FoodCategory
    quantity: float
    unit: str
    purchase_date: Optional[datetime] = None
    expiration_date: Optional[datetime] = None
    calories: Optional[float] = None
    protein: Optional[float] = None


class IngredientUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[FoodCategory] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    expiration_date: Optional[datetime] = None
    consumed: Optional[bool] = None
