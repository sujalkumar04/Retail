"""Inventory management service"""

from typing import Dict, List, Optional, Tuple
from src.utils.helpers import load_json_data


class InventoryService:
    """Service for checking inventory and availability"""
    
    def __init__(self):
        self.inventory_data = load_json_data("inventory.json")
        self.inventory = self.inventory_data.get("inventory", {})
        self.warehouses = self.inventory_data.get("warehouses", [])
        self.delivery_estimates = self.inventory_data.get("delivery_estimates", {})
    
    def check_availability(
        self,
        sku: str,
        color: Optional[str] = None,
        size: Optional[str] = None,
        location: str = "online"
    ) -> Tuple[bool, int]:
        """
        Check if product is available
        Returns: (is_available, quantity)
        """
        if sku not in self.inventory:
            return False, 0
        
        product_inventory = self.inventory[sku]
        
        # Check online inventory
        if location == "online":
            online_inv = product_inventory.get("online", {})
            
            if color and size:
                quantity = online_inv.get(color, {}).get(size, 0)
            elif color:
                quantity = sum(online_inv.get(color, {}).values())
            elif size:
                quantity = sum(
                    sizes.get(size, 0)
                    for sizes in online_inv.values()
                )
            else:
                quantity = sum(
                    sum(sizes.values())
                    for sizes in online_inv.values()
                )
            
            return quantity > 0, quantity
        
        # Check store inventory
        else:
            stores_inv = product_inventory.get("stores", {})
            store_inv = stores_inv.get(location, {})
            
            if color and size:
                quantity = store_inv.get(color, {}).get(size, 0)
            elif color:
                quantity = sum(store_inv.get(color, {}).values())
            elif size:
                quantity = sum(
                    sizes.get(size, 0)
                    for sizes in store_inv.values()
                )
            else:
                quantity = sum(
                    sum(sizes.values())
                    for sizes in store_inv.values()
                )
            
            return quantity > 0, quantity
    
    def get_available_stores(self, sku: str, color: Optional[str] = None, size: Optional[str] = None) -> List[str]:
        """Get list of stores where product is available"""
        if sku not in self.inventory:
            return []
        
        stores_inv = self.inventory[sku].get("stores", {})
        available_stores = []
        
        for store_name, store_inv in stores_inv.items():
            is_available, _ = self.check_availability(sku, color, size, store_name)
            if is_available:
                available_stores.append(store_name)
        
        return available_stores
    
    def get_delivery_estimate(self, customer_location: str, fulfillment_type: str = "standard") -> str:
        """Get delivery time estimate"""
        # Simplified logic - in production, this would use actual location data
        if "Mumbai" in customer_location or "Delhi" in customer_location:
            location_type = "same_city"
        elif any(city in customer_location for city in ["Bangalore", "Chennai", "Hyderabad", "Pune"]):
            location_type = "metro_to_metro"
        else:
            location_type = "other"
        
        estimates = self.delivery_estimates.get(location_type, {})
        return estimates.get(fulfillment_type, "4-6 days")
    
    def get_fulfillment_options(
        self,
        sku: str,
        color: Optional[str],
        size: Optional[str],
        customer_location: str
    ) -> Dict:
        """Get all fulfillment options for a product"""
        options = {
            "home_delivery": {
                "available": False,
                "estimate": None
            },
            "store_pickup": {
                "available": False,
                "stores": []
            },
            "click_collect": {
                "available": False,
                "stores": []
            }
        }
        
        # Check online availability for home delivery
        is_available, quantity = self.check_availability(sku, color, size, "online")
        if is_available:
            options["home_delivery"]["available"] = True
            options["home_delivery"]["estimate"] = self.get_delivery_estimate(customer_location)
        
        # Check store availability
        available_stores = self.get_available_stores(sku, color, size)
        if available_stores:
            options["store_pickup"]["available"] = True
            options["store_pickup"]["stores"] = available_stores
            options["click_collect"]["available"] = True
            options["click_collect"]["stores"] = available_stores
        
        return options
    
    def reserve_inventory(self, sku: str, color: str, size: str, quantity: int = 1) -> bool:
        """Reserve inventory for checkout (mock implementation)"""
        is_available, available_qty = self.check_availability(sku, color, size)
        return is_available and available_qty >= quantity
