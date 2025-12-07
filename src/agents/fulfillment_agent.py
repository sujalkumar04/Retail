"""Fulfillment agent for delivery coordination"""

from typing import Dict
from .base_agent import BaseAgent
from config.prompts import PromptTemplates


class FulfillmentAgent(BaseAgent):
    """AI agent for fulfillment and delivery"""
    
    def __init__(self):
        super().__init__("FulfillmentAgent")
    
    def get_system_prompt(self, context: Dict) -> str:
        """Get fulfillment agent system prompt"""
        order_details = context.get("order_details") or {}
        delivery_slots = context.get("delivery_slots") or []
        pickup_locations = context.get("pickup_locations") or []
        express_available = context.get("express_available", True)
        
        # Format data
        order_text = self._format_order_details(order_details)
        slots_text = self._format_delivery_slots(delivery_slots)
        locations_text = self._format_pickup_locations(pickup_locations)
        
        # Fill in prompt template
        prompt = PromptTemplates.FULFILLMENT_AGENT.format(
            order_details=order_text,
            delivery_slots=slots_text,
            pickup_locations=locations_text,
            express_available="Yes" if express_available else "No"
        )
        
        return prompt
    
    def _format_order_details(self, order: Dict) -> str:
        """Format order details"""
        if not order:
            return "No order details"
        
        return f"Order {order.get('order_id', 'N/A')}: {order.get('item_count', 0)} items"
    
    def _format_delivery_slots(self, slots: list) -> str:
        """Format delivery slots"""
        if not slots:
            return "No slots available"
        
        formatted = []
        for slot in slots[:5]:  # Show first 5
            formatted.append(f"{slot.get('date')} {slot.get('time_slot')}")
        
        return "; ".join(formatted)
    
    def _format_pickup_locations(self, locations: list) -> str:
        """Format pickup locations"""
        if not locations:
            return "No locations available"
        
        formatted = []
        for loc in locations[:3]:  # Show first 3
            formatted.append(f"{loc.get('store_name')} ({loc.get('distance')})")
        
        return "; ".join(formatted)
    
    def can_handle(self, user_message: str, context: Dict) -> bool:
        """Check if message is about fulfillment"""
        keywords = [
            "deliver", "delivery", "ship", "shipping", "pickup",
            "when will", "track", "tracking"
        ]
        message_lower = user_message.lower()
        return any(keyword in message_lower for keyword in keywords)
