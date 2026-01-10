from pydantic import BaseModel
from typing import Type, Any
from abc import abstractmethod

class BaseTool(BaseModel):
  name: str           # 工具名称
  description: str    # 工具描述
  args_schema: Type[BaseModel]   # 工具的参数结构

  def run(self, **kwargs) -> Any:
    """
    Synchronized execution entry, including parameter verification
    """
    # automatically verify parameters
    validated_args = self.args_schema(**kwargs)
    return self._run(validated_args)
  
  @abstractmethod
  def _run(self, args: BaseModel) -> Any:
    """The specific tool subclass implements this logic."""
    pass

  def to_openai_schema(self) -> dict:
    return {
      "type": "function",
      "function": {
        "name": self.name,
        "description": self.description,
        "parameters": self.args_schema.model_json_schema()
      }
    }
  