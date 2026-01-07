from nano_agents.agents.simple_agent import SimpleAgent
from nano_agents.core.llm import LLM
from dotenv import load_dotenv

if __name__ == "__main__":
  llm = LLM()
  simpleAgent = SimpleAgent(name="simpleAgent", llm=llm)
  while True:
    print("请输入(输入q代表结束):")
    input_text = input()
    if input_text == 'q':
      break
    # test the streaming run
    for partial_response in simpleAgent.stream_run(input_text=input_text):
      pass
    # test the non-streaming run
    # response_text = simpleAgent.run(input_text=input_text)