from openai import OpenAI
import os
from typing import List, Dict, Any
import json


class RecipeMatcher:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def find_recipes_for_ingredients(self, ingredients: List[str], dietary_restrictions: List[str] = []) -> List[Dict[str, Any]]:
        """Find recipe suggestions based on available ingredients"""
        try:
            ingredients_text = ", ".join(ingredients)
            restrictions_text = ", ".join(dietary_restrictions) if dietary_restrictions else "none"

            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": """You are a recipe expert. Suggest 3 recipes using available ingredients.
                        Return JSON array: [{name, ingredients_needed: [from list], additional_ingredients: [to buy], 
                        prep_time, calories, difficulty, instructions: [brief steps]}]
                        Prioritize using ingredients that will expire soon."""
                    },
                    {
                        "role": "user",
                        "content": f"Suggest recipes using: {ingredients_text}. Dietary restrictions: {restrictions_text}. Return ONLY valid JSON array."
                    }
                ],
                max_tokens=1500
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
            print(f"Recipe matching error: {e}")
            return []

    def generate_meal_plan(self, pantry_items: List[Dict[str, Any]], days: int = 3) -> List[Dict[str, Any]]:
        """Generate a meal plan based on pantry items"""
        try:
            # Extract ingredient names, prioritizing expiring items
            sorted_items = sorted(pantry_items, key=lambda x: x.get("expiration_date", "9999-12-31"))
            ingredients = [item["name"] for item in sorted_items[:15]]  # Top 15 expiring
            
            ingredients_text = ", ".join(ingredients)

            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": f"""You are a meal planning expert. Create a {days}-day meal plan using available ingredients.
                        Return JSON array of days: [{{
                            day, 
                            breakfast: {{name, ingredients, calories}}, 
                            lunch: {{name, ingredients, calories}}, 
                            dinner: {{name, ingredients, calories}}
                        }}]
                        Use expiring ingredients first."""
                    },
                    {
                        "role": "user",
                        "content": f"Create {days}-day meal plan with: {ingredients_text}. Return ONLY valid JSON."
                    }
                ],
                max_tokens=2000
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
            print(f"Meal plan generation error: {e}")
            return []

    def suggest_shopping_list(self, desired_meals: List[str], pantry_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate shopping list for desired meals"""
        try:
            meals_text = ", ".join(desired_meals)
            have_ingredients = [item["name"] for item in pantry_items]
            have_text = ", ".join(have_ingredients)

            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": """You are a shopping assistant. Generate a shopping list for meals.
                        Return JSON array: [{item, quantity, unit, estimated_price, category}]
                        Only include items not already available."""
                    },
                    {
                        "role": "user",
                        "content": f"Shopping list for: {meals_text}. Already have: {have_text}. Return ONLY valid JSON array."
                    }
                ],
                max_tokens=1000
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
            print(f"Shopping list generation error: {e}")
            return []
