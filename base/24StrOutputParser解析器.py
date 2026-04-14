from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models.tongyi import ChatTongyi

from langchain_core.output_parsers import StrOutputParser    #解析器的导入

parser = StrOutputParser()   #解析器的实例化    可将model的输出AIMessage对象解析成字符串

model=ChatTongyi(model="qwen3-max")  #模型的实例化\

prompt = PromptTemplate.from_template("我领居姓名为{name},家里有一条小猫，帮他的小猫起一个别具一个的名称，不要说其他废话")  #提示词模板的实例化

Chain =prompt |model| parser|model |parser|model|parser|model  #链式调用，prompt的输出作为model的输入，model的输出作为parser的输入

res =Chain.invoke(input={"name":"张小明"})  #invoke注入字典，得到最终的结果

print(res.content)  #输出结果