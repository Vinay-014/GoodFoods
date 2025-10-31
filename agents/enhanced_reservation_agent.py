from typing import List, Dict, Any, Tuple
import json
import logging
from utils.llm_client import LLMClient
from tools.tool_registry import tool_registry
from tools.enhanced_reservation_tools import enhanced_reservation_tools
from config import config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedReservationAgent:
    def __init__(self):
        self.llm_client = LLMClient(
            base_url=config.LLM_BASE_URL,
            api_key=config.LLM_API_KEY,
            model=config.LLM_MODEL
        )
        self.tools = tool_registry.get_tool_schemas()
        self.conversation_history: List[Dict[str, str]] = [
            {
                "role": "system",
                "content": """You are a friendly and helpful AI assistant for GoodFoods restaurant reservations. 

CRITICAL: When creating reservations, you MUST use valid restaurant IDs from search results.
- Restaurant IDs always start with "rest_" followed by numbers (e.g., "rest_001", "rest_042")
- NEVER make up restaurant IDs like "Italian_dinner_date" or "romantic_spot"
- ALWAYS use the exact restaurant_id from search results

Steps for booking:
1. First search for restaurants using search_restaurants
2. Get valid restaurant_id from the search results  
3. Use that exact restaurant_id when calling create_reservation

If you don't have a valid restaurant_id, search for restaurants first.

Be conversational and helpful. Don't show technical details to users."""
            }
        ]
    
    def process_message(self, user_message: str) -> Tuple[str, Dict[str, Any]]:
        """Process user message with natural conversation flow"""
        
        # Add user message to conversation history
        self.conversation_history.append({"role": "user", "content": user_message})
        
        # Get LLM response with tool calling
        response = self.llm_client.generate_response(
            messages=self.conversation_history,
            tools=self.tools
        )
        
        if "error" in response:
            error_msg = "I'm having some technical issues right now. Please try again in a moment."
            self.conversation_history.append({"role": "assistant", "content": error_msg})
            return error_msg, {}
        
        assistant_message = response["choices"][0]["message"]
        tool_results = {}
        
        # Handle tool calls
        if "tool_calls" in assistant_message:
            tool_calls = self.llm_client.extract_tool_calls(response)
            
            for tool_call in tool_calls:
                function_name = tool_call["function"]
                arguments = tool_call["arguments"]
                
                # Execute the tool
                result = self._execute_tool(function_name, arguments)
                tool_results[function_name] = result
                
                # Add tool response to conversation
                self.conversation_history.append({
                    "role": "tool",
                    "content": json.dumps({"result": result}),
                    "tool_call_id": tool_call["id"]
                })
            
            # Get final natural response after tool execution
            final_response = self.llm_client.generate_response(
                messages=self.conversation_history
            )
            
            if "error" not in final_response:
                final_message = final_response["choices"][0]["message"]["content"]
                self.conversation_history.append({"role": "assistant", "content": final_message})
                return final_message, tool_results
            else:
                error_msg = "I encountered an issue while processing your request. Let's try that again."
                self.conversation_history.append({"role": "assistant", "content": error_msg})
                return error_msg, tool_results
        else:
            # No tool calls needed
            message_content = assistant_message["content"]
            self.conversation_history.append({"role": "assistant", "content": message_content})
            return message_content, tool_results
    
    def _execute_tool(self, function_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Safely execute tools with proper error handling"""
        try:
            # Use the global instance directly
            if function_name == "search_restaurants":
                result = enhanced_reservation_tools.search_restaurants(**arguments)
            elif function_name == "check_availability":
                result = enhanced_reservation_tools.check_availability(**arguments)
            elif function_name == "create_reservation":
                # Validate restaurant_id before creating reservation
                restaurant_id = arguments.get('restaurant_id', '')
                if not restaurant_id or not restaurant_id.startswith('rest_'):
                    # Try to find a restaurant by name
                    restaurant_name = arguments.get('restaurant_name', '')
                    if restaurant_name:
                        # Search for restaurant by name to get valid ID
                        search_results = enhanced_reservation_tools.search_restaurants(
                            cuisine=None, location=None, party_size=arguments.get('party_size')
                        )
                        # Find restaurant by name match
                        matching_restaurant = next(
                            (r for r in search_results if r['name'].lower() == restaurant_name.lower()), 
                            None
                        )
                        if matching_restaurant:
                            arguments['restaurant_id'] = matching_restaurant['id']
                        else:
                            return {"success": False, "error": f"Restaurant '{restaurant_name}' not found"}
                    else:
                        return {"success": False, "error": "Invalid restaurant ID provided"}
                
                result = enhanced_reservation_tools.create_reservation(**arguments)
            elif function_name == "cancel_reservation":
                result = enhanced_reservation_tools.cancel_reservation(**arguments)
            elif function_name == "get_reservation_details":
                result = enhanced_reservation_tools.get_reservation_details(**arguments)
            elif function_name == "get_restaurant_recommendations":
                result = enhanced_reservation_tools.get_restaurant_recommendations(**arguments)
            else:
                result = {"error": f"Unknown tool: {function_name}"}
            
            return result
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def clear_conversation(self):
        """Clear conversation history and reset to initial state"""
        self.conversation_history = [
            {
                "role": "system",
                "content": """You are a friendly and helpful AI assistant for GoodFoods restaurant reservations. 
Help customers find restaurants, make reservations, and answer questions naturally.

Be conversational and don't show technical details. Gather information politely and confirm bookings clearly."""
            }
        ]