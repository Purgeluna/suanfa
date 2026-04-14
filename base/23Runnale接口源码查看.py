from langchain_core.prompts import  PromptTemplate
from langchain_community.llms.tongyi import Tongyi

prompt = PromptTemplate.from_template("请你用中文介绍一下自己")
model=Tongyi(model="qwen3-max")

chain = prompt | model | prompt |model #链式调用，prompt的输出作为model的输入
print(type(chain))
