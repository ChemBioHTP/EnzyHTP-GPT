#!/usr/bin/bash

# This script is a part of first time installation.
# This script is to config environment variables of the current conda env.
# This script currently depends on the `develop_refactor` branch of EnzyHTP (https://github.com/ChemBioHTP/EnzyHTP/tree/develop_refactor).
# This script should be executed when `enzyhtp-gpt` env is activated.
# This script should be modified before execution.

# Store the initial working directory
initial_dir=$(pwd)

# Change the working directory to the parent directory of this script
cd "$(dirname "$0")"/..

# Default variable value to the path of your enzyhtp folder,
# making sure not to add a slash at the end.
enzyhtp_installation_path=~/bin/EnzyHTP

# Default environment name
target_env_name=enzyhtp-gpt

# Function to display help message
show_help() {
    echo "Usage: ${0##*/} [-n|--name ENV_NAME]"
    echo
    echo "Install EnzyHTP to your conda environment."
    echo
    echo "   --path        The path to EnzyHTP folder."
    echo "   -n, --name    Specify the name of the conda environment. Defaults to current environment."
    echo "   -h, --help    Display this help and exit."
}

# Define the options
OPTS=$(getopt -o hn: --long help,name,path: -- "$@")

# Exit if the options have not been correctly specified.
if [ $? != 0 ]; then exit 1; fi

# Extract options and their arguments into variables.
eval set -- "$OPTS"

while true; do
    case "$1" in
        -h|--help)
            show_help
            exit 0;;
        --path)
            enzyhtp_installation_path="$2"; shift 2;;
        -n|--name)
            target_env_name="$2"; shift 2;;
        --)
            shift; break;;
        *)
            break;;
    esac
done

# Reference: https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#saving-environment-variables

# ========== Don't change anything below this line. ==========

cd $enzyhtp_installation_path
source dev-tools/conda-install --name $target_env_name
