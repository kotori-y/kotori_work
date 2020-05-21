# -*- coding: utf-8 -*-
"""
Created on Wed May 22 18:46:15 2019

@Author: CBDD Group, CSU, China
@Homepage: http://www.scbdd.com
@Mail: yzjkid9@gmail.com
@Blog: https://blog.moyule.me

♥I love Megumi forerver♥
"""

print (__doc__)

import requests
import pandas as pd
import time

def SEA(smi):

    start_url = 'http://sea.bkslab.org/search'
    
    headers = {
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
                }
    
    data = {
            'ref_type': 'library',
            'ref_library_id': 'default',
            'query_type': 'custom',
            'query_custom_targets_paste': smi,#Mol
            }
        
    s = requests.Session()
    response = s.post(url=start_url, headers=headers, data=data)
    page = s.get(response.url).text
    
    attemp = 0
    while 'pending' in page:
        time.sleep(15)
        page = s.get(response.url).text
        attemp += 1
        if attemp == 5:
            SEA(smi)
    
    df = pd.read_html(page)[0]

    return df






