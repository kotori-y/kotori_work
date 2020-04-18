# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 11:12:48 2019

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
from deepchem.models.tensorgraph.models.graph_models import GraphConvModel
from deepchem.data.data_loader import CSVLoader



def loadCSV(tasks, smiles_field, featurizer):
    """
    """
    loader = deepchem.data.CSVLoader(
            tasks=tasks,
            smiles_field=smiles_field,
            featurizer=featurizer
            )
    
    
    