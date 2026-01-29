from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from models.receipt import Receipt, ReceiptCreate, ReceiptUpdate
from services.firebase_service import FirebaseService
from services.ocr_service import OCRService
from middleware.auth import get_current_user
from typing import Dict, Any, List
import base64

router = APIRouter(prefix="/api/receipts", tags=["receipts"])
firebase_service = FirebaseService()
ocr_service = OCRService()


@router.post("/upload")
async def upload_receipt(
    receipt_data: ReceiptCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Upload and process a receipt image"""
    try:
        # Process receipt with OCR
        processed_data = ocr_service.process_receipt(receipt_data.image_base64)
        
        # Enhance with nutrition data
        if "items" in processed_data:
            processed_data["items"] = ocr_service.enhance_with_nutrition(processed_data["items"])
        
        # Create receipt in Firestore
        receipt_id = firebase_service.create_receipt(current_user["uid"], processed_data)
        
        if not receipt_id:
            raise HTTPException(status_code=500, detail="Failed to save receipt")
        
        # Automatically add items to pantry
        if "items" in processed_data:
            from services.expiration_service import ExpirationService
            from datetime import datetime
            
            for item in processed_data["items"]:
                # Determine category (simplified logic)
                category = "pantry"  # Default
                item_lower = item["name"].lower()
                
                if any(word in item_lower for word in ["milk", "cheese", "yogurt", "butter"]):
                    category = "dairy"
                elif any(word in item_lower for word in ["chicken", "beef", "pork", "fish", "meat"]):
                    category = "meat"
                elif any(word in item_lower for word in ["apple", "banana", "lettuce", "tomato", "vegetable", "fruit"]):
                    category = "produce"
                elif any(word in item_lower for word in ["frozen", "ice cream"]):
                    category = "frozen"
                
                purchase_date = processed_data.get("purchase_date", datetime.now())
                expiration_date = ExpirationService.estimate_expiration_date(
                    item["name"],
                    category,
                    purchase_date
                )
                
                pantry_item = {
                    "name": item["name"],
                    "category": category,
                    "quantity": item.get("quantity", 1.0),
                    "unit": item.get("unit", "item"),
                    "purchase_date": purchase_date,
                    "expiration_date": expiration_date,
                    "calories": item.get("calories", 0),
                    "protein": item.get("protein", 0),
                    "receipt_id": receipt_id,
                    "consumed": False
                }
                
                firebase_service.create_pantry_item(current_user["uid"], pantry_item)
        
        processed_data["receipt_id"] = receipt_id
        return processed_data
        
    except Exception as e:
        print(f"Receipt upload error: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/")
async def get_receipts(
    current_user: Dict[str, Any] = Depends(get_current_user),
    limit: int = 50
):
    """Get all receipts for the current user"""
    try:
        receipts = firebase_service.get_user_receipts(current_user["uid"], limit)
        return receipts
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{receipt_id}")
async def get_receipt(
    receipt_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get a specific receipt"""
    try:
        receipt = firebase_service.get_receipt(receipt_id)
        
        if not receipt:
            raise HTTPException(status_code=404, detail="Receipt not found")
        
        # Verify ownership
        if receipt.get("user_id") != current_user["uid"]:
            raise HTTPException(status_code=403, detail="Not authorized")
        
        return receipt
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{receipt_id}")
async def update_receipt(
    receipt_id: str,
    receipt_update: ReceiptUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Update a receipt"""
    try:
        # Verify ownership
        receipt = firebase_service.get_receipt(receipt_id)
        if not receipt:
            raise HTTPException(status_code=404, detail="Receipt not found")
        if receipt.get("user_id") != current_user["uid"]:
            raise HTTPException(status_code=403, detail="Not authorized")
        
        # Update
        update_data = receipt_update.dict(exclude_unset=True)
        success = firebase_service.update_receipt(receipt_id, update_data)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to update receipt")
        
        return {"message": "Receipt updated successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{receipt_id}")
async def delete_receipt(
    receipt_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Delete a receipt"""
    try:
        # Verify ownership
        receipt = firebase_service.get_receipt(receipt_id)
        if not receipt:
            raise HTTPException(status_code=404, detail="Receipt not found")
        if receipt.get("user_id") != current_user["uid"]:
            raise HTTPException(status_code=403, detail="Not authorized")
        
        # Delete
        success = firebase_service.delete_receipt(receipt_id)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to delete receipt")
        
        return {"message": "Receipt deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
