# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 09:13:17 2019

@Author: Zhi-Jiang Yang, Dong-Sheng Cao
@Institution: CBDD Group, Xiangya School of Pharmaceutical Science, CSU, China
@Homepage: http://www.scbdd.com
@Mail: yzjkid9@gmail.com; oriental-cds@163.com
@Blog: https://blog.moyule.me

♥I love Princess Zelda forever♥
"""


import random


def GenPwd(length):
    """
    """
    while True:
        pwd = [chr(random.randint(33,126)) for _ in range(length)]
        yield ''.join(pwd)
 
       
if '__main__' == __name__:
    length = random.randint(10,100)
    pwd = GenPwd(length)
    print(pwd.__next__())