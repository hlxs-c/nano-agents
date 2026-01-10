import json

from nano_agents.tools.tool_manager import ToolManager
from nano_agents.tools.builtin.websearch import WebSearchTool

if __name__ == "__main__":
  manager = ToolManager()
  manager.register(WebSearchTool())

  # 1. 获取输入给LLM的工具 schema
  print(json.dumps(manager.get_tools_schema()))

  # 2. 模拟执行（Agent 拿到 LLM（或者解析出来的） 的JSON后调用）
  tool = manager.get_tool("web_search")
  result = tool.run(query="Python Agent", max_results=3)
  print(result)