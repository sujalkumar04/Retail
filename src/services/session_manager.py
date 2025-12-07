"""Session management service with Redis"""

from typing import Optional, Dict
import json
import redis
from datetime import datetime, timedelta
from src.models.session import Session
from config.settings import settings


class SessionManager:
    """Manages conversation sessions with Redis storage"""
    
    def __init__(self):
        try:
            self.redis_client = redis.Redis(
                host=settings.redis_host,
                port=settings.redis_port,
                db=settings.redis_db,
                decode_responses=True
            )
            # Test connection
            self.redis_client.ping()
            self.redis_available = True
        except (redis.ConnectionError, redis.RedisError):
            print("Warning: Redis not available, using in-memory storage")
            self.redis_available = False
            self.memory_store = {}
    
    def create_session(
        self,
        session_id: str,
        customer_id: Optional[str] = None,
        channel: str = "web_chat"
    ) -> Session:
        """Create a new session"""
        session = Session(
            session_id=session_id,
            customer_id=customer_id,
            channel=channel
        )
        
        self.save_session(session)
        return session
    
    def get_session(self, session_id: str) -> Optional[Session]:
        """Retrieve session by ID"""
        if self.redis_available:
            session_data = self.redis_client.get(f"session:{session_id}")
            if session_data:
                data = json.loads(session_data)
                return Session(**data)
        else:
            if session_id in self.memory_store:
                return self.memory_store[session_id]
        
        return None
    
    def save_session(self, session: Session) -> bool:
        """Save session to storage"""
        session_data = session.model_dump_json()
        
        if self.redis_available:
            # Save with TTL
            ttl = settings.session_ttl
            self.redis_client.setex(
                f"session:{session.session_id}",
                ttl,
                session_data
            )
            return True
        else:
            self.memory_store[session.session_id] = session
            return True
    
    def delete_session(self, session_id: str) -> bool:
        """Delete session"""
        if self.redis_available:
            return bool(self.redis_client.delete(f"session:{session_id}"))
        else:
            if session_id in self.memory_store:
                del self.memory_store[session_id]
                return True
            return False
    
    def get_or_create_session(
        self,
        session_id: str,
        customer_id: Optional[str] = None,
        channel: str = "web_chat"
    ) -> Session:
        """Get existing session or create new one"""
        session = self.get_session(session_id)
        if session:
            return session
        
        return self.create_session(session_id, customer_id, channel)
    
    def extend_session(self, session_id: str) -> bool:
        """Extend session TTL"""
        if self.redis_available:
            return bool(self.redis_client.expire(
                f"session:{session_id}",
                settings.session_ttl
            ))
        return True
    
    def get_active_sessions(self, customer_id: str) -> list:
        """Get all active sessions for a customer"""
        active_sessions = []
        
        if self.redis_available:
            # Scan for sessions
            for key in self.redis_client.scan_iter(match="session:*"):
                session_data = self.redis_client.get(key)
                if session_data:
                    session = Session(**json.loads(session_data))
                    if session.customer_id == customer_id:
                        active_sessions.append(session)
        else:
            for session in self.memory_store.values():
                if session.customer_id == customer_id:
                    active_sessions.append(session)
        
        return active_sessions
