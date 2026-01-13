import nano_agents
from nano_agents.core.llm import LLM

# 框架配置初始化
nano_agents.setup("../.env")

if __name__ == "__main__":
  try:
    llmClient = LLM()

    exampleMessages = [
      {"role": "system", "content": "You are a helpful assistant that writes Python code."},
      {"role": "user", "content": "写一个快速排序算法"}
    ]

    # 测试流式响应
    for chunk in llmClient.think(messages=exampleMessages):
      continue

    # 测试非流式响应
    # responseText = llmClient.invoke(messages=exampleMessages)

  except Exception as e:
    print(e)