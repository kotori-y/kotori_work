# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 08:55:02 2020

@Author: Zhi-Jiang Yang, Dong-Sheng Cao
@Institution: CBDD Group, Xiangya School of Pharmaceutical Science, CSU, China
@Homepage: http://www.scbdd.com
@Mail: yzjkid9@gmail.com; oriental-cds@163.com
@Blog: https://blog.iamkotori.com

♥I love Princess Zelda forever♥
"""


import re
import multiprocessing as mp
from functools import partial
import pandas as pd
from rdkit import Chem
from rdkit.Chem.rdSLNParse import MolFromQuerySLN
from mol_utils import getmol


def getNum(sln):
    num = re.findall('\<max\=(.*?)\>', sln)
    num = int(num[0]) if num else 0
    return num


class SlnFilter(object):

    def __init__(self, slnStrings, nJobs=1):
        """Initialization

        Parameters
        ----------
        slnStrings : Iterable object, each element is str
            [description]
        nJobs : int, optional
            [description], by default 1
        """
        self.slnStrings = slnStrings
        self.nJobs = nJobs
        self.loadSLN()

    def loadSLN(self, slnStrings=None):

        slnStrings = slnStrings or self.slnStrings
        self.slnPatterns = [MolFromQuerySLN(sln) for sln in slnStrings]

    def check(self, mol, limits=None):

        limits = limits or [0]*len(self.slnPatterns)

        res = []
        for patt, lim in zip(self.slnPatterns, limits):
            length = len(mol.GetSubstructMatches(patt))
            if length > lim:
                res.append(False)
            else:
                res.append(True)
        return res

    def run(self, mols, limits=None):

        func = partial(self.check, limits=limits)
        # pool = mp.Pool(self.nJobs)
        # self.filterResult = pool.map_async(func, mols).get()
        # pool.close()
        # pool.join()
        self.filterResult = [func(mol) for mol in mols]


if '__main__' == __name__:
    slnStrings = pd.read_csv(r'*.csv')
    slnStrings = slnStrings.SLN.values

    mols = pd.read_csv(r'*.csv')
    # mols = mols.sample(n=10)

    pool = mp.Pool(4)
    mols = pool.map_async(getmol, mols.SMILES).get()
    pool.close()
    pool.join()

    # mols = [getmol(smi) for smi in mols.SMILES]
    limits = list(map(getNum, slnStrings))

    Filter = SlnFilter(slnStrings)
    Filter.run(mols, limits=limits)
    print(Filter.filterResult)