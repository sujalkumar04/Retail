"""Scenario runner for automated testing"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.orchestrator import AgentOrchestrator, WorkflowEngine
from src.services import SessionManager
from src.utils.context_manager import ContextManager
from src.models.cart import Cart
from src.utils.helpers import generate_id
from demo.demo_conversations import DEMO_SCENARIOS


class ScenarioRunner:
    """Run demo scenarios"""
    
    def __init__(self):
        self.session_manager = SessionManager()
        self.orchestrator = AgentOrchestrator()
        self.workflow_engine = WorkflowEngine()
    
    def run_scenario(self, scenario_name: str):
        """Run a specific scenario"""
        scenario = None
        for s in DEMO_SCENARIOS:
            if s["name"] == scenario_name:
                scenario = s
                break
        
        if not scenario:
            print(f"Scenario '{scenario_name}' not found")
            return
        
        print(f"\n{'='*60}")
        print(f"Running Scenario: {scenario['name']}")
        print(f"{'='*60}\n")
        
        # Create session
        session_id = generate_id("DEMO")
        customer_id = scenario["customer_id"]
        
        session = self.session_manager.create_session(
            session_id=session_id,
            customer_id=customer_id,
            channel="web_chat"
        )
        
        context_manager = ContextManager(session)
        
        # Get customer
        customer = self.workflow_engine.get_customer_by_id(customer_id)
        
        # Create cart
        cart = Cart(customer_id=customer_id)
        context_manager.set_context("cart", cart)
        
        # Run conversation
        for i, message in enumerate(scenario["messages"], 1):
            print(f"\n[User]: {message}")
            
            # Add user message
            context_manager.add_user_message(message)
            
            # Build context
            additional_context = {
                "customer": customer,
                "cart": cart.model_dump() if hasattr(cart, 'model_dump') else cart,
                "workflow_engine": self.workflow_engine
            }
            
            # Get response
            response = self.orchestrator.process_message(
                user_message=message,
                context_manager=context_manager,
                additional_context=additional_context
            )
            
            # Add assistant message
            context_manager.add_assistant_message(response)
            
            print(f"\n[Assistant]: {response}")
            print(f"\n{'-'*60}")
        
        print(f"\n{'='*60}")
        print(f"Scenario Complete!")
        print(f"Session ID: {session_id}")
        print(f"Messages: {len(session.messages)}")
        print(f"{'='*60}\n")
    
    def run_all_scenarios(self):
        """Run all demo scenarios"""
        for scenario in DEMO_SCENARIOS:
            self.run_scenario(scenario["name"])
            print("\n\n")


def main():
    """Main entry point"""
    runner = ScenarioRunner()
    
    if len(sys.argv) > 1:
        scenario_name = " ".join(sys.argv[1:])
        runner.run_scenario(scenario_name)
    else:
        print("Available scenarios:")
        for i, scenario in enumerate(DEMO_SCENARIOS, 1):
            print(f"{i}. {scenario['name']}")
        print("\nUsage: python scenario_runner.py [scenario_name]")
        print("Or run all: python scenario_runner.py")


if __name__ == "__main__":
    main()
