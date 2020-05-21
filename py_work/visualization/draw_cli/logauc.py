# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 16:06:14 2019

@Author: Zhi-Jiang Yang, Dong-Sheng Cao
@Institution: CBDD Group, Xiangya School of Pharmaceutical Science, CSU, China
@Homepage: http://www.scbdd.com
@Mail: yzjkid9@gmail.com; oriental-cds@163.com
@Blog: https://blog.moyule.me

♥I love Princess Zelda forever♥
"""

from load import load
from sklearn.metrics import auc
import os
import matplotlib.pyplot as plt
import re
from math import log, log10
import math
from tqdm import tqdm
import numpy as np


def draw_logauc(folder_path='.',label_field='Label',score_field='average',figsize=(5,5),ascending=False,savedir=None):
    files = os.listdir(folder_path)   
    font_kws = {'family':'arial','size':18}
    f,ax = plt.subplots(figsize=figsize)
    
    i = 0   
    rounds = len(files)
    length = 10
    
    Lam = 0.001
    step = 0.001
    e = math.e
        
    decoyf = [(math.log10(ratio)+2) for ratio in np.arange(Lam,1+step,step)]
    
    for file in files:
        target = re.findall('\d\d_(.*?)_\w',file)[0]
        df = load(os.path.join(folder_path,file))
        pos = df[label_field].values.sum()
        neg = len(df)-pos
    
        resl = list()
        v = df.copy()
        v.sort_values(score_field,ascending=ascending,inplace=True)
        v = v.reset_index(drop=True)
        neg_idx = v[v.Label==0].index.tolist()

        ligandf = list()
        
        for ratio in np.arange(Lam,1+step,step):
            df_i = v.iloc[:neg_idx[int(neg*ratio)-1],:]
            linum = df_i[label_field].sum()
            ligandf.append(round(linum/pos,2)*100)
            
        
        for index in np.arange(len(decoyf)-1):
            x_i = (10**decoyf[index])/100
            x_i_ = (10**decoyf[index+1])/100

            y_i = ligandf[index]/100
            y_i_ = ligandf[index+1]/100

            bi = y_i_ - x_i_*((y_i_-y_i)/(x_i_-x_i))


            res = ((y_i_-y_i)/log(10,e))+bi*(log10(x_i_)-log10(x_i))
            resl.append(res)
            

        area = sum(resl)/log10(1/Lam)
        plt.plot(decoyf,ligandf,label='{} (AUC={})'.format(target, '%.3f'%area))
        i += 1
        ratio = i/rounds
        num = int(length*ratio)
        p = ''.join(['|','>'*num, '*'*(length-num), '|', ' ', '{}%'.format(round(ratio*100,1))])
        print(p,end='\r')
        
    resl = []
    
    ligandrandl = [10**i for i in decoyf]
    
    for index in range(len(decoyf)-1):
        rx_i = (10**decoyf[index])/100
        rx_i_ = (10**decoyf[index+1])/100

        ry_i = ligandrandl[index]/100
        ry_i_ = ligandrandl[index+1]/100

        bi = ry_i_ - rx_i_*((ry_i_-ry_i)/(rx_i_-rx_i))


        res = ((ry_i_-ry_i)/log(10,e))+bi*(log10(rx_i_)-log10(rx_i))
        resl.append(res)
    rlogAuc = sum(resl)/log10(1/Lam)
        
    plt.plot(decoyf,ligandrandl,linestyle='--',label=''.join(['Random',' logAUC=%.3f' %rlogAuc]),color='black')
    
    
    ax.tick_params(width=1.3)
    ax.set_xticks([-1,0,1,2])
    ax.set_xticklabels(['$\mathregular{10^{-1}}$',
                        '$\mathregular{10^{0}}$',
                        '$\mathregular{10^{1}}$',
                        '$\mathregular{10^{2}}$'])
    ax.set_xlim([-1,2])
    ax.set_ylim([0,100])
    ax.spines['bottom'].set_linewidth(1.3)
    ax.spines['left'].set_linewidth(1.3)
    ax.spines['top'].set_linewidth(1.3)
    ax.spines['right'].set_linewidth(1.3) 
    ax.set_xlabel('% Decoys Found',fontdict=font_kws)
    ax.set_ylabel('% Ligands Found',fontdict=font_kws)
    ax.tick_params(direction='in', which='both', labelsize=12)
    ax.legend(fontsize=6.5)
    if savedir:
        plt.savefig(savedir,bbox_inches='tight')
    else:
        pass
    plt.show()
    

       
if '__main__' == __name__:
    f = draw_logauc('..\data', savedir='..\dmeo_3.pdf')
    
    
    