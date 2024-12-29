#! python3
# -*- coding: utf-8 -*-
'''
The main script of the MMPBGBSA Slurm Job. This script is currently for test use.

@File   : mmpbgbsa_main_script.py
@Created: 2024/12/18 21:42
@Author : Zhong, Yinjie
@Email  : yinjie.zhong@vanderbilt.edu
'''

# Here put the import lib.
from os import environ, path
from typing import List, Union
from time import sleep
from requests import post, put
from statistics import mean
from json import loads

# Here put enzy_htp modules.
from enzy_htp import interface, _LOGGER
from enzy_htp.analysis import binding_energy
from enzy_htp.core.clusters.accre import Accre
from enzy_htp.structure import PDBParser, StructureEnsemble
from enzy_htp.workflow.config import StatusCode

DATA_DIR = f"{path.dirname(path.abspath(__file__))}/data/"
WORK_DIR = f"{path.dirname(path.abspath(__file__))}/work_dir/"

app_host = environ.get("app_host")
experiment_id = environ.get("experiment_id")
file_dir = environ.get("file_dir", path.curdir)
access_token = environ.get("access_token")
ref_pdb_filename = environ.get("ref_pdb_filename")
topology_filename = environ.get("topology_filename")
trajectory_filename = environ.get("trajectory_filename")
ligand_pattern = environ.get("ligand_pattern")
mutant = environ.get("mutant")
replica_id = environ.get("replica_id")

RESULT_POST_URL = f"https://{app_host}/api/experiment/{experiment_id}"

cluster = Accre()
cpu_job_config = {
    "cluster" : cluster,
    "res_keywords" : {
        "account" : "yang_lab_csb",
        "partition" : "production",
        'walltime' : '1-00:00:00',
    }
}

def post_result(experiment_id: str, mutant: str, replica_id: str, pdb_filename: str = None, **kwargs):
    """Post the result to the mutexa.

    Args:
        experiment_id (int): The experiment ID associated with this result.
        pdb_filename (str): The name of the PDB file of the result.
        mutant (str): The name of the mutant protein. e.g.: 'A##B C##D'
        replica_id (str): The ID of the MD simulation relica of one mutant.
        kwargs: Keyword arguments containing metrics and other attributes.
    """
    payload = {
        "experiment_id": experiment_id,
        "pdb_filename": pdb_filename,
        "mutant": mutant,
        "replica_id": replica_id,
    }
    payload.update(kwargs)
    try:
        response = put(RESULT_POST_URL,
            headers={
                "Authorization": f"Bearer {access_token}"
            },
            data=payload,
            timeout=30)
        if (response.ok):
            return
        else:
            _LOGGER.warning(f"Result POST failed with error: {response.status_code}")
    except Exception as e:
        _LOGGER.warning(f"Unable to access the Web Server. {e}")
    finally:
        _LOGGER.info(f"Job result record:")
        for key, value in kwargs.items():
            _LOGGER.info(f"\t{key}: {value};")
        return

stru_esm: StructureEnsemble = interface.amber.load_traj(prmtop_path=topology_filename, traj_path=trajectory_filename, ref_pdb=ref_pdb_filename)
binding_values = binding_energy(stru=stru_esm, ligand=ligand_pattern, cluster_job_config=cpu_job_config)

post_result(experiment_id=experiment_id, mutant=mutant, replica_id=replica_id, mmpbgbsa=mean(binding_values))
