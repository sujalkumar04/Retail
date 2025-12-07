"""Loyalty agent for points and promotions"""

from typing import Dict
from .base_agent import BaseAgent
from config.prompts import PromptTemplates


class LoyaltyAgent(BaseAgent):
    """AI agent for loyalty and promotions"""
    
    def __init__(self):
        super().__init__("LoyaltyAgent")
    
    def get_system_prompt(self, context: Dict) -> str:
        """Get loyalty agent system prompt"""
        customer = context.get("customer") or {}
        promotions = context.get("active_promotions") or []
        coupons = context.get("available_coupons") or []
        
        # Customer loyalty info
        loyalty_tier = customer.get("loyalty_tier", "Bronze")
        points_balance = customer.get("loyalty_points", 0)
        expiring_points = 0  # Mock
        member_since = customer.get("member_since", "Recently")
        
        # Format promotions
        promo_text = self._format_promotions(promotions)
        coupon_text = self._format_coupons(coupons)
        
        # Fill in prompt template
        prompt = PromptTemplates.LOYALTY_AGENT.format(
            loyalty_tier=loyalty_tier,
            points_balance=points_balance,
            expiring_points=expiring_points,
            member_since=member_since,
            active_promotions=promo_text,
            available_coupons=coupon_text
        )
        
        return prompt
    
    def _format_promotions(self, promotions: list) -> str:
        """Format active promotions"""
        if not promotions:
            return "No active promotions"
        
        formatted = []
        for promo in promotions[:5]:
            formatted.append(f"- {promo.get('name')}: {promo.get('description')}")
        
        return "\n".join(formatted)
    
    def _format_coupons(self, coupons: list) -> str:
        """Format available coupons"""
        if not coupons:
            return "No coupons available"
        
        formatted = []
        for coupon in coupons[:5]:
            formatted.append(f"- {coupon.get('code')}: {coupon.get('description')}")
        
        return "\n".join(formatted)
    
    def can_handle(self, user_message: str, context: Dict) -> bool:
        """Check if message is about loyalty/promotions"""
        keywords = [
            "points", "loyalty", "reward", "discount", "offer",
            "promotion", "coupon", "code", "save", "deal"
        ]
        message_lower = user_message.lower()
        return any(keyword in message_lower for keyword in keywords)
