#!/usr/bin/python

import chimera
from chimera import openModels, Molecule

def getChains():
    """Get the chain names in a protein molecule"""
    #TODO, check if there is a quick method to get the list of chains
    mols = openModels.list(modelTypes=[Molecule])
    chains = []
    m = mols[0] # get the first model
    for residue in m.residues:
        if residue.id.chainId not in chains:
            chains.append(str(residue.id.chainId))

    chains = sorted(chains)

    return chains

def getMol():
    """Get the protein molecule"""
    mols = openModels.list(modelTypes=[Molecule])
    return mols[0]

def getMolName():
    """Get protein id"""
    mols = openModels.list(modelTypes=[Molecule])
    return str(mols[0].name)

def getResidueInChain(chain):
    """Get the residue index and its name in a specific chain
    
    Returns:
        list (list): a list of residue info, each residue info contains residue index, and name
    """
    chains = []
    mols = openModels.list(modelTypes=[Molecule])
    mol = mols[0]
    r = []
    for residue in mol.residues:
        if chain == residue.id.chainId:
            r.append([residue.id.position, str(residue.type).upper()])

    return r

def getLabeledResidueInChain(labels, chain, residues):
    """Get the indies of labeled residue in chain started from 0

    Args:
        labels: labeled residues
        chain: selected chain
        residue_labels (list), residues in chain

    Returns:
        list: indies of labeled residues in residue_labels
    """
    l = []
    for index, residue in enumerate(residues):
        for label in labels:
            if label[1] == chain and label[2] == residue[0]:
                l.append(index)

    return l

def residueSingleLetter(name):
    """Convert three-letters name to single-letter name
    """
    d = {'ALA': 'A', 'ARG': 'R', 'ASN': 'N', 'ASP': 'D', 'CYS': 'C', 'GLU': 'E', 'GLN': 'Q', 'GLY': 'G', 'HIS': 'H', 'ILE': 'I', 'LEU': 'L', 'LYS': 'K', 'MET': 'M', 'PHE': 'F', 'PRO': 'P', 'SER': 'S', 'THR': 'T', 'TRP': 'W', 'TYR': 'Y', 'VAL': 'V'}

    if name in d:
        #print name
        return d[name]
    else:
        return '-'

def getLabels(labels, chain):
    """Get the labeled residue in the specified chain

    Args:
        labels, info returned from model
        chain, chain ID

    Returns:
        string, labeled chain for chimera display
    """
    s = ''

    for label in labels:
        if label[1] == chain:
            s += ':'+str(label[2])+'.'+chain+' '

    return s

def getLabelsInTable(labels, chain):
    """Get the informaiton of labeled residues

    Args:
        labels: infor returned from model
        chain: selected chain ID

    Returns:
        list: a list of information of labeled residues in the selected chain
    """
    l = []

    for label in labels:
        if label[1] == chain:
            l.append(label)

    return l

def validResidue(name):
    """Convert three-letters name to single-letter name
    """
    d = {'ALA': 'A', 'ARG': 'R', 'ASN': 'N', 'ASP': 'D', 'CYS': 'C', 'GLU': 'E', 'GLN': 'Q', 'GLY': 'G', 'HIS': 'H', 'ILE': 'I', 'LEU': 'L', 'LYS': 'K', 'MET': 'M', 'PHE': 'F', 'PRO': 'P', 'SER': 'S', 'THR': 'T', 'TRP': 'W', 'TYR': 'Y', 'VAL': 'V'}

    if name in d:
        return True
    else:
        return False
