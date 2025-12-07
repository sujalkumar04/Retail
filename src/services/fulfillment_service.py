"""Fulfillment and delivery service"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
from src.utils.helpers import generate_id


class FulfillmentService:
    """Service for managing order fulfillment and delivery"""
    
    def __init__(self):
        self.deliveries = {}
    
    def schedule_delivery(
        self,
        order_id: str,
        address: str,
        fulfillment_type: str = "home_delivery",
        preferred_date: Optional[datetime] = None
    ) -> Dict:
        """Schedule delivery for an order"""
        delivery_id = generate_id("DEL")
        
        # Calculate delivery date
        if preferred_date:
            delivery_date = preferred_date
        else:
            # Default: 3 days from now
            delivery_date = datetime.now() + timedelta(days=3)
        
        delivery = {
            "delivery_id": delivery_id,
            "order_id": order_id,
            "fulfillment_type": fulfillment_type,
            "address": address,
            "scheduled_date": delivery_date,
            "status": "scheduled",
            "tracking_number": generate_id("TRK"),
            "created_at": datetime.now()
        }
        
        self.deliveries[delivery_id] = delivery
        
        return delivery
    
    def get_delivery_slots(self, location: str, date: Optional[datetime] = None) -> List[Dict]:
        """Get available delivery slots"""
        # Mock delivery slots
        base_date = date or datetime.now() + timedelta(days=1)
        
        slots = []
        for day_offset in range(7):  # Next 7 days
            slot_date = base_date + timedelta(days=day_offset)
            
            # Morning slot
            slots.append({
                "date": slot_date.strftime("%Y-%m-%d"),
                "time_slot": "9:00 AM - 12:00 PM",
                "available": True
            })
            
            # Afternoon slot
            slots.append({
                "date": slot_date.strftime("%Y-%m-%d"),
                "time_slot": "2:00 PM - 5:00 PM",
                "available": True
            })
            
            # Evening slot
            slots.append({
                "date": slot_date.strftime("%Y-%m-%d"),
                "time_slot": "5:00 PM - 8:00 PM",
                "available": True
            })
        
        return slots[:10]  # Return first 10 slots
    
    def get_pickup_locations(self, customer_location: str) -> List[Dict]:
        """Get available pickup locations"""
        # Mock pickup locations
        locations = [
            {
                "store_name": "Mumbai - Phoenix Mall",
                "address": "High Street Phoenix, Lower Parel, Mumbai",
                "distance": "2.5 km",
                "available": True
            },
            {
                "store_name": "Mumbai - Palladium",
                "address": "Palladium Mall, Lower Parel, Mumbai",
                "distance": "3.1 km",
                "available": True
            },
            {
                "store_name": "Delhi - Select Citywalk",
                "address": "Select Citywalk, Saket, New Delhi",
                "distance": "5.2 km",
                "available": True
            }
        ]
        
        return locations[:3]
    
    def track_delivery(self, tracking_number: str) -> Dict:
        """Track delivery status"""
        # Find delivery by tracking number
        for delivery in self.deliveries.values():
            if delivery.get("tracking_number") == tracking_number:
                return {
                    "tracking_number": tracking_number,
                    "status": delivery.get("status", "unknown"),
                    "scheduled_date": delivery.get("scheduled_date"),
                    "current_location": "In transit",
                    "estimated_delivery": delivery.get("scheduled_date")
                }
        
        return {
            "tracking_number": tracking_number,
            "status": "not_found"
        }
    
    def update_delivery_status(self, delivery_id: str, status: str) -> bool:
        """Update delivery status"""
        if delivery_id in self.deliveries:
            self.deliveries[delivery_id]["status"] = status
            self.deliveries[delivery_id]["updated_at"] = datetime.now()
            return True
        return False
    
    def calculate_shipping_fee(
        self,
        cart_total: float,
        fulfillment_type: str,
        customer_tier: str = "Bronze"
    ) -> float:
        """Calculate shipping fee"""
        # Free shipping thresholds by tier
        free_shipping_thresholds = {
            "Bronze": 2000,
            "Silver": 1500,
            "Gold": 1000,
            "Platinum": 0
        }
        
        threshold = free_shipping_thresholds.get(customer_tier, 2000)
        
        # Free shipping if above threshold
        if cart_total >= threshold:
            return 0.0
        
        # Store pickup is free
        if fulfillment_type in ["store_pickup", "click_collect"]:
            return 0.0
        
        # Standard shipping fee
        if fulfillment_type == "express_delivery":
            return 200.0
        
        return 100.0
