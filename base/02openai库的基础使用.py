# 获取client 对象

from openai import OpenAI
client=OpenAI(
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# 2、调用模型
response=client.chat.completions.create(
    model="deepseek-v3.1",
    messages=[
        {"role":"system","content":"你是一个Python编程专家，并且不说废话简单回答"},
        {"role":"assistant","content":"好的，我是编程专家，并且没有废话，你想知道些什么"},
        {"role":"user","content":"输出1-10的数字，并且使用python 编码"}
    ]
)

print(response.choices[0].message.content)

