"""Base agent class"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from src.utils.llm_client import LLMClient
from src.utils.context_manager import ContextManager


class BaseAgent(ABC):
    """Abstract base class for all agents"""
    
    def __init__(self, name: str):
        self.name = name
        self.llm_client = LLMClient()
    
    @abstractmethod
    def get_system_prompt(self, context: Dict) -> str:
        """Get system prompt for this agent"""
        pass
    
    def process(
        self,
        user_message: str,
        context_manager: ContextManager,
        additional_context: Optional[Dict] = None
    ) -> str:
        """Process user message and generate response"""
        # Get conversation history
        history = context_manager.get_conversation_history()
        
        # Build context
        context = additional_context or {}
        context["session"] = context_manager.session
        
        # Get system prompt
        system_prompt = self.get_system_prompt(context)
        
        # Format messages for LLM
        messages = self.llm_client.format_messages(
            system_prompt=system_prompt,
            conversation_history=history,
            user_message=user_message
        )
        
        # Generate response
        response = self.llm_client.generate(messages)
        
        return response
    
    async def process_stream(
        self,
        user_message: str,
        context_manager: ContextManager,
        additional_context: Optional[Dict] = None
    ):
        """Process user message and generate streaming response"""
        # Get conversation history
        history = context_manager.get_conversation_history()
        
        # Build context
        context = additional_context or {}
        context["session"] = context_manager.session
        
        # Get system prompt
        system_prompt = self.get_system_prompt(context)
        
        # Format messages for LLM
        messages = self.llm_client.format_messages(
            system_prompt=system_prompt,
            conversation_history=history,
            user_message=user_message
        )
        
        # Generate streaming response
        async for chunk in self.llm_client.generate_stream(messages):
            yield chunk
    
    def can_handle(self, user_message: str, context: Dict) -> bool:
        """Determine if this agent can handle the user message"""
        # Default implementation - can be overridden by specific agents
        return False
