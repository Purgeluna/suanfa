import numpy as np

'''计算两个向量的点积，2哥向量同维度的数字乘积之和'''
def get_dot(veca,vecb):
    if len(veca) !=len(vecb):
        raise ValueError("向量维度不匹配无法计算")
    dot_sum=0

    for a,b in zip(veca,vecb):
        dot_sum+=a*b
    return dot_sum

'''计算单个向量的模长'''
def get_norm(vecc):
    len_sum=0
    sum=0
    for i in vecc:
        len_sum+=i*i
    sum=np.sqrt(len_sum)
    return sum

A=[0.5,0.5]
B=[0.7,0.7]
C=[0.4,0.7]
D=[-0.3,0.5]
# 计算余弦相似度
def cosine_similarity(a,b):

    dot_sum=get_dot(a,b)    #计算点积
    len_a=get_norm(a)
    len_b=get_norm(b)
    similarity=dot_sum/len_a*len_b
    return similarity

simi=cosine_similarity(A,D)
print(simi)   #输出相似度


