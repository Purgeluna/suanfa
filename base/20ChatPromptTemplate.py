from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi

chat_prompt_template = ChatPromptTemplate.from_messages(
[
    ("system","你是一个边塞诗人，可以作诗"),
    MessagesPlaceholder("history"),
    ("human","请你作一首七言律诗OK吗"),
]
)

history=[
    ("human","请你作一首七言律诗"),
    ("ai","床前明月光，疑是地上霜。举头望明月，低头思故乡。"),
    ("human","请你再作一首七言律诗"),
    ("ai","白日依山尽，黄河入海流。欲穷千里目，更上一层楼。")
]

prompt_text=chat_prompt_template.invoke(input={"history":history}).to_string()  #invoke注入字典

# print(prompt_text)
# 结果如下：
# 你是一个边塞诗人，可以作诗
# human: 请你作一首七言律诗
# ai: 床前明月光，疑是地上霜。举头望明月，低头思故乡。
# human: 请你再作一首七言律诗
# ai: 白日依山尽，黄河入海流。欲穷千里目，更上一层楼。
# human: 请你作一首七言律诗OK吗

model = ChatTongyi(model="qwen3-max")
res=model.invoke(prompt_text)

print(res.content,type(res))

# 结果如下：
# 床前明月光，疑是地上霜。举头望明月，低头思故乡。
# 白日依山尽，黄河入海流

