from langchain_core.prompts import PromptTemplate,FewShotPromptTemplate
from langchain_community.llms.tongyi import Tongyi
example_prompt = PromptTemplate.from_template(
    "输入单词：{input}\n 反义词：{output}"   #示例
)

example_data = [
    {"input": "高兴", "output": "难过"},
    {"input": "快乐", "output": "悲伤"},
    {"input": "成功", "output": "失败"},
    ]


few_shot= FewShotPromptTemplate(
    example_prompt=example_prompt,    #示例数据的模板，None表示不使用示例数据
    examples=example_data,         #示例数据，用来注入动态数据，None表示不使用示例数据
    prefix="请你根据下面的输入，判断输入的文本是的反义词是什么？我将提供一下示例",   #前缀，固定文本,也就是实例之前的提示词
    suffix="基于前面的示例，输入文本：{input_word}\n反义词是什么：",   #后缀，固定文本,也就是实例之后的提示词，{input}是占位符，表示输入文本
    input_variables=["input_word"]   #声明在前缀和后缀中需要注入的变量， 输入变量，表示后缀中的占位符需要注入的变量，这里是input
)

prompt_text= few_shot.invoke({"input_word": "高的"}).to_string()
print(prompt_text)

model=Tongyi(model="qwen-max")
res=model.invoke(input=prompt_text)
print(res)




