"""Loyalty and promotions service"""

from typing import Dict, List, Optional
from datetime import datetime
from src.utils.helpers import load_json_data


class LoyaltyService:
    """Service for loyalty points and promotions"""
    
    def __init__(self):
        loyalty_data = load_json_data("loyalty_rules.json")
        promotions_data = load_json_data("promotions.json")
        
        self.tiers = loyalty_data.get("loyalty_tiers", [])
        self.earning_rules = loyalty_data.get("points_earning_rules", {})
        self.redemption_rules = loyalty_data.get("points_redemption_rules", {})
        
        self.promotions = promotions_data.get("promotions", [])
        self.coupons = promotions_data.get("coupon_codes", [])
    
    def get_tier_info(self, points: int) -> Dict:
        """Get loyalty tier information based on points"""
        for tier in self.tiers:
            min_points = tier.get("min_points", 0)
            max_points = tier.get("max_points")
            
            if max_points is None:
                if points >= min_points:
                    return tier
            elif min_points <= points <= max_points:
                return tier
        
        return self.tiers[0] if self.tiers else {}
    
    def calculate_points_earned(
        self,
        amount: float,
        customer_tier: str = "Bronze",
        category: Optional[str] = None
    ) -> int:
        """Calculate loyalty points earned from purchase"""
        base_rule = self.earning_rules.get("base_rule", {})
        points_per_100 = base_rule.get("points_per_100", 1)
        
        # Base points
        base_points = int((amount / 100) * points_per_100)
        
        # Apply tier multiplier
        tier_info = next((t for t in self.tiers if t["tier"] == customer_tier), None)
        if tier_info:
            multiplier = tier_info.get("benefits", {}).get("points_multiplier", 1.0)
            base_points = int(base_points * multiplier)
        
        # Apply category multiplier
        if category:
            category_multipliers = self.earning_rules.get("category_multipliers", {})
            category_mult = category_multipliers.get(category, 1.0)
            base_points = int(base_points * category_mult)
        
        return base_points
    
    def get_points_value(self, points: int) -> float:
        """Convert points to currency value"""
        redemption_rate = self.redemption_rules.get("redemption_rate", {})
        points_to_currency = redemption_rate.get("points_to_currency", 1.0)
        return points * points_to_currency
    
    def get_applicable_promotions(
        self,
        cart_total: float,
        customer_tier: str = "Bronze",
        categories: Optional[List[str]] = None
    ) -> List[Dict]:
        """Get applicable promotions for current purchase"""
        applicable = []
        
        for promo in self.promotions:
            if not promo.get("active", False):
                continue
            
            # Check minimum purchase amount
            min_amount = promo.get("min_purchase_amount", 0)
            if cart_total < min_amount:
                continue
            
            # Check categories
            promo_categories = promo.get("applicable_categories", [])
            if promo_categories and categories:
                if not any(cat in promo_categories for cat in categories):
                    continue
            
            # Check customer type
            applicable_to = promo.get("applicable_to")
            if applicable_to and applicable_to == "platinum_members" and customer_tier != "Platinum":
                continue
            
            applicable.append(promo)
        
        return applicable
    
    def apply_promotion(self, promotion: Dict, cart_total: float) -> float:
        """Calculate discount from promotion"""
        promo_type = promotion.get("type")
        value = promotion.get("value", 0)
        
        if promo_type == "percentage_discount":
            discount = (cart_total * value) / 100
            max_discount = promotion.get("max_discount")
            if max_discount:
                discount = min(discount, max_discount)
            return discount
        
        elif promo_type == "flat_discount":
            return value
        
        return 0.0
    
    def validate_coupon(self, code: str, customer_tier: str = "Bronze") -> Optional[Dict]:
        """Validate coupon code"""
        for coupon in self.coupons:
            if coupon.get("code") == code and coupon.get("active", False):
                # Check customer eligibility
                applicable_to = coupon.get("applicable_to")
                if applicable_to:
                    if applicable_to == "new_customers":
                        # Would check if customer is new
                        pass
                    elif applicable_to == "platinum_members" and customer_tier != "Platinum":
                        continue
                
                return coupon
        
        return None
    
    def get_best_promotion(
        self,
        cart_total: float,
        customer_tier: str = "Bronze",
        categories: Optional[List[str]] = None
    ) -> Optional[Dict]:
        """Get the best applicable promotion"""
        applicable = self.get_applicable_promotions(cart_total, customer_tier, categories)
        
        if not applicable:
            return None
        
        # Find promotion with maximum discount
        best_promo = None
        max_discount = 0.0
        
        for promo in applicable:
            discount = self.apply_promotion(promo, cart_total)
            if discount > max_discount:
                max_discount = discount
                best_promo = promo
        
        return best_promo
