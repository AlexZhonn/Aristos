from fastapi import APIRouter, HTTPException, Depends
from models.comparison import Comparison, ComparisonCreate, ComparisonResponse
from services.firebase_service import FirebaseService
from services.delivery_analyzer import DeliveryAnalyzer
from middleware.auth import get_current_user
from typing import Dict, Any

router = APIRouter(prefix="/api/compare", tags=["comparisons"])
firebase_service = FirebaseService()
delivery_analyzer = DeliveryAnalyzer()


@router.post("/analyze", response_model=ComparisonResponse)
async def analyze_delivery(
    comparison_data: ComparisonCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Analyze delivery item and suggest home cooking alternative"""
    try:
        delivery_item = comparison_data.delivery_item
        
        # Analyze delivery item
        analysis = delivery_analyzer.analyze_delivery_item(
            delivery_item.name,
            delivery_item.restaurant,
            delivery_item.price,
            comparison_data.image_base64
        )
        
        # Get home cooking alternative
        home_alternative = delivery_analyzer.suggest_home_alternative(
            delivery_item.name,
            delivery_item.price,
            analysis.get("ingredients", [])
        )
        
        # Calculate savings and calorie difference
        savings = delivery_item.price - home_alternative.get("estimated_cost", 0)
        
        delivery_calories = analysis.get("calories", 0) or delivery_item.calories or 0
        home_calories = home_alternative.get("calories", 0)
        calorie_difference = delivery_calories - home_calories if home_calories else None
        
        # Generate recommendation
        recommendation = delivery_analyzer.generate_recommendation(
            delivery_item.price,
            home_alternative.get("estimated_cost", 0),
            delivery_calories,
            home_calories
        )
        
        # Create comparison object
        comparison = {
            "user_id": current_user["uid"],
            "delivery_item": {
                "name": delivery_item.name,
                "restaurant": delivery_item.restaurant,
                "price": delivery_item.price,
                "calories": delivery_calories
            },
            "home_cooking_alternative": {
                "recipe_name": home_alternative.get("recipe_name", f"Homemade {delivery_item.name}"),
                "estimated_cost": home_alternative.get("estimated_cost", 0),
                "ingredients": home_alternative.get("ingredients", []),
                "calories": home_calories,
                "prep_time": home_alternative.get("prep_time", 30)
            },
            "savings": round(savings, 2),
            "calorie_difference": round(calorie_difference, 0) if calorie_difference else None
        }
        
        # Save to Firestore
        comparison_id = firebase_service.create_comparison(current_user["uid"], comparison)
        comparison["comparison_id"] = comparison_id
        
        return {
            "comparison": comparison,
            "recommendation": recommendation
        }
        
    except Exception as e:
        print(f"Comparison error: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/history")
async def get_comparison_history(
    current_user: Dict[str, Any] = Depends(get_current_user),
    limit: int = 50
):
    """Get comparison history for current user"""
    try:
        comparisons = firebase_service.get_user_comparisons(current_user["uid"], limit)
        return comparisons
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{comparison_id}")
async def get_comparison(
    comparison_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get a specific comparison"""
    try:
        # Get from history (implementation depends on Firestore structure)
        comparisons = firebase_service.get_user_comparisons(current_user["uid"], 100)
        
        for comp in comparisons:
            if comp.get("comparison_id") == comparison_id:
                return comp
        
        raise HTTPException(status_code=404, detail="Comparison not found")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
