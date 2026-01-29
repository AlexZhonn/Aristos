from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime


class UserPreferences(BaseModel):
    dietary_restrictions: List[str] = []
    daily_calorie_goal: int = 2000
    daily_budget: float = 50.0
    protein_goal: float = 150.0


class User(BaseModel):
    uid: str
    email: EmailStr
    display_name: Optional[str] = None
    preferences: UserPreferences = UserPreferences()
    created_at: datetime = datetime.now()


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    display_name: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    display_name: Optional[str] = None
    preferences: Optional[UserPreferences] = None
