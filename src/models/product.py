"""Product catalog models"""

from typing import List, Dict, Optional
from pydantic import BaseModel, Field


class ProductRating(BaseModel):
    """Product rating information"""
    average: float = 0.0
    count: int = 0


class Product(BaseModel):
    """Product with complete details"""
    sku: str
    name: str
    category: str
    subcategory: str
    brand: str
    
    # Pricing
    price: float
    original_price: float
    discount_percent: int = 0
    
    # Details
    description: str
    fabric: Optional[str] = None
    care: Optional[str] = None
    
    # Variants
    sizes: List[str] = Field(default_factory=list)
    colors: List[str] = Field(default_factory=list)
    
    # Media
    images: List[str] = Field(default_factory=list)
    
    # Metadata
    tags: List[str] = Field(default_factory=list)
    ratings: ProductRating = Field(default_factory=ProductRating)
    complementary_products: List[str] = Field(default_factory=list)
    
    def get_formatted_price(self) -> str:
        """Get formatted price with currency"""
        return f"₹{self.price:,.0f}"
    
    def get_discount_info(self) -> str:
        """Get discount information"""
        if self.discount_percent > 0:
            return f"{self.discount_percent}% off (was ₹{self.original_price:,.0f})"
        return "No discount"
    
    def matches_preferences(self, preferences: Dict) -> bool:
        """Check if product matches customer preferences"""
        if not preferences:
            return True
        
        # Check budget range
        budget_ranges = {
            "budget": (0, 2000),
            "mid": (2000, 5000),
            "mid-premium": (5000, 15000),
            "premium": (15000, 30000),
            "luxury": (30000, float('inf'))
        }
        
        budget_range = preferences.get("budget_range", "mid")
        min_price, max_price = budget_ranges.get(budget_range, (0, float('inf')))
        
        if not (min_price <= self.price <= max_price):
            return False
        
        # Check styles
        pref_styles = preferences.get("styles", [])
        if pref_styles:
            product_tags_lower = [tag.lower() for tag in self.tags]
            if not any(style.lower() in product_tags_lower for style in pref_styles):
                return False
        
        return True


class ProductCategory(BaseModel):
    """Product category"""
    id: str
    name: str
    parent: Optional[str] = None