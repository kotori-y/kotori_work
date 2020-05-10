# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 16:46:32 2019

@Author: Zhi-Jiang Yang, Dong-Sheng Cao
@Institution: CBDD Group, Xiangya School of Pharmaceutical Science, CSU, China
@Homepage: http://www.scbdd.com
@Mail: yzjkid9@gmail.com; oriental-cds@163.com
@Blog: https://blog.moyule.me

♥I love Princess Zelda forever♥
"""


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def smooth(x,y,):
    from scipy import interpolate
    x_new = np.linspace(x.min(),x.max(),10000)
    func = interpolate.interp1d(x,y,kind='cubic')
    y_new = func(x_new)
    return [x_new, y_new]

def load(file):   
    data = pd.read_csv(file)
    data = data.iloc[:-1,:]
    return data

def draw(ax, t, file):
    data = load(file)
    font_kws = {'family':'arial','size':20}
#    font_kws_title = fontdict={'family':'arial','size':30}
    for col in data.columns[1:]:
        ax.plot(*smooth(data.Tc, data[col]),label=col,lw=2)
    ax.set_xlim([0,1])
    ax.tick_params(direction='in', which='both', labelsize=12)
    ax.spines['bottom'].set_linewidth(1.2)
    ax.spines['left'].set_linewidth(1.2)
    ax.spines['right'].set_linewidth(1.2)
    ax.spines['top'].set_linewidth(1.2)
    ax.set_xlabel('Simillarity',fontdict=font_kws)
    ax.set_ylabel('Hit Ratio',fontdict=font_kws)
    ax.set_title('({}) {}'.format(t, file.replace('.csv','')),fontdict=font_kws,loc='left',pad=15)
    ax.legend()
        

if '__main__' == __name__:
    import os
    os.chdir(r'C:\Users\0720\Desktop\MATE\Sorcha'
            )  
    f,axes = plt.subplots(1,3,figsize=(8*3,8*0.618))
#     draw(r'Top1.csv')
    for ax, file, t in zip(axes.flatten(), [r'Top1.csv', r'Top5.csv', r'Top10.csv'],['a','b','c']):
        draw(ax,t,file)
