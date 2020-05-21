# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 09:34:03 2019

@Author: Zhi-Jiang Yang, Dong-Sheng Cao
@Institution: CBDD Group, Xiangya School of Pharmaceutical Science, CSU, China
@Homepage: http://www.scbdd.com
@Mail: yzjkid9@gmail.com; oriental-cds@163.com
@Blog: https://blog.moyule.me

♥I love Princess Zelda forever♥
"""

print(__doc__)

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import KFold,RandomizedSearchCV
from sklearn.metrics import confusion_matrix,accuracy_score,auc,roc_auc_score
from sklearn.metrics import precision_score,recall_score
from imblearn.metrics import specificity_score,sensitivity_score
import pandas as pd
import os
from xgboost import XGBClassifier
import numpy as np


def GetData(File):
    print('>>>Loading Data...\n')
    df = pd.read_csv(File)
    try:
        x = df.drop('SMILES',axis=1)
    except:
        x = df.drop('Smiles',axis=1)
    y = x.pop('Label')
    return x,y   


class ML(object):
    
    def __init__(self):
#        self.x = 0
#        self.y = 0
        self.model = 0
        self.AUC = 0
        self.acc = 0
        self.spec = 0
        self.sens = 0
        self.y_pred = 0
        self.y_pred_proba_pos = 0
    
    def Rf_clf(self,n_estimators=100,seed=None):
        self.model = RandomForestClassifier(n_estimators=n_estimators
                                     ,n_jobs=-1
                                     ,random_state=seed
    #                                 ,max_features=0.5
                                     ,min_samples_leaf=4
                                     ,min_samples_split=10
                                     ,class_weight='balanced')
    
    def XGB_clf(self,learning_rate=0.05,max_depth=6,n_estimators=500):
        
        self.model = XGBClassifier(learning_rate=learning_rate
                                   ,max_depth=max_depth
                                   ,n_estimators=n_estimators
                                   )
    
        
    def Fit(self,X_train,Y_train):
        print('>>>Fitting, wait please...')
        self.model.fit(X_train,Y_train)
        
        
    def Predict(self,x_test):
        self.y_pred = self.model.predict(x_test)
        self.y_pred_proba_pos = self.model.predict_proba(x_test)[:,1]

        
    def GetMetrics(self,y_test):
        tn, fp, fn, tp = confusion_matrix(y_test,self.y_pred).flatten()
        self.acc = '%.3f'%accuracy_score(y_test,self.y_pred)
        self.AUC = '%.3f'%roc_auc_score(y_test,self.y_pred_proba_pos)
#        self.sens = tp/(tp+fn)
        self.sens = '%.3f'%sensitivity_score(y_test,self.y_pred)
#        self.spec = '%.3f'%(tn/(tn+fp))
        self.spec = '%.3f'%specificity_score(y_test,self.y_pred)


    def output(self):
        df = pd.DataFrame({'Accuracy':[float(self.acc)],
                           'Sensitivity':[float(self.sens)],
                           'Specificity':[float(self.spec)],
                           'AUC':[float(self.AUC)]
                           })
        return df


def main(X_train,Y_train,x_test,y_test):
    ml = ML()
    ml.Rf_clf()
#    ml.XGB_clf()
    ml.Fit(X_train,Y_train)
    ml.Predict(x_test)
    ml.GetMetrics(y_test)
    df = ml.output()
    return df
    
   
if '__main__' == __name__:
       
    TrainFile = input('Enter the ABSOLUTE PATH of TRAINING set:\n'
                      )    
    TestFile = input('Enter the ABSOLUTE PATH of TESTING set:\n'
                      )
        
    X_train,Y_train = GetData(TrainFile)
    x_test,y_test = GetData(TestFile)
    X_train,x_test = np.array(X_train),np.array(x_test)
   
    print('----------Crossing Validation----------')
#    kf = KFold(n_splits=5,shuffle=True)
#    
#    cv = pd.DataFrame({'Accuracy':[0],
#                       'Sensitivity':[0],
#                       'Specificity':[0],
#                       'AUC':[0]
#                       })
#    
#    for train_index,valid_index in kf.split(X_train):
#        x_train,x_valid = X_train[train_index],X_train[valid_index]
#        y_train,y_valid = Y_train[train_index],Y_train[valid_index]
#        cv += main(x_train,y_train,x_valid,y_valid)
#    cv = cv/5    
    print('--------------Testing Set----------------')
    res = main(X_train,Y_train,x_test,y_test)    
    
    
