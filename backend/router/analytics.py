from fastapi import APIRouter, HTTPException, Depends
from services.firebase_service import FirebaseService
from services.analytics_service import AnalyticsService
from middleware.auth import get_current_user
from typing import Dict, Any

router = APIRouter(prefix="/api/analytics", tags=["analytics"])
firebase_service = FirebaseService()
analytics_service = AnalyticsService()


@router.get("/spending")
async def get_spending_trends(
    current_user: Dict[str, Any] = Depends(get_current_user),
    days: int = 14
):
    """Get spending trends over time"""
    try:
        receipts = firebase_service.get_user_receipts(current_user["uid"], limit=200)
        trends = analytics_service.calculate_spending_trends(receipts, days)
        return trends
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/calories")
async def get_calorie_trends(
    current_user: Dict[str, Any] = Depends(get_current_user),
    days: int = 14
):
    """Get calorie consumption trends"""
    try:
        receipts = firebase_service.get_user_receipts(current_user["uid"], limit=200)
        
        # Get consumed pantry items (you might want to add a filter for this in firebase_service)
        pantry_items = firebase_service.get_user_pantry(current_user["uid"])
        consumed_items = [item for item in pantry_items if item.get("consumed", False)]
        
        trends = analytics_service.calculate_calorie_trends(receipts, consumed_items, days)
        return trends
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/waste")
async def get_waste_stats(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get food waste statistics"""
    try:
        pantry_items = firebase_service.get_user_pantry(current_user["uid"])
        stats = analytics_service.calculate_waste_stats(pantry_items)
        return stats
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/savings")
async def get_savings_stats(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get savings from home cooking vs delivery"""
    try:
        comparisons = firebase_service.get_user_comparisons(current_user["uid"], limit=200)
        savings = analytics_service.calculate_savings(comparisons)
        return savings
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/today")
async def get_today_summary(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get today's summary statistics"""
    try:
        receipts = firebase_service.get_user_receipts(current_user["uid"], limit=50)
        
        # Get consumed pantry items
        pantry_items = firebase_service.get_user_pantry(current_user["uid"])
        consumed_items = [item for item in pantry_items if item.get("consumed", False)]
        
        # Get user's daily budget
        budget = current_user.get("preferences", {}).get("daily_budget", 50.0)
        
        summary = analytics_service.get_today_summary(receipts, consumed_items, budget)
        return summary
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
