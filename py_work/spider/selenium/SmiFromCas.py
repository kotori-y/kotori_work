# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 17:27:07 2019

@Author: Kotori_Y
@Blog: blog.moyule.me
@Weibo: Kotori-Y
@Mail: yzjkid9@gmail.com
 
                 //
     \\         //
      \\       //
##DDDDDDDDDDDDDDDDDDDDDD##
## DDDDDDDDDDDDDDDDDDDD ##   
## hh                hh ##   
## hh    //    \\    hh ##   
## hh   //      \\   hh ##    
## hh                hh ##     
## hh      wwww      hh ##      
## hh                hh ##       
## MMMMMMMMMMMMMMMMMMMM ##
##MMMMMMMMMMMMMMMMMMMMMM##                             
     \/            \/


♥I love Megumi forerver♥
"""

print (__doc__)

from rdkit.Chem import AllChem as Chem
import pandas as pd
import datetime
import os
import csv
from selenium import webdriver
from lxml import etree
import numpy
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
from tqdm import tqdm
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

#options = webdriver.FirefoxOptions()
#options.add_argument('user-agent="Opera/12.02 (Android 4.1; Linux; Opera Mobi/ADR-1111101157; U; en-US) Presto/2.9.201 Version/12.02"')

profile = webdriver.FirefoxProfile()
profile.set_preference("browser.startup.homepage", "about:blank")
profile.set_preference("startup.homepage_welcome_url", "about:blank")
profile.set_preference("startup.homepage_welcome_url.additional", "about:blank")

desired_capabilities = DesiredCapabilities.FIREFOX  # 修改页面加载策略
desired_capabilities["pageLoadStrategy"] = "none"  # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出

driver = webdriver.Firefox(profile
                           ,executable_path = r"C:\Program Files\Mozilla Firefox\geckodriver.exe"
#                           ,firefox_options=options
                           )

def wait(xpath):
    Wait(driver,5).until(EC.presence_of_element_located(
            (By.XPATH,xpath)
            )
    )

def visit(cas): 
    url = 'http://www.chemnet.com/cas/supplier.cgi?terms={}\
    &l=&exact=dict&f=plist&mark=&submit.x=0&submit.y=0&submit=search'.format(cas.strip()
    )
    
    
    driver.get(url)
    try:
        wait(xpath='//*[@id="main-en"]/div[1]/table/tbody/tr/td/table/tbody/tr[5]/td[2]'
             )
        html = driver.page_source
        html = etree.HTML(html)
    
    except:
        html = None
        
    return html    
    
def InChiToSmiles(InChi):
    m = Chem.MolFromInchi(InChi)
    smi = Chem.MolToSmiles(m,canonical=True)
    return smi

def getSmiles(html):
    InChi = html.xpath('//*[@id="main-en"]/div[1]/table/tbody/tr/td/table/tbody/tr[5]/td[2]/text()')[0]
    smi = InChiToSmiles(InChi)
    return smi
  
def main(Casl):
    Smil = []
    for cas in tqdm(Casl):
        html = visit(cas)
        try:
            Smi = getSmiles(html)
        except:
            print(cas)
            Smi = None
        Smil.append(Smi)
        driver.get('about:blank')
        
        
    return Smil
            

if '__main__' == __name__:
    df = pd.read_excel(r"C:\Users\0720\Desktop\MATE\akuma\MOAs.xlsx")
    Casl = list(df['CAS'])
    Smil = main(Casl)    
    
    


 
    


