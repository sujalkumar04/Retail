"""Web chat channel"""

from typing import Dict, Any
from .base_channel import BaseChannel


class WebChatChannel(BaseChannel):
    """Web chat channel with rich formatting support"""
    
    def __init__(self):
        super().__init__("web_chat")
    
    def format_message(self, message: str, metadata: Dict[str, Any] = None) -> Dict:
        """Format message for web chat"""
        formatted = {
            "text": message,
            "channel": self.channel_name,
            "timestamp": metadata.get("timestamp") if metadata else None
        }
        
        # Add rich formatting if available
        if metadata:
            if "products" in metadata:
                formatted["products"] = metadata["products"]
            if "images" in metadata:
                formatted["images"] = metadata["images"]
            if "buttons" in metadata:
                formatted["buttons"] = metadata["buttons"]
        
        return formatted
    
    def parse_incoming_message(self, raw_message: Dict) -> Dict:
        """Parse incoming web chat message"""
        return {
            "text": raw_message.get("message", raw_message.get("text", "")),
            "session_id": raw_message.get("session_id"),
            "customer_id": raw_message.get("customer_id")
        }
    
    def get_channel_constraints(self) -> Dict:
        """Web chat constraints"""
        return {
            "max_message_length": 5000,
            "supports_rich_formatting": True,
            "supports_images": True,
            "supports_buttons": True,
            "supports_markdown": True
        }
