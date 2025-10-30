from typing import List, Dict, Any, Optional
from datetime import datetime, time, timedelta
import uuid
import re
from models.restaurant import Restaurant, Reservation, CuisineType, PriceRange
from data.sample_restaurants import generate_sample_restaurants
from tools.tool_registry import tool_registry

class EnhancedReservationTools:
    def __init__(self):
        self.restaurants = generate_sample_restaurants(75)
        self.reservations: List[Reservation] = []
        self.conversation_context = {}
    
    @tool_registry.register_tool
    def search_restaurants(self, 
                          cuisine: Optional[str] = None,
                          location: Optional[str] = None,
                          party_size: Optional[int] = None,
                          price_range: Optional[str] = None,
                          date: Optional[str] = None,
                          time: Optional[str] = None,
                          features: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Search for restaurants based on multiple criteria including cuisine, location, 
        party size, price range, date, time, and special features.
        
        Args:
            cuisine: Type of cuisine (Italian, Mexican, Chinese, etc.)
            location: Area or neighborhood to search in
            party_size: Number of people in the party (1-20)
            price_range: Budget range ($, $$, $$$, $$$$)
            date: Reservation date in YYYY-MM-DD format
            time: Reservation time in HH:MM format  
            features: Special features like outdoor seating, romantic, etc.
        """
        filtered_restaurants = self.restaurants.copy()
        
        # Apply filters - only if values are provided and not "null"
        if cuisine and cuisine.lower() != "null":
            filtered_restaurants = [r for r in filtered_restaurants 
                                  if cuisine.lower() in r.cuisine.value.lower()]
        
        if location and location.lower() != "null":
            filtered_restaurants = [r for r in filtered_restaurants 
                                  if location.lower() in r.location.lower()]
        
        if party_size:
            # Ensure party_size is integer and within valid range
            try:
                party_size_int = int(party_size)
                if 1 <= party_size_int <= 20:
                    filtered_restaurants = [r for r in filtered_restaurants 
                                          if r.available_tables >= party_size_int]
            except (ValueError, TypeError):
                # If party_size is invalid, ignore the filter
                pass
        
        if price_range and price_range != "null":
            filtered_restaurants = [r for r in filtered_restaurants 
                                  if r.price_range.value == price_range]
        
        if features:
            # Handle both list and single string features
            if isinstance(features, str):
                features = [features]
            
            for feature in features:
                if feature and feature.lower() != "null":
                    filtered_restaurants = [r for r in filtered_restaurants 
                                          if any(f.lower() == feature.lower() 
                                               for f in r.special_features)]
        
        # Sort by relevance (rating, then availability)
        filtered_restaurants.sort(key=lambda x: (x.rating, x.available_tables), reverse=True)
        
        return self._format_restaurant_results(filtered_restaurants[:10])

    
    @tool_registry.register_tool
    def check_availability(self, restaurant_id: str, date: str, time: str, party_size: int) -> Dict[str, Any]:
        """
        Check real-time availability for a specific restaurant, date, and time.
        
        Args:
            restaurant_id: Unique identifier for the restaurant
            date: Reservation date in YYYY-MM-DD format
            time: Reservation time in HH:MM format
            party_size: Number of people in the party
        """
        restaurant = next((r for r in self.restaurants if r.id == restaurant_id), None)
        if not restaurant:
            return {"available": False, "message": "Restaurant not found"}
        
        # Validate date and time
        if not self._validate_date(date):
            return {"available": False, "message": "Invalid date format. Use YYYY-MM-DD"}
        
        if not self._validate_time(time):
            return {"available": False, "message": "Invalid time format. Use HH:MM"}
        
        # Check capacity
        if restaurant.available_tables < party_size:
            return {
                "available": False, 
                "message": f"Not enough tables available for {party_size} people. Only {restaurant.available_tables} tables left."
            }
        
        # Check restaurant hours
        reservation_time = datetime.strptime(time, "%H:%M").time()
        if not restaurant.is_open_at(reservation_time):
            return {
                "available": False,
                "message": f"Restaurant is closed at {time}. Open from {restaurant.opening_time} to {restaurant.closing_time}"
            }
        
        # Check if date is too far in future
        reservation_date = datetime.strptime(date, "%Y-%m-%d")
        max_date = datetime.now() + timedelta(days=30)
        if reservation_date > max_date:
            return {
                "available": False,
                "message": "Reservations can only be made up to 30 days in advance"
            }
        
        return {
            "available": True,
            "restaurant_name": restaurant.name,
            "restaurant_id": restaurant.id,
            "party_size": party_size,
            "date": date,
            "time": time,
            "available_tables": restaurant.available_tables,
            "message": "Table available! Ready to book your reservation."
        }
    
    @tool_registry.register_tool
    def create_reservation(self, 
                          restaurant_id: str,
                          customer_name: str,
                          customer_phone: str,
                          customer_email: str,
                          party_size: int,
                          date: str,
                          time: str,
                          special_requests: str = "") -> Dict[str, Any]:
        """
        Create a new restaurant reservation with customer details and special requests.
        
        Args:
            restaurant_id: ID of the restaurant to book
            customer_name: Full name of the customer
            customer_phone: Contact phone number
            customer_email: Contact email address
            party_size: Number of people in the party
            date: Reservation date in YYYY-MM-DD format
            time: Reservation time in HH:MM format
            special_requests: Any special requirements or dietary needs
        """
        # Validate inputs
        validation_result = self._validate_reservation_inputs(
            customer_name, customer_phone, customer_email, party_size, date, time
        )
        if not validation_result["valid"]:
            return {"success": False, "message": validation_result["message"]}
        
        # Check availability
        availability = self.check_availability(restaurant_id, date, time, party_size)
        if not availability["available"]:
            return {"success": False, "message": availability["message"]}
        
        # Create reservation
        reservation = Reservation(
            id=f"RES_{uuid.uuid4().hex[:8].upper()}",
            restaurant_id=restaurant_id,
            customer_name=customer_name,
            customer_phone=customer_phone,
            customer_email=customer_email,
            party_size=party_size,
            reservation_date=date,
            reservation_time=time,
            special_requests=special_requests,
            created_at=datetime.now().isoformat()
        )
        
        # Update restaurant occupancy
        restaurant = next(r for r in self.restaurants if r.id == restaurant_id)
        restaurant.current_reservations += 1
        
        self.reservations.append(reservation)
        
        return {
            "success": True,
            "reservation_id": reservation.id,
            "confirmation_number": reservation.id,
            "restaurant_name": restaurant.name,
            "customer_name": customer_name,
            "party_size": party_size,
            "date": date,
            "time": time,
            "special_requests": special_requests,
            "message": f"🎉 Reservation confirmed! Your confirmation number is {reservation.id}"
        }
    
    @tool_registry.register_tool
    def cancel_reservation(self, reservation_id: str) -> Dict[str, Any]:
        """
        Cancel an existing reservation by reservation ID.
        
        Args:
            reservation_id: The unique reservation ID to cancel
        """
        reservation = next((r for r in self.reservations if r.id == reservation_id), None)
        if not reservation:
            return {"success": False, "message": "Reservation not found. Please check your reservation ID."}
        
        # Update restaurant occupancy
        restaurant = next((r for r in self.restaurants if r.id == reservation.restaurant_id), None)
        if restaurant:
            restaurant.current_reservations = max(0, restaurant.current_reservations - 1)
        
        # Remove reservation
        self.reservations = [r for r in self.reservations if r.id != reservation_id]
        
        return {
            "success": True,
            "cancelled_reservation_id": reservation_id,
            "message": f"Reservation {reservation_id} has been successfully cancelled."
        }
    
    @tool_registry.register_tool
    def get_reservation_details(self, reservation_id: str) -> Dict[str, Any]:
        """
        Retrieve detailed information about a specific reservation.
        
        Args:
            reservation_id: The unique reservation ID to look up
        """
        reservation = next((r for r in self.reservations if r.id == reservation_id), None)
        if not reservation:
            return {"found": False, "message": "Reservation not found"}
        
        restaurant = next((r for r in self.restaurants if r.id == reservation.restaurant_id), None)
        
        return {
            "found": True,
            "reservation": reservation.to_dict(),
            "restaurant": {
                "name": restaurant.name if restaurant else "Unknown",
                "location": restaurant.location if restaurant else "Unknown",
                "address": restaurant.address if restaurant else "Unknown",
                "cuisine": restaurant.cuisine.value if restaurant else "Unknown",
                "phone": restaurant.contact_phone if restaurant else "Unknown"
            }
        }
    
    @tool_registry.register_tool
    def get_restaurant_recommendations(self, 
                                     occasion: Optional[str] = None,
                                     group_type: Optional[str] = None,
                                     preferences: Optional[str] = None,
                                     budget: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get personalized restaurant recommendations based on occasion, group type, preferences, and budget.
        
        Args:
            occasion: Type of occasion (romantic, business, family, celebration, etc.)
            group_type: Size and type of group (couple, large group, family, etc.)
            preferences: Any specific preferences or requirements
            budget: Price range preference ($, $$, $$$, $$$$)
        """
        all_restaurants = self.restaurants.copy()
        filtered_restaurants = all_restaurants
        
        # Filter by occasion
        if occasion:
            occasion_lower = occasion.lower()
            if any(word in occasion_lower for word in ["romantic", "date", "anniversary"]):
                filtered_restaurants = [r for r in filtered_restaurants 
                                      if any(feat.lower() in ["romantic", "candlelit", "fine dining"] 
                                           for feat in r.special_features)]
            elif any(word in occasion_lower for word in ["business", "meeting"]):
                filtered_restaurants = [r for r in filtered_restaurants 
                                      if any(feat.lower() in ["business lunch", "private dining", "power outlets"] 
                                           for feat in r.special_features)]
            elif any(word in occasion_lower for word in ["family", "kids"]):
                filtered_restaurants = [r for r in filtered_restaurants 
                                      if any(feat.lower() in ["family friendly", "kids menu", "play area"] 
                                           for feat in r.special_features)]
        
        # Filter by group type
        if group_type:
            group_lower = group_type.lower()
            if any(word in group_lower for word in ["large", "group"]):
                filtered_restaurants = [r for r in filtered_restaurants if r.capacity >= 50]
            elif any(word in group_lower for word in ["small", "couple"]):
                filtered_restaurants = [r for r in filtered_restaurants if r.capacity <= 40]
        
        # Filter by budget
        if budget:
            filtered_restaurants = [r for r in filtered_restaurants if r.price_range.value == budget]
        
        # Calculate relevance scores
        scored_restaurants = []
        for restaurant in filtered_restaurants:
            score = self._calculate_recommendation_score(restaurant, occasion, group_type, preferences)
            scored_restaurants.append((restaurant, score))
        
        # Sort by score
        scored_restaurants.sort(key=lambda x: x[1], reverse=True)
        
        # Format results
        results = []
        for restaurant, score in scored_restaurants[:8]:
            result = {
                "id": restaurant.id,
                "name": restaurant.name,
                "location": restaurant.location,
                "cuisine": restaurant.cuisine.value,
                "price_range": restaurant.price_range.value,
                "rating": restaurant.rating,
                "available_tables": restaurant.available_tables,
                "special_features": restaurant.special_features,
                "match_score": round(score, 2),
                "recommendation_reason": self._generate_recommendation_reason(restaurant, occasion, group_type)
            }
            results.append(result)
        
        return results
    
    def _calculate_recommendation_score(self, restaurant, occasion, group_type, preferences) -> float:
        """Calculate relevance score for recommendations"""
        score = restaurant.rating
        
        # Occasion bonus
        if occasion:
            occasion_lower = occasion.lower()
            if "romantic" in occasion_lower and any(feat.lower() in ["romantic", "candlelit"] for feat in restaurant.special_features):
                score += 1.0
            if "business" in occasion_lower and any(feat.lower() in ["business lunch", "private dining"] for feat in restaurant.special_features):
                score += 0.8
            if "family" in occasion_lower and any(feat.lower() in ["family friendly", "kids menu"] for feat in restaurant.special_features):
                score += 0.8
        
        # Group type suitability
        if group_type:
            group_lower = group_type.lower()
            if "large" in group_lower and restaurant.capacity >= 50:
                score += 0.5
            if "small" in group_lower and restaurant.capacity <= 40:
                score += 0.3
        
        return score
    
    def _generate_recommendation_reason(self, restaurant, occasion, group_type) -> str:
        """Generate personalized recommendation reason"""
        reasons = []
        
        if restaurant.rating >= 4.5:
            reasons.append("excellent ratings")
        elif restaurant.rating >= 4.0:
            reasons.append("highly rated")
        
        if occasion:
            if "romantic" in occasion.lower() and any(feat.lower() in ["romantic", "candlelit"] for feat in restaurant.special_features):
                reasons.append("perfect for romantic occasions")
            if "business" in occasion.lower() and any(feat.lower() in ["business lunch", "private dining"] for feat in restaurant.special_features):
                reasons.append("ideal for business meetings")
            if "family" in occasion.lower() and any(feat.lower() in ["family friendly", "kids menu"] for feat in restaurant.special_features):
                reasons.append("great for families")
        
        if reasons:
            return f"Recommended because: {', '.join(reasons)}"
        return "A wonderful dining option based on your preferences"
    
    def _format_restaurant_results(self, restaurants: List[Restaurant]) -> List[Dict[str, Any]]:
        """Format restaurant objects for API response"""
        return [
            {
                "id": r.id,
                "name": r.name,
                "location": r.location,
                "cuisine": r.cuisine.value,
                "price_range": r.price_range.value,
                "rating": r.rating,
                "available_tables": r.available_tables,
                "capacity": r.capacity,
                "special_features": r.special_features,
                "contact_phone": r.contact_phone,
                "address": r.address,
                "opening_time": r.opening_time.strftime("%H:%M"),
                "closing_time": r.closing_time.strftime("%H:%M")
            }
            for r in restaurants
        ]
    
    def _validate_reservation_inputs(self, name, phone, email, party_size, date, time):
        """Validate reservation inputs"""
        if not all([name.strip(), phone.strip(), email.strip()]):
            return {"valid": False, "message": "Please provide complete customer information"}
        
        if party_size <= 0 or party_size > 20:
            return {"valid": False, "message": "Party size must be between 1 and 20 people"}
        
        if not self._validate_email(email):
            return {"valid": False, "message": "Please provide a valid email address"}
        
        if not self._validate_phone(phone):
            return {"valid": False, "message": "Please provide a valid phone number"}
        
        if not self._validate_date(date):
            return {"valid": False, "message": "Invalid date format. Please use YYYY-MM-DD"}
        
        if not self._validate_time(time):
            return {"valid": False, "message": "Invalid time format. Please use HH:MM"}
        
        return {"valid": True, "message": "All inputs are valid"}
    
    def _validate_email(self, email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def _validate_phone(self, phone: str) -> bool:
        # Basic phone validation
        cleaned = re.sub(r'[\s\-\(\)]', '', phone)
        return cleaned.isdigit() and len(cleaned) >= 10
    
    def _validate_date(self, date_str: str) -> bool:
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False
    
    def _validate_time(self, time_str: str) -> bool:
        try:
            datetime.strptime(time_str, '%H:%M')
            return True
        except ValueError:
            return False

# Global instance
enhanced_reservation_tools = EnhancedReservationTools()