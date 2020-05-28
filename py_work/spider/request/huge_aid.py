"""
@Author: Jun-Hong He, Zhi-Jiang Yang
@Institution: CBDD Group, Xiangya School of Pharmaceutical Science, CSU, China
@Homepage: http://www.scbdd.com

♥I love Princess Zelda forever♥
"""


import os
import re
import argparse
import multiprocessing as mp

from requests import Session




class HugeDownloader(object):
    
    def __init__(self, args):
        self.session = Session()
        self.args = args
        # self.lock = mp.Lock()
    
    def downloadSingle(self, url, aid, step, attemp=0):
        file_name = os.path.join(self.args.output, 'aid_{}_{}.csv'.format(aid, step))
        lock.acquire()
        try:
            response = self.session.get(url,stream=True)
        except:
            if attemp < 4:
                lock.release()
                self.downloadSingle(url, aid, step, attemp+1)
            else:
                pass
        lock.release()
        
        with open(file_name,'ab') as f:
            for item in response.iter_content(chunk_size=512):
                if item:
                    f.write(item) 
        f.close()
        print('{} update {}'.format(file_name, response))

    def inchikey(self, aid):
        url = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/%s/sids/XML?list_return=listkey'%(aid)
        response = self.session.get(url,stream=True)
        key = re.findall('<ListKey>(\d+)</ListKey>',response.text)[0]
        size = re.findall('<Size>(\d+)</Size>',response.text)[0]
        
        return int(key), int(size)

	
    def geturl(self, aid):
        key, size = self.inchikey(aid)
        for step in range(0, size, 10000):
            url = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/{}/CSV?sid=listkey&listkey={}&listkey_start={}&listkey_count=10000'.format(aid,key,step)    
            yield url, step

    def getlock(self, l):
        global lock
        lock = l

    def downloadAssay(self):
        items = self.geturl(self.args.aid)
        lock = mp.Lock()
        pool = mp.Pool(self.args.n_jobs, initializer=self.getlock, initargs=(lock,))
        
        for url,step in items:
            # print(url)
            pool.apply_async(self.downloadSingle, args=(url, self.args.aid, step))
        pool.close()
        pool.join()
        print("Done!!!")
 


def add_arguments(parser):
    """Helper function to fill the parser object.

    Args:
        parser: Parser object
    Returns:
        None
    """
    parser.add_argument('--aid', default='485294',
                        help='the id of assay',
                        type=str)
    parser.add_argument('-o',
                        '--output', default='./',
                        help='the folder to save result',
                        type=str)
    parser.add_argument('--n_jobs', default=1,
                        help='the number of processor to used',
                        type=int)    
    

def main():
    PARSER = argparse.ArgumentParser()
    add_arguments(PARSER)
    args = PARSER.parse_args()
    
    download = HugeDownloader(args)
    download.downloadAssay()
    

if '__main__'  ==__name__:
    main()