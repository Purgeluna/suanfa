from collections import deque

import numpy as np


# 二叉树 ，每个节点最多两个子节点，数据结构：二叉树与遍历 实现前中后序遍历

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val     # 节点值
        self.left = left   # 左子节点
        self.right = right # 右子节点

 # 前 / 中 / 后序遍历的核心规则前 / 中 / 后序遍历的核心规则
# 跟左右   左跟右  左右跟

# 1、 二叉树的构建
#       1
#      /  \
#     3   2
#        /
#       4
root=TreeNode(1)
root.right=TreeNode(2)
root.left=TreeNode(3)
root.right.left=TreeNode(4)

# 2、递归的核心是「分解子问题」：遍历当前节点的左子树 → 遍历右子树（根节点访问时机不同）
''' 前序遍历（递归）'''
def preorder_recur(root):
    res=[]
    def  traverse (node):
        if not node:
            return
        res.append(node.val)
        traverse(node.left)   # 2. 遍历左子树
        traverse(node.right)  # 3. 遍历右子树
    traverse(root)
    return res

'''中序遍历递归'''
def inorder_recur(root):
    res=[]
    def traverse(node):
        if not node:
            return
        traverse(node.left)  # 1. 遍历左子树
        res.append(node.val)  # 2. 访问根节点
        traverse(node.right)  # 3. 遍历右子树
    traverse(root)
    return res

'''后序遍历'''
def postorder_recur(root):
    res=[]
    def traverse(node):
        if not node:
            return
        traverse(node.left)  # 1. 遍历左子树
        traverse(node.right)  # 2. 遍历左子树
        res.append(node.val)  # 3. 访问根节点
    traverse(root)
    return res


print("前序递归：", preorder_recur(root))  #  [1, 3, 2, 4]
print("中序递归：", inorder_recur(root))   # [3, 1, 4, 2]
print("后序递归：", postorder_recur(root)) # [3, 1, 4, 2]

'''4、递归方法（栈）保持待访问的节点'''

'''1、前序迭代
栈：后进先出，那么对于前序遍历，先压右子树 再压左子树
'''
def preorder_iter(root):
    res=[]
    if not root:
        return
    stack=[root]  #初始化栈为根节点
    while stack:
        node=stack.pop()
        res.append(node.val)     #栈顶元素出栈，访问 根节点
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    return res

print("前序迭代：", preorder_iter(root))  # [1, 3, 2, 4]

'''2、中序迭代  左根右'''
def inorder_iter(root):
    res = []
    stack = []
    cur = root  # 游标节点，初始指向根
    while cur or stack:
        # 先遍历到左子树最深处，依次压栈
        while cur:
            stack.append(cur)
            cur = cur.left
        # 弹出栈顶（左子树最深处），访问
        cur = stack.pop()
        res.append(cur.val)
        # 处理右子树
        cur = cur.right
    return res

print("中序迭代：", inorder_iter(root))

'''3、后序迭代   参考前序   将前序 跟左右  改为   跟右左   然后 反转得到   左右跟
         注意压栈顺序  相反'''
def postorder_iter(root):
    res = []
    if not root:
        return res
    stack = [root]
    while stack:
        node = stack.pop()
        res.append(node.val)
        # 先压左、再压右 → 弹出顺序是右、左 → 结果是根右左
        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)
    return res[::-1]  # 反转 → 左右根

print("后序迭代：", postorder_iter(root)) # [3, 2, 1]

'''4、层序遍历'''
def levelorder(root):
    res=[]
    if not root:
        return
    queue=deque([root])

    while queue:
        node = queue.popleft()
        res.append(node.val)
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    return res

print("层序遍历：", levelorder(root))  # [1, 3, 2,4]
# 小结：
#
# 迭代前序遍历：忘记「先压右、再压左」（栈的后进先出特性）；
# 后序遍历：「前序调整 + 反转」的技巧
# 后序遍历的应用：删除二叉树（先删左右子树、再删根）、计算子树和；
#
# 中序遍历的特性：二叉搜索树（BST）的中序遍历是「升序序列」；
# 边界条件：未处理「空节点」（如 root=None、子节点为空的情况）。
# 边界条件：未处理「空节点」（如 root=None、子节点为空的情况）

# 前 / 中 / 后序遍历的核心是「根节点的访问时机」，递归写法是基础，迭代写法需掌握栈的使用；
# 递归遍历的终止条件永远是「节点为空」，迭代遍历需利用栈的「后进先出」特性控制顺序；
# 中序遍历是二叉搜索树的核心遍历方式，后序遍历可通过「前序调整 + 反转」快速实现；
# 所有遍历的时间复杂度都是 O (n)，空间复杂度 O (n)（递归栈 / 迭代栈的开销）。



# matplotlib   图形绘制
import matplotlib.pyplot as plt

epochs = np.arange(1, 21)  # 训练轮数：1-20
train_loss = np.array([0.8, 0.7, 0.6, 0.5, 0.45, 0.4, 0.38, 0.35, 0.32, 0.3,
                       0.28, 0.27, 0.26, 0.25, 0.24, 0.23, 0.22, 0.21, 0.2, 0.19])
val_loss = np.array([0.85, 0.75, 0.65, 0.58, 0.55, 0.52, 0.5, 0.48, 0.47, 0.46,
                     0.45, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51, 0.52])  # 验证损失上升（过拟合）
train_acc = np.array([0.6, 0.65, 0.7, 0.75, 0.78, 0.8, 0.82, 0.83, 0.84, 0.85,
                      0.86, 0.87, 0.88, 0.89, 0.9, 0.91, 0.92, 0.93, 0.94, 0.95])
val_acc = np.array([0.58, 0.62, 0.68, 0.72, 0.74, 0.76, 0.77, 0.78, 0.785, 0.79,
                    0.79, 0.785, 0.78, 0.775, 0.77, 0.765, 0.76, 0.755, 0.75, 0.745])

plt.figure(figsize=(10,6))
plt.plot(epochs,train_loss,label='Train loss',color='blue',linestyle='-',linewidth=2,marker='o')
plt.plot(epochs,val_loss,label='valid loss',color='red',linestyle='-',linewidth=2,marker='s')

plt.title("train and valid loss curve",fontsize=14,fontweight='bold')   #标题

plt.xlabel('Epochs', fontsize=12)  # x轴标签
plt.ylabel('Loss', fontsize=12)    # y轴标签
plt.legend(loc='upper right', fontsize=10)  # 图例（显示label）
plt.grid(True, alpha=0.3)  # 网格线（alpha：透明度）
plt.xticks(epochs[::2])    # x轴刻度：每2轮显示一次
plt.tight_layout()         # 自动调整布局（避免标签被截断）
# 4. 保存/显示图片
# plt.savefig('loss_curve.png', dpi=300, bbox_inches='tight')  # 保存（dpi=300：高清）
plt.show()  # 显示图片







