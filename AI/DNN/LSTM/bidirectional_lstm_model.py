# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 10:10:50 2020

@Author: Zhi-Jiang Yang, Dong-Sheng Cao
@Institution: CBDD Group, Xiangya School of Pharmaceutical Science, CSU, China
@Homepage: http://www.scbdd.com
@Mail: yzjkid9@gmail.com; oriental-cds@163.com
@Blog: https://blog.iamkotori.com

♥I love Princess Zelda forever♥
"""


import keras.backend as K
from keras.layers import Input, Dropout, BatchNormalization, Multiply
from keras.layers import Multiply, Lambda, RepeatVector, Bidirectional, Permute
from keras.layers.core import Dense, Flatten, Masking
from keras.layers.recurrent import LSTM
from keras.models import Model
from keras.optimizers import Adam, RMSprop
from keras.callbacks import EarlyStopping, TensorBoard, ModelCheckpoint, LambdaCallback

from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from mol_utils import smiles_to_hot, train_test_split
from attention import my_attention_vec

#####################
"""
UNITS
"""
LSTM_UNITS = 256
DENSE_UNITS = 256
#####################

#####################
"""
FITTING
"""
LR = 1e-3
DECAY = 1e-5
EPOCHS = 150
BATCH_SIZE = 128
####################

####################
"""
ONE_HOT
"""
PADDING = 'none'
SMILES_FIELD = 'Canonical_NoISO'
LABEL_FIELD = 'logD'
MAX_LEN = 80
RANDOM_STATE = 777
####################

####################
"""
ATTENTION
"""
ATTENTION = True
####################

####################
"""
CALL_BACK
"""
TB_PATH = './tbCallBack/attention_after_lstm_00' #run tensorboard --logdir=.\tbCallBack\attention_after_latm_xx
WEIGHTS_PATH = './weights/weights00/weights.{epoch:02d}-{val_r2_keras:.2f}.hdf5'
PATIENCE = 50
TEST_HISTORY = {}
####################

"""
INPUTS
"""
TIME_STEPS = 80
INPUT_DIM = 30



def build_bilstm_model():
    """
    """    
    # inputs.shape = (batch_size, time_steps, input_dim)
    _input = Input(shape = (TIME_STEPS, INPUT_DIM))
    #mask
    mask = Masking()(_input)
    #bn
    bn = BatchNormalization(axis=2)(mask)
    #bi-lstm
    activations = Bidirectional(LSTM(LSTM_UNITS, return_sequences=True))(bn)
    #attention
    if ATTENTION:
        #attention
        attention = my_attention_vec(activations, LSTM_UNITS*2)
        #merge
        sent_representation = Multiply()([activations, attention])
        sent_representation = Lambda(lambda xin: K.sum(xin, axis=-2), output_shape=(LSTM_UNITS*2,))(sent_representation)
        
        probabilities = Dense(1)(sent_representation)
    else:
        probabilities = Dense(1)(activations)

    # output = Dense(DENSE_UNITS, activation='relu')(attention_mul)
    # output = Dropout(0.5)(output)

    # output = Dense(1)(output)
    
    model = Model(input=_input, output=probabilities)
    adam = Adam(lr=LR, decay=DECAY)
#    rmsprop = RMSprop(lr=LR, decay=DECAY)
    model.compile(optimizer=adam, loss='mse', metrics=[r2_keras])
    
    return model
    

def r2_keras(y_true, y_pred):
    SS_res =  K.sum(K.square(y_true - y_pred)) 
    SS_tot = K.sum(K.square(y_true - K.mean(y_true))) 
    return ( 1 - SS_res/(SS_tot + K.epsilon()) )  
    
def test_r2(epoch, logs):
    """
    """
    y_pred = m.predict(X_test)
    
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    res = dict(zip(('loss','mae','r2'), (mse, mae, r2)))
    TEST_HISTORY[epoch] = res
    print(res)
  


if '__main__' == __name__:
    
    
    
    m = build_bilstm_model()
    m.summary()
    
    
    
#    early_stopping = EarlyStopping(monitor='val_loss', patience=PATIENCE, mode='min')
#    tbCallBack = TensorBoard(log_dir=TB_PATH)
#    checkpoint = ModelCheckpoint(WEIGHTS_PATH, save_best_only=True)
#    lck = LambdaCallback(on_epoch_end=test_r2)
#    
#    history = m.fit([X_train], y_train, epochs=EPOCHS,
#                    batch_size=BATCH_SIZE, validation_data=(X_val, y_val),
#                    callbacks=[early_stopping, tbCallBack, lck]
#                    )
#    
#    
#    
#    
        