# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 13:33:17 2020

@Author: Zhi-Jiang Yang, Dong-Sheng Cao
@Institution: CBDD Group, Xiangya School of Pharmaceutical Science, CSU, China
@Homepage: http://www.scbdd.com
@Mail: yzjkid9@gmail.com; oriental-cds@163.com
@Blog: https://blog.iamkotori.com

♥I love Princess Zelda forever♥
"""

from multiprocessing import Pool
import xml.etree.ElementTree as ET
from lxml import etree
from requests import Session
import json
import os

os.chdir(r'')

class MolFromProtein(object):
    """
    """
    def __init__(self, UniprotID):
        """
        """
        self.UniprotID = UniprotID
        self.session = Session()
        
        self.headers = {
            "Connection": "keep-alive",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Cookie": "_ga=GA1.3.757562829.1572445921; csrftoken=nEd76UY2CAro6FtS8rAVTvJxWc1ZFy7XBMs3Rltm265uLG4z5wXOHSyDewy8j5Pa; chembl-website-v0.2-data-protection-accepted=true; _gid=GA1.3.302613681.1586835743",
            "Host": "www.ebi.ac.uk",
            "Origin": "https://www.ebi.ac.uk",
            "Referer": "https://www.ebi.ac.uk/chembl/g/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
            }
        
    
    def GetInfoFromUniprot(self):
        """
        """
        request_url = 'https://www.uniprot.org/uniprot/{}.xml'.format(self.UniprotID)
        try:
            r = self.session.get(request_url,timeout=30)
            if r.status_code == 200:
                tree = ET.fromstring(r.text)
                entry = tree[0]
                dbReference = entry.findall('{http://uniprot.org/uniprot}dbReference[@type="ChEMBL"]')
                res = [i.attrib['id'] for i in dbReference]
                # print(res)
            else:
                res = [None]       
        except:
            res = [None]
    
        return ''.join(res)
        
        
    def GetDownloadID(self):
        """
        """
        ChEMBLID = self.GetInfoFromUniprot()
        
        url = 'https://www.ebi.ac.uk/chembl/g/#browse/activities/filter/target_chembl_id%3A{}%20AND%20standard_type%3A(IC50%20OR%20Ki%20OR%20EC50%20OR%20Kd)%20AND%20_exists_%3Astandard_value%20AND%20_exists_%3Aligand_efficiency'.format(ChEMBLID)
        # print(url)
        html = self.session.get(url, headers=self.headers).text
        tree = etree.HTML(html)
        token = tree.xpath('//*[@class="GLaDOS-top-s3cre7"]//@value')[0]
        # token = token.encode('utf-8').decode('utf-8')
        # print(token)
    
    
        data = {
            "csrfmiddlewaretoken": token,
            "index_name": "chembl_26_activity",
            "query": '{"bool":{"must":[{"query_string":{"analyze_wildcard":true,"query":"target_chembl_id:%s AND standard_type:(IC50 OR Ki OR EC50 OR Kd) AND _exists_:standard_value AND _exists_:ligand_efficiency"}}],"filter":[]}}'%(ChEMBLID),
            # "query": '{"bool":{"must":[{"query_string":{"analyze_wildcard": true,"query":"_metadata.related_targets.all_chembl_ids:%s"}}],"filter":[]}}'%(self.GetInfoFromUniprot()),
            "format": "CSV",
            "context_id": "undefined",
            "download_columns_group": "undefined",
            }
        
        # print(data['csrfmiddlewaretoken'])
        
        url = 'https://www.ebi.ac.uk/chembl/glados_api/shared/downloads/queue_download/'
        response = self.session.post(url, headers=self.headers, data=data)
        html = response.text
        # return html
        # print(json.loads(html)['download_id'])
        # print(html)
        return json.loads(html)['download_id']
        
    def Download(self):
        url = 'https://www.ebi.ac.uk/chembl/dynamic-downloads/%s.gz'%(self.GetDownloadID())
        # print(url)
        r = self.session.get(url, headers=self.headers)
        assert r.status_code == 200
        with open('./data/{}.csv.gz'.format(self.UniprotID), 'wb') as f_obj:
            for chunk in r.iter_content(chunk_size=512):
                f_obj.write(chunk)
        f_obj.close()
        print('{} Finished'.format(self.UniprotID))
        
def main(UniprotID):
    """
    """
    try:
        download = MolFromProtein(UniprotID)
        download.Download()
    except:
        with open('Error.log', 'a') as f_obj:
            f_obj.write(UniprotID)
            f_obj.write('\n')
        f_obj.close()
    
    
    
if '__main__' == __name__:
    import pandas as pd
    
    data = pd.read_csv(r'pro_info.csv')
    unis = data.uni.tolist()
    
    ps = Pool()
    for UniprotID in unis:
        ps.apply_async(main, args=(UniprotID, ))
    ps.close()
    ps.join()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    