# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 21:31:29 2020

@author: Kotori Y
@Homepage: http://www.scbdd.com
@Mail: yzjkid9@gmail.com; oriental-cds@163.com
@Blog: https://blog.iamkotori.com

♥I love Princess Zelda forever♥
"""


import time
import base64
import rsa
import binascii
import requests
import re
from PIL import Image
import random
from urllib.parse import quote_plus
# import http.cookiejar as cookielib
import json
from lxml import etree

agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0'
headers = {
    'User-Agent': agent
}


class WeiboLogin(object):
    """
    通过登录 weibo.com 然后跳转到 m.weibo.cn
    """

    def __init__(self, user, password):
        super(WeiboLogin, self).__init__()
        self.user = user
        self.password = password
        self.session = requests.Session()
        # self.cookie_path = cookie_path
        # self.session.cookies = cookielib.LWPCookieJar(filename=self.cookie_path)
        self.index_url = "http://weibo.com/login.php"
        self.session.get(self.index_url, headers=headers, timeout=30)
        self.postdata = dict()

    def get_su(self):
        """
        对 email 地址和手机号码 先 javascript 中 encodeURIComponent
        对应 Python 3 中的是 urllib.parse.quote_plus
        然后在 base64 加密后decode
        """
        username_quote = quote_plus(self.user)
        username_base64 = base64.b64encode(username_quote.encode("utf-8"))
        return username_base64.decode("utf-8")

    # 预登陆获得 servertime, nonce, pubkey, rsakv
    def get_server_data(self, su):
        """与原来的相比，微博的登录从 v1.4.18 升级到了 v1.4.19
        这里使用了 URL 拼接的方式，也可以用 Params 参数传递的方式
        """
        pre_url = "http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su="
        pre_url = pre_url + su + "&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.19)&_="
        pre_url = pre_url + str(int(time.time() * 1000))
        pre_data_res = self.session.get(pre_url, headers=headers)
        # print(pre_data_res.text)
        sever_data = eval(pre_data_res.content.decode("utf-8").replace("sinaSSOController.preloginCallBack", ''))

        return sever_data

    def get_password(self, servertime, nonce, pubkey):
        """对密码进行 RSA 的加密"""
        rsaPublickey = int(pubkey, 16)
        key = rsa.PublicKey(rsaPublickey, 65537)  # 创建公钥
        message = str(servertime) + '\t' + str(nonce) + '\n' + str(self.password)  # 拼接明文js加密文件中得到
        message = message.encode("utf-8")
        passwd = rsa.encrypt(message, key)  # 加密
        passwd = binascii.b2a_hex(passwd)  # 将加密信息转换为16进制。
        return passwd

    def get_cha(self, pcid):
        """获取验证码，并且用PIL打开，
        1. 如果本机安装了图片查看软件，也可以用 os.subprocess 的打开验证码
        2. 可以改写此函数接入打码平台。
        """
        cha_url = "https://login.sina.com.cn/cgi/pin.php?r="
        cha_url = cha_url + str(int(random.random() * 100000000)) + "&s=0&p="
        cha_url = cha_url + pcid
        cha_page = self.session.get(cha_url, headers=headers)
        with open("cha.jpg", 'wb') as f:
            f.write(cha_page.content)
            f.close()
        try:
            im = Image.open("cha.jpg")
            im.show()
            im.close()
        except Exception as e:
            print(u"请到当前目录下，找到验证码后输入")

    def pre_login(self):
        # su 是加密后的用户名
        su = self.get_su()
        sever_data = self.get_server_data(su)
        servertime = sever_data["servertime"]
        nonce = sever_data['nonce']
        rsakv = sever_data["rsakv"]
        pubkey = sever_data["pubkey"]
        showpin = sever_data["showpin"]  # 这个参数的意义待探索
        password_secret = self.get_password(servertime, nonce, pubkey)

        self.postdata = {
            'entry': 'weibo',
            'gateway': '1',
            'from': '',
            'savestate': '7',
            'useticket': '1',
            'pagerefer': "https://passport.weibo.com",
            'vsnf': '1',
            'su': su,
            'service': 'miniblog',
            'servertime': servertime,
            'nonce': nonce,
            'pwencode': 'rsa2',
            'rsakv': rsakv,
            'sp': password_secret,
            'sr': '1366*768',
            'encoding': 'UTF-8',
            'prelt': '115',
            "cdult": "38",
            'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
            'returntype': 'TEXT'  # 这里是 TEXT 和 META 选择，具体含义待探索
        }
        return sever_data

    def login(self):
        # 先不输入验证码登录测试
        try:
            sever_data = self.pre_login()
            login_url = 'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)&_'
            login_url = login_url + str(time.time() * 1000)
            login_page = self.session.post(login_url, data=self.postdata, headers=headers)
            ticket_js = login_page.json()
            ticket = ticket_js["ticket"]
        except Exception as e:
            sever_data = self.pre_login()
            login_url = 'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)&_'
            login_url = login_url + str(time.time() * 1000)
            pcid = sever_data["pcid"]
            self.get_cha(pcid)
            self.postdata['door'] = input(u"请输入验证码")
            login_page = self.session.post(login_url, data=self.postdata, headers=headers)
            ticket_js = login_page.json()
            print(ticket_js)
            time.sleep(5)
            ticket = ticket_js["ticket"]
        # 以下内容是 处理登录跳转链接
        save_pa = r'==-(\d+)-'
        ssosavestate = int(re.findall(save_pa, ticket)[0]) + 3600 * 7
        jump_ticket_params = {
            "callback": "sinaSSOController.callbackLoginStatus",
            "ticket": ticket,
            "ssosavestate": str(ssosavestate),
            "client": "ssologin.js(v1.4.19)",
            "_": str(time.time() * 1000),
        }
        jump_url = "https://passport.weibo.com/wbsso/login"
        jump_headers = {
            "Host": "passport.weibo.com",
            "Referer": "https://weibo.com/",
            "User-Agent": headers["User-Agent"]
        }
        jump_login = self.session.get(jump_url, params=jump_ticket_params, headers=jump_headers)
        uuid = jump_login.text

        uuid_pa = r'"uniqueid":"(.*?)"'
        uuid_res = re.findall(uuid_pa, uuid, re.S)[0]
        web_weibo_url = "http://weibo.com/%s/profile?topnav=1&wvr=6&is_all=1" % uuid_res
        weibo_page = self.session.get(web_weibo_url, headers=headers)
        weibo_pa = r'<title>(.*?)</title>'
        # print(weibo_page.content.decode("utf-8"))
        userID = re.findall(weibo_pa, weibo_page.content.decode("utf-8", 'ignore'), re.S)[0]
        print(u"欢迎你 %s" % userID)

        # weibo.com 登录成功
        # 利用 weibo.com 的 cookie 登录到  m.weibo.cn
        # print("利用 weibo.com 的 cookie 登录到  m.weibo.cn")
        Mheaders = {
            "Host": "login.sina.com.cn",
            "User-Agent": agent
        }

        # m.weibo.cn 登录的 url 拼接
        _rand = str(time.time())
        mParams = {
            "url": "https://m.weibo.cn/",
            "_rand": _rand,
            "gateway": "1",
            "service": "sinawap",
            "entry": "sinawap",
            "useticket": "1",
            "returntype": "META",
            "sudaref": "",
            "_client_version": "0.6.26",
        }
        murl = "https://login.sina.com.cn/sso/login.php"
        mhtml = self.session.get(murl, params=mParams, headers=Mheaders)
        mhtml.encoding = mhtml.apparent_encoding
        mpa = r'replace\((.*?)\);'
        mres = re.findall(mpa, mhtml.text)

        # 关键的跳转步骤，这里不出问题，基本就成功了。
        Mheaders["Host"] = "passport.weibo.cn"
        self.session.get(eval(mres[0]), headers=Mheaders)
        # mlogin = self.session.get(eval(mres[0]), headers=Mheaders)
        # print(mlogin.status_code)
        # 进过几次 页面跳转后，m.weibo.cn 登录成功，下次测试是否登录成功
        Mheaders["Host"] = "m.weibo.cn"
        Set_url = "https://m.weibo.cn"
        pro = self.session.get(Set_url, headers=Mheaders)
        pa_login = r'isLogin":true,'
        login_res = re.findall(pa_login, pro.text)
        print(login_res)

        # 可以通过 session.cookies 对 cookies 进行下一步相关操作
        # self.session.cookies.save()
    
    def blockUID(self, uid, count=1):
        url = 'https://weibo.com/aj/filter/block?ajwvr=6'
        
        self.session.headers["Referer"] = 'http://weibo.com/u/{}'.format(uid)
        
        data = {"uid": uid,
                "filter_type": "1",
                "status": "1",
                "interact": "1",
                "follow": "1"} 
        response = self.session.post(url, data=data)
        html = response.text
        html = json.loads(html)
        msg = html['msg']
                
        print('No.{:5s}: {} {}'.format(str(count), uid, msg))
        
        time.sleep(0.5)
            
    
    def main(self, url):
        response = self.session.get(url)
        mid = re.findall('do=mblog&act=(\d+)', response.text)[0]
        print(mid)
        COUNT = 1
        
        for page in range(1,100):
            comment_url = 'https://weibo.com/aj/v6/comment/big?ajwvr=6&id={}&from=singleWeiBo&page={}'.format(mid, page)
            
            response = self.session.get(comment_url)
            time.sleep(5)
            html = response.text
        
            json.loads(html)
            html = json.loads(html)
            html = html['data']['html']
            nums = re.findall('共(.*)条回复', html)
            
            html = etree.HTML(html)
            html.xpath('//*[@class="list_box"]')
            comment_box = html.xpath('//*[@class="list_ul"]')[0]    
            
            
            for comment,num in zip(comment_box.xpath('div')[:-1], nums):
                num = int(num)
                comment_id = comment.xpath('@comment_id')[0]
                
                uid = comment.xpath('*[@class="WB_face W_fl"]/a/img/@usercard')[0][3:]
                self.blockUID(uid, COUNT)
                COUNT += 1
                
                n = 0
                p = 1
                while n < num:
                    level2 = "https://weibo.com/aj/v6/comment/big?ajwvr=6&more_comment=big&root_comment_id={}&is_child_comment=ture&id={}&from=singleWeiBo&child_comment_page={}".format(
                        comment_id, mid, p)
                    
                    response = self.session.get(level2)
                    
                    html = response.text
    
                    json.loads(html)
                    html = json.loads(html)
                    html = html['data']['html']
                    
                    for uid in re.findall('usercard="id=(\d+)"', html):
                        self.blockUID(uid, COUNT)
                        COUNT += 1
                        n += 1
                    p += 1
                
                
                
                
if __name__ == '__main__':    
    username = input("Usename: ")  # 用户名
    password = input("password: ")  # 密码
    url = input("Weibo Url: ")
    # cookie_path = r""  # 保存cookie 的文件名称
    weibo = WeiboLogin(username, password, 
                       # cookie_path
                       )
    weibo.login()
    weibo.main(url)
    
    

    