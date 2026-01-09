#!/bin/bash
#SBATCH --job-name=mutexa_dev_tool
#SBATCH --account=yang_lab_int
#SBATCH --partition=interactive
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=12G
#SBATCH --time=1-00:00:00
#SBATCH --no-requeue
#SBATCH --export=NONE
#SBATCH --qos=mutant_int

ls -l /home/${slurm_user}
