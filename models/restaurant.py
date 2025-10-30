from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel
import uuid
from datetime import datetime, time

class CuisineType(str, Enum):
    ITALIAN = "Italian"
    MEXICAN = "Mexican"
    CHINESE = "Chinese"
    INDIAN = "Indian"
    AMERICAN = "American"
    JAPANESE = "Japanese"
    FRENCH = "French"
    THAI = "Thai"
    MEDITERRANEAN = "Mediterranean"
    VEGAN = "Vegan"

class PriceRange(str, Enum):
    BUDGET = "$"
    MODERATE = "$$"
    FINE_DINING = "$$$"
    LUXURY = "$$$$"

class Restaurant(BaseModel):
    id: str
    name: str
    location: str
    cuisine: CuisineType
    price_range: PriceRange
    capacity: int
    current_reservations: int = 0
    opening_time: time = time(11, 0)  # 11 AM
    closing_time: time = time(23, 0)  # 11 PM
    rating: float = 4.0
    special_features: List[str] = []
    contact_phone: str = ""
    address: str = ""
    
    @property
    def available_tables(self) -> int:
        return max(0, self.capacity - self.current_reservations)
    
    def is_open_at(self, target_time: time) -> bool:
        return self.opening_time <= target_time <= self.closing_time

class Reservation(BaseModel):
    id: str
    restaurant_id: str
    customer_name: str
    customer_phone: str
    customer_email: str
    party_size: int
    reservation_date: str  # YYYY-MM-DD
    reservation_time: str  # HH:MM
    special_requests: str = ""
    status: str = "confirmed"
    created_at: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "restaurant_id": self.restaurant_id,
            "customer_name": self.customer_name,
            "customer_phone": self.customer_phone,
            "customer_email": self.customer_email,
            "party_size": self.party_size,
            "reservation_date": self.reservation_date,
            "reservation_time": self.reservation_time,
            "special_requests": self.special_requests,
            "status": self.status,
            "created_at": self.created_at
        }