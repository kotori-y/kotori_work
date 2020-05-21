# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 15:17:07 2019

@Author: Zhi-Jiang Yang, Dong-Sheng Cao
@Institution: CBDD Group, Xiangya School of Pharmaceutical Science, CSU, China
@Homepage: http://www.scbdd.com
@Mail: yzjkid9@gmail.com; oriental-cds@163.com
@Blog: https://blog.moyule.me

♥I love Princess Zelda forever♥
"""

import pandas as pd
import numpy as np
from load import load
from math import floor
import matplotlib.pyplot as plt
from sklearn.metrics import auc
from matplotlib.ticker import MultipleLocator

def frame_enrich(file, label_col, Ascore, Dscore, ratios=[0.001,0.01,0.05,0.1],dim=4):
    data = load(file)
    label = data.pop(label_col)
    label = np.where(label>0,1,0)
    framework = data.pop('inchey_fram')
    scores = Ascore + Dscore
    data = data.loc[:,scores]
    data['Label'] = label
    data['FrameWork'] = framework
    length = len(data)
    
    active = load('data/framework10_query_5.csv').inchikey
    
    all_frame = data[~data.FrameWork.isin(active.values)]
    all_frame = len(all_frame.drop_duplicates('FrameWork'))   
    active_frame = data[(~data.FrameWork.isin(active.values)) & (data.Label==1)]
    active_frame = len(active_frame.drop_duplicates('FrameWork'))
    
    res = []
    
    for col in data.columns[:-2]:
        ascending = col in Ascore
        st = data.sort_values(col,ascending=ascending).copy()
        for ratio in ratios:
            aim = st.iloc[:floor(length*ratio),:].copy()
            Ns = aim[(aim.Label==1) & (~aim.FrameWork.isin(active.values))]
            Ns = len(Ns.drop_duplicates('FrameWork'))
            Nd = aim[~aim.FrameWork.isin(active.values)]
            Nd = len(Nd.drop_duplicates('FrameWork'))
            val = (Ns/Nd)/(active_frame/all_frame)
            res.append(val)
    res = pd.DataFrame(np.array(res).reshape(-1,dim)).T
    res.columns = ['Mol_{}'.format(i) for i in scores]
    res.index = ['{}%'.format(x*100) for x in ratios]
    return res


def frame_curve(file, label_col, Ascore, Dscore):
    def _getfctor():
        for score in scores:
            factor = []
            ascending = score in Ascore
            data_s = data.sort_values(score, ascending=ascending).copy()
            for ratio in np.arange(0.001,1.001,0.001):
                data_si = data_s.iloc[:floor(length*ratio),:]
                data_si = data_si[data_si.Label==1]
                fc = len(set(data_si['Frame'])-active)/frames
                if fc != 1:
                    factor.append(fc)
                else:
                    while len(factor)!=1000:
                        factor.append(1)
                        
            yield factor,score
    
    def smooth(x,y):
        from scipy import interpolate
        x_new = np.linspace(x.min(),x.max(),2000)
        func = interpolate.interp1d(x,y,kind='cubic')
        y_new = func(x_new)
        return [x_new, y_new]
       
    data = load(file)
    label = data.pop(label_col)
    frame = data.pop('inchey_fram')
    scores = Ascore + Dscore
    label = np.where(label>0,1,0)
    
    data = data.loc[:,scores]
    data['Label'] = label
    data['Frame'] = frame.values
    
    active = set(load('data/framework10_query_5.csv').inchikey)
    frames = len(set(data[data.Label==1]['Frame']) - active)
    length = len(data)
    
    f,ax = plt.subplots(figsize=(5,5)) 
#    colors = plt.get_cmap('tab20').colors
    for item in _getfctor():
        factor,score = item
        area = auc(np.arange(0.001,1.001,0.001),factor)
        ax.plot(np.arange(0.001,1.001,0.001),factor,label='{} (AUC={})'.format(score,'%.3f'%area),
                lw=1.5,alpha=1)
    ax.set_xlim([0,1])
    ax.set_ylim([0,1])
    ax.set_xticks([x/10 for x in range(0,11,2)])
    ax.set_yticks([x/10 for x in range(0,11,2)])
    ml = MultipleLocator(0.1)
    ax.yaxis.set_minor_locator(ml)
    ax.xaxis.set_minor_locator(ml)
    
    ax.set_xlabel('Fraction of Samples',size=12)
    ax.set_ylabel('Recall of Frameworks',size=12)
    
    ax.spines['bottom'].set_linewidth(1.5)
    ax.spines['left'].set_linewidth(1.5)
    ax.spines['top'].set_linewidth(1.5)
    ax.spines['right'].set_linewidth(1.5) 
    ax.tick_params(direction='in', which='both', labelsize=12)
    ax.legend(fontsize=8,ncol=2,loc=4)
#    ax.minorticks_on()
    plt.show()
    return f
    
            
            
        
   
#    
#if '__main__'==__name__:
#    file = r'C:\Users\0720\Desktop\MATE\Akuma\Similarity_average.csv'
#    
#    
#    
#    f = frame_curve(file,'value',['MACCS', 'AP', 'Daylight', 
#                              'Torsion', 'ECFP4', 'FCFP4',
#                              'ECFC4','FCFC4'])
#    
    
    #['MACCS', 'AP', 'Daylight', 'Torsion', 'ECFP2', 'ECFP4',
#       'ECFP6', 'FCFP2', 'FCFP4', 'FCFP6', 'FCFC2', 'FCFC4', 'FCFC6', 'ECFC2',
#       'ECFC4', 'ECFC6']
#    
    
    
    
    
    
    
    
    
    
    
    
    
    