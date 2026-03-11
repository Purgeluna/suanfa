1235
1235
# 第一周
# 异常处理

# 基础异常处理：
try  :
        print("这是一个异常处理的例子,try")
        a =10/0
        print("result: ",a)
except ZeroDivisionError as e:
        print("这是一个异常处理的例子,except")
        print(e)
finally:
        print("这是一个异常处理的例子,finally")

print("END")


# 多类型的异常处理：
try :
        print("try")
        r=10/int(2)
        print("result: ",r)
except ZeroDivisionError as e:
       print("ZeroDivisionError",e)
except ValueError as e:
       print("ValueError",e)
else:
         print("no error")
finally:
        print("finally")
print("END")

# Python的错误其实也是class，所有的错误类型都继承自BaseException
# try...except可以跨多层调用 ，只要错误没有被捕获，就会一直往上抛出，直到被捕获或者到达顶层程序。
def foo(s):
        return 10 / int(s)
def bar(s):
        return foo(s)*2

def main():
        try:
                bar('0')
        except Exception as e:
                print('Error:', e)
        finally:
                print("finally")
# if __name__ == '__main__':
#         main()

# 调试:
'''
1. print()调试    容易打印很多无用信息，并且在调试完成后需要删除这些print语句
2. 断言 assert   启动Python解释器时可以用-O参数来关闭assert
3. logging
4. pdb    让程序以单步方式运行，可以随时查看运行状态,pdb.set_trace() # 运行到这里会自动暂停
'''
def foo(s):
        n=int(s)
        assert n!=0,'n is zero'  #assert的意思是，表达式n != 0应该是TruE，否则抛出AssertionError，并且错误信息是n is zero
        return 10/n
foo('1')



import logging
s='1';
n=int(s)
logging.basicConfig(level=logging.INFO)
logging.info('n = %d' % n)
print(10/n)


import pdb
s='0'
n=int(s)
# pdb.set_trace()
print(10/n)


