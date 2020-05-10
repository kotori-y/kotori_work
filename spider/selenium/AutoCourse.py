# -*- coding: utf-8 -*-
"""
Created on Sat Sep 15 15:11:57 2018

@author: Kotori_Y
@WEIBO: Michariel
E-mail: yzjkid9@gmail.com

μ’sic Forever♪♪♪♪♪♪♪♪♪
I love Kotori forever(・8・)
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

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

desired_capabilities = DesiredCapabilities.FIREFOX 
desired_capabilities["pageLoadStrategy"] = "none"

driver = webdriver.Firefox(profile,executable_path = r"geckodriver.exe")
wait = WebDriverWait(driver, 30)

def login():
    driver.get('***')
#    sign = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.content-from:nth-child(1) > a:nth-child(1)')
#    )
#    )
#    sign.click()
    
    user = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#userName')
                                                      )
    )
    passwd = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#passWord')
                                                        )
    )
    
    user.send_keys('198211085')
    passwd.send_keys('117422')
    
    dl = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#login-btn')
                                                )
    )
    dl.click()
    

def study():
    online = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.block-nav > li:nth-child(2) > a:nth-child(1)')
    )
    )
    online.click()
    
    course = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.zxxxy > ul:nth-child(1) > li:nth-child(1) > a:nth-child(1) > img:nth-child(1)')
    )
    )
    course.click()


def main():
    n = 0
    login()
    windows = driver.current_window_handle
    study()
    while True:
        all_handles = driver.window_handles
        if len(all_handles) > 1:
            break
        else:
            time.sleep(10)
    print(all_handles)
    for handle in all_handles:
        if handle != windows:
            driver.switch_to.window(handle)
            while True:
                time.sleep(210)
                driver.refresh()
                n += 1
                print('>>>REFRESH #{}'.format(n))

    
if __name__ == '__main__':
    main()
