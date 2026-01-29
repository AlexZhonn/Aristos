from datetime import datetime, timedelta
from typing import Dict, Optional


class ExpirationService:
    # Default expiration days for different food categories
    EXPIRATION_DEFAULTS = {
        "produce": 7,
        "dairy": 14,
        "meat": 3,
        "pantry": 365,
        "frozen": 180,
        "beverages": 30,
        "snacks": 90,
        "other": 30
    }

    # Specific items with known expiration periods
    SPECIFIC_ITEMS = {
        "milk": 7,
        "eggs": 21,
        "chicken": 2,
        "beef": 3,
        "pork": 3,
        "fish": 1,
        "lettuce": 5,
        "tomatoes": 7,
        "bananas": 5,
        "apples": 14,
        "bread": 5,
        "yogurt": 14,
        "cheese": 30,
        "butter": 60,
        "spinach": 5,
        "berries": 5,
        "carrots": 21,
        "potatoes": 60,
        "onions": 30,
        "garlic": 60
    }

    @staticmethod
    def estimate_expiration_date(
        item_name: str,
        category: str,
        purchase_date: Optional[datetime] = None
    ) -> datetime:
        """Estimate expiration date for an item"""
        if purchase_date is None:
            purchase_date = datetime.now()

        # Check if item has specific expiration
        item_lower = item_name.lower()
        days = None
        
        for key, value in ExpirationService.SPECIFIC_ITEMS.items():
            if key in item_lower:
                days = value
                break

        # Fall back to category default
        if days is None:
            days = ExpirationService.EXPIRATION_DEFAULTS.get(category, 30)

        return purchase_date + timedelta(days=days)

    @staticmethod
    def get_urgency_level(expiration_date: datetime) -> str:
        """Get urgency level for an item based on expiration date"""
        now = datetime.now()
        days_until_expiration = (expiration_date - now).days

        if days_until_expiration < 0:
            return "expired"
        elif days_until_expiration == 0:
            return "expires_today"
        elif days_until_expiration <= 1:
            return "urgent"
        elif days_until_expiration <= 3:
            return "warning"
        else:
            return "good"

    @staticmethod
    def get_urgency_color(urgency: str) -> str:
        """Get color code for urgency level"""
        colors = {
            "expired": "#EF4444",  # red
            "expires_today": "#F97316",  # orange
            "urgent": "#F59E0B",  # amber
            "warning": "#EAB308",  # yellow
            "good": "#22C55E"  # green
        }
        return colors.get(urgency, "#6B7280")  # gray default

    @staticmethod
    def should_send_notification(expiration_date: datetime, last_notified: Optional[datetime] = None) -> bool:
        """Determine if a notification should be sent for an expiring item"""
        now = datetime.now()
        days_until_expiration = (expiration_date - now).days

        # Send notification at 3 days, 1 day, and on expiration day
        should_notify = days_until_expiration in [3, 1, 0]

        # Don't spam - only send if not notified in last 12 hours
        if should_notify and last_notified:
            hours_since_notified = (now - last_notified).total_seconds() / 3600
            return hours_since_notified >= 12

        return should_notify
