# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 14:16:36 2020

@Author: Zhi-Jiang Yang, Dong-Sheng Cao
@Institution: CBDD Group, Xiangya School of Pharmaceutical Science, CSU, China
@Homepage: http://www.scbdd.com
@Mail: yzjkid9@gmail.com; oriental-cds@163.com
@Blog: https://blog.iamkotori.com

♥I love Princess Zelda forever♥
"""


import numpy as np
import matplotlib.pyplot as plt


def bubble_plot(x, y, sizeData, hueData, yticklabels=None):
    
    fig, ax = plt.subplots(figsize=(6,20))
    
    s = 800
    radius = sizeData/sizeData.max()
    hue = hueData/hueData.max()
    
    scatter = ax.scatter(x, y, c=hue, s=radius*s, cmap='RdBu', edgecolor='grey')
    
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
    
    
    handles, labels = scatter.legend_elements(
        prop="sizes", alpha=0.8, num=5, 
        func=lambda x: (x/s)*sizeData.max(),
        color=(182/255, 31/255, 46/255)
    )
    
    legendSize = ax.legend(
        handles, labels, 
        loc="upper right", title="Gene Number", 
        fontsize=14, title_fontsize=12,
        labelspacing=1.3,
        bbox_to_anchor=(1.35, 0.75),
        edgecolor='#ffffff'
    )
    
    
    ax.grid(True, zorder=-1000)
    ax.set_axisbelow(True)
    
    cbar = plt.colorbar(scatter, 
                 cax = fig.add_axes([0.98, 0.41, 0.06, 0.1]),
                 # ticks=hueData
                 )
    cbar.ax.set_title('$pP_{value}$', pad=12, fontsize=14)
    cbar.ax.set_yticklabels(["{:.1f}".format(x*hueData.max()) for x in cbar.get_ticks()],
                            fontsize=12)

    ax.add_artist(legendSize)
    
    
    ax.set_xlim([x.min()-1, x.max()+1])
    ax.spines['right'].set_linewidth(3)
    ax.spines['left'].set_linewidth(3)
    ax.spines['top'].set_linewidth(3)
    ax.spines['bottom'].set_linewidth(3)
    
    ax.tick_params(
            direction='in', which='both', 
            length=8, width=2,
        )
    
    
    cbar.ax.tick_params(
            direction='in', which='both', 
            length=4, color='#000000',
            left=True
        )
    
    ax.set_title(
        'The Most Enriched Pathways', 
        fontdict={'size':20, 'family':'arial'},
        pad=18,
        weight='bold'
        )
    
    plt.show()
    return fig





if "__main__" == __name__:

    import pandas as pd
    
    data = pd.read_csv(
        'Annotation_filter_KEGG.csv', 
        usecols=['Term_1', 'Count', 'PValue', 'FoldEnrichment']
    )

    x = data.FoldEnrichment.values
    y = np.arange(1, len(x)+1)
    
    sizeData = data.Count.values
    hueData = -np.log10(data.PValue.values)
    
    fig = bubble_plot(x, y, sizeData, hueData, data.Term_1.values)