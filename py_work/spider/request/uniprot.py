

import xml.etree.ElementTree as ET
import requests
from lxml import etree




def Uniprot2Chembl(uniprotID: str):
    chemblID = ""
    try:
        searchUrl = f"https://www.ebi.ac.uk/chembl/api/data/target/search.xml?q={uniprotID}"

        resp = requests.get(searchUrl)
        xml = resp.text

        tree = ET.fromstring(xml)

        targets = tree.find("targets").findall("target")
        for target in targets:
            if target.find("organism").text == "Homo sapiens":
                chemblID = target.find("target_chembl_id").text
                return chemblID
    except :
        pass
    return chemblID


def search_target_in_chembl(chemblID: str):

    try:
        targetUrl = f"https://www.ebi.ac.uk/chembl/api/data/target/{chemblID}.xml"
        resp = requests.get(targetUrl)
        xml = resp.text
        tree = ET.fromstring(xml)
        component_id = tree.find("*//component_id").text

        componentUrl = f"https://www.ebi.ac.uk/chembl/api/data/target_component/{component_id}.xml"
        resp = requests.get(componentUrl)
        xml = resp.text
        tree = ET.fromstring(xml)
        protein_classification_id = tree.find("*//protein_classification_id").text

        protein_class_url = f"https://www.ebi.ac.uk/chembl/api/data/protein_class/{protein_classification_id}.json"
        resp = requests.get(protein_class_url)
        data = resp.json()

        out = list(data.values())
        
        for _ in range(8 - len(out)):
            out.append(None)

    except:
        out = [None]*8
    
    return out


def main(uniprotID):
    print(uniprotID)
    chemblID = Uniprot2Chembl(uniprotID)
    clf = search_target_in_chembl(chemblID)
    return clf
    


if "__main__" == __name__:
    import pandas as pd
    import multiprocessing as mp
    
        
    data = pd.read_excel(r"C:\Users\0720\Desktop\MATE\xgl\Additional file1.xlsx")
    data = data.sample(4)
    pool = mp.Pool()
    out = pool.map_async(main, data.UniprotID.values).get()
    pool.close()
    pool.join()
    
    out = dict(zip(data.UniprotID.values, out))
    out = pd.DataFrame(out)
    
    print(out)
    
    # uniprotID = "O00408"
    # # chemblID = "CHEMBL4296087"
    # chemblID = Uniprot2Chembl(uniprotID)
    # clf = search_target_in_chembl(chemblID)
    # print(clf)
    
    
    
    
    
    
    
    
    