from fastapi import APIRouter, HTTPException, Depends
from models.ingredient import Ingredient, IngredientCreate, IngredientUpdate
from services.firebase_service import FirebaseService
from services.expiration_service import ExpirationService
from middleware.auth import get_current_user
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/pantry", tags=["pantry"])
firebase_service = FirebaseService()
expiration_service = ExpirationService()


@router.get("/")
async def get_pantry(
    current_user: Dict[str, Any] = Depends(get_current_user),
    category: Optional[str] = None
):
    """Get all pantry items for the current user"""
    try:
        items = firebase_service.get_user_pantry(current_user["uid"], category)
        
        # Add urgency level to each item
        for item in items:
            exp_date = item.get("expiration_date")
            if isinstance(exp_date, str):
                exp_date = datetime.fromisoformat(exp_date.replace("Z", "+00:00"))
            
            if exp_date:
                item["urgency"] = expiration_service.get_urgency_level(exp_date)
                item["urgency_color"] = expiration_service.get_urgency_color(item["urgency"])
                item["days_until_expiration"] = (exp_date - datetime.now()).days
        
        return items
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/expiring")
async def get_expiring_items(
    current_user: Dict[str, Any] = Depends(get_current_user),
    days: int = 3
):
    """Get items expiring within specified days"""
    try:
        cutoff_date = datetime.now() + timedelta(days=days)
        items = firebase_service.get_expiring_items(current_user["uid"], cutoff_date)
        
        # Add urgency info
        for item in items:
            exp_date = item.get("expiration_date")
            if isinstance(exp_date, str):
                exp_date = datetime.fromisoformat(exp_date.replace("Z", "+00:00"))
            
            if exp_date:
                item["urgency"] = expiration_service.get_urgency_level(exp_date)
                item["urgency_color"] = expiration_service.get_urgency_color(item["urgency"])
                item["days_until_expiration"] = (exp_date - datetime.now()).days
        
        return items
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/")
async def add_pantry_item(
    item_data: IngredientCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Manually add an item to pantry"""
    try:
        # Set defaults
        purchase_date = item_data.purchase_date or datetime.now()
        
        # Estimate expiration if not provided
        if item_data.expiration_date:
            expiration_date = item_data.expiration_date
        else:
            expiration_date = expiration_service.estimate_expiration_date(
                item_data.name,
                item_data.category,
                purchase_date
            )
        
        # Create pantry item
        pantry_item = {
            "name": item_data.name,
            "category": item_data.category,
            "quantity": item_data.quantity,
            "unit": item_data.unit,
            "purchase_date": purchase_date,
            "expiration_date": expiration_date,
            "calories": item_data.calories or 0,
            "protein": item_data.protein or 0,
            "consumed": False
        }
        
        item_id = firebase_service.create_pantry_item(current_user["uid"], pantry_item)
        
        if not item_id:
            raise HTTPException(status_code=500, detail="Failed to create pantry item")
        
        pantry_item["item_id"] = item_id
        return pantry_item
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{item_id}")
async def update_pantry_item(
    item_id: str,
    item_update: IngredientUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Update a pantry item"""
    try:
        update_data = item_update.dict(exclude_unset=True)
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No update data provided")
        
        success = firebase_service.update_pantry_item(item_id, update_data)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to update item")
        
        return {"message": "Item updated successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{item_id}/consume")
async def mark_consumed(
    item_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Mark a pantry item as consumed"""
    try:
        update_data = {
            "consumed": True,
            "consumed_date": datetime.now()
        }
        
        success = firebase_service.update_pantry_item(item_id, update_data)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to mark as consumed")
        
        return {"message": "Item marked as consumed"}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{item_id}")
async def delete_pantry_item(
    item_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Delete a pantry item"""
    try:
        success = firebase_service.delete_pantry_item(item_id)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to delete item")
        
        return {"message": "Item deleted successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
