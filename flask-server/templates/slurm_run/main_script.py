#! python3
# -*- encoding: utf-8 -*-
'''
The main script of the Slurm Job. This script is currently for test use.

@File    :   main_script.py
@Created :   2024/06/21 16:18
@Author  :   Zhong, Yinjie
@Version :   1.0
@Contact :   yinjie.zhong@vanderbilt.edu
'''

# Here put the import lib.
from sys import argv
from time import sleep
from requests import post, put

from enzy_htp import interface, _LOGGER
from enzy_htp.structure import PDBParser
from enzy_htp.preparation import remove_solvent, remove_hydrogens, protonate_stru
from enzy_htp.mutation import assign_mutant, mutate_stru
from enzy_htp.geometry import equi_md_sampling
from enzy_htp.analysis import spi_metric
from enzy_htp.workflow.config import StatusCode

# TODO (Zhong): JWT is required for authentication.
experiment_id = "${experiment_id}"
STATUS_UPDATE_URL = f"https://enzyhtp.app.vanderbilt.edu/api/experiment/{experiment_id}"

pdb_filepath = argv[1]
ph = 7.4
mutation_pattern = "{WT}"

wt_stru = PDBParser().get_structure(pdb_filepath)
remove_solvent(stru=wt_stru)
remove_hydrogens(stru=wt_stru, polypeptide_only=True)
protonate_stru(stru=wt_stru, ph=ph, protonate_ligand=True)

mutants = assign_mutant(stru=wt_stru, pattern=mutation_pattern)
mutants_count = len(mutants)

# mutation
for i, mut in enumerate(mutants):
    mutant_result = []
    mutant_stru = mutate_stru(wt_stru, mut, engine="pymol")

    # Do something here.
    sleep(10.0)

    # Send a request to the backend of Web Application to update status and progress.
    response = put(STATUS_UPDATE_URL, data={"status": StatusCode.RUNNING, "progress": i/mutants_count})
