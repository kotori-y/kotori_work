# -*- coding: utf-8 -*-

#Created on Thu Dec 12 14:47:59 2019
#
#@Author: Zhi-Jiang Yang, Dong-Sheng Cao
#@Institution: CBDD Group, Xiangya School of Pharmaceutical Science, CSU, China
#@Homepage: http://www.scbdd.com
#@Mail: yzjkid9@gmail.com; oriental-cds@163.com
#@Blog: https://blog.moyule.me
#
#♥I love Princess Zelda forever♥


import time


class Clock():
    """
    """
    def __init__(self):
        pass
    
    def get_local_time(self):
        self.local = time.strftime('%H:%M:%S',
                                   time.localtime(time.time()
                                   ))
    