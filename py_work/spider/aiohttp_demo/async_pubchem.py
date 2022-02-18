import asyncio
from collections import namedtuple

import aiohttp
import re


async def fetch_pubchem(cid, item_list=['InChI', 'InChI Key', 'Canonical SMILES']):
    def GetRegx(item):
        return r'"TOCHeading": "{}".*?"String": "(.*?)"'.format(item)

    def GetInfo(regx_list):
        idx = 0
        while idx != len(regx_list):
            regx = regx_list[idx]
            check = re.findall(regx, html, re.S)
            if check:
                yield check[0]
            else:
                yield None
            idx += 1

    request_url = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{}/JSON/'.format(cid)
    async with aiohttp.ClientSession() as session:
        async with session.get(request_url) as response:
            html = await response.text()

    regx_list = [GetRegx(item) for item in item_list]
    info_list = [info for info in GetInfo(regx_list)]
    info_list.insert(0, cid)
    item_list = [x.replace(' ', '_') for x in item_list]
    item_list.insert(0, 'CID')

    res = namedtuple('PubChem', item_list)
    print(res(*info_list))
    return res(*info_list)


if __name__ == "__main__":
    import time

    start = time.time()

    cids = [2144, 7475, 240]
    loop = asyncio.get_event_loop()
    tasks = [fetch_pubchem(cid) for cid in cids]
    res = loop.run_until_complete(asyncio.gather(*tasks))
    loop.close()

    print(res)

    end = time.time()

    print(end - start)
