from pydantic import BaseModel
from typing import TypeVar, Generic, Type
from abc import  ABC, abstractmethod

# 1. Define TypeVar for generic type
InputModelType = TypeVar("InputModelType", bound=BaseModel)
OutputModelType = TypeVar("OutputModelType", bound=BaseModel)

class BaseTool(ABC, Generic[InputModelType, OutputModelType]):
  name: str           # Name of the tool
  description: str    # Description of the tool
  args_schema: Type[InputModelType]   # Schema of the tool arguments

  def run(self, **kwargs) -> OutputModelType:
    """
    Synchronized execution entry, including parameter verification
    """
    # automatically verify parameters
    validated_args = self.args_schema(**kwargs)
    return self._run(validated_args)
  
  async def arun(self, **kwargs) -> OutputModelType:
    """
    Asynchronous execution entry, including parameter verification
    """
    # automatically verify parameters
    validated_args = self.args_schema(**kwargs)
    return await self._arun(validated_args)

  @abstractmethod
  def _run(self, args: InputModelType) -> OutputModelType:
    """The specific tool subclass implements this logic."""
    pass

  async def _arun(self, args: InputModelType) -> OutputModelType:
    """
    The specific tool subclass implements this logic asynchronously.
    By default, it calls the synchronous _run method to support gradual migration.
    """
    return self._run(args)

  def to_openai_schema(self) -> dict:
    """Convert the tool to OpenAI function schema."""
    return {
      "type": "function",
      "function": {
        "name": self.name,
        "description": self.description,
        "parameters": self.args_schema.model_json_schema()
      }
    }
  