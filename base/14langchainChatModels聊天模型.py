'''
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages import HumanMessage,SystemMessage,AIMessage

# SystemMessage   设定系统角色
# HumanMessage    设定用户角色

# chat_models  聊天的模型  需要指定模型名称
# 这里的模型名称是qwen3-max  也可以是qwen2-max  qwen3-mini  qwen2-mini

chat = ChatTongyi(model='qwen3-max')
messages = [
    SystemMessage(content="你是一个边塞诗人。且不说过多的废话，直接回答用户的问题。"),
    HumanMessage(content="请你背诵一首诗歌"),
    AIMessage(content="床前明月光，疑是地上霜。举头望明月，低头思故乡。"),
    HumanMessage(content="请你写一首诗歌,参考上面的格式"),
]
res=chat.stream(input=messages)
# for chunk in chat.stream(input=messages):
#     print(chunk.content, end="", flush=True)
for chunk in res:
    print(chunk.content, end="", flush=True)

'''


# 本地ollama 流式输出
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage,SystemMessage,AIMessage
model=ChatOllama(model="lfm2")
messages=[
    SystemMessage(content="你是一个边塞诗人。且不说过多的废话，直接回答用户的问题。"),
    HumanMessage(content="请你背诵一 首诗歌"),
    AIMessage(content="床前明月光，疑是地上霜。举头望明月，低头思故乡。"),
    HumanMessage(content="请你写一首诗歌,参考上面的格式"),
]
res=model.stream(input=messages)
for chunk in res:
    print(chunk.content, end="", flush=True)





