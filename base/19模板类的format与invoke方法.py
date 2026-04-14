from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import FewShotPromptTemplate
"""
PromptTemplate -> StringPromptTemplate >BasePromptTemplate -> RootPromptTemplate -> runable
FewShotPromptTemplate  ->StringPromptTemplate  ->  BasePromptTemplate -> RootPromptTemplate ->runable
ChatPromptTemplate  ->BaseChatPromptTemplate-> BasePromptTemplate -> RootPromptTemplate -> runable
继承关系   顶级父类相同，都是BasePromptTemplate
"""
template=PromptTemplate.from_template(r"我的邻居是{lastname}，她最喜欢{hobby}")
res=template.format(lastname="张小明",hobby="吃")
print(res,type(res))  #string类型，format方法得到的结果是一个字符串，字符串中的占位符被替换成了对应的值

res1=template.invoke(input={"lastname":"张小明","hobby":"吃"})

print(res1,type(res1)) # StringPromptValue，invoke方法得到的结果是一个StringPromptValue对象，字符串中的占位符被替换成了对应的值，并且这个对象还包含了一些额外的信息，比如原始的模板字符串，注入的变量等，可以通过这个对象的方法来获取这些信息
#invoke方法得到的结果是一个字符串，和format方法得到的结果一样，但是invoke方法会对字符串进行一些处理，比如去掉多余的空格，换行等，
# 所以得到的结果可能会有所不同





