import re

from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time
import random

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from tqdm import tqdm


class EMOBSS_Caculator:
    def __init__(self):
        profile = webdriver.FirefoxOptions()
        profile.set_preference("browser.startup.homepage", "about:blank")
        profile.set_preference("startup.homepage_welcome_url", "about:blank")
        profile.set_preference("startup.homepage_welcome_url.additional", "about:blank")

        desired_capabilities = DesiredCapabilities.FIREFOX  # 修改页面加载策略
        desired_capabilities["pageLoadStrategy"] = "none"  # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出

        self.driver = webdriver.Firefox()

        self.driver.get("https://www.ebi.ac.uk/Tools/psa/emboss_needle/")

    # the action of clicking
    def click(self, selector):
        self.driver.find_element(By.CSS_SELECTOR, selector).click()

    def wait(self, selector):
        Wait(self.driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))

    def send_keys(self, selector, keys):
        self.driver.find_element(By.CSS_SELECTOR, selector).clear()
        self.driver.find_element(By.CSS_SELECTOR, selector).send_keys(keys)

    def query(self, seq1, seq2):
        aseq = '#asequence'
        bseq = '#bsequence'
        btn = '#jd_submitButtonPanel > input'

        self.wait(aseq)
        self.send_keys(aseq, seq1)
        self.send_keys(bseq, seq2)
        # self.click(btn)


if __name__ == "__main__":
    app = EMOBSS_Caculator()
    app.query(
        seq1="MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSHGSAQVKGHGKKVADALTNAVAHVDDMPNALSALSDLHAHKLRVDPVNFKLLSHCLLVTLAAHLPAEFTPAVHASLDKFLASVSTVLTSKYR",
        seq2="MVLSGEDKSNIKAAWGKIGGHGAEYGAEALERMFASFPTTKTYFPHFDVSHGSAQVKGHGKKVADALASAAGHLDDLPGALSALSDLHAHKLRVDPVNFKLLSHCLLVTLASHHPADFTPAVHASLDKFLASVSTVLTSKYR"
    )


