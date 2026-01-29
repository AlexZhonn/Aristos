from fastapi import APIRouter, HTTPException, Depends
from models.user import User, UserCreate, UserUpdate, UserPreferences
from services.firebase_service import FirebaseService
from middleware.auth import get_current_user
from typing import Dict, Any

router = APIRouter(prefix="/api/auth", tags=["authentication"])
firebase_service = FirebaseService()


@router.post("/register", response_model=Dict[str, Any])
async def register(user_data: UserCreate):
    """Register a new user (handled by Firebase Auth on client side, this creates the Firestore document)"""
    try:
        # This endpoint is called after Firebase Auth creates the user
        # We just create the Firestore document here
        return {
            "message": "Registration endpoint - use Firebase Auth on client side",
            "status": "client_side_registration"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/setup-profile")
async def setup_profile(
    preferences: UserPreferences,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Set up user profile after Firebase Auth registration"""
    try:
        user_data = {
            "uid": current_user["uid"],
            "email": current_user["email"],
            "display_name": current_user.get("display_name", ""),
            "preferences": preferences.dict()
        }
        
        success = firebase_service.create_user(current_user["uid"], user_data)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to create profile")
        
        return {"message": "Profile created successfully", "user": user_data}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/me")
async def get_current_user_profile(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Get current authenticated user"""
    return current_user


@router.put("/profile")
async def update_profile(
    user_update: UserUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Update user profile"""
    try:
        update_data = {}
        
        if user_update.display_name is not None:
            update_data["display_name"] = user_update.display_name
        
        if user_update.preferences is not None:
            update_data["preferences"] = user_update.preferences.dict()
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No update data provided")
        
        success = firebase_service.update_user(current_user["uid"], update_data)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to update profile")
        
        return {"message": "Profile updated successfully", "updated_fields": list(update_data.keys())}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
