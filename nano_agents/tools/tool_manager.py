from typing import Dict, Optional
from .base_tool import BaseTool

class ToolManager:
  def __init__(self):
    self.tools: Dict[str, BaseTool] = {}
  
  def register(self, tool: BaseTool):
    self.tools[tool.name] = tool
  
  def get_tool(self, name: str) -> Optional[BaseTool]:
    return self.tools.get(name)
  
  def get_tools_schema(self) -> list[dict]:
    """Generate the tools parameter directly for passing to LLM"""
    return [tool.to_openai_schema() for tool in self.tools.values()]
