"""Sales agent for customer interactions"""

from typing import Dict
from .base_agent import BaseAgent
from config.prompts import PromptTemplates
from config.settings import settings


class SalesAgent(BaseAgent):
    """AI Sales Associate for customer interactions"""
    
    def __init__(self):
        super().__init__("SalesAgent")
    
    def get_system_prompt(self, context: Dict) -> str:
        """Get sales agent system prompt"""
        session = context.get("session")
        customer = context.get("customer") or {}
        cart = context.get("cart") or {}
        promotions = context.get("active_promotions", [])
        
        # Extract customer info
        customer_name = customer.get("name", "Valued Customer")
        loyalty_tier = customer.get("loyalty_tier", "Bronze")
        purchase_history = customer.get("purchase_summary", "No previous purchases")
        
        # Extract cart info
        cart_items = cart.get("summary", "Empty cart")
        
        # Extract channel
        channel = session.channel if session else "web_chat"
        
        # Format promotions
        promo_text = "None active"
        if promotions:
            promo_text = "; ".join([p.get("name", "") for p in promotions[:3]])
        
        # Fill in prompt template
        prompt = PromptTemplates.SALES_AGENT_SYSTEM.format(
            store_name=settings.store_name,
            channel=channel,
            customer_name=customer_name,
            loyalty_tier=loyalty_tier,
            purchase_history=purchase_history,
            cart_items=cart_items,
            active_promotions=promo_text
        )
        
        # Add channel adaptation
        channel_guidance = PromptTemplates.CHANNEL_ADAPTATION.get(channel, "")
        if channel_guidance:
            prompt += f"\n\nCHANNEL GUIDANCE: {channel_guidance}"
        
        return prompt
    
    def can_handle(self, user_message: str, context: Dict) -> bool:
        """Sales agent handles general queries and browsing"""
        # Sales agent is the default handler
        return True
