#!/usr/bin/bash
# This script is used to automatically configure the production environment for docker images.
# This script is not suitable for development environment configuration.

# If there is inconvenience in international Internet communication in your current location, 
# you can enable (uncomment) the following lines or modify them according to your own needs 
# to download dependent packages through the mirror address.
# conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
# conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/
# conda config --set show_channel_urls yes

# Install required packages on Ubuntu.
apt-get update
apt-get install -y git libgl1 libquadmath0

# Build the `enzyhtp-gpt` environment.
echo "Creating conda environment: enzyhtp-gpt."
conda env create -f environment.yml -y

echo "Successfully created conda environment, now activating..."
source activate enzyhtp-gpt

# Store the initial working directory
initial_dir=$(pwd)
enzyhtp_base_dir=/var/bin

# Clone `enzyhtp` repository to local.
mkdir -p $enzyhtp_base_dir
cd $enzyhtp_base_dir
# echo Cloning EnzyHTP to local...
# git clone https://github.com/ChemBioHTP/EnzyHTP.git

# Configure `EnzyHTP` to environment.
cd $initial_dir
echo Configuring EnzyHTP to environment...

# The execution of the following 2 command may take more than 10 minutes. (continue)
# cd "$enzyhtp_base_dir/EnzyHTP"
# source dev-tools/conda-install --name enzyhtp-gpt

# If you think it is too slow, you can comment them, and then enable the next line, before executing the `docker build`; (continue)

# but if there is any dependency package of `EnzyHTP` that have not been updated
# to the `environment.yml of the current directory, errors may be raised when you run the docker container.

# Switch back to the initial directory.
cd $initial_dir
