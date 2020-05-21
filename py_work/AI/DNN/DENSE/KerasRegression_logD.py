# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 15:59:49 2019

@Author: Zhi-Jiang Yang, Dong-Sheng Cao
@Institution: CBDD Group, Xiangya School of Pharmaceutical Science, CSU, China
@Homepage: http://www.scbdd.com
@Mail: yzjkid9@gmail.com; oriental-cds@163.com
@Blog: https://blog.moyule.me

♥I love Zelda Princess forever♥
"""


from keras.models import Sequential
from keras.utils import to_categorical
from keras.optimizers import SGD
from keras.optimizers import Adam,RMSprop
from keras.layers import Dense, Dropout, Activation
from sklearn.model_selection import train_test_split,KFold
from sklearn.preprocessing import scale
#from sklearn.datasets import load_iris
import numpy as np
import pandas as pd
import os
from sklearn.metrics import r2_score,mean_squared_error,mean_absolute_error
from sklearn.preprocessing import StandardScaler
from keras import regularizers
import keras.backend as K
#import gc
#from sklearn.decomposition import PCA
from tqdm import tqdm
import warnings
warnings.filterwarnings("ignore")


#X_train,X_test,y_train,y_test = train_test_split(data,Y)

#kf = KFold(n_splits=5,shuffle=True,random_state=10)

#for train_index,test_index in kf.split(X):
#    print(train_index)

def buildnetwork():
    model = Sequential()
    model.add(Dense(512,activation='relu',input_dim=44,
    #                kernel_regularizer=regularizers.l2(0.01),
    #                activity_regularizer=regularizers.l1(0.01)
                    ))
#    model.add(Dropout(0.4))
    model.add(Dense(512,activation='relu'))
#    model.add(Dropout(0.4))
    model.add(Dense(512,activation='relu'))
#    model.add(Dropout(0.4))
    model.add(Dense(512,activation='relu'))
#    model.add(Dropout(0.4))
    model.add(Dense(256,activation='relu'))
#    model.add(Dropout(0.4))
    model.add(Dense(256,activation='relu'))
#    model.add(Dropout(0.4))
    model.add(Dense(256,activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1))

    adam = Adam(lr=1e-4, decay=1e-5)
    rmeprop = RMSprop(lr=1e-4)
    model.compile(
            loss='mse'
            ,optimizer=adam
            ,metrics=['mae']
            )
    return model

#now is best
def buildnetwork_2():
    model = Sequential()
    model.add(Dense(512,activation='relu',input_dim=44,
    #                kernel_regularizer=regularizers.l2(0.01),
    #                activity_regularizer=regularizers.l1(0.01)
                    ))
#    model.add(Dropout(0.4))
    model.add(Dense(512,activation='relu'))
#    model.add(Dropout(0.4))
    model.add(Dense(512,activation='relu'))
##    model.add(Dropout(0.4))
#    model.add(Dense(512,activation='relu'))
##    model.add(Dropout(0.4))
#    model.add(Dense(512,activation='relu'))
#    model.add(Dropout(0.4))
#    model.add(Dense(256,activation='relu'))
#    model.add(Dropout(0.5))
#    model.add(Dense(256,activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1))

    adam = Adam(lr=1e-3, decay=1e-5)
    rmeprop = RMSprop(lr=1e-4)
    model.compile(
            loss='mse'
            ,optimizer=adam
            ,metrics=['mae']
            )
    return model


def buildnetwork_3():
    model = Sequential()
    model.add(Dense(512,activation='relu',input_dim=44,
    #                kernel_regularizer=regularizers.l2(0.01),
    #                activity_regularizer=regularizers.l1(0.01)
                    ))
#    model.add(Dropout(0.4))
    model.add(Dense(512,activation='relu'))
#    model.add(Dropout(0.4))
    model.add(Dense(512,activation='relu'))
##    model.add(Dropout(0.4))
#    model.add(Dense(512,activation='relu'))
##    model.add(Dropout(0.4))
#    model.add(Dense(512,activation='relu'))
#    model.add(Dropout(0.4))
#    model.add(Dense(256,activation='relu'))
#    model.add(Dropout(0.5))
#    model.add(Dense(256,activation='relu'))
    model.add(Dropout(0.6))
    model.add(Dense(1))

    adam = Adam(lr=1e-3, decay=1e-5)
    rmeprop = RMSprop(lr=1e-4)
    model.compile(
            loss='mse'
            ,optimizer=adam
            ,metrics=['mae']
            )
    return model


def crossvalid(X,y,n_splits=5,epochs=500):
    smis = X.pop('SMILES')
    smil,y_predl = [],[]
#    rmsel,r2l,mael = [],[],[]
    n = 0
    kf = KFold(n_splits=n_splits,shuffle=True,random_state=10)
    for train_index,test_index in kf.split(X):
        n += 1
        print('Fold_{}'.format(n))
        model = buildnetwork_2()
        Scaler = StandardScaler()
        X_train,X_test = X.iloc[train_index],X.iloc[test_index]
        y_train,y_test = y[train_index],y[test_index]
        smil.extend(smis[test_index])
        Scaler.fit(X_train)
        X_train = Scaler.transform(X_train)
        X_test = Scaler.transform(X_test)
        print('>>>Fitting')
        model.fit(X_train,y_train,epochs=epochs,batch_size=128,validation_data=(X_test,y_test),verbose=0)
        y_pred = model.predict(X_test)
#        rmsel.append(mean_squared_error(y_test,y_pred)**0.5)
#        r2l.append(r2_score(y_test,y_pred))
#        mael.append(mean_absolute_error(y_test,y_pred))
        print(r2_score(y_test,y_pred))
        y_predl.extend(list(y_pred))
        del model,Scaler
    data = pd.DataFrame({'SMILES':smil,'y_pred':y_predl})
    return data

def valid(X,y):
    X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=10)
    X_train,X_valid,y_train,y_valid = train_test_split(X_train,y_train,test_size=0.25,random_state=10)
    Scaler = StandardScaler()
    Scaler.fit(X_train)
    X_train = Scaler.transform(X_train)
    X_test = Scaler.transform(X_test)
    X_valid = Scaler.transform(X_valid)
    model = buildnetwork_2()
    history = model.fit(X_train,y_train,epochs=500,batch_size=128,validation_data=(X_valid,y_valid))
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test,y_pred)
    rmse = mean_squared_error(y_test,y_pred)
    mae = mean_absolute_error(y_test,y_pred)
    print(r2,rmse,mae)
    return history
    
def test(X,y,train_index,test_index,epochs=370,batch_size=128,verbose=0):    
    X_train,X_test = X[train_index],X[test_index]
    y_train,y_test = y[train_index],y[test_index]
    Scaler = StandardScaler()
    Scaler.fit(X_train)
    X_train = Scaler.transform(X_train)
    X_test = Scaler.transform(X_test)
    model = buildnetwork_2()
    print('>>>Fitting...')
    model.fit(X_train,y_train,epochs=epochs,batch_size=batch_size,verbose=verbose)
    print('>>>Predicting...')
    y_pred = model.predict(X_test)
    rmse = round(mean_squared_error(y_test,y_pred)**0.5,3)
    r2 = round(r2_score(y_test,y_pred),3)
    mae = round(mean_absolute_error(y_test,y_pred),3)
    print('{}  {}  {}'.format(rmse,r2,mae),end='\n\n')
    del model,Scaler
    return y_pred
    

def pred(X_train,X_test,y_train,y_test=None,epochs=370,batch_size=128):
    model = buildnetwork_2()
    print('>>>Fitting')
    model.fit(X_train,y_train,verbose=0,epochs=epochs,batch_size=batch_size)
    print('>>>Predicting')
    y_pred = model.predict(X_test)
    return y_pred



if '__main__' == __name__:
    out = pd.DataFrame()
    os.environ["CUDA_VISIBLE_DEVICES"] = "1,2,3,4"
#    data = pd.DataFrame()
    os.chdir(r'**')
    X = pd.read_csv(r"**")
    X.drop(['Inchkey','SMILES'],axis=1,inplace=True)
    y = X.pop('LogD7.4')
    
#    X = np.array(X)
    df = pd.read_csv(r"Sample_logD.csv")
    df = df.applymap(lambda x: [False,True][x])
    
    for idx in df.index:
        turn = idx+1
        print('----------Turn: {}----------'.format(turn))
        IDX = df.loc[idx].values
        train_index = ~IDX
        test_index = IDX
        y_pred = test(X,y,train_index,test_index)
        out['Turn_{}'.format(turn)] = list(y_pred.flatten())
        out.to_csv('DNN_out.csv',index=False,sep=',')
#    for n in range(100):
#        print('--------------Turn: {}--------------'.format(n+1))
#        test_index = list(idx[idx['Label']==n]['index'])
#        train_index = list(set(IDX)-set(test_index))
#        y_pred = test(X,y,train_index,test_index)
#        data['X_{}'.format(n+1)] = list(y_pred)
#        
   
#    y_pred = pred(X_train,X_test,y_train)


    
##    history = valid(X,y)
##    metric_dic = history.history
#    a,b,c = crossvalid(X,y,epochs=370)
