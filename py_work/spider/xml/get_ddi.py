# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 12:47:42 2018

@author: Kotori_Y
@WEIBO: Michariel
E-mail: yzjkid9@gmail.com

μ’sic Forever♪♪♪♪♪♪♪♪♪
I love Kotori forever(・8・)
"""

import os
import xml.etree.ElementTree as ET
import csv

os.chdir(r'C:\Users\mtdzj04\Desktop')

tree = ET.parse("Structure2D_CID_1.xml")
root = tree.getroot()
##################################################    错误代码示范（逃）    ################################################## 


with open('All_Interactions.csv','a',newline = '') as f:
    writer = csv.writer(f)
    for item in root:
        for drug_a in item.findall('{http://www.drugbank.ca}name'):
            for DDIs in item.findall('{http://www.drugbank.ca}drug-interactions'):                
                for DDI in DDIs.findall('{http://www.drugbank.ca}drug-interaction'):
                    for descri in DDI.findall('{http://www.drugbank.ca}description'):
                        for drug_b in DDI.findall('{http://www.drugbank.ca}name'):
                            for code in DDI.findall('{http://www.drugbank.ca}drugbank-id'):
                                data = [drug_a.text,item[0].text,drug_b.text,code.text,descri.text]
                                writer.writerows([data])

##################################################    错误代码示范（逃）    ##################################################
                                


#正确代码（大概）示范
                                
"""
import os
import csv
import xml.etree.ElementTree as ET

os.chdir(r'C:\Users\mtdzj04\Desktop')

file = 'PubChemAnnotations_source=ChemIDplus.xml'

tree = ET.parse(file)
roots = tree.getroot()

with open('CAS.csv', 'a+', newline = '') as f:
    writer = csv.writer(f)
    writer.writerow(['SourceID', 'Name', 'URL', 'CID', 'CAS'])
    for root in roots:
        for sID, name, url in zip(root.findall('{http://pubchem.ncbi.nlm.nih.gov/}SourceID'), 
                             root.findall('{http://pubchem.ncbi.nlm.nih.gov/}Name'),
                             root.findall('{http://pubchem.ncbi.nlm.nih.gov/}URL')):
            break
        
        for LinkToPubChemBy in root.findall('{http://pubchem.ncbi.nlm.nih.gov/}LinkToPubChemBy'):
            for cid in LinkToPubChemBy.findall('{http://pubchem.ncbi.nlm.nih.gov/}CID'):
                break
            break
        
        for DATA in root.findall('{http://pubchem.ncbi.nlm.nih.gov/}Data'):
            for value in DATA.findall('{http://pubchem.ncbi.nlm.nih.gov/}Value'):
                for string in value.findall('{http://pubchem.ncbi.nlm.nih.gov/}String'):
                    break
                break
            break
        
        data = [sID.text, name.text, url.text, cid.text, string.text]
        writer.writerows([data])
"""