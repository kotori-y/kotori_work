# -*- coding: utf-8 -*-
"""
Created on Sat Sep 29 19:15:42 2018

@author: Kotori_Y
@WEIBO: Michariel
E-mail: yzjkid9@gmail.com

μ’sic Forever♪♪♪♪♪♪♪♪♪
I love Kotori forever(・8・)
"""

from selenium import webdriver
import time
import re

driver = webdriver.Firefox(executable_path = r'~/geckodriver.exe')

def login():
    driver.get('http://gra.csu.xuetangx.com/#/'
               )
    driver.find_element_by_css_selector('div.col-md-2:nth-child(3) > ul:nth-child(1) > li:nth-child(1) > a:nth-child(1)'
                                        ).click()
    
    driver.find_element_by_css_selector('div.form-group:nth-child(3) > input:nth-child(1)'
                                        ).click()
    time.sleep(2)
    driver.find_element_by_css_selector('div.form-group:nth-child(3) > input:nth-child(1)'
                                        ).send_keys('id')
    
    driver.find_element_by_css_selector('div.form-group:nth-child(5) > input:nth-child(1)'
                                        ).click()
    time.sleep(2)
    driver.find_element_by_css_selector('div.form-group:nth-child(5) > input:nth-child(1)'
                                        ).send_keys('pwd')
    
    driver.find_element_by_css_selector('.btn'
                                        ).click()
def choose_course():
    time.sleep(10)
    driver.find_element_by_css_selector('.nav-menu > ul:nth-child(1) > li:nth-child(2) > a:nth-child(1)'
                                        ).click()
    time.sleep(3)
    driver.find_element_by_css_selector('a.btn'
                                        ).click()   
    time.sleep(5)
    handles = driver.window_handles
    driver.switch_to_window(handles[-1])
    
    time.sleep(5)
    html = driver.page_source
    global now_class
    now_class = re.findall(r'<h2>第(.)章.*?</h2>.*?<a href="/courses/.*?">第(.)节.*?</a>', html, re.S)
    if now_class[0][0] == '一':
        now_class = [1, int(now_class[0][-1])]
    elif now_class[0][0] == '二':
        now_class = [2, int(now_class[0][-1])]
    elif now_class[0][0] == '三':
        now_class = [3, int(now_class[0][-1])]
    elif now_class[0][0] == '四':
        now_class = [4, int(now_class[0][-1])]
    else:
        now_class = [5, int(now_class[0][-1])]
    
    print(now_class)
    driver.find_element_by_xpath('//*[@id="course-content"]/p/a'
                                        ).click()
def play():
    while True:
        
        try:
            time.sleep(10)
            html = driver.page_source
            video = re.findall('<div id="(video_.*?)" class="video closed"',html, re.S)       
            break
        
        except:
            driver.refresh
 
    driver.find_element_by_css_selector('.xt_video_player_volume_icon'
                                        ).click()

    driver.find_element_by_xpath('//*[@id="' + video[0] + '"]/div/div[1]/div[1]/div[1]'
                                 ).click()
    
def process():
    a = ''
    time.sleep(120)
    
    while True:
        time.sleep(5)
        
        html = driver.page_source
        cost = re.findall('<div class="xt_video_player_current_time_display fl"><span>(.*)</span> / <span>(.*)</span></div>', html, re.S)
        print(cost)
        
        b = cost[0][0]        
        if b != a and cost[0][1] != '00:00':             
            if cost[0][0] == cost[0][1]:
                break
            else:
                pass        
        else:
            driver.refresh
            play()
        
        a = b
            

def next_course(c,s): 
    try:       
        selector = '#ui-accordion-accordion-panel-' + c + '> li:nth-child(' + s + ') > a:nth-child(1)'
        time.sleep(10)
        driver.find_element_by_css_selector(selector).click(
            )
    except:
        driver.refresh()
        next_course(c,s)

def main():
    login()
    choose_course()
    play()
    new_class = now_class
    sign = 1
    while sign == 1:
        process()
        
        if new_class[0] == 1 and new_class[-1] != 6:
            c = 0
            s = new_class[-1] +1
        
        elif new_class[0] == 1 and new_class[-1] == 6:
            driver.find_element_by_css_selector('#ui-accordion-accordion-header-1 > a').click(
                                                )
            c = 1
            s = 1
        
        elif new_class[0] == 2 and new_class[-1] != 4:
            c = 1
            s = new_class[-1] +1
        
        elif new_class[0] == 2 and new_class[-1] == 4:
            driver.find_element_by_css_selector('#ui-accordion-accordion-header-2 > a').click(
                                                )                
            c = 2
            s = 1
        
        elif new_class[0] == 3 and new_class[-1] != 4:
            c = 2
            s = new_class[-1] +1
        
        elif new_class[0] == 3 and new_class[-1] == 4:
            driver.find_element_by_css_selector('#ui-accordion-accordion-header-3 > a').click(
                                                )
            c = 3
            s = 1
            
        elif new_class[0] == 4 and new_class[-1] != 5:
            c = 3
            s = new_class[-1] +1
        
        elif new_class[0] == 4 and new_class[-1] == 5:
            c = 4
            s = 1
        
        elif new_class[0] == 5 and new_class[-1] != 6:
            c = 4
            s = new_class[-1] +1
        
        else:
            sign = 0
        
        if sign == 0:
            print("The class is over!")
            driver.quit()
        
        else:
            c =str(c)
            s = str(s)
            new_class = [int(c) + 1, int(s)]
            print(new_class)            
            next_course(c,s)
            play()
        
        
            

if __name__ ==  '__main__':
    main()