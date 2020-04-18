# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 21:46:41 2019

You are not expected to understand my codes!

@Author: Kotori_Y
@Blog: blog.moyule.me
@Weibo: Kotori-Y
@Mail: yzjkid9@gmail.com

I love Megumi forerver!
"""

print(__doc__)

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split,KFold
from sklearn.metrics import accuracy_score,precision_score,recall_score
import pandas as pd
import time
import os
from tqdm import tqdm

kf = KFold(n_splits=5)#kfold


start = time.clock()

#os.chdir(r'E:\student\yzy\Importance')
#files = os.listdir()
#os.makedirs('FeatureAna')

#df = df.sample(frac=1).reset_index(drop=True)
#df.drop('SMILES',axis=1,inplace=True)
#y = df.pop('Label')

#fold = 0


####################################### 5-Fold #######################################

#df_i = pd.DataFrame()#creat a dataframe for importance
#df_m = pd.DataFrame()#creat a dataframe for metrics

#for train_index, test_index in kf.split(df):
#    col = list(df.columns)
#    fold += 1
#    X_train, x_test = df.iloc[train_index], df.iloc[test_index]
#    Y_train, y_test = y.iloc[train_index], y.iloc[test_index]
#    X = X_train.copy()
#    x = x_test.copy()
#    
#    for _ in tqdm(range(len(df.columns))):
#        
#        rfc = RandomForestClassifier(n_estimators=500,n_jobs=-1)
##        print('----------------Fitting----------------')
#        rfc.fit(X,Y_train)
#       
#        fea = pd.DataFrame(
#                {
#                 'Feature':col,
#                 'Importance':rfc.feature_importances_,
#                 'Fold':'fold_{}'.format(fold),
#                 'Class':len(col)
#                         }
#                )
#        fea.sort_values('Importance',ascending=False,inplace=True)
#        df_i = pd.concat([df_i,fea],ignore_index=True)
#       
#        #cal correlate metrics
#        acc = accuracy_score(y_test,rfc.predict(x))
#        pre = precision_score(y_test,rfc.predict(x))
#        rec = recall_score(y_test,rfc.predict(x))
#        
#        me = pd.DataFrame(
#                {
#                 'Precision':[pre],
#                 'Recall':[rec],
#                 'Accuracy':[acc],
#                 'Fold':['fold_{}'.format(fold)],
#                 'Class':[len(col)]
#                        }
#                )    
#        df_m = pd.concat([df_m,me],ignore_index=True)
#        
#        #drop the most unimportant feature
#        drop = list(fea['Feature'])[-1]
#        
#        X.drop(drop,axis=1,inplace=True)
#        x.drop(drop,axis=1,inplace=True)
#        col.remove(drop)
#       
#        del rfc,fea,me
#    
#    
#end = time.clock()
#
#print(end-start)
#
#df_i.to_csv('Importances.csv')
#df_m.to_csv('Metrics.csv')

###########################################################################################












####################################### ONCE #######################################
def Selection(file,filepath):
    os.chdir(filepath)
    print('-----{} start-----'.format(file.replace('.csv','')))
    df_i = pd.DataFrame()#creat a dataframe for importance
    df_m = pd.DataFrame()#creat a dataframe for metrics
    
    #df_1 = pd.read_csv(r'E:\student\kotori\Lemon\backup\2C9_In_MACCS-1.csv')
    #df_0 = pd.read_csv(r'E:\student\kotori\Lemon\backup\2C9_In_MACCS-0.csv')
    #df_1 = df_1.sample(len(df_0),replace=True)
    #df = pd.concat([df_1,df_0],ignore_index=True,sort=False)
    
    df = pd.read_csv(file)
    df = df.sample(frac=1).reset_index(drop=True)
#    df = df.iloc[:,3:]
#    try:
#        df.drop('SMILES',axis=1,inplace=True)
#    except:
#        df.drop('Smiles',axis=1,inplace=True)
    y = df.pop('grades')
    
    col = list(df.columns)
    X_train,x_test,Y_train,y_test = train_test_split(df,y,test_size=0.2)
    X = X_train.copy()
    x = x_test.copy()
    
    for _ in tqdm(range(len(df.columns))):
            
            rfc = RandomForestClassifier(n_estimators=500,n_jobs=-1)
    #        print('----------------Fitting----------------')
            rfc.fit(X,Y_train)
           
            fea = pd.DataFrame(
                    {
                     'Feature':col
                     ,'Importance':rfc.feature_importances_
       
                     ,'Class':len(col)
                             }
                    )
            fea.sort_values('Importance',ascending=False,inplace=True)
            df_i = pd.concat([df_i,fea],ignore_index=True,sort=False)
           
            #cal correlate metrics
            acc = accuracy_score(y_test,rfc.predict(x))
            pre = precision_score(y_test,rfc.predict(x))
            rec = recall_score(y_test,rfc.predict(x))
            
            me = pd.DataFrame(
                    {
                     'Precision':[pre]
                     ,'Recall':[rec]
                     ,'Accuracy':[acc]
                     #,'Fold':['fold_{}'.format(fold)]
                     ,'Class':[len(col)]
                            }
                    )    
            df_m = pd.concat([df_m,me],ignore_index=True,sort=False)
            
            #drop the most unimportant feature
            drop = list(fea['Feature'])[-1]
            
            X.drop(drop,axis=1,inplace=True)
            x.drop(drop,axis=1,inplace=True)
            col.remove(drop)
           
            del rfc,fea,me
    #file = '2C9_In_MACCS'
    #df_i.to_csv('FeatureAna/{}_Importances_oversampling.csv'.format(file),index=False)
    #df_m.to_csv('FeatureAna/{}_Metrics_oversampling.csv'.format(file),index=False)
    return df_i,df_m
    
def main():
    tempt = print("Input the absolute path of your file locate and ensure the file only contain 'SMILES', 'Label' and the features vector\n")
    filepath = input("The absolute path: ")
    files = os.listdir(filepath)
    for file in files:        
        df_i, df_m = Selection(file,filepath)
#        os.chdir(r'E:\student\yzy\All')
#        
#        part_1_class = list(range(1000,1717))
#        
#        df_i_a = df_i[df_i['Class'].isin(part_1_class)]
#        df_i_b = df_i[~df_i['Class'].isin(part_1_class)]
#        df_i.iloc[:,:].to_csv(file.replace('.csv','') + '_Importances.csv',index=False)
#        df_m.to_csv(file.replace('.csv','') + '_Metrics.csv',index=False)
        df_i.to_csv('{}_Importances.csv'.format(file.replace('.csv','')))

if '__main__' == __name__:    
    main()
              #,'Fold':'fold_{}'.format(fold)
