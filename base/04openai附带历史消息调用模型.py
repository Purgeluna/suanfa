from openai import OpenAI

client=OpenAI(
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

response=client.chat.completions.create(
    model="qwen-math-turbo",
    messages=[
        {"role":"system","content":"你是AI助理，回答简洁高效"},
        {"role":"user","content":"小明有2条狗"},
        {"role":"assistant","content":"好的"},
        {"role":"user","content":"小红有2只猫"},
        {"role":"assistant","content":"好的"},
        {"role": "user", "content": "总共几个宠物？"},
    ],
    stream=True
)

for chunk in response:
    print(
        chunk.choices[0].delta.content,
        end="",
        flush=True
    )


    # openai 当中在messages的list内，组织历史iaoi提供给模型，短期历史记忆