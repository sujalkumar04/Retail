"""Base channel interface"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseChannel(ABC):
    """Abstract base class for all channels"""
    
    def __init__(self, channel_name: str):
        self.channel_name = channel_name
    
    @abstractmethod
    def format_message(self, message: str, metadata: Dict[str, Any] = None) -> Dict:
        """Format message for this channel"""
        pass
    
    @abstractmethod
    def parse_incoming_message(self, raw_message: Dict) -> Dict:
        """Parse incoming message from this channel"""
        pass
    
    def get_channel_constraints(self) -> Dict:
        """Get channel-specific constraints (message length, etc.)"""
        return {
            "max_message_length": 2000,
            "supports_rich_formatting": False,
            "supports_images": False,
            "supports_buttons": False
        }
