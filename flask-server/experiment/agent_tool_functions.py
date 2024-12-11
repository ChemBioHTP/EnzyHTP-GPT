#! python3
# -*- encoding: utf-8 -*-
'''
@File    :   assistant_functions.py
@Created :   2024/10/28 15:11
@Author  :   Zhong, Yinjie
@Version :   1.0
@Contact :   yinjie.zhong@vanderbilt.edu
'''

# Here put the import lib.
from typing import List, Tuple, Union

from enzy_htp import PDBParser
from enzy_htp.core import _LOGGER
from enzy_htp.mutation.mutation_pattern import decode_position_pattern
from enzy_htp.structure import Residue

from .models import Experiment

def find_target_protein_path(experiment: Experiment, **kwargs) -> Tuple[bool, str]:
    """Return the PDB filepath of the wild-type protein.
    
    Returns:
        is_successful (bool): Indidate if the protein path is successfully located.
        pdb_filepath (str): The PDB filepath of the wild-type protein.
    """
    if (experiment.pdb_filename):
        return True, experiment.pdb_filename
    else:
        return False, "Not available"

def find_residue_around(experiment: Experiment, target_residue: str, distance: Union[int, str], **kwargs) -> Tuple[bool, str]:
    """Find the residues around a specific residue.
    
    Args:
        experiment (Experiment): The Experiment instance calling this assistant.
        target_residue (str): The chain id and residue index of the target residue. Example: A.100.
        distance (int | str): The distance cutoff for finding the surrounding residues. Unit: Angstrom.
    
    Returns:
        is_successful (bool): Indidate if the region pattern is successfully generated.
        region_pattern (str): The pattern defining the expected region.
    """
    structure = PDBParser().get_structure(experiment.pdb_filepath)
    try:
        chain_id = target_residue.split(".")[0]
        res_id = target_residue.split(".")[1]
        target_residue_instance = structure.find_residue_with_key((chain_id, int(res_id)))
        if (target_residue_instance is None):
            return False, str()
        else:
            region_pattern = f"resi {res_id} around {distance}"
            # selected_residue_tuples: List[tuple] = decode_position_pattern(position_pattern)
            # residues_key_list = [f"{residue_tuple[0]}.{residue_tuple[1]}" for residue_tuple in selected_residue_tuples]
            # return residues_key_list
            return True, region_pattern
    except Exception as e:
        _LOGGER.error(e)
        return False, str()

def find_residue_by_name(experiment: Experiment, name: str, **kwargs) -> Tuple[bool, str]:
    """Find the key of a residue by its name.
    
    Args:
        is_successful (bool): Indidate if the region pattern is successfully generated.
        experiment (Experiment): The Experiment instance calling this assistant.
        name (str): The 3-letter PDB name of the residue.
    
    Returns:
        residue_key_str (str): The key of a residue.
    """
    structure = PDBParser().get_structure(experiment.pdb_filepath)
    residues = structure.find_residue_name(name=name)
    if (len(residues) > 0):
        residue_key_str = residues[0].key_str
        return True, residue_key_str
    else:
        return False, str()

TOOL_FUNCTION_MAPPER = {
    "find_target_protein_path": find_target_protein_path,
    "find_residue_around": find_residue_around,
    "find_residue_by_name": find_residue_by_name,
}