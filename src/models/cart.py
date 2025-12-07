"""Shopping cart models"""

from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class CartItem(BaseModel):
    """Individual item in shopping cart"""
    sku: str
    name: str
    price: float
    quantity: int = 1
    size: Optional[str] = None
    color: Optional[str] = None
    image: Optional[str] = None
    
    def get_subtotal(self) -> float:
        """Calculate subtotal for this item"""
        return self.price * self.quantity


class Cart(BaseModel):
    """Shopping cart with items and calculations"""
    customer_id: str
    items: List[CartItem] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    def add_item(self, item: CartItem) -> None:
        """Add item to cart or update quantity if exists"""
        # Check if item already exists (same SKU, size, color)
        for existing_item in self.items:
            if (existing_item.sku == item.sku and 
                existing_item.size == item.size and 
                existing_item.color == item.color):
                existing_item.quantity += item.quantity
                self.updated_at = datetime.now()
                return
        
        # Add new item
        self.items.append(item)
        self.updated_at = datetime.now()
    
    def remove_item(self, sku: str, size: Optional[str] = None, color: Optional[str] = None) -> bool:
        """Remove item from cart"""
        for i, item in enumerate(self.items):
            if (item.sku == sku and 
                (size is None or item.size == size) and 
                (color is None or item.color == color)):
                self.items.pop(i)
                self.updated_at = datetime.now()
                return True
        return False
    
    def update_quantity(self, sku: str, quantity: int, size: Optional[str] = None, color: Optional[str] = None) -> bool:
        """Update item quantity"""
        for item in self.items:
            if (item.sku == sku and 
                (size is None or item.size == size) and 
                (color is None or item.color == color)):
                if quantity <= 0:
                    return self.remove_item(sku, size, color)
                item.quantity = quantity
                self.updated_at = datetime.now()
                return True
        return False
    
    def get_subtotal(self) -> float:
        """Calculate cart subtotal"""
        return sum(item.get_subtotal() for item in self.items)
    
    def get_item_count(self) -> int:
        """Get total number of items"""
        return sum(item.quantity for item in self.items)
    
    def clear(self) -> None:
        """Clear all items from cart"""
        self.items = []
        self.updated_at = datetime.now()
    
    def is_empty(self) -> bool:
        """Check if cart is empty"""
        return len(self.items) == 0
    
    def get_summary(self) -> str:
        """Get formatted cart summary"""
        if self.is_empty():
            return "Cart is empty"
        
        summary = f"{self.get_item_count()} items, Total: ₹{self.get_subtotal():,.0f}"
        return summary