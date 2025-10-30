from typing import List, Dict, Any, Optional
from tools.reservation_tools import reservation_tools_instance

class SearchTools:
    def __init__(self):
        self.reservation_tools = reservation_tools_instance
    
    def get_restaurant_recommendations(self, 
                                     occasion: Optional[str] = None,
                                     group_type: Optional[str] = None,
                                     preferences: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get restaurant recommendations based on occasion and preferences"""
        
        all_restaurants = self.reservation_tools.restaurants
        
        # Filter based on occasion and group type
        filtered_restaurants = all_restaurants.copy()
        
        if occasion:
            occasion_lower = occasion.lower()
            if "romantic" in occasion_lower or "date" in occasion_lower or "anniversary" in occasion_lower:
                filtered_restaurants = [r for r in filtered_restaurants 
                                      if any(feat.lower() in ["romantic", "candlelit", "fine dining"] 
                                           for feat in r.special_features)]
            elif "business" in occasion_lower or "meeting" in occasion_lower:
                filtered_restaurants = [r for r in filtered_restaurants 
                                      if any(feat.lower() in ["business lunch", "private dining", "power outlets"] 
                                           for feat in r.special_features)]
            elif "family" in occasion_lower or "kids" in occasion_lower:
                filtered_restaurants = [r for r in filtered_restaurants 
                                      if any(feat.lower() in ["family friendly", "kids menu", "play area"] 
                                           for feat in r.special_features)]
            elif "celebration" in occasion_lower or "birthday" in occasion_lower:
                filtered_restaurants = [r for r in filtered_restaurants 
                                      if any(feat.lower() in ["private dining", "chef's table", "tasting menu"] 
                                           for feat in r.special_features)]
        
        if group_type:
            group_lower = group_type.lower()
            if "large" in group_lower or "group" in group_lower:
                filtered_restaurants = [r for r in filtered_restaurants if r.capacity >= 50]
            elif "small" in group_lower or "couple" in group_lower:
                filtered_restaurants = [r for r in filtered_restaurants if r.capacity <= 40]
        
        # Sort by relevance (rating and match with preferences)
        filtered_restaurants.sort(key=lambda x: x.rating, reverse=True)
        
        # Convert to response format
        results = []
        for restaurant in filtered_restaurants[:8]:  # Top 8 recommendations
            results.append({
                "id": restaurant.id,
                "name": restaurant.name,
                "location": restaurant.location,
                "cuisine": restaurant.cuisine.value,
                "price_range": restaurant.price_range.value,
                "rating": restaurant.rating,
                "available_tables": restaurant.available_tables,
                "special_features": restaurant.special_features,
                "recommendation_reason": self._get_recommendation_reason(restaurant, occasion, group_type)
            })
        
        return results
    
    def _get_recommendation_reason(self, restaurant, occasion: Optional[str], group_type: Optional[str]) -> str:
        """Generate a reason for the recommendation"""
        reasons = []
        
        if occasion:
            if "romantic" in occasion.lower():
                if any(feat.lower() in ["romantic", "candlelit"] for feat in restaurant.special_features):
                    reasons.append("perfect for romantic dinners")
                if restaurant.cuisine.value in ["French", "Italian"]:
                    reasons.append("offers romantic ambiance")
            
            if "business" in occasion.lower():
                if any(feat.lower() in ["business lunch", "power outlets"] for feat in restaurant.special_features):
                    reasons.append("ideal for business meetings")
            
            if "family" in occasion.lower():
                if any(feat.lower() in ["family friendly", "kids menu"] for feat in restaurant.special_features):
                    reasons.append("great for families with children")
        
        if group_type and "large" in group_type.lower():
            if restaurant.capacity >= 50:
                reasons.append("can accommodate large groups")
        
        if restaurant.rating >= 4.5:
            reasons.append("highly rated by customers")
        elif restaurant.rating >= 4.0:
            reasons.append("well-rated establishment")
        
        if reasons:
            return f"Recommended because: {', '.join(reasons)}"
        else:
            return "Great choice based on your preferences"

search_tools_instance = SearchTools()