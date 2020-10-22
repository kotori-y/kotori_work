# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 14:53:29 2020

@Author: Zhi-Jiang Yang, Dong-Sheng Cao
@Institution: CBDD Group, Xiangya School of Pharmaceutical Science, CSU, China
@Homepage: http://www.scbdd.com
@Mail: yzjkid9@gmail.com; oriental-cds@163.com
@Blog: https://blog.iamkotori.com

♥I love Princess Zelda forever♥
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap

# optHist = pd.read_csv(r"./parp/optHistory.csv")
# history = optHist.groupby('step').mean()
# history = history.drop('swarm', axis=1).drop('Turn', axis=1)
# history = history.drop('substructure', axis=1)

def make_patch_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)

def drawMultiYaxis(
        data:np.ndarray, labels:list, colors:list,
        mainFaceColor='#ffffff', axFaceColor='#ffffff'
    ):
    
    fig, host = plt.subplots(figsize=(16,8), facecolor=mainFaceColor)
    host.set_facecolor(axFaceColor)
    fig.subplots_adjust(right=0.75)
    
    tkw = dict(size=4, width=1.5)
    
    lines = []
    num = 0
    
    for value, label, color in zip(data.T, labels, colors):
        if not num:
            p, = host.plot(value, label=label, color=color, lw=3)
            host.set_xlabel("Step", fontsize=20)
            host.set_ylabel(label, fontsize=20)
            host.yaxis.label.set_color(p.get_color())
            host.spines['left'].set_color(p.get_color())
            host.spines['top'].set_color('none')
            
            host.tick_params(axis='y', colors=p.get_color(), **tkw)
            host.tick_params(axis='x', **tkw)
            host.tick_params(direction='in', which='both', 
                             labelsize=18, length=8,
                             width=4)
            
            host.spines['bottom'].set_linewidth(4)
            host.spines['left'].set_linewidth(4)
        else:    
            par = host.twinx()
            par.spines["right"].set_position(("axes", 1+((num-1)*0.08)))    
            make_patch_spines_invisible(par)
            par.spines["right"].set_visible(True)
            # par.set_ylabel(label, fontsize=20)
            
            p, = par.plot(value, label=label, color=color, lw=3)
            par.yaxis.label.set_color(p.get_color())
            par.spines['right'].set_color(p.get_color())
            par.spines['right'].set_linewidth(4)
            
            # par.tick_params(axis='y', colors=p.get_color(), **tkw)
            par.tick_params(direction='in', which='both', 
                            labelsize=18, colors=p.get_color(), length=8, width=4)
            
            
        num += 1
        lines.append(p)
    plt.legend(lines, [l.get_label() for l in lines], loc=4, fontsize=14)
    plt.grid(axis='y')
    plt.show()
    
    
    return fig
        
        
        
if '__main__' == __name__:
    optHist = pd.read_csv(r"paper\demo\parp\optHistory.csv")
    history = optHist.iloc[:50, :]
    
    history = optHist.groupby('step').mean()
    history = history.drop('swarm', axis=1).drop('Turn', axis=1)
    history = history.drop('substructure', axis=1)
    # history = history.drop('smiles', axis=1)
    
    data = np.array(history)
    labels = history.columns
    colors = list(get_cmap('Set2').colors)
    colors[0] = (0., 0., 0.,)
    fig = drawMultiYaxis(
            data, labels, colors,
            # mainFaceColor='#e6fdff',
            # axFaceColor='#b3d9e8',
        )
    
    
    
    