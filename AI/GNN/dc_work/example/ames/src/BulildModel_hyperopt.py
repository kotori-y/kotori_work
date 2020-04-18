# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 08:54:35 2019

@Author: Zhi-Jiang Yang, Dong-Sheng Cao
@Institution: CBDD Group, Xiangya School of Pharmaceutical Science, CSU, China
@Homepage: http://www.scbdd.com
@Mail: yzjkid9@gmail.com; oriental-cds@163.com
@Blog: https://blog.moyule.me

♥I love Princess Zelda forever♥
"""

import deepchem as dc
import numpy as np
from deepchem.models.tensorgraph.models.graph_models import GraphConvTensorGraph
from LoadCSV import FeaturizerCSV
from BuildModel import Model
from sklearn.metrics import accuracy_score,roc_auc_score,confusion_matrix
from hyperopt import fmin, tpe, hp



class HyperSearch(Model):
    """
    A demo to combine Hyperopt and DeepChem
    """
    def __init__(self,model_type,mode,n_tasks,dataset):
        super().__init__(model_type,mode,n_tasks)
        self.dataset = dataset
        splitter = dc.splits.RandomSplitter()
        self.fold_datasets = splitter.k_fold_split(self.dataset, 5)
        
    def _get_score(self,params):
#        dataset = params.pop('dataset')
#        splitter = dc.splits.RandomSplitter()
#        fold_datasets = splitter.k_fold_split(self.dataset, 5)
        
        res = []
        print(params)
        for train, val in self.fold_datasets:
            model = self.get_model(train, **params)
            y_proba = model.predict(val)[:,:,1]
            area = roc_auc_score(val.y.flatten(), y_proba.flatten())
            res.append(area)
            del model
        
        return -sum(res)/5
    
    def SearchBestModel(self,space):
        best_idx = fmin(fn=self._get_score, space=space, 
                        algo=tpe.suggest,max_evals=2)
        
        self.best_params = {'batch_size':[32,64,128][best_idx['batch_size']],
                            'epoch':range(100,350,50)[best_idx['epoch']]}
        
        self.best_model = self.get_model(self.dataset,**self.best_params)
#    def GetBestModel(self):
#        self.
    
    
if '__main__'==__name__:
    demo = FeaturizerCSV(tasks=['Label'], 
                   smiles_field='SMILES',
                   featurizer='GraphConv')
     
    tasks, all_dataset, transformers = demo.generate_feature('../data/ames_data.csv',
                                                             split='stratified')
    
    train_set, valid_set, test_set = all_dataset
#    splitter = dc.splits.RandomSplitter()
#    print('spliting')
#    fold_datasets = splitter.k_fold_split(train_set, 5)
#    
#    for train,val in fold_datasets:
#        print(len(train),len(val))
    
    hyper = HyperSearch(model_type='GCT',
                        mode='classification',
                        n_tasks=1,
                        dataset=train_set)
#     
    space = {'batch_size': hp.choice('batch_size', [32,64,128]),
             'epoch': hp.choice('epoch', range(100,350,50))}
#       
    hyper.SearchBestModel(space)
    print(hyper.best_params)
    model = hyper.best_model
    y_proba = model.predict(valid_set)[:,:,1].flatten()
    y_val = model.y.flatten()
    area = roc_auc_score(y_val,y_proba)
    print(area)
    
    
            
        
        
        
    