"""Payment gateway service (mock implementation)"""

from typing import Dict, Optional, List
from datetime import datetime
from src.utils.helpers import generate_id


class PaymentGatewayService:
    """Mock payment gateway for processing payments"""
    
    def __init__(self):
        self.transactions = {}
    
    def process_payment(
        self,
        amount: float,
        payment_method: str,
        customer_id: str,
        order_id: str,
        payment_details: Optional[Dict] = None
    ) -> Dict:
        """
        Process a payment (mock implementation)
        Returns payment result with transaction ID
        """
        # Generate transaction ID
        transaction_id = generate_id("TXN")
        
        # Mock payment processing
        # In production, this would integrate with actual payment gateway
        result = {
            "success": True,
            "transaction_id": transaction_id,
            "amount": amount,
            "payment_method": payment_method,
            "status": "completed",
            "timestamp": datetime.now().isoformat(),
            "message": "Payment processed successfully"
        }
        
        # Store transaction
        self.transactions[transaction_id] = {
            "customer_id": customer_id,
            "order_id": order_id,
            "amount": amount,
            "method": payment_method,
            "status": "completed",
            "created_at": datetime.now()
        }
        
        return result
    
    def verify_payment(self, transaction_id: str) -> Dict:
        """Verify payment status"""
        if transaction_id in self.transactions:
            return {
                "verified": True,
                "status": self.transactions[transaction_id]["status"]
            }
        return {
            "verified": False,
            "status": "not_found"
        }
    
    def refund_payment(self, transaction_id: str, amount: Optional[float] = None) -> Dict:
        """Process refund (mock implementation)"""
        if transaction_id not in self.transactions:
            return {
                "success": False,
                "message": "Transaction not found"
            }
        
        transaction = self.transactions[transaction_id]
        refund_amount = amount or transaction["amount"]
        
        refund_id = generate_id("REF")
        
        return {
            "success": True,
            "refund_id": refund_id,
            "amount": refund_amount,
            "status": "refunded",
            "timestamp": datetime.now().isoformat()
        }
    
    def get_payment_methods(self, customer_id: str) -> List[Dict]:
        """Get available payment methods for customer"""
        # Mock payment methods
        return [
            {"type": "card", "name": "Credit/Debit Card"},
            {"type": "upi", "name": "UPI"},
            {"type": "netbanking", "name": "Net Banking"},
            {"type": "wallet", "name": "Digital Wallet"},
            {"type": "cod", "name": "Cash on Delivery"}
        ]
    
    def calculate_payment_fee(self, amount: float, payment_method: str) -> float:
        """Calculate payment processing fee"""
        # Mock fee calculation
        fees = {
            "card": 0.02,  # 2%
            "upi": 0.0,    # Free
            "netbanking": 0.01,  # 1%
            "wallet": 0.0,
            "cod": 50.0  # Flat fee
        }
        
        if payment_method == "cod":
            return fees["cod"]
        
        fee_percent = fees.get(payment_method, 0.0)
        return amount * fee_percent
