import firebase_admin
from firebase_admin import credentials, firestore, auth
from typing import Optional, Dict, Any, List
import os
from datetime import datetime


class FirebaseService:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirebaseService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not FirebaseService._initialized:
            self.initialize()
            FirebaseService._initialized = True

    def initialize(self):
        """Initialize Firebase Admin SDK"""
        try:
            cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH")
            if cred_path and os.path.exists(cred_path):
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred)
            else:
                # For development without credentials file
                firebase_admin.initialize_app()
            
            self.db = firestore.client()
            print("Firebase initialized successfully")
        except Exception as e:
            print(f"Firebase initialization error: {e}")
            self.db = None

    def get_user(self, uid: str) -> Optional[Dict[str, Any]]:
        """Get user document from Firestore"""
        if not self.db:
            return None
        try:
            user_ref = self.db.collection("users").document(uid)
            user_doc = user_ref.get()
            if user_doc.exists:
                return user_doc.to_dict()
            return None
        except Exception as e:
            print(f"Error getting user: {e}")
            return None

    def create_user(self, uid: str, user_data: Dict[str, Any]) -> bool:
        """Create user document in Firestore"""
        if not self.db:
            return False
        try:
            user_data["created_at"] = datetime.now()
            self.db.collection("users").document(uid).set(user_data)
            return True
        except Exception as e:
            print(f"Error creating user: {e}")
            return False

    def update_user(self, uid: str, user_data: Dict[str, Any]) -> bool:
        """Update user document in Firestore"""
        if not self.db:
            return False
        try:
            self.db.collection("users").document(uid).update(user_data)
            return True
        except Exception as e:
            print(f"Error updating user: {e}")
            return False

    def verify_token(self, id_token: str) -> Optional[Dict[str, Any]]:
        """Verify Firebase ID token"""
        try:
            decoded_token = auth.verify_id_token(id_token)
            return decoded_token
        except Exception as e:
            print(f"Error verifying token: {e}")
            return None

    # Receipts
    def create_receipt(self, user_id: str, receipt_data: Dict[str, Any]) -> Optional[str]:
        """Create receipt document"""
        if not self.db:
            return None
        try:
            receipt_ref = self.db.collection("receipts").document()
            receipt_data["receipt_id"] = receipt_ref.id
            receipt_data["user_id"] = user_id
            receipt_data["processed_at"] = datetime.now()
            receipt_ref.set(receipt_data)
            return receipt_ref.id
        except Exception as e:
            print(f"Error creating receipt: {e}")
            return None

    def get_user_receipts(self, user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get all receipts for a user"""
        if not self.db:
            return []
        try:
            receipts = (
                self.db.collection("receipts")
                .where("user_id", "==", user_id)
                .order_by("purchase_date", direction=firestore.Query.DESCENDING)
                .limit(limit)
                .stream()
            )
            return [receipt.to_dict() for receipt in receipts]
        except Exception as e:
            print(f"Error getting receipts: {e}")
            return []

    def get_receipt(self, receipt_id: str) -> Optional[Dict[str, Any]]:
        """Get single receipt"""
        if not self.db:
            return None
        try:
            receipt_doc = self.db.collection("receipts").document(receipt_id).get()
            if receipt_doc.exists:
                return receipt_doc.to_dict()
            return None
        except Exception as e:
            print(f"Error getting receipt: {e}")
            return None

    def update_receipt(self, receipt_id: str, receipt_data: Dict[str, Any]) -> bool:
        """Update receipt"""
        if not self.db:
            return False
        try:
            self.db.collection("receipts").document(receipt_id).update(receipt_data)
            return True
        except Exception as e:
            print(f"Error updating receipt: {e}")
            return False

    def delete_receipt(self, receipt_id: str) -> bool:
        """Delete receipt"""
        if not self.db:
            return False
        try:
            self.db.collection("receipts").document(receipt_id).delete()
            return True
        except Exception as e:
            print(f"Error deleting receipt: {e}")
            return False

    # Pantry Items
    def create_pantry_item(self, user_id: str, item_data: Dict[str, Any]) -> Optional[str]:
        """Create pantry item"""
        if not self.db:
            return None
        try:
            item_ref = self.db.collection("pantry_items").document()
            item_data["item_id"] = item_ref.id
            item_data["user_id"] = user_id
            item_ref.set(item_data)
            return item_ref.id
        except Exception as e:
            print(f"Error creating pantry item: {e}")
            return None

    def get_user_pantry(self, user_id: str, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get user's pantry items"""
        if not self.db:
            return []
        try:
            query = self.db.collection("pantry_items").where("user_id", "==", user_id).where("consumed", "==", False)
            
            if category:
                query = query.where("category", "==", category)
            
            items = query.order_by("expiration_date").stream()
            return [item.to_dict() for item in items]
        except Exception as e:
            print(f"Error getting pantry: {e}")
            return []

    def get_expiring_items(self, user_id: str, before_date: datetime) -> List[Dict[str, Any]]:
        """Get items expiring before a certain date"""
        if not self.db:
            return []
        try:
            items = (
                self.db.collection("pantry_items")
                .where("user_id", "==", user_id)
                .where("consumed", "==", False)
                .where("expiration_date", "<=", before_date)
                .order_by("expiration_date")
                .stream()
            )
            return [item.to_dict() for item in items]
        except Exception as e:
            print(f"Error getting expiring items: {e}")
            return []

    def update_pantry_item(self, item_id: str, item_data: Dict[str, Any]) -> bool:
        """Update pantry item"""
        if not self.db:
            return False
        try:
            self.db.collection("pantry_items").document(item_id).update(item_data)
            return True
        except Exception as e:
            print(f"Error updating pantry item: {e}")
            return False

    def delete_pantry_item(self, item_id: str) -> bool:
        """Delete pantry item"""
        if not self.db:
            return False
        try:
            self.db.collection("pantry_items").document(item_id).delete()
            return True
        except Exception as e:
            print(f"Error deleting pantry item: {e}")
            return False

    # Comparisons
    def create_comparison(self, user_id: str, comparison_data: Dict[str, Any]) -> Optional[str]:
        """Create comparison"""
        if not self.db:
            return None
        try:
            comp_ref = self.db.collection("comparisons").document()
            comparison_data["comparison_id"] = comp_ref.id
            comparison_data["user_id"] = user_id
            comparison_data["created_at"] = datetime.now()
            comp_ref.set(comparison_data)
            return comp_ref.id
        except Exception as e:
            print(f"Error creating comparison: {e}")
            return None

    def get_user_comparisons(self, user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get user comparison history"""
        if not self.db:
            return []
        try:
            comparisons = (
                self.db.collection("comparisons")
                .where("user_id", "==", user_id)
                .order_by("created_at", direction=firestore.Query.DESCENDING)
                .limit(limit)
                .stream()
            )
            return [comp.to_dict() for comp in comparisons]
        except Exception as e:
            print(f"Error getting comparisons: {e}")
            return []

    # Notifications
    def create_notification(self, user_id: str, notification_data: Dict[str, Any]) -> Optional[str]:
        """Create notification"""
        if not self.db:
            return None
        try:
            notif_ref = self.db.collection("notifications").document()
            notification_data["notification_id"] = notif_ref.id
            notification_data["user_id"] = user_id
            notification_data["sent_at"] = datetime.now()
            notification_data["read"] = False
            notif_ref.set(notification_data)
            return notif_ref.id
        except Exception as e:
            print(f"Error creating notification: {e}")
            return None

    def get_user_notifications(self, user_id: str, unread_only: bool = False) -> List[Dict[str, Any]]:
        """Get user notifications"""
        if not self.db:
            return []
        try:
            query = self.db.collection("notifications").where("user_id", "==", user_id)
            
            if unread_only:
                query = query.where("read", "==", False)
            
            notifications = query.order_by("sent_at", direction=firestore.Query.DESCENDING).limit(50).stream()
            return [notif.to_dict() for notif in notifications]
        except Exception as e:
            print(f"Error getting notifications: {e}")
            return []

    def mark_notification_read(self, notification_id: str) -> bool:
        """Mark notification as read"""
        if not self.db:
            return False
        try:
            self.db.collection("notifications").document(notification_id).update({"read": True})
            return True
        except Exception as e:
            print(f"Error marking notification read: {e}")
            return False

    # Push tokens
    def save_push_token(self, user_id: str, token: str) -> bool:
        """Save Expo push token for user"""
        if not self.db:
            return False
        try:
            self.db.collection("push_tokens").document(user_id).set({
                "user_id": user_id,
                "token": token,
                "updated_at": datetime.now()
            })
            return True
        except Exception as e:
            print(f"Error saving push token: {e}")
            return False

    def get_push_token(self, user_id: str) -> Optional[str]:
        """Get Expo push token for user"""
        if not self.db:
            return None
        try:
            token_doc = self.db.collection("push_tokens").document(user_id).get()
            if token_doc.exists:
                return token_doc.to_dict().get("token")
            return None
        except Exception as e:
            print(f"Error getting push token: {e}")
            return None
