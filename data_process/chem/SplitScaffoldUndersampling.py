# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 14:26:33 2020

@Author: Zhi-Jiang Yang, Dong-Sheng Cao
@Institution: CBDD Group, Xiangya School of Pharmaceutical Science, CSU, China
@Homepage: http://www.scbdd.com
@Mail: yzjkid9@gmail.com; oriental-cds@163.com
@Blog: https://blog.moyule.me


♥I love Princess Zelda forever♥
"""

"""
1. Spliting data with scaffold under the ratio: 4:1
2. Oversampling trainning data

2 loop 100 times
"""

import os
import re
from math import ceil
import pandas as pd
import numpy as np
import openbabel as ob
from rdkit import Chem
from rdkit.Chem.Scaffolds import MurckoScaffold
from imblearn.under_sampling import RandomUnderSampler
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from imblearn.metrics import sensitivity_score, specificity_score
from tqdm import tqdm
import multiprocessing as mp
import warnings
warnings.filterwarnings('ignore')

def obsmitosmile(smi):
    """
    """
    conv = ob.OBConversion()
    conv.SetInAndOutFormats("smi", "can")
    conv.SetOptions("K", conv.OUTOPTIONS)
    mol = ob.OBMol()
    conv.ReadString(mol, smi)
    smile = conv.WriteString(mol)
    smile = smile.replace('\t\n', '')
    return smile


def GetMol(Smiles):
    """
    """
    mol = Chem.MolFromSmiles(Smiles)
    if not mol:
        mol = Chem.MolFromSmiles(obsmitosmile(Smiles))
        
    return mol if mol else None


def SmilesToFrameInChIKey(SMILES):
    """
    """
    mol = GetMol(SMILES)
    
    if mol:
        frame = MurckoScaffold.GetScaffoldForMol(mol)
        try:
            frame = MurckoScaffold.MakeScaffoldGeneric(frame)
        except:
            pass
    else:
        frame = None
    
    frame = Chem.MolToInchiKey(frame) if frame else None
    return frame


def Sample(X,y):
    """
    """
    rus = RandomUnderSampler()
    X_resampled, y_resampled = rus.fit_resample(X, y)
    
    return X_resampled, y_resampled


def Split(file,loop):
    """
    """
    print(">>> Spliting......")
    df = pd.read_csv(os.path.join('./docking_origin_data_ywl',file))
    df = df.dropna(axis=0)
    Scaffold = df.mol.map(lambda x: SmilesToFrameInChIKey(x))
    df.insert(1,'Scaffold',Scaffold)
    Scaffold = list(set(Scaffold))
    
    for n in range(1,loop+1):
        train_idx,test_idx = [],[]
        for scaffold in tqdm(Scaffold):
            df_s = df[df.Scaffold==scaffold]
        
            if len(df_s) >= 5:
                df_train = df_s.sample(frac=0.8)
            else:
                df_train = df_s.sample(n=1)
            
            df_test = df_s[~df_s.index.isin(df_train.index)]
            train_idx.extend(df_train.index)
            test_idx.extend(df_test.index)
        
        X_train = df.loc[train_idx]
        X_test = df.loc[test_idx]
        
        X_train.drop(['mol','Scaffold','name'],axis=1,inplace=True)
        X_test.drop(['mol','Scaffold','name','number'],axis=1,inplace=True)
        y_train = X_train.pop('Label')
        y_test = X_test.pop('Label')
    
        yield X_train,X_test,y_train,y_test,train_idx,n
    

def main(file):
    """
    """
    N = re.findall('_(.*?)_final',file)[0]
    try:
        os.mkdir('./res/{}'.format(N))
    except FileExistsError:
        pass
    
    pred_res = pd.DataFrame()
    fit_res = pd.DataFrame()
    metrics_res = pd.DataFrame(index=['SE','SP','AUC'])
    metrics_fit = pd.DataFrame(index=['SE','SP','AUC'])
    split_res = pd.DataFrame()
    
    for X_train,X_test,y_train,y_test,train_idx,turn in Split(file,10):
        
        print('============== {} =============='.format(turn))
        
        # X_train,X_test,y_train,y_test,train_idx = Split(file)
        X_test = np.array(X_test)
        # number_test = X_test.pop('number')
        split_res['Turn{}_TrainIdx'.format(turn)] = train_idx
        
        metrics_staion = pd.DataFrame()
        
        for n in tqdm(range(1,101)):
            
            X_resampled, y_resampled = Sample(X_train,y_train)
            number_resampled = X_resampled[:,0]
            X_resampled = X_resampled[:,1:]
            
            model = XGBClassifier(learning_rate=0.05,
                                  max_depth=6,
                                  n_estimators=500,
                                  subsample=0.8)
            model.fit(X_resampled,y_resampled)
            
            y_pred_proba = model.predict_proba(X_test)[:,1]
            pred_res['Turn{}_{}'.format(turn,n)] = list(y_pred_proba)
            
            y_fit_proba = model.predict_proba(X_resampled)[:,1]
            station_fit = pd.DataFrame({'Number':number_resampled,
                                        'Proba':y_fit_proba,
                                        'Label':list(y_resampled)})
            
            station_fit['IDX'] = '{}_{}'.format(turn,n)
            fit_res = pd.concat([fit_res,station_fit],axis=0,
                                ignore_index=True,sort=False)
            metrics_staion = pd.concat([metrics_staion,station_fit],axis=0,
                                ignore_index=True,sort=False)
            
        y_pred_proba_mean = pred_res.mean(axis=1)
        y_pred_mean = (y_pred_proba_mean>=0.5)+0
        
        se = sensitivity_score(y_test, y_pred_mean)
        sp = specificity_score(y_test, y_pred_mean)
        auc = roc_auc_score(y_test, y_pred_proba_mean)
        metrics_res['Turn_{}'.format(turn)] = [se,sp,auc]
        
        metrics_staion = metrics_staion.groupby('Number').mean()
        y_fit_mean = (metrics_staion.Proba>=0.5)+0
        y_fit_test = metrics_staion.Label.values
        
        se_fit = sensitivity_score(y_fit_test, y_fit_mean)
        sp_fit = specificity_score(y_fit_test, y_fit_mean)
        auc_fit = roc_auc_score(y_fit_test, metrics_staion.Proba.values)
        metrics_fit['Turn_{}'.format(turn)] = [se_fit,sp_fit,auc_fit]
        
        
    pred_res.to_csv('./res/{}/PredProba_{}.csv'.format(N,N)
                    ,index=False)
    fit_res.to_csv('./res/{}/FitProba_{}.csv'.format(N,N)
                    ,index=False)
        
        
    metrics_res_mean = metrics_res.mean(axis=1)
    metrics_res_var = metrics_res.var(axis=1)
    
    metrics_res['Mean'] = list(metrics_res_mean)
    metrics_res['Var'] = list(metrics_res_var)
    
    metrics_fit_mean = metrics_fit.mean(axis=1)
    metrics_fit_var = metrics_fit.var(axis=1)
    
    metrics_fit['Mean'] = list(metrics_fit_mean)
    metrics_fit['Var'] = list(metrics_fit_var)
    
    
    metrics_res.to_csv('./res/{}/PredMetrics_{}.csv'.format(N,N))
    metrics_fit.to_csv('./res/{}/FitMetrics_{}.csv'.format(N,N))
    
    split_res.to_csv('./res/{}/TrainIdx_{}.csv'.format(N,N),
                       index=False)
    

if '__main__' == __name__:
    # files = os.listdir('./docking_origin_data_ywl')
    # pool = mp.Pool()
    # for file in files:
    #     pool.apply_async(main, args=(file,))
    # pool.close()
    # pool.join()
    main('07_hivrt_final_moe_all.csv')
    
    
    
    
    
            
            
            
            
        
        
        
        
    








