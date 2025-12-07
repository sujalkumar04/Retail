"""Order management models"""

from typing import List, Optional, Dict
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class OrderStatus(str, Enum):
    """Order status enumeration"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    RETURNED = "returned"


class OrderItem(BaseModel):
    """Individual item in an order"""
    sku: str
    name: str
    price: float
    quantity: int
    size: Optional[str] = None
    color: Optional[str] = None
    image: Optional[str] = None
    
    def get_subtotal(self) -> float:
        """Calculate subtotal for this item"""
        return self.price * self.quantity


class ShippingAddress(BaseModel):
    """Shipping address for order"""
    name: str
    address: str
    phone: str
    email: Optional[str] = None


class PaymentInfo(BaseModel):
    """Payment information"""
    method: str  # card, upi, cod, etc.
    status: str = "pending"
    transaction_id: Optional[str] = None
    amount: float


class Order(BaseModel):
    """Complete order with items and tracking"""
    order_id: str
    customer_id: str
    
    # Items
    items: List[OrderItem]
    
    # Pricing
    subtotal: float
    discount: float = 0.0
    shipping_fee: float = 0.0
    tax: float = 0.0
    total: float
    
    # Status
    status: OrderStatus = OrderStatus.PENDING
    
    # Shipping
    shipping_address: ShippingAddress
    fulfillment_type: str = "home_delivery"  # home_delivery, store_pickup, click_collect
    
    # Payment
    payment_info: PaymentInfo
    
    # Tracking
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    estimated_delivery: Optional[datetime] = None
    tracking_number: Optional[str] = None
    
    # Metadata
    notes: Optional[str] = None
    applied_promotions: List[str] = Field(default_factory=list)
    loyalty_points_earned: int = 0
    loyalty_points_redeemed: int = 0
    
    def update_status(self, new_status: OrderStatus) -> None:
        """Update order status"""
        self.status = new_status
        self.updated_at = datetime.now()
    
    def get_item_count(self) -> int:
        """Get total number of items"""
        return sum(item.quantity for item in self.items)
    
    def get_summary(self) -> str:
        """Get formatted order summary"""
        return f"Order {self.order_id}: {self.get_item_count()} items, ₹{self.total:,.0f} ({self.status.value})"
    
    def calculate_totals(self) -> None:
        """Recalculate all totals"""
        self.subtotal = sum(item.get_subtotal() for item in self.items)
        self.total = self.subtotal - self.discount + self.shipping_fee + self.tax
        self.updated_at = datetime.now()