# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 14:15:42 2020

@Author: Zhi-Jiang Yang, Dong-Sheng Cao
@Institution: CBDD Group, Xiangya School of Pharmaceutical Science, CSU, China
@Homepage: http://www.scbdd.com
@Mail: yzjkid9@gmail.com; oriental-cds@163.com
@Blog: https://blog.moyule.me

♥I love Princess Zelda forever♥
"""


import os
import re
# from math import ceil
import pandas as pd
import numpy as np
# import openbabel as ob
# from rdkit import Chem
# from rdkit.Chem.Scaffolds import MurckoScaffold
from imblearn.under_sampling import RandomUnderSampler
from xgboost import XGBClassifier
# from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, accuracy_score
from sklearn.model_selection import StratifiedKFold
from imblearn.metrics import sensitivity_score, specificity_score
from tqdm import tqdm
import multiprocessing as mp
import warnings
warnings.filterwarnings('ignore')


def GetKFold(X,y,Kfold=5):
    """
    Spliting data to Kfold on Stratified method
    """
    skf = StratifiedKFold(n_splits=5, shuffle=True)
    for train_index, test_index in skf.split(X, y):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        
        yield X_train, X_test, y_train, y_test
        
    
def Sample(X,y):
    """
    """
    rus = RandomUnderSampler()
    X_resampled, y_resampled = rus.fit_resample(X, y)
    
    return X_resampled, y_resampled


def BuildModel(X,y):
    """
    """
    model = model = XGBClassifier(learning_rate=0.05,
                                  max_depth=6,
                                  n_estimators=500,
                                  subsample=0.8)
    model.fit(X, y)
    
    return model


def GetProba(X_train, X_test,
             y_train, y_test,
             loop=100):
    """
    """
    res = pd.DataFrame()
    res_fit = pd.DataFrame()
    
    X_test = X_test[:,1:]
    for n in tqdm(range(loop)):
        X_resampled, y_resampled = Sample(X_train, y_train)
        number = X_resampled[:,0]
        X_resampled = X_resampled[:,1:]
        
        model = BuildModel(X_resampled, y_resampled)
        y_proba = model.predict_proba(X_test)[:,1]
        y_proba_fit = model.predict_proba(X_resampled)[:,1]
        res = pd.concat([res, pd.Series(y_proba,index=y_test.index)],axis=1)
        res_fit = pd.concat([res_fit, pd.DataFrame({'Proba_fit':y_proba_fit, 
                                                    'Label':y_resampled,
                                                    'number':number})])
            
    res = res.mean(axis=1)
    res_fit = res_fit.groupby('number').mean()
    return res, res_fit

        
def main(file):
    """
    """
    N = re.findall('_(.*?)_final',file)[0]
    try:
        os.mkdir('./res_0314/{}'.format(N))
    except FileExistsError:
        pass
    
    res = pd.DataFrame()
    res_fit = pd.DataFrame()
    
    metrics = pd.DataFrame(index=['SE','SP','ACC','AUC'])
    metrics_fit = pd.DataFrame(index=['SE','SP','ACC','AUC'])
    
    X = pd.read_csv(os.path.join('./docking_origin_data_ywl',file))##
    X = X.dropna(axis=0)
    X.drop(['mol','name'],axis=1,inplace=True)
    y = X.pop('Label')
    X = np.array(X)
    
    
    for turn in range(1, 11):
        proba = pd.DataFrame()
        proba_fit = pd.DataFrame()
        
        print('================ {} Turn: {} ================'.format(N, turn))
             
        for X_train,X_test,y_train,y_test in GetKFold(X,y,Kfold=5):
            res_,res_fit_ = GetProba(X_train,X_test,
                                     y_train,y_test,
                                     loop=100)
        
            proba = pd.concat([proba, res_])
            proba_fit = pd.concat([proba_fit, res_fit_])
            proba_fit['Turn'] = turn
            
            
        proba.sort_index(inplace=True)
        res['Turn_{}'.format(turn)] = proba[0]
        # print(res)
        res_fit = pd.concat([res_fit,proba_fit])
    
    # return res, res_fit
    
    for proba,turn in zip(res.iteritems(), range(1,11)):
        
        y_pred = (proba[1]>=0.5)+0
        acc = accuracy_score(y, y_pred)
        se = sensitivity_score(y, y_pred)
        sp = specificity_score(y, y_pred)
        auc = roc_auc_score(y, proba[1])
        metrics['Turn_{}'.format(turn)] = [se,sp,acc,auc]
        
        y_pred_fit = (res_fit[res_fit.Turn==turn].Proba_fit>=0.5)+0
        y_true_fit = res_fit[res_fit.Turn==turn].Label.values
        acc = accuracy_score(y_true_fit, y_pred_fit)
        se = sensitivity_score(y_true_fit, y_pred_fit)
        sp = specificity_score(y_true_fit, y_pred_fit)
        auc = roc_auc_score(y_pred_fit, res_fit[res_fit.Turn==turn].Proba_fit)
        metrics_fit['Turn_{}'.format(turn)] = [se,sp,acc,auc]
        
        
    metrics['Mean'] = metrics.loc[:,'Turn_1':'Turn_10'].mean(axis=1)
    metrics['Std'] = metrics.loc[:,'Turn_1':'Turn_10'].std(axis=1)
    
    metrics_fit['Mean'] = metrics_fit.loc[:,'Turn_1':'Turn_10'].mean(axis=1)
    metrics_fit['Std'] = metrics_fit.loc[:,'Turn_1':'Turn_10'].std(axis=1)
    
    
    res.insert(0,'Label',y)
    
    metrics.to_csv(r'./res_0314/{}/Metrics_{}.csv'.format(N,N))
    res.to_csv(r'./res_0314/{}/Proba_{}.csv'.format(N,N),index=False)
    
    metrics_fit.to_csv(r'./res_0314/{}/MetricsFit_{}.csv'.format(N,N))
    res_fit.to_csv(r'./res_0314/{}/ProbaFit_{}.csv'.format(N,N),index=False)

    
    # return metrics, metrics_fit


if '__main__' == __name__:
#     files = os.listdir('./docking_origin_data_ywl')
#     pool = mp.Pool()
#     for file in files:
#         pool.apply_async(main, args=(file,))
#     pool.close()
#     pool.join()
    main(r'01_ampc_final_moe_all.csv')
    
        
        
    
                
            
                
    
    

               
            
            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    