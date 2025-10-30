from typing import List, Dict, Any
from tools.reservation_tools import reservation_tools_instance
import random

class RecommendationEngine:
    def __init__(self):
        self.restaurants = reservation_tools_instance.restaurants
    
    def get_personalized_recommendations(self, 
                                      user_preferences: Dict[str, Any],
                                      previous_bookings: List[str] = None) -> List[Dict[str, Any]]:
        """Get personalized restaurant recommendations based on user preferences and history"""
        
        filtered_restaurants = self.restaurants.copy()
        
        # Apply preference filters
        if user_preferences.get("cuisine"):
            cuisine_pref = user_preferences["cuisine"].lower()
            filtered_restaurants = [r for r in filtered_restaurants 
                                  if cuisine_pref in r.cuisine.value.lower()]
        
        if user_preferences.get("location"):
            location_pref = user_preferences["location"].lower()
            filtered_restaurants = [r for r in filtered_restaurants 
                                  if location_pref in r.location.lower()]
        
        if user_preferences.get("price_range"):
            price_pref = user_preferences["price_range"]
            filtered_restaurants = [r for r in filtered_restaurants 
                                  if r.price_range.value == price_pref]
        
        if user_preferences.get("party_size"):
            party_size = user_preferences["party_size"]
            filtered_restaurants = [r for r in filtered_restaurants 
                                  if r.available_tables >= party_size]
        
        # Apply occasion-based filtering
        occasion = user_preferences.get("occasion", "").lower()
        if occasion:
            if "romantic" in occasion:
                filtered_restaurants = [r for r in filtered_restaurants 
                                      if any(feat.lower() in ["romantic", "candlelit", "fine dining"] 
                                           for feat in r.special_features)]
            elif "business" in occasion:
                filtered_restaurants = [r for r in filtered_restaurants 
                                      if any(feat.lower() in ["business lunch", "private dining"] 
                                           for feat in r.special_features)]
            elif "family" in occasion:
                filtered_restaurants = [r for r in filtered_restaurants 
                                      if any(feat.lower() in ["family friendly", "kids menu"] 
                                           for feat in r.special_features)]
            elif "celebration" in occasion:
                filtered_restaurants = [r for r in filtered_restaurants 
                                      if any(feat.lower() in ["private dining", "chef's table"] 
                                           for feat in r.special_features)]
        
        # Sort by relevance score
        filtered_restaurants.sort(key=lambda x: self._calculate_relevance_score(x, user_preferences), reverse=True)
        
        # Convert to response format
        recommendations = []
        for restaurant in filtered_restaurants[:6]:  # Top 6 recommendations
            rec = {
                "id": restaurant.id,
                "name": restaurant.name,
                "location": restaurant.location,
                "cuisine": restaurant.cuisine.value,
                "price_range": restaurant.price_range.value,
                "rating": restaurant.rating,
                "available_tables": restaurant.available_tables,
                "special_features": restaurant.special_features,
                "match_score": self._calculate_relevance_score(restaurant, user_preferences),
                "recommendation_reason": self._generate_recommendation_reason(restaurant, user_preferences)
            }
            recommendations.append(rec)
        
        return recommendations
    
    def _calculate_relevance_score(self, restaurant, user_preferences: Dict[str, Any]) -> float:
        """Calculate relevance score for a restaurant based on user preferences"""
        score = restaurant.rating  # Start with base rating
        
        # Cuisine match
        if user_preferences.get("cuisine"):
            if user_preferences["cuisine"].lower() in restaurant.cuisine.value.lower():
                score += 1.0
        
        # Location match
        if user_preferences.get("location"):
            if user_preferences["location"].lower() in restaurant.location.lower():
                score += 0.5
        
        # Price range match
        if user_preferences.get("price_range"):
            if restaurant.price_range.value == user_preferences["price_range"]:
                score += 0.5
        
        # Party size suitability
        if user_preferences.get("party_size"):
            if restaurant.available_tables >= user_preferences["party_size"]:
                score += 0.3
        
        # Occasion suitability
        occasion = user_preferences.get("occasion", "").lower()
        if occasion:
            if "romantic" in occasion and any(feat.lower() in ["romantic", "candlelit"] for feat in restaurant.special_features):
                score += 0.7
            if "business" in occasion and any(feat.lower() in ["business lunch", "private dining"] for feat in restaurant.special_features):
                score += 0.7
            if "family" in occasion and any(feat.lower() in ["family friendly", "kids menu"] for feat in restaurant.special_features):
                score += 0.7
        
        return round(score, 2)
    
    def _generate_recommendation_reason(self, restaurant, user_preferences: Dict[str, Any]) -> str:
        """Generate a personalized reason for recommending this restaurant"""
        reasons = []
        
        # Rating-based reason
        if restaurant.rating >= 4.5:
            reasons.append("excellent ratings")
        elif restaurant.rating >= 4.0:
            reasons.append("high customer satisfaction")
        
        # Cuisine match
        if user_preferences.get("cuisine"):
            if user_preferences["cuisine"].lower() in restaurant.cuisine.value.lower():
                reasons.append("matches your preferred cuisine")
        
        # Location convenience
        if user_preferences.get("location"):
            if user_preferences["location"].lower() in restaurant.location.lower():
                reasons.append("convenient location")
        
        # Occasion suitability
        occasion = user_preferences.get("occasion", "").lower()
        if occasion:
            if "romantic" in occasion and any(feat.lower() in ["romantic", "candlelit"] for feat in restaurant.special_features):
                reasons.append("perfect for romantic occasions")
            if "business" in occasion and any(feat.lower() in ["business lunch", "private dining"] for feat in restaurant.special_features):
                reasons.append("ideal for business meetings")
            if "family" in occasion and any(feat.lower() in ["family friendly", "kids menu"] for feat in restaurant.special_features):
                reasons.append("great for family gatherings")
        
        # Special features
        if restaurant.special_features:
            notable_features = [feat for feat in restaurant.special_features 
                              if feat not in ["Wheelchair Access", "Vegetarian Options", "Gluten Free"]]
            if notable_features:
                reasons.append(f"features: {', '.join(notable_features[:2])}")
        
        if reasons:
            return f"Recommended because: {', '.join(reasons)}"
        else:
            return "A wonderful dining option based on availability"
    
    def get_trending_restaurants(self) -> List[Dict[str, Any]]:
        """Get currently trending/popular restaurants"""
        # Simulate trending based on rating and availability
        trending = sorted(self.restaurants, 
                         key=lambda x: (x.rating, x.available_tables), 
                         reverse=True)[:5]
        
        return [
            {
                "id": r.id,
                "name": r.name,
                "cuisine": r.cuisine.value,
                "location": r.location,
                "rating": r.rating,
                "trending_reason": "Highly rated and good availability"
            }
            for r in trending
        ]