from fastapi import APIRouter, HTTPException, Depends
from models.notification import Notification, NotificationCreate, PushTokenRegister
from services.firebase_service import FirebaseService
from services.notification_service import NotificationService
from middleware.auth import get_current_user
from typing import Dict, Any

router = APIRouter(prefix="/api/notifications", tags=["notifications"])
firebase_service = FirebaseService()
notification_service = NotificationService()


@router.get("/")
async def get_notifications(
    current_user: Dict[str, Any] = Depends(get_current_user),
    unread_only: bool = False
):
    """Get notifications for current user"""
    try:
        notifications = firebase_service.get_user_notifications(
            current_user["uid"],
            unread_only=unread_only
        )
        return notifications
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{notification_id}/read")
async def mark_notification_read(
    notification_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Mark a notification as read"""
    try:
        success = firebase_service.mark_notification_read(notification_id)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to mark notification as read")
        
        return {"message": "Notification marked as read"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/register-token")
async def register_push_token(
    token_data: PushTokenRegister,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Register Expo push token for user"""
    try:
        success = firebase_service.save_push_token(
            current_user["uid"],
            token_data.expo_push_token
        )
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to register push token")
        
        return {"message": "Push token registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/test")
async def send_test_notification(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Send a test push notification"""
    try:
        push_token = firebase_service.get_push_token(current_user["uid"])
        
        if not push_token:
            raise HTTPException(status_code=404, detail="No push token registered")
        
        success = await notification_service.send_push_notification(
            push_token,
            "🎉 Test Notification",
            "This is a test notification from Aristos!",
            {"type": "test"}
        )
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to send notification")
        
        return {"message": "Test notification sent successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
