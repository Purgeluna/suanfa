from langchain_core.prompts import PromptTemplate
from langchain_community.llms import Tongyi
prompt_template = PromptTemplate.from_template(
    "我的邻居姓{lastname}，请问他的名字是什么？他刚生了{gender}孩子，帮他女儿起一个名字，要求唯美，好听，寓意美好。"
)
model=Tongyi(model="qwen-max")
# 方式1  ：  调用format方法，注入信息即可
'''prompt_text = prompt_template.format(lastname="蔡",gender="女")
res=model.invoke(input=prompt_text)   #invoke方法是非流式输出(一次得到结果)  stream方法是流式输出（分块得到结果）
print(res)                                  # 这里用invoke方法是因为我们只需要一次得到结果，不需要分块输出

res2=model.stream(input=prompt_text)   #invoke方法是非流式输出(一次得到结果)  stream方法是流式输出（分块得到结果）
for chunk in res2:                              #流式 输出的  要chunk 遍历
    print(chunk,end="",flush=True)
'''

# 方式2 ：    chain 链式
# 构建执行链条的写作方式，但是字符串的注入方式和上面是一样的，都是通过format方法注入信息  ，不能直接在链条中注入信息
chian = prompt_template | model

res = chian.invoke(input={"lastname":"蔡","gender":"女"})
print(res)


