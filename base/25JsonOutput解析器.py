from langchain_core.output_parsers import JsonOutputParser,StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models.tongyi import ChatTongyi

# 创建所需的解析器
Jsonparser = JsonOutputParser()   #解析器的实例化    可将model的输出AIMessage对象解析成字符串
str_parser = StrOutputParser()   #解析器的实例化    可将model的输出AIMessage对象解析成字符串
# 创建模型
model=ChatTongyi(model="qwen3-max")  #模型的实例化

# 创建提示词模板
first_prompt = PromptTemplate.from_template("一二姓{name1}，布布姓{name2},帮他们未来的小猫起一个名字，要求使用一二和布布的姓,使用谐音，不必是这两个原本的字，"
                                            "要求名字要有创意，独特，并且好听，寓意好,不要使用原本的字，但要有谐音，好听"
                                            "并封装为JSON格式返回给我，要求key是name,value是你起的名字，不要说其他废话")  #提示词模板的实例化

second_prompt = PromptTemplate.from_template("请你用一句话介绍一下{name}的名字的由来")

chain =first_prompt | model | Jsonparser  | second_prompt|model |str_parser#链式调用，prompt的输出作为model的输入，model的输出作为parser的输入

res=chain.invoke(input={"name1":"L","name2":"C"})  #invoke注入字典，得到最终的结果  没有tostring,因为str_parser已经将model的输出解析成字符串了，不需要再调用tostring方法了

# print(res)  #输出结果
# print(type(res))  #输出结果的类型，应该是字符串类型

# 流式输出
for chunk in chain.stream(input={"name1":"刘","name2":"蔡"}):
    print(chunk,end="")  #end=""表示不换行，流式输出会逐步输出结果，而不是一次性输出完整的结果