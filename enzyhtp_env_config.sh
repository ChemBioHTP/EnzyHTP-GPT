#!/bin/bash

# This script is a part of first time installation.
# This script is to config environment variables of the current conda env.
# This script depends on the `develop-refactor` branch of EnzyHTP (https://github.com/ChemBioHTP/EnzyHTP/tree/develop_refactor).
# This script should be executed when `enzyhtp-gpt` env is activated.
# This script should be modified before execution.

# Reference: https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#saving-environment-variables


# Change the variable value to the path of your enzyhtp folder,
# making sure not to add a slash at the end.
enzyhtp_installation_path=~/bin/EnzyHTP

# Change the variable value to the name of your enzyhtp-gpt environment.
env_name=enzyhtp-gpt

# ========== Don't change anything below this line. ==========

cd $enzyhtp_installation_path
source dev-tools/conda-install --name $target_env_name
