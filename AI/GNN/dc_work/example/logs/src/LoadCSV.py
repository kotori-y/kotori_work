# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 13:19:04 2019

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


class FeaturizerCSV(object):
    """
    Here, we use CSV file as the demo to test generate features.
    
    =====
    steps:
        1. Choosing the featurizer. In this dmeo, 'GraphConv' has been used;
        2. Useing the generated featurizer to get a CSVLoader;
        3. Useing the 'featurize' method to get data after featuring.
    """
    def __init__(self, tasks, smiles_field, featurizer):
        """
        1. Choosing the featurizer
        """
        self.tasks = tasks
        self.smiles_field = smiles_field
        if featurizer == 'ECFP':
            self.featurizer = dc.feat.CircularFingerprint(size=1024)
        elif featurizer == 'GraphConv':
            self.featurizer = dc.feat.ConvMolFeaturizer()
        elif featurizer == 'Weave':
            self.featurizer = dc.feat.WeaveFeaturizer()
        elif featurizer == 'Raw':
            self.featurizer = dc.feat.RawFeaturizer()
        elif featurizer == 'AdjacencyConv':
            self.featurizer = dc.feat.AdjacencyFingerprint(
                    max_n_atoms=150, max_valence=6)
        
    def _get_loader(self):
        """
        args:
            :tasks: the targets' field name
            :smiles_field: SMILES' field name
            :featurizer: featurizer
        """
        loader = dc.data.CSVLoader(
                tasks=self.tasks,
                smiles_field=self.smiles_field,
                featurizer=self.featurizer
                )
        return loader
       
    def generate_feature(self,data_file,shard_size=8192,splitter=None,**kwargs):
        """
        args:
            :data_file: the path of file
            :shard_size: pass
            :splitter: the way to spliter data:
                >index: spliter with index
                >random: as the name
                >butina: ?
                >task: ?
                >scaffold: as the name
                >stratified
        """
        loader = self._get_loader()
        dataset = loader.featurize(data_file, shard_size=shard_size)
        
        if not splitter:
            
            transformers = [
        dc.trans.NormalizationTransformer(
            transform_y=True, dataset=dataset, move_mean=True)
    ]
            for transformer in transfomers:
                 dataset = transformer.transform(dataset)
             
            return self.tasks, dataset, transformers
        
        
        
        else:
            splitters = {
      'index': dc.splits.IndexSplitter(),
      'random': dc.splits.RandomSplitter(),
      'scaffold': dc.splits.ScaffoldSplitter(),
      'butina': dc.splits.ButinaSplitter(),
      'task': dc.splits.TaskSplitter(),
      'stratified': dc.splits.RandomStratifiedSplitter()}
            
            splitter = splitters[splitter]
            
            if splitter == 'task':
                K = kwargs.get('K',5)
                fold_datasets = splitter.k_fold_split(dataset, K)
                all_dataset = fold_datasets
            else:
                frac_train = kwargs.get('frac_train', 0.8)
                frac_valid = kwargs.get('frac_valid', 0.1)
                frac_test = kwargs.get('frac_test', 0.1)
                
            train, valid, test = splitter.train_valid_test_split(
                dataset,
                frac_train=frac_train,
                frac_valid=frac_valid,
                frac_test=frac_test)
#            all_dataset = (train, valid, test)
        
            transformers = [
        dc.trans.NormalizationTransformer(
            transform_y=True, dataset=train, move_mean=True)
    ]
#            
            for transformer in transformers:
                train = transformer.transform(train)
                valid = transformer.transform(valid)
                test = transformer.transform(test)
            all_dataset = (train, valid, test)
        
        return self.tasks, all_dataset, transformers


            
    
    
    
if '__main__'==__name__:
    demo = FeaturizerCSV(tasks=['logS'], 
                   smiles_field='Smiles',
                   featurizer='GraphConv')
     
    tasks, dataset, transfomers = demo.generate_feature('../data/logS.csv',
                                                        splitter='random')
    train_set,valid_set,test_set = dataset
    print(train_set.y)
        
             
             
             
             
             
             
             
            
             
             
        