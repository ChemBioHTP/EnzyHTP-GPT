#!/bin/bash
#SBATCH --job-name=mutexa_mmpbsa_${username}
#SBATCH --account=yang_lab_csb
#SBATCH --partition=production
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=12G
#SBATCH --time=10-00:00:00
#SBATCH --no-requeue
#SBATCH --export=NONE

source ~/bin/enzyhtp_env.sh
source activate enzyhtp

export file_dir=$(dirname "$0")

export app_host="${app_host}"
export access_token="${access_token}"
export experiment_id="${experiment_id}"
export topology_filename="${topology_filename}"
export trajectory_filename="${trajectory_filename}"
export ligand_pattern="${ligand_pattern}"
export mutant="${mutant}"
export replica_id="${replica_id}"

python -u mmpbgbsa_main_script.py
