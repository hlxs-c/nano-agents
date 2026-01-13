from typing import Optional, Iterator

from nano_agents.core.agent import Agent
from nano_agents.core.llm import LLM
from nano_agents.core.message import Message

class SimpleAgent(Agent):
  """Simple agent for chat."""

  def __init__(
    self,
    name: str,
    llm: LLM,
    system_prompt: Optional[str] = None,
  ):
    super().__init__(name, llm, system_prompt)
  
  def run(self, input_text: str, **kwargs):
    """
    Run the simple agent.
    Args:
      input_text: user input.
      **kwargs: other args.
    Returns:
      agent response.
    """
    # construct a message list for the current round of chat
    messages = []

    # add the system message
    if self.system_prompt:
      messages.append({"role": "system", "content": self.system_prompt})
    
    # add the history messages to the message list
    for msg in self._history:
      messages.append(msg.to_dict())
    
    # add current user message
    messages.append({"role": "user", "content": input_text})

    # call the llm
    response = self.llm.invoke(messages=messages, **kwargs)

    # save to history
    self._history.append(Message(role="user", content=input_text))
    self._history.append(Message(role="assistant", content=response))

    return response

  def stream_run(self, input_text: str, **kwargs):
    """
    Streaming run the agent.
    Args:
      input_text: user input.
      **kwargs: other args.
    Yields:
      Agent response chunk.
    """
    # construct a message list for the current round of chat
    messages = []

    # add the system message
    if self.system_prompt:
      messages.append({"role": "system", "content": self.system_prompt})
    
    # add the history messages to the message list
    for msg in self._history:
      messages.append(msg.to_dict())
    
    # add current user message
    messages.append({"role": "user", "content": input_text})

    # streaming call the llm
    full_response = ""
    for chunk in self.llm.stream_invoke(messages=messages, **kwargs):
      full_response += chunk
      yield chunk
    
    # save complete conversation to history
    self.add_message(Message(role="user", content=input_text))
    self.add_message(Message(role="assistant", content=full_response))