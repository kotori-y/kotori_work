# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 23:39:39 2020

@Author: Zhi-Jiang Yang, Dong-Sheng Cao
@Institution: CBDD Group, Xiangya School of Pharmaceutical Science, CSU, China
@Homepage: http://www.scbdd.com
@Mail: yzjkid9@gmail.com; oriental-cds@163.com
@Blog: https://blog.moyule.me

♥I love Princess Zelda forever♥
"""


import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd 
import os
import re
import matplotlib.lines as mlines
from matplotlib.legend import Legend

def DrawKDE(data, color, ax):
    sns.kdeplot(data, ax=ax, clip=[data.min(),data.max()], color=color, label=None)


def DrawXGL():
    os.chdir(r'./property_AD')
    files = os.listdir()
    
    colors = sns.color_palette("hls", 9)
    colors[-1] = '#ffc107'
    colors[-2] = '#07ffc1'
    neg_color = colors.pop(0)
    X_label = ['Num. of Hydrogen Bond Acceptors',
               'Num. of Hydrogen Bond Donors',
               'Num. of Rotable Bonds',
               'Formal Charge',
               'logP(o/w)',
               'Molecular Mass']
    
    f, axes = plt.subplots(8, 6, figsize=(23*0.8,23), sharex='col')
    plt.subplots_adjust(wspace=0.3, hspace=0.3)
    
    for file,color,axs in zip(files, colors, axes):
        N = re.findall('_(.*?)_',file)[0]
        
        df = pd.read_csv(file)
        df = df.loc[:,['Label', 'a_acc', 'a_don', 
                       'b_rotN', 'FCharge', 'SlogP', 
                       'molecular weight']
                    ]
        
        pos = df[df.Label==1].iloc[:,1:]
        neg = df[df.Label==0].iloc[:,1:]
        
        for pos_data, neg_data, ax, idx in zip(pos.iteritems(), neg.iteritems(), axs, range(len(axs))):
            DrawKDE(pos_data[1].values, color=color, ax=ax)
            DrawKDE(neg_data[1].values, color=neg_color, ax=ax)
            
            if idx==0:
                legend = [mlines.Line2D([0], [0], color=c) for c in [color, neg_color]]
                leg = Legend(ax, legend, labels=['Ligand', 'Decoy'], ncol=1, bbox_to_anchor=(8.1, 0.7), edgecolor='white',title=N,borderpad=0.6)
                ax.add_artist(leg)
            else:
                ax.set_ylabel('Density',fontdict={'family': 'arial', 'size':10})
                pass
            ax.spines['bottom'].set_color('#caaca8')
            ax.spines['right'].set_color('none')
            ax.spines['left'].set_color('#caaca8')
            ax.spines['top'].set_color('none')
            ax.spines['bottom'].set_linewidth(1.5)
            ax.spines['left'].set_linewidth(1.5)
            ax.tick_params(direction='in', which='both', labelsize=8, width=0.3, color='#caaca8')
            
            ax.grid(ls='--', color='#caaca8')
            
            if file == files[-1]:
                ax.set_xlabel(X_label[idx],fontdict={'family': 'arial', 'size':10})
            else:
                pass
    
    return f


if '__main__' == __name__:
    f = DrawXGL()
    # f.savefig(r'../DUDE_matrix0323.pdf',bbox_inches = 'tight', pad_inches = .5)
    
    
    
    
    
    
    
    
    