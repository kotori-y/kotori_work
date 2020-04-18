# -*- coding: utf-8 -*-
"""
Created on Wed May 15 19:29:28 2019

@Author: CBDD Group, CSU, China
@Homepage: http://www.scbdd.com
@Mail: yzjkid9@gmail.com
@Blog: https://blog.moyule.me

♥I love Megumi forerver♥
"""

print (__doc__)

from rdkit.Chem import AllChem as Chem
import openbabel as ob
#import pandas as pd
import numpy as np
#import os


class MolProcesser(object):
    
    def __init__(self, Config=False):
        """initialization Attributes"""
                
    def _obsmitosmile(self,smiles):
        conv = ob.OBConversion()
        conv.SetInAndOutFormats("smi", "can")
        conv.SetOptions("K", conv.OUTOPTIONS)
        mol = ob.OBMol()
        conv.ReadString(mol, smi)
        smile = conv.WriteString(mol)
        smile = smile.replace('\t\n', '')
        return smile    
            
    def process(self,smiles):
        m = Chem.MolFromSmiles(smiles)
        if not m:
            smile = self._obsmitosmile(smiles)
            m = Chem.MolFromSmiles(smile)
        else:
            pass
        
        smi = Chem.MolToSmiles(m,isomericSmiles=False) if m else 'unrecognized'
        inchikey = Chem.MolToInchiKey(Chem.MolFromSmiles(smi)) if m else 'unrecognized'   
        return smi, inchikey


def main_single(SMILES):
    processer = MolProcesser()
    inchikey, smi = processer.process(SMILES)
    return inchikey, smi


def main_multi(SMILES_Iterable):
    """
    :param SMILES_Iterable: a set of SMILES
    :type SMILES_Iterable: Iterable object
    :rtype: array    
    """
    processer = MolProcesser()
    res = np.array(list((map(processer.process, SMILES_Iterable))))
    smi_list, inchikey_list = res[:,0],res[:,1]
    return smi_list, inchikey_list

if '__main__' == __name__:
    smi = ['N[C@@H](Cc1[nH]cnc1)C']*5
    
    smi_list, inchikey_list = main_multi(smi)









