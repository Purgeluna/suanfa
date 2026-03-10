import numpy as np
import pandas as pd
from pandas import Series, DataFrame

'''
# Series  类似字典 包含索引与数据，Series 对象本身及其索引都有一个 name 属性
# 一维 的 nupy 数组 以及一个与之相关的数据标签（即索引）组成的对象
ser1=pd.Series([1, 2, 3, 4, 5], index=['a', 'b', 'c', 'd', 'e'], name='number')
print("Series:",ser1)

# DataFrame  二维 的 nupy 数组 以及一个与之相关的数据标签（即索引）组成的对象
# DataFrame 是一个表格型的数据结构，它包含一组有序的列，每列可以是不同的值类型（数值、字符串、布尔值等）。
# DataFrame既有行索引（index）又有列索引（columns），可以看作是一个由 Series 组成的字典。
df={'name':['Tom', 'Jack', 'Steve', 'Ricky'], 'age':[28, 34, 29, 42],
    'city':['Beijing', 'Shanghai', 'Guangzhou', 'Shenzhen']}
df1=pd.DataFrame(df)
print("DataFrame: df1",df1)

df2=pd.DataFrame(df,columns=['city','name','age'])

df3=pd.DataFrame(df,columns=['city','height','age'])  # height 列不存在，结果为NaN
print("DataFrame: df2",df2)
print("DataFrame: df3",df3)

df4=pd.DataFrame(df,columns=['city','age'],index=['Tom', 'Jack', 'Steve', 'Ricky'])
# index指定行索引 ,消除默认的行索引，使用指定的行索引
print("DataFrame: df4",df4)

print("DataFrame: df4['age']",df4['age'])  #访问列，结果是一个 Series 对象
print("DataFrame: df4['name']",df4['city'])  #访问列，结果是一个 Series 对象

df4.columns.name='name'
df4.index.name='index'
print("DataFrame: df4",df4)

# Pandas  基本数据操作
s1=pd.Series(np.random.rand(20))
d1=pd.DataFrame(np.random.rand(20).reshape(5,4),columns=['A','B','C','D'])

print(s1.head(3))  #默认前5行，head()方法返回前n行数据
print(s1.tail(3))  #默认后5行，tail()方法返回后

# 转置 T属性返回DataFrame的转置，即行列互换
print(d1.T)

s2=pd.Series(np.random.rand(5),index=['a','b','c','d','e'])
print(s2)
s3=s2.reindex(['a','c','b','d','e','f'])  #reindex()方法改变Series的索引，增加了一个索引f，结果为NaN
print(s3)

print(s3.isnull())  #isnull()方法返回一个布尔值Series，表示每个元素是否为NaN
print(s3.notnull())  #notnull()方法返回一个布尔值Series，

s4=pd.Series(np.random.randint(0,10,5),index=['a','b','c','d','e'])
print(s4)
s5=s4.reindex(['a','c','b','d','e','f'],fill_value=0)
#reindex()方法改变Series的索引，增加了一个索引f，结果为0
print(s5)
# s6=s4.reindex(np.arange(15),method='ffill')   #必须是统一类型的索引，不能是字符串和整数混合，method='ffill'表示前向填充，即用前一个值填充缺失值
# print(s6)

# 类似地 Dataframe 也有 reindex()方法，可以改变行索引和列索引
df5=pd.DataFrame(np.random.rand(5,4),columns=['A','B','C','D'],index=['a','b','c','d','e'])
print(df5)
df6=df5.reindex(index=['a','c','f','d','e'])
print(df6)
del(df6['B'])  #删除列B
print(df6)

df6.index.name='index1'
df6.columns.name='columns1'
print(df6)

df6.drop('C',axis=1,inplace=True)  #drop()方法删除列C，axis=1表示删除列，inplace=True表示在原DataFrame上修改
print(df6)

df6.drop('d',axis=0,inplace=True)  #drop()方法删除行d，axis=0表示删除行，inplace=True表示在原DataFrame上修改
print(df6)

'''

# pandas实例  解析数据清洗
# 实例1   电商订单数据清洗与分析

df = pd.DataFrame({
    "订单号": ["D001", "D002", "D003", "D004", "D001", "D005", None, "D007"],
    "商品类别": ["电子产品", "服装", "电子产品", "食品", "电子产品", "服装", "食品", "服装"],
    "地区": ["华东", "华北", "华东", "华南", "华东", "华北", "华南", "华北"],
    "单价": [3000, 299, 4999, 25, 3000, 199, 35, None],
    "数量": [1, 2, 0, 10, -1, -3, 5, 2],
    "折扣": [0.9, 1, 0.85, 1, 0.9, 0.8, 1, 0.9]
})
print("原始数据：\n", df)

print("数据信息")
print(df.info())

# 缺失值统计
print(":缺失值统计：\n", df.isnull().sum())

# 数据清晰
# 1、删除订单号重复
df_cleaned=df.drop_duplicates(subset=['订单号'])
print("删除订单号重复：\n", df_cleaned)

# 2、删除订单号为空
df_cleaned=df_cleaned.dropna(subset='订单号')
print("删除订单号为空：\n", df_cleaned)

# 3、填充单价的缺失值 使用同类别的平均单价进行填充
df_cleaned=df_cleaned.groupby("商品类别").apply(lambda x: x.fillna(x['单价'].mean()))
print("填充单价的缺失值：\n", df_cleaned)

# 异常值过滤
df_cleaned=df_cleaned[(df_cleaned['单价'] > 0) & (df_cleaned['数量'] > 0)]
print("异常值过滤：\n", df_cleaned)

# 计算金额
df_cleaned['金额']=df_cleaned['单价']*df_cleaned['数量']*df_cleaned['折扣']
print("计算金额：\n", df_cleaned)

# 分地区统计
result1=df_cleaned.groupby('地区')['金额'].sum().round(2)
print("分地区统计：\n", result1)

result2=df_cleaned.groupby(df_cleaned['商品类别'])['金额'].sum().round(2)
print("商品类别：\n", result2)

df_cleaned.to_excel("cleaned_orders.xlsx", index=False)  #保存清洗后的数据到Excel文件，index=False表示不保存行索引
