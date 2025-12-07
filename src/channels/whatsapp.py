"""WhatsApp channel"""

from typing import Dict, Any
from .base_channel import BaseChannel


class WhatsAppChannel(BaseChannel):
    """WhatsApp channel with casual messaging"""
    
    def __init__(self):
        super().__init__("whatsapp")
    
    def format_message(self, message: str, metadata: Dict[str, Any] = None) -> Dict:
        """Format message for WhatsApp"""
        # WhatsApp prefers shorter messages with emojis
        formatted = {
            "text": message,
            "channel": self.channel_name
        }
        
        if metadata:
            # WhatsApp supports buttons
            if "buttons" in metadata:
                formatted["buttons"] = metadata["buttons"][:3]  # Max 3 buttons
        
        return formatted
    
    def parse_incoming_message(self, raw_message: Dict) -> Dict:
        """Parse incoming WhatsApp message"""
        return {
            "text": raw_message.get("Body", raw_message.get("text", "")),
            "from": raw_message.get("From"),
            "phone": raw_message.get("From")
        }
    
    def get_channel_constraints(self) -> Dict:
        """WhatsApp constraints"""
        return {
            "max_message_length": 1000,
            "supports_rich_formatting": False,
            "supports_images": True,
            "supports_buttons": True,
            "max_buttons": 3,
            "prefer_casual_tone": True
        }
