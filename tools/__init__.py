from typing import List, Dict, Any

def get_tool_definitions() -> List[Dict[str, Any]]:
    """Define all available tools for the LLM"""
    
    return [
        {
            "type": "function",
            "function": {
                "name": "search_restaurants",
                "description": "Search for restaurants based on cuisine, location, party size, price range, and availability",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "cuisine": {
                            "type": "string",
                            "description": "Type of cuisine (Italian, Mexican, Chinese, etc.)"
                        },
                        "location": {
                            "type": "string", 
                            "description": "Location or area to search in"
                        },
                        "party_size": {
                            "type": "integer",
                            "description": "Number of people in the party"
                        },
                        "price_range": {
                            "type": "string",
                            "description": "Price range ($, $$, $$$, $$$$)"
                        },
                        "date": {
                            "type": "string",
                            "description": "Reservation date in YYYY-MM-DD format"
                        },
                        "time": {
                            "type": "string", 
                            "description": "Reservation time in HH:MM format"
                        }
                    },
                    "required": []
                }
            }
        },
        {
            "type": "function", 
            "function": {
                "name": "check_availability",
                "description": "Check availability for a specific restaurant, date, and time",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "restaurant_id": {
                            "type": "string",
                            "description": "ID of the restaurant to check"
                        },
                        "date": {
                            "type": "string",
                            "description": "Reservation date in YYYY-MM-DD format"
                        },
                        "time": {
                            "type": "string",
                            "description": "Reservation time in HH:MM format" 
                        },
                        "party_size": {
                            "type": "integer",
                            "description": "Number of people in the party"
                        }
                    },
                    "required": ["restaurant_id", "date", "time", "party_size"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "create_reservation", 
                "description": "Create a new reservation at a restaurant",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "restaurant_id": {
                            "type": "string",
                            "description": "ID of the restaurant"
                        },
                        "customer_name": {
                            "type": "string",
                            "description": "Name of the customer"
                        },
                        "customer_phone": {
                            "type": "string", 
                            "description": "Phone number of the customer"
                        },
                        "customer_email": {
                            "type": "string",
                            "description": "Email address of the customer"
                        },
                        "party_size": {
                            "type": "integer", 
                            "description": "Number of people in the party"
                        },
                        "date": {
                            "type": "string",
                            "description": "Reservation date in YYYY-MM-DD format"
                        },
                        "time": {
                            "type": "string",
                            "description": "Reservation time in HH:MM format"
                        },
                        "special_requests": {
                            "type": "string",
                            "description": "Any special requests or dietary requirements"
                        }
                    },
                    "required": ["restaurant_id", "customer_name", "customer_phone", "customer_email", "party_size", "date", "time"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "cancel_reservation",
                "description": "Cancel an existing reservation",
                "parameters": {
                    "type": "object", 
                    "properties": {
                        "reservation_id": {
                            "type": "string",
                            "description": "ID of the reservation to cancel"
                        }
                    },
                    "required": ["reservation_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_reservation_details", 
                "description": "Get details of a specific reservation",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reservation_id": {
                            "type": "string",
                            "description": "ID of the reservation to look up"
                        }
                    },
                    "required": ["reservation_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_restaurant_recommendations",
                "description": "Get personalized restaurant recommendations based on occasion, group type, and preferences",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "occasion": {
                            "type": "string", 
                            "description": "Type of occasion (romantic dinner, business meeting, family gathering, celebration, etc.)"
                        },
                        "group_type": {
                            "type": "string",
                            "description": "Type of group (large group, small group, couple, family, etc.)"
                        },
                        "preferences": {
                            "type": "string",
                            "description": "Any specific preferences or requirements"
                        }
                    },
                    "required": []
                }
            }
        }
    ]