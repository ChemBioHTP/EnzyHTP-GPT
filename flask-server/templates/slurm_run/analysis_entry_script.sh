#!/bin/bash
#SBATCH --job-name=mutexa_analysis_${username}
#SBATCH --account=yang_lab
#SBATCH --partition=production
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=12G
#SBATCH --time=10-00:00:00
#SBATCH --no-requeue
#SBATCH --export=NONE

source ~/.bashrc
source ~/bin/enzyhtp_env.sh
conda activate enzy_htp

export USER="${slurm_user}"
export file_dir=$(cd "$(dirname "$0")/input";pwd)

export app_host="${app_host}"
export experiment_id="${experiment_id}"
export access_token="${access_token}"
export mutant="${mutant}"
export replica_id="${replica_id}"
export metrics='${metrics}'

export topology_filename="${topology_filename}"
export trajectory_filename="${trajectory_filename}"
export ref_pdb_filename="${ref_pdb_filename}"

python -u "${file_dir}/analysis_main_script.py" 2>&1
