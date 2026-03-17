import json

from openai import  OpenAI

client=OpenAI(
    # base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    base_url="http://127.0.0.1:8045/v1",
    # api_key="sk-b044"
)

schema=["期数","中奖号码","一等奖"]
# 原始开奖数据
raw_data = [
    "2025年第100期，开好红球22 21 06 01 03 11 篮球 07，一等奖中奖为2注。",
    "2025101期，有3注1等奖，10注2等奖，开号篮球11，中奖红球3、5、7、11、12、16。"
]
# 期望抽取结果
extracted_results = [
    {"期数": "2025100", "中奖号码": [1, 3, 6, 11, 21, 22, 7], "一等奖": "2注"},
    {"期数": "2025101", "中奖号码": [3, 5, 7, 11, 12, 16, 11], "一等奖": "3注"}
]

questions=[
    "2025年第102期，开出红球09 15 18 23 27 30 篮球 05，一等奖共中出8注。",
    "2025103期，一等奖中奖注数为5注，二等奖15注，篮球号码08，红球中奖号为1、4、8、19、25、32。"
]
# 构建messages
messages=[
    {
        "role": "system","content": f"你帮我完成信息抽取，我给你句子，你抽取{schema}信息，按JSON字符串输出，如果某些信息不存在，用'原文未提及'表示，请参考如下示例："
    }]

for item1,item2 in zip(raw_data,extracted_results):
    messages.append({"role":"user","content":f"{item1}"})
    # messages.append({"role":"answers","content":json.dump(f"{item2}",ensure_ascii=False)})
    messages.append({"role":"assistant","content":f"{item2}"})

# for i in messages:
#     print(i)

for qes in questions:
    response=client.chat.completions.create(
        model="gemini-3-flash",
        messages=messages+[{"role":"user","content":f"请你按照上述例子，回答这个句子的内容是什么？{qes}"}]
    )
    # 回答问题
    print(response.choices[0].message.content)

