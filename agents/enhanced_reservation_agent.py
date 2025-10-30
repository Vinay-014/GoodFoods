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
Your role is to help customers find restaurants, make reservations, and answer questions naturally.

IMPORTANT GUIDELINES:
1. Be conversational and friendly - don't show technical details to users
2. When users want to book a table, gather all needed information naturally:
   - Restaurant choice
   - Date and time  
   - Number of people
   - Customer name, phone, email
3. If information is missing, ask for it politely
4. Once you have all details, proceed with the booking
5. Confirm the reservation clearly when successful

DO NOT show technical tool calls or internal processes to the user.
DO NOT mention "search_restaurants", "create_reservation" or other function names.
DO speak naturally like a helpful restaurant host.

Available cuisines: Italian, Mexican, Chinese, Indian, American, Japanese, French, Thai, Mediterranean, Vegan
Price ranges: $ (Budget), $$ (Moderate), $$$ (Fine Dining), $$$$ (Luxury)

Start by warmly greeting the user and offering help with their dining needs."""
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
                result = enhanced_reservation_tools.create_reservation(**arguments)
            elif function_name == "cancel_reservation":
                result = enhanced_reservation_tools.cancel_reservation(**arguments)
            elif function_name == "get_reservation_details":
                result = enhanced_reservation_tools.get_reservation_details(**arguments)
            elif function_name == "get_restaurant_recommendations":
                result = enhanced_reservation_tools.get_restaurant_recommendations(**arguments)
            else:
                result = {"error": f"Unknown tool: {function_name}"}
            
            # For create_reservation, return the result directly without nesting
            if function_name == "create_reservation":
                return result  # Return the actual reservation data directly
            else:
                return {"success": True, "result": result}
            
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