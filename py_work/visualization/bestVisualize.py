# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 15:28:31 2020

@Author: Zhi-Jiang Yang, Dong-Sheng Cao
@Institution: CBDD Group, Xiangya School of Pharmaceutical Science, CSU, China
@Homepage: http://www.scbdd.com
@Mail: yzjkid9@gmail.com; oriental-cds@163.com
@Blog: https://blog.iamkotori.com

♥I love Princess Zelda forever♥
"""


import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
import pandas as pd
import numpy as np
from scipy.stats import gaussian_kde



def bestScatter(
        reference, data=None, 
        color='#134261', cmap='Blues'
    ):
    
    fig, ax = plt.subplots(figsize=(9,9*.618))
    ax.set_facecolor('#FFFFFF')
    
    refer = ax.scatter(*reference,
                       color=color, marker='*', s=100,
                       label="121")
    
    z = gaussian_kde(data.T)(data.T)
    x = data[:, 0]
    y = data[:, 1]
    gen = ax.scatter(x, y, c=z, cmap=cmap, label='456', s=25, edgecolors='grey')
    
    cbar = plt.colorbar(gen)
    ax.hlines(0.5, x.min(), x.max())
    # bar.set_ticklabels(data[:,0])
    
    # lines = [refer, gen]
    # plt.legend(lines, [l.get_label() for l in lines], loc=3, fontsize=14)
    
    ax.grid(True)
    plt.show()
    return fig



if '__main__' == __name__:
    
    data = pd.read_csv('paper\demo\optBest.txt', sep='\t')
    data = data.loc[:, ['logSmort','Proba']]
    data = data.to_numpy()
    
    fig = bestScatter(data[0], data[1:, :])