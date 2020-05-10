# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 20:57:12 2019

@Author: Zhi-Jiang Yang, Dong-Sheng Cao
@Institution: CBDD Group, Xiangya School of Pharmaceutical Science, CSU, China
@Homepage: http://www.scbdd.com
@Mail: yzjkid9@gmail.com; oriental-cds@163.com
@Blog: https://blog.moyule.me

♥I love Princess Zelda forever♥
"""


import shap
import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import KFold
from load import load


class CV_shap(object):
    """
    """
    def __init__(self,file,label_col,features,loop,nthread=20):
        self.shap_data = None
        self.aver = None
        self.data = load(file)
        self.nthread = nthread
        label = self.data.pop(label_col)
        self.features = features
        self.loop = loop
        self.data = self.data.loc[:,features]
        self.data['Label'] = list(label)
        
    def _build_model(self,X_train,y_train,
                    n_estimators=150,
                    learning_rate=0.2,
                    max_depth=6,
                    subsample=1):
        """
        """
        print('>>>Fitting')
        model = XGBClassifier(n_estimators=n_estimators,
                              learning_rate=learning_rate,
                              max_depth=max_depth,
                              subsample=subsample,
                              nthread=self.nthread)
        
        model.fit(X_train,y_train)
        return model
    
    def _get_shap(self,model,X_test):
        explainer = shap.TreeExplainer(model)
        y_base = explainer.expected_value
        shap_values = explainer.shap_values(X_test)
        shap_values = pd.DataFrame(shap_values)
        shap_values['base_line'] = float(y_base)
        return shap_values
    
    def get_cv_shap(self):
        RES = []
        cols = self.features
        cols.append('Baseline')
        cols.append('Label')
        
        for turn in range(self.loop):
            print('--------------Turn: {}--------------'.format(turn))
            IDX = []
            out = pd.DataFrame()
            kf = KFold(n_splits=5,shuffle=True)
            for train_index,test_index in kf.split(self.data):
                IDX.extend(list(test_index))
                X_train,X_test = self.data.iloc[train_index,:],self.data.iloc[test_index,:]
                y_train,y_test = X_train.pop('Label'),X_test.pop('Label')
                model = self._build_model(X_train,y_train)
                shap_val = self._get_shap(model,X_test)
                shap_val['Label'] = y_test.values
                out = pd.concat([out,shap_val],ignore_index=True)
            out.index = IDX
            out = out.sort_index()
            RES.append(out)
        self.shap_data = sum(RES)/self.loop
        self.shap_data.columns = cols
        print('>>> Finished')
        print('------------------------------\n')
        return self.shap_data


if '__main__' == __name__:
    import os
    os.chdir(r'C:\Users\0720\Desktop\MATE\yzy\SHAP_data')
    shap_cv = CV_shap('maccs_training.csv',
                      'Label',
                      ['MACCS(-47)', 'MACCS(-62)'],
                      1)
    
    
    
    
    
    
    
    
    
