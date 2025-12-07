"""Mobile app channel"""

from typing import Dict, Any
from .base_channel import BaseChannel


class MobileAppChannel(BaseChannel):
    """Mobile app channel with concise messaging"""
    
    def __init__(self):
        super().__init__("mobile_app")
    
    def format_message(self, message: str, metadata: Dict[str, Any] = None) -> Dict:
        """Format message for mobile app"""
        # Keep messages concise for mobile
        formatted = {
            "text": message,
            "channel": self.channel_name
        }
        
        if metadata:
            # Add quick action buttons
            if "quick_actions" in metadata:
                formatted["quick_actions"] = metadata["quick_actions"]
            if "products" in metadata:
                # Simplified product cards for mobile
                formatted["products"] = metadata["products"]
        
        return formatted
    
    def parse_incoming_message(self, raw_message: Dict) -> Dict:
        """Parse incoming mobile app message"""
        return {
            "text": raw_message.get("message", ""),
            "session_id": raw_message.get("session_id"),
            "customer_id": raw_message.get("customer_id"),
            "device_type": raw_message.get("device_type", "mobile")
        }
    
    def get_channel_constraints(self) -> Dict:
        """Mobile app constraints"""
        return {
            "max_message_length": 1000,
            "supports_rich_formatting": True,
            "supports_images": True,
            "supports_buttons": True,
            "prefer_concise": True
        }
