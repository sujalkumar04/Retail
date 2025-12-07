"""Agent orchestrator for routing requests"""

from typing import Dict, Optional
from src.agents import (
    SalesAgent, RecommendationAgent, InventoryAgent,
    PaymentAgent, FulfillmentAgent, LoyaltyAgent, PostPurchaseAgent
)
from src.utils.context_manager import ContextManager


class AgentOrchestrator:
    """Routes user requests to appropriate agents"""
    
    def __init__(self):
        # Initialize all agents
        self.agents = {
            "sales": SalesAgent(),
            "recommendation": RecommendationAgent(),
            "inventory": InventoryAgent(),
            "payment": PaymentAgent(),
            "fulfillment": FulfillmentAgent(),
            "loyalty": LoyaltyAgent(),
            "post_purchase": PostPurchaseAgent()
        }
    
    def route_message(
        self,
        user_message: str,
        context_manager: ContextManager,
        additional_context: Optional[Dict] = None
    ) -> tuple:
        """
        Route message to appropriate agent
        Returns: (agent_name, agent_instance)
        """
        context = additional_context or {}
        
        # Check each agent's can_handle method
        for agent_name, agent in self.agents.items():
            if agent_name == "sales":
                continue  # Sales is fallback
            
            if agent.can_handle(user_message, context):
                return agent_name, agent
        
        # Default to sales agent
        return "sales", self.agents["sales"]
    
    def process_message(
        self,
        user_message: str,
        context_manager: ContextManager,
        additional_context: Optional[Dict] = None
    ) -> str:
        """Process message through appropriate agent"""
        # Route to agent
        agent_name, agent = self.route_message(user_message, context_manager, additional_context)
        
        # Update current agent in session
        context_manager.set_context("current_agent", agent_name)
        
        # Process message
        response = agent.process(user_message, context_manager, additional_context)
        
        return response
    
    async def process_message_stream(
        self,
        user_message: str,
        context_manager: ContextManager,
        additional_context: Optional[Dict] = None
    ):
        """Process message through appropriate agent with streaming"""
        # Route to agent
        agent_name, agent = self.route_message(user_message, context_manager, additional_context)
        
        # Update current agent in session
        context_manager.set_context("current_agent", agent_name)
        
        # Process message with streaming
        async for chunk in agent.process_stream(user_message, context_manager, additional_context):
            yield chunk
    
    def get_agent(self, agent_name: str):
        """Get specific agent by name"""
        return self.agents.get(agent_name)
