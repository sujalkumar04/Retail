"""Webhook routes for external integrations"""

from fastapi import APIRouter, Request

router = APIRouter()


@router.post("/whatsapp")
async def whatsapp_webhook(request: Request):
    """WhatsApp webhook endpoint"""
    data = await request.json()
    # Process WhatsApp webhook
    return {"status": "received"}


@router.post("/telegram")
async def telegram_webhook(request: Request):
    """Telegram webhook endpoint"""
    data = await request.json()
    # Process Telegram webhook
    return {"status": "received"}


@router.get("/whatsapp")
async def whatsapp_verify(request: Request):
    """WhatsApp webhook verification"""
    # Verify webhook for WhatsApp
    return {"status": "verified"}
