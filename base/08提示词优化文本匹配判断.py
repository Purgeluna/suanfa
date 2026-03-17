import json

from  openai import  OpenAI

client=OpenAI(
    base_url="http://127.0.0.1:8045/v1")

examples_data = {
    "是": [
        ("公司ABC发布了季度财报，显示盈利增长。", "财报披露，公司ABC利润上升。"),
        ("公司ITCAST发布了年度财报，显示盈利大幅度增长。", "财报披露，公司ITCAST更赚钱了。")
    ],
    "不是": [
        ("黄金价格下跌，投资者抛售。", "外汇市场交易额创下新高。"),
        ("央行降息，刺激经济增长。", "新能源技术的创新。")
    ]
}

questions = [
    ("利率上升，影响房地产市场。", "高利率对房地产有一定的冲击。"),
    ("油价大幅度下跌，能源公司面临挑战。", "未来智能城市的建设趋势越加明显。"),
    ("股票市场今日大涨，投资者乐观。", "持续上涨的市场让投资者感到满意。")
]

# 设置系统
messages=[{"role":"system","content":f"请你帮我完成文本匹配，我给你一些案例，请你根据他们，回答接下的句子是否匹配，只要回答是或者不是，具体参考以下案例："}]

# 构建messages

for key,value in examples_data.items():
    for i in value:
        messages.append({"role":"user","content":f"句子1：{i[0]},句子2：{i[1]}"})
        messages.append({"role":"assistant","content":key})

# for i in messages:
#     print(i)

for qes in questions:
    response=client.chat.completions.create(
        model="gemini-3-flash",
        messages=messages+[{"role":"user","content":f"请按照上面的例子回答这些句子的匹配{qes}"}]
    )
    print(response.choices[0].message.content)
