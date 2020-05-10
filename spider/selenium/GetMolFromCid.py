# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 21:23:53 2019

@Author: CBDD Group, CSU, China
@Homepage: http://www.scbdd.com
@Mail: yzjkid9@gmail.com
@Blog: https://blog.moyule.me

♥I love Megumi forerver♥
"""

print (__doc__)

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
import time
#options = webdriver.FirefoxOptions()
#options.add_argument('user-agent="Opera/12.02 (Android 4.1; Linux; Opera Mobi/ADR-1111101157; U; en-US) Presto/2.9.201 Version/12.02"')

profile = webdriver.FirefoxProfile()
profile.set_preference("browser.startup.homepage", "about:blank")
profile.set_preference("startup.homepage_welcome_url", "about:blank")
profile.set_preference("startup.homepage_welcome_url.additional", "about:blank")

desired_capabilities = DesiredCapabilities.FIREFOX  # 修改页面加载策略
desired_capabilities["pageLoadStrategy"] = "none"  # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出

driver = webdriver.Firefox(profile
                           ,executable_path = r"~/geckodriver.exe"
#                           ,firefox_options=options
                           )

def excute(xpath,func):
    while True:
        try:
            Wait(driver,30).until(EC.presence_of_element_located(
                    (By.XPATH,xpath)
                    )
            )
            break
        except:
            pass
    func

def wait(xpath):
    Wait(driver,5).until(EC.presence_of_element_located(
            (By.XPATH,xpath)
            )
    )


def remove(xpath):
    
    Wait(driver,60).until(
            EC.staleness_of(
                    driver.find_element(By.XPATH,xpath)
                    )
            )
   
def switchframe(xpath):
    
    Wait(driver,30).until(
    EC.frame_to_be_available_and_switch_to_it(
            (By.XPATH, xpath)
            )
    )
   
#the action of clicking
def click(xpath):
    driver.find_element_by_xpath(xpath).click(
            )

#the action of sending
def send_keys(xpath,keys):
    driver.find_element_by_xpath(xpath).clear(
            )
    driver.find_element_by_xpath(xpath).send_keys(keys
                                )


def visit(url):
    driver.get(url)
    
    
if '__main__' == __name__:
    #smil = []
    #df = pd.read_csv(r"C:\Users\0720\Desktop\MATE\akuma\data06200846.csv")
    df = df.fillna(0)
    for idx in tqdm(df.index):
        if df.loc[idx,'SMILES'] == 0:
            cid = df.loc[idx,'cid']
            try:
                url = 'https://pubchem.ncbi.nlm.nih.gov/compound/{}'.format(cid)
                visit(url)
                wait(xpath='//*[@id="Canonical-SMILES"]')
                html = driver.page_source
                html = etree.HTML(html)
                smi = html.xpath('//*[@id="Canonical-SMILES"]//*[@class="section-content-item"]')[0].xpath('string(.)')
            except:
                smi = None
            df.loc[idx,'SMILES'] = smi
            print(smi)
        else:
            pass
        
        driver.get('about:blank')
        
#        smil.append(smi)
#    df['SMILES'] = smil

            
        
        
        
                
                
                
                
                
                
                
                
                
                
    