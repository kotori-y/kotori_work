# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 18:33:35 2019

You are not expected to understand my codes!

@Author: Kotori_Y
@Blog: blog.moyule.me
@Weibo: Kotori-Y
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

#wait until some element could be located
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

#log in 
def login(username, passwd):
    click(xpath='//*[@class="text2"][@name="login"]'
          )
    send_keys(xpath='//*[@class="text2"][@name="login"]', keys=username
              )
    
    click(xpath='//*[@class="text2"][@name="pwd"]'
          )
    send_keys(xpath='//*[@class="text2"][@name="pwd"]', keys=passwd
              )
    
    click(xpath='/html/body/div[2]/div[2]/form/table/tbody/tr[3]/td/a[1]'
          )
    
#switch to a new page
def switch(js):
    driver.execute_script(js
                          )#访问所需property的URL
    handles = driver.window_handles
    driver.switch_to_window(handles[-1]
    )


def next_page(pagenumber):
    pagenumber = str(pagenumber)
    send_keys(xpath='//*[@id="pageInput"]', keys=pagenumber
              )
    driver.find_element_by_xpath('//*[@id="pageInput"]').send_keys(Keys.ENTER
                                )


def option(item):
    click(xpath='//*[@name="property"]')
    time.sleep(0.5)
    click(xpath='//*[@name="property"]/option[{}]'.format(item))

def showfull(index):
    click(xpath='//*[@id="Browser"]/div[{}]//*[@class="smarts"]/a'.format(index))

def collect(html,index):
    
    index = str(index)
    
    name = html.xpath('//*[@id="Browser"]/div[{}]//*[@class="smart"]/text()'.format(index
                      )
        )[0]
    
    group = html.xpath('//*[@id="Browser"]/div[{}]//*[@class="comment"]/text()'.format(index
                       )
        )[0]

    smart = html.xpath('//*[@id="Browser"]/div[{}]//*[@class="smarts"]/text()'.format(index
                       )
        )[0]
        
    author = html.xpath('//*[@id="Browser"]/div[{}]//*[@class="article-data"]/a[1]/@title'.format(index
                        )
        )[0]
        
    article = html.xpath('//*[@id="Browser"]/div[{}]//*[@class="article-data"]/a[2]/@title'.format(index
                        )
        )[0]
    
    ID = html.xpath('//*[@id="Browser"]/div[{}]//*[@title="TA-identifier of the alert"]/text()'.format(index
                     )
        )[0]   

    return name,group,smart,author,article,ID

def main():
    
    data = dict()
    
   
    
    
    while True:
        driver.get('https://ochem.eu/login/show.do'
                   )
        
        try: 
            switchframe(xpath='//*[@frameborder="0"]'
                        )
            wait(xpath='//*[@class="text2"][@name="login"]'
                 )
            break
        
        except:
            pass
    
    
    login(username='kotori_y',passwd='YZJ753gooD'
          )
    driver.switch_to_default_content() #switch out of last frame
    
#    while True:
#        try:
#            wait(xpath='//*[@id="yui-gen6"]')
#            on_stop = driver.find_element_by_xpath('//*[@id="yui-gen6"]')#悬停
#            ActionChains(driver).move_to_element(on_stop).perform()#悬停
#        except:
#            driver.refresh()
#    
    
    switch(js='window.open("https://ochem.eu/alerts/show.do");'
           )
    
    while True:
        
        try: 
            switchframe(xpath='//*[@frameborder="0"]'
                        )
            wait(xpath='//*[@name="property"]'
                 )
            break
        
        except:
            pass
    
    
    for item in range(2,23):
         nl = list()
         gl = list()
         sl = list()
         aul = list()
         atl = list()
         IDl = list()
         info = []
        
         while True:
            try:
                item = str(item)
                option(item)
                wait(xpath='//*[@id="Browser"]/div[1]')
                break
            except:
                pass
        
         html = driver.page_source
         html = etree.HTML(html)
        
         classes = html.xpath('//*[@name="property"]/option[{}]/text()'.format(item))[0]
         print('----------------------------------{}----------------------------------'.format(classes))
         print(html.xpath('//*[@id="Browser"]/div[1]//*[@class="smart"]/text()'))
         pagerange = html.xpath('//*[@class="pgr pager"]//a[2]/@page')
        
         if pagerange == []:
            time.sleep(15)
            html = driver.page_source
            html = etree.HTML(html)
            length = len(html.xpath('//*[@class="browser-item"]'))
            for x in range(1,length+1):
                
                try:
                    showfull(x)
                except:
                    pass
                
                name,group,smart,author,article,ID = collect(html,x)
                nl.append(name)
                gl.append(group)
                sl.append(smart)
                aul.append(author)
                atl.append(article)
                IDl.append(ID)
                
                
            info.append(nl)
            info.append(gl)
            info.append(sl)
            info.append(aul)
            info.append(atl)
            info.append(IDl)
                
            data[classes] = info
                
         else:
            pagerange = int(pagerange[0])
            
            
            while True:
                
                try:
                    wait(xpath='//*[@id="pageInput"]')
                    break
                except:
                    pass
                
                
            for i in range(1,pagerange+1):
                
                
                while True:
                    try:
                        next_page(pagenumber=i)
#                        re(xpath='//*[@id="Browser"]/div[1]')
                        wait(xpath='//*[@id="Browser"]/div[1]')
                        break
                    except:
                        option(item)
                time.sleep(15)
                html = driver.page_source
                html = etree.HTML(html)
                
                length = len(html.xpath('//*[@class="browser-item"]'))
                
                for x in range(1,length+1):
                
                    try:
                        showfull(x)
                    except:
                        pass
                    
                    name,group,smart,author,article,ID = collect(html,x)
                    nl.append(name)
                    gl.append(group)
                    sl.append(smart)
                    aul.append(author)
                    atl.append(article)
                    IDl.append(ID)
#                    time.sleep(0.2)
                    
                info.append(nl)
                info.append(gl)
                info.append(sl)
                info.append(aul)
                info.append(atl)
                info.append(IDl)
                
                data[classes] = info
    
    return data      
        
        
        
    
if '__main__' == __name__:
     data = main()


