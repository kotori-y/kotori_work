# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 08:59:28 2019

@Author: Zhi-Jiang Yang, Dong-Sheng Cao
@Institution: CBDD Group, Xiangya School of Pharmaceutical Science, CSU, China
@Homepage: http://www.scbdd.com
@Mail: yzjkid9@gmail.com; oriental-cds@163.com
@Blog: https://blog.moyule.me

♥I love Princess Zelda forever♥
"""

import pandas as pd
import numpy as np
# from load import load
from math import floor
import matplotlib.pyplot as plt
from sklearn.metrics import auc
from matplotlib.ticker import MultipleLocator
import re
import math
import warnings
from tqdm import tqdm
warnings.filterwarnings('ignore')

class Framerich(object):
    """
    """
    def __init__(self,file):
        self.file = file
#        self.active = set(load('data/framework20_query_17.csv').inchikey)
        
    def _load(self,value_field='value',**kwargs):
        """
        """
        if re.findall('\.xlsx', self.file) or re.findall('\.xls', self.file):
            data = pd.read_excel(self.file,**kwargs)
        elif re.findall('\.csv', self.file):
            data = pd.read_csv(self.file,**kwargs)
        elif re.findall('\.txt', self.file,**kwargs):
            data = pd.read_csv(self.file,sep='\t')
        
        try:
            data.drop('average',axis=1,inplace=True)
        except:
            print(self.file)
        
        label = np.where(data[value_field]>0,1,0)
        frame = data.pop('inchey_fram')
        
        data = data.iloc[:,-5:]
        data['Label'] = label
        data['Frame'] = frame.values    
        return data
    
    def _getY(self):
        data = self._load()
        scorers = data.columns[:-2]
#        print(scorers)
        active = set(load(r"C:\Users\0720\Desktop\MATE\Akuma\py_work\framework10_query_5.csv").inchikey)
        frames = len(set(data[data.Label==1]['Frame']) - active)
        length = len(data)
        
        for score in scorers:
            factor = []
            data_s = data.sort_values(score,ascending=False)
            for ratio in tqdm(np.arange(0.001,1.001,0.001)):
                data_si = data_s.iloc[:floor(length*ratio),:]
                data_si = data_si[data_si.Label==1]
                fc = len(set(data_si['Frame'])-active)/frames
                if fc != 1:
                    factor.append(fc)
                else:
                    while len(factor) != 1000:
                        factor.append(1)         
            yield factor
    
    def GetData(self):
        data = np.stack(self._getY(),axis=1)
        average = data.mean(axis=1)
        data_max = data.max(axis=1)
        data_min = data.min(axis=1)
        return average,data_max,data_min            
            
    def draw(self,ax,color,**kwargs):
        average,y_max,y_min = self.GetData()
        x = np.arange(0.001,1.001,0.001)
        area = auc(x,average)
        fp = re.findall('(.*?)_5mol',self.file)[0]
        
        if fp != 'Torsion':
            fp = fp.upper()
        else:
            pass
        
        ax.plot(x,average,color=color,alpha=1,label='{} (AUC={})'.format(fp,'%.3f'%area),lw=1)
        ax.fill_between(x,y_max,y_min,where=y_max>=y_min,color=color,alpha=0.08)
        
def main(files,colors):
    f,ax = plt.subplots(figsize=(5,5))
    
    for file in files:
        color = colors[(re.findall('(.*?)_5mol',file)[0]).upper()]
        Framerich(file).draw(ax,color)
    ml = MultipleLocator(0.1)
    ax.yaxis.set_minor_locator(ml)
    ax.xaxis.set_minor_locator(ml)
    ax.tick_params(direction='in', which='both', labelsize=8, width=0.3)
    ax.set_xlim([0,1.0])
    ax.set_ylim([0,1.0])
    ax.set_xlabel('Fraction of Samples',fontdict={'family': 'arial', 'size':10})
    ax.set_ylabel('Fraction of Frameworks',fontdict={'family': 'arial', 'size':10})
    ax.spines['bottom'].set_linewidth(.5)
    ax.spines['left'].set_linewidth(.5)
    ax.spines['right'].set_linewidth(.5)
    ax.spines['top'].set_linewidth(.5)
    ax.legend(loc=4,ncol=2,prop={'size':5})
    return f
    
if '__main__' == __name__:
    import os
    os.chdir(r'C:\Users\0720\Desktop\MATE\Akuma\FP_revised')
    
    colors = {'ECFP2': '#708090',
             'ECFP4': '#808080',
             'ECFP6': '#5F9EA0',
             'FCFP2': '#8FBC8B',
             'FCFP4': '#20B2AA',
             'FCFP6': '#3CB371',
             'ECFC2': '#8B008B',
             'ECFC4': '#BA55D3',
             'ECFC6': '#9370DB',
             'FCFC2': '#BC8F8F',
             'FCFC4': '#DEB887',
             'FCFC6': '#F4A460',
             'MACCS': '#DC143C',
             'FP2': '#F08080',
             'AP': '#FFD700',
             'TORSION': '#008080'}
    
    files = [r"FP2_5mol-similarity_revised.csv",
             r"MACCS_5mol-similarity_revised.csv",
             r"Torsion_5mol-similarity_revised.csv",
             r"AP_5mol-similarity_revised.csv",
             r"ecfp4_5mol-similarity_revised.csv",
             r"fcfp4_5mol-similarity_revised.csv",
             r"ecfc4_5mol-similarity_revised.csv",
             r"fcfc4_5mol-similarity_revised.csv",
             ]
    f = main(files,colors)
             
#    cfc_files = ["ecfc2_similarity.csv",
#                "ecfc4_similarity.csv",
#                "ecfc6_similarity.csv",
#                "fcfc2_similarity.csv",
#                "fcfc4_similarity.csv",
#                "fcfc6_similarity.csv"]  
#
#
#    cfp_files = ["ecfp2_similarity.csv",
#                "ecfp4_similarity.csv",
#                "ecfp6_similarity.csv",
#                "fcfp2_similarity.csv",
#                "fcfp4_similarity.csv",
#                "fcfp6_similarity.csv"]        

    
#    for F,n in zip([files,cfp_files,cfc_files],['BEST','CFP','CFC']):    
#        f = main(F,colors)
#        f.savefig('figure/{}_ActiveFrame.pdf'.format(n))
#            
            
            
            
