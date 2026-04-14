
# 对14的基础上进行简化，去掉了示例数据和提问问题的部分，直接给出系统提示和一个测试输入：
from langchain_community.chat_models.tongyi import ChatTongyi

model=ChatTongyi(model='qwen3-max')
messages=[
    # 角色   内容  system / human / ai
    ("system","你是一个边塞诗人。且不说过多的废话，直接回答用户的问题。"),
    ("human","请你背诵一首诗歌"),
    ("ai","床前明月光，疑是地上霜。举头望明月，低头思故乡。"),
    ("human","请你写一首 诗歌,参考上面的格式"),
    ]

res=model.stream(input=messages)
for chunk in res:
    print(chunk.content, end="", flush=True)
    #flush=True  强制刷新输出缓冲区，确保每个chunk都能及时显示在控制台上 end =""  让输出不换行