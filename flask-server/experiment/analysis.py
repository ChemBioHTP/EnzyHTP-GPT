#! python3
# -*- coding: utf-8 -*-
'''
@File   : analysis.py
@Created: 2024/12/07 12:56
@Author : Zhong, Yinjie
@Email  : yinjie.zhong@vanderbilt.edu
'''

from typing import Callable, Dict, List
from enzy_htp.analysis import binding_energy, ddg_fold_of_mutants, ele_field_strength_at_along, rmsd, spi_metric
from enzy_htp.structure import StructureEnsemble, Ligand
from enzy_htp.structure.structure_selection import select_stru

# TODO (Zhong): Add Amber path to Mutexa.

def mmpbgbsa(stru_esm: StructureEnsemble, ligand: str, **kwargs):
    """Calculate the binding energy of `ligand` in `stru`.
    
    Args:
        stru_esm (StructureEnsemble): The StructureEnsemble instance to analyze.
        ligand: The target ligand of the calculation represented as a selection pattern.
            Note that the ligand has to be part of Structure().
            Note that the ligand can be a small molecule or a protein.
    """
    binding_values = binding_energy(stru=stru_esm, ligand=ligand, **kwargs)
    return sum(binding_values)/len(binding_values)

def ddg_fold(stru_esm: StructureEnsemble, **kwargs):
    pass

def electric_field(stru_esm: StructureEnsemble, region_pattern: str, **kwargs):
    pass

def active_site_rmsd(stru_esm: StructureEnsemble, region_pattern: str, **kwargs):
    """Calculate the RMSD value of a StructureEnsemble instance with specified region pattern.
    
    Args:
        stru_esm (StructureEnsemble): A collection of different geometries of the same enzyme structure.
        region_pattern (str): A pymol-formatted selection string which defines the region for calculating RMSD value.
    """
    rmsd_values = rmsd(stru_esm=stru_esm, region_pattern=region_pattern)
    return sum(rmsd_values)/len(rmsd_values)

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
    return sum(spi_values)/len(spi_values)

# TODO (Zhong): cavity, ddg_fold and electric_field.
METRICS_MAPPER: Dict[str, Callable] = {
    "active_site_rmsd": active_site_rmsd,
    "cavity": None,
    "ddg_fold": ddg_fold,
    "electric_field": electric_field,
    "mmpbgbsa": mmpbgbsa,
    "spi": spi,
}
