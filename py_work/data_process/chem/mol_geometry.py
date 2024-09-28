from itertools import product
import rdkit
from rdkit import Chem
import numpy as np
from rdkit.Chem import rdMolTransforms


class MolGeometryCovert:

    @staticmethod
    def _get_angle(vec1, vec2):
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        if norm1 == 0 or norm2 == 0:
            return 0
        vec1 = vec1 / (norm1 + 1e-5)  # 1e-5: prevent numerical errors
        vec2 = vec2 / (norm2 + 1e-5)
        angle = np.arccos(np.dot(vec1, vec2))
        return angle

    @staticmethod
    def _get_dihedral(a, b, c, d):
        # v_ba = a - b
        # v_bc = c - b
        # nabc = np.cross(v_ba, v_bc)
        #
        # v_cb = b - c
        # v_cd = d - c
        # nbcd = np.cross(v_cb, v_cd)
        #
        # t = np.sqrt(np.dot(nabc, nabc) * np.dot(nbcd, nbcd))
        # if t == 0:
        #     return 0
        #
        # temp = np.dot(nabc, nbcd) / t
        # temp = 1 if temp > 1 else temp
        # temp = -1 if temp < -1 else temp
        # theta = np.arccos(temp)
        # return theta

        # 计算向量AB、BC和CD
        AB = b - a
        BC = c - b
        CD = d - c

        # 计算平面ABC和平面BCD的法向量
        N1 = np.cross(AB, BC)
        N2 = np.cross(BC, CD)

        # 计算N1和N2之间的夹角
        dot_product = np.dot(N1, N2)
        cross_product_norm = np.linalg.norm(np.cross(N1, N2))
        angle = np.arctan2(cross_product_norm, dot_product)

        if angle > np.pi:
            angle -= 2 * np.pi

        return angle

    @staticmethod
    def get_mol_angle(bonds, atom_poses):
        E = len(bonds)
        edge_indices = np.arange(E)

        super_atoms = []
        super_edges = []
        bond_angles = []

        for tar_edge_i in range(E):
            tar_edge = bonds[tar_edge_i]
            src_edge_indices = edge_indices[bonds[:, 1] == tar_edge[0]]

            for src_edge_i in src_edge_indices:
                if src_edge_i == tar_edge_i:
                    continue

                src_edge = bonds[src_edge_i]

                super_edges.append([src_edge_i, tar_edge_i])
                super_atoms.append([*bonds[src_edge_i], *bonds[tar_edge_i]])

                angle = MolGeometryCovert._get_angle(
                    atom_poses[src_edge[0]] - atom_poses[src_edge[1]],
                    atom_poses[tar_edge[1]] - atom_poses[tar_edge[0]]
                )
                bond_angles.append(angle)

        super_atoms = np.array(super_atoms, 'int64')
        super_edges = np.array(super_edges, 'int64')
        bond_angles = np.array(bond_angles, 'float32')

        return super_edges, super_atoms, bond_angles

    @staticmethod
    def get_mol_dihedral(mol, super_bonds, bonds):
        E = len(super_bonds)
        superedge_indices = np.arange(E)

        ultra_atoms = []
        ultra_bonds = []
        dihedral_angles = []

        for tar_superedge_i in range(E):
            tar_superedge = super_bonds[tar_superedge_i]

            src_superedge_indices = superedge_indices[super_bonds[:, 1] == tar_superedge[0]]

            for src_superedge_i in src_superedge_indices:
                if src_superedge_i == tar_superedge_i:
                    continue

                src_superedge = super_bonds[src_superedge_i]

                src_edge_pair = [bonds[src_superedge[0]], bonds[src_superedge[1]]]
                tar_edge_pair = [bonds[tar_superedge[0]], bonds[tar_superedge[1]]]

                if (src_edge_pair[1] != tar_edge_pair[0]).any():
                    continue

                ultra_bonds.append([src_superedge_i, tar_superedge_i])

                tmp = [*super_bonds[src_superedge_i], *super_bonds[tar_superedge_i]]
                # if src_superedge_i == 85 and tar_superedge_i == 101:
                if src_superedge_i == 90 and tar_superedge_i == 9:
                # if src_superedge_i == 84 and tar_superedge_i == 101:
                    print('')
                ultra_atoms.append([*bonds[tmp[0]], *bonds[tmp[1]], *bonds[tmp[2]], *bonds[tmp[3]]])

                a = int(src_edge_pair[0][0])
                b = int(src_edge_pair[0][1])
                c = int(tar_edge_pair[1][0])
                d = int(tar_edge_pair[1][1])

                # dihedral = MolGeometryCovert._get_dihedral(a, b, c, d) * 1
                dihedral = rdMolTransforms.GetDihedralRad(mol.GetConformer(), a, b, c, d)
                dihedral_angles.append(dihedral)

        ultra_bonds = np.array(ultra_bonds, 'int64')
        dihedral_angles = np.array(dihedral_angles, 'float32')
        return ultra_bonds, ultra_atoms, dihedral_angles


    @staticmethod
    def mol_to_geometry(mol: rdkit.Chem.rdchem.Mol):
        bonds = []
        for bond in mol.GetBonds():
            atom_i = bond.GetBeginAtomIdx()
            atom_j = bond.GetEndAtomIdx()

            bonds += [(atom_i, atom_j), (atom_j, atom_i)]

        bonds = np.array(bonds)
        atom_poses = mol.GetConformer().GetPositions()

        super_bonds, super_atoms, bond_angles = MolGeometryCovert.get_mol_angle(bonds, atom_poses)
        ultra_bonds, ultra_atoms, dihedral_angles = MolGeometryCovert.get_mol_dihedral(mol, super_bonds, bonds)

        return super_bonds, super_atoms, bond_angles


if __name__ == "__main__":
    m = Chem.MolFromMolFile('./data/Conformer3D_COMPOUND_CID_2244.sdf', removeHs=False)
    MolGeometryCovert.mol_to_geometry(m)

    print("DONE!!!")
