#!/bin/bash
#SBATCH --job-name=mutexa_gpt_${username}
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
export pdb_filename="${pdb_filename}"
export mutation_pattern="${mutation_pattern}"
export constraints_str="${constraints_str}"

echo "It's $(date +"%Y-%m-%d %T %Z") now. The bash script is in $file_dir directory."
echo "The PDB file is $pdb_filename"
ls -l $file_dir
cd $file_dir

python -u main_script.py
