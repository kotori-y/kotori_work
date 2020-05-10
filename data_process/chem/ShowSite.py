# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 22:27:54 2018

You are not expected to understand my codes!

@author: Kotori_Y
@weibo: Michariel
@mail: yzjkid9@gmial.com

I love Megumi forerver!
"""

import os
from rdkit.Chem import AllChem as Chem#Chem/AllChem为rdkit十分重要的类
from rdkit.Chem import Draw#画图
from rdkit.Chem.Draw import IPythonConsole#使分子在Ipython中显示
import time

def show(index,som=None,file=r"C:\Users\0720\Desktop\Sorcha\merged.sdf"):
    """index，int型，为查询分子在sdf中的顺序；som，int型，为待查询的原子序号；file，str型，为所查询sdf文件的绝对路径"""
    start = time.clock()
    suppl = Chem.SDMolSupplier(file)#读取含多个分子的sdf文件，若只含一个分子使用Chem。Chem.MolFromMolFile(**.sdf)

    m = suppl[index-1]#获取目标分子，从0开始计数
    
    try:#判断是否传入int型的som
        atom = m.GetAtomWithIdx(som-1)#获取目标原子，使用.GetAtomWithIdx(*)函数
        print('The atom of som: ' + atom.GetSymbol() + '\n')#获取原子符号，使用.GetSymbol(*)函数
        
        neighbors = [x.GetIdx() for x in atom.GetNeighbors()]#获取目标原子的相邻原子，使用.GetNeighbors(*)。并且获得相邻原子的标号，使用.GetIdx(*)函数
        
        for neighbor in neighbors:#对相邻原子进行遍历
            print('The neighbor of som: ' + m.GetAtomWithIdx(neighbor).GetSymbol(),end = ' ')
            print('The bondtype between them: ',end ='') 
            print(m.GetBondBetweenAtoms(neighbor,som-1).GetBondType())#获取目标原子与相邻原子的键的类型，使用.GetBondBetweenAtoms(*)及GetBondType(*)
        neighbors.append(som-1)#将目标原子加入相邻原子列表中，用于高亮显示
    except:
        neighbors = []
    
    try:
        print('\nThe info of drug you searched: '+ str(m.GetPropsAsDict())+'\n')
    except:
        pass
       
    global mol
    mol = Chem.MolFromSmiles(Chem.MolToSmiles(m))
    
    pic = Draw.MolToImage(m,highlightAtoms=neighbors,size=(600,600),fitImage=True)
    end = time.clock()
    print(end - start)
    return pic

