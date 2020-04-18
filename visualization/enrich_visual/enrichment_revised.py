# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 21:03:34 2019

@Author: Zhi-Jiang Yang, Dong-Sheng Cao
@Institution: CBDD Group, Xiangya School of Pharmaceutical Science, CSU, China
@Homepage: http://www.scbdd.com
@Mail: yzjkid9@gmail.com; oriental-cds@163.com
@Blog: https://blog.moyule.me

♥I love Princess Zelda forever♥
"""

import pandas as pd
import numpy as np
import math
import re
from matplotlib.ticker import MultipleLocator
import matplotlib.pyplot as plt
from sklearn.metrics import auc
import warnings
warnings.filterwarnings('ignore')

class EnrichCurve(object):
    """
    """
    def __init__(self,file):
        self.file = file
        
    def _load(self,**kwargs):
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
        
        label = np.where(data.value>0,1,0)
        data = data.iloc[:,-5:]
        data['Label'] = label
        return data
    
    def _getY(self):
        data = self._load()
        total = data.Label.sum()
        length = len(data)
        scorers = data.columns[:-1]
        
        for scorer in scorers:
            data_s = data.sort_values(scorer,ascending=False)
            n_label = data_s.Label.values
            y = [n_label[:math.ceil(length*ratio)].sum()/total for ratio in np.arange(0,1.01,0.01)]
            yield y
            
    
    def getData(self):
        data = np.stack(self._getY(),axis=1)
        average = data.mean(axis=1)
        data_max = data.max(axis=1)
        data_min = data.min(axis=1)
        return average,data_max,data_min
    
    
    def draw(self,ax,color,**kwargs):
        average,y_max,y_min = self.getData()
        x = np.arange(0,1.01,0.01)
        area = auc(x,average)
        fp = re.findall('(.*?)_5mol',self.file)[0]
        
        if fp != 'Torsion':
            fp = fp.upper()
        else:
            pass
        
        ax.plot(x,average,color=color,alpha=1,label='{} (AUC={})'.format(fp,'%.3f'%area),lw=1)
        # ax.fill_between(x,y_max,y_min,where=y_max>=y_min,color=color,alpha=0.08)
        
        
        
        
def main(files,colors):
    f,ax = plt.subplots(figsize=(5,5))
    
    for file in files:
        color = colors[(re.findall('(.*?)_5mol',file)[0]).upper()]
        EnrichCurve(file).draw(ax,color)
    ml = MultipleLocator(0.1)
    ax.yaxis.set_minor_locator(ml)
    ax.xaxis.set_minor_locator(ml)
    ax.tick_params(direction='in', which='both', labelsize=8, width=0.3)
    ax.set_xlim([0,1.0])
    ax.set_ylim([0,1.0])
    ax.set_xlabel('Fraction of Samples',fontdict={'family': 'arial', 'size':10})
    ax.set_ylabel('Fraction of Actives',fontdict={'family': 'arial', 'size':10})
    ax.spines['bottom'].set_linewidth(.5)
    ax.spines['left'].set_linewidth(.5)
    ax.spines['right'].set_linewidth(.5)
    ax.spines['top'].set_linewidth(.5)
    ax.legend(loc=4,ncol=2,prop={'size':5})
    return f
    
    
    
if '__main__' == __name__:
    import os
    os.chdir(r'FP_revised')
    
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
#             
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
#                "fcfp6_similarity.csv"
#                ]        

    
#    files = os.listdir()
#    for F,n in zip([files,cfc_files,cfp_files],['BEST','CFC','CFP']):    
    f = main(files,colors)
#        f.savefig('figure/ActiveMol/{}figure_mol_BG_thiner.pdf'.format(n))
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    