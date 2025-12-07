"""Conversation session models"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class MessageRole(str, Enum):
    """Message role enumeration"""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class Message(BaseModel):
    """Individual conversation message"""
    role: MessageRole
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Session(BaseModel):
    """Conversation session with context"""
    session_id: str
    customer_id: Optional[str] = None
    channel: str = "web_chat"
    
    # Conversation
    messages: List[Message] = Field(default_factory=list)
    
    # Context
    current_agent: Optional[str] = None
    workflow_state: str = "browsing"  # browsing, cart, checkout, post_purchase
    context: Dict[str, Any] = Field(default_factory=dict)
    
    # Tracking
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    last_activity: datetime = Field(default_factory=datetime.now)
    
    def add_message(self, role: MessageRole, content: str, metadata: Dict = None) -> None:
        """Add message to conversation"""
        message = Message(
            role=role,
            content=content,
            metadata=metadata or {}
        )
        self.messages.append(message)
        self.last_activity = datetime.now()
        self.updated_at = datetime.now()
    
    def get_conversation_history(self, limit: int = 10) -> List[Message]:
        """Get recent conversation history"""
        return self.messages[-limit:] if self.messages else []
    
    def get_context_value(self, key: str, default: Any = None) -> Any:
        """Get value from session context"""
        return self.context.get(key, default)
    
    def set_context_value(self, key: str, value: Any) -> None:
        """Set value in session context"""
        self.context[key] = value
        self.updated_at = datetime.now()
    
    def update_workflow_state(self, state: str) -> None:
        """Update workflow state"""
        self.workflow_state = state
        self.updated_at = datetime.now()
    
    def is_active(self, timeout_minutes: int = 30) -> bool:
        """Check if session is still active"""
        time_diff = datetime.now() - self.last_activity
        return time_diff.total_seconds() < (timeout_minutes * 60)
    
    def get_summary(self) -> str:
        """Get session summary"""
        return f"Session {self.session_id}: {len(self.messages)} messages, {self.workflow_state} state"