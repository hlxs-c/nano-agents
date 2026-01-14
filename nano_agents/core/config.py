from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

class LLMConfig(BaseModel):
  api_key: str
  base_url: str
  model_name: str
  temperature: float = 0.7
  timeout: int = 60

class Settings(BaseSettings):
  # 模块化配置
  llm: LLMConfig

  # 配置读取规则
  model_config = SettingsConfigDict(
    env_prefix="NANO_",         # 环境变量前缀，防止冲突
    env_nested_delimiter="__",  # 支持嵌套，NANO_LLM__API_KEY
    env_file_encoding="utf-8",
    extra="ignore"              # 忽略其他前缀开头的环境变量
  )