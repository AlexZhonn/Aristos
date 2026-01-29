from apscheduler.schedulers.asyncio import AsyncIOScheduler
from services.firebase_service import FirebaseService
from services.notification_service import NotificationService
from services.expiration_service import ExpirationService
from datetime import datetime, timedelta
import asyncio


class NotificationScheduler:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.firebase_service = FirebaseService()
        self.notification_service = NotificationService()
        self.expiration_service = ExpirationService()

    def start(self):
        """Start the scheduler"""
        # Run expiration check twice daily (morning and evening)
        self.scheduler.add_job(
            self.check_expiring_items,
            'cron',
            hour='8,18',
            minute=0
        )
        
        # Run daily summary at 8 PM
        self.scheduler.add_job(
            self.send_daily_summaries,
            'cron',
            hour=20,
            minute=0
        )
        
        self.scheduler.start()
        print("📅 Notification scheduler started")

    def stop(self):
        """Stop the scheduler"""
        self.scheduler.shutdown()

    async def check_expiring_items(self):
        """Check all users for expiring items and send notifications"""
        print("🔍 Checking for expiring items...")
        
        try:
            # This is a simplified version - in production, you'd want to batch process users
            # For now, this would need to iterate through users
            # You might want to add a method to get all users or use Cloud Functions
            pass
        except Exception as e:
            print(f"Error checking expiring items: {e}")

    async def send_daily_summaries(self):
        """Send daily summaries to all users"""
        print("📊 Sending daily summaries...")
        
        try:
            # Similar to above - would iterate through users
            # Send summary of spending, calories, and pantry status
            pass
        except Exception as e:
            print(f"Error sending daily summaries: {e}")

    async def send_expiration_notification(self, user_id: str, item_name: str, days_until: int):
        """Send expiration notification to a user"""
        try:
            # Get user's push token
            push_token = self.firebase_service.get_push_token(user_id)
            
            if not push_token:
                return
            
            # Create notification message
            notif_data = self.notification_service.create_expiration_notification(
                item_name,
                days_until
            )
            
            # Send push notification
            await self.notification_service.send_push_notification(
                push_token,
                notif_data["title"],
                notif_data["body"],
                {
                    "type": "expiration",
                    "item_name": item_name,
                    "days_until": days_until
                }
            )
            
            # Store in Firestore
            self.firebase_service.create_notification(
                user_id,
                {
                    "type": "expiration",
                    "title": notif_data["title"],
                    "body": notif_data["body"],
                    "data": {
                        "item_name": item_name,
                        "days_until": days_until
                    }
                }
            )
            
        except Exception as e:
            print(f"Error sending expiration notification: {e}")


# Global scheduler instance
scheduler = NotificationScheduler()


def start_scheduler():
    """Start the notification scheduler"""
    scheduler.start()


def stop_scheduler():
    """Stop the notification scheduler"""
    scheduler.stop()
