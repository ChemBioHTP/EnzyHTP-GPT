#!/bin/bash
#SBATCH --job-name=md_qm
#SBATCH --account=yang_lab_csb
#SBATCH --partition=production
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=12G
#SBATCH --time=10-00:00:00
#SBATCH --no-requeue
#SBATCH --export=NONE

file_dir=$(dirname "$0")
echo "It's $(date +"%Y-%m-%d %T %Z") now. The bash script is in $file_dir directory."
echo "The PDB file is ${pdb_filename}"
ls -l $file_dir
