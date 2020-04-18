#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/05/22 16:13
# @Author  : Catkin
# @Website : blog.catkin.moe

import datetime,time,requests,re,random,model,warnings
import pandas as pd
from bs4 import BeautifulSoup
from collections import OrderedDict  
from requests_toolbelt import MultipartEncoder
import multiprocessing as mp


"""
THANKS FOR MY FRIEND: CATKIN
"""


def HitPickV2(smile):
    # http://mips.helmholtz-muenchen.de/HitPickV2/target_prediction.jsp
    smiles = '1 '+smile+'\n'
    try:
        url = 'http://mips.helmholtz-muenchen.de/HitPickV2/TargetPredictionController'   
        s = requests.session()
        data = {
            'list_smiles': (None,smiles),
            "exp": (None,None,'application/octet-stream'),
        }
        response = s.post(url, files=data,timeout=60)
        patterns_x = re.compile('var fileId = "(.*?)";')
        x = re.findall(patterns_x,response.text)[0]
        status_url = 'http://mips.helmholtz-muenchen.de/HitPickV2/StatusController?processID='+x
        y = []
        while y == []:
            status_response = s.get(status_url,timeout=60).text
            patterns_y = re.compile('(.*?)/')
            y = re.findall(patterns_y,status_response)
            if y != []:
                break
            time.sleep(120)
        fid = y[0]
        download_url = 'http://mips.helmholtz-muenchen.de/HitPickV2/results/'+fid+'//Step1_Results_Prediction/Results/all_compounds_targets.json'
        temp = pd.read_json(download_url,orient='split')
        df = pd.DataFrame(columns=["Query Compound","Predicted/Known Target","Protein Complex","Most Similar Compound","Precision","Tc"])
        df["Query Compound"]=temp[0]
        df["Predicted/Known Target"]=temp[2]
        df["Protein Complex"]=temp[3]
        df["Precision"]=temp[5]
        df["Tc"]=temp[4]
        df["Most Similar Compound"]=temp[1]
        df.sort_values(by='Precision',ascending=False,inplace=True)
    except:
        df = pd.DataFrame()
    return df

def swiss(smile):
    # http://www.swisstargetprediction.ch/
    try:
        start_url = 'http://www.swisstargetprediction.ch/predict.php'
        s = requests.session()
        body = {"organism": 'Homo_sapiens', "smiles": smile, "Example": ""}
        response = s.post(start_url, data=body, timeout=60)
        patterns = re.compile('location.replace\("(.*?)"\);')
        x = re.findall(patterns,response.text)[0]
        result_url = 'http://www.swisstargetprediction.ch/'+x
        time.sleep(15)
        page = s.get(result_url,timeout=60).text
        df = pd.read_html(page,header=0)[0]
        clean_actives = [x.replace(' &nbsp','') for x in df['Known actives (3D/2D)']]
        df['Known actives (3D/2D)'] = clean_actives
    except:
        df = pd.DataFrame()
    return df
    
def ChEMBL(smile):
    info_data = pd.read_csv('Target_Info_ver2.csv',sep='\t',index_col=0)
    dicts = OrderedDict()
    HEAD = 30
    for value in [1,10]:
        themodel = model.modelofChEMBL(value)
        dicts['ChEMBL_'+str(value)] = model.ChEMBL(smile,value,HEAD,info_data,themodel)
    return dicts

def ppb(smile):
    # http://gdbtools.unibe.ch:8080/PPB/
    try:
        url = 'http://gdbtools.unibe.ch:8080/PPB/search.jsp?tarnum=20&group4=APfp&group1=Shape&group2=Mqn&group3=Smi&group5=sFP&group6=ecFP&group7=sh_smi_sf&group8=sh_smi_mqn&group9=sh_smi_sf_ec&group10=sh_mq_smi_sf_ec&pdbID=&mask=&smi='+smile+'&fp=&searchMethod=&searchLimit=&PDB_LIGANDS=&PDB_LIGANDS_smi=&inputMol='+smile+'&testMode=OFF&testMolTars=&testMolName=null'
        s = requests.session()
        response = s.get(url,timeout=60)
        df = pd.DataFrame(columns=['Rank', 'ChEMBL-ID', 'ChEMBL-Name','Target Full Name', 'APfp', 'Xfp', 'MQN', 'SMIfp',
           'Sfp', 'ECfp4', 'Ffp1', 'Ffp2', 'Ffp3', 'Ffp4', 'identical'])
        soup = BeautifulSoup(response.text,'lxml')
        text = soup.find('textarea',id="tarea").get_text().strip('\n')
        r_text = text.replace(' ','\t')
        r_list = r_text.split('\n')
        t = [x.split('\t') for x in r_list]
        temp = pd.DataFrame(t)
        df['Rank'] = temp.index + 1
        df['Target Full Name'] = temp[2]
        df['ChEMBL-ID'] = temp[1]
        df['ChEMBL-Name'] = temp[0]    
        for idx in range(len(df)):
            df.iloc[idx,4:14] = list(temp.iloc[idx,13:23])
            if temp.iloc[idx,33] == 'YES':
                df.iloc[idx,-1] = 1
            else:
                df.iloc[idx,-1] = 0
    except:
        df = pd.DataFrame()
    return df

def ppb2(smile):
    # http://ppb2.gdb.tools/
    urls = OrderedDict([
            ('NN(ECfp4)',
              'http://ppb2.gdb.tools/predict?smi='+smile+'&fp=ECfp4&method=Sim&scoringmethod=TANIMOTO'),
             ('NN(Xfp)',
              'http://ppb2.gdb.tools/predict?smi='+smile+'&fp=Xfp&method=Sim&scoringmethod=CBD'),
             ('NN(MQN)',
              'http://ppb2.gdb.tools/predict?smi='+smile+'&fp=MQN&method=Sim&scoringmethod=CBD'),
             ('NN(ECfp4) + NB(ECfp4)',
              'http://ppb2.gdb.tools/predict?smi='+smile+'&fp=ECfp4&method=SimPlusNaiveBayes&scoringmethod=TANIMOTO'),
             ('NN(Xfp) + NB(ECfp4)',
              'http://ppb2.gdb.tools/predict?smi='+smile+'&fp=Xfp&method=SimPlusNaiveBayes&scoringmethod=CBD'),
             ('NN(MQN) + NB(ECfp4)',
              'http://ppb2.gdb.tools/predict?smi='+smile+'&fp=MQN&method=SimPlusNaiveBayes&scoringmethod=CBD'),
             ('NB(ECfp4)',
              'http://ppb2.gdb.tools/predict?smi='+smile+'&fp=ECfp4&method=NaiveBayes&scoringmethod=TANIMOTO'),
             ('DNN(ECfp4)',
              'http://ppb2.gdb.tools/predict?smi='+smile+'&fp=ECfp4&method=DNN&scoringmethod=TANIMOTO')
             ])
    dicts = OrderedDict()
    for idx,method in enumerate(urls.keys()):
        url = urls[method]
        def getDF(url):
            s = requests.session()
            response = s.get(url)
            df = pd.read_html(response.text,header=0)[1]
            df.columns=['Rank', 'ChEMBL ID', 'Common name','Method_ID']
            df['Method_ID'] = method
            return df
        try:
            dicts[method] = getDF(url)
        except:
            dicts[method] = pd.DataFrame()
    return dicts

def spider(smile):
    # http://modlabcadd.ethz.ch/software/spider/
    try:
        url = 'http://modlabcadd.ethz.ch/software/spider/'
        s = requests.session()
        res = s.get(url,timeout=60)
        start_url = 'http://modlabcadd.ethz.ch/software/spider/Form'
        patterns_s = re.compile('name="SecurityID" value="(.*?)" class="hidden"')
        SecurityID = re.findall(patterns_s,res.text)[0]
        body = {"SpiderMoleculeName": "1", "SpiderMoleculeSmiles": smile, "SpiderAgreement": "1", "action_FormDo": "Submit", "SecurityID": SecurityID}
        response = s.post(start_url, data=body, timeout=60)    
        patterns_x = re.compile('<a href="/software/spider/spider-results/\?jid=(.*?)#top">')
        x = re.findall(patterns_x,response.text)[0]
        result_url = 'http://modlabcadd.ethz.ch/software/spider/spider-results/?jid='+x
        y0 = []
        while y0 == []:
            page = requests.get(result_url,timeout=60).text
            patterns_y = re.compile('"(.*?)result.dat">DOWNLOAD</a></td>')
            y0 = re.findall(patterns_y,page)
            time.sleep(5)
        y = y0[0]
        download_url = 'http://modlabcadd.ethz.ch'+y+'result.dat'
        result = requests.get(download_url,timeout=60).text.strip('\n')
        if "Sorry, it seems you were trying to access a page that doesn't exist." in result:
            df = pd.DataFrame()
        else:
            r_list = result.split('\n')
            t = [x.split('\t') for x in r_list]
            df = pd.DataFrame(t)
            columns = ['ID','Target','Confidence Level']
            df.columns = columns
    except:
        df = pd.DataFrame()
    return df

def SEA(smile):
    try:
        start_url = 'http://sea.bkslab.org/search'
        data = {
            'ref_type': 'library',
            'ref_library_id': 'default',
            'query_type': 'custom',
            'query_custom_targets_paste': smile,
        }
        r = requests.Session()
        response = r.post(url=start_url, data=data, timeout=60)
        page = r.get(response.url,timeout=60).text
        while 'This page will periodically referesh to check' in page:
            time.sleep(15)
            page = r.get(response.url,timeout=60).text
        df = pd.read_html(page,header=0)[0]
        page = re.sub('<th>Query</th>', '', page, re.S)
        page = re.sub('(<tr class="spanning info">[\w\W]*?</tr>)', '', page, re.S)
        if (pd.isnull(df.iloc[0,1]) & pd.isnull(df.iloc[0,2]) & pd.isnull(df.iloc[0,3]) & pd.isnull(df.iloc[0,4])):
            df.drop(0, axis=0, inplace=True)
    except:
        df = pd.DataFrame()
    return df

def TargetHunter(smile):
    # https://www.cbligand.org/TargetHunter/search_target.php
    try:
        login_url = 'https://www.cbligand.org/TargetHunter/login.php'
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
              'Connection': 'close',
              }
        data = {
            'usrname': 'catkin7',
            'usrpasswd': 'y7B5@t!g',
            'btnLogin2': 'Login',
            }
        r = requests.Session()
        response = r.post(url=login_url, data=data, headers=header,timeout=60,verify=False)
        search_url = 'https://www.cbligand.org/TargetHunter/search_target.php'
        
        data = {
            "File1":(None, '', 'application/octet-stream'),
            "hiddensmi":(None, smile),
            "Smiles":(None, smile),
            "Fingerprint":(None, 'FP2'),
            "searchtype":(None, 'sim2d'),
            "similarity":(None, '60'),
            "ChEMBL":(None, 'on'),
            "PubChem":(None, 'on'),
            "Submit":(None, 'Submit'),
            }
        page = r.post(search_url, files=data, headers=header,timeout=60).text
        patterns = re.compile('(wrk\d*)')
        wrkid = re.findall(patterns,page)[0]
        result_url = 'https://www.cbligand.org/TargetHunter/retrieve_target.php?similarity=60&dir='+wrkid+'&FP=FP2'
        result_page = r.get(result_url, headers=header,timeout=60).text
        df = pd.read_html(result_page,header=0)[1]
        clean_target = [x.replace('Find Assays Nearby','') for x in df['Target']]
        df['Target'] = clean_target
    except:
        df = pd.DataFrame()
    return df

def PASSonline(smile):
    # http://www.pharmaexpert.ru/passonline/predict.php
    try:
        login_url = 'http://www.pharmaexpert.ru/passonline/predict.php'
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
                  'Connection': 'close',
                  }
        data = {
            'user_login': 'cenuswei',
            'user_password': 'f353630039',
            }
        r = requests.Session()
        response = r.post(url=login_url, data=data, headers=header,timeout=60)
        resid_url = 'http://www.pharmaexpert.ru/passonline/result_id.php'
        data = {
            'smi': smile,
            }
        result_id = r.post(url=resid_url, data=data, headers=header,timeout=60).text.strip()
        pred1_url = 'http://www.pharmaexpert.ru/passonline/pred1.php?id_task='+result_id+'&ots=4'
        page1 = r.get(url=pred1_url,headers=header,timeout=60).text
        while 'automatically updated every 10 seconds' in page1:
            time.sleep(10)
            page1 = r.get(url=pred1_url,headers=header,timeout=60).text
        df = pd.read_html(page1,header=0,thousands=None)[0]
        df.columns=['Probability to be active', 'Probability to be inactive', 'Biological Activity']
    except:
        df = pd.DataFrame()
    return df

def ChemMapper(smile):
    # http://www.lilab-ecust.cn/chemmapper/    
    t1 = time.time()
    try:
        url = 'http://www.lilab-ecust.cn/chemmapper/submitform.html'
        sets = [chr(i) for i in range(65,91)] + [chr(i) for i in range(97,123)] + [ str(i) for i in range(10)] #大写字母+小写字母+数字
        num = random.sample(sets,16) 
        randomStr = ''.join(num) 
        boundary = '----WebKitFormBoundary'+randomStr
        header = {  
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': '1310',
        'Content-Type': 'multipart/form-data; boundary='+boundary,
        'DNT': '1',
        'Host': 'www.lilab-ecust.cn',
        'Origin': 'http://www.lilab-ecust.cn',
        'Referer': 'http://www.lilab-ecust.cn/chemmapper/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
              }
        params = {
            'smiles': (None, smile, None),
            'inputFile': ('', None, 'application/octet-stream'),
            'jobName': (None, 'None', None),
            'email': (None, None, None),
            'targetMethod': (None, 'tar', None),
            'program': (None, 'FeatureAlign', None),
            'targetData': (None, 'DrugBank', None),
            'bioDbSel': (None, '1', None),
            'dbctrl': (None, '1', None),
            'screenDatabase': (None, 'NCI', None),
            '_generateConf': (None, 'on', None),
            'threshold': (None, '1.2', None),
                  }
        r = requests.Session()
        data = MultipartEncoder(boundary=boundary,fields = params)
        page = r.post(url=url, data=data, headers=header,timeout=60).text    
        
        patterns = re.compile('<span style="color: red;">(\d*)</span>')
        jobid = re.findall(patterns,page)[0]
        
        status_url = 'http://www.lilab-ecust.cn/chemmapper/result/status.html?jobId='+jobid
        status_code = r.get(url=status_url,timeout=60).text
        while status_code != "complete":
            time.sleep(10)
            status_code = r.get(url=status_url,timeout=60).text
            t2 = time.time()
            if t2-t1>1200:
                df = pd.DataFrame()
                return df
            if status_code == "complete":
                break
        result_url = 'http://www.lilab-ecust.cn/chemmapper/result/getResult.html?jobId='+jobid
        result_page = r.get(url=result_url,timeout=60).text    
        df = pd.read_html(result_page,header=0)[0].iloc[:,2:]
        df.drop(df.index[-1], axis=0, inplace=True)
    except:
        df = pd.DataFrame()
    return df

def main(status):
    '''
    Please Enter the number to choose mode:
    1:HitPickV2
    2:swiss
    3:ppb
    4:spider
    5:SEA
    6:TargetHunter
    7:PASSonline
    8:ChemMapper
    9:ChEMBL
    10:ppb2
    11:All
    12:Quit
    '''
    modes = OrderedDict([(1,'HitPickV2'),(2,'swiss'),(3,'ppb'),(4,'spider'),(5,'SEA'),(6,'TargetHunter'),
            (7,'PASSonline'),(8,'ChemMapper'),(9,'ChEMBL'),(10,'ppb2'),(11,'All'),(12,'Quit'),])
    mode = input('Choose the mode: ')
    starttime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    if mode == '1':
        smile = input('Enter the smile: ')
        df = HitPickV2(smile)
        df.to_excel('result_'+starttime+'.xlsx',index=False)
    elif mode == '2':
        smile = input('Enter the smile: ')
        df = swiss(smile)
        df.to_excel('result_'+starttime+'.xlsx',index=False)
    elif mode == '3':
        smile = input('Enter the smile: ')
        df = ppb(smile)
        df.to_excel('result_'+starttime+'.xlsx',index=False)    
    elif mode == '4':
        smile = input('Enter the smile: ')
        df = spider(smile)
        df.to_excel('result_'+starttime+'.xlsx',index=False)  
    elif mode == '5':
        smile = input('Enter the smile: ')
        df = SEA(smile)
        df.to_excel('result_'+starttime+'.xlsx',index=False)   
    elif mode == '6':
        smile = input('Enter the smile: ')
        df = TargetHunter(smile)
        df.to_excel('result_'+starttime+'.xlsx',index=False)      
    elif mode == '7':
        smile = input('Enter the smile: ')
        df = PASSonline(smile)
        df.to_excel('result_'+starttime+'.xlsx',index=False)    
    elif mode == '8':
        smile = input('Enter the smile: ')
        df = ChemMapper(smile)
        df.to_excel('result_'+starttime+'.xlsx',index=False)       
    elif mode == '9':
        smile = input('Enter the smile: ')
        writer = pd.ExcelWriter('result_'+starttime+'.xlsx',engine='openpyxl')
        dicts = ChEMBL(smile)
        for key in dicts.keys():    
            temp = dicts[key]
            temp.to_excel(writer,sheet_name=key,index=False)
        writer.save()               
    elif mode == '10':
        smile = input('Enter the smile: ')
        writer = pd.ExcelWriter('result_'+starttime+'.xlsx',engine='openpyxl')
        dicts = ppb2(smile)
        for key in dicts.keys():    
            temp = dicts[key]
            temp.to_excel(writer,sheet_name=key,index=False)
        writer.save()            
    elif mode == '11':
        smile = input('Enter the smile: ')
        pool = mp.Pool(10)
        t1 = pool.apply_async(HitPickV2,args=(smile, ))
        t2 = pool.apply_async(swiss,args=(smile, ))
        t3 = pool.apply_async(ppb,args=(smile, ))
        t4 = pool.apply_async(spider,args=(smile, ))
        t5 = pool.apply_async(SEA,args=(smile, ))
        t6 = pool.apply_async(TargetHunter,args=(smile, ))
        t7 = pool.apply_async(PASSonline,args=(smile, ))
        t8 = pool.apply_async(ChemMapper,args=(smile, ))
        t9 = pool.apply_async(ChEMBL,args=(smile, ))
        t10 = pool.apply_async(ppb2,args=(smile, ))
        writer = pd.ExcelWriter('result_'+starttime+'.xlsx',engine='openpyxl')
        for i in range(1,9):
            a = eval('t'+str(i)).get()
            print(modes[i]+' done...')
            a.to_excel(writer,sheet_name=modes[i],index=False)
        chembl_dicts = t9.get()
        for key in chembl_dicts.keys():    
            temp = chembl_dicts[key]
            temp.to_excel(writer,sheet_name=key,index=False)        
        ppb2_dicts = t10.get()
        for key in ppb2_dicts.keys():    
            temp = ppb2_dicts[key]
            temp.to_excel(writer,sheet_name=key,index=False)     
        writer.save()            
    elif mode == '12':
        status = False
    else:
        print('Please enter correct mode!')
    return status

if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    status = True
    while status is True:
        print(main.__doc__)
        status = main(status)
