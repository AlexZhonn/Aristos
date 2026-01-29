from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, Dict, Any
from services.firebase_service import FirebaseService

security = HTTPBearer()
firebase_service = FirebaseService()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> Dict[str, Any]:
    """
    Validate Firebase ID token and return user info
    """
    try:
        token = credentials.credentials
        decoded_token = firebase_service.verify_token(token)
        
        if not decoded_token:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication credentials"
            )
        
        # Get user data from Firestore
        user_data = firebase_service.get_user(decoded_token["uid"])
        
        if not user_data:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )
        
        return {
            "uid": decoded_token["uid"],
            "email": decoded_token.get("email"),
            **user_data
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Auth error: {e}")
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials"
        )


class AuthMiddleware:
    """Auth middleware for dependency injection"""
    pass
