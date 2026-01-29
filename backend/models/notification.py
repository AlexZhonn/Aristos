from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum


class NotificationType(str, Enum):
    EXPIRATION = "expiration"
    BUDGET = "budget"
    ACHIEVEMENT = "achievement"
    MEAL_SUGGESTION = "meal_suggestion"
    DAILY_SUMMARY = "daily_summary"


class Notification(BaseModel):
    notification_id: str
    user_id: str
    type: NotificationType
    title: str
    body: str
    data: Optional[Dict[str, Any]] = None
    read: bool = False
    sent_at: datetime = datetime.now()


class NotificationCreate(BaseModel):
    type: NotificationType
    title: str
    body: str
    data: Optional[Dict[str, Any]] = None


class PushTokenRegister(BaseModel):
    expo_push_token: str
