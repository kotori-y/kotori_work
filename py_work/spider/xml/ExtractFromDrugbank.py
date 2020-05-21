# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 13:34:44 2019

You are not expected to understand my codes!

@Author: Kotori_Y
@Blog: blog.moyule.me
@Weibo: Michariel
@Mail: yzjkid9@gmial.com

I love Megumi forerver!
"""

import xml.etree.ElementTree as ET
import os
import pandas as pd

os.chdir(r'C:\DrugBank\ver5.1.2')

file = 'full database.xml'

SMIS = []
MWS = []
MFS = []
INchikey = []
Name = []
Id = []
CAS = []
ATCS = []
http = '{http://www.drugbank.ca}'


tree = ET.parse(file)
drugs = tree.getroot()

for drug in drugs:
    
    SMI = None
    
    MW = None
    
    MF = None
    
    inchikey = None
    ATC = []
    



    name,bank_id,cas = drug.findall(http+'name'),drug[0],drug.findall(http+'cas-number')

    for exp in drug.findall(http+'experimental-properties'):
        for property in exp.findall(http+'property'):
            for kind,value in zip(property.findall(http+'kind'),property.findall(http+'value')):
                if kind.text == 'Molecular Weight':
                    MW = value.text
                elif kind.text == 'Molecular Formula':
                    MF = value.text
                else:
                    pass

    for cal in drug.findall(http+'calculated-properties'):
        for property in cal.findall(http+'property'):
            for kind,value in zip(property.findall(http+'kind'),property.findall(http+'value')):
                if kind.text == 'Molecular Weight' and MW == None:
                    MW = value.text
                elif kind.text == 'SMILES':
                    SMI = value.text
                elif kind.text == 'InChIKey':
                    inchikey = value.text
                elif kind.text == 'Molecular Formula':
                    MF = value.text
                else:
                    pass
    for atcs in drug.findall(http+'atc-codes'):
        for atc in atcs.findall(http+'atc-code'):
            ATC.append(atc.attrib['code'])
    
    Id.append(bank_id.text)
    Name.append(name[0].text)
    MFS.append(MF)
    MWS.append(MW)
    CAS.append(cas[0].text)
    ATCS.append(ATC)
    INchikey.append(inchikey)
    SMIS.append(SMI)
    

df = pd.DataFrame()

df['DrugBank_ID'] = Id

df['Name'] = Name

df['Molecular_Formula'] = MFS

df['Molecular_Weight'] = MWS

df['CAS'] = CAS

df['ATC_Code'] = ATCS

df['InChIKey'] = INchikey

df['SMILES'] = SMIS



#df.to_csv('DrugBank_Version5.1.1.csv',index=False)