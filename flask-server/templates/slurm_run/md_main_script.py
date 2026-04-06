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
import re
from contextlib import ExitStack
from os import environ, path
from typing import Callable, Dict, List, Optional, Tuple, Union
from time import sleep
from requests import patch, post, put
from statistics import mean
from json import dumps, loads

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

resolved_pdb_filepath = path.join(file_dir, path.basename(pdb_filename)) if pdb_filename else str()
if (not resolved_pdb_filepath) or (not path.isfile(resolved_pdb_filepath)):
    legacy_pdb_filepath = path.join(file_dir, pdb_filename) if pdb_filename else str()
    if legacy_pdb_filepath and path.isfile(legacy_pdb_filepath):
        resolved_pdb_filepath = legacy_pdb_filepath
    else:
        _LOGGER.warning(
            f"Unable to find PDB by basename under file_dir. "
            f"basename_path={resolved_pdb_filepath}, legacy_path={legacy_pdb_filepath}"
        )

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
        "account" : "yang_lab",
        "partition" : "batch",
        'walltime' : '10-00:00:00',
    }
}

PROGRESS_UPDATE_URL = f"https://{app_host}/api/experiment/{experiment_id}"
TRAJ_UPLOAD_URL = f"https://{app_host}/api/experiment/{experiment_id}?store_only=1"
EQUIL_ALL_STAGE_FILES = ["equi_npt.out", "equi_npt_free_bb.out"]
EQUIL_NPT_STAGE_FILES = ["equi_npt.out", "equi_npt_free_bb.out"]
EQUILIBRATION_METHOD_LABEL = "Chodera automated equilibration detection scheme (PMCID: PMC4945107)"
EQUILIBRATION_MIN_TAIL_POINTS = 10

MDOUT_STATE_PATTERN = re.compile(
    r"NSTEP\s*=\s*(\d+)\s+TIME\(PS\)\s*=\s*([-\d.Ee+]+)\s+TEMP\(K\)\s*=\s*([-\d.Ee+]+)\s+PRESS\s*=\s*([-\d.Ee+]+)"
)
MDOUT_ENERGY_PATTERN = re.compile(
    r"Etot\s*=\s*([-\d.Ee+]+)\s+EKtot\s*=\s*([-\d.Ee+]+)\s+EPtot\s*=\s*([-\d.Ee+]+)"
)
MDOUT_TRAILER_SECTION_PATTERN = re.compile(
    r"A\s+V\s+E\s+R\s+A\s+G\s+E\s+S\s+O\s+V\s+E\s+R|R\s+M\s+S\s+F\s+L\s+U\s+C\s+T\s+U\s+A\s+T\s+I\s+O\s+N\s+S"
)

def _parse_mdout_records(mdout_filepath: str) -> List[dict]:
    """Parse Amber mdout records into a list of time/temperature/pressure/energy entries."""
    if (not mdout_filepath) or (not path.isfile(mdout_filepath)):
        return list()
    try:
        with open(mdout_filepath, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
    except Exception as exc:
        _LOGGER.warning(f"Unable to read mdout file {mdout_filepath}: {exc}")
        return list()

    records: List[dict] = []
    line_index = 0
    while (line_index < len(lines)):
        if MDOUT_TRAILER_SECTION_PATTERN.search(lines[line_index]):
            break
        state_match = MDOUT_STATE_PATTERN.search(lines[line_index])
        if (not state_match):
            line_index += 1
            continue
        nstep_str, time_ps_str, temp_k_str, press_str = state_match.groups()
        record = {
            "nstep": int(float(nstep_str)),
            "time_ps": float(time_ps_str),
            "temp_k": float(temp_k_str),
            "press": float(press_str),
            "etot": None,
            "ektot": None,
            "eptot": None,
        }
        if records:
            last_record = records[-1]
            if (
                record["nstep"] <= last_record["nstep"]
                and record["time_ps"] <= last_record["time_ps"]
            ):
                break
        if (line_index + 1 < len(lines)):
            energy_match = MDOUT_ENERGY_PATTERN.search(lines[line_index + 1])
            if (energy_match):
                etot_str, ektot_str, eptot_str = energy_match.groups()
                record["etot"] = float(etot_str)
                record["ektot"] = float(ektot_str)
                record["eptot"] = float(eptot_str)
                line_index += 1
        records.append(record)
        line_index += 1
    return records

def _collect_stage_records(replica_dir: str, stage_filenames: List[str]) -> List[dict]:
    """Collect and time-stitch mdout records from stages in a replica directory."""
    stitched_records: List[dict] = []
    time_offset = 0.0
    for stage_filename in stage_filenames:
        mdout_path = path.join(replica_dir, stage_filename)
        stage_records = _parse_mdout_records(mdout_path)
        if (not stage_records):
            continue
        stage_start_time = stage_records[0]["time_ps"]
        for record in stage_records:
            entry = record.copy()
            entry["time_ps"] = (entry["time_ps"] - stage_start_time) + time_offset
            entry["stage"] = stage_filename.removesuffix(".out")
            stitched_records.append(entry)
        time_offset = stitched_records[-1]["time_ps"] if stitched_records else time_offset
    return stitched_records

def _collect_equilibration_record_sets(replica_dir: str) -> Tuple[List[dict], List[dict]]:
    all_stage_records = _collect_stage_records(replica_dir=replica_dir, stage_filenames=EQUIL_ALL_STAGE_FILES)
    npt_stage_records = _collect_stage_records(replica_dir=replica_dir, stage_filenames=EQUIL_NPT_STAGE_FILES)
    return all_stage_records, npt_stage_records

def _plot_equilibration_curve(
    records: List[dict],
    y_key: str,
    y_label: str,
    title: str,
    output_filepath: str,
    stage_order: List[str],
) -> bool:
    """Plot one equilibration curve image from parsed records."""
    if (not records):
        return False
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as exc:
        _LOGGER.warning(f"Matplotlib not available, skip plot {output_filepath}: {exc}")
        return False

    plt.figure(figsize=(8.0, 4.5))
    plotted = False
    for stage in stage_order:
        x_values: List[float] = []
        y_values: List[float] = []
        for record in records:
            if (record.get("stage") != stage):
                continue
            y_value = record.get(y_key)
            if (y_value is None):
                continue
            x_values.append(float(record["time_ps"]))
            y_values.append(float(y_value))
        if (not x_values):
            continue
        plotted = True
        plt.plot(x_values, y_values, linewidth=1.2, label=stage)

    if (not plotted):
        plt.close()
        return False

    plt.xlabel("Time (ps)")
    plt.ylabel(y_label)
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_filepath, dpi=150)
    plt.close()
    return True

def generate_equilibration_plots(trajectory_filepath: str) -> List[str]:
    """Generate temperature/pressure/energy equilibration plots for one replica."""
    replica_dir = path.dirname(trajectory_filepath or "")
    if (not replica_dir) or (not path.isdir(replica_dir)):
        return list()

    all_stage_records, npt_stage_records = _collect_equilibration_record_sets(replica_dir=replica_dir)
    if (not all_stage_records) and (not npt_stage_records):
        return list()

    plot_dir = path.join(replica_dir, "plots")
    try:
        if (not path.isdir(plot_dir)):
            from os import makedirs
            makedirs(plot_dir, exist_ok=True)
    except Exception as exc:
        _LOGGER.warning(f"Unable to create plot directory {plot_dir}: {exc}")
        return list()

    output_paths: List[str] = []
    temperature_plot = path.join(plot_dir, "equil_temperature.png")
    if _plot_equilibration_curve(
        records=all_stage_records,
        y_key="temp_k",
        y_label="Temperature (K)",
        title="Equilibration Temperature",
        output_filepath=temperature_plot,
        stage_order=[stage.removesuffix(".out") for stage in EQUIL_ALL_STAGE_FILES],
    ):
        output_paths.append(temperature_plot)

    pressure_plot = path.join(plot_dir, "equil_pressure.png")
    if _plot_equilibration_curve(
        records=npt_stage_records,
        y_key="press",
        y_label="Pressure",
        title="Equilibration Pressure (NPT)",
        output_filepath=pressure_plot,
        stage_order=[stage.removesuffix(".out") for stage in EQUIL_NPT_STAGE_FILES],
    ):
        output_paths.append(pressure_plot)

    energy_plot = path.join(plot_dir, "equil_energy.png")
    if _plot_equilibration_curve(
        records=all_stage_records,
        y_key="etot",
        y_label="Etot",
        title="Equilibration Total Energy",
        output_filepath=energy_plot,
        stage_order=[stage.removesuffix(".out") for stage in EQUIL_ALL_STAGE_FILES],
    ):
        output_paths.append(energy_plot)

    return output_paths

def _estimate_statistical_inefficiency(values: List[float]) -> float:
    """Estimate statistical inefficiency g from a 1D timeseries."""
    n = len(values)
    if (n < 3):
        return 1.0
    mean_val = sum(values) / n
    centered = [value - mean_val for value in values]
    variance = sum(value * value for value in centered) / n
    if (variance <= 1e-16):
        return 1.0

    g = 1.0
    max_lag = max(1, min(n - 1, n // 2))
    for lag in range(1, max_lag + 1):
        cov = sum(centered[idx] * centered[idx + lag] for idx in range(0, n - lag)) / (n - lag)
        autocorrelation = cov / variance
        if (autocorrelation <= 0.0) and (lag > 5):
            break
        g += 2.0 * autocorrelation * (1.0 - lag / n)
    return max(float(g), 1.0)

def _detect_equilibration(values: List[float]) -> Tuple[int, float, float]:
    """Detect equilibration onset t0 by maximizing effective sample size."""
    sample_size = len(values)
    if (sample_size == 0):
        return 0, 1.0, 0.0
    if (sample_size < 5):
        return 0, 1.0, float(sample_size)

    best_t0 = 0
    best_g = 1.0
    # Initialize from zero so candidate windows can actually win.
    best_neff = 0.0
    for t0 in range(0, sample_size - 2):
        truncated = values[t0:]
        g_value = _estimate_statistical_inefficiency(truncated)
        neff = len(truncated) / g_value if (g_value > 0.0) else 0.0
        if (neff > best_neff):
            best_t0 = t0
            best_g = g_value
            best_neff = neff
    return int(best_t0), float(best_g), float(best_neff)

def _assess_equilibration_series(records: List[dict], key: str) -> Optional[dict]:
    """Run Chodera-style equilibration detection for one metric series."""
    if (not records):
        return None
    values: List[float] = []
    times_ps: List[float] = []
    for record in records:
        value = record.get(key)
        if (value is None):
            continue
        values.append(float(value))
        times_ps.append(float(record["time_ps"]))
    if (not values):
        return None

    t0_index, g_value, neff = _detect_equilibration(values=values)
    safe_t0 = min(max(t0_index, 0), len(values) - 1)
    discarded_fraction = safe_t0 / len(values)
    tail_n_points = len(values) - safe_t0
    status = "equilibrated" if (tail_n_points > EQUILIBRATION_MIN_TAIL_POINTS) else "not equilibrated"
    return {
        "n_points": len(values),
        "t0_index": safe_t0,
        "t0_ps": float(times_ps[safe_t0]),
        "tail_n_points": tail_n_points,
        "g": g_value,
        "neff_max": neff,
        "discarded_fraction": discarded_fraction,
        "status": status,
    }

def generate_equilibration_assessment(
    trajectory_filepath: str,
    mutant: str,
    replica_id: Union[int, str],
) -> Optional[str]:
    """Generate one JSON assessment file for equilibration quality."""
    replica_dir = path.dirname(trajectory_filepath or "")
    if (not replica_dir) or (not path.isdir(replica_dir)):
        return None

    all_stage_records, npt_stage_records = _collect_equilibration_record_sets(replica_dir=replica_dir)
    if (not all_stage_records) and (not npt_stage_records):
        return None

    plots_dir = path.join(replica_dir, "plots")
    try:
        if (not path.isdir(plots_dir)):
            from os import makedirs
            makedirs(plots_dir, exist_ok=True)
    except Exception as exc:
        _LOGGER.warning(f"Unable to create plots directory for equilibration assessment: {exc}")
        return None

    series_assessment = {
        "temp_k": _assess_equilibration_series(records=all_stage_records, key="temp_k"),
        "press": _assess_equilibration_series(records=npt_stage_records or all_stage_records, key="press"),
        "etot": _assess_equilibration_series(records=all_stage_records, key="etot"),
    }
    series_assessment = {key: value for key, value in series_assessment.items() if value is not None}
    if (not series_assessment):
        return None

    status_values = [entry.get("status", "unknown") for entry in series_assessment.values()]
    overall_status = "equilibrated" if all(status == "equilibrated" for status in status_values) else "caution"
    assessment_dict = {
        "method": EQUILIBRATION_METHOD_LABEL,
        "mutant": mutant,
        "replica_id": str(replica_id),
        "overall_status": overall_status,
        "series": series_assessment,
    }

    assessment_filepath = path.join(plots_dir, "equil_assessment.json")
    try:
        with open(assessment_filepath, "w", encoding="utf-8") as fobj:
            fobj.write(dumps(assessment_dict, ensure_ascii=False, indent=2))
    except Exception as exc:
        _LOGGER.warning(f"Unable to write equilibration assessment file {assessment_filepath}: {exc}")
        return None
    return assessment_filepath

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
    
def post_trajectory_and_topology_file(
    mutant: str,
    replica_id: Union[int, str],
    trajectory_filepath: str,
    topology_filepath: str,
    equil_plot_filepaths: Optional[List[str]] = None,
    equil_assessment_filepath: Optional[str] = None,
) -> None:
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
    equil_plot_filepaths = equil_plot_filepaths or []
    try:
        data = {
            "mutant": mutant,
            "replica_id": str(replica_id),
        }
        with ExitStack() as file_stack:
            traj_handle = file_stack.enter_context(open(trajectory_filepath, mode="rb"))
            topo_handle = file_stack.enter_context(open(topology_filepath, mode="rb"))
            files: List[Tuple[str, Tuple[str, object, str]]] = [
                ("trajectory", (path.basename(trajectory_filepath), traj_handle, "application/octet-stream")),
                ("topology", (path.basename(topology_filepath), topo_handle, "application/octet-stream")),
            ]
            for plot_filepath in equil_plot_filepaths:
                if (not plot_filepath) or (not path.isfile(plot_filepath)):
                    continue
                ext = path.splitext(plot_filepath)[1].lower()
                if (ext not in {".png", ".jpg", ".jpeg", ".webp", ".gif"}):
                    continue
                plot_handle = file_stack.enter_context(open(plot_filepath, mode="rb"))
                image_mime = "image/png" if ext == ".png" else "application/octet-stream"
                files.append(("equil_plots", (path.basename(plot_filepath), plot_handle, image_mime)))
            if equil_assessment_filepath and path.isfile(equil_assessment_filepath):
                assessment_handle = file_stack.enter_context(open(equil_assessment_filepath, mode="rb"))
                files.append((
                    "equil_assessment",
                    (path.basename(equil_assessment_filepath), assessment_handle, "application/json"),
                ))
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
        if (equil_plot_filepaths):
            _LOGGER.info(f"\tequilibration_plots: {equil_plot_filepaths}")
        if (equil_assessment_filepath):
            _LOGGER.info(f"\tequilibration_assessment: {equil_assessment_filepath}")
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

    wt_stru = PDBParser().get_structure(resolved_pdb_filepath)
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
                equilibration_plot_paths = generate_equilibration_plots(
                    trajectory_filepath=stru_esm.coordinate_list,
                )
                equilibration_assessment_filepath = generate_equilibration_assessment(
                    trajectory_filepath=stru_esm.coordinate_list,
                    mutant=mutant_name,
                    replica_id=replica_id,
                )

                post_trajectory_and_topology_file(
                    mutant=mutant_name, replica_id=replica_id,
                    trajectory_filepath=stru_esm.coordinate_list,
                    topology_filepath=stru_esm.topology_source_file,
                    equil_plot_filepaths=equilibration_plot_paths,
                    equil_assessment_filepath=equilibration_assessment_filepath,
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
