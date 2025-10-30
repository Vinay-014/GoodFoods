import requests
import json
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class LLMClient:
    def __init__(self, base_url: str, api_key: str, model: str):
        self.base_url = base_url
        self.api_key = api_key
        self.model = model
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def generate_response(self, messages: List[Dict[str, str]], tools: List[Dict] = None) -> Dict[str, Any]:
        """Generate response from LLM with optional tool calling"""
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.1,
            "max_tokens": 1000
        }
        
        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"LLM API error: {response.status_code} - {response.text}")
                return {"error": f"API error: {response.status_code}"}
                
        except Exception as e:
            logger.error(f"LLM request failed: {str(e)}")
            return {"error": str(e)}
    
    def extract_tool_calls(self, response: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract tool calls from LLM response"""
        tool_calls = []
        
        try:
            choices = response.get("choices", [])
            if choices:
                message = choices[0].get("message", {})
                if "tool_calls" in message:
                    for tool_call in message["tool_calls"]:
                        tool_calls.append({
                            "id": tool_call.get("id"),
                            "function": tool_call["function"]["name"],
                            "arguments": json.loads(tool_call["function"]["arguments"])
                        })
        except Exception as e:
            logger.error(f"Error extracting tool calls: {str(e)}")
        
        return tool_calls