"""Inventory agent for stock checking"""

from typing import Dict
from .base_agent import BaseAgent
from config.prompts import PromptTemplates


class InventoryAgent(BaseAgent):
    """AI agent for inventory and availability queries"""
    
    def __init__(self):
        super().__init__("InventoryAgent")
    
    def get_system_prompt(self, context: Dict) -> str:
        """Get inventory agent system prompt"""
        inventory_data = context.get("inventory_data") or {}
        customer = context.get("customer") or {}
        
        customer_location = customer.get("preferred_store", "Mumbai")
        preferred_store = customer.get("preferred_store", "Mumbai - Phoenix Mall")
        
        # Format inventory data
        inventory_text = self._format_inventory_data(inventory_data)
        
        # Fill in prompt template
        prompt = PromptTemplates.INVENTORY_AGENT.format(
            inventory_data=inventory_text,
            customer_location=customer_location,
            preferred_store=preferred_store
        )
        
        return prompt
    
    def _format_inventory_data(self, inventory_data: Dict) -> str:
        """Format inventory data for prompt"""
        if not inventory_data:
            return "No inventory data available"
        
        parts = []
        
        # Online availability
        online_available = inventory_data.get("online_available", False)
        online_qty = inventory_data.get("online_quantity", 0)
        parts.append(f"Online: {'Available' if online_available else 'Out of stock'} ({online_qty} units)")
        
        # Store availability
        available_stores = inventory_data.get("available_stores", [])
        if available_stores:
            parts.append(f"Available in stores: {', '.join(available_stores)}")
        
        # Fulfillment options
        fulfillment = inventory_data.get("fulfillment_options", {})
        if fulfillment.get("home_delivery", {}).get("available"):
            estimate = fulfillment["home_delivery"].get("estimate", "3-5 days")
            parts.append(f"Home Delivery: {estimate}")
        
        if fulfillment.get("store_pickup", {}).get("available"):
            parts.append("Store Pickup: Available")
        
        return "\n".join(parts)
    
    def can_handle(self, user_message: str, context: Dict) -> bool:
        """Check if message is about inventory/availability"""
        keywords = [
            "available", "stock", "in stock", "out of stock",
            "delivery", "shipping", "pickup", "store", "when can"
        ]
        message_lower = user_message.lower()
        return any(keyword in message_lower for keyword in keywords)
