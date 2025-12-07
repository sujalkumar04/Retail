"""Voice assistant channel"""

from typing import Dict, Any
from .base_channel import BaseChannel


class VoiceAssistantChannel(BaseChannel):
    """Voice assistant channel"""
    
    def __init__(self):
        super().__init__("voice")
    
    def format_message(self, message: str, metadata: Dict[str, Any] = None) -> Dict:
        """Format message for voice"""
        # Voice needs natural, spoken language
        # Remove formatting, lists, etc.
        formatted = {
            "text": self._convert_to_spoken(message),
            "channel": self.channel_name,
            "ssml": self._generate_ssml(message)
        }
        
        return formatted
    
    def _convert_to_spoken(self, message: str) -> str:
        """Convert text to spoken format"""
        # Remove markdown, bullets, etc.
        spoken = message.replace("*", "").replace("_", "")
        spoken = spoken.replace("- ", "")
        return spoken
    
    def _generate_ssml(self, message: str) -> str:
        """Generate SSML for voice synthesis"""
        # Basic SSML wrapper
        return f"<speak>{self._convert_to_spoken(message)}</speak>"
    
    def parse_incoming_message(self, raw_message: Dict) -> Dict:
        """Parse incoming voice message"""
        return {
            "text": raw_message.get("transcript", raw_message.get("text", "")),
            "audio_url": raw_message.get("audio_url"),
            "confidence": raw_message.get("confidence", 1.0)
        }
    
    def get_channel_constraints(self) -> Dict:
        """Voice constraints"""
        return {
            "max_message_length": 500,
            "supports_rich_formatting": False,
            "supports_images": False,
            "supports_buttons": False,
            "prefer_natural_language": True,
            "avoid_lists": True
        }
