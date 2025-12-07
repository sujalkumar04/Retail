"""Product catalog service"""

from typing import List, Dict, Optional
from src.models.product import Product
from src.utils.helpers import load_json_data


class ProductCatalogService:
    """Service for product search and filtering"""
    
    def __init__(self):
        self.products_data = load_json_data("products.json")
        self.products = self._load_products()
    
    def _load_products(self) -> List[Product]:
        """Load products from JSON data"""
        products = []
        for product_data in self.products_data.get("products", []):
            try:
                products.append(Product(**product_data))
            except Exception as e:
                print(f"Error loading product {product_data.get('sku')}: {e}")
        return products
    
    def get_product_by_sku(self, sku: str) -> Optional[Product]:
        """Get product by SKU"""
        for product in self.products:
            if product.sku == sku:
                return product
        return None
    
    def search_products(
        self,
        query: Optional[str] = None,
        category: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        tags: Optional[List[str]] = None,
        limit: int = 10
    ) -> List[Product]:
        """Search products with filters"""
        results = self.products.copy()
        
        # Filter by query (name, description, tags)
        if query:
            query_lower = query.lower()
            results = [
                p for p in results
                if (query_lower in p.name.lower() or
                    query_lower in p.description.lower() or
                    any(query_lower in tag.lower() for tag in p.tags))
            ]
        
        # Filter by category
        if category:
            results = [p for p in results if p.category.lower() == category.lower()]
        
        # Filter by price range
        if min_price is not None:
            results = [p for p in results if p.price >= min_price]
        if max_price is not None:
            results = [p for p in results if p.price <= max_price]
        
        # Filter by tags
        if tags:
            results = [
                p for p in results
                if any(tag.lower() in [t.lower() for t in p.tags] for tag in tags)
            ]
        
        return results[:limit]
    
    def get_recommendations(
        self,
        customer_preferences: Dict,
        limit: int = 5
    ) -> List[Product]:
        """Get product recommendations based on preferences"""
        matching_products = [
            p for p in self.products
            if p.matches_preferences(customer_preferences)
        ]
        
        # Sort by rating and discount
        matching_products.sort(
            key=lambda p: (p.ratings.average, p.discount_percent),
            reverse=True
        )
        
        return matching_products[:limit]
    
    def get_complementary_products(self, sku: str, limit: int = 3) -> List[Product]:
        """Get complementary products for a given SKU"""
        product = self.get_product_by_sku(sku)
        if not product or not product.complementary_products:
            return []
        
        complementary = []
        for comp_sku in product.complementary_products[:limit]:
            comp_product = self.get_product_by_sku(comp_sku)
            if comp_product:
                complementary.append(comp_product)
        
        return complementary
    
    def get_products_by_category(self, category: str, limit: int = 10) -> List[Product]:
        """Get products by category"""
        return self.search_products(category=category, limit=limit)
    
    def get_all_categories(self) -> List[Dict]:
        """Get all product categories"""
        return self.products_data.get("categories", [])
