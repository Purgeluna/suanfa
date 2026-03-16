from openai import OpenAI
import os


# 本地ollama   或者   云平台
client = OpenAI(
    # base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    base_url="http://localhost:11434/v1",
)

messages = [{"role": "user", "content": "你是谁,一句话介绍自己"}]
completion = client.chat.completions.create(
    # model="deepseek-v3.1",  # 您可以按需更换为其它深度思考模型
    model="lfm2",  #    ollama本地模型的调用
    messages=messages,
    stream=True
)
for chunk in completion:
    print(chunk.choices[0].delta.content,end="",flush=True)
