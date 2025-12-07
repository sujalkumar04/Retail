"""LLM client for OpenAI, Anthropic, and Groq"""

from typing import List, Dict, Optional, AsyncIterator
import openai
from config.settings import settings


class LLMClient:
    """Client for interacting with LLM providers"""
    
    def __init__(self):
        self.provider = settings.llm_provider
        self.model = settings.llm_model
        self.temperature = settings.llm_temperature
        
        if self.provider == "openai":
            self.client = openai.OpenAI(api_key=settings.openai_api_key)
        elif self.provider == "groq":
            try:
                from groq import Groq
                self.client = Groq(api_key=settings.groq_api_key)
            except ImportError:
                print("Warning: groq package not installed. Install with: pip install groq")
                self.client = None
        elif self.provider == "anthropic":
            # Anthropic client would be initialized here
            pass
    
    def generate(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: int = 1000
    ) -> str:
        """Generate a response from the LLM"""
        temp = temperature if temperature is not None else self.temperature
        
        if self.provider == "openai":
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temp,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        
        elif self.provider == "groq":
            if not self.client:
                return "Groq client not available. Please install: pip install groq"
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temp,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        
        return "LLM response not available"
    
    async def generate_stream(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: int = 1000
    ) -> AsyncIterator[str]:
        """Generate a streaming response from the LLM"""
        temp = temperature if temperature is not None else self.temperature
        
        if self.provider == "openai":
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temp,
                max_tokens=max_tokens,
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        
        elif self.provider == "groq":
            if not self.client:
                yield "Groq client not available. Please install: pip install groq"
                return
            
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temp,
                max_tokens=max_tokens,
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
    
    def format_messages(
        self,
        system_prompt: str,
        conversation_history: List[Dict],
        user_message: str
    ) -> List[Dict[str, str]]:
        """Format messages for LLM API"""
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history
        for msg in conversation_history:
            messages.append({
                "role": msg.get("role", "user"),
                "content": msg.get("content", "")
            })
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        return messages
