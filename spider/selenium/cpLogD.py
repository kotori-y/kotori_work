# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 15:42:14 2019

You are not expected to understand my codes!

@Author: Kotori_Y
@Blog: blog.moyule.me
@Weibo: Michariel
@Mail: yzjkid9@gmial.com

I love Megumi forerver!
"""

print(__doc__)

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
                           ,executable_path = r"~/geckodriver.exe"
#                           ,firefox_options=options
                           )


def wait(xpath):
    Wait(driver,30).until(EC.presence_of_element_located(
            (By.XPATH,xpath)
            )
    )

def re(xpath):
    
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
    
def query(smi,confidence):
    while True:
        try:
            send_keys(xpath='//*[@id="operations-Predict-logdGet"]/div[2]/div/div[2]/div[2]/table/tbody/tr[2]/td[2]/input',keys=smi)
            send_keys(xpath='//*[@id="operations-Predict-logdGet"]/div[2]/div/div[2]/div[2]/table/tbody/tr[3]/td[2]/input',keys=confidence)
            click(xpath='//*[@class="btn execute opblock-control__btn"]')
            wait(xpath='//*[@class="response"]//*[@class="col response-col_status"]')
            break
        except:
            pass
        
    
    html = driver.page_source
    html = etree.HTML(html)
    
    status = html.xpath('//*[@class="response"]//*[@class="col response-col_status"]/text()')[0]
    if status == '200':
    
        result = html.xpath('//*[@class=" microlight"]/span/text()')
        result = ''.join(result)
        result = eval(result)
        
        pred = result['predictionMidpoint']
        
        
    else:
        pred = 'N/A'
    
    click(xpath='//*[@class="btn btn-clear opblock-control__btn"]')
    time.sleep(1)
    
    print(pred)
    
    return pred
    
    
def main():
    
    resd = dict()
    
    df = pd.read_csv(r"~/External_validation_set83.csv")
    
    while True:
        try:
            driver.get('https://cplogd.service.pharmb.io/#/Predict/logdGet'
                       )
            wait(xpath='//*[@class="btn try-out__btn"]')
            break
        except:
            pass
    
    click(xpath='//*[@class="btn try-out__btn"]')

    
    wait(xpath='//*[@id="operations-Predict-logdGet"]/div[2]/div/div[2]/div[2]/table/tbody/tr[2]/td[2]')
    
    for con in [0.8,0.9]:
        con = str(con)
        resl = list()
        for smi in tqdm(df['SMILES']):
           resl.append(query(smi,con)) 
        
        resd[con] = resl
    
    return resd
    
    
if '__main__' == __name__:
    Result = main()
        
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            



