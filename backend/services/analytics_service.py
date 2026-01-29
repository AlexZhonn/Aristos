from typing import Dict, List, Any
from datetime import datetime, timedelta
from collections import defaultdict


class AnalyticsService:
    @staticmethod
    def calculate_spending_trends(receipts: List[Dict[str, Any]], days: int = 14) -> Dict[str, Any]:
        """Calculate spending trends over time"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        daily_spending = defaultdict(float)
        total_spent = 0.0
        
        for receipt in receipts:
            purchase_date = receipt.get("purchase_date")
            if isinstance(purchase_date, str):
                purchase_date = datetime.fromisoformat(purchase_date.replace("Z", "+00:00"))
            
            if purchase_date and purchase_date >= cutoff_date:
                date_key = purchase_date.strftime("%Y-%m-%d")
                amount = float(receipt.get("total_amount", 0))
                daily_spending[date_key] += amount
                total_spent += amount

        # Create data points for chart
        data_points = []
        current_date = datetime.now() - timedelta(days=days)
        
        for i in range(days):
            date_key = current_date.strftime("%Y-%m-%d")
            data_points.append({
                "date": date_key,
                "amount": round(daily_spending.get(date_key, 0), 2),
                "label": current_date.strftime("%d")
            })
            current_date += timedelta(days=1)

        average_daily = total_spent / days if days > 0 else 0

        return {
            "total_spent": round(total_spent, 2),
            "average_daily": round(average_daily, 2),
            "data_points": data_points,
            "days": days
        }

    @staticmethod
    def calculate_calorie_trends(receipts: List[Dict[str, Any]], pantry_consumed: List[Dict[str, Any]], days: int = 14) -> Dict[str, Any]:
        """Calculate calorie consumption trends"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        daily_calories = defaultdict(float)
        total_calories = 0.0
        
        # Add calories from consumed pantry items
        for item in pantry_consumed:
            consumed_date = item.get("consumed_date")
            if isinstance(consumed_date, str):
                consumed_date = datetime.fromisoformat(consumed_date.replace("Z", "+00:00"))
            
            if consumed_date and consumed_date >= cutoff_date:
                date_key = consumed_date.strftime("%Y-%m-%d")
                calories = float(item.get("calories", 0))
                daily_calories[date_key] += calories
                total_calories += calories

        # Create data points
        data_points = []
        current_date = datetime.now() - timedelta(days=days)
        
        for i in range(days):
            date_key = current_date.strftime("%Y-%m-%d")
            data_points.append({
                "date": date_key,
                "calories": round(daily_calories.get(date_key, 0), 0),
                "label": current_date.strftime("%d")
            })
            current_date += timedelta(days=1)

        average_daily = total_calories / days if days > 0 else 0

        return {
            "total_calories": round(total_calories, 0),
            "average_daily": round(average_daily, 0),
            "data_points": data_points,
            "days": days
        }

    @staticmethod
    def calculate_waste_stats(pantry_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate food waste statistics"""
        total_items = len(pantry_items)
        expired_items = []
        total_waste_value = 0.0
        
        now = datetime.now()
        
        for item in pantry_items:
            expiration_date = item.get("expiration_date")
            if isinstance(expiration_date, str):
                expiration_date = datetime.fromisoformat(expiration_date.replace("Z", "+00:00"))
            
            if expiration_date and expiration_date < now and not item.get("consumed", False):
                expired_items.append(item)
                # Estimate waste value (rough calculation)
                total_waste_value += 5.0  # Average $5 per wasted item

        waste_percentage = (len(expired_items) / total_items * 100) if total_items > 0 else 0

        return {
            "total_items": total_items,
            "expired_items": len(expired_items),
            "waste_percentage": round(waste_percentage, 1),
            "estimated_waste_value": round(total_waste_value, 2),
            "most_wasted_categories": AnalyticsService._get_waste_by_category(expired_items)
        }

    @staticmethod
    def _get_waste_by_category(expired_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Group wasted items by category"""
        category_counts = defaultdict(int)
        
        for item in expired_items:
            category = item.get("category", "other")
            category_counts[category] += 1

        return [
            {"category": cat, "count": count}
            for cat, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
        ][:5]

    @staticmethod
    def calculate_savings(comparisons: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate total savings from home cooking vs delivery"""
        total_savings = 0.0
        total_comparisons = len(comparisons)
        
        for comp in comparisons:
            savings = float(comp.get("savings", 0))
            total_savings += savings

        average_savings = total_savings / total_comparisons if total_comparisons > 0 else 0

        return {
            "total_savings": round(total_savings, 2),
            "average_savings_per_meal": round(average_savings, 2),
            "comparisons_made": total_comparisons,
            "projected_yearly_savings": round(average_savings * 365, 2) if total_comparisons > 0 else 0
        }

    @staticmethod
    def get_today_summary(receipts: List[Dict[str, Any]], pantry_consumed: List[Dict[str, Any]], budget: float) -> Dict[str, Any]:
        """Get today's summary statistics"""
        today = datetime.now().date()
        
        today_spending = 0.0
        today_calories = 0.0
        today_protein = 0.0
        
        # Today's receipts
        for receipt in receipts:
            purchase_date = receipt.get("purchase_date")
            if isinstance(purchase_date, str):
                purchase_date = datetime.fromisoformat(purchase_date.replace("Z", "+00:00"))
            
            if purchase_date and purchase_date.date() == today:
                today_spending += float(receipt.get("total_amount", 0))

        # Today's consumption
        for item in pantry_consumed:
            consumed_date = item.get("consumed_date")
            if isinstance(consumed_date, str):
                consumed_date = datetime.fromisoformat(consumed_date.replace("Z", "+00:00"))
            
            if consumed_date and consumed_date.date() == today:
                today_calories += float(item.get("calories", 0))
                today_protein += float(item.get("protein", 0))

        remaining_budget = budget - today_spending

        return {
            "spending": {
                "spent_today": round(today_spending, 2),
                "remaining_budget": round(remaining_budget, 2),
                "budget": round(budget, 2)
            },
            "nutrition": {
                "calories_today": round(today_calories, 0),
                "protein_today": round(today_protein, 1)
            }
        }
