# 组件串联，将上一个组件的输出作为下一个组件的输入，形成一个链式结构。  前提是Runable组件的输入输出类型必须匹配，才能正确连接。
# chain 的基础使用

from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi

# 构建提示词木模板
chat_prompt_template = ChatPromptTemplate.from_messages(
[
    ("system","你是一个边塞诗人，可以作诗"),
    MessagesPlaceholder("history"),    #占位符，表示历史对话记录，可以在运行时注入具体的历史对话内容
    ("human","请你作一首七言律诗OK吗"),
]
)

history=[
    ("human","请你作一首七言律诗"),
    ("ai","床前明月光，疑是地上霜。举头望明月，低头思故乡。"),
    ("human","请你再作一首七言律诗"),
    ("ai","白日依山尽，黄河入海流。欲穷千里目，更上一层楼。")
]

chat_prompt_template.invoke(input={"history":history}).to_string()  #invoke注入字典

'''常规方法'''
# model = ChatTongyi(model="qwen3-max")
# res=model.invoke(chat_prompt_template)

'''链式调用'''
model = ChatTongyi(model="qwen3-max")
Chain = chat_prompt_template | model  #链式调用，chat_prompt_template的输出作为model的输入

res=Chain.invoke(input={"history":history})  #invoke注入字典
print(res.content)

# stream 流式输出
for res in Chain.stream(input={"history":history}):
    print(res.content,end="")  #end=""表示不换行，流式输出会逐步输出结果，而不是一次性输出完整的结果


# invoke 一次性输出完整结果，stream 流式输出逐步输出结果，适合处理大文本或者需要实时反馈的场景