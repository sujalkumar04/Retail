"""Context manager for conversation state"""

from typing import Dict, Any, List, Optional
from src.models.session import Session, Message, MessageRole


class ContextManager:
    """Manages conversation context and memory"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def add_user_message(self, content: str) -> None:
        """Add user message to context"""
        self.session.add_message(MessageRole.USER, content)
    
    def add_assistant_message(self, content: str, metadata: Dict = None) -> None:
        """Add assistant message to context"""
        self.session.add_message(MessageRole.ASSISTANT, content, metadata)
    
    def get_conversation_history(self, limit: int = 10) -> List[Dict[str, str]]:
        """Get formatted conversation history for LLM"""
        messages = self.session.get_conversation_history(limit)
        return [
            {"role": msg.role.value, "content": msg.content}
            for msg in messages
        ]
    
    def set_context(self, key: str, value: Any) -> None:
        """Set context variable"""
        self.session.set_context_value(key, value)
    
    def get_context(self, key: str, default: Any = None) -> Any:
        """Get context variable"""
        return self.session.get_context_value(key, default)
    
    def update_workflow_state(self, state: str) -> None:
        """Update workflow state"""
        self.session.update_workflow_state(state)
    
    def get_workflow_state(self) -> str:
        """Get current workflow state"""
        return self.session.workflow_state
    
    def build_context_summary(self) -> str:
        """Build a summary of current context for agents"""
        cart = self.get_context("cart")
        customer = self.get_context("customer")
        
        summary_parts = []
        
        if customer:
            summary_parts.append(f"Customer: {customer.get('name', 'Unknown')}")
            summary_parts.append(f"Loyalty: {customer.get('loyalty_tier', 'Bronze')}")
        
        if cart and not cart.get("is_empty", True):
            summary_parts.append(f"Cart: {cart.get('summary', 'Empty')}")
        
        summary_parts.append(f"State: {self.session.workflow_state}")
        
        return " | ".join(summary_parts)
