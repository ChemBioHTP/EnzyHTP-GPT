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
from statistics import mean

# Here put enzy_htp modules.
from enzy_htp import interface, _LOGGER
from enzy_htp.core.clusters.accre import Accre
from enzy_htp.structure import PDBParser
from enzy_htp.structure.structure_selection import select_stru
from enzy_htp.preparation import remove_solvent, remove_hydrogens, protonate_stru
from enzy_htp.mutation import assign_mutant, mutate_stru
from enzy_htp.mutation_class import get_mutant_name_str
from enzy_htp.geometry import equi_md_sampling
from enzy_htp.analysis import spi_metric
from enzy_htp.workflow.config import StatusCode

DATA_DIR = f"{path.dirname(path.abspath(__file__))}/data/"
WORK_DIR = f"{path.dirname(path.abspath(__file__))}/work_dir/"

app_host = environ.get("app_host")
experiment_id = environ.get("experiment_id")
file_dir = environ.get("file_dir", path.curdir)
access_token = environ.get("access_token")
pdb_filename = environ.get("pdb_filename")
mutation_pattern = environ.get("mutation_pattern")

md_length = float(environ.get("md_length", 30.0))
ph = float(environ.get("ph", 7.4))
pocket_range = int(environ.get("pocket_range", 5))

cluster = Accre()
gpu_job_config = {
    "cluster" : cluster,
    "res_keywords" : {
        "account" : "csb_gpu_acc",
        "partition" : "a100x4"
    }
}
cpu_job_config = {
    "cluster" : cluster,
    "res_keywords" : {
        "account" : "yang_lab_csb",
        "partition" : "production",
        'walltime' : '1-00:00:00',
    }
}

PROGRESS_UPDATE_URL = f"https://{app_host}/api/experiment/{experiment_id}"
RESULTS_POST_URL = f"https://{app_host}/api/experiment/{experiment_id}/results"
print(f"Send PATCH request to {PROGRESS_UPDATE_URL} so as to update the status and progress.")

def synchronize_job_status(status: int = None, progress: float = None) -> None:
    """Synchronize the Job Status to the Web Server. If the web server is not accessible, log the status and error information.
    
    Args:
        status (int): Latest job status.
        progress (float): The progress of current job (Float value from 0 to 1).
    """    
    try:
        response = put(PROGRESS_UPDATE_URL,
            headers={
                "Authorization": f"Bearer {access_token}"
            },
            data={
                "status": status,
                "progress": progress
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
    
def post_job_result(**kwargs) -> None:
    """Post the result record to the web server."""
    try:
        response = post(RESULTS_POST_URL,
            headers={
                "Authorization": f"Bearer {access_token}"
            },
            data=kwargs,
            timeout=30)
        if (response.ok):
            return
        else:
            _LOGGER.warning(f"Result POST failed with status code: {response.status_code}")
    except Exception as e:
        _LOGGER.warning(f"Unable to access the Web Server. {e}")
    finally:
        _LOGGER.info(f"Job result record:")
        for key, value in kwargs.items():
            _LOGGER.info(f"\t{key}: {value};")
        return

synchronize_job_status(status=StatusCode.INITIALIZING, progress=0.0)

has_ligand = False

try:
    wt_stru = PDBParser().get_structure(pdb_filename)
    remove_solvent(wt_stru)
    remove_hydrogens(stru=wt_stru, polypeptide_only=True)
    protonate_stru(stru=wt_stru, ph=ph, protonate_ligand=True)

    if (wt_stru.ligands):
        has_ligand = True

    mutants = assign_mutant(stru=wt_stru, pattern=mutation_pattern)
    mutants_count = len(mutants)

    synchronize_job_status(status=StatusCode.RUNNING, progress=0.0)

    # mutation
    for i, mut in enumerate(mutants):
        mutant_result = []
        mutant_dir = path.join(WORK_DIR, f"mutant_{i}")
        mutant_stru = mutate_stru(wt_stru, mut, engine="pymol")

        ligand_chrg_spin_mapper = dict()
        pocket = list()
        if (has_ligand):
            for i, ligand in enumerate(mutant_stru.ligands):
                # Set charge-Spin to default value: (0, 1)
                ligand_chrg_spin_mapper[ligand.name] = (0, 1)

                if (i == 0):
                    # Set pocket to the default value: 5 Ang. around the ligand. We can only deal with the first ligand at present.
                    selection = select_stru(mutant_stru, f"br. (resi {ligand.idx} around {pocket_range})")
                    pocket.extend(selection.involved_residues)
                    pocket.append(ligand)
        pocket = list(set(pocket))

        mutant_stru.assign_ncaa_chargespin(ligand_chrg_spin_mapper)
        remove_hydrogens(mutant_stru, polypeptide_only=True)
        protonate_stru(mutant_stru, protonate_ligand=False)

        # Do something here.
        # sampling
        md_constraints = []
        mut_constraints = []
        for cons in md_constraints:
            mut_constraints.append(cons(mutant_stru))
        param_method = interface.amber.build_md_parameterizer()

        
        md_result = equi_md_sampling(
            stru=mutant_stru,
            param_method=param_method,
            prod_constrain=mut_constraints,
            prod_time=md_length,
            record_period=md_length*0.1,
            work_dir=f"{mutant_dir}/MD/",
            cluster_job_config=gpu_job_config,
            cpu_equi_step=True,
            cpu_job_config=cpu_job_config,
            job_check_period=10,
        )

        result_record_dict = {
            "mutant": get_mutant_name_str(mut),
        }

        if has_ligand:
            spi_list = list()
            for ensemble in md_result:
                spi_value = spi_metric(ensemble, mutant_stru.ligands[0], pocket)
                spi_list.append(spi_value)
            result_record_dict["spi"] = mean(spi_list)

        post_job_result(result_record_dict)

        # Send a request to the backend of Web Application to update status and progress.
        synchronize_job_status(status=StatusCode.RUNNING, progress=i/mutants_count)

    synchronize_job_status(status=StatusCode.EXIT_OK, progress=1.0)
except Exception as e:
    _LOGGER.error(e)
    synchronize_job_status(status=StatusCode.EXIT_WITH_ERROR)
