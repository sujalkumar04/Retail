"""Payment agent for checkout"""

from typing import Dict
from .base_agent import BaseAgent
from config.prompts import PromptTemplates


class PaymentAgent(BaseAgent):
    """AI agent for payment processing"""
    
    def __init__(self):
        super().__init__("PaymentAgent")
    
    def get_system_prompt(self, context: Dict) -> str:
        """Get payment agent system prompt"""
        customer = context.get("customer") or {}
        order_details = context.get("order_details") or {}
        
        # Format saved payment methods
        saved_methods = customer.get("saved_payment_methods", [])
        methods_text = self._format_payment_methods(saved_methods)
        
        # Get loyalty points
        loyalty_points = customer.get("loyalty_points", 0)
        
        # Gift card balance (mock)
        gift_card_balance = 0
        
        # Format order details
        order_text = self._format_order_details(order_details)
        
        # Fill in prompt template
        prompt = PromptTemplates.PAYMENT_AGENT.format(
            saved_methods=methods_text,
            loyalty_points=loyalty_points,
            gift_card_balance=gift_card_balance,
            order_details=order_text
        )
        
        return prompt
    
    def _format_payment_methods(self, methods: list) -> str:
        """Format saved payment methods"""
        if not methods:
            return "No saved payment methods"
        
        formatted = []
        for method in methods:
            if method.get("type") == "card":
                formatted.append(f"{method.get('brand')} ending in {method.get('last_four')}")
            elif method.get("type") == "upi":
                formatted.append(f"UPI: {method.get('id')}")
        
        return "; ".join(formatted) if formatted else "No saved methods"
    
    def _format_order_details(self, order: Dict) -> str:
        """Format order details"""
        if not order:
            return "No order details available"
        
        parts = []
        parts.append(f"Subtotal: ₹{order.get('subtotal', 0):,.0f}")
        
        discount = order.get('discount', 0)
        if discount > 0:
            parts.append(f"Discount: -₹{discount:,.0f}")
        
        shipping = order.get('shipping_fee', 0)
        if shipping > 0:
            parts.append(f"Shipping: ₹{shipping:,.0f}")
        
        parts.append(f"Total: ₹{order.get('total', 0):,.0f}")
        
        return "\n".join(parts)
    
    def can_handle(self, user_message: str, context: Dict) -> bool:
        """Check if message is about payment"""
        keywords = [
            "pay", "payment", "checkout", "buy", "purchase",
            "card", "upi", "cod", "cash on delivery"
        ]
        message_lower = user_message.lower()
        return any(keyword in message_lower for keyword in keywords)
