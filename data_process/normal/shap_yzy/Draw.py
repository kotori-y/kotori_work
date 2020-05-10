# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 22:08:54 2019

@Author: Zhi-Jiang Yang, Dong-Sheng Cao
@Institution: CBDD Group, Xiangya School of Pharmaceutical Science, CSU, China
@Homepage: http://www.scbdd.com
@Mail: yzjkid9@gmail.com; oriental-cds@163.com
@Blog: https://blog.moyule.me

♥I love Princess Zelda forever♥
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from load import load
import shap

class Draw(object):
    """
    """
    def __init__(self,ori_data,loading,**kwarg):
        """
        """
        self.ori_data = load(ori_data)
        if not loading:
            self.shap_data = kwarg.get('shap_data')
        else:
            self.shap_data = load(kwarg.get('shap_data'))
          
    def get_abs_mean(self): 
        shap_data = self.shap_data.iloc[:,:-2]
        aver = shap_data.applymap(lambda x: abs(x))
        aver = aver.apply(lambda x: x.mean())
        self.aver = aver.sort_values(ascending=False)
           
    def draw_hist(self,top,savedir=None,**kwgs):
        print('------------------------------')
        print('Drawing Hist Plot')
        aver = self.aver.sort_values()
        aver = aver[:top]
        f,ax = plt.subplots(figsize=(5*0.618,5))
        for x,y in zip(range(len(aver)), aver.values):
            ax.barh(x,y,color='#1E88E5') 
            ax.set_yticks(range(len(aver)))
            ax.set_yticklabels(aver.keys(),fontdict={'size':5})
            ax.set_ylim([-0.5,len(aver)-0.5])
            ax.spines['bottom'].set_linewidth(0.5)
            ax.spines['left'].set_linewidth(0.5)
            ax.spines['right'].set_linewidth(0.5)
            ax.spines['top'].set_linewidth(0.5)
            ax.tick_params(direction='in', which='both', labelsize=5, length=2)
            ax.set_xlabel('mean(|SHAP value|)\n(average impact on model output magnitude)',fontdict={'size':7})
        if savedir:
            plt.savefig(savedir,bbox_inches='tight',**kwgs)
        else:
            pass
        plt.show()
        print('>>> Finished')
        print('------------------------------\n')
        
    def draw_scatter(self,label,savedir=None,**kwgs):
        print('------------------------------')
        print('>>> Drawing Scatter Plot')
        ori_data = self.ori_data.drop('Label',axis=1)
        shap_data = self.shap_data.iloc[:,:-2]
        f,ax = plt.subplots()
        font_kws = {'size':8}
        ax.scatter(ori_data[label], shap_data[label],s=5,color='#1E88E5',alpha=0.8)
        ax.spines['right'].set_linewidth(1.2)
        ax.spines['top'].set_linewidth(1.2)
        ax.spines['bottom'].set_linewidth(1.2)
        ax.spines['left'].set_linewidth(1.2)
        ax.hlines(0,ori_data[label].min()-0.1,ori_data[label].max()+0.1,lw=0.8)
        ax.set_xlim(ori_data[label].min()-0.1,ori_data[label].max()+0.1)
        ax.set_xlabel(label, fontdict=font_kws)
        ax.tick_params(direction='in', which='both',labelsize=5)
        ax.set_ylabel('SHAP Value', fontdict=font_kws,labelpad=0.5)
        if savedir:
            plt.savefig(savedir,bbox_inches='tight',**kwgs)
        else:
            pass
        plt.show()
        print('>>> Finished')
        print('------------------------------\n')

    def draw_violin(self,top,savedir=None,**kwgs):
        print('------------------------------')
        print('>>> Drawing Violin Plot...')
        aver = self.aver.iloc[:top]
        shap_data = self.shap_data.iloc[:,:-2]
        data = shap_data.T.reindex(aver.keys()).T   
        f,ax = plt.subplots()
        colors = ['#3be0d9','#3dbb2f','#2b49ac','#2dc481','#6283f1','#898846','#da7985','#c61920','#f2c44a','#1d2ea8',
        '#aa1948','#00afd8','#f58233','#7ab800','#eeaf00','#f7347a','#ffd8ef','#a97afb','#32f3c9','#db0545']
        violin_parts = ax.violinplot([data[col] for col in data.columns])
        for partname in ('cbars','cmins','cmaxes'):
            vp = violin_parts[partname]
            vp.set_edgecolor('black')
            vp.set_linewidth(0.5)
    
        for vp,color in zip(violin_parts['bodies'],colors):
            vp.set_facecolor(color)
            vp.set_edgecolor(color)
            vp.set_alpha(0.8)
    
        ax.set_xlim([0.5,top+0.5])
        ax.hlines(0,0.5,top+0.5,lw=0.5)
        ax.set_xticks(range(1,top+1))
        ax.set_xticklabels(data.columns,rotation=90,fontdict={'size':7})
        ax.spines['bottom'].set_linewidth(1.2)
        ax.spines['left'].set_linewidth(1.2)
        ax.spines['right'].set_linewidth(1.2)
        ax.spines['top'].set_linewidth(1.2)
        ax.tick_params(direction='in', which='both')
        if savedir:
            plt.savefig(savedir,bbox_inches = 'tight',**kwgs)
        else:
            pass
        plt.show()
        print('>>> Finished')
        print('------------------------------\n')
        
    def draw_summary(self,top,cols,savedir=None,**kwargs):
        print('------------------------------')
        print('>>> Drawing Summary Plot...')
        shap.summary_plot(shap_values=np.array(self.shap_data.iloc[:,:-2]),
                        features=np.array(self.ori_data[cols]),
                        show=False,
                        max_display=top,
                       feature_names=cols)
        if savedir:
            plt.savefig(savedir,kwargs)
        else:
            pass
        plt.show()
        print('>>> Finished')
        print('------------------------------\n')
        
    def draw_force(self,idx,cols,savedir=None,**kwargs):
        print('------------------------------')
        print('>>> Drawing Force Plot...')
        val = self.shap_data.iloc[idx,:]
        shap.force_plot(val.Baseline, val[:-2].values,
                        self.ori_data.loc[idx,cols].apply(lambda x: '%.0f'%x),
                        matplotlib=True,show=False)
        if savedir:
            plt.savefig(savedir,kwargs)
        else:
            pass
        plt.show()
        print('>>> Finished')
        print('------------------------------\n')

  
  
  
if '__main__'==__name__:
    d = Draw(ori_data=r"C:\Users\0720\Desktop\MATE\yzy\SHAP_data\maccs_training.csv",
             loading=True,
             shap_data=r"C:\Users\0720\Desktop\MATE\yzy\MACCS_SHAP\MACCS_CV_Shap.csv")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    