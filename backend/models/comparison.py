from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class DeliveryItem(BaseModel):
    name: str
    restaurant: str
    price: float
    calories: Optional[float] = None


class HomeCookingAlternative(BaseModel):
    recipe_name: str
    estimated_cost: float
    ingredients: List[str]
    calories: Optional[float] = None
    prep_time: Optional[int] = None  # in minutes


class Comparison(BaseModel):
    comparison_id: str
    user_id: str
    delivery_item: DeliveryItem
    home_cooking_alternative: HomeCookingAlternative
    savings: float
    calorie_difference: Optional[float] = None
    created_at: datetime = datetime.now()


class ComparisonCreate(BaseModel):
    delivery_item: DeliveryItem
    image_base64: Optional[str] = None


class ComparisonResponse(BaseModel):
    comparison: Comparison
    recommendation: str
