# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 19:16:04 2020

@author: admin
"""

import os,math
import pandas as pd
import numpy as np
from keras.models import Model
from keras.layers import Input,Dense,Dropout,Average,Multiply,Concatenate
from keras.callbacks import TensorBoard
from keras.optimizers import Adam
import h5py


# parameter
os.chdir('E:\\student\\ysq\\PCM\\bindingDB\\DNN')
##########################################################
'''
dl_merge1:df_2d,df_proa
dl_merge2:df_2d,df_prob
dl_merge3:df_ecfp4,df_proa
dl_merge4:df_ecfp4,df_prob
dl_merge5:df_maccs,df_proa
dl_merge6:df_maccs,df_prob
不同的模型记得修改Ta的值
'''
Ta = 'dl_merge5'
##########################################################

def dl_merge1():
    proa_2d = Input(shape=(950,),name='2D_proa')
    x1 = Dense(512, activation='relu')(proa_2d)
    x1 = Dropout(0.5)(x1)
    x1 = Dense(256, activation='relu')(x1)
    x1 = Dropout(0.5)(x1)   
    x1 = Dense(64, activation='relu')(x1)
    x1 = Dropout(0.5)(x1)   
    x1 = Dense(1, activation='sigmoid')(x1)
    
    model = Model(inputs=proa_2d, outputs=x1)

    # summarize layers
    print(model.summary())
    # plot graph
#    plot_model(model, to_file=Ta+'.png')
    adam = Adam(lr = 1e-3, decay = 1e-5)
    model.compile(optimizer=adam,loss='binary_crossentropy', metrics=['accuracy'])    
    return model

def dl_merge2():
    prob_2d = Input(shape=(388,),name='2D_prob')
    x2 = Dense(256, activation='relu')(prob_2d)
    x2 = Dropout(0.5)(x2)
    x2 = Dense(96, activation='relu')(x2)
    x2 = Dropout(0.5)(x2)   
    x2 = Dense(1, activation='sigmoid')(x2)
    model = Model(inputs=prob_2d, outputs=x2)

    # summarize layers
    print(model.summary())
    # plot graph
#    plot_model(model, to_file=Ta+'.png')
    adam = Adam(lr = 1e-3, decay = 1e-5)
    model.compile(optimizer=adam,loss='binary_crossentropy', metrics=['accuracy'])    
    return model
    
def dl_merge3():
    proa_ecfp4 = Input(shape=(1786,),name='ECFP4_proa')
    x3 = Dense(512, activation='relu')(proa_ecfp4)
    x3 = Dropout(0.5)(x3)
    x3 = Dense(256, activation='relu')(x3)
    x3 = Dropout(0.5)(x3)  
    x3 = Dense(64, activation='relu')(x3)
    x3 = Dropout(0.5)(x3)  
    x3 = Dense(1, activation='sigmoid')(x3)
    
    model = Model(inputs=proa_ecfp4, outputs=x3)

    # summarize layers
    print(model.summary())
    # plot graph
#    plot_model(model, to_file=Ta+'.png')
    adam = Adam(lr = 1e-3, decay = 1e-5)
    model.compile(optimizer=adam,loss='binary_crossentropy', metrics=['accuracy'])    
    return model

def dl_merge4():
    prob_ecfp4 = Input(shape=(1224,),name='ECFP4_prob')
    x4 = Dense(512, activation='relu')(prob_ecfp4)
    x4 = Dropout(0.5)(x4)
    x4 = Dense(256, activation='relu')(x4)
    x4 = Dropout(0.5)(x4)
    x4 = Dense(64, activation='relu')(x4)
    x4 = Dropout(0.5)(x4)  
    x4 = Dense(1, activation='sigmoid')(x4)
    model = Model(inputs=prob_ecfp4, outputs=x4)

    # summarize layers
    print(model.summary())
    # plot graph
#    plot_model(model, to_file=Ta+'.png')
    adam = Adam(lr = 1e-3, decay = 1e-5)
    model.compile(optimizer=adam,loss='binary_crossentropy', metrics=['accuracy'])    
    return model
    
def dl_merge5():
    proa_maccs = Input(shape=(929,),name='MACCS_proa')
    x5 = Dense(512, activation='relu')(proa_maccs)
    x5 = Dropout(0.5)(x5)
    x5 = Dense(256, activation='relu')(x5)
    x5 = Dropout(0.5)(x5)  
    x5 = Dense(64, activation='relu', name='weight')(x5)
    x5 = Dropout(0.5)(x5)  
    x5 = Dense(1, activation='sigmoid')(x5)    
    model = Model(inputs=proa_maccs, outputs=x5)

    # summarize layers
    print(model.summary())
    # plot graph
#    plot_model(model, to_file=Ta+'.png')
    adam = Adam(lr = 1e-3, decay = 1e-5)
    model.compile(optimizer=adam,loss='binary_crossentropy', metrics=['accuracy'])    
    return model

def dl_merge6():
    prob_maccs = Input(shape=(367,), name='MACCS_prob')
    x6 = Dense(256, activation='relu')(prob_maccs)
    x6 = Dropout(0.5)(x6)
    x6 = Dense(128, activation='relu', name='weight')(x6)
    x6 = Dropout(0.5)(x6)  
    x6 = Dense(1, activation='sigmoid')(x6)
    model = Model(inputs=prob_maccs, outputs=x6)

    # summarize layers
    print(model.summary())
    # plot graph
#    plot_model(model, to_file=Ta+'.png')
    adam = Adam(lr = 1e-3, decay = 1e-5)
    model.compile(optimizer=adam,loss='binary_crossentropy', metrics=['accuracy'])    
    return model


def merge(UNIT_NUM=32):
    
    proa_2d = Input(shape=(950,),name='2D_proa')
    x1 = Dense(512, activation='relu')(proa_2d)
    x1 = Dropout(0.5)(x1)
    x1 = Dense(256, activation='relu')(x1)
    x1 = Dropout(0.5)(x1)   
    x1 = Dense(64, activation='relu')(x1)
    x1 = Dropout(0.5)(x1)
    x1 = Dense(UNIT_NUM, activation='relu')(x1)
    

    prob_2d = Input(shape=(388,),name='2D_prob')
    x2 = Dense(256, activation='relu')(prob_2d)
    x2 = Dropout(0.5)(x2)
    x2 = Dense(96, activation='relu')(x2)
    x2 = Dropout(0.5)(x2)
    x2 = Dense(UNIT_NUM, activation='relu')(x2)

    proa_ecfp4 = Input(shape=(1786,),name='ECFP4_proa')
    x3 = Dense(512, activation='relu')(proa_ecfp4)
    x3 = Dropout(0.5)(x3)
    x3 = Dense(256, activation='relu')(x3)
    x3 = Dropout(0.5)(x3)  
    x3 = Dense(64, activation='relu')(x3)
    x3 = Dropout(0.5)(x3)  
    x3 = Dense(UNIT_NUM, activation='relu')(x3)

    prob_ecfp4 = Input(shape=(1224,),name='ECFP4_prob')
    x4 = Dense(512, activation='relu')(prob_ecfp4)
    x4 = Dropout(0.5)(x4)
    x4 = Dense(256, activation='relu')(x4)
    x4 = Dropout(0.5)(x4)
    x4 = Dense(64, activation='relu')(x4)
    x4 = Dropout(0.5)(x4)    
    x4 = Dense(UNIT_NUM, activation='relu')(x4)
    
    
    proa_maccs = Input(shape=(929,),name='MACCS_proa')
    x5 = Dense(512, activation='relu')(proa_maccs)
    x5 = Dropout(0.5)(x5)
    x5 = Dense(256, activation='relu')(x5)
    x5 = Dropout(0.5)(x5)  
    x5 = Dense(128, activation='relu')(x5)   
    x5 = Dropout(0.5)(x5)  
    x5 = Dense(UNIT_NUM, activation='relu')(x5)
    
    
    prob_maccs = Input(shape=(367,), name='MACCS_prob')
    x6 = Dense(256, activation='relu')(prob_maccs)
    x6 = Dropout(0.5)(x6)
    x6 = Dense(128, activation='relu')(x6)
    x6 = Dropout(0.5)(x6)  
    x6 = Dense(UNIT_NUM, activation='relu')(x6)
    
    
    multiplied = Concatenate()([x1, x2, x3, x4, x5, x6])
    multiplied = Dropout(0.5)(multiplied)
    output = Dense(1, activation='sigmoid')(multiplied)
    
    model = Model(inputs=[proa_2d, prob_2d, proa_ecfp4, prob_ecfp4, proa_maccs, prob_maccs], outputs=output)

    # summarize layers
    print(model.summary())
    # plot graph
#    plot_model(model, to_file=Ta+'.png')
    adam = Adam(lr = 1e-3, decay = 1e-5)
    model.compile(optimizer=adam,loss='binary_crossentropy', metrics=['accuracy'])    
    return model
    
def GetX(file):
    h5f = h5py.File(file, 'r')
    X = h5f[file][:]
    return X

    

if "__main__" == __name__:
    m = merge()
    os.chdir(r"E:/student/ysq/PCM/bindingDB/data/mol_prot/nnn")
    X1 = GetX("X1.h5")
    X2 = GetX("X2.h5")
    X3 = GetX("X3.h5")
    X4 = GetX("X4.h5")
    X5 = GetX("X5.h5")
    X6 = GetX("X6.h5")
    label = GetX("y.h5")
    
#    X1.pop('label').values.reshape(-1, 1)
#    model6 = dl_merge6()
#    model6.fit(X6, y6, epochs=100)
#    
#    df5 = pd.read_csv(r"E:/student/ysq/PCM/bindingDB/DNN2/MACCS_proa_label.csv")
#    X5 = df5.iloc[:, 5:]
#    
#    X5 = np.array(X5)
#    model5 = dl_merge5()
#    model5.fit(X5, y5, epochs=100)

# Only use numeric columns

#df2 = pd.read_csv(r"E:/student/ysq/PCM/bindingDB/DNN2/MACCS_proa_label.csv")
#X_train = input_table.iloc[:,5:-2].copy()
#y_train = input_table.iloc[:,-2].copy()

#model = eval(Ta+'()')
#hist = model.fit(X_train, y_train,epochs=200, batch_size=128,shuffle=True,verbose=2,callbacks=[TensorBoard(log_dir='./temp/log')])
#model.save_weights('E:\\student\\ysq\\PCM\\bindingDB\\DNN'+'\\'+Ta+'_weights.h5')
#output_table = pd.DataFrame(y_train.copy())