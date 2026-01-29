from openai import OpenAI
import os
from typing import Dict, Any, Optional
import json


class DeliveryAnalyzer:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def analyze_delivery_item(self, item_name: str, restaurant: str, price: float, image_base64: Optional[str] = None) -> Dict[str, Any]:
        """Analyze a delivery item and extract nutrition info"""
        try:
            messages = [
                {
                    "role": "system",
                    "content": """You are a food analyst. Analyze the delivery food item and provide:
                    - Estimated calories
                    - Main ingredients list
                    - Serving size
                    Return JSON: {calories, ingredients: [list], serving_size, description}"""
                }
            ]

            if image_base64:
                # Clean up base64 string
                if "," in image_base64:
                    image_base64 = image_base64.split(",")[1]

                messages.append({
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"Analyze this {item_name} from {restaurant} (${price}). Return ONLY valid JSON."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ]
                })
            else:
                messages.append({
                    "role": "user",
                    "content": f"Analyze {item_name} from {restaurant} (${price}). Return ONLY valid JSON."
                })

            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=500
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
            print(f"Delivery analysis error: {e}")
            return {
                "calories": 0,
                "ingredients": [],
                "serving_size": "1 serving",
                "description": item_name
            }

    def suggest_home_alternative(self, delivery_item: str, delivery_price: float, ingredients: list[str]) -> Dict[str, Any]:
        """Suggest a home cooking alternative"""
        try:
            ingredients_text = ", ".join(ingredients) if ingredients else delivery_item

            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": """You are a recipe expert. Suggest a home-cooked alternative to a delivery item.
                        Return JSON: {
                            recipe_name, 
                            estimated_cost, 
                            ingredients: [list with quantities], 
                            calories, 
                            prep_time (minutes),
                            cooking_steps: [brief steps]
                        }
                        Be realistic with costs and portions."""
                    },
                    {
                        "role": "user",
                        "content": f"Suggest home alternative for '{delivery_item}' (delivery: ${delivery_price}). Main ingredients: {ingredients_text}. Return ONLY valid JSON."
                    }
                ],
                max_tokens=800
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
            print(f"Alternative suggestion error: {e}")
            return {
                "recipe_name": f"Homemade {delivery_item}",
                "estimated_cost": delivery_price * 0.4,
                "ingredients": ingredients or ["basic ingredients"],
                "calories": 0,
                "prep_time": 30,
                "cooking_steps": ["Prepare ingredients", "Cook", "Serve"]
            }

    def generate_recommendation(self, delivery_price: float, home_cost: float, delivery_calories: float, home_calories: float) -> str:
        """Generate a recommendation based on comparison"""
        savings = delivery_price - home_cost
        calorie_diff = delivery_calories - home_calories
        
        recommendation_parts = []
        
        # Cost analysis
        if savings > 10:
            recommendation_parts.append(f"💰 You could save ${savings:.2f} by cooking at home!")
        elif savings > 5:
            recommendation_parts.append(f"💵 Save ${savings:.2f} by cooking yourself.")
        elif savings > 0:
            recommendation_parts.append(f"Small savings of ${savings:.2f} with home cooking.")
        else:
            recommendation_parts.append("Delivery is similarly priced, but home cooking gives you control over ingredients.")

        # Calorie analysis
        if calorie_diff > 300:
            recommendation_parts.append(f"🥗 Home cooking can save you ~{int(calorie_diff)} calories!")
        elif calorie_diff > 100:
            recommendation_parts.append(f"Home version is lighter by ~{int(calorie_diff)} calories.")
        elif calorie_diff < -100:
            recommendation_parts.append("Home version may be more filling and nutritious.")

        # Overall recommendation
        if savings > 5 or calorie_diff > 200:
            recommendation_parts.append("✅ Recommendation: Cook at home for better value and health!")
        elif savings > 0:
            recommendation_parts.append("👍 Cooking at home is a good option.")
        else:
            recommendation_parts.append("Either option works - consider your time and mood!")

        return " ".join(recommendation_parts)
