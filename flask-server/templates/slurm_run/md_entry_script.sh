#!/bin/bash
#SBATCH --job-name=mutexa_md_${username}
#SBATCH --account=yang_lab_csb
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
export access_token="${access_token}"
export experiment_id="${experiment_id}"
export pdb_filename="${pdb_filename}"
export metrics='${metrics}'
export mutation_pattern="${mutation_pattern}"
export constraints_str="${constraints_str}"
export md_length="${md_length}"

echo "It's $(date +"%Y-%m-%d %T %Z") now. The bash script is in $file_dir directory."
echo "The PDB file is $pdb_filename"
ls -l $file_dir
cd $file_dir

python -u "${file_dir}/md_main_script.py" 2>&1
