# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 09:21:27 2019

@Author: Zhi-Jiang Yang, Dong-Sheng Cao
@Institution: CBDD Group, Xiangya School of Pharmaceutical Science, CSU, China
@Homepage: http://www.scbdd.com
@Mail: yzjkid9@gmail.com; oriental-cds@163.com
@Blog: https://blog.moyule.me

♥I love Princess Zelda forever♥
"""


import warnings
warnings.filterwarnings('ignore')

import deepchem as dc
from deepchem.models.tensorgraph.models.graph_models import WeaveTensorGraph
#from deepchem.models.tensorgraph.models.graph_models import MPNNTensorGraph
#from deepchem.models.tensorgraph.models.graph_models import GraphConvModel
#from deepchem.feat import WeaveFeaturizer
from deepchem.feat.graph_features import ConvMolFeaturizer
from deepchem.feat.graph_features import WeaveFeaturizer
from deepchem.data.data_loader import CSVLoader 

import pandas as pd
import numpy as np

#featurizer = ConvMolFeaturizer()
featurizer = WeaveFeaturizer()
train_loader = CSVLoader(tasks=['LogD7.4'], smiles_field='smiles', featurizer=featurizer)
test_loader = CSVLoader(tasks=[None], smiles_field='smiles', featurizer=featurizer)

X_train = train_loader.featurize('../demo_data/reg/training_set.csv')
X_test = test_loader.featurize('../demo_data/reg/testing_set.csv')

model = dc.models.WeaveTensorGraph(n_tasks=1,mode='regression')
model.fit(X_train)
print(model.predic(X_test))