from typing import List

import rdkit
from rdkit import Chem


class MolRemover:
    def __init__(self):
        self.METAL_LIST = [
            3,  # Li Lithium
            4,  # Be Beryllium
            11,  # Na Sodium
            12,  # Mg Magnesium
            13,  # Al Aluminum
            19,  # K Potassium
            20,  # Ca Calcium
            21,  # Sc Scandium
            22,  # Ti Titanium
            23,  # V Vanadium
            24,  # Cr Chromium
            25,  # Mn Manganese
            26,  # Fe Iron
            27,  # Co Cobalt
            28,  # Ni Nickel
            29,  # Cu Copper
            30,  # Zn Zinc
            31,  # Ga Gallium
            37,  # Rb Rubidium
            38,  # Sr Strontium
            39,  # Y Yttrium
            40,  # Zr Zirconium
            41,  # Nb Niobium
            42,  # Mo Molybdenum
            43,  # Tc Technetium
            44,  # Ru Ruthenium
            45,  # Rh Rhodium
            46,  # Pd Palladium
            47,  # Ag Silver
            48,  # Cd Cadmium
            49,  # In Indium
            50,  # Sn Tin
            55,  # Cs Cesium
            56,  # Ba Barium
            57,  # La Lanthanum
            58,  # Ce Cerium
            59,  # Pr Praseodymium
            60,  # Nd Neodymium
            61,  # Pm Promethium
            62,  # Sm Samarium
            63,  # Eu Europium
            64,  # Gd Gadolinium
            65,  # Tb Terbium
            66,  # Dy Dysprosium
            67,  # Ho Holmium
            68,  # Er Erbium
            69,  # Tm Thulium
            70,  # Yb Ytterbium
            71,  # Lu Lutetium
            72,  # Hf Hafnium
            73,  # Ta Tantalum
            74,  # W Tungsten
            75,  # Re Rhenium
            76,  # Os Osmium
            77,  # Ir Iridium
            78,  # Pt Platinum
            79,  # Au Gold
            80,  # Hg Mercury
            81,  # Tl Thallium
            82,  # Pb Lead
            83,  # Bi Bismuth
            84,  # Po Polonium
            87,  # Fr Francium
            88,  # Ra Radium
            89,  # Ac Actinium
            90,  # Th Thorium
            91,  # Pa Protactinium
            92,  # U Uranium
            93,  # Np Neptunium
            94,  # Pu Plutonium
            95,  # Am Americium
            96,  # Cm Curium
            97,  # Bk Berkelium
            98,  # Cf Californium
            99,  # Es Einsteinium
            100,  # Fm Fermium
            101,  # Md Mendelevium
            102,  # No Nobelium
            103,  # Lr Lawrencium
            104,  # Rf Rutherfordium
            105,  # Db Dubnium
            106,  # Sg Seaborgium
            107,  # Bh Bohrium
            108,  # Hs Hassium
            109,  # Mt Meitnerium
            110,  # Ds Darmstadtium
            111,  # Rg Roentgenium
            112,  # Cn Copernicium
            113,  # Nh Nihonium
            114,  # Fl Flerovium
            115,  # Mc Moscovium
            116,  # Lv Livermorium
        ]

        self.METALLOIDS_LIST = [
            5,  # B
            14,  # Si
            32,  # Ge
            33,  # As
            51,  # Sb
            52,  # Te
            85,  # At
        ]

    @staticmethod
    def check_mol_valid(mol) -> bool:
        """
        The check_mol_valid function checks if the molecule is valid.

        :param mol: Check if the molecule is valid
        :return: A boolean value
        :doc-author: Trelent
        """
        return mol is not None and type(mol) == rdkit.Chem.rdchem.Mol

    @staticmethod
    def check_mol_with_blocklist(mol: rdkit.Chem.rdchem.Mol, blocklist: List[int]) -> bool:
        """
        The check_mol_with_blocklist function takes a molecule and a list of atom numbers as input.
        It then checks if the molecule is valid, and if it is, it checks to see if any of the atoms in
        the blocklist are present in the molecule. If they are not present, then False is returned; otherwise True.

        :param mol: rdkit.Chem.rdchem.Mol: Specify the molecule that is passed to the function
        :param blocklist: List[int]: Specify the atoms that should be blocked
        :return: True if the molecule contains any of the atoms in blocklist
        :doc-author: Trelent
        """
        if MolRemover.check_mol_valid(mol):
            for atom in blocklist:
                patt = Chem.MolFromSmarts(f"[#{atom}]")
                if patt is not None and mol.HasSubstructMatch(patt):
                    return True
        return False

    def remove_mol_with_metal(self, mol: rdkit.Chem.rdchem.Mol) -> bool:
        """
        The remove_mol_with_metal function removes molecules that contain metals.

        :param self: Bind the method to a class
        :param mol: rdkit.Chem.rdchem.Mol: Pass in the molecule to be checked
        :return: A boolean value
        :doc-author: Trelent
        """
        return self.check_mol_with_blocklist(mol, self.METAL_LIST)

    def remove_mol_with_metalloids(self, mol: rdkit.Chem.rdchem.Mol) -> bool:
        """
        The remove_mol_with_metalloids function removes molecules that contain metalloids.

        :param self: Bind the method to a class
        :param mol: rdkit.Chem.rdchem.Mol: Pass in the molecule that is being checked
        :return: True if the molecule contains a metalloid
        :doc-author: Trelent
        """
        return self.check_mol_with_blocklist(mol, self.METALLOIDS_LIST)


if __name__ == "__main__":
    smiles = [
        "[Se]([Se]c1c([N+](=O)[O-])cccc1)c1c([N+](=O)[O-])cccc1",
        "CC12[Fe]3456(C1(C)C3(C)C4(C)C25C)C1(C)C6(C)C(C)C(C)C1C",
        "Clc1c(Cl)ccc(N2C(=O)CC(NC(=O)C(=C)C)=N2)c1",
        "[Ge](c1ccccc1)(c1ccccc1)(c1ccccc1)c1ccccc1",
        "S(C)c1c(C(=O)O)c(C)nc(-c2ccc(F)cc2)n1",
        'test'
    ]
    mols = [Chem.MolFromSmiles(smi) for smi in smiles]

    mvs = MolRemover()
    res = {}
    for i, _mol in enumerate(mols):
        res[smiles[i]] = not mvs.check_mol_valid(_mol) or mvs.remove_mol_with_metal(_mol) or mvs.remove_mol_with_like_metal(_mol)

    print(res)

