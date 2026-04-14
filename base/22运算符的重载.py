class Test(object):
    def __init__(self,name):
        self.name = name

    def __or__(self, other):
        return MySequence(self,other)
    def __str__(self):
        return self.name

class MySequence(object):
    def __init__(self,*args):
        self.sequence = []
        for arg in args:
            self.sequence.append(arg)
    def __or__(self, other):
        self.sequence.append(other)
        return self
    def __run__(self):
        for i in self.sequence:
            print(i)

if __name__ == '__main__':
    a=Test('a')
    print(a.name)
    b=Test('b')
    c=Test('c')
    d=a|b|c            #[a,b,c]
    print(d.sequence)  # [<__main__.Test object at 0x0000021B9C9F3A30>, <__main__.Test object at 0x0000021B9C9F3A60>, <__main__.Test object at 0x0000021B9C9F3A90>]


