# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 19:50:44 2019

You are not expected to understand my codes!

@author: Kotori_Y
@weibo: Michariel
@mail: yzjkid9@gmial.com

I love Megumi forerver!
"""

import pandas as pd
import numpy as np
from itertools import product
from sklearn.preprocessing import scale
print(__file__+'//..')


############################## INTRODUCTION ##############################

#该函数将返回一个n*n的DataFrame
#1.按F5运行程序
#2.在Ipython控制台中输入函数，并填入参数.e.g.,df = Tanimoto(file=r"C:\Users\0720\Documents\parp_cansmiles_wash_moe2d.txt", col=7),
#df为变量名，可自定义。


def Tanimoto_Single(file, col):
    """Calculate Tanimoto
    
    :param file: the path of your file
    :type file: str
    :param col: the index of first 
    file为数据文件的路径
    col为第col列开始为描述符，从0开始计数。
    """
    
    values = []
#    df = pd.read_table(file)
    df = pd.read_csv(file)
    
    df = df.iloc[:,col:]
    data = np.array(df)
    
    length = len(data)
    
    for pair in product(list(range(length)), repeat=2): #进行排列组合运算
    	up = data[pair[0]]*data[pair[-1]] #获取两个特征向量的数组，进行相关运算，下同
    	down = data[pair[0]]**2 + data[pair[-1]]**2
    	value = up.sum()/(down.sum()-up.sum())#计算公式
    	values.append(value)
    Tani = np.array(values).reshape((length,length))
    
    return Tani 



def Tanimoto_Multi(file_i, col_i, file_v, col_v):
    
    values =[]
    
    df_i = pd.read_table(file_i)
    df_v = pd.read_table(file_v)
#    df_i = pd.read_csv(file_i)
#    df_v = pd.read_csv(file_v)
    
    df_i = df_i.iloc[:,col_i:]
    df_v = df_v.iloc[:,col_v:]
    
    length_i = len(df_i)
    length_v = len(df_v)
    
    data_i = scale(df_i)
    data_v = scale(df_v)
    
    index = []
    for x in range(length_i):
        for y in range(length_v):
            index.append((x,y))
            
    for pair in index:
        up = data_i[pair[0]]*data_v[pair[-1]] #获取两个特征向量的数组，进行相关运算，下同
        down = data_i[pair[0]]**2 + data_v[pair[-1]]**2
        
        try:
            value = up.sum()/(down.sum()-up.sum())#计算公式
            values.append(value)
        except ZeroDivisionError:
            values.append(0)
    
    Tani = np.array(values).reshape((length_i,length_v))
    Tani = pd.DataFrame(Tani)
#        
    return Tani
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    