"""Customer data models"""

from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class CustomerPreferences(BaseModel):
    """Customer style and shopping preferences"""
    styles: List[str] = Field(default_factory=list)
    colors: List[str] = Field(default_factory=list)
    sizes: Dict[str, str] = Field(default_factory=dict)
    budget_range: str = "mid"


class SavedAddress(BaseModel):
    """Customer saved address"""
    type: str  # home, office, etc.
    address: str
    is_default: bool = False


class SavedPaymentMethod(BaseModel):
    """Customer saved payment method"""
    type: str  # card, upi, etc.
    last_four: Optional[str] = None
    brand: Optional[str] = None
    id: Optional[str] = None


class PurchaseHistoryItem(BaseModel):
    """Individual purchase record"""
    order_id: str
    date: str
    items: List[Dict]
    total: float


class Customer(BaseModel):
    """Customer profile with complete information"""
    id: str
    name: str
    email: str
    phone: str
    age: Optional[int] = None
    gender: Optional[str] = None
    
    # Loyalty
    loyalty_tier: str = "Bronze"
    loyalty_points: int = 0
    member_since: Optional[str] = None
    
    # Preferences
    preferred_store: Optional[str] = None
    preferred_channel: Optional[str] = None
    device_preferences: List[str] = Field(default_factory=list)
    preferences: CustomerPreferences = Field(default_factory=CustomerPreferences)
    
    # History
    purchase_history: List[PurchaseHistoryItem] = Field(default_factory=list)
    browsing_history: List[str] = Field(default_factory=list)
    wishlist: List[str] = Field(default_factory=list)
    
    # Saved information
    saved_addresses: List[SavedAddress] = Field(default_factory=list)
    saved_payment_methods: List[SavedPaymentMethod] = Field(default_factory=list)
    
    def get_total_spent(self) -> float:
        """Calculate total amount spent by customer"""
        return sum(item.total for item in self.purchase_history)
    
    def get_default_address(self) -> Optional[SavedAddress]:
        """Get default shipping address"""
        for addr in self.saved_addresses:
            if addr.is_default:
                return addr
        return self.saved_addresses[0] if self.saved_addresses else None
    
    def get_purchase_summary(self) -> str:
        """Get formatted purchase history summary"""
        if not self.purchase_history:
            return "No previous purchases"
        
        recent = self.purchase_history[-3:]  # Last 3 orders
        summary = []
        for item in recent:
            summary.append(f"Order {item.order_id} on {item.date}: ₹{item.total}")
        return "; ".join(summary)