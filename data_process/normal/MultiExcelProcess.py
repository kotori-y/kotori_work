# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 16:38:55 2019

You are not expected to understand my codes!

@Author: Kotori_Y
@Blog: blog.moyule.me
@Weibo: Michariel
@Mail: yzjkid9@gmial.com

I love Megumi forerver!
"""

print(__doc__)

#xlsfile = r"C:\Users\0720\Documents\Tencent Files\1223821976\FileRecv\stardrop.xlsx"
#book = xlrd.open_workbook(xlsfile) 
#
#os.chdir(r'C:\Users\0720\Desktop\Sorcha\data_set')
#for sheet in book.sheets():
#    inchikeys = []
#    df = pd.read_excel(xlsfile,sheet.name)
#    for smi in list(df['SMILES']):
#        mol = Chem.MolFromSmiles(smi)
#        inchikeys.append(Chem.MolToInchiKey(mol))
#    df['InchiKey'] = inchikeys
#    df.to_csv(sheet.name+'.csv',index=False)
#    
#    
#     







#df = pd.read_excel(r"C:\Users\0720\Desktop\demodemo.xlsx")
#col = df.columns
#
#
##def dudulu(x,y):
#os.chdir(r'C:\Users\0720\Desktop\MATE\Sorcha\IDK')
#
#files = os.listdir()
#
#for file in tqdm(files):
#    W = pd.ExcelWriter(file)
#    book = xlrd.open_workbook(file)
#    n = 0
#    for sheet in book.sheets():
#        n += 1
#        df = pd.read_excel(file,sheet.name)
#        print(file+ ' ' + sheet.name+' read' + str(n))
#    #        
#    #        mean_e = df.ele.mean()
#    #        var_e = df.ele.var()
#    #        
#    #        mean_p = df.pha.mean()
#    #        var_p = df.pha.std()
#    #        
#    #        df['z-score_ele'] = df['ele'].map(lambda x: (x-mean_e)/var_e)
#    #        df['z-score_pha'] = df['pha'].map(lambda x: (x-mean_p)/var_p)
#    #        df['z-score'] = df.apply(lambda x: x['z-score_ele'] + x['z-score_pha'], axis=1)
##        
#        df.sort_values('z-score',ascending=False)
#        df.to_excel(W,sheet_name=sheet.name,index=False)
#    W.save()
#            
#            
##t1 = threading.Thread(target=dudulu,args=(0,6))           
##t2 = threading.Thread(target=dudulu,args=(6,12))      
##t3 = threading.Thread(target=dudulu,args=(12,18))
##t4 = threading.Thread(target=dudulu,args=(18,26))
##      
##t = [t1,t2,t3,t4]
##
##for i in t:
##     i.start()
##i.join()
##        
##        
##        
##        
#os.chdir(r'C:\Users\0720\Desktop\MATE\Sorcha\all')
#
#def SplitExcel(files):
#    #loop file
#    for file in tqdm(files):
#        #read the mother-table
#        df = pd.read_excel(file)
#        lim = len(df)/500
#        
#        df_i = df.copy()
#        df_i.sort_values('z-score', ascending=False, inplace=True)
#        
#        #creat new excel
#        W = pd.ExcelWriter(file)
#        
#        n = 0
#        df_i.to_excel(W,sheet_name='sheet_0',index=False)
#        
#        while True:
#            df[n*500:(n+1)*500:].to_excel(W,sheet_name='sheet_'+str(n+1),index=False)
#            n += 1
#            if n == lim:
#                break
#            else:
#                pass
#        W.save()
#        
        
import pandas as pd
import numpy as np
import os
import xlrd
from tqdm import tqdm
import threading

def split(file):
    
    df = pd.read_csv(file)
    length = len(df)
    
    
    
    b = 9999
    cut = [0]
    print('-----------------Find cutting point-----------------')
    for index in tqdm(range(length)):
        a = list(df['com2_Z'])[index]
        if a<=b:
            pass
        else:
            cut.append(index)
        b = a

    W = pd.ExcelWriter(file.replace('csv','xlsx'))
    df.to_excel(W,sheet_name='All',index=False)
    print('----------------------Splitting----------------------')
    mol = 0
    for index in tqdm(range(len(cut))):
        mol += 1
        v = df.copy()
        
        if index != len(cut)-1:
            v = v.iloc[cut[index]:cut[index+1],:]
        else:
            v = v.iloc[cut[index]:,:]
            
        ele_mean = v.ele.mean()
        ele_std = v.ele.std()
        v['ele_Z'] = v['ele'].map(lambda x: (x-ele_mean)/ele_std) 
        
        pha_mean = v.pha.mean()
        pha_std = v.pha.std()
        v['pha_Z'] = v['pha'].map(lambda x: (x-pha_mean)/pha_std)
        
        v['com2_Z'] = v.apply(lambda x:x['ele_Z']+x['pha_Z'],axis=1)
        
        v = v.sort_values('com2_Z',ascending=False)
        
        v.to_excel(W,sheet_name='Mol_{}'.format(mol),index=False)
    
    print('-----------------Saving Now-----------------')
    W.save()
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    