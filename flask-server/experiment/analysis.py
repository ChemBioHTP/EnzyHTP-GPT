#! python3
# -*- coding: utf-8 -*-
'''
@File   : analysis.py
@Created: 2024/12/07 12:56
@Author : Zhong, Yinjie
@Email  : yinjie.zhong@vanderbilt.edu
'''

from statistics import mean
from typing import Callable, Dict, List
from enzy_htp.analysis import binding_energy, ddg_fold_of_mutants, ele_field_strength_at_along, rmsd, spi_metric
from enzy_htp.analysis.cavity import ensemble_cavity_volumes
from enzy_htp.core import _LOGGER
from enzy_htp.mutation import assign_mutant
from enzy_htp.mutation_class import Mutation
from enzy_htp.structure import Structure, StructureEnsemble, Ligand
from enzy_htp.structure.structure_selection import select_stru

def active_site_rmsd(stru_esm: StructureEnsemble, region_pattern: str, **kwargs) -> float:
    """Calculate the RMSD value of a StructureEnsemble instance with specified region pattern.
    
    Args:
        stru_esm (StructureEnsemble): A collection of different geometries of the same enzyme structure.
        region_pattern (str): A pymol-formatted selection string which defines the region for calculating RMSD value.
    """
    rmsd_values = rmsd(stru_esm=stru_esm, region_pattern=region_pattern)
    return mean(rmsd_values)

def cavity(stru_esm: StructureEnsemble, ligand: str, **kwargs) -> float:
    """The cavity volume of a binding pocket of the protein, defined by where the ligand located in the `structure_0`.
    
    Args:
        stru_esm (StructureEnsemble): The StructureEnsemble instance to analyze.
        ligand (str): The target ligand of the calculation represented as a selection pattern.
            Note that the ligand has to be part of Structure().
            Note that the ligand can be a small molecule or a protein.
    """
    cavity_volumes = ensemble_cavity_volumes(stru_esm=stru_esm, contain_ligand=ligand, frame_0_based=True)
    return mean(cavity_volumes)

def ddg_fold(stru: Structure, mutant: List[Mutation], **kwargs):
    """Calculate the change of dG_fold of the protein mutants in a mutant space.

    Args:
        stru (Structure): The target molecule of the calculation represented as a `Structure` instance.
        mutant (List[Mutation]): The target mutant to assess.
    """
    ddg_dict = ddg_fold_of_mutants(stru=stru, mutant_space=[mutant])
    return ddg_dict[tuple(mutant)]

def dsi(linker_sequence: str, **kwargs):
    """The domain seperation index of the two domains of a bidomain enzyme. 
    This index describes how seperate the two domains are in the dynamic motion of the enzyme.
    A study by Ning et al showed it is predictive for the cold-adaption ability (the ability to maintain activity at lower temperature) of bidomain enzymes.

    Args:
        linker_sequence (str): the sequence of the linker. (use to define the sequence range of the two domains) 
    """
    pass

def electric_field(stru_esm: StructureEnsemble, atom_1: str, atom_2: str, unit: str = "kcal/(mol*e*Ang)", **kwargs):
    """Calculate the RMSD value of a StructureEnsemble instance with specified region pattern.
    
    Args:
        stru_esm (StructureEnsemble): A collection of different geometries of the same enzyme structure.
        atom_1 (str): The first atom of the bond of interest.
        atom_2 (str): The second atom of the bond of interest.
        unit (str, optional): The unit of the output EF.
    
    Note:
        The format of atom_1, atom_2 is "Chain_id.Residue_index.Atom_name"
        E.g. "A.125.CA" - means the CA atom in residue 125 of chain A.

    Returns:
        average_electric_field (float | None): The specified field strength in `unit`.
    """
    structure_0 = stru_esm.structure_0
    atom_1_selected = atom_2_selected = None

    try:
        atom_1_ids = atom_1.split(".")
        atom_1_res = structure_0.find_residue_with_key((atom_1_ids[0], int(atom_1_ids[1])))
        atom_1_selected = atom_1_res.find_atom_name(atom_1_ids[2])
        atom_2_ids = atom_2.split(".")
        atom_2_res = structure_0.find_residue_with_key((atom_2_ids[0], int(atom_2_ids[1])))
        atom_2_selected = atom_2_res.find_atom_name(atom_2_ids[2])
    except:
        _LOGGER.error("Invalid `atom_1` or `atom_2` argument values: Cannot find specified atoms.")
        return None
    
    ef_values = list()
    for stru in stru_esm.structures(remove_solvent=True):
        ef_result = ele_field_strength_at_along(stru=stru, p1=atom_1_selected, p2=atom_2_selected)
        ef_values.append(ef_result)
        continue
    return mean(ef_values)

def mmpbgbsa(stru_esm: StructureEnsemble, ligand: str, **kwargs) -> float:
    """Calculate the binding energy of `ligand` in `stru`.
    
    Args:
        stru_esm (StructureEnsemble): The StructureEnsemble instance to analyze.
        ligand: The target ligand of the calculation represented as a selection pattern.
            Note that the ligand has to be part of Structure().
            Note that the ligand can be a small molecule or a protein.
    """
    binding_values = binding_energy(stru=stru_esm, ligand=ligand, non_armer_cpu_num=2, **kwargs)
    return mean(binding_values)

def spi(stru_esm: StructureEnsemble, ligand: str, region_pattern: str, **kwargs) -> float:
    """Calculates the spi metric for a StructureEnsemble using a pymol-formatted pocket selection string pattern.
    
    Args:
        stru_esm (StructureEnsemble): The StructureEnsemble instance to analyze.
        ligand: The target ligand of the calculation represented as a selection pattern.
            Note that the ligand has to be part of Structure().
            Note that the ligand can be a small molecule or a protein.
        region_pattern: A pymol-formatted sele str which defines the denominator in the spi metric.
    """
    ligand: Ligand = select_stru(stru=stru_esm.structure_0, pattern=ligand)
    spi_values: List[float] = spi_metric(stru_esm, ligand, region_pattern)
    return mean(spi_values)

# TODO (Zhong): cavity, ddg_fold and electric_field.
METRICS_MAPPER: Dict[str, Callable] = {
    "active_site_rmsd": active_site_rmsd,
    "cavity": cavity,
    "ddg_fold": ddg_fold,
    "dsi": dsi,
    "electric_field": electric_field,
    "mmpbgbsa": mmpbgbsa,
    "spi": spi,
}
