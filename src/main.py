"""Main entry point for CLI testing"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.orchestrator import AgentOrchestrator, WorkflowEngine
from src.services import SessionManager
from src.utils.context_manager import ContextManager
from src.models.cart import Cart
from src.utils.helpers import generate_id


def main():
    """Interactive CLI for testing"""
    print("\n" + "="*60)
    print("🛍️  Retail AI Agent - Interactive CLI")
    print("="*60 + "\n")
    
    # Initialize services
    session_manager = SessionManager()
    orchestrator = AgentOrchestrator()
    workflow_engine = WorkflowEngine()
    
    # Create session
    session_id = generate_id("CLI")
    customer_id = input("Enter customer ID (or press Enter for CUST001): ").strip() or "CUST001"
    
    session = session_manager.create_session(
        session_id=session_id,
        customer_id=customer_id,
        channel="web_chat"
    )
    
    context_manager = ContextManager(session)
    
    # Get customer
    customer = workflow_engine.get_customer_by_id(customer_id)
    if customer:
        print(f"\n✓ Loaded customer: {customer.get('name')} ({customer.get('loyalty_tier')} tier)")
    
    # Create cart
    cart = Cart(customer_id=customer_id)
    context_manager.set_context("cart", cart)
    
    print(f"✓ Session created: {session_id}")
    print("\nType 'quit' or 'exit' to end the session\n")
    print("-"*60 + "\n")
    
    # Conversation loop
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\n👋 Thank you for shopping with us!\n")
                break
            
            # Add user message
            context_manager.add_user_message(user_input)
            
            # Build context
            additional_context = {
                "customer": customer,
                "cart": cart.model_dump() if hasattr(cart, 'model_dump') else cart,
                "workflow_engine": workflow_engine
            }
            
            # Get response
            response = orchestrator.process_message(
                user_message=user_input,
                context_manager=context_manager,
                additional_context=additional_context
            )
            
            # Add assistant message
            context_manager.add_assistant_message(response)
            
            print(f"\nAssistant: {response}\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Session interrupted. Goodbye!\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")
    
    # Save session
    session_manager.save_session(session)
    print(f"Session saved: {len(session.messages)} messages")


if __name__ == "__main__":
    main()
