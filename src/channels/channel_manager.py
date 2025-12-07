"""Channel manager for routing and session continuity"""

from typing import Dict, Optional
from .web_chat import WebChatChannel
from .mobile_app import MobileAppChannel
from .whatsapp import WhatsAppChannel
from .kiosk import KioskChannel
from .voice_assistant import VoiceAssistantChannel


class ChannelManager:
    """Manages multiple channels and session continuity"""
    
    def __init__(self):
        self.channels = {
            "web_chat": WebChatChannel(),
            "mobile_app": MobileAppChannel(),
            "whatsapp": WhatsAppChannel(),
            "kiosk": KioskChannel(),
            "voice": VoiceAssistantChannel()
        }
    
    def get_channel(self, channel_name: str):
        """Get channel by name"""
        return self.channels.get(channel_name)
    
    def format_for_channel(
        self,
        channel_name: str,
        message: str,
        metadata: Optional[Dict] = None
    ) -> Dict:
        """Format message for specific channel"""
        channel = self.get_channel(channel_name)
        if channel:
            return channel.format_message(message, metadata)
        
        # Default format
        return {"text": message}
    
    def parse_from_channel(
        self,
        channel_name: str,
        raw_message: Dict
    ) -> Dict:
        """Parse message from specific channel"""
        channel = self.get_channel(channel_name)
        if channel:
            return channel.parse_incoming_message(raw_message)
        
        # Default parse
        return {"text": raw_message.get("text", "")}
