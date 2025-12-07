"""Demo conversation scenarios"""

DEMO_SCENARIOS = [
    {
        "name": "Product Discovery",
        "customer_id": "CUST001",
        "messages": [
            "Hi, I'm looking for a dress for a summer party",
            "Show me something in pastel colors",
            "Do you have the pink floral one in size M?",
            "Great! Add it to my cart",
            "What else would go well with this dress?"
        ]
    },
    {
        "name": "Loyalty & Checkout",
        "customer_id": "CUST002",
        "messages": [
            "Hello, I'd like to check my loyalty points",
            "Are there any active promotions?",
            "I want to buy a formal suit",
            "Show me navy blue suits in size 42",
            "Add the Navy Blue Formal Suit to cart",
            "I'd like to checkout",
            "Use my saved Amex card",
            "Schedule delivery for tomorrow afternoon"
        ]
    },
    {
        "name": "Inventory Check",
        "customer_id": "CUST003",
        "messages": [
            "Do you have skinny fit jeans in size 26?",
            "What colors are available?",
            "Is it available for store pickup?",
            "Which stores have it?",
            "I'll pick it up from Bangalore UB City"
        ]
    },
    {
        "name": "Post-Purchase Support",
        "customer_id": "CUST001",
        "messages": [
            "I want to track my recent order",
            "When will it be delivered?",
            "Can I change the delivery address?",
            "I'd like to return an item from my last order"
        ]
    }
]


def get_scenario(name: str):
    """Get scenario by name"""
    for scenario in DEMO_SCENARIOS:
        if scenario["name"] == name:
            return scenario
    return None


def list_scenarios():
    """List all available scenarios"""
    return [s["name"] for s in DEMO_SCENARIOS]
