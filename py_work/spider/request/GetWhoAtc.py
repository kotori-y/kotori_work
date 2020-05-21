# -*- coding: utf-8 -*-
"""
Created on Sun Mar  8 11:49:05 2020

@Author: Zhi-Jiang Yang, Dong-Sheng Cao
@Institution: CBDD Group, Xiangya School of Pharmaceutical Science, CSU, China
@Homepage: http://www.scbdd.com
@Mail: yzjkid9@gmail.com; oriental-cds@163.com
@Blog: https://blog.moyule.me

@Doc: Get the WHO ATC code from pubchem (https://pubchem.ncbi.nlm.nih.gov/classification/#hid=79)

♥I love Princess Zelda forever♥
"""

import multiprocessing as mp
from lxml import etree
from requests import Session
import pandas as pd
import re


def getHNID(node):
    s = Session()
    try:
        url = 'https://pubchem.ncbi.nlm.nih.gov/classification/cgi/classifications.fcgi?format=jsonp&hid=79&depth=1&start=node_{}&child_max=100&callback=jQuery18303179896066565475_1583640150698'.format(node)
        response = s.post(url,timeout=5)    
        html = response.text
        name,hnid = re.findall('"Information": {.*"Name": "(.*?)"[\w\W]*?"HNID": (.*?)[\,|\n].*?}',html,re.S)[0]
        if len(re.findall('(.*?) - .*?',name)[0])==7:
            return name,hnid.strip()
        else:
            return None,None
    except:
        getHNID(node)
    
            
def getCID(HNID):
    s = Session()
    try:
        url = 'https://www.ncbi.nlm.nih.gov/pccompound?DbFrom=pchierarchy&Cmd=Link&Db=pccompound&LinkName=pchierarchy_pccompound&IdsFromResult={}'.format(HNID)
        response = s.get(url,timeout=10)        
        html = etree.HTML(response.content)
        cid = html.xpath('//*[@class="termtext"][text()="CID: "]/following-sibling::dd[1]/text()')
        return cid #a list
    except:
        getCID(HNID)


def extract(node,res):
    name,hnid = getHNID(node)
    print(name,hnid)
    if hnid:
        res[name] = '|'.join(getCID(hnid))


def main():
    res = mp.Manager().dict()
    pool = mp.Pool()
    for node in range(1,6231): #node_1 to node_6230
        pool.apply_async(extract,args=(node,res,))
    pool.close()
    pool.join()
    return res


if '__main__'==__name__:
    res = main()
    res = pd.DataFrame(dict(res),index=[0],columns='CID').T
    res.to_csv(r'./ATCData.csv')