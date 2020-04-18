# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 10:46:46 2019

@Author: Zhi-Jiang Yang, Dong-Sheng Cao
@Institution: CBDD Group, Xiangya School of Pharmaceutical Science, CSU, China
@Homepage: http://www.scbdd.com
@Mail: yzjkid9@gmail.com; oriental-cds@163.com
@Blog: https://blog.moyule.me

♥I love Zelda Princess forever♥
"""

import pandas as pd
import os
import requests
from lxml import etree
import multiprocessing

def getuni(file):
    """
    """
    print('{} start'.format(file))
    proxies = {"http": "http://58.218.10.49:808",
               "http": "http://58.241.58.115:808",
               "http": "http://114.239.145.255:808"} 
    unil = []
    df = pd.read_csv(file)
    targets = list(set(df['Target']))
    s = requests.Session()
    for target in targets:
        try:
            request_url = 'https://www.uniprot.org/uniprot/?query={}&sort=score'.format(target.replace(' ','+'))
            r = s.get(request_url,timeout=60,proxies=proxies)
            if r.status_code == 200:
                html = r.text
                html = etree.HTML(html)
                uni = html.xpath('//*[@class="grid"]/tbody/tr[1]/@id')
                if uni:
                    uni = uni[0]
                else:
                    uni = None
            else:
                uni = None
        except:
            uni = None
        print('{}: {}'.format(target,uni))
        unil.append(uni)
    df_i = pd.DataFrame({'Target':targets,'Uniprot':unil})
    df = pd.merge(df,df_i,how='left',on='Target')
    df.to_csv(file,index=False,sep=',')
    print('{} finished'.format(file))

#
if '__main__' == __name__:
    
    os.chdir(r'.\data')
#    try:
#        os.makedirs(r'Uni')
#    except:
#        pass
    files = os.listdir()
    pool = multiprocessing.Pool(6)
    for i in range(6):
        pool.apply_async(getuni,args=(files[i],))   
    pool.close()
    pool.join()