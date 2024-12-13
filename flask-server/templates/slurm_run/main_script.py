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
from typing import List, Union
from time import sleep
from requests import post, put
from statistics import mean
from json import loads

# Here put enzy_htp modules.
from enzy_htp import interface, _LOGGER
from enzy_htp.core.clusters.accre import Accre
from enzy_htp.structure import PDBParser, StructureEnsemble
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
constraints_str = environ.get("constraints_str")
md_length = float(environ.get("md_length", 30.0))
ph = float(environ.get("ph", 7.4))
pocket_range = int(environ.get("pocket_range", 5))

md_constraints = []
try:
    md_constraints = loads(constraints_str)
except Exception as e:
    _LOGGER.error(f"Exception raised when loading `constraints_str`: {e}")

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
TRAJ_UPLOAD_URL = f"https://{app_host}/api/experiment/{experiment_id}"
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
    
def post_trajectory_and_topology_file(mutant: str, replica_id: Union[int, str], trajectory_filepath: str, topology_filepath: str) -> None:
    """Post the trajectory and topology file to the web server.

    Args:
        mutant_name (str): The name of the mutant associated with the trajectory. e.g.: 'A##B C##D'
        replica_id (int | str): The ID of the MD simulation relica of one mutant.
        topology_file (FileStorage): The FileStorage instance of the Amber prmtop file.
        traj_file (FileStorage): The FileStorage instance of the new trajectory file.
    """
    try:
        data = {
            "mutant": mutant,
            "replica_id": str(replica_id),
        }
        files = {
            "trajectory": open(trajectory_filepath, mode="rb"),
            "topology": open(topology_filepath, mode="rb"),
        }
        response = post(TRAJ_UPLOAD_URL,
            headers={
                "Authorization": f"Bearer {access_token}"
            },
            data=data,
            files=files,
            timeout=300)
        if (response.ok):
            return
        else:
            _LOGGER.warning(f"Result POST failed with status code: {response.status_code}")
    except Exception as e:
        _LOGGER.warning(f"Unable to access the Web Server. {e}")
    finally:
        _LOGGER.info(f"Trajectory file transmitted:")
        _LOGGER.info(f"\tmutant: {mutant}, replica_id: {replica_id}, \n\ttrajectory_file: {trajectory_filepath}, \n\ttopology_file: {topology_filepath}.")
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
    for i, mutant in enumerate(mutants):
        mutant_result = []
        mutant_dir = path.join(WORK_DIR, f"mutant_{i}")
        mutant_stru = mutate_stru(wt_stru, mutant, engine="pymol")

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
        mut_constraints = []
        try:
            # TODO: A correct manner to parse the constraints.
            for cons in md_constraints:
                mut_constraints.append(cons(mutant_stru))
                continue
        except:
            _LOGGER.error(f"Exception raised when loading `constraints_str`: {e}")

        param_method = interface.amber.build_md_parameterizer()
        
        md_result: List[StructureEnsemble] = equi_md_sampling(
            stru=mutant_stru,
            param_method=param_method,
            prod_constrain=mut_constraints,
            prod_time=md_length,
            record_period=md_length*0.01,
            work_dir=f"{mutant_dir}/MD/",
            cluster_job_config=gpu_job_config,
            cpu_equi_step=True,
            cpu_equi_job_config=cpu_job_config,
            job_check_period=10,
        )

        result_record_dict = {
            "mutant": get_mutant_name_str(mutant),
        }

        for replica_id, stru_esm in enumerate(md_result):
            mutant_name = get_mutant_name_str(mutant=mutant)

            post_trajectory_and_topology_file(
                mutant=mutant_name, replica_id=replica_id,
                trajectory_filepath = stru_esm.coordinate_list,
                topology_filepath = stru_esm.topology_source_file
            )

        if has_ligand:
            spi_list = list()
            for ensemble in md_result:
                spi_value = spi_metric(ensemble, mutant_stru.ligands[0], pocket)
                spi_list.append(spi_value)
            result_record_dict["spi"] = mean(spi_list)

        post_trajectory_and_topology_file(result_record_dict)

        # Send a request to the backend of Web Application to update status and progress.
        synchronize_job_status(status=StatusCode.RUNNING, progress=i/mutants_count)

    synchronize_job_status(status=StatusCode.EXIT_OK, progress=1.0)
except Exception as e:
    _LOGGER.error(e)
    synchronize_job_status(status=StatusCode.EXIT_WITH_ERROR)
