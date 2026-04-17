#! python3
# -*- encoding: utf-8 -*-
'''
Functions here are expected to be called by OpenAI Assistants.

Each function has two return values: is_successful (bool) & output (str).

@File    :   assistant_functions.py
@Created :   2024/10/28 15:11
@Author  :   Zhong, Yinjie
@Version :   1.0
@Contact :   yinjie.zhong@vanderbilt.edu
'''

# Here put the import lib.
import math
from json import dumps
from typing import Any, List, Tuple, Union
from os import path
from statistics import mean, pstdev, stdev

from enzy_htp import PDBParser
from enzy_htp.core import _LOGGER
from enzy_htp.mutation.mutation_pattern import decode_position_pattern
from enzy_htp.structure import Residue

from .models import Experiment

def summon_next_agent(experiment: Experiment, **kwargs) -> Tuple[bool, str]:
    """Suggest an optional completion of all tasks of the current agent and an optional summon of the next agent in the workflow.
    
    Args:
        experiment (Experiment): The Experiment instance calling this assistant.
    
    Returns:
        is_successful (bool): Indidate if the next agent summon option is on.
        message (str): The message indicating the switch.
    """
    experiment.update_attributes(
        mapper={
            "summon_next_agent": True
        }
    )
    return True, "Next agent summon option is on."

def summon_upload_box(experiment: Experiment, **kwargs) -> Tuple[bool, str]:
    """Summon an upload box in frontend so that user can choose to upload files to the backend.
    
    Args:
        experiment (Experiment): The Experiment instance calling this assistant.

    Returns:
        is_successful (bool): Indidate if the upload box summon is on.
        message (str): The message indicating the status.
    """
    if (not experiment.pdb_filepath or not path.isfile(experiment.pdb_filepath)):
        experiment.update_attributes(
            mapper={
                "summon_upload_pdb": True
            }
        )
        return True, "The PDB file summon upload box is on."
    else:
        return False, "The PDB file already exists."

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

def _coerce_numeric_values(values: List[Union[int, float, str]]) -> List[float]:
    numeric_values: List[float] = []
    for value in values or []:
        try:
            numeric_values.append(float(value))
        except (TypeError, ValueError):
            continue
    return numeric_values

def _coerce_metric_pairs(
    labels: List[Any],
    values: List[Union[int, float, str]],
) -> Tuple[bool, str, List[Tuple[str, float]]]:
    if (not isinstance(labels, list)) or (not isinstance(values, list)):
        return False, "labels and values must both be arrays.", []
    if (len(labels) != len(values)):
        return False, "labels and values must have the same length.", []

    metric_pairs: List[Tuple[str, float]] = []
    for label, value in zip(labels, values):
        try:
            numeric_value = float(value)
        except (TypeError, ValueError):
            continue
        metric_pairs.append((str(label), numeric_value))

    if (not metric_pairs):
        return False, "No numeric metric values provided.", []
    return True, "", metric_pairs

def calculate_mean(values: List[Union[int, float, str]], **kwargs) -> Tuple[bool, str]:
    """Compute the arithmetic mean of a list of numeric values."""
    numeric_values = _coerce_numeric_values(values)
    if (not numeric_values):
        return False, "No numeric values provided."
    return True, str(mean(numeric_values))

def calculate_standard_deviation(values: List[Union[int, float, str]], ddof: Union[int, str] = 1, **kwargs) -> Tuple[bool, str]:
    """Compute the standard deviation of a list of numeric values."""
    numeric_values = _coerce_numeric_values(values)
    if (not numeric_values):
        return False, "No numeric values provided."
    try:
        ddof_value = int(ddof)
    except (TypeError, ValueError):
        return False, "ddof must be an integer."
    if (ddof_value < 0):
        return False, "ddof must be >= 0."
    if (len(numeric_values) <= ddof_value):
        return False, f"Need at least {ddof_value + 1} values to compute standard deviation."
    if (ddof_value == 0):
        std_value = pstdev(numeric_values)
    elif (ddof_value == 1):
        std_value = stdev(numeric_values)
    else:
        mean_value = mean(numeric_values)
        variance = sum((value - mean_value) ** 2 for value in numeric_values) / (len(numeric_values) - ddof_value)
        std_value = variance ** 0.5
    return True, str(std_value)

def sort_metrics_by_value(
    labels: List[Any],
    values: List[Union[int, float, str]],
    descending: bool = True,
    **kwargs,
) -> Tuple[bool, str]:
    """Sort metric label/value pairs by numeric value and return ordered labels and values."""
    is_valid, error_message, metric_pairs = _coerce_metric_pairs(labels=labels, values=values)
    if (not is_valid):
        return False, error_message

    ordered_pairs = sorted(metric_pairs, key=lambda item: item[1], reverse=bool(descending))
    result = {
        "labels": [label for label, _ in ordered_pairs],
        "values": [value for _, value in ordered_pairs],
    }
    return True, dumps(result)

def filter_metrics_by_percentage(
    labels: List[Any],
    values: List[Union[int, float, str]],
    percentage: Union[int, float, str],
    descending: bool = True,
    **kwargs,
) -> Tuple[bool, str]:
    """Sort metric label/value pairs and keep the top percentage in sorted order."""
    is_valid, error_message, metric_pairs = _coerce_metric_pairs(labels=labels, values=values)
    if (not is_valid):
        return False, error_message

    try:
        pct = float(percentage)
    except (TypeError, ValueError):
        return False, "percentage must be a number in (0, 100]."
    if (pct <= 0) or (pct > 100):
        return False, "percentage must be in (0, 100]."

    ordered_pairs = sorted(metric_pairs, key=lambda item: item[1], reverse=bool(descending))
    keep_count = max(1, math.ceil(len(ordered_pairs) * (pct / 100.0)))
    kept_pairs = ordered_pairs[:keep_count]
    result = {
        "labels": [label for label, _ in kept_pairs],
        "values": [value for _, value in kept_pairs],
        "selected_count": keep_count,
        "total_count": len(ordered_pairs),
        "percentage": pct,
    }
    return True, dumps(result)

TOOL_FUNCTION_MAPPER = {
    "summon_next_agent": summon_next_agent,
    "summon_upload_box": summon_upload_box,
    "find_target_protein_path": find_target_protein_path,
    "find_residue_around": find_residue_around,
    "find_residue_by_name": find_residue_by_name,
    "calculate_mean": calculate_mean,
    "calculate_standard_deviation": calculate_standard_deviation,
    "sort_metrics_by_value": sort_metrics_by_value,
    "filter_metrics_by_percentage": filter_metrics_by_percentage,
}
