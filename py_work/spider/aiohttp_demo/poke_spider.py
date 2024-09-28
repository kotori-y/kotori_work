import re
import os
import asyncio
from typing import List, Dict

import httpx
import pandas as pd
from lxml import etree
# from httpx import ConnectTimeout,

MAX_ID = 1010


TYPE_HASH = {
    "Normal": "一般",
    "Wasser": "水",
    "Feuer": "火",
    "Elektro": "电",
    "Pflanze": "草",
    "Flug": "飞行",
    "Käfer": "虫",
    "Gift": "毒",
    "Gestein": "岩石",
    "Boden": "地面",
    "Kampf": "格斗",
    "Eis": "冰",
    "Psycho": "超能",
    "Geist": "幽灵",
    "Drache": "龙",
    "Stahl": "钢",
    "Unlicht": "恶",
    "Fee": "妖精"
}


def timeout_catch(func):
    async def wrapper(*args, **kw):
        try:
            return await func(*args, **kw)
        except httpx.ConnectError:
            return ""

    return wrapper


class PokeSpider:
    def __init__(self):
        self.client = httpx.AsyncClient()

    @timeout_catch
    async def id_to_name(self, dex_id: int) -> str:
        if 0 < dex_id <= MAX_ID:
            url = f"https://www.pokewiki.de/{dex_id}"
            resp = await self.client.get(url, timeout=30)

            if resp.status_code == 200:
                html = resp.text

                tree = etree.HTML(html)
                name = tree.xpath('//*[@id="mw-content-text"]/div/ul[1]/li[1]/a/@title')
                if name:
                    return name[0]
        return ""

    @timeout_catch
    async def obtain_poke_info(self, dex_id: int) -> Dict:
        out = {
            "ID": dex_id,
            "Names": {
                "CHS": "",
                "ENG": "",
            },
            "Types": []
        }
        if 0 < dex_id <= MAX_ID:
            name = await self.id_to_name(dex_id)
            url = f"https://www.pokewiki.de/{name}"
            resp = await self.client.get(url, timeout=30)

            if resp.status_code == 200:
                html = resp.text
                tree = etree.HTML(html)

                _types = tree.xpath('//a[text()="Typen"]/parent::td/following-sibling::td/a/@title')
                if _types:
                    types = [TYPE_HASH[x] for x in _types[:2]]
                    out["Types"] = types

                _chs = tree.xpath('//*[contains(text(), "Chinesisch")]//following-sibling::td[1]/text()')
                if _chs:
                    chs = _chs[0].split("/")[-1].strip()
                    out["Names"]["CHS"] = chs

                _eng = tree.xpath('//*[contains(text(), "Englisch")]//following-sibling::td[1]/text()')
                if _eng:
                    eng = _eng[0].split("/")[0].strip()
                    out["Names"]["ENG"] = eng

        return out

    async def run(self, dex_id_array: List[int]):
        out = {}
        for dex_id in dex_id_array:
            await self.obtain_poke_info(dex_id)
        return out

    async def async_run(self, dex_id_array: List[int]):
        task_list = []
        for dex_id in dex_id_array:
            task = asyncio.create_task(self.id_to_name(dex_id))
            task_list.append(task)

        return await asyncio.gather(*task_list)


if __name__ == "__main__":
    spider = PokeSpider()
    name_hash = asyncio.run(spider.run(list(range(6, 7))))
    # name_hash = asyncio.run(spider.async_run(list(range(1, 10))))

    print("DONE!!!")
