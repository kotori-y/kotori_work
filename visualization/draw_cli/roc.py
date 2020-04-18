# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 15:25:36 2019

@Author: Zhi-Jiang Yang, Dong-Sheng Cao
@Institution: CBDD Group, Xiangya School of Pharmaceutical Science, CSU, China
@Homepage: http://www.scbdd.com
@Mail: yzjkid9@gmail.com; oriental-cds@163.com
@Blog: https://blog.moyule.me

♥I love Princess Zelda forever♥
"""

from load import load
from sklearn.metrics import roc_curve,auc
import os
import matplotlib.pyplot as plt
import re


def drawroc(folder_path='.',label_field='Label',score_idx=[1],figsize=(5,5),ascending=False,savedir=None):
    files = os.listdir(folder_path)   
    font_kws = {'family':'arial','size':18}
    f,ax = plt.subplots(figsize=figsize)
    
    if ascending:
        pos_label = 0
    else:
        pos_label = 1
    
    i = 0   
    rounds = len(files)
    length = 10
    
    for file in files:
#        target = re.findall('\d\d_(.*?)_\w',file)[0]
        data = load(os.path.join(folder_path,file))
        
        label = data[label_field].values
        scores = data.iloc[:,score_idx]
        
        for label,score in scores.iteritems():
            fpr, tpr, _= roc_curve(label, score, pos_label=pos_label)  
            area = auc(fpr,tpr)
            ax.plot(fpr,tpr,linewidth=1.5,label='{} (AUC={})'.format(label, '%.3f'%area))
        i += 1
        ratio = i/rounds
        num = int(length*ratio)
        p = ''.join(['|','>'*num, '*'*(length-num), '|', ' ', '{}%'.format(round(ratio*100,1))])
        print(p,end='\r')
        
    ax.set_xlabel('false positive rate', fontdict=font_kws)
    ax.set_ylabel('true positive rate', fontdict=font_kws)
    ax.set_ylim([0.0,1.0])
    ax.set_xlim([0.0,1.0])
    ax.spines['bottom'].set_linewidth(1.3)
    ax.spines['left'].set_linewidth(1.3)
    ax.spines['top'].set_linewidth(1.3)
    ax.spines['right'].set_linewidth(1.3) 
    ax.tick_params(direction='in', which='both', labelsize=12)
    ax.legend(fontsize=6.5)
            
    ax.plot([0, 1], [0, 1], '--', color=(0.6, 0.6, 0.6), label='Random')
    if savedir:
        plt.savefig(savedir)
    plt.show()
    return f
    
    
       
if '__main__' == __name__:
    f = drawroc('..\data', savedir='..\dmeo.pdf')