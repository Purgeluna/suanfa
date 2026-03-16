#面向过程的程序设计把计算机程序视为一系列的命令集合，即一组函数的顺序执行
##面向对象的程序设计把计算机程序视为一组对象的集合，这些对象包含数据和操作数据的方法

#类  在Class内部，可以有属性和方法，而外部代码可以通过直接调用实例变量的方法来操作数据，这样，就隐藏了内部的复杂逻辑。
class Student(object):
    def __init__(self,name,score):
        self.name = name
        self.score = score
    def print_score(self):
        print('%s:%s' % (self.name,self.score))

    def get_grade(self):
        if self.score >= 90:
            return 'A'
        elif self.score >= 60:
            return 'B'
        else:
            return 'C'

a1=Student('小明',90)
a1.print_score() #小明:90
print(a1.get_grade()) #A

# 如果要让内部属性不被外部访问，可以把属性的名称前加上两个下划线__，
# 在Python中，实例的变量名如果以__开头，就变成了一个私有变量（private），只有内部可以访问，外部不能访问，
'''内部可以访问，外部不能访问'''

class Teacher(object):
    def __init__(self,name,score):
        self.__name = name
        self.__score = score
    def print_score(self):
        print('%s:%s' % (self.__name,self.__score))

a2=Teacher('小红',80)
a2.print_score() #小红:80

'''如果外部代码要获取name和score怎么办如果外部代码要获取name和score怎么办'''

class Teacher(object):
    def __init__(self,name,score):
        self.__name = name
        self.__score = score
    def print_score(self):
        print('%s:%s' % (self.__name,self.__score))
    def get_name(self):
        return self.__name
    def get_score(self):
        return self.__score

'''如果又要允许外部代码修改score怎么办'''

class Teacher(object):
    def __init__(self,name,score):
        self.__name = name
        self.__score = score
    def print_score(self):
        print('%s:%s' % (self.__name,self.__score))
    def get_name(self):
        return self.__name
    def get_score(self):
        return self.__score
    def set_score(self,score):
        if 0 <= score <= 100:
            self.__score = score
        else:
            raise ValueError('bad score')

'''变量名类似__xxx__的，也就是以双下划线开头，并且以双下划线结尾的，是特殊变量，
特殊变量是可以直接访问的，不是private变量，
所以，不能用__name__、__score__这样的变量名'''

# 练习：
class Student(object):
    def __init__(self, name, gender):
        self.name = name
        self.__gender = gender

    def get_gender(self):
        return self.__gender

    def set_gender(self, gender):
        if gender == 'male' or gender =='female':
            self.__gender=gender
            print('测试成功!')
        else:
            raise ValueError('测试失败!')


bart = Student('Bart', 'male')
if bart.get_gender() != 'male':
    print('测试失败!')
else:
    bart.set_gender('female')
    if bart.get_gender() != 'female':
        print('测试失败!')
    else:
        print('测试成功!')

#继承和多态 子类和父类都存在相同的run()方法时，我们说，子类的run()覆盖了父类的run()，在代码运行的时候，
# 总是会调用子类的run()。这样，我们就获得了继承的另一个好处：多态
'''判断一个变量是否是某个类型可以用isinstance()判断：'''
class Animal(object):

    def run(self):
        print('Animal is running...')


class Dog(Animal):
    def run(self):
        print('Dog is running...')
class Cat(Animal):
    def run(self):
        print('Cat is running...')

cat=Cat()
dog=Dog()
cat.run() #Cat is running...
dog.run() #Dog is running...
isinstance(cat,Animal) #True
isinstance(cat,Cat) #True
isinstance(cat,Dog) #False
isinstance(dog,Animal) #True


def run_twice(animal):
    animal.run()
    animal.run()
run_twice(Animal()) #Animal is running... Animal is running...
run_twice(Dog()) #Dog is running... Dog is running...
run_twice(Cat()) #Cat is running... Cat is running...

class Tortoise(Animal):
    def run(self):
        print('Tortoise is running slowly...')

'''多态真正的威力：调用方只管调用，不管细节，而当我们新增一种Animal的子类时，
只要确保run()方法编写正确，不用管原来的代码是如何调用的。这就是著名的“开闭”原则：'''

'''获取对象信息  type()函数返回的是什么类型呢？它返回对应的Class类型'''
print(type(123)) #<class 'int'>
print(type('str')) #<class 'str'>
print(type(None)) #<class 'NoneType'>

'''isinstance()判断的是一个对象是否是该类型本身，或者位于该类型的父继承链上。
总是优先使用isinstance()判断类型，可以将指定类型及其子类“一网打尽”。'''
# 还可以判断一个变量是否是某些类型中的一种，比如下面的代码就可以判断是否是list或者tuple
# >>> isinstance([1, 2, 3], (list, tuple))
# True
# >>> isinstance((1, 2, 3), (list, tuple))
# True

# 案例
class Student(object):
    count = 0
    def __init__(self, name):
        self.name = name
        Student.count += 1

if Student.count != 0:
    print('测试失败!')
else:
    bart = Student('Bart')
    if Student.count != 1:
        print('测试失败!')
    else:
        lisa = Student('Bart')
        if Student.count != 2:
            print('测试失败!')
        else:
            print('Students:', Student.count)
            print('测试通过!')

# 封装的核心是：“隐藏内部，暴露接口”。
# 对内部：可以自由修改实现逻辑，只要接口不变，不影响外部；
# 对外部：只需关注如何调用接口，不用关心内部如何工作，降低使用成本，同时保证数据安全。

# 基本数据结构
'''链表 node'''
class Node(object):
    def __init__(self, value, next=None):
        self.value = value # 数据域
        self.next = next  # 指针域
# 节点关系构建：

node1=Node(1)
node2=Node(2)
node3=Node(3)
node1.next=node2
node2.next=node3

# 头节点（链表的入口，关键！）
'''需要指定一个头节点，才能访问链表的所有节点'''
head = node1


print(node1.value) #1
print(node1.next.value) #2
print(node1.next.next.value) #3
print(node3.next) #None
# 链表核心操作（增删改查）  所有操作的核心：通过头节点遍历找到目标位置，再修改指针指向
'''1、查：遍历链表'''
def traveerse(head):
    cur=head
    while cur is not None:
        print(cur.value)
        cur=cur.next
traveerse(head) #1 2 3      #遍历全部

'''2、查：查找特定值'''
def find(head,value):
    cuur=head
    while cuur is not None:
        if cuur.value==value:
            return cuur
        cuur=cuur.next
print(find(head,2).value) #2  #查找特定值

'''3、增：在链表头部插入新节点'''

def insert_head(head,value):
    newnode=Node(value) #创建新节点
    newnode.next=head #新节点指向原头节点
    return newnode #返回新节点作为新的头节点

head=insert_head(head,0) #在链表头部插入新节点0
traveerse(head) #0 1 2 3

'''4、增：在链表尾部插入新节点'''
def append_tail(head,value):
    newhead=Node(value) #创建新节点
    if not head: #如果链表为空，新节点作为头节点
        return newhead
    cur=head
    while cur.next is not None: #遍历找到链表尾部
        cur=cur.next
    cur.next=newhead #尾节点指向新节点
    return head #返回头节点
head=append_tail(head,4) #在链表尾部插入新节点4
traveerse(head) #0 1 2 3 4

# 中间插入（指定索引后新增）
'''寻找到插入位置的前一个节点，修改指针指向'''
def insert_middle(head,index,value):
    newnode=Node(value) #创建新节点

    if index==0: #如果索引为0，在链表头部插入新节点
        newnode.next=head
        return newnode
    cur=head
    count=0
    while cur and count < index - 1:
        cur = cur.next
        count += 1
    if not cur:  # 索引越界
        raise ValueError("索引超出链表长度")
    newnode.next = cur.next  # 新节点指向当前节点的下一个节点
    cur.next = newnode  # 当前节点指向新节点
    return head  # 返回头节点

head=insert_middle(head,2,99) #在索引2位置插入新节点99
traveerse(head) #0 1 99 2 3 4

'''5、删：删除指定值的节点  遍历找到要删除节点的前一个节点'''
def delete(head,value):
    if not head: #如果链表为空，直接返回None
        return None
    if head and head.value==value:
        return head.next #如果头节点是要删除的节点，返回下一个节点作为新的头节点
    prev, cur = None, head
    while cur:
        if cur.value==value:
            prev.next=cur.next #前一个节点指向当前节点的下一个节点，跳过当前节点
            break
        # prev, cur = cur, cur.next
        prev = cur
        cur = cur.next
    return head #返回头节点
head=delete(head,99) #删除值为99的节点
traveerse(head) #0 1 2 3 4

'''删除指定索引的节点,遍历找到要删除节点的前一个节点'''
def delete_by_index(head,index):
    if head is None: #如果链表为空，直接返回None
        return None
    if index==0 and head: #如果索引为0，返回下一个节点作为新的头节点
        return head.next
    prev, cur = None, head
    count =0
    while  cur and count < index - 1: #遍历找到要删除节点的前一个节点
        cur = cur.next
        count += 1
    if not cur or not cur.next: #如果索引越界，直接返回原链表
        return head
    cur.next=cur.next.next #前一个节点指向当前节点的下一个节点，跳过当前节点

    return head #返回头节点
delete_by_index(head,2) #删除索引为2的节点

'''改：修改指定索引的节点值 遍历找到要修改节点'''
def update(head,index,value):
    if head is None: #如果链表为空，直接返回None
        return None
    cur=head
    count=0
    while cur :
        if count==index: #找到要修改节点
            cur.value=value #修改节点值
            break
        cur=cur.next
        count+=1
    raise ValueError("索引超出链表长度") #如果索引越界，抛出异常
update(head,2,88) #修改索引为2的节点值为88
traveerse(head) #0 1 88 3 4























