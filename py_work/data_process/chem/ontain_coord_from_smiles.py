import numpy as np
from rdkit.Chem import AllChem as Chem


def get_MMFF_atom_poses(mol, numConfs=None, return_energy=False):
    """the atoms of mol will be changed in some cases."""
    conf = None
    try:
        new_mol = Chem.AddHs(mol)
        Chem.EmbedMultipleConfs(new_mol, numConfs=numConfs)
        # MMFF generates multiple conformations
        res = Chem.MMFFOptimizeMoleculeConfs(new_mol)
        res = [x for x in res if x[0] == 0]
        new_mol = Chem.RemoveHs(new_mol)
        index = np.argmin([x[1] for x in res])
        energy = res[index][1]
        conf = new_mol.GetConformer(id=int(index))
    except:
        new_mol = mol
        Chem.Compute2DCoords(new_mol)
        energy = 0
        conf = new_mol.GetConformer()

    atom_poses = conf.GetPositions()
    if return_energy:
        return new_mol, atom_poses, energy
    else:
        return new_mol, atom_poses


if __name__ == "__main__":
    smiles = "NS(=O)(=O)c1cc2c(cc1Cl)NC(CSCc1ccccc1)=NS2(=O)=O"
    mol = Chem.MolFromSmiles(smiles)

    get_MMFF_atom_poses(mol, numConfs=3, return_energy=False)
