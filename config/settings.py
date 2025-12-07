"""
Configuration settings for the Retail AI Agent system
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # LLM Configuration
    openai_api_key: str = Field(default="", env="OPENAI_API_KEY")
    anthropic_api_key: str = Field(default="", env="ANTHROPIC_API_KEY")
    groq_api_key: str = Field(default="", env="GROQ_API_KEY")
    llm_provider: str = Field(default="openai", env="LLM_PROVIDER")  # openai, anthropic, groq
    llm_model: str = Field(default="gpt-4-turbo-preview", env="LLM_MODEL")
    llm_temperature: float = Field(default=0.7, env="LLM_TEMPERATURE")
    
    # Redis Configuration
    redis_host: str = Field(default="localhost", env="REDIS_HOST")
    redis_port: int = Field(default=6379, env="REDIS_PORT")
    redis_db: int = Field(default=0, env="REDIS_DB")
    
    # API Configuration
    api_host: str = Field(default="0.0.0.0", env="API_HOST")
    api_port: int = Field(default=8000, env="API_PORT")
    debug: bool = Field(default=True, env="DEBUG")
    
    # Session Configuration
    session_ttl: int = Field(default=3600, env="SESSION_TTL")
    max_conversation_history: int = Field(default=50, env="MAX_CONVERSATION_HISTORY")
    
    # Business Configuration
    store_name: str = Field(default="ABFRL Fashion Store", env="STORE_NAME")
    currency: str = Field(default="INR", env="CURRENCY")
    currency_symbol: str = Field(default="₹", env="CURRENCY_SYMBOL")
    
    # Channel Tokens
    whatsapp_api_token: Optional[str] = Field(default=None, env="WHATSAPP_API_TOKEN")
    telegram_bot_token: Optional[str] = Field(default=None, env="TELEGRAM_BOT_TOKEN")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
