from datetime import datetime, time
import re

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_phone(phone: str) -> bool:
    """Validate phone number format"""
    # Basic validation - can be enhanced based on requirements
    pattern = r'^[\+]?[1-9][\d]{0,15}$'
    return bool(re.match(pattern, phone.replace(' ', '').replace('-', '')))

def validate_date(date_str: str) -> bool:
    """Validate date format YYYY-MM-DD"""
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validate_time(time_str: str) -> bool:
    """Validate time format HH:MM"""
    try:
        datetime.strptime(time_str, '%H:%M')
        return True
    except ValueError:
        return False

def get_future_dates(days: int = 30):
    """Get list of future dates for dropdowns"""
    today = datetime.now()
    return [(today + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(days)]

def format_restaurant_display(restaurant):
    """Format restaurant information for display"""
    return f"""
**{restaurant['name']}** ⭐ {restaurant['rating']}
*{restaurant['cuisine']} • {restaurant['price_range']} • {restaurant['location']}*
📞 {restaurant['contact_phone']}
📍 {restaurant['address']}
🎯 Features: {', '.join(restaurant['special_features'])}
🪑 Available Tables: {restaurant['available_tables']}
"""