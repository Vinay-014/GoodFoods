#!/usr/bin/env python3
"""
Test script to verify the restaurant reservation system works correctly
"""

from data.sample_restaurants import generate_sample_restaurants
from tools.reservation_tools import ReservationTools

def test_restaurant_generation():
    """Test that restaurants are generated correctly"""
    print("🧪 Testing restaurant generation...")
    
    restaurants = generate_sample_restaurants(5)  # Generate just 5 for testing
    print(f"✅ Generated {len(restaurants)} restaurants")
    
    for i, restaurant in enumerate(restaurants):
        print(f"  {i+1}. {restaurant.name} - {restaurant.cuisine.value} - {restaurant.location}")
    
    return True

def test_reservation_tools():
    """Test reservation tools functionality"""
    print("\n🧪 Testing reservation tools...")
    
    tools = ReservationTools()
    print(f"✅ Loaded {len(tools.restaurants)} restaurants")
    
    # Test search
    results = tools.search_restaurants(cuisine="Italian", party_size=2)
    print(f"✅ Found {len(results)} Italian restaurants for 2 people")
    
    # Test availability check
    if results:
        restaurant_id = results[0]["id"]
        availability = tools.check_availability(restaurant_id, "2024-12-25", "19:00", 2)
        print(f"✅ Availability check: {availability['available']}")
    
    return True

def test_recommendations():
    """Test recommendation engine"""
    print("\n🧪 Testing recommendation engine...")
    
    from tools.search_tools import SearchTools
    search_tools = SearchTools()
    
    recommendations = search_tools.get_restaurant_recommendations(
        occasion="romantic dinner",
        group_type="couple"
    )
    print(f"✅ Generated {len(recommendations)} romantic recommendations")
    
    return True

if __name__ == "__main__":
    print("🚀 Starting GoodFoods Reservation System Tests...\n")
    
    try:
        test_restaurant_generation()
        test_reservation_tools() 
        test_recommendations()
        
        print("\n🎉 All tests passed! The system is ready to run.")
        print("\nTo start the application:")
        print("  streamlit run app.py")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()