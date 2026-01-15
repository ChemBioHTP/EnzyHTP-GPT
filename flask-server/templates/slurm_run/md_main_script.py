#! python3
# -*- encoding: utf-8 -*-
'''
The main script of the MD Slurm Job. This script is currently for test use.

@File    :   main_script.py
@Created :   2024/06/21 16:18
@Author  :   Zhong, Yinjie
@Contact :   yinjie.zhong@vanderbilt.edu
'''

# Here put the import lib.
from os import environ, path
from typing import List, Union, Dict, Callable
from time import sleep
from requests import post, put, patch
from statistics import mean
from json import loads

# Here put enzy_htp modules.
from enzy_htp import interface, _LOGGER
from enzy_htp.core.clusters.accre_r9 import AccreR9
from enzy_htp.structure import PDBParser, StructureEnsemble, StructureConstraint
from enzy_htp.structure.structure_constraint import create_distance_constraint, create_angle_constraint, create_dihedral_constraint
from enzy_htp.structure.structure_selection import select_stru
from enzy_htp.preparation import remove_solvent, remove_hydrogens, protonate_stru
from enzy_htp.mutation import assign_mutant, mutate_stru
from enzy_htp.mutation_class import get_mutant_name_str
from enzy_htp.geometry import equi_md_sampling

# Here put local modules.
from analysis_main_script import main as analysis_main

class StatusCode():
    """
    Class representing various execution statuses.

    Attributes:
        CREATED (int): The initial status when a WorkUnit or WorkFlow instance is created. Value: -9
        PENDING (int): The status when a WorkUnit or WorkFlow instance is pending for initialization and execution. Value: -8
        INITIALIZING (int): The status when a WorkUnit or WorkFlow instance is undergoing initialization. Value: -7
        READY_TO_START (int): The status when a WorkUnit or WorkFlow instance has passed the self-inspection but hasn't yet been started. Value: -6
        READY_WITH_UPDATES (int): The status when a previously executed WorkUnit or WorkFlow instance have its input arguments changed
                                due to the influence from the update in the input values of the task during continue computing. Value: -5
        SUSPECIOUS_UPDATES (int): The status when a previously `EXIT_OK` WorkUnit or WorkFlow instance has detected but unsure argument updates
                                    during reloading. Value: -4
        RUNNING (int): Indicates that the workunit or workflow is currently in execution. Value: -3
        PAUSE_IN_INNER_UNITS (int): Specific to WorkFlow and ControlWorkUnit instances. Indicates
                                    that the workflow is running but an inner unit is paused as expected. Value: -2
        EXPECTED_PAUSE (int): Specific to Basic WorkUnit instances. Indicates that a unit is paused and its outer
                              layers should be marked as `RUNNING_WITH_PAUSE_IN_INNER_UNITS`. Value: -1
        EXIT_OK (int): Indicates successful completion of the work unit or workflow. Value: 0
        ERROR_IN_INNER_UNITS (int): Specific to WorkFlow and ControlWorkUnit. Indicates error(s) in the
                                    inner units of a workflow. Value: 1
        EXIT_WITH_ERROR (int): Specific to Basic WorkUnit instances. Indicates that the work unit or workflow
                               exited with an error. Value: 2
        EXIT_WITH_ERROR_AND_PAUSE (int): Specific to WorkFlow and ControlWorkUnit. Indicates the coexistence of error(s)
                                        and expected pause(s) in the inner units of a workflow. Value: 3
        CANCELLED (int): Indicates that the workunit or workflow is cancelled.
                        Any workflows or workunits inside it should be marked with this status. Value: 8
        DEPRECATED (int): Indicates that the workunit or workflow is deprecated.
                        Any workflows or workunits inside it should be marked with this status and deleted. Value: 8
        FAILED_INITIALIZATION (int): Indicates that the initialization of the workunit or workflow failed. Value: 9
    """
    CREATED = -9
    PENDING = -8
    INITIALIZING = -7
    READY_TO_START = -6
    READY_WITH_UPDATES = -5
    SUSPECIOUS_UPDATES = -4             # For Reload time only.
    RUNNING = -3
    RUNNING_WITH_PAUSE_IN_INNER_UNITS = -2   # For WorkFlow and ControlWorkUnit only.
    EXPECTED_PAUSE = -1                 # For Basic WorkUnit only. If a unit is paused, set its outer layers as `RUNNING_WITH_PAUSE_IN_INNER_UNITS`.
    EXIT_OK = 0
    EXIT_WITH_ERROR_IN_INNER_UNITS = 1  # For WorkFlow and ControlWorkUnit only.
    EXIT_WITH_ERROR = 2                 # For Science API only.
    EXIT_WITH_ERROR_AND_PAUSE = 3       # For WorkFlow and ControlWorkUnit only.
    CANCELLED = 7
    DEPRECATED = 8
    FAILED_INITIALIZATION = 9

    #region Status Group, for logical judgment only.
    queued_status = [PENDING, INITIALIZING, RUNNING, RUNNING_WITH_PAUSE_IN_INNER_UNITS]
    pause_excluding_error_statuses = [EXPECTED_PAUSE, RUNNING_WITH_PAUSE_IN_INNER_UNITS]
    pause_including_error_statuses = [EXPECTED_PAUSE, RUNNING_WITH_PAUSE_IN_INNER_UNITS, EXIT_WITH_ERROR_AND_PAUSE]
    error_excluding_pause_statuses = [EXIT_WITH_ERROR, EXIT_WITH_ERROR_IN_INNER_UNITS, FAILED_INITIALIZATION]
    error_including_pause_statuses = [EXIT_WITH_ERROR, EXIT_WITH_ERROR_IN_INNER_UNITS, FAILED_INITIALIZATION, EXIT_WITH_ERROR_AND_PAUSE]
    error_or_pause_statuses = [EXIT_WITH_ERROR, EXIT_WITH_ERROR_IN_INNER_UNITS, EXPECTED_PAUSE, RUNNING_WITH_PAUSE_IN_INNER_UNITS, EXIT_WITH_ERROR_AND_PAUSE]
    unexecutable_statuses = [CREATED, PENDING, INITIALIZING, DEPRECATED, FAILED_INITIALIZATION]
    unexecuted_statuses = [CREATED, PENDING, INITIALIZING, READY_TO_START, FAILED_INITIALIZATION]    # Note its distinction from `unexecutable_statuses`.
    skippable_statuses = [EXIT_OK]
    #endregion

    status_text_mapper = {
        CREATED: "Created",
        PENDING: "Pending",
        INITIALIZING: "Initializing",
        READY_TO_START: "Ready to Start",
        READY_WITH_UPDATES: "Ready with Updates",
        SUSPECIOUS_UPDATES: "Suspecious Updates",
        RUNNING: "Running",
        RUNNING_WITH_PAUSE_IN_INNER_UNITS: "Running with Pause in Inner Units",
        EXPECTED_PAUSE: "Expected Pause",
        EXIT_OK: "Completed",
        EXIT_WITH_ERROR_IN_INNER_UNITS: "Exit with Error in Inner Units",
        EXIT_WITH_ERROR: "Exit with Error",
        EXIT_WITH_ERROR_AND_PAUSE: "Exit with Error and Pause",
        CANCELLED: "Cancelled",
        DEPRECATED: "Deprecated",
        FAILED_INITIALIZATION: "Initialization Failed."
    }


DATA_DIR = f"{path.dirname(path.abspath(__file__))}/data/"
WORK_DIR = f"{path.dirname(path.abspath(__file__))}/work_dir/"

app_host = environ.get("app_host")
experiment_id = environ.get("experiment_id")
file_dir = environ.get("file_dir", path.curdir)
access_token = environ.get("access_token")
pdb_filename = environ.get("pdb_filename")
mutation_pattern = environ.get("mutation_pattern")
constraints_str = environ.get("constraints_str")
md_length = float(environ.get("md_length", 0.05))
ph = float(environ.get("ph", 7.4))
pocket_range = int(environ.get("pocket_range", 5))
metrics = loads(environ.get("metrics", "[]"))

cluster = AccreR9()
gpu_job_config = {
    "cluster" : cluster,
    "res_keywords" : {
        "account" : "csb_gpu_acc",
        "partition" : "batch_gpu",
        "nodes": "1",
        "node_cores" : "nvidia_geforce_rtx_2080_ti:1",
    }
}
cpu_job_config = {
    "cluster" : cluster,
    "res_keywords" : {
        "account" : "yang_lab_csb",
        "partition" : "batch",
        'walltime' : '10-00:00:00',
    }
}

PROGRESS_UPDATE_URL = f"https://{app_host}/api/experiment/{experiment_id}"
TRAJ_UPLOAD_URL = f"https://{app_host}/api/experiment/{experiment_id}?store_only=1"

def synchronize_job_status(status: int = None, progress: float = None) -> None:
    """Synchronize the Job Status to the Web Server. If the web server is not accessible, log the status and error information.
    
    Args:
        status (int): Latest job status.
        progress (float): The progress of current job (Float value from 0 to 1).
    """    
    try:
        response = patch(PROGRESS_UPDATE_URL,
            headers={
                "Authorization": f"Bearer {access_token}"
            },
            data={
                "status": status,
                "progress": progress,
            },
            timeout=30)
        if (response.ok):
            _LOGGER.info(f"Updated Job status and progress.")
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
    if (not trajectory_filepath or not topology_filepath):
        return
    if (not path.isfile(trajectory_filepath) or not path.isfile(topology_filepath)):
        _LOGGER.warning("Trajectory/topology file missing, skipping upload.")
        return
    try:
        data = {
            "mutant": mutant,
            "replica_id": str(replica_id),
        }
        with open(trajectory_filepath, mode="rb") as traj_handle, open(topology_filepath, mode="rb") as topo_handle:
            files = {
                "trajectory": traj_handle,
                "topology": topo_handle,
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

def create_constraints(constraints_str: str) -> List[StructureConstraint]:
    """Create constraints with the json formatted string generated by the metrics planner.
    
    Args:
        constraints_str (str): The json formatted string recording constraint information.
    """
    constraint_function_mapper: Dict[str, Callable] = {
        "distance": create_distance_constraint,
        "angle": create_angle_constraint,
        "dihedral": create_dihedral_constraint,
    }
    constraint_dicts: List[dict] = []
    mutant_constraints = []
    try:
        constraint_dicts = loads(constraints_str)
    except Exception as e:
        _LOGGER.error(f"Exception raised when loading `constraints_str`: {e}")
        return list()
    for constraint_dict in constraint_dicts:
        constraint_type = constraint_dict.get("type", None)
        constraint_arguments = constraint_dict.get("arguments", None)
        constraint_func = constraint_function_mapper.get(constraint_type, None)
        if (not constraint_func):
            _LOGGER.warning(f"No matched constraint for `{constraint_type}`.")
        else:
            try:
                mutant_constraints.append(constraint_func(*constraint_arguments))
            except Exception as exc:
                _LOGGER.error(f"Exception raised when creating `{constraint_type}` constraint.")
        continue
    return mutant_constraints

if __name__ == "__main__":
    print(f"Send PATCH request to {PROGRESS_UPDATE_URL} so as to update the status and progress.")
    
    synchronize_job_status(status=StatusCode.INITIALIZING, progress=0.0)

    has_ligand = False
    mut_constraints = create_constraints(constraints_str=constraints_str)

    wt_stru = PDBParser().get_structure(path.join(file_dir, pdb_filename))
    remove_solvent(wt_stru)
    remove_hydrogens(stru=wt_stru, polypeptide_only=True)
    protonate_stru(stru=wt_stru, ph=ph, protonate_ligand=True)

    if (wt_stru.ligands):
        has_ligand = True
    
    try:
        mutants = assign_mutant(stru=wt_stru, pattern=mutation_pattern)
        mutants_count = len(mutants)

        synchronize_job_status(status=StatusCode.RUNNING, progress=0.0)

        # mutation
        for i, mutant in enumerate(mutants):
            mutant_result = []
            mutant_dir = path.join(WORK_DIR, f"mutant_{i}")
            mutant_stru = mutate_stru(wt_stru, mutant, engine="pymol")

            # ligand_pattern = str()
            # region_pattern = str()

            ligand_chrg_spin_mapper = dict()
            pocket = list()
            if (has_ligand):
                for i, ligand in enumerate(mutant_stru.ligands):
                    # Set charge-Spin to default value: (0, 1)
                    ligand_chrg_spin_mapper[ligand.name] = (0, 1)
                # Set pocket region pattern.
                # ligand_pattern = "+".join([(f"(resi {ligand.idx} and chain {ligand.chain.name})") for ligand in mutant_stru.ligands])
                # region_pattern = f"br. ({ligand_pattern}) around {pocket_range} and not ({ligand_pattern})"

            mutant_stru.assign_ncaa_chargespin(ligand_chrg_spin_mapper)
            remove_hydrogens(mutant_stru, polypeptide_only=True)
            protonate_stru(mutant_stru, protonate_ligand=False)

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
                    trajectory_filepath=stru_esm.coordinate_list,
                    topology_filepath=stru_esm.topology_source_file
                )
                analysis_main(
                    stru_esm=stru_esm, metrics=metrics,
                    mutant_name=mutant_name, replica_id=replica_id,
                )

            # Send a request to the backend of Web Application to update status and progress.
            progress = (i + 1.0) / mutants_count
            synchronize_job_status(status=StatusCode.RUNNING, progress=(i+1.0)/mutants_count)

        synchronize_job_status(status=StatusCode.EXIT_OK, progress=1.0)
    except Exception as e:
        _LOGGER.error(e)
        synchronize_job_status(status=StatusCode.EXIT_WITH_ERROR)
