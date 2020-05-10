# -*- coding: utf-8 -*-
"""
Created on Fri Aug  2 19:57:03 2019

@Author: Zhi-Jiang Yang, Dong-Sheng Cao
@Institution: CBDD Group, Xiangya School of Pharmaceutical Science, CSU, China
@Homepage: http://www.scbdd.com
@Mail: yzjkid9@gmail.com; oriental-cds@163.com
@Blog: https://blog.moyule.me

♥I love Princess Zelda forever♥
"""

import requests
import re
from lxml import etree
import smtplib
from email.mime.text import MIMEText
import time
import json


class Douban(object):
    
    def __init__(self,uname,pwd):
        self.uname = uname
        self.pwd = pwd
        self.s = requests.Session()
        
    def login(self):
        login_url = 'https://accounts.douban.com/j/mobile/login/basic'
        data = {'name': self.uname, 'password': self.pwd}
        headers = {'Cookie': 'll="108090"; bid=VdkI2ex0Hho; _vwo_uuid_v2=D44D24E8891A0C0F1475EB67B257C9B75|df3dbeac495d0147d9f5fed7a3231abb; douban-fav-remind=1; ct=y; push_noty_num=0; push_doumail_num=0; douban-profile-remind=1; __utmc=30149280; __utmv=30149280.20005; ap_v=0,6.0; __utmt=1; __utma=30149280.452277992.1564733753.1564742137.1564743871.3; __utmz=30149280.1564743871.3.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; apiKey=; _pk_ref.100001.2fad=%5B%22%22%2C%22%22%2C1564743999%2C%22https%3A%2F%2Fblog.catkin.moe%2F%22%5D; _pk_ses.100001.2fad=*; dbcl2="200055821:iWnyIEWprYQ"; last_login_way=account; ck=UOK7; __utmb=30149280.14.5.1564743894811; _pk_id.100001.2fad=dc3c69fa88be4bd2.1553151285.3.1564744028.1564147688.; login_start_time=1564744029367',
                   'Host': 'accounts.douban.com',
                   'Origin': 'https://accounts.douban.com',
                   'Referer': 'https://accounts.douban.com/passport/login',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
                   }
        self.response = self.s.post(login_url,data=data,headers=headers).text
        
    def browse(self):
        html = self.s.get('https://www.douban.com/people/166362786/notes').text
        html = etree.HTML(html)
        self.newest = html.xpath('//*[@class="article"]/div[3]/@data-url')[0]
        html = self.s.get(self.newest).text
        html = etree.HTML(html)
        self.contents = html.xpath('//*[@class="article"]')[0].xpath('string(.)')
        diary = re.findall("夜航船\n([\w\W]*?)©",self.contents)[0].replace('\n','').split(' ')
        while True:
            try:
                diary.remove('')
            except:
                break
        return ''.join(diary)


class QQmail(object):
    
    def __init__(self,uname,pwd):
        self.uname = uname
        self.pwd = pwd
        self.smtp = smtplib.SMTP_SSL("smtp.qq.com",465)
        
    def login(self):
        self.smtp.login(self.uname,self.pwd)
        
    def send(self,to,words):
        message = MIMEText(words,"plain","utf-8")
        message["Subject"] = "NOTICE"
        message["To"] = to
        message["From"] = self.uname
        self.smtp.sendmail(self.uname,to,message.as_string())
    
            
        
if '__main__' == __name__:
    station = None
    douban = Douban('***********','***************')   
    douban.login()
    print(json.loads(douban.response)['status'],end='\n\n')
    
    
    while True:
        now = time.strftime('%H:%M')
        if now == '22:20':
            print('--------------------Inspecting Start--------------------')
            break
        else:
            pass
    
    while True:
        
        contents = douban.browse()
        print(contents,end='\n\n')
        if (contents != station) and station:
            mail = QQmail("*******","*******************") 
            mail.login()
            mail.send('*******@qq.com',contents)
            break
        else:
            station = contents
            time.sleep(900)
            now = time.strftime('%H:%M')
            if now == '23:30':
                break