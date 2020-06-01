# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 11:49:52 2020

@Author: Zhi-Jiang Yang, Dong-Sheng Cao
@Institution: CBDD Group, Xiangya School of Pharmaceutical Science, CSU, China
@Homepage: http://www.scbdd.com
@Mail: yzjkid9@gmail.com; oriental-cds@163.com
@Blog: https://blog.iamkotori.com

♥I love Princess Zelda forever♥
"""


from itertools import product
import matplotlib.pyplot as plt
from itertools import cycle
import numpy as np
import matplotlib.lines as mlines
from matplotlib.legend import Legend

class Drawer(object):
    
    def __init__(self, mean, std):
        assert mean.shape == std.shape and\
        (mean.index == std.index).all() and\
            (mean.columns == mean.columns).all()
            
        self.mean = mean
        self.std = std
        self.idxs = mean.index
        self.cols = mean.columns


    def getMeanStd(self):
        """
        """
        for idx,col in product(self.idxs, self.cols):
            m = self.mean.loc[idx, col]
            s = self.std.loc[idx, col]
            yield m,s
            
    def draw(self, colors, ylim, step=1.5, width=0.2):
        n = 0
        cs = cycle(colors)
        move = (len(self.cols) - 1) / 2
        
        self.f, ax = plt.subplots(figsize=(16,9), facecolor=(.18, .31, .31))
        ax.set_facecolor('#eafff5')
        for ms, color in zip(self.getMeanStd(), cs):
            n += 1
            center = ((n-1)//len(self.cols) + 1) * step
            x = (move - ((n-1)%6))*width
            x = center - x
            ax.bar(x, ms[0], width=width, yerr=ms[1], color=color)
        
        ax.set_ylim(ylim)
        ax.spines['bottom'].set_color('#caaca8')
        ax.spines['right'].set_color('#caaca8')
        ax.spines['left'].set_color('#caaca8')
        ax.spines['top'].set_color('#caaca8')
        ax.spines['bottom'].set_linewidth(1.5)
        ax.spines['left'].set_linewidth(1.5)
        ax.spines['top'].set_linewidth(1.5)
        ax.spines['right'].set_linewidth(1.5)
        ax.tick_params(direction='in', which='both', labelsize=12, width=0.3, color='#caaca8')
        
        ax.set_xticks(np.arange(step, step*len(self.idxs)+step, step))
        ax.set_xticklabels(self.idxs)
        
        ax.grid(ls='--', color='#caaca8', axis="y")
            
        legend = [mlines.Line2D([0], [0], color=c, lw=12) for c in colors]
        leg = Legend(ax, legend, labels=self.cols, ncol=1, 
                     #bbox_to_anchor=(8.1, 0.7), 
                     edgecolor='white', borderpad=0.6, facecolor='#eafff5')
        ax.add_artist(leg)
        
        ax.tick_params(labelcolor='tab:orange')
              