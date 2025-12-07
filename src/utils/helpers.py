"""Helper utility functions"""

import json
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime


def format_currency(amount: float, currency_symbol: str = "₹") -> str:
    """Format amount as currency"""
    return f"{currency_symbol}{amount:,.0f}"


def generate_id(prefix: str = "") -> str:
    """Generate unique ID with optional prefix"""
    unique_id = str(uuid.uuid4())[:8].upper()
    return f"{prefix}{unique_id}" if prefix else unique_id


def load_json_data(filename: str) -> Dict:
    """Load JSON data from data directory"""
    # Use absolute path relative to this file
    base_dir = Path(__file__).parent.parent.parent
    data_dir = base_dir / "data"
    file_path = data_dir / filename
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: {filename} not found at {file_path}")
        return {}
    except json.JSONDecodeError:
        print(f"Warning: {filename} is not valid JSON")
        return {}


def save_json_data(filename: str, data: Dict) -> bool:
    """Save JSON data to data directory"""
    # Use absolute path relative to this file
    base_dir = Path(__file__).parent.parent.parent
    data_dir = base_dir / "data"
    file_path = data_dir / filename
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except OSError as e:
        # Handle read-only filesystem (e.g. Vercel)
        print(f"Warning: Could not save {filename} (likely read-only filesystem): {e}")
        return False
    except Exception as e:
        print(f"Error saving {filename}: {e}")
        return False


def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Format datetime object"""
    return dt.strftime(format_str)


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to maximum length"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def parse_size_from_text(text: str) -> Optional[str]:
    """Extract size from user text"""
    text_lower = text.lower()
    
    # Common sizes
    sizes = ["xs", "s", "m", "l", "xl", "xxl", "free size"]
    for size in sizes:
        if size in text_lower:
            return size.upper() if size != "free size" else "Free Size"
    
    # Numeric sizes (for shoes, pants, etc.)
    import re
    numeric_match = re.search(r'\b(\d{2,3})\b', text)
    if numeric_match:
        return numeric_match.group(1)
    
    return None


def parse_color_from_text(text: str) -> Optional[str]:
    """Extract color from user text"""
    text_lower = text.lower()
    
    # Common colors
    colors = [
        "red", "blue", "green", "yellow", "black", "white", "grey", "gray",
        "pink", "purple", "orange", "brown", "navy", "maroon", "beige",
        "gold", "silver", "tan", "burgundy"
    ]
    
    for color in colors:
        if color in text_lower:
            return color.capitalize()
    
    return None


def calculate_discount(original_price: float, discounted_price: float) -> int:
    """Calculate discount percentage"""
    if original_price <= 0:
        return 0
    discount = ((original_price - discounted_price) / original_price) * 100
    return int(discount)


def validate_phone(phone: str) -> bool:
    """Validate Indian phone number"""
    import re
    pattern = r'^(\+91)?[6-9]\d{9}$'
    return bool(re.match(pattern, phone.replace("-", "").replace(" ", "")))


def validate_email(email: str) -> bool:
    """Validate email address"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))
