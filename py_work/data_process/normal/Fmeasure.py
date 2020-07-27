# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 14:02:37 2020

@Author: Zhi-Jiang Yang, Dong-Sheng Cao
@Institution: CBDD Group, Xiangya School of Pharmaceutical Science, CSU, China
@Homepage: http://www.scbdd.com
@Mail: yzjkid9@gmail.com; oriental-cds@163.com
@Blog: https://blog.iamkotori.com

♥I love Princess Zelda forever♥
"""


import pandas as pd
import numpy as np
from sklearn.metrics import matthews_corrcoef, precision_recall_fscore_support
import warnings
warnings.filterwarnings('ignore')


class Measure(object):
    
    def __init__(self, data, label_col, score_col):
        
        self.data = data
        self.y_true = data[label_col].values
        self.y_score = data[score_col].values
        
    def getFScore(self, beta=1):
        for thre in X:
            y_pred = np.where(self.y_score<thre, 0, 1)
            yield precision_recall_fscore_support(self.y_true, y_pred, 
                                                  beta=beta, average='binary')
    
    def getMccScore(self):
        for thre in X:
            y_pred = np.where(self.y_score<thre, 0, 1)
            yield matthews_corrcoef(self.y_true, y_pred)
    
    
    
    

if '__main__' == __name__:
    out = []
    thres = []
    data = pd.read_csv(r'bioactivity_disposed_2_CATS.csv')
    
    measure = Measure(data, 'label', 'P (label=1)')
    
    X = np.arange(0.001, 1.001, 0.001)
    
    for beta in np.arange(0.1, 1.1, 0.1):
        y = np.array(list(measure.getFScore(beta=beta)))
        idx = y[:, -2].argmax()
        
        out.append(y[idx][:-1])
        thres.append(X[idx])
        
    out = pd.DataFrame(out)
    out.columns = ['Precision', 'Recall', 'Fbeta_Score']
    out['Threshold'] = thres
    out.index = ['F{}'.format(x/10) for x in range(1,11)]
        # print(, X[idx])
        
    