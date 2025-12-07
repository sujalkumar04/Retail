"""Post-purchase agent for support"""

from typing import Dict
from .base_agent import BaseAgent
from config.prompts import PromptTemplates


class PostPurchaseAgent(BaseAgent):
    """AI agent for post-purchase support"""
    
    def __init__(self):
        super().__init__("PostPurchaseAgent")
    
    def get_system_prompt(self, context: Dict) -> str:
        """Get post-purchase agent system prompt"""
        customer = context.get("customer") or {}
        inquiry_details = context.get("inquiry_details", "General inquiry")
        
        # Format order history
        order_history = customer.get("purchase_history", [])
        history_text = self._format_order_history(order_history)
        
        # Fill in prompt template
        prompt = PromptTemplates.POST_PURCHASE_AGENT.format(
            order_history=history_text,
            inquiry_details=inquiry_details
        )
        
        return prompt
    
    def _format_order_history(self, history: list) -> str:
        """Format order history"""
        if not history:
            return "No order history"
        
        formatted = []
        for order in history[-5:]:  # Last 5 orders
            formatted.append(
                f"Order {order.get('order_id')} on {order.get('date')}: "
                f"₹{order.get('total', 0):,.0f}"
            )
        
        return "\n".join(formatted)
    
    def can_handle(self, user_message: str, context: Dict) -> bool:
        """Check if message is about post-purchase support"""
        keywords = [
            "return", "exchange", "refund", "cancel", "track",
            "order status", "where is my", "complaint", "issue",
            "problem", "help with order"
        ]
        message_lower = user_message.lower()
        return any(keyword in message_lower for keyword in keywords)
