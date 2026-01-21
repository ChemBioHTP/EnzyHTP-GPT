#!/usr/bin/env python3
import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path


DEFAULT_CONFIG = {
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

STATE_FILENAME = "job_state.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def ensure_config(config_path: Path) -> dict:
    if config_path.exists():
        return load_json(config_path)
    save_json(config_path, DEFAULT_CONFIG)
    return DEFAULT_CONFIG


def load_manifest(package_dir: Path) -> dict:
    manifest_path = package_dir / "manifest.json"
    if not manifest_path.exists():
        raise FileNotFoundError(f"manifest.json not found in {package_dir}")
    return load_json(manifest_path)


def render_script(job: dict, template: str, package_dir: Path) -> str:
    commands = "\n".join(job.get("commands", []))
    env_lines = job.get("env_lines", "")
    resource_lines = job.get("resource_lines", "")
    work_dir = job.get("work_dir", "")
    work_dir = str((package_dir / work_dir).resolve()) if work_dir else str(package_dir.resolve())
    return template.format(
        job_name=job.get("id", "md_job"),
        commands=commands,
        env_lines=env_lines,
        resource_lines=resource_lines,
        work_dir=work_dir,
    )


def submit_jobs(args: argparse.Namespace) -> int:
    package_dir = Path(args.package).resolve()
    manifest = load_manifest(package_dir)
    config_path = Path(args.config).resolve() if args.config else package_dir / "md_cli_config.json"
    config = ensure_config(config_path)
    scheduler_name = args.scheduler or config.get("default_scheduler", "slurm")
    scheduler = config.get("schedulers", {}).get(scheduler_name)
    if not scheduler:
        raise ValueError(f"Unknown scheduler '{scheduler_name}'.")

    scripts_dir = package_dir / "generated_scripts"
    scripts_dir.mkdir(parents=True, exist_ok=True)
    state_path = package_dir / STATE_FILENAME
    state = {"scheduler": scheduler_name, "jobs": []}

    for job in manifest.get("jobs", []):
        script_content = render_script(job, scheduler["script_template"], package_dir)
        script_path = scripts_dir / f"{job['id']}.sh"
        script_path.write_text(script_content, encoding="utf-8")
        script_path.chmod(script_path.stat().st_mode | 0o111)

        job_record = {
            "id": job["id"],
            "mutant": job.get("mutant"),
            "replica_id": job.get("replica_id"),
            "script_path": str(script_path),
            "submit_output": "",
            "scheduler_job_id": "",
        }

        if not args.no_submit:
            submit_cmd = scheduler["submit_cmd"].format(script_path=script_path)
            result = subprocess.run(submit_cmd, shell=True, capture_output=True, text=True, cwd=package_dir)
            output = (result.stdout or "") + (result.stderr or "")
            job_record["submit_output"] = output.strip()
            job_record["scheduler_job_id"] = _extract_job_id(output)

        state["jobs"].append(job_record)

    save_json(state_path, state)
    print(f"Wrote job state to {state_path}")
    return 0


def status_jobs(args: argparse.Namespace) -> int:
    package_dir = Path(args.package).resolve()
    config_path = Path(args.config).resolve() if args.config else package_dir / "md_cli_config.json"
    config = ensure_config(config_path)
    state_path = package_dir / STATE_FILENAME
    if not state_path.exists():
        print("No job_state.json found. Submit jobs first.", file=sys.stderr)
        return 2

    state = load_json(state_path)
    scheduler_name = args.scheduler or state.get("scheduler") or config.get("default_scheduler", "slurm")
    scheduler = config.get("schedulers", {}).get(scheduler_name)
    if not scheduler:
        raise ValueError(f"Unknown scheduler '{scheduler_name}'.")

    for job in state.get("jobs", []):
        job_id = job.get("scheduler_job_id")
        if not job_id:
            continue
        cmd = scheduler["status_cmd"].format(job_id=job_id)
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=package_dir)
        output = (result.stdout or "") + (result.stderr or "")
        print(f"[{job_id}] {job['id']}\n{output.strip()}\n")
    return 0


def cancel_jobs(args: argparse.Namespace) -> int:
    package_dir = Path(args.package).resolve()
    config_path = Path(args.config).resolve() if args.config else package_dir / "md_cli_config.json"
    config = ensure_config(config_path)
    state_path = package_dir / STATE_FILENAME
    if not state_path.exists():
        print("No job_state.json found. Submit jobs first.", file=sys.stderr)
        return 2

    state = load_json(state_path)
    scheduler_name = args.scheduler or state.get("scheduler") or config.get("default_scheduler", "slurm")
    scheduler = config.get("schedulers", {}).get(scheduler_name)
    if not scheduler:
        raise ValueError(f"Unknown scheduler '{scheduler_name}'.")

    for job in state.get("jobs", []):
        job_id = job.get("scheduler_job_id")
        if not job_id:
            continue
        cmd = scheduler["cancel_cmd"].format(job_id=job_id)
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=package_dir)
        output = (result.stdout or "") + (result.stderr or "")
        print(f"[{job_id}] {job['id']} -> {output.strip()}")
    return 0


def init_config(args: argparse.Namespace) -> int:
    config_path = Path(args.config).resolve() if args.config else Path("md_cli_config.json").resolve()
    if config_path.exists() and not args.force:
        print(f"{config_path} already exists. Use --force to overwrite.")
        return 1
    save_json(config_path, DEFAULT_CONFIG)
    print(f"Wrote default config to {config_path}")
    return 0


def _extract_job_id(output: str) -> str:
    match = re.search(r"\b(\d+)\b", output)
    return match.group(1) if match else ""


def main() -> int:
    parser = argparse.ArgumentParser(description="EnzyHTP manual MD CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Write a default scheduler config file")
    init_parser.add_argument("--config", help="Path to config file")
    init_parser.add_argument("--force", action="store_true", help="Overwrite config if it exists")
    init_parser.set_defaults(func=init_config)

    submit_parser = subparsers.add_parser("submit", help="Generate scripts and submit jobs")
    submit_parser.add_argument("--package", required=True, help="Path to the downloaded MD package")
    submit_parser.add_argument("--config", help="Path to scheduler config")
    submit_parser.add_argument("--scheduler", help="Scheduler name in config")
    submit_parser.add_argument("--no-submit", action="store_true", help="Only generate scripts, do not submit")
    submit_parser.set_defaults(func=submit_jobs)

    status_parser = subparsers.add_parser("status", help="Check status of submitted jobs")
    status_parser.add_argument("--package", required=True, help="Path to the downloaded MD package")
    status_parser.add_argument("--config", help="Path to scheduler config")
    status_parser.add_argument("--scheduler", help="Scheduler name in config")
    status_parser.set_defaults(func=status_jobs)

    cancel_parser = subparsers.add_parser("cancel", help="Cancel submitted jobs")
    cancel_parser.add_argument("--package", required=True, help="Path to the downloaded MD package")
    cancel_parser.add_argument("--config", help="Path to scheduler config")
    cancel_parser.add_argument("--scheduler", help="Scheduler name in config")
    cancel_parser.set_defaults(func=cancel_jobs)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
