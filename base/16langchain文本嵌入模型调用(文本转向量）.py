from langchain_community.embeddings import DashScopeEmbeddings

# 创建模型对象
# model=DashScopeEmbeddings(model="dashscope-embedding-3-small")
model=DashScopeEmbeddings()   #不指定模型，默认使用text-embedding-v1

# 单个文本输入，输出对应的向量表示
print(model.embed_query("我是一二"))

# 多个文本输入，输出对应的向量表示列表
print(model.embed_documents(["我是布布","我是一二三四五六七八九十"]))   #输入一个列表，输出一个列表，每个元素是对应输入文本的向量表示


# ollama  本地服务，访问本地嵌入模型
''' 
from langchain_ollama import OllamaEmbeddings   

model=OllamaEmbeddings(model="qwen3-embedding:4b")   #指定模型名称
print(model.embed_query("我是一二"))
print(model.embed_documents(["我是布布","我是一二三四五六七八九十"]))   #输入一个列表，输出一个列表，每个元素是对应输入文本的向量表示

'''
