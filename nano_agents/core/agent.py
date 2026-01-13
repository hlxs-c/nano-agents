from abc import ABC, abstractmethod
from typing import Optional
from .message import Message
from .llm import LLM

class Agent(ABC):
  """Base Agent class"""
  def __init__(
    self,
    name: str,
    llm: LLM,
    system_prompt: Optional[str] = None,
  ):
    self.name = name
    self.llm = llm
    self.system_prompt = system_prompt
    self._history: list[Message] = []

  @abstractmethod
  def run(self, input_text: str, **kwargs) -> str:
    """Run Agent"""
    pass

  def add_message(self, message: Message):
    """Add message to the history"""
    self._history.append(message)
  
  def clear_history(self):
    """Clear the history"""
    self._history.clear()
  
  def get_history(self) -> list[Message]:
    """Get the history"""
    return self._history.copy()

  def __str__(self):
    return f"Agent(name={self.name}, model={self.llm.model})"

  def __repr__(self):
    return self.__str__()