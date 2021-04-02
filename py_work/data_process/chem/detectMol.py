'''
Description: the script detect the composition of molecules
Author: Kotori Y
Date: 2021-04-02 17:11:21
LastEditors: Kotori Y
LastEditTime: 2021-04-02 17:18:10
FilePath: \kotori_work\py_work\data_process\chem\detectMol.py
AuthorMail: kotori@cbdd.me
'''
from rdkit import Chem


def detectMoleculeComposition(mol, elements=[6, 7, 8]):
    """Detect the composition of molecules

    Parameters
    ----------
    mol : rdkit.Chem.rdchem.Mol
        molecule to be detected
    elements : list, optional
        the only allow atomic number of ATOM in mol, by default [6, 7, 8]

    Returns
    -------
    [type]
        [description]
    """
    nAtoms = mol.GetNumAtoms()

    elements = [f"#{elem}" for elem in elements]
    smarts = f"[!*,{','.join(elements)}]"

    patt = Chem.MolFromSmarts(smarts)
    detectNum = mol.GetSubstructMatches(patt)

    return (nAtoms == len(detectNum))


if "__main__" == __name__:
    smis = ("C1CCOC(CNCCCCC)C1", "C1CCSC(CCCCCCC)C1", "c1ccncc1")
    for smi in smis:
        mol = Chem.MolFromSmiles(smi)
        print(detectMoleculeComposition(mol, [6, 7, 8])) # C, N, O
