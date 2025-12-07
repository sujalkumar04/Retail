"""Workflow engine for multi-step processes"""

from typing import Dict, List, Optional
from src.models.cart import Cart, CartItem
from src.models.order import Order, OrderItem, OrderStatus, ShippingAddress, PaymentInfo
from src.services import (
    ProductCatalogService, InventoryService, PaymentGatewayService,
    LoyaltyService, FulfillmentService
)
from src.utils.helpers import generate_id, load_json_data
from datetime import datetime


class WorkflowEngine:
    """Manages multi-step workflows (browse → cart → checkout → fulfillment)"""
    
    def __init__(self):
        self.product_catalog = ProductCatalogService()
        self.inventory_service = InventoryService()
        self.payment_service = PaymentGatewayService()
        self.loyalty_service = LoyaltyService()
        self.fulfillment_service = FulfillmentService()
        
        # Load customer data
        self.customers_data = load_json_data("customers.json")
    
    def get_customer_by_id(self, customer_id: str) -> Optional[Dict]:
        """Get customer data by ID"""
        for customer in self.customers_data.get("customers", []):
            if customer.get("id") == customer_id:
                return customer
        return None
    
    def add_to_cart(
        self,
        cart: Cart,
        sku: str,
        quantity: int = 1,
        size: Optional[str] = None,
        color: Optional[str] = None
    ) -> Dict:
        """Add item to cart"""
        # Get product details
        product = self.product_catalog.get_product_by_sku(sku)
        if not product:
            return {"success": False, "message": "Product not found"}
        
        # Check inventory
        is_available, available_qty = self.inventory_service.check_availability(
            sku, color, size
        )
        
        if not is_available or available_qty < quantity:
            return {
                "success": False,
                "message": f"Only {available_qty} units available"
            }
        
        # Create cart item
        cart_item = CartItem(
            sku=sku,
            name=product.name,
            price=product.price,
            quantity=quantity,
            size=size,
            color=color,
            image=product.images[0] if product.images else None
        )
        
        # Add to cart
        cart.add_item(cart_item)
        
        return {
            "success": True,
            "message": f"Added {product.name} to cart",
            "cart_summary": cart.get_summary()
        }
    
    def create_order_from_cart(
        self,
        cart: Cart,
        customer_id: str,
        shipping_address: Dict,
        payment_method: str,
        fulfillment_type: str = "home_delivery"
    ) -> Dict:
        """Create order from cart"""
        if cart.is_empty():
            return {"success": False, "message": "Cart is empty"}
        
        # Get customer
        customer = self.get_customer_by_id(customer_id)
        if not customer:
            return {"success": False, "message": "Customer not found"}
        
        # Calculate totals
        subtotal = cart.get_subtotal()
        
        # Apply best promotion
        customer_tier = customer.get("loyalty_tier", "Bronze")
        best_promo = self.loyalty_service.get_best_promotion(
            subtotal,
            customer_tier
        )
        
        discount = 0.0
        if best_promo:
            discount = self.loyalty_service.apply_promotion(best_promo, subtotal)
        
        # Calculate shipping
        shipping_fee = self.fulfillment_service.calculate_shipping_fee(
            subtotal,
            fulfillment_type,
            customer_tier
        )
        
        # Calculate tax (simplified - 18% GST)
        tax = (subtotal - discount + shipping_fee) * 0.18
        
        # Calculate total
        total = subtotal - discount + shipping_fee + tax
        
        # Create order
        order_id = generate_id("ORD")
        
        order = Order(
            order_id=order_id,
            customer_id=customer_id,
            items=[
                OrderItem(**item.model_dump())
                for item in cart.items
            ],
            subtotal=subtotal,
            discount=discount,
            shipping_fee=shipping_fee,
            tax=tax,
            total=total,
            shipping_address=ShippingAddress(**shipping_address),
            fulfillment_type=fulfillment_type,
            payment_info=PaymentInfo(
                method=payment_method,
                amount=total
            )
        )
        
        # Process payment
        payment_result = self.payment_service.process_payment(
            amount=total,
            payment_method=payment_method,
            customer_id=customer_id,
            order_id=order_id
        )
        
        if not payment_result.get("success"):
            return {
                "success": False,
                "message": "Payment failed"
            }
        
        # Update payment info
        order.payment_info.status = "completed"
        order.payment_info.transaction_id = payment_result.get("transaction_id")
        order.update_status(OrderStatus.CONFIRMED)
        
        # Schedule delivery
        if fulfillment_type == "home_delivery":
            delivery = self.fulfillment_service.schedule_delivery(
                order_id=order_id,
                address=shipping_address.get("address", ""),
                fulfillment_type=fulfillment_type
            )
            order.tracking_number = delivery.get("tracking_number")
            order.estimated_delivery = delivery.get("scheduled_date")
        
        # Calculate loyalty points
        points_earned = self.loyalty_service.calculate_points_earned(
            total,
            customer_tier
        )
        order.loyalty_points_earned = points_earned
        
        # Clear cart
        cart.clear()
        
        return {
            "success": True,
            "message": "Order placed successfully",
            "order": order.model_dump(),
            "points_earned": points_earned
        }
    
    def get_workflow_state(self, cart: Cart, customer_id: Optional[str]) -> str:
        """Determine current workflow state"""
        if not customer_id:
            return "browsing"
        
        if cart.is_empty():
            return "browsing"
        
        return "cart"
