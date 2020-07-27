# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 08:37:19 2020

@Author: Zhi-Jiang Yang, Dong-Sheng Cao
@Institution: CBDD Group, Xiangya School of Pharmaceutical Science, CSU, China
@Homepage: http://www.scbdd.com
@Mail: yzjkid9@gmail.com; oriental-cds@163.com
@Blog: https://blog.iamkotori.com

♥I love Princess Zelda forever♥
"""


from rdkit import Chem
import openbabel as ob
from itertools import compress
from scopy.ScoTox import Toxfilter
from scopy.ScoFH import FHfilter
from scopy.ScoDruglikeness import PC_rules, PC_properties




class Filter(Toxfilter, FHfilter, PC_rules, PC_properties):
    
    def obsmitosmile(self,smiles):
        conv = ob.OBConversion()
        conv.SetInAndOutFormats("smi", "can")
        conv.SetOptions("K", conv.OUTOPTIONS)
        mol = ob.OBMol()
        conv.ReadString(mol, smiles)
        smile = conv.WriteString(mol)
        smile = smile.replace('\t\n', '')
        return smile
    
    def getMol(self, smiles):
        """
        """
        mol = Chem.MolFromSmiles(smiles)
        if not mol:
            mol = Chem.MolFromSmiles(self.obsmitosmile(smiles)) 
        return mol
    
    def __init__(self, data, smiles_field='SMILES'):
        
        self.smiles = data[smiles_field].values
        self.mols = list(map(self.getMol, self.smiles))
        self.data = data
        
        Toxfilter.__init__(self, self.mols, n_jobs=-1)
        FHfilter.__init__(self, self.mols, n_jobs=-1)
        PC_rules.__init__(self, self.mols, n_jobs=-1)
        PC_properties.__init__(self, self.mols, n_jobs=-1)

    def runfilter(self):
        
        def trans(dic):
            return [1 if x['Disposed']=='Accepted' else 0 for x in dic]
        
# =============================================================================
#         Drug-likeness
# =============================================================================
        sa = self.CalculateSAscore() #SA score
        ro5 = self.CheckLipinskiRule() #Linpinski Rule
        
# =============================================================================
#         Frequent-Hitters
# =============================================================================
        pains = self.Check_PAINS() #PAINS
        bms = self.Check_BMS() #BMS
        
# =============================================================================
#         Toxicity
# =============================================================================
        # ele = self.Check_Potential_Electrophilic()
        ld50 = self.Check_LD50_Oral()
        ames = self.Check_Genotoxic_Carcinogenicity_Mutagenicity()
        
        sureChEMBL = self.Check_SureChEMBL()
        ntd = self.Check_NTD()
        
        
        res = pd.DataFrame({'Linpinski': trans(ro5),
                            'PAINS': trans(pains),
                            'BMS': trans(bms),
                            # 'PotentialElectrophilic': trans(ele),
                            'LD50': trans(ld50),
                            'GenotoxicCarcinogenicityMutagenicity': trans(ames),
                            'sureChEMBL': trans(sureChEMBL),
                            'NTD': trans(ntd)})
        
        res['Summary'] = (res==1).all(axis=1).values + 0
        res['SA_Score'] = sa
        res = pd.concat((self.data, res), axis=1)
        
        out1 = res[res['Summary']==1]
        out2 = res[res['Summary']!=1]
        
        
        return out1, out2
        
        
        

if '__main__' == __name__:
    import pandas as pd
    
    data = pd.read_csv(r'iter_1.csv')
    f = Filter(data, 'Transformed Molecule')
    res = f.runfilter()
    
        
        
        
        
        
              
        
        
        
        
        
        
        
        
        