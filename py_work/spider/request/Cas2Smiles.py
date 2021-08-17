import json

import requests


def cas_2_smiles(cas):
    """

    Args:
        cas: string, cas number (xxx-yyy-zzz) Length is not fixed

    Returns: string, smiles

    """
    assert len(cas.split("-")) == 3  # check cas number
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{cas}/json"
    resp = requests.get(url)
    out = json.loads(resp.text).get("PC_Compounds", [])
    if out:
        out = out[0]
        props = out.get("props", [])
        for prop in props:
            urn = prop.get("urn", False)
            if urn and (urn.get("name", "") == "Canonical") and (urn.get("label") == "SMILES"):
                return prop.get("value", {}).get("sval", "")
    return None


if "__main__" == __name__:
    cas_ = "12626-15-2"
    smiles = cas_2_smiles(cas_)
    print(smiles)
