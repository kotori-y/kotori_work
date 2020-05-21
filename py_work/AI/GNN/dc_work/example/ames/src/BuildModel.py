# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 16:07:49 2019

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
from sklearn.metrics import accuracy_score,roc_auc_score,confusion_matrix
#from sklearn.metrics import sen


class Model(object):
    """
    Here, we use GCT model to implement a classfication task
    """
    def __init__(self, model_type, mode, n_tasks):
        self.model_type = model_type
        self.mode = mode
        self.n_tasks = n_tasks
        
    def get_model(self, train_set, epoch=100, batch_size=64,
                  graph_conv_layers=[64, 64],
                  dense_layer_size=128,
                  dropout=0.0):
        
        if self.model_type == 'GCT':
            model = GraphConvTensorGraph(n_tasks=self.n_tasks,
                                   batch_size=batch_size,
                                   mode=self.mode,
                                   graph_conv_layers=graph_conv_layers,
                                   dense_layer_size=dense_layer_size,
                                   dropout=dropout)
            print('>>>Fitting...')
            model.fit(train_set,nb_epoch=epoch)
            return model
            

#def EvaluateModel(y_true,y_pred,mode,):
    
           
            
if '__main__'==__name__:
    import warnings
    warnings.filterwarnings('ignore')
    import os
    os.environ["CUDA_VISIBLE_DEVICES"] = "1"
    
    os.environ["TF_FORCE_GPU_ALLOW_GROWTH"]='true'
    import tensorflow as tf
    config = tf.ConfigProto()
    config.gpu_options.per_process_gpu_memory_fraction = 0.9
    tf.keras.backend.set_session(tf.Session(config=config))
    
    
    
    demo = FeaturizerCSV(tasks=['Label'], 
                   smiles_field='SMILES',
                   featurizer='GraphConv')    
    
    tasks, dataset, transformers = demo.generate_feature('../data/ames_data.csv',
                                                        splitter='stratified')
    
    train_set,valid_set,test_set = dataset
    
    m = Model(model_type='GCT',
              mode='classification',
              n_tasks=1)
    
    model = m.get_model(train_set=train_set,epoch=100,batch_size=32,
                        graph_conv_layers=[64, 64, 64],
                        dense_layer_size=128,
                        dropout=0.15)
       
    print('>>>Predicting...')
    y_proba = model.predict(valid_set)[:,:,1].flatten()
    y_pred = np.where(y_proba>0.5,1,0)
    
    print('>>>Evaluating...')
    y_true = valid_set.y.flatten()
    acc = round(accuracy_score(y_true,y_pred),3)
    
    tn, fp, fn, tp = confusion_matrix(y_true,y_pred).flatten()
    sens = round(tp/(tp+fn),3)
    spec = round(tn/(tn+fp),3)
    
    area = round(roc_auc_score(y_true,y_proba),3)
    
    print('===============')
    print('Accuracy: {}\nAUC: {}\nSpecificity: {}\nSensitivity: {}'.format(acc, area, spec, sens))
    print('===============')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    