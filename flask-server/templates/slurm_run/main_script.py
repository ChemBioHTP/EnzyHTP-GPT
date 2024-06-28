#! python3
# -*- encoding: utf-8 -*-
'''
The main script of the Slurm Job. This script is currently for test use.

@File    :   main_script.py
@Created :   2024/06/21 16:18
@Author  :   Zhong, Yinjie
@Version :   1.0
@Contact :   yinjie.zhong@vanderbilt.edu
'''

# Here put the import lib.
from os import environ, path
from time import sleep
from requests import post, put

from enzy_htp import interface, _LOGGER
from enzy_htp.structure import PDBParser
from enzy_htp.preparation import remove_solvent, remove_hydrogens, protonate_stru
from enzy_htp.mutation import assign_mutant, mutate_stru
from enzy_htp.geometry import equi_md_sampling
from enzy_htp.analysis import spi_metric
from enzy_htp.workflow.config import StatusCode


# TODO (Zhong): JWT is required for authentication.
experiment_id = "${experiment_id}"
STATUS_UPDATE_URL = f"https://enzyhtp.app.vanderbilt.edu/api/experiment/{experiment_id}"

file_dir = environ.get("file_dir", path.curdir)
access_token = environ.get("access_token")
pdb_filename = environ.get("pdb_filename")
mutation_pattern = "{WT}"
ph = 7.4

def synchronize_job_status(status: int, progress: float) -> None:
    """Synchronize the Job Status to the Web Server. If the web server is not accessible, log the status and error information.
    
    Args:
        status (int): Latest job status.
        progress (float): The progress of current job (Float value from 0 to 1).
    """
    try:
        response = put(STATUS_UPDATE_URL,
            headers={
                "Authorization": f"Bearer {access_token}"
            },
            data={
                "status": StatusCode.RUNNING,
                "progress": 0.0
            },
            timeout=30)
        if (response.ok):
            return
        else:
            _LOGGER.warning(f"Synchronization failed with status code: {response.status_code}")
    except Exception as e:
        _LOGGER.warning(f"Unable to access the Web Server. {e}")
    finally:
        _LOGGER.info(f"Job Status Code: {status}, Progress: {progress}")
        return
    
    
synchronize_job_status(status=StatusCode.INITIALIZING, progress=0.0)

try:
    wt_stru = PDBParser().get_structure(path.join(file_dir, pdb_filename))
    remove_solvent(stru=wt_stru)
    remove_hydrogens(stru=wt_stru, polypeptide_only=True)
    protonate_stru(stru=wt_stru, ph=ph, protonate_ligand=True)

    mutants = assign_mutant(stru=wt_stru, pattern=mutation_pattern)
    mutants_count = len(mutants)

    synchronize_job_status(status=StatusCode.RUNNING, progress=0.0)

    # mutation
    for i, mut in enumerate(mutants):
        mutant_result = []
        mutant_stru = mutate_stru(wt_stru, mut, engine="pymol")

        # Do something here.
        sleep(10.0)

        # Send a request to the backend of Web Application to update status and progress.
        synchronize_job_status(status=StatusCode.RUNNING, progress=i/mutants_count)

    synchronize_job_status(status=StatusCode.EXIT_OK, progress=1.0)
except:
    synchronize_job_status(status=StatusCode.EXIT_WITH_ERROR)
