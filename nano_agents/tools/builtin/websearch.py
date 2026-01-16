from pydantic import BaseModel, Field
from typing import Type

from nano_agents.tools.base_tool import BaseTool

class WebSearchInput(BaseModel):
  query: str = Field(description="The search query text.")
  max_results: int = Field(description="Number of results to return.", default=5)

class WebSearchOutput(BaseModel):
  results: list[str]

class WebSearchTool(BaseTool):
  name: str = "web_search"
  description: str = "Search the internet for information."
  args_schema: Type[BaseModel] = WebSearchInput

  def _run(self, args: WebSearchInput) -> WebSearchOutput:
    return WebSearchOutput(results=[f"Result {i}" for i in range(args.max_results)])