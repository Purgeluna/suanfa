# from langchain_community.llms.tongyi import Tongyi
#
# model=Tongyi(model="qwen-max")
#
# res=model.stream(input="你是谁。你可以做些什么？")
# for chunk in res:
#     print(chunk,end="",flush=True)
#

# 本地ollama 流式输出
from langchain_ollama import OllamaLLM

model=OllamaLLM(model="lfm2")

res=model.stream(input="你是谁。你可以做些什么？")
# res=model.invoke(input="你是谁，你能做什么?")     非  流式输出
for chunk in res:                              #流式 输出的  要chunk 遍历
    print(chunk,end="",flush=True)