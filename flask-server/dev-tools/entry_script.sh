#!/bin/bash

# source ~/.bashrc
# conda create -n enzy_htp python=3.9 -y
# conda activate enzy_htp
# cd ~/bin/EnzyHTP
# source dev-tools/conda-install

source ~/.bashrc
conda activate enzyhtp
python -c "import enzy_htp; print('EnzyHTP version:', enzy_htp.__version__)" > log 2>&1
