from typing import Optional, Dict, Any, Literal
from datetime import datetime
from pydantic import BaseModel, Field

# Define the type of message role and restrict its possible values
MessageRole = Literal["user", "assistant", "system", "tool"]

class Message(BaseModel):
  """Message class"""
  content: str
  role: MessageRole
  timestamp: datetime = Field(default_factory=datetime.now)
  metadata: Dict[str, Any] = Field(default_factory=dict)
  
  def to_dict(self) -> Dict[str, Any]:
    """Convert to dictionary format (OpenAI API format)"""
    return {
      "role": self.role,
      "content": self.content
    }

  def __str__(self) -> str:
    return f"[{self.role}] {self.content}"