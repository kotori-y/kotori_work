# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 09:10:20 2019

You are not expected to understand my codes!

@Author: Kotori_Y
@Blog: blog.moyule.me
@Weibo: Michariel
@Mail: yzjkid9@gmial.com

I love Megumi forerver!
"""

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


profile = webdriver.FirefoxProfile()
profile.set_preference("browser.startup.homepage", "about:blank")
profile.set_preference("startup.homepage_welcome_url", "about:blank")
profile.set_preference("startup.homepage_welcome_url.additional", "about:blank")

desired_capabilities = DesiredCapabilities.FIREFOX  # 修改页面加载策略
desired_capabilities["pageLoadStrategy"] = "none"  # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出

driver = webdriver.Firefox(profile,executable_path = r"~/geckodriver.exe")

def wait(xpath):
    Wait(driver,30).until(EC.presence_of_element_located(
            (By.XPATH,xpath)
            )
    )
    
driver.get('https://www.vmall.com/'
           )

while True:
    try:
        xpath = '//*[@id="top-index-loginUrl"]'
        wait(xpath
             )
        time.sleep(3)
        driver.find_element_by_xpath(xpath).click(
                                             )
        break
    except:
        driver.refresh()
        
        
time.sleep(30)

js='window.open("https://www.vmall.com/product/10086689592595.html");'
driver.execute_script(js)#访问所需property的URL
handles = driver.window_handles
driver.switch_to_window(handles[-1])

while True:

    nowTime=datetime.datetime.now().strftime('%H:%M')#现在
    if nowTime == '10:07':
        time.sleep(10)
        driver.refresh()
    if nowTime == '10:08':
        break
    
#while True:
#    nowTime=datetime.datetime.now().strftime('%H:%M')#现在
#    driver.refresh()
#    if nowTime == '09:39':
#        
#        break
        

while True:
    
    try:
        #wait(xpath='//*[@id="pro-skus"]/dl[2]/div/ul/li[2]/div/a/p/span')
        
        driver.find_element_by_xpath('//*[@id="pro-skus"]/dl[2]/div/ul/li[2]/div/a/p/span').click()
        
        driver.find_element_by_xpath('//*[@id="pro-operation"]/a[2]').click()
        driver.find_element_by_xpath('//*[@id="checkoutSubmit"]').click()
        break
    
    except:
        js='window.open("https://www.vmall.com/product/10086689592595.html");'
        driver.execute_script(js)#访问所需property的URL
        handles = driver.window_handles
        driver.switch_to_window(handles[-1])

        
