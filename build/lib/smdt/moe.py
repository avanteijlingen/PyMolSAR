"""
This module mainly implements the calculation of MOE-type descriptors, which
include LabuteASA, TPSA, slogPVSA, MRVSA, PEOEVSA, EstateVSA and VSAEstate,
respectively (60).
"""

from rdkit import Chem
from rdkit.Chem import MolSurf as MOE
from rdkit.Chem.EState import EState_VSA as EVSA
import pandas as pd

################################################################

def CalculateLabuteASA(mol):
    """
    #################################################################
    Calculation of Labute's Approximate Surface Area (ASA from MOE)

    Usage:

        result=CalculateLabuteASA(mol)

        Input: mol is a molecule object

        Output: result is a dict form
    #################################################################
    """
    res = {}
    temp = MOE.pyLabuteASA(mol, includeHs=1)
    res['LabuteASA'] = round(temp, 3)
    return res


def CalculateTPSA(mol):
    """
    #################################################################
    Calculation of topological polar surface area based on fragments.

    Implementation based on the Daylight contrib program tpsa.

    Usage:

        result=CalculateTPSA(mol)

        Input: mol is a molecule object

        Output: result is a dict form
    #################################################################
    """
    res = {}
    temp = MOE.TPSA(mol)
    res['MTPSA'] = round(temp, 3)
    return res


def CalculateSLOGPVSA(mol, bins=None):
    """
    #################################################################
    MOE-type descriptors using LogP contributions and surface

    area contributions.

    logpBins=[-0.4,-0.2,0,0.1,0.15,0.2,0.25,0.3,0.4,0.5,0.6]

    You can specify your own bins to compute some descriptors.

    Usage:

        result=CalculateSLOGPVSA(mol)

        Input: mol is a molecule object

        Output: result is a dict form
    #################################################################
    """
    temp = MOE.SlogP_VSA_(mol, bins, force=1)
    res = {}
    for i, j in enumerate(temp):
        res['slogPVSA' + str(i)] = round(j, 3)
    return res


def CalculateSMRVSA(mol, bins=None):
    """
    #################################################################
    MOE-type descriptors using MR contributions and surface

    area contributions.

    mrBins=[1.29, 1.82, 2.24, 2.45, 2.75, 3.05, 3.63,3.8,4.0]

    You can specify your own bins to compute some descriptors.

    Usage:

        result=CalculateSMRVSA(mol)

        Input: mol is a molecule object

        Output: result is a dict form
    #################################################################
    """
    temp = MOE.SMR_VSA_(mol, bins, force=1)
    res = {}
    for i, j in enumerate(temp):
        res['MRVSA' + str(i)] = round(j, 3)
    return res


def CalculatePEOEVSA(mol, bins=None):
    """
    #################################################################
    MOE-type descriptors using partial charges and surface

    area contributions.

    chgBins=[-.3,-.25,-.20,-.15,-.10,-.05,0,.05,.10,.15,.20,.25,.30]

    You can specify your own bins to compute some descriptors

    Usage:

        result=CalculatePEOEVSA(mol)

        Input: mol is a molecule object

        Output: result is a dict form
    #################################################################
    """
    temp = MOE.PEOE_VSA_(mol, bins, force=1)
    res = {}
    for i, j in enumerate(temp):
        res['PEOEVSA' + str(i)] = round(j, 3)
    return res


def CalculateEstateVSA(mol, bins=None):
    """
    #################################################################
    MOE-type descriptors using Estate indices and surface area

    contributions.

    estateBins=[-0.390,0.290,0.717,1.165,1.540,1.807,2.05,4.69,9.17,15.0]

    You can specify your own bins to compute some descriptors

    Usage:

        result=CalculateEstateVSA(mol)

        Input: mol is a molecule object

        Output: result is a dict form
    #################################################################
    """
    temp = EVSA.EState_VSA_(mol, bins, force=1)
    res = {}
    for i, j in enumerate(temp):
        res['EstateVSA' + str(i)] = round(j, 3)
    return res


def CalculateVSAEstate(mol, bins=None):
    """
    #################################################################
    MOE-type descriptors using Estate indices and surface

    area contributions.

    vsaBins=[4.78,5.00,5.410,5.740,6.00,6.07,6.45,7.00,11.0]

    You can specify your own bins to compute some descriptors

    Usage:

        result=CalculateVSAEstate(mol)

        Input: mol is a molecule object

        Output: result is a dict form
    #################################################################
    """
    temp = EVSA.VSA_EState_(mol, bins, force=1)
    res = {}
    for i, j in enumerate(temp):
        res['VSAEstate' + str(i)] = round(j, 3)
    return res


def GetMOEofMol(mol):
    """
    #################################################################
    The calculation of MOE-type descriptors (ALL).

    Usage:

        result=GetMOE(mol)

        Input: mol is a molecule object

        Output: result is a dict form
    #################################################################
    """
    result = {}
    result.update(CalculateLabuteASA(mol))
    result.update(CalculateTPSA(mol))
    result.update(CalculateSLOGPVSA(mol, bins=None))
    result.update(CalculateSMRVSA(mol, bins=None))
    result.update(CalculatePEOEVSA(mol, bins=None))
    result.update(CalculateEstateVSA(mol, bins=None))
    result.update(CalculateVSAEstate(mol, bins=None))
    return result

def GetMOE(df_x):
    labels = ['LabuteASA','MTPSA']
    for i in range(12):
        labels.append('slogPVSA' + str(i))
    for i in range(11):
        labels.append('VSAEstate' + str(i))
    for i in range(11):
        labels.append('EstateVSA' + str(i))
    for i in range(14):
        labels.append('PEOEVSA' + str(i))
    for i in range(10):
        labels.append('MRVSA' + str(i))
    r = {}
    for key in labels:
        r[key] = []
    for m in df_x['SMILES']:
        mol = Chem.MolFromSmiles(m)
        res = GetMOEofMol(mol)
        for key in labels:
            r[key].append(res[key])
    return pd.DataFrame(r)