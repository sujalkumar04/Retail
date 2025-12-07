"""Chat API routes"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
import json

from src.orchestrator import AgentOrchestrator, WorkflowEngine
from src.services import SessionManager
from src.utils.context_manager import ContextManager
from src.models.cart import Cart
from src.utils.helpers import generate_id

router = APIRouter()

# Initialize services
session_manager = SessionManager()
orchestrator = AgentOrchestrator()
workflow_engine = WorkflowEngine()


class ChatRequest(BaseModel):
    """Chat request model"""
    message: str
    session_id: Optional[str] = None
    customer_id: Optional[str] = None
    channel: str = "web_chat"


class ChatResponse(BaseModel):
    """Chat response model"""
    response: str
    session_id: str
    agent: Optional[str] = None


@router.post("/message", response_model=ChatResponse)
async def send_message(request: ChatRequest):
    """Send a message and get response"""
    try:
        # Get or create session
        session_id = request.session_id or generate_id("SESS")
        session = session_manager.get_or_create_session(
            session_id=session_id,
            customer_id=request.customer_id,
            channel=request.channel
        )
        
        # Create context manager
        context_manager = ContextManager(session)
        
        # Add user message
        context_manager.add_user_message(request.message)
        
        # Get customer data
        customer = None
        if request.customer_id:
            customer = workflow_engine.get_customer_by_id(request.customer_id)
        
        # Get or create cart
        cart = context_manager.get_context("cart")
        if not cart:
            cart = Cart(customer_id=request.customer_id or "guest")
            context_manager.set_context("cart", cart)
        
        # Build additional context
        additional_context = {
            "customer": customer,
            "cart": cart.model_dump() if hasattr(cart, 'model_dump') else cart,
            "workflow_engine": workflow_engine
        }
        
        # Process message
        response = orchestrator.process_message(
            user_message=request.message,
            context_manager=context_manager,
            additional_context=additional_context
        )
        
        # Add assistant message
        context_manager.add_assistant_message(response)
        
        # Save session
        session_manager.save_session(session)
        
        return ChatResponse(
            response=response,
            session_id=session_id,
            agent=context_manager.get_context("current_agent")
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/message/stream")
async def send_message_stream(request: ChatRequest):
    """Send a message and get streaming response"""
    try:
        # Get or create session
        session_id = request.session_id or generate_id("SESS")
        session = session_manager.get_or_create_session(
            session_id=session_id,
            customer_id=request.customer_id,
            channel=request.channel
        )
        
        # Create context manager
        context_manager = ContextManager(session)
        
        # Add user message
        context_manager.add_user_message(request.message)
        
        # Get customer data
        customer = None
        if request.customer_id:
            customer = workflow_engine.get_customer_by_id(request.customer_id)
        
        # Get or create cart
        cart = context_manager.get_context("cart")
        if not cart:
            cart = Cart(customer_id=request.customer_id or "guest")
            context_manager.set_context("cart", cart)
        
        # Build additional context
        additional_context = {
            "customer": customer,
            "cart": cart.model_dump() if hasattr(cart, 'model_dump') else cart,
            "workflow_engine": workflow_engine
        }
        
        async def generate():
            full_response = ""
            async for chunk in orchestrator.process_message_stream(
                user_message=request.message,
                context_manager=context_manager,
                additional_context=additional_context
            ):
                full_response += chunk
                yield f"data: {json.dumps({'chunk': chunk})}\n\n"
            
            # Add assistant message
            context_manager.add_assistant_message(full_response)
            
            # Save session
            session_manager.save_session(session)
            
            # Send completion
            yield f"data: {json.dumps({'done': True, 'session_id': session_id})}\n\n"
        
        return StreamingResponse(generate(), media_type="text/event-stream")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/session/{session_id}")
async def get_session(session_id: str):
    """Get session information"""
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {
        "session_id": session.session_id,
        "customer_id": session.customer_id,
        "channel": session.channel,
        "message_count": len(session.messages),
        "workflow_state": session.workflow_state
    }
