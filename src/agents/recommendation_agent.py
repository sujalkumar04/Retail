"""Recommendation agent for product suggestions"""

from typing import Dict, List
from .base_agent import BaseAgent
from config.prompts import PromptTemplates


class RecommendationAgent(BaseAgent):
    """AI agent for personalized product recommendations"""
    
    def __init__(self):
        super().__init__("RecommendationAgent")
    
    def get_system_prompt(self, context: Dict) -> str:
        """Get recommendation agent system prompt"""
        customer = context.get("customer") or {}
        products = context.get("available_products") or []
        
        # Format customer profile
        customer_profile = self._format_customer_profile(customer)
        
        # Format product catalog
        product_catalog = self._format_product_catalog(products)
        
        # Fill in prompt template
        prompt = PromptTemplates.RECOMMENDATION_AGENT.format(
            customer_profile=customer_profile,
            product_catalog=product_catalog
        )
        
        return prompt
    
    def _format_customer_profile(self, customer: Dict) -> str:
        """Format customer profile for prompt"""
        if not customer:
            return "New customer, no profile available"
        
        profile_parts = []
        
        # Basic info
        profile_parts.append(f"Name: {customer.get('name', 'Unknown')}")
        profile_parts.append(f"Loyalty Tier: {customer.get('loyalty_tier', 'Bronze')}")
        
        # Preferences
        preferences = customer.get("preferences", {})
        if preferences:
            styles = preferences.get("styles", [])
            if styles:
                profile_parts.append(f"Preferred Styles: {', '.join(styles)}")
            
            colors = preferences.get("colors", [])
            if colors:
                profile_parts.append(f"Preferred Colors: {', '.join(colors)}")
            
            budget = preferences.get("budget_range", "mid")
            profile_parts.append(f"Budget Range: {budget}")
        
        # Purchase history
        purchase_history = customer.get("purchase_history", [])
        if purchase_history:
            recent = purchase_history[-3:]
            history_text = "; ".join([
                f"{item.get('date')}: {len(item.get('items', []))} items"
                for item in recent
            ])
            profile_parts.append(f"Recent Purchases: {history_text}")
        
        return "\n".join(profile_parts)
    
    def _format_product_catalog(self, products: List) -> str:
        """Format product catalog for prompt"""
        if not products:
            return "No products available"
        
        catalog_parts = []
        for product in products[:10]:  # Limit to 10 products
            product_info = (
                f"- {product.get('name')} ({product.get('sku')}): "
                f"₹{product.get('price')} "
                f"[{product.get('category')}] "
                f"{product.get('description', '')[:100]}"
            )
            catalog_parts.append(product_info)
        
        return "\n".join(catalog_parts)
    
    def can_handle(self, user_message: str, context: Dict) -> bool:
        """Check if message is asking for recommendations"""
        keywords = [
            "recommend", "suggestion", "what should", "help me find",
            "looking for", "show me", "similar", "like this"
        ]
        message_lower = user_message.lower()
        return any(keyword in message_lower for keyword in keywords)
