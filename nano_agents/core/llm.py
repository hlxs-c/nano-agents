import os
from typing import Optional, Iterator
from openai import OpenAI

import nano_agents

class LLM:
  """
  LLM Client, it is used to call any service compatible with the OpenAI interface and defaults to using streaming responses.

  Design Concept:
    - Parameters take precedence, environment variables serve as fallback
    - By default, it supports streaming responses for a better user experience
    - Supports multiple LLM service providers (OpenAI-compatible)
    - Unified calling interface
  """
  def __init__(
    self,
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    temperature: Optional[float] = 0.7,
    max_tokens: Optional[int] = None,
    timeout: Optional[int] = None,
    **kwargs
  ):
    """
    Initialize the LLM client, prioritizing the provided parameters; if none are given, load them from environment variables.

    Args:
      model: Model name, if not provided, read from the environment variable LLM_MODEL_ID
      api_key: API key, if not provided, read from the environment variable LLM_API_KEY
      base_url: Service provider address, if not provided, it will be read from the environment variable LLM_BASE_URL
      temperature: Default is 0.7
      max_tokens: Maximum token count
      timeout: Timeout, if not provided, it will be read from the environment variable LLM_TIME_OUT, default is 60 seconds
    """
    # Prioritize using incoming parameters, if not provided, load from environment variables
    settings = nano_agents.get_settings()
    self.model = model or settings.llm.model_name
    self.api_key = api_key or settings.llm.api_key
    self.base_url = base_url or settings.llm.base_url
    self.temperature = temperature or settings.llm.temperature
    self.max_tokens = max_tokens
    self.timeout = timeout or settings.llm.timeout
    self.kwargs = kwargs

    if not all([self.model, self.api_key, self.base_url]):
      raise ValueError("The model name, API key, and service address must be provided or defined in the .env file.")
  
    # Create OpenAI client
    self._client = OpenAI(
      api_key=self.api_key,
      base_url=self.base_url,
      timeout=self.timeout
    )
  
  def think(self, messages: list[dict[str, str]], temperature: Optional[float] = None) -> Iterator[str]:
    """
    Call the llm for thinking and return a streaming response.
    This is the main calling method, which defaults to using streaming response for a better user experience.

    Args:
      messages: message list
      temperature: temperature parameter, if not provided, use the initialized value
    Yields:
      str: Text fragment for streaming response
    """
    print(f"🧠 Calling the {self.model} model...")
    try:
      response = self._client.chat.completions.create(
        model=self.model,
        messages=messages,
        temperature=temperature if temperature is not None else self.temperature,
        max_tokens=self.max_tokens,
        stream=True
      )

      # Process streaming response
      print("✅ LLM response successful:")
      for chunk in response:
        delta = chunk.choices[0].delta
        content = getattr(delta, "content", "") or ""
        if content:
          print(content, end="", flush=True)
          yield content
      # Line break after streaming output ends
      print()
    except Exception as e:
      print(f"❌ An error occurred while calling the LLM API: {e}")
      raise RuntimeError(f"LLM call failed: {str(e)}")
  
  def invoke(self, messages: list[dict[str, str]], temperature: Optional[float] = None) -> str:
    """
    Non streaming call LLM returns a complete response.
    Suitable for scenarios that do not require streaming output.
    """
    try:
      print(f"🧠 Calling the {self.model} model...")
      response = self._client.chat.completions.create(
        model=self.model,
        messages=messages,
        temperature=temperature if temperature is not None else self.temperature,
        max_tokens=self.max_tokens
      )
      responseText = response.choices[0].message.content
      print("✅ LLM response successful:")
      print(responseText)
      return responseText
    except Exception as e:
      print(f"❌ An error occurred while calling the LLM API: {e}")
      raise RuntimeError(f"LLM call failed: {str(e)}")
  
  def stream_invoke(self, messages: list[dict[str, str]], temperature: Optional[float] = None) -> Iterator[str]:
    """
    Stream call LLM's alias method, which has the same functionality as the think method.
    Maintain backward compatibility.
    """
    yield from self.think(messages=messages, temperature=temperature)