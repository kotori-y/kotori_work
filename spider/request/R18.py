# -*- coding: utf-8 -*-
"""
Created on Wed May  6 20:35:49 2020

@Author: Zhi-Jiang Yang, Dong-Sheng Cao
@Institution: CBDD Group, Xiangya School of Pharmaceutical Science, CSU, China
@Homepage: http://www.scbdd.com
@Mail: yzjkid9@gmail.com; oriental-cds@163.com
@Blog: https://blog.iamkotori.com

♥I love Princess Zelda forever♥
"""

import re
import os
from requests import Session
from lxml import etree
import cv2


class MSdownloader(object):
    """
    """
    def __init__(self, username, password):
        """
        """
        self.username = username
        self.password = password
        self.s = Session()
        
    def login(self):
        """
        """
        login_url = ""   
        data = {"username": self.username,
        "password": self.password,
        "remember-me": "1"}
        
        response = self.s.post(login_url, data=data)
        print(response.content.decode('utf-8'))
        
        self.obtainBalance()
        print('Balance: {}'.format(self.balance))
         
    def obtainBalance(self):
        """
        """
        user_url = ''
        response = self.s.get(user_url)
        
        tree = etree.HTML(response.text)
        balance = tree.xpath('//*[@class="card-title pricing-card-title"]/text()')
        self.balance = int(balance[0])
      
    def browseImg(self, img_url):
        """
        """
        cap = cv2.VideoCapture(img_url)
        if cap.isOpened():
            ret,img = cap.read()
            x, y = img.shape[0:2]
            img = cv2.resize(img, (int(y/2), int(x/2)))
            cv2.imshow("image",img)
            cv2.waitKey()
    
    def purchase(self, url):
        """
        """
        idx = re.findall('details/(.*)', url)
        buy_url = ''
        data = {"type": "1",
                "id": idx}
        self.s.post(buy_url, data=data)
        print('Purchase Succeeded!')
        self.obtainBalance()
        print('Balance: {}'.format(self.balance))
        self.s.get(url)
        
    def download(self, tree, url):
        """
        """
        _dir = input('the folder to saved: ')
        if not os.path.exists(_dir):
            os.makedirs(_dir)
        n = 0
        pages = len(tree.xpath('//*[@class="pagination justify-content-center"]/li'))
        #print(pages)
        for p in range(1, pages+1):
            url_page = '{}?p={}'.format(url, p)
            #print(url_page)
            response = self.s.get(url_page)
            tree = etree.HTML(response.text)
            imgs = tree.xpath('//img/@src')
            for img in imgs:
                #print(img)
                with open('{}/{}.jpg'.format(_dir, n), 'wb+') as f_obj:
                    f_obj.write(self.s.get(img).content)
                f_obj.close()
                n += 1
         
    def search(self, keyword, page=1):
        """
        """
        search_url = ''.format(keyword, page)
        response = self.s.get(search_url)
        tree = etree.HTML(response.text)
        album = tree.xpath('//*[@class="col-md-3"]')
        
        for al in album:
            img_url = al.xpath('div/a/img/@src')[0]
            self.browseImg(img_url)
            cv2.destroyAllWindows()
            
            print('=====================================================')
            flag = input('More Detail? ([y]/n/d)')
            if flag in ['', 'y', 'd']:
                url = al.xpath('div/a/@href')[0]
                url = ''.format(url)
                # idx = re.findall('details/(.*)', url)
                response = self.s.get(url)
                tree = etree.HTML(response.text)
                buy = 1 if not tree.xpath('//*[@action="/order/buy"]') else 0
                
                if flag == 'd':
                    if buy:
                        self.download(tree, url)
                    else:
                        price = tree.xpath('//*[@class="mb-0"][3]/text()')[0]
                        self.obtainBalance()
                        while True:
                            try:
                                buy = input('Not puchased, buy it? {}/{} ([y]/n)'.format(price, self.balance))
                                assert buy in ['', 'y', 'n']
                                break
                            except:
                                pass
                        if buy in ['', 'y']:
                            self.purchase(url)
                            self.download(tree, url)
                        else:
                            pass
                            
                        
                else:
                    imgs = tree.xpath('//img/@src')
                    for img in imgs:
                        self.browseImg(img)
                    cv2.destroyAllWindows()
                    
                    if tree.xpath('//*[@action="/order/buy"]'):
                        dl = 0
                        price = tree.xpath('//*[@class="mb-0"][3]/text()')[0]
                        self.obtainBalance()
                        while True:
                            try:
                                buy = input('Not purchased, buy it? {}/{} ([y]/n)'.format(price, self.balance))
                                assert buy in ['', 'y', 'n']
                                break
                            except:
                                pass
                        
                        if buy in ['', 'y']:
                            self.purchase(url)
                            dl = 1
                        else:
                            pass
                    
                    #purchased, downloaded
                    else:
                        dl = 1
                    
                    if dl:
                        while True:
                            try:
                                download = input('Purchased, download? (y/n)')
                                assert download in ['y', 'n']
                                break
                            except:
                                print('Invalid Input')
                        
                        if download == 'y':
                            self.download(tree, url)
                        else:
                            pass
                    else:
                        pass
            elif flag == 'exit':
                print('=====================================================', end='\n\n')
                break
            
            else:
                pass
            
            con = input('continue? ([y]/n)')
            print('=====================================================', end='\n\n')
            if con == '' or con == 'y':
                pass
            else:
                break
                                
                    
                    

if '__main__' == __name__:
    username = ""
    password = ""
    
    ms = MSdownloader(username, password)
    ms.login()
    print('>>> Start\n')
    while True:
        keyword = input('The girl you want to seach: ')
        if keyword == 'exit':
            break
        ms.search(keyword)
            