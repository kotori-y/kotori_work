# -*- coding: utf-8 -*-
"""
Created on Fri May 29 10:40:02 2020

@Author: Zhi-Jiang Yang, Dong-Sheng Cao
@Institution: CBDD Group, Xiangya School of Pharmaceutical Science, CSU, China
@Homepage: http://www.scbdd.com
@Mail: yzjkid9@gmail.com; oriental-cds@163.com
@Blog: https://blog.iamkotori.com

♥I love Princess Zelda forever♥
"""


"""
FutureWarning: 
    arrays to stack must be passed as a "sequence" type such as list or tuple. 
    Support for non-sequence iterables such as generators is deprecated as of 
    NumPy 1.16 and will raise an error in the future.
"""

import numpy as np
import warnings
warnings.filterwarnings('ignore')



def getSimilarity(data, binary=True):
    """
    

    Parameters
    ----------
    data : numpy.ndarray
        fingrtprint or descriptor in 2d-arrry.

    Yields
    ------
    value : numpy.ndarray
        the similarity between a molecule and the lib.

    """
    for arr in data:
        up = arr*data #获取两个特征向量的数组，进行相关运算，下同
        
        if binary:
            down = arr + data
        else:
            down = arr**2 + data**2
            
        value = up.sum(axis=1)/(down.sum(axis=1)-up.sum(axis=1))#计算公式
        yield value
        
        
        
def main(data):
    """
    

    Parameters
    ----------
    data : numpy.ndarray
        DESCRIPTION.

    Returns
    -------
    Similarity matrix.

    """
    simi = getSimilarity(data)
    try:
        simi = np.vstack(simi)
    except:
        simi = np.array(list(simi))
    
    return simi
        
        

if "__main__" == __name__:
    data = np.random.randint(0,2,(1660,1660)) #fake data
    
    simi = main(data)











