#! python3
# -*- coding: utf-8 -*-
'''
@File   : analysis.py
@Created: 2024/12/07 12:56
@Author : Zhong, Yinjie
@Email  : yinjie.zhong@vanderbilt.edu
'''

from statistics import mean
from typing import Callable, Dict, List, Optional, Tuple
from enzy_htp.analysis import binding_energy, ddg_fold_of_mutants, ele_field_strength_at_along, rmsd, spi_metric
from enzy_htp.analysis.dsi import dsi as eh_dsi
from enzy_htp.analysis.cavity import ensemble_cavity_volumes
from enzy_htp.core import _LOGGER
from enzy_htp.mutation import assign_mutant
from enzy_htp.mutation_class import Mutation
from enzy_htp.structure import Structure, StructureEnsemble, Ligand
from enzy_htp.structure.structure_selection import select_stru

def active_site_rmsd(
    stru_esm: StructureEnsemble,
    pocket_selection_pattern: Optional[str] = None,
    **kwargs,
) -> Optional[float]:
    """Calculate the RMSD value of a StructureEnsemble instance with specified region pattern.

    Args:
        stru_esm (StructureEnsemble): A collection of different geometries of the same enzyme structure.
        pocket_selection_pattern (str): A pymol-formatted selection string which defines the region
            for calculating RMSD value.
    """
    if not pocket_selection_pattern:
        pocket_selection_pattern = kwargs.pop("region_pattern", None)
    if not pocket_selection_pattern:
        _LOGGER.error("`pocket_selection_pattern` is required for active site RMSD calculation.")
        return None
    rmsd_values = rmsd(stru_esm=stru_esm, region_pattern=pocket_selection_pattern)
    return mean(rmsd_values)

def cavity(stru_esm: StructureEnsemble, ligand_selection_pattern: str=None, pocket_compositing_residue_pattern: str=None, **kwargs) -> float:
    """The cavity volume of a binding pocket of the protein, defined by where the ligand located in the `structure_0`.
    
    Args:
        stru_esm (StructureEnsemble): The StructureEnsemble instance to analyze.
        ligand_selection_pattern (str): The target ligand of the calculation represented as a selection pattern.
            Note that the ligand has to be part of Structure().
            Note that the ligand can be a small molecule or a protein.
        pocket_compositing_residue_pattern (str): A pymol-formatted sele str which defines the pocket region.
    """
    if ligand_selection_pattern:
        cavity_volumes = ensemble_cavity_volumes(stru_esm=stru_esm, contain_ligand=ligand_selection_pattern, frame_0_based=True)
    elif pocket_compositing_residue_pattern:
        # convert pattern to List[Residue]
        stru = stru_esm.structure_0
        pocket_residues = select_stru(stru=stru, pattern=pocket_compositing_residue_pattern).involved_residues
        cavity_volumes = ensemble_cavity_volumes(stru_esm=stru_esm, composing_residues=pocket_residues, frame_0_based=True)
    else:
        _LOGGER.error("Either `ligand_selection_pattern` or `pocket_compositing_residue_pattern` has to be provided for cavity volume calculation.")
        return 0
    return mean(cavity_volumes)

def ddg_fold(stru: Structure, mutant: List[Mutation], **kwargs):
    """Calculate the change of dG_fold of the protein mutants in a mutant space.

    Args:
        stru (Structure): The target molecule of the calculation represented as a `Structure` instance.
        mutant (List[Mutation]): The target mutant to assess.
    """
    ddg_dict = ddg_fold_of_mutants(stru=stru, mutant_space=[mutant])
    return ddg_dict[tuple(mutant)]

def _sanitize_domain_sequence(seq: str) -> str:
    return "".join(seq.split()).upper()


def _build_chain_maps(stru: Structure) -> List[Tuple[str, str, List[Tuple[str, int]]]]:
    chain_maps: List[Tuple[str, str, List[Tuple[str, int]]]] = []
    for chain in stru.polypeptides:
        chain.sort_residues()
        seq_chars: List[str] = []
        residue_keys: List[Tuple[str, int]] = []
        for res in chain.residues:
            seq_name = res.sequence_name.strip()
            if len(seq_name) != 1:
                continue
            seq_chars.append(seq_name.upper())
            residue_keys.append((chain.name, res.idx))
        if seq_chars:
            chain_maps.append((chain.name, "".join(seq_chars), residue_keys))
    return chain_maps


def _find_domain_range_in_chain(chain_seq: str, domain_seq: str, chain_id: str) -> Optional[Tuple[int, int]]:
    start = chain_seq.find(domain_seq)
    if start == -1:
        return None
    if chain_seq.find(domain_seq, start + 1) != -1:
        _LOGGER.warning(
            f"Domain sequence appears multiple times in chain {chain_id}; using first match."
        )
    end = start + len(domain_seq) - 1
    return start, end


def _domain_sequences_to_residue_ranges(
    stru: Structure, domain1_sequence: str, domain2_sequence: str
) -> Tuple[List[Tuple[str, int]], List[Tuple[str, int]]]:
    domain1_seq = _sanitize_domain_sequence(domain1_sequence)
    domain2_seq = _sanitize_domain_sequence(domain2_sequence)
    if not domain1_seq or not domain2_seq:
        raise ValueError("Both domain1_sequence and domain2_sequence must be non-empty.")

    chain_maps = _build_chain_maps(stru)
    if not chain_maps:
        raise ValueError("No polypeptide chains found for DSI alignment.")

    def best_match(domain_seq: str) -> Tuple[str, int, int, List[Tuple[str, int]]]:
        matches: List[Tuple[str, int, int, List[Tuple[str, int]]]] = []
        for chain_id, chain_seq, residue_keys in chain_maps:
            result = _find_domain_range_in_chain(chain_seq, domain_seq, chain_id)
            if not result:
                continue
            start, end = result
            matches.append((chain_id, start, end, residue_keys))
        if not matches:
            raise ValueError(f"Unable to find domain sequence in any chain: {domain_seq}")
        if len(matches) > 1:
            _LOGGER.warning(
                "Domain sequence matches multiple chains; using first match "
                f"in chain {matches[0][0]}."
            )
        return matches[0]

    chain_id_1, start_1, end_1, residue_keys_1 = best_match(domain1_seq)
    chain_id_2, start_2, end_2, residue_keys_2 = best_match(domain2_seq)

    if chain_id_1 != chain_id_2:
        _LOGGER.warning(
            "Domain sequences mapped to different chains for DSI: "
            f"{chain_id_1} vs {chain_id_2}."
        )

    domain1_residues = [residue_keys_1[start_1], residue_keys_1[end_1]]
    domain2_residues = [residue_keys_2[start_2], residue_keys_2[end_2]]
    return domain1_residues, domain2_residues


def dsi(stru_esm: StructureEnsemble, domain1_sequence: str, domain2_sequence: str, **kwargs):
    """The domain seperation index of the two domains of a bidomain enzyme. 
    This index describes how seperate the two domains are in the dynamic motion of the enzyme.
    A study by Ning et al showed it is predictive for the cold-adaption ability (the ability to maintain activity at lower temperature) of bidomain enzymes.

    Args:
        domain1_sequence (str): The sequence of the first domain. The backend will locate this
            exact sequence in the chain to determine its residue range.
        domain2_sequence (str): The sequence of the second domain. The backend will locate this
            exact sequence in the chain to determine its residue range.
    """
    try:
        domain1_residues, domain2_residues = _domain_sequences_to_residue_ranges(
            stru=stru_esm.structure_0,
            domain1_sequence=domain1_sequence,
            domain2_sequence=domain2_sequence,
        )
    except Exception as exc:
        _LOGGER.error(f"Unable to resolve DSI domains: {exc}")
        return None

    result = eh_dsi(
        ensemble=stru_esm,
        domain1_residues=domain1_residues,
        domain2_residues=domain2_residues,
    )
    return mean(result)

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

def mmpbgbsa(
    stru_esm: StructureEnsemble,
    ligand_selection_pattern: Optional[str] = None,
    **kwargs,
) -> Optional[float]:
    """Calculate the binding energy of `ligand_selection_pattern` in `stru`.

    Args:
        stru_esm (StructureEnsemble): The StructureEnsemble instance to analyze.
        ligand_selection_pattern: The target ligand of the calculation represented as a selection pattern.
            Note that the ligand has to be part of Structure().
            Note that the ligand can be a small molecule or a protein.
    """
    if not ligand_selection_pattern:
        ligand_selection_pattern = kwargs.pop("ligand", None)
    if not ligand_selection_pattern:
        _LOGGER.error("`ligand_selection_pattern` is required for MMPB/GBSA calculation.")
        return None
    binding_values = binding_energy(
        stru=stru_esm,
        ligand=ligand_selection_pattern,
        non_armer_cpu_num=2,
        **kwargs,
    )
    return mean(binding_values)

def spi(stru_esm: StructureEnsemble, substrate_selection_pattern: str, pocket_selection_pattern: str = None, **kwargs) -> float:
    """Calculates the spi metric for a StructureEnsemble using a pymol-formatted pocket selection string pattern.
    
    Args:
        stru_esm (StructureEnsemble): The StructureEnsemble instance to analyze.
        substrate_selection_pattern: The target substrate of the calculation represented as a selection pattern.
            Note that the substrate has to be part of Structure().
            Note that the substrate can be a small molecule or a protein.
        pocket_selection_pattern: A pymol-formatted sele str which defines the denominator in the spi metric.
    """
    ligand: Ligand = select_stru(stru=stru_esm.structure_0, pattern=substrate_selection_pattern)
    if not pocket_selection_pattern:
        pocket_selection_pattern = f"br. ({substrate_selection_pattern}) around 5"
    spi_values: List[float] = spi_metric(stru_esm, ligand, pocket_selection_pattern)
    return mean(spi_values)

METRICS_MAPPER: Dict[str, Callable] = {
    "active_site_rmsd": active_site_rmsd,
    "cavity": cavity,
    "ddg_fold": ddg_fold,
    "dsi": dsi,
    "electric_field": electric_field,
    "mmpbgbsa": mmpbgbsa,
    "spi": spi,
}
