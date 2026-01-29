import httpx
import os
from typing import List, Dict, Any, Optional
from datetime import datetime


class NotificationService:
    EXPO_PUSH_URL = "https://exp.host/--/api/v2/push/send"

    def __init__(self):
        self.access_token = os.getenv("EXPO_PUSH_ACCESS_TOKEN")

    async def send_push_notification(
        self,
        expo_push_token: str,
        title: str,
        body: str,
        data: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Send push notification via Expo"""
        try:
            message = {
                "to": expo_push_token,
                "sound": "default",
                "title": title,
                "body": body,
                "data": data or {}
            }

            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }

            if self.access_token:
                headers["Authorization"] = f"Bearer {self.access_token}"

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.EXPO_PUSH_URL,
                    json=message,
                    headers=headers,
                    timeout=10.0
                )

                if response.status_code == 200:
                    result = response.json()
                    if result.get("data", {}).get("status") == "ok":
                        return True
                    print(f"Push notification error: {result}")
                    return False
                else:
                    print(f"Push notification failed: {response.status_code}")
                    return False

        except Exception as e:
            print(f"Error sending push notification: {e}")
            return False

    async def send_batch_notifications(
        self,
        notifications: List[Dict[str, Any]]
    ) -> List[bool]:
        """Send multiple push notifications"""
        messages = []
        for notif in notifications:
            messages.append({
                "to": notif["token"],
                "sound": "default",
                "title": notif["title"],
                "body": notif["body"],
                "data": notif.get("data", {})
            })

        try:
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }

            if self.access_token:
                headers["Authorization"] = f"Bearer {self.access_token}"

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.EXPO_PUSH_URL,
                    json=messages,
                    headers=headers,
                    timeout=30.0
                )

                if response.status_code == 200:
                    results = response.json()
                    return [r.get("status") == "ok" for r in results.get("data", [])]

        except Exception as e:
            print(f"Error sending batch notifications: {e}")

        return [False] * len(notifications)

    def create_expiration_notification(self, item_name: str, days_until: int) -> Dict[str, str]:
        """Create expiration notification message"""
        if days_until == 0:
            title = "⏰ Item Expiring Today!"
            body = f"{item_name} expires today. Use it or lose it!"
        elif days_until == 1:
            title = "⚠️ Item Expiring Tomorrow"
            body = f"{item_name} expires tomorrow. Plan to use it soon!"
        else:
            title = f"📅 Item Expiring in {days_until} Days"
            body = f"{item_name} will expire soon. Consider using it!"

        return {"title": title, "body": body}

    def create_budget_notification(self, spent: float, budget: float) -> Dict[str, str]:
        """Create budget warning notification"""
        percentage = (spent / budget) * 100
        
        if percentage >= 100:
            title = "💰 Budget Exceeded!"
            body = f"You've spent ${spent:.2f} of your ${budget:.2f} budget."
        elif percentage >= 90:
            title = "💸 Approaching Budget Limit"
            body = f"You've spent ${spent:.2f} (90%) of your ${budget:.2f} budget."
        else:
            title = "💵 Budget Update"
            body = f"You've spent ${spent:.2f} of your ${budget:.2f} budget."

        return {"title": title, "body": body}

    def create_achievement_notification(self, achievement: str, description: str) -> Dict[str, str]:
        """Create achievement notification"""
        return {
            "title": f"🏆 Achievement Unlocked: {achievement}",
            "body": description
        }

    def create_meal_suggestion_notification(self, ingredients: List[str]) -> Dict[str, str]:
        """Create meal suggestion notification"""
        if len(ingredients) == 0:
            return {
                "title": "🍳 Time to Shop!",
                "body": "Your pantry is running low. Time to restock!"
            }
        
        items_text = ", ".join(ingredients[:3])
        if len(ingredients) > 3:
            items_text += f" and {len(ingredients) - 3} more"

        return {
            "title": "🍳 Cook Before They Expire!",
            "body": f"You have {items_text}. Check out recipe suggestions!"
        }
