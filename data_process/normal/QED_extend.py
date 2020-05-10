# -*- coding: utf-8 -*-
"""
Created on Mon May 13 09:44:00 2019

@Author: CBDD Group, CSU, China
@Homepage: http://www.scbdd.com
@Mail: yzjkid9@gmail.com
@Blog: https://blog.moyule.me

♥I love Megumi forerver♥
"""

print (__doc__)

import pandas as pd
from math import e as ex
from math import log
from tqdm import tqdm
from math import exp

#
#def dfunc(x,a,b,c,d,e,f,dmax):
#    
#    part_one = (-(x-c+(d/2))/e)
#    part_one = 1 + ex**part_one
#    part_one = b/part_one
#    
#    part_two = (-(x-c-(d/2))/f)
#    part_two = 1 + ex**part_two
#    part_two = 1 - (1/part_two)
#    
#    res = a + part_one*part_two
#    
#    res = res/dmax
#    
#    return res


def ADS(x,a,b,c,d,e,f,max_val):
     
    y = a+(b/(1+exp(-(x-c+d/2)/e)))*(1-1/(1+exp(-(x-c-d/2)/f))) #[ADS]
    y = y/max_val
    return y



def SDS(x,a,b,c,d,e,max_val):
    
    y = a+b*(1+exp(-d/(2*e)))*(1+exp(d/(2*e)))*exp(-(x-c)/e)/((1+exp(-((x-c+d/2)/e)))*(1+exp(-((x-c-d/2)/e)))) #[SDS]
    y = y/max_val
    return y



def QED(data):
    di = 0
    n = 7

        
    for key,value in data.items():
#        n += 1
        max_val = param['Max_val'][key]
        a = param['a'][key]
        b = param['b'][key]
        c = param['c'][key]
        d = param['d'][key]
        e = param['e'][key]
        f = param['f'][key]
        try:
            if f != 0:            
                di += log(ADS(value,a,b,c,d,e,f,max_val))
            
            else:
                di += log(SDS(value,a,b,c,d,e,max_val))
        except:
            di += 0
    try:
        res = exp(di/n)
    except:
        res = 0
    
    return res



if '__main__' == __name__:
#    file = input("Input file path:\n")
#    ads_param = pd.read_csv(r"C:\Users\0720\Desktop\MATE\yzy\QED_test\20190522\ADS_param.csv",index_col='X')
#    param = ads_param.to_dict()
#    sds_param = pd.read_csv(r"C:\Users\0720\Desktop\MATE\yzy\QED_test\20190522\SDS_param.csv",index_col='X')
#    param.update(sds_param.to_dict())
    
    param = pd.read_csv(r"",index_col='X')
    param.fillna(0,inplace=True)
    param = param.to_dict()
    
    df = pd.read_csv(r"")
    df['Label'] = 1
    df_i = df.copy()
    df_i.drop(['Label','Smiles'],axis=1,inplace=True)
    data = df_i.apply(lambda x: x.to_dict(),axis=1)
    df['QED'] = data.map(QED)
    #df['QEDw'] = data.map(QEDw)
    
    

    
def QEDw(data):
    di = 0
    W = 4.2
    
    try:
        for key,value in data.items():
    #        n += 1
            a = param['a'][key]
            b = param['b'][key]
            c = param['c'][key]
            d = param['d'][key]
            e = param['e'][key]
            f = param['f'][key]
            dmax = param['d(x)MAX'][key]
            weight = param['weight'][key]
            
            di += weight*log(dfunc(value,a,b,c,d,e,f,dmax))
        res = ex**(di/W)
    except:
       res = 0
    
    return res