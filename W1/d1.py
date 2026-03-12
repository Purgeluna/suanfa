
import numpy as np

a=np.array([1,3,2,4,6])
b=np.random.randn(4,5)  #0-1之间的随机数，4行5列
print(a)
print(b)
c=np.ones((1,2),dtype=np.int32)
print(c)
d=np.zeros((3,4),dtype=np.float64)
print(d)

e=np.linspace(1,10,5)  #从1开始到10结束，等差数列，个数为5
print(e)
f=np.arange(1,10,2)  #从1开始到10结束，步长为2
print(f)

print("-------------------------------------")
# 广播机制
a1=np.array([1,2,3])
b1=np.array([[10,20,30],[1,2,3]])
c1=a1+b1
print(c1)

f1=np.arange(5)
f2=f1.reshape(5,1) #从0开始到5结束，步长为1，变成5行1列
f3=f2.flatten()

print("f1:",f1,"\nf2:",f2,"\nf3:",f3)

print("-------------------------------------")

arr = np.array([1,2,3])  # 形状 (3,)  是一个一维数组，包含3个元素形状 (shape): (3,)。这个括号里的逗号表示它只有一个轴（Axis 0），这个轴上有 3 个元素。
print(arr.shape)  # 输出 (3,)
print(arr)  #1,2,3
arr2=arr[np.newaxis, :]       # 扩展为 (1,3)  (2维数组）
arr3=arr[:, np.newaxis]

print(arr2.shape)  # 输出 (1,3)
print(arr2)  # [[1 2 3]]
print(arr3.shape)  # 输出 (3,1)
print(arr3)  # [[1] [2] [3]]

a = np.array([[1,2], [3,4]])
b = np.array([[5,6], [7,8]])
a11=np.concatenate([a, b], axis=0)  # 垂直拼接：(4,2)  增加行
a22=np.concatenate([a, b], axis=1)  # 水平拼接：(2,4)  增加列  concatenate  concatenate oncatenate
print(a11)
print(a22)
a33=np.split(a, 2, axis=0)          # 沿行拆分为 2 份
a44=np.split(a, 2, axis=1)          # 沿列拆分为 2 份
print(a33)
print(a44)


print("-------------------------------------")
# 装饰器  代码运行期间   动态增加功能的方式，称之为“装饰器”（Decorator）
def now():
    print('2015-3-25')
k=now
print(k)  #<function now at 0x7f8c8c8c8c8c> 地址
m=k.__name__
print(m)  #now

def log(func):
    def  wrapper(*args,**kw):
        print('call %s' % func.__name__)
        return func(*args,**kw)
    return wrapper


@log  #把@log放到now()函数的定义处，相当于执行了语句
def now():
    print('2015-3-25')
now()

#上下文管理器  with语句

#传统
# f = open('test.txt', 'r')
# try :
#     data=f.load(f)
# finally:
#     f.close()

#with语句  # 退出 with 块后，文件自动关闭，无需手动操作
# with open('test.txt', 'r') as f:
#     data=f.load(f)
# # 类似做法：
# 自定义 GPU 资源管理器

'''
常见错误语法：
语法错误（SyntaxError）:代码不符合 Python 语法规则，比如少写冒号、括号不匹配，程序运行前就会被检测到。  
运行时异常（RuntimeError）:代码语法正确，但运行时出现问题，比如除以零、访问不存在的文件

异常类型	触发场景
ValueError	传入无效参数，比如字符串转数字失败
TypeError	操作类型不匹配，比如字符串和数字相加
IndexError	列表 / 元组索引越界
KeyError	字典访问不存在的键
FileNotFoundError	打开不存在的文件
ZeroDivisionError	除数为 0
'''

L = [
    ['Apple', 'Google', 'Microsoft'],
    ['Java', 'Python', 'Ruby', 'PHP'],
    ['Adam', 'Bart', 'Bob']
]

# 打印Apple:
print(L[0][0])
# 打印Python:
print(L[1][1])
# 打印Bob:
print(L[2][2])

birth =input('birth: ')
birth = int(birth)
if birth < 2000:
    print('00前')
else:    print('00后')

# 模式匹配：
age=15

match age:
    case x  if x <10:
        print('儿童')
    case 10:
        print('少年')
    case 50 :
        print('成年人')
    case _:
        print('not sure')