from __future__ import annotations

import json
import re
import tempfile
from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from zipfile import ZIP_DEFLATED, ZipFile

from enzy_htp import interface
from enzy_htp.core.clusters.accre_r9 import AccreR9
from enzy_htp.geometry import deployable_equi_md_sampling
from enzy_htp.mutation import assign_mutant, mutate_stru
from enzy_htp.mutation_class import get_mutant_name_str
from enzy_htp.preparation import remove_hydrogens, remove_solvent, protonate_stru
from enzy_htp.structure import PDBParser, Structure, StructureConstraint
from enzy_htp.structure.structure_constraint import (
    create_angle_constraint,
    create_dihedral_constraint,
    create_distance_constraint,
)

from .models import Experiment

PACKAGE_VERSION = "1.0"
DEFAULT_REPLICA_COUNT = 3


def build_manual_md_package(experiment: Experiment) -> Tuple[BytesIO, str]:
    """Build a deployable MD input package and return a zip BytesIO and filename."""
    pdb_path = experiment.pdb_filepath
    if not pdb_path or not Path(pdb_path).is_file():
        raise ValueError("PDB file not found. Please re-upload the PDB file.")

    md_length = _coerce_md_length(experiment.md_length)
    constraints_spec = _normalize_constraints(experiment.constraints)

    with tempfile.TemporaryDirectory(prefix="enzyhtp_md_pack_") as temp_dir:
        pack_root = Path(temp_dir) / "manual_md_pack"
        inputs_dir = pack_root / "inputs"
        jobs_dir = pack_root / "jobs"
        scripts_dir = pack_root / "generated_scripts"
        inputs_dir.mkdir(parents=True, exist_ok=True)
        jobs_dir.mkdir(parents=True, exist_ok=True)
        scripts_dir.mkdir(parents=True, exist_ok=True)

        wt_stru = _prepare_wt_structure(pdb_path)
        mutants = assign_mutant(stru=wt_stru, pattern=experiment.mutation_pattern)

        manifest_jobs: List[Dict] = []
        mutant_records: List[Dict] = []

        for mutant_index, mutant in enumerate(mutants):
            mutant_name = get_mutant_name_str(mutant)
            safe_mutant_name = _safe_name(mutant_name or f"mutant_{mutant_index}")
            mutant_dir = inputs_dir / safe_mutant_name
            md_dir = mutant_dir / "MD"
            md_dir.mkdir(parents=True, exist_ok=True)

            mutant_stru = mutate_stru(wt_stru, mutant, engine="pymol")
            _prepare_mutant_structure(mutant_stru)

            constraints = _build_constraints(mutant_stru, constraints_spec)
            gpu_job_config, cpu_job_config = _default_job_configs()
            param_method = interface.amber.build_md_parameterizer()

            md_results = deployable_equi_md_sampling(
                stru=mutant_stru,
                param_method=param_method,
                parallel_runs=DEFAULT_REPLICA_COUNT,
                work_dir=str(md_dir),
                prod_constrain=constraints,
                prod_time=md_length,
                record_period=md_length * 0.01,
                cluster_job_config=gpu_job_config,
                cpu_equi_step=True,
                cpu_equi_job_config=cpu_job_config,
            )

            mutant_records.append({
                "name": mutant_name,
                "safe_name": safe_mutant_name,
                "replica_count": len(md_results),
                "path": f"inputs/{safe_mutant_name}",
            })

            for replica_id, replica_result in enumerate(md_results):
                job_list = replica_result.get("job_list", [])
                for job_index, job in enumerate(job_list):
                    job_id = _safe_name(f"{safe_mutant_name}_rep{replica_id}_job{job_index}")
                    script_name = f"{job_id}.sh"
                    script_path = jobs_dir / script_name
                    script_path.write_text(job.sub_script_str, encoding="utf-8")

                    job_meta = _build_job_manifest_entry(
                        job_id=job_id,
                        mutant_name=mutant_name,
                        replica_id=replica_id,
                        pack_root=pack_root,
                        job=job,
                        script_path=f"jobs/{script_name}",
                    )
                    manifest_jobs.append(job_meta)

        _write_manifest(
            pack_root=pack_root,
            experiment=experiment,
            mutant_records=mutant_records,
            jobs=manifest_jobs,
            md_length=md_length,
            constraints_spec=constraints_spec,
        )
        _write_cli_assets(pack_root)

        zip_bytes = BytesIO()
        with ZipFile(zip_bytes, "w") as zf:
            for file_path in pack_root.rglob("*"):
                if file_path.is_file():
                    zf.write(file_path, file_path.relative_to(pack_root), compress_type=ZIP_DEFLATED)
        zip_bytes.seek(0)

        zip_prefix = re.sub(r'[\\/:"*?<>|]', "", experiment.name)
        zip_name = f"{zip_prefix} Manual MD Pack.zip"
        return zip_bytes, zip_name


def _prepare_wt_structure(pdb_path: str) -> Structure:
    wt_stru = PDBParser().get_structure(pdb_path)
    remove_solvent(wt_stru)
    remove_hydrogens(stru=wt_stru, polypeptide_only=True)
    protonate_stru(stru=wt_stru, ph=7.4, protonate_ligand=True)
    return wt_stru


def _prepare_mutant_structure(mutant_stru: Structure) -> None:
    ligand_chrg_spin_mapper = {}
    if mutant_stru.ligands:
        for ligand in mutant_stru.ligands:
            ligand_chrg_spin_mapper[ligand.name] = (0, 1)
    mutant_stru.assign_ncaa_chargespin(ligand_chrg_spin_mapper)
    remove_hydrogens(mutant_stru, polypeptide_only=True)
    protonate_stru(mutant_stru, protonate_ligand=False)


def _default_job_configs() -> Tuple[Dict, Dict]:
    cluster = AccreR9()
    gpu_job_config = {
        "cluster": cluster,
        "res_keywords": {
            "account": "csb_gpu_acc",
            "partition": "batch_gpu",
            "nodes": "1",
            "node_cores": "nvidia_geforce_rtx_2080_ti:1",
        },
    }
    cpu_job_config = {
        "cluster": cluster,
        "res_keywords": {
            "account": "yang_lab",
            "partition": "batch",
            "walltime": "10-00:00:00",
        },
    }
    return gpu_job_config, cpu_job_config


def _build_constraints(stru: Structure, constraints_spec: List[Dict]) -> List[StructureConstraint]:
    if not constraints_spec:
        return []
    built: List[StructureConstraint] = []
    for constraint in constraints_spec:
        ctype = str(constraint.get("type", "")).lower()
        args = constraint.get("arguments", [])
        if not isinstance(args, list):
            continue
        if ctype == "distance":
            cons = _create_constraint(
                create_distance_constraint, stru, args, expected_atoms=2
            )
        elif ctype == "angle":
            cons = _create_constraint(
                create_angle_constraint, stru, args, expected_atoms=3
            )
        elif ctype == "dihedral":
            cons = _create_constraint(
                create_dihedral_constraint, stru, args, expected_atoms=4
            )
        else:
            cons = None
        if cons is not None:
            built.append(cons)
    return built


def _create_constraint(factory, stru: Structure, args: List, expected_atoms: int) -> Optional[StructureConstraint]:
    if len(args) < expected_atoms:
        return None
    atom_args = args[:expected_atoms]
    target_value = None
    if len(args) >= expected_atoms + 1:
        try:
            target_value = float(args[expected_atoms])
        except (TypeError, ValueError):
            target_value = None
    if target_value is None:
        temp = factory(*atom_args, target_value=0.0, topology=stru)
        return temp.clone_current()
    return factory(*atom_args, target_value=target_value, topology=stru)


def _build_job_manifest_entry(
    job_id: str,
    mutant_name: str,
    replica_id: int,
    pack_root: Path,
    job,
    script_path: str,
) -> Dict:
    env_settings = job.mimo.get("env_settings", "")
    if isinstance(env_settings, dict):
        env_lines = "\n".join(filter(None, [env_settings.get("head", ""), env_settings.get("tail", "")])).strip()
    else:
        env_lines = str(env_settings).strip()
    res_keywords = job.mimo.get("res_keywords", {})
    resource_lines = job.cluster.parser_resource_str(res_keywords)
    work_dir = job.mimo.get("work_dir", "")
    try:
        work_dir_rel = str(Path(work_dir).resolve().relative_to(pack_root.resolve()))
    except Exception:
        work_dir_rel = str(work_dir)

    return {
        "id": job_id,
        "mutant": mutant_name,
        "replica_id": replica_id,
        "work_dir": work_dir_rel,
        "commands": job.mimo.get("commands", []),
        "env_lines": env_lines,
        "resource_lines": resource_lines.strip(),
        "step_names": job.mimo.get("md_names", []),
        "default_script": script_path,
    }


def _write_manifest(
    pack_root: Path,
    experiment: Experiment,
    mutant_records: List[Dict],
    jobs: List[Dict],
    md_length: float,
    constraints_spec: List[Dict],
) -> None:
    manifest = {
        "version": PACKAGE_VERSION,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "experiment": {
            "id": experiment.id,
            "name": experiment.name,
            "md_length_ns": md_length,
            "mutation_pattern": experiment.mutation_pattern,
            "constraints": constraints_spec,
        },
        "mutants": mutant_records,
        "jobs": jobs,
        "inputs_root": "inputs",
    }
    (pack_root / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def _write_cli_assets(pack_root: Path) -> None:
    base_dir = Path(__file__).resolve().parents[1]
    cli_path = base_dir / "tools" / "md_cli.py"
    readme_path = base_dir / "templates" / "manual_md" / "README.md"

    (pack_root / "md_cli.py").write_text(cli_path.read_text(encoding="utf-8"), encoding="utf-8")
    (pack_root / "README.md").write_text(readme_path.read_text(encoding="utf-8"), encoding="utf-8")
    (pack_root / "md_cli_config.json").write_text(
        _default_cli_config_json(), encoding="utf-8"
    )


def _default_cli_config_json() -> str:
    config = {
        "default_scheduler": "slurm",
        "schedulers": {
            "slurm": {
                "submit_cmd": "sbatch {script_path}",
                "status_cmd": "squeue -j {job_id}",
                "cancel_cmd": "scancel {job_id}",
                "script_template": (
                    "#!/bin/bash\n"
                    "#SBATCH --job-name={job_name}\n"
                    "#SBATCH --output={job_name}.out\n"
                    "#SBATCH --error={job_name}.err\n"
                    "{resource_lines}\n\n"
                    "{env_lines}\n"
                    "cd {work_dir}\n"
                    "{commands}\n"
                ),
            },
            "pbs": {
                "submit_cmd": "qsub {script_path}",
                "status_cmd": "qstat {job_id}",
                "cancel_cmd": "qdel {job_id}",
                "script_template": (
                    "#!/bin/bash\n"
                    "#PBS -N {job_name}\n"
                    "#PBS -o {job_name}.out\n"
                    "#PBS -e {job_name}.err\n"
                    "{resource_lines}\n\n"
                    "{env_lines}\n"
                    "cd {work_dir}\n"
                    "{commands}\n"
                ),
            },
            "lsf": {
                "submit_cmd": "bsub < {script_path}",
                "status_cmd": "bjobs {job_id}",
                "cancel_cmd": "bkill {job_id}",
                "script_template": (
                    "#!/bin/bash\n"
                    "#BSUB -J {job_name}\n"
                    "#BSUB -o {job_name}.out\n"
                    "#BSUB -e {job_name}.err\n"
                    "{resource_lines}\n\n"
                    "{env_lines}\n"
                    "cd {work_dir}\n"
                    "{commands}\n"
                ),
            },
        },
    }
    return json.dumps(config, indent=2)


def _coerce_md_length(value) -> float:
    try:
        md_length = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("Invalid md_length; expected a numeric value in nanoseconds.") from exc
    if md_length <= 0:
        raise ValueError("Invalid md_length; expected a positive value in nanoseconds.")
    return md_length


def _normalize_constraints(constraints_spec) -> List[Dict]:
    if constraints_spec in (None, ""):
        return []
    if isinstance(constraints_spec, str):
        try:
            constraints_spec = json.loads(constraints_spec)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid constraints format; expected JSON list.") from exc
    if not isinstance(constraints_spec, list):
        raise ValueError("Invalid constraints format; expected list of constraint objects.")
    return constraints_spec


def _safe_name(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value).strip("_")
