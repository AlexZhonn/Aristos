from openai import OpenAI
import os
from typing import Dict, Any, Optional
import json


class NutritionService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def get_food_nutrition(self, food_name: str, quantity: float = 1.0, unit: str = "serving") -> Dict[str, Any]:
        """Get nutrition information for a food item"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": """You are a nutrition expert. Provide detailed nutrition information for food items.
                        Return JSON: {calories, protein, carbs, fat, fiber, sugar, sodium}
                        All values in grams except calories (kcal) and sodium (mg)."""
                    },
                    {
                        "role": "user",
                        "content": f"Nutrition data for {quantity} {unit} of {food_name}. Return ONLY valid JSON."
                    }
                ],
                max_tokens=300
            )

            content = response.choices[0].message.content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()

            return json.loads(content)

        except Exception as e:
            print(f"Nutrition lookup error: {e}")
            return {
                "calories": 0,
                "protein": 0,
                "carbs": 0,
                "fat": 0,
                "fiber": 0,
                "sugar": 0,
                "sodium": 0
            }

    def estimate_recipe_nutrition(self, recipe_name: str, ingredients: list[str]) -> Dict[str, Any]:
        """Estimate nutrition for a home-cooked recipe"""
        try:
            ingredients_text = ", ".join(ingredients)
            
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": """You are a nutrition expert. Estimate total nutrition for a recipe.
                        Return JSON: {calories, protein, carbs, fat, servings, calories_per_serving}"""
                    },
                    {
                        "role": "user",
                        "content": f"Estimate nutrition for {recipe_name} using: {ingredients_text}. Return ONLY valid JSON."
                    }
                ],
                max_tokens=300
            )

            content = response.choices[0].message.content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()

            return json.loads(content)

        except Exception as e:
            print(f"Recipe nutrition error: {e}")
            return {
                "calories": 0,
                "protein": 0,
                "carbs": 0,
                "fat": 0,
                "servings": 1,
                "calories_per_serving": 0
            }
