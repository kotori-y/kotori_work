import re

import pandas as pd
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import random

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from tqdm import tqdm


class BrendaSpider:
    def __init__(self):
        profile = webdriver.FirefoxOptions()
        profile.set_preference("browser.startup.homepage", "about:blank")
        profile.set_preference("startup.homepage_welcome_url", "about:blank")
        profile.set_preference("startup.homepage_welcome_url.additional", "about:blank")

        desired_capabilities = DesiredCapabilities.FIREFOX  # 修改页面加载策略
        desired_capabilities["pageLoadStrategy"] = "none"  # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出

        self.driver = webdriver.Firefox()

        self.driver.get("https://www.brenda-enzymes.org/index.php")

    # the action of clicking
    def click(self, selector):
        self.driver.find_element(By.CSS_SELECTOR, selector).click()

    def wait(self, selector):
        Wait(self.driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))

    def wait_disappear(self, selector):
        Wait(self.driver, 30).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, selector)))

    def send_keys(self, selector, keys):
        self.driver.find_element(By.CSS_SELECTOR, selector).clear()
        self.driver.find_element(By.CSS_SELECTOR, selector).send_keys(keys)

    def search(self, ec_number):
        tgt_url = f"https://www.brenda-enzymes.org/enzyme.php?ecno={ec_number}#kcat/KM%20VALUE%20[1/mMs%3Csup%3E-1%3C/sup%3E]"
        self.driver.get(tgt_url)

        wrapper = ".flat-wrapper"
        unfold_btn = "#tab305_se"

        self.wait(wrapper)
        if 'Error 404 - Enzyme not found!' in self.driver.page_source:
            return False

        try:
            self.wait(unfold_btn)
            self.click(unfold_btn)
            return True
        except TimeoutException:
            return False

    def analysis_page(self):
        def foobar(tmp_list):
            return ','.join([x.strip() for x in tmp_list])

        html = self.driver.page_source
        tree = etree.HTML(html)

        values = tree.xpath('//*[@id="tab305"]/div[contains(@class, "row")]//div[1]//span/text()')
        substrate = tree.xpath('//*[@id="tab305"]/div[contains(@class, "row")]//div[2]//span/text()')
        organism = tree.xpath('//*[@id="tab305"]/div[contains(@class, "row")]//div[3]//span/a/text()')

        uniprot_rows = tree.xpath('//*[@id="tab305"]/div[contains(@class, "row")]//div[4]//span')
        uniprot = [x.xpath('string(.)') for x in uniprot_rows]

        commentary = tree.xpath('//*[@id="tab305"]/div[contains(@class, "row")]//div[5]//span/text()')

        return {
            'values': values[:len(organism)],
            'substrate': substrate[:len(organism)],
            'organism': organism,
            'uniprot': uniprot,
            'commentary': commentary
        }

    def run(self, ec_number):
        flag = self.search(ec_number)
        if flag:
            return pd.DataFrame(self.analysis_page())
        return pd.DataFrame()


if __name__ == "__main__":
    demo = BrendaSpider()

    for ec_number_ in ["7.1.1.8", "1.1.1.1", "10.5.1.1", "1.1.1.2"]:
        out = pd.DataFrame(demo.run(ec_number_))
        if not out.empty:
            out = out.applymap(lambda x: x.strip()).applymap(lambda x: None if x == "-" else x)
            out.insert(0, 'ec_number', ec_number_)
            out.to_csv(fr'E:\Mate\wjj\0307\{ec_number_}.txt', sep="\t", index=False)
        demo.driver.get('about:blank')
        time.sleep(1)
    # print(pd.DataFrame(ans_))
