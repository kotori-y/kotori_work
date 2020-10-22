# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 14:43:09 2020

@Author: Zhi-Jiang Yang, Dong-Sheng Cao
@Institution: CBDD Group, Xiangya School of Pharmaceutical Science, CSU, China
@Homepage: http://www.scbdd.com
@Mail: yzjkid9@gmail.com; oriental-cds@163.com
@Blog: https://blog.iamkotori.com

♥I love Princess Zelda forever♥
"""


import numpy as np
import matplotlib.pyplot as plt
import re
import matplotlib.lines as mlines
from matplotlib.legend import Legend


def horizon(x, y, category, yticklabels=None):
    
    lines = []
    _uni = set(category)
    colors = ['#76d6df', '#ffb822', '#ff8b85']
    
        
    fig, ax = plt.subplots(figsize=(6,20))
    
    
    for cate, color in zip(_uni, colors):
        _x = x[category==cate]
        _y = y[category==cate]
        
        label = re.findall('.*_(.*)_.*', cate)[0]
        p = ax.barh(_y, _x, color=color, label=label)
        lines.append(p)
    
    
    ax.set_ylim(0, len(x)+1)
    
    if yticklabels is not None:
        ax.set_yticks(y)
        ax.set_yticklabels(
            yticklabels, 
            fontdict={'family':'arial', 'size':18}
    )
    
    ax.set_xticklabels(
            [int(x) for x in plt.xticks()[0]], 
            fontdict={'family':'arial', 'size':18}
        )
    
    legend = [mlines.Line2D([0], [0], color=c, linewidth=20) for c in colors][::-1]
    leg = Legend(ax, legend, labels=[p.get_label() for p in lines[::-1]], ncol=1, 
                 bbox_to_anchor=(1.40, 0.65), edgecolor='white', labelspacing=1.8,
                 handletextpad=1.5, title_fontsize=18, 
                 prop={'family':'arial', 'size':16},
                 title='Type', borderpad=0.6)
    ax.add_artist(leg)
    
    
    ax.spines['right'].set_linewidth(3)
    ax.spines['left'].set_linewidth(3)
    ax.spines['top'].set_linewidth(3)
    ax.spines['bottom'].set_linewidth(3)
    
    ax.grid(True)
    ax.set_axisbelow(True)
    
    ax.set_title(
        'The Most Enriched GO Terms', 
        fontdict={'size':20, 'family':'arial'},
        pad=18,
        weight='bold'
        )
    
    ax.tick_params(
            direction='in', which='both', 
            length=8, width=2,
        )
    
    
    plt.show()
    return fig
    
    
    
    


    
    
    
    
if '__main__' == __name__:
    import pandas as pd
    
    data = pd.read_csv(
        'Annotation_filter_GO.csv',
        # usecols=['Term_1', 'Count', 'PValue']
    )
    
    data = data[data.PValue<=0.005]
    
    x = data.Count.values
    y = np.arange(1, len(x)+1)
    
    fig = horizon(x, y, 
            data.Category.values,
            yticklabels=data.Term_1.values)