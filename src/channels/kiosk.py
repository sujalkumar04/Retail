"""Kiosk channel"""

from typing import Dict, Any
from .base_channel import BaseChannel


class KioskChannel(BaseChannel):
    """In-store kiosk channel"""
    
    def __init__(self):
        super().__init__("kiosk")
    
    def format_message(self, message: str, metadata: Dict[str, Any] = None) -> Dict:
        """Format message for kiosk"""
        # Kiosk needs clear, direct messaging
        formatted = {
            "text": message,
            "channel": self.channel_name
        }
        
        if metadata:
            # Large touch-friendly buttons
            if "buttons" in metadata:
                formatted["buttons"] = metadata["buttons"]
            if "products" in metadata:
                formatted["products"] = metadata["products"]
        
        return formatted
    
    def parse_incoming_message(self, raw_message: Dict) -> Dict:
        """Parse incoming kiosk message"""
        return {
            "text": raw_message.get("message", ""),
            "kiosk_id": raw_message.get("kiosk_id"),
            "store_location": raw_message.get("store_location")
        }
    
    def get_channel_constraints(self) -> Dict:
        """Kiosk constraints"""
        return {
            "max_message_length": 2000,
            "supports_rich_formatting": True,
            "supports_images": True,
            "supports_buttons": True,
            "large_touch_targets": True,
            "prefer_direct_language": True
        }
