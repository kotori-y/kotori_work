# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 22:40:54 2020

@Author: Zhi-Jiang Yang, Dong-Sheng Cao
@Institution: CBDD Group, Xiangya School of Pharmaceutical Science, CSU, China
@Homepage: http://www.scbdd.com
@Mail: yzjkid9@gmail.com; oriental-cds@163.com
@Blog: https://blog.iamkotori.com

♥I love Princess Zelda forever♥
"""

from collections import Counter
from itertools import product
from PIL import Image

import numpy as np


def pos(weight, height, block=10):
    if weight % block != 0:
        weight = ((weight//block) + 1) * block
    
    if height % block != 0:
        height = ((height//block) + 1) * block
        
    for a,b in zip(product(range(0,weight,block), range(0,height,block)), 
                   product(range(block,weight+block,block), range(block,height+block,block)
                           )
                   ):
        
        x1,y1 = a
        x2,y2 = b
        
        yield x1,x2,y1,y2


def ImgToPixel(file, block_size):
    """
    """
    img = Image.open(file)
    h,w = img.size
    img_array = np.array(img)
    arr = img_array.copy()
    
    for x1,x2,y1,y2 in pos(w,h,block_size):
        part = arr[x1:x2, y1:y2]
        part = part.reshape(-1, 3)
        
        c = Counter([tuple(x) for x in part.tolist()])
        arr[x1:x2, y1:y2] = np.array(c.most_common(1)[0][0])
        
    im = Image.fromarray(arr).convert('RGB')
    
    return im