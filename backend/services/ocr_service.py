import base64
from openai import OpenAI
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
import json


class OCRService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def process_receipt(self, image_base64: str) -> Dict[str, Any]:
        """Process receipt image using OpenAI Vision API"""
        try:
            # Remove data URL prefix if present
            if "," in image_base64:
                image_base64 = image_base64.split(",")[1]

            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": """You are a receipt analyzer. Extract all items from the receipt with their prices and quantities. 
                        Return a JSON object with:
                        - store_name: string
                        - purchase_date: ISO date string (estimate if not clear)
                        - total_amount: float
                        - items: array of {name: string, quantity: float, price: float, unit: string}
                        
                        Be precise with numbers. If quantity is not specified, assume 1."""
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Extract all information from this receipt. Return ONLY valid JSON, no markdown formatting."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_base64}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=2000
            )

            content = response.choices[0].message.content
            # Clean up response - remove markdown code blocks if present
            content = content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()

            receipt_data = json.loads(content)
            
            # Ensure purchase_date is datetime
            if "purchase_date" in receipt_data and isinstance(receipt_data["purchase_date"], str):
                try:
                    receipt_data["purchase_date"] = datetime.fromisoformat(receipt_data["purchase_date"].replace("Z", "+00:00"))
                except:
                    receipt_data["purchase_date"] = datetime.now()
            else:
                receipt_data["purchase_date"] = datetime.now()

            return receipt_data

        except Exception as e:
            print(f"OCR error: {e}")
            raise Exception(f"Failed to process receipt: {str(e)}")

    def enhance_with_nutrition(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Add nutrition information to receipt items"""
        try:
            items_text = ", ".join([item["name"] for item in items])
            
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": """You are a nutrition expert. For each food item, estimate calories and protein per typical serving.
                        Return JSON array with same order: [{name, calories, protein}]
                        Use reasonable estimates for grocery items. If it's a non-food item, set calories and protein to 0."""
                    },
                    {
                        "role": "user",
                        "content": f"Provide nutrition data for these items: {items_text}. Return ONLY valid JSON array."
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

            nutrition_data = json.loads(content)

            # Merge nutrition data with items
            for i, item in enumerate(items):
                if i < len(nutrition_data):
                    item["calories"] = nutrition_data[i].get("calories", 0)
                    item["protein"] = nutrition_data[i].get("protein", 0)

            return items

        except Exception as e:
            print(f"Nutrition enhancement error: {e}")
            # Return items without nutrition data
            for item in items:
                item["calories"] = 0
                item["protein"] = 0
            return items
