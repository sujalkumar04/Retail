"""Basic tests for agents"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agents import SalesAgent, RecommendationAgent, InventoryAgent
from src.models.session import Session
from src.utils.context_manager import ContextManager


def test_sales_agent():
    """Test sales agent initialization"""
    agent = SalesAgent()
    assert agent.name == "SalesAgent"
    print("✓ Sales agent test passed")


def test_recommendation_agent():
    """Test recommendation agent"""
    agent = RecommendationAgent()
    assert agent.name == "RecommendationAgent"
    
    # Test can_handle
    assert agent.can_handle("recommend a dress", {})
    assert agent.can_handle("show me similar items", {})
    assert not agent.can_handle("hello", {})
    print("✓ Recommendation agent test passed")


def test_inventory_agent():
    """Test inventory agent"""
    agent = InventoryAgent()
    assert agent.name == "InventoryAgent"
    
    # Test can_handle
    assert agent.can_handle("is this available?", {})
    assert agent.can_handle("check stock", {})
    print("✓ Inventory agent test passed")


def test_context_manager():
    """Test context manager"""
    session = Session(session_id="TEST001", channel="web_chat")
    context_mgr = ContextManager(session)
    
    # Test adding messages
    context_mgr.add_user_message("Hello")
    assert len(session.messages) == 1
    
    context_mgr.add_assistant_message("Hi there!")
    assert len(session.messages) == 2
    
    # Test context
    context_mgr.set_context("test_key", "test_value")
    assert context_mgr.get_context("test_key") == "test_value"
    
    print("✓ Context manager test passed")


if __name__ == "__main__":
    test_sales_agent()
    test_recommendation_agent()
    test_inventory_agent()
    test_context_manager()
    print("\n✅ All tests passed!")
