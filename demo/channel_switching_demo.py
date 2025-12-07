"""Channel switching demo - shows session continuity across channels"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.orchestrator import AgentOrchestrator, WorkflowEngine
from src.services import SessionManager
from src.utils.context_manager import ContextManager
from src.models.cart import Cart
from src.channels import ChannelManager
from src.utils.helpers import generate_id


def demo_channel_switching():
    """Demonstrate switching channels while maintaining session"""
    
    print("\n" + "="*60)
    print("Channel Switching Demo")
    print("="*60 + "\n")
    
    # Initialize services
    session_manager = SessionManager()
    orchestrator = AgentOrchestrator()
    workflow_engine = WorkflowEngine()
    channel_manager = ChannelManager()
    
    # Create session
    session_id = generate_id("CHAN")
    customer_id = "CUST001"
    
    # Start on web chat
    print("📱 Starting on WEB CHAT\n")
    session = session_manager.create_session(
        session_id=session_id,
        customer_id=customer_id,
        channel="web_chat"
    )
    
    context_manager = ContextManager(session)
    customer = workflow_engine.get_customer_by_id(customer_id)
    cart = Cart(customer_id=customer_id)
    context_manager.set_context("cart", cart)
    
    # Web chat interaction
    message1 = "Show me summer dresses"
    print(f"[User on Web]: {message1}")
    
    additional_context = {
        "customer": customer,
        "cart": cart.model_dump() if hasattr(cart, 'model_dump') else cart,
        "workflow_engine": workflow_engine
    }
    
    response1 = orchestrator.process_message(message1, context_manager, additional_context)
    print(f"[Assistant]: {response1}\n")
    print("-"*60 + "\n")
    
    # Switch to mobile
    print("📱 Switching to MOBILE APP\n")
    session.channel = "mobile_app"
    session_manager.save_session(session)
    
    message2 = "Add the floral maxi dress to cart"
    print(f"[User on Mobile]: {message2}")
    
    response2 = orchestrator.process_message(message2, context_manager, additional_context)
    print(f"[Assistant]: {response2}\n")
    print("-"*60 + "\n")
    
    # Switch to WhatsApp
    print("💬 Switching to WHATSAPP\n")
    session.channel = "whatsapp"
    session_manager.save_session(session)
    
    message3 = "What's in my cart?"
    print(f"[User on WhatsApp]: {message3}")
    
    response3 = orchestrator.process_message(message3, context_manager, additional_context)
    print(f"[Assistant]: {response3}\n")
    print("-"*60 + "\n")
    
    # Switch to kiosk
    print("🏬 Switching to IN-STORE KIOSK\n")
    session.channel = "kiosk"
    session_manager.save_session(session)
    
    message4 = "I want to checkout"
    print(f"[User at Kiosk]: {message4}")
    
    response4 = orchestrator.process_message(message4, context_manager, additional_context)
    print(f"[Assistant]: {response4}\n")
    
    print("="*60)
    print("Demo Complete!")
    print(f"Session ID: {session_id}")
    print(f"Channels used: Web → Mobile → WhatsApp → Kiosk")
    print(f"Total messages: {len(session.messages)}")
    print(f"Cart items: {len(cart.items)}")
    print("="*60 + "\n")


if __name__ == "__main__":
    demo_channel_switching()
