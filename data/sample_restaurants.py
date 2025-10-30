import random
from models.restaurant import Restaurant, CuisineType, PriceRange
from datetime import time

def generate_sample_restaurants(count: int = 75) -> list[Restaurant]:
    """Generate sample restaurant data"""
    
    restaurant_names = [
        "Bella", "Sapore", "Gusto", "Trattoria", "Ristorante", "Cafe", "Bistro",
        "Grill", "Kitchen", "Table", "Feast", "Harvest", "Vine", "Spice", "Flame",
        "Ocean", "Garden", "Market", "Street", "Urban", "Classic", "Modern"
    ]
    
    location_areas = [
        "Downtown", "Midtown", "Uptown", "East Side", "West End", "North District",
        "South Quarter", "Central Plaza", "Riverside", "Harbor View", "City Center",
        "Metro", "Historic District", "Financial District", "Arts Quarter"
    ]
    
    features_list = [
        ["Outdoor Seating", "Live Music", "Wine Bar"],
        ["Private Dining", "Chef's Table", "Tasting Menu"],
        ["Family Friendly", "Kids Menu", "Play Area"],
        ["Romantic", "Candlelit", "Fine Dining"],
        ["Business Lunch", "Free WiFi", "Power Outlets"],
        ["Wheelchair Access", "Vegetarian Options", "Gluten Free"],
        ["Late Night", "Happy Hour", "Cocktail Bar"],
        ["Waterfront", "Skyline View", "Rooftop"]
    ]
    
    restaurants = []
    
    for i in range(count):
        name_base = random.choice(restaurant_names)
        name_suffix = random.choice([" Italian", " Grill", " Kitchen", " Bistro", " Cafe", ""])
        restaurant_name = f"{name_base}{name_suffix}"
        
        location = f"{random.choice(location_areas)}"
        
        # Ensure diverse cuisine distribution
        cuisine = random.choice(list(CuisineType))
        
        # Capacity based on restaurant type
        if cuisine in [CuisineType.FRENCH, CuisineType.JAPANESE]:
            capacity = random.randint(15, 50)
            price_range = random.choice([PriceRange.FINE_DINING, PriceRange.LUXURY])
        elif cuisine == CuisineType.AMERICAN:
            capacity = random.randint(50, 150)
            price_range = random.choice([PriceRange.BUDGET, PriceRange.MODERATE])
        else:
            capacity = random.randint(30, 100)
            price_range = random.choice(list(PriceRange))
        
        # Rating based on price range
        base_rating = 4.0
        if price_range in [PriceRange.FINE_DINING, PriceRange.LUXURY]:
            base_rating += random.uniform(0.3, 0.8)
        else:
            base_rating += random.uniform(0.0, 0.5)
        
        restaurant = Restaurant(
            id=f"rest_{i+1:03d}",
            name=restaurant_name,
            location=location,
            cuisine=cuisine,
            price_range=price_range,
            capacity=capacity,
            current_reservations=random.randint(0, capacity // 2),
            rating=round(base_rating, 1),
            special_features=random.sample(
                random.choice(features_list), 
                random.randint(1, 3)
            ),
            contact_phone=f"+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
            address=f"{random.randint(100, 999)} {random.choice(['Main', 'Oak', 'Maple', 'Park', 'Broadway'])} St, {location}"
        )
        
        restaurants.append(restaurant)
    
    return restaurants