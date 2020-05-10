# -*- coding: utf-8 -*-
"""
Created on Mon Dec 24 10:13:26 2018

You are not expected to understand my codes!

@author: Kotori_Y
@weibo: Kotori-Y
@mail: yzjkid9@gmial.com

I love Megumi forerver!
"""

from sklearn.metrics import classification_report
from sklearn.metrics import auc
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
from tqdm import tqdm
import seaborn as sns

print(__doc__)

############################################## INTRODUCTION ##############################################
#                                   0.确保待处理的csv文件真实Label列的列名为‘Label_True’,概率值的为‘P'(大写);    #
#                                   1.建立一个空文件夹，将待处理的文件放入此文件夹中;                            #
#                                   2.修改'os.chdir()'处中的绝对路径;                                       #
#                                   3.修改beta值;                                                        #
##########################################################################################################





os.chdir(r"C:\Users\0720\Desktop\MATE\ywl\Demo") #此处为csv文件的文件夹，确保此文件夹只有待处理的文件
#
#files = os.listdir()
#classes = []
#aucl =  {}
#tprls = {}
#fprls = {}
#
#for file in files:
#
#    df = pd.read_csv(file)
#    print(file + ' Start')
#
#    tprl = []
#    fprl = []
#    
#       
#    for n in tqdm(np.arange(0,1,0.01)):
#        
#        def trans(x):
#            if x['P'] > n:
#                return 1
#            else:
#                return 0
#        
#        vv = df.copy()
#        vv['Label_Pre'] = vv.apply(trans,axis=1)
#        
#        tp = len(vv[(vv['Label_Pre']==1)&(vv['Label_True']==1)])
#        fp = len(vv[(vv['Label_Pre']==1)&(vv['Label_True']==0)])
#        
#        tn = len(vv[(vv['Label_Pre']==0)&(vv['Label_True']==0)])
#        fn = len(vv[(vv['Label_Pre']==0)&(vv['Label_True']==1)])
#
#        tpr = tp/(tp+fn)
#        fpr = fp/(fp+tn)
#        tprl.append(tpr)
#        fprl.append(fpr)
#        
#        tprls[file.replace('.csv','')] = tprl
#        fprls[file.replace('.csv','')] = fprl
#        
#       
#    
#    aucl[file.replace('.csv','')] = auc(fprl,tprl)
#    classes.append(file.replace('.csv',''))
#    
#    print(file + ' over')
#                
#plt.figure(figsize=(15,15))
#colors = ['aqua', 'darkorange', 'cornflowerblue']
#for i, color in zip(classes, colors):
#    plt.plot(fprls[i], tprls[i], color=color, lw=4,
#             label='ROC-{0} (area={1:0.2f})'
#             ''.format(i, aucl[i]))
#    
#plt.xlim([0.0, 1.05])
#plt.ylim([0.0, 1.05])
#plt.xticks(fontsize=20)
#plt.yticks(fontsize=20)
#plt.xlabel('False Positive Rate',fontsize=24)
#plt.ylabel('True Positive Rate',fontsize = 24)
##plt.title('Receiver operating characteristic of different descriptors',fontsize = 28)
#plt.legend()
#plt.legend(loc="lower right",fontsize=18)
#
#ax = plt.gca()                                            # get current axis 获得坐标轴对象
#ax.spines['right'].set_color('none') 
#ax.spines['top'].set_color('none')         # 将右边 上边的两条边颜色设置为空 其实就相当于抹掉这两条边
#
#ax.spines['bottom'].set_linewidth(4)
#ax.spines['left'].set_linewidth(4)
#
#plt.savefig(r'C:\Users\0720\Desktop\ROC_Curve.png')
#plt.show()




files = os.listdir()
classes = []
fkls = {}
precisionl = {}
recalll = {}
index = {}
scorel = {}

for file in files:

    df = pd.read_excel(file)
    print(file + ' Start')
    fscorel = []
    precisions = []
    recalls = []
   
    for n in tqdm(np.arange(0,1.00,0.01)):
        
        def trans(x):
            if x['P(Label=1)'] > n:
                return 1
            else:
                return 0
        
        vv = df.copy()
        vv['Label_Pred'] = vv.apply(trans,axis=1)
        
        tp = len(vv[(vv['Label_Pred']==1)&(vv['Label']==1)])
        fp = len(vv[(vv['Label_Pred']==1)&(vv['Label']==0)])
        
        tn = len(vv[(vv['Label_Pred']==0)&(vv['Label']==0)])
        fn = len(vv[(vv['Label_Pred']==0)&(vv['Label']==1)])
        
        
        try:
            precision = tp/(tp+fp)
        except:
            pprecision = 0
            
        try:
            recall = tp/(tp+fn)
        except:
            recall = 0
            
        precisions.append(precision)
        recalls.append(recall)
        
        
        
        
        
        
        
        
        
        
        
        ######################################这里是beta值#################################
        
        
        
        beta = 0.05  
        
        
        
        
        
       ######################################这里是beta值#################################
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        fscore = ((1+beta**2)*precision*recall)/(beta**2*precision+recall)
        fscorel.append(fscore)
    
    index[file.replace('.csv','')] = fscorel.index(max(fscorel))
    scorel[file.replace('.csv','')] = max(fscorel)
        
    fkls[file.replace('.csv','')] = fscorel
    precisionl[file.replace('.csv','')] = precisions
    recalll[file.replace('.csv','')] = recalls
    classes.append(file.replace('.csv',''))
    
     
    
    
    print(file + ' over')
print('--------------------{}--------------------'.format(beta))
sns.set_style(style='darkgrid')  
plt.figure(figsize=(20,12.36))
x = np.arange(0,1.00,0.01)
colors = ['#ff7f24','#eead0e','#00b2ee','#bbbbbb','#080404','#ff4747','#a8ff56','#ff4ba6','#e8fd42','#b854ff']
for i, color in zip(classes, colors):
    plt.plot(x, fkls[i], color=color, lw=2,
             label='F Curve-{0} (best score ={1:0.2f}, threshold ={2:0.2f})'
             ''.format(i, scorel[i], (index[i])*0.01))

    plt.scatter(x[index[i]], scorel[i],s=100,color=color)
    
    plt.vlines(x[index[i]],0,scorel[i],colors = color, linestyles = "dashed")
    plt.hlines(scorel[i],0,x[index[i]],colors = color, linestyles = "dashed")
plt.xlim([0.0, 1.05])
plt.ylim([0.0, 1.05])
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.xlabel('Threshold',fontsize=24)
plt.ylabel('F{} score'.format(beta),fontsize = 24)
#plt.title('F0.5 score curve of different descriptors',fontsize = 30)
plt.legend()
plt.legend(fontsize=14)
ax = plt.gca()                                            # get current axis 获得坐标轴对象

ax.spines['right'].set_color('none') 
ax.spines['top'].set_color('none')         # 将右边 上边的两条边颜色设置为空 其实就相当于抹掉这两条边

ax.spines['bottom'].set_linewidth(4)
ax.spines['left'].set_linewidth(4)

#plt.savefig(r'C:\Users\0720\Desktop\MATE\lemon\Fscore_{}.pdf'.format(beta))
plt.show()



plt.figure(figsize=(20,12.36))
#colors = ['darkorange', 'cornflowerblue','aqua']
for i, color in zip(classes, colors):
    plt.plot(recalll[i], precisionl[i], color=color, lw=4,
             label='{0} (recall={1:0.2f}, precision={2:0.2f})'
             ''.format(i,recalll[i][index[i]],precisionl[i][index[i]]))
    plt.scatter(recalll[i][index[i]],precisionl[i][index[i]],s=150,color=color)
    plt.vlines(recalll[i][index[i]],0,precisionl[i][index[i]],colors = color, linestyles = "--")
    plt.hlines(precisionl[i][index[i]],0,recalll[i][index[i]],colors = color, linestyles = "--")
plt.xlim([0.0, 1.05])
plt.ylim([0.0, 1.05])
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.xlabel('Recall',fontsize=24)
plt.ylabel('Precision',fontsize = 24)
#plt.title('Recall-Precision relation',fontsize = 30)
plt.legend()
plt.legend(fontsize=14)
ax = plt.gca()                                            # get current axis 获得坐标轴对象

ax.spines['right'].set_color('none') 
ax.spines['top'].set_color('none')         # 将右边 上边的两条边颜色设置为空 其实就相当于抹掉这两条边

ax.spines['bottom'].set_linewidth(4)
ax.spines['left'].set_linewidth(4)

#plt.savefig(r'C:\Users\0720\Desktop\MATE\lemon\P-R_{}.pdf'.format(beta))
plt.show()


#



















































