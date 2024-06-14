#!/bin/bash


# Filename
echo "The PDB file is ${pdb_filename}."


/sb/apps/amber22/bin/tleap -s -f scratch/tleap.in > scratch/tleap.out
/sb/apps/amber22/bin/add_pdb -i scratch/amber_parameterizer/amber_parm_missing_pdb_info.prmtop -p scratch/amber_parameterizer/amber_parm_ref_pdb.pdb -o scratch/amber_parameterizer/amber_parm_000006.prmtop