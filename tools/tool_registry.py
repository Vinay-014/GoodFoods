from typing import Dict, Any, Callable, List, Optional, Union
import inspect
from datetime import datetime

class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, Dict[str, Any]] = {}
        self.functions: Dict[str, Callable] = {}
    
    def register_tool(self, func: Callable) -> Callable:
        tool_schema = self._generate_tool_schema(func)
        self.tools[func.__name__] = tool_schema
        self.functions[func.__name__] = func
        return func
    
    def _generate_tool_schema(self, func: Callable) -> Dict[str, Any]:
        sig = inspect.signature(func)
        parameters = {"type": "object", "properties": {}, "required": []}
        
        for name, param in sig.parameters.items():
            if name == 'self':
                continue
            param_info = {"type": self._python_type_to_json_type(param.annotation)}
            if param.default == inspect.Parameter.empty:
                parameters["required"].append(name)
            parameters["properties"][name] = param_info
        
        return {
            "type": "function",
            "function": {
                "name": func.__name__,
                "description": func.__doc__ or "",
                "parameters": parameters
            }
        }
    
    def _python_type_to_json_type(self, py_type) -> str:
        type_map = {str: "string", int: "integer", float: "number", bool: "boolean", 
                   list: "array", dict: "object", Optional[str]: "string", 
                   Optional[int]: "integer", Optional[float]: "number", 
                   Optional[bool]: "boolean", Optional[list]: "array", 
                   Optional[dict]: "object"}
        return type_map.get(py_type, "string")
    
    def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        if tool_name not in self.functions:
            return {"error": f"Tool {tool_name} not found"}
        
        try:
            clean_arguments = self._convert_arguments(tool_name, arguments)
            result = self.functions[tool_name](**clean_arguments)
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _convert_arguments(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        if tool_name not in self.functions:
            return arguments
        
        sig = inspect.signature(self.functions[tool_name])
        converted_args = {}
        
        for param_name, param_value in arguments.items():
            if param_name not in sig.parameters:
                continue
            if param_value is None:
                continue
                
            param_type = sig.parameters[param_name].annotation
            try:
                if param_type == int or param_type == Optional[int]:
                    converted_args[param_name] = int(param_value)
                elif param_type == float or param_type == Optional[float]:
                    converted_args[param_name] = float(param_value)
                elif param_type == bool or param_type == Optional[bool]:
                    if isinstance(param_value, str):
                        converted_args[param_name] = param_value.lower() in ['true', '1', 'yes', 'y']
                    else:
                        converted_args[param_name] = bool(param_value)
                else:
                    converted_args[param_name] = param_value
            except (ValueError, TypeError):
                converted_args[param_name] = param_value
        
        return converted_args
    
    def get_tool_schemas(self) -> List[Dict[str, Any]]:
        return list(self.tools.values())

tool_registry = ToolRegistry()