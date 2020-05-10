# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 21:37:20 2019

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
import numpy as np


class Enrichment(object):
    
    def __init__(self, folder_path='.',label_field='Label',score_field='average',figsize=(5,5),ascending=False,savedir=None):
        self.folder_path = folder_path
        self.label_field = label_field
        self.score_field = score_field
        self.figsize = figsize
        self.ascending = ascending
        self.savedir = savedir        
                              
    def Load(self,file):
        self.df = load(file)
#        self.df = abs(self.df)
        self.length = len(self.df)
        self.hit_all = self.df[self.label_field].values.sum()
#        self.hit_all = len(self.df[self.df[self.label_col]==1])
#        self.scorers = pd.Series(self.score_col)

    
    def sort_count(self):
        res = []

        df_i = self.df.sort_values(self.score_field,ascending=self.ascending).copy()
        for scape in np.arange(0,1,0.01):
            sampled = int(self.length*scape)
            hit_sampled = df_i.iloc[:sampled+1,:][self.label_field].values.sum()
            res.append(hit_sampled)
#        print(res)
        return res 

    def show_enrichment_roc(self):
        files = os.listdir(self.folder_path)   
        font_kws = {'family':'arial','size':18}
        f,ax = plt.subplots(figsize=self.figsize)
        
        for file in files:
            target = re.findall('\d\d_(.*?)_\w',file)[0]
            self.Load(os.path.join(self.folder_path,file))
#            print(self.hit_all,file)
            
#            f,ax = plt.subplots(figsize=(5,5))
            
            self.res = self.sort_count()
            
#            for item in res:
            y = [round(x/self.hit_all,2) for x in self.res]
            AUC = auc(np.arange(0,1.00,0.01),y)
            AUC = '%.3f'%AUC
            plt.plot(np.arange(0,1.00,0.01),y,label='{} (AUC={})'.format(target,AUC))
            
#        ax.set_yticks([0,int(self.hit_all*0.2),
#                       int(self.hit_all*0.4),
#                       int(self.hit_all*0.6),
#                       int(self.hit_all*0.8),
#                       int(self.hit_all*1.0)])
#            
#            plt.plot([0, 1], [0, self.hit_all], color='navy', lw=1, linestyle='--')
        ax.set_ylim([0,1])
        ax.set_xlim([0,1])
        ax.set_yticklabels([0,20,40,60,80,100])
        ax.set_xticklabels([0,20,40,60,80,100])
        ax.set_xlabel('top % of ranked database', fontdict=font_kws)
        ax.set_ylabel('% found Activities (yield)', fontdict=font_kws)
        ax.tick_params(direction='in', which='both', labelsize=12)
        ax.spines['bottom'].set_linewidth(1.3)
        ax.spines['left'].set_linewidth(1.3)
        ax.spines['right'].set_color('None')
        ax.spines['top'].set_color('None')
        ax.tick_params(width=1.3)
        ax.legend(fontsize=6.5)
        if self.savedir:
            plt.savefig(self.savedir,bbox_inches='tight')
        else:
            pass
        plt.show()
        
        
        
        
if '__main__' == __name__:
    f = Enrichment('..\data', savedir='..\dmeo_4.pdf')
    f.show_enrichment_roc()