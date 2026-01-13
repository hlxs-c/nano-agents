from nano_agents.core.config import Settings

# 定义一个全局变量，初始化为None
_global_settings: Settings = None

def setup(env_file: str = ".env"):
  global _global_settings
  _global_settings = Settings(_env_file=env_file)
  return _global_settings

def get_settings() -> Settings:
  global _global_settings
  if _global_settings is None:
    _global_settings = Settings()
  return _global_settings